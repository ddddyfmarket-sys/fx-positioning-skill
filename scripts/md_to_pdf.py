#!/usr/bin/env python3
"""Render an FX positioning note (Markdown) into a styled, one-page PDF.

Converts Markdown -> styled HTML -> PDF. The HTML is laid out to read like a
sell-side desk note (navy headings, section rules, monospace code spans).

Rendering backend, tried in order until one works:
  1. headless Chrome / Chromium / Edge  (best fidelity, usually present on macOS)
  2. weasyprint                          (pip install weasyprint)
  3. wkhtmltopdf                         (brew install wkhtmltopdf)

Usage:
    python3 md_to_pdf.py [note.md] [-o out.pdf]

If the input path is omitted, the newest fx_positioning_note_*.md in the current
directory is used. If -o is omitted, the PDF is written next to the .md with the
same stem.
"""
import argparse
import glob
import os
import shutil
import subprocess
import sys
import tempfile

CSS = """
@page { size: A4; margin: 16mm 16mm; }
body { font-family: -apple-system, "Helvetica Neue", Arial, sans-serif;
  font-size: 10.3px; line-height: 1.42; color: #1a1a1a; max-width: 100%; }
h1 { font-size: 19px; margin: 0 0 2px; color: #0b1f3a; }
h1 + p em { color: #555; font-size: 10px; }
h2 { font-size: 12.5px; margin: 14px 0 5px; padding-bottom: 2px;
  border-bottom: 1px solid #c9d3df; color: #0b1f3a; }
p { margin: 5px 0; }
ul { margin: 4px 0; padding-left: 18px; }
li { margin: 3px 0; }
strong { color: #0b1f3a; }
code { background: #eef2f7; padding: 1px 4px; border-radius: 3px;
  font-family: "SF Mono", Menlo, monospace; font-size: 9px; color: #334; }
hr { border: none; border-top: 1px solid #ccc; margin: 14px 0 6px; }
hr + p em { color: #777; font-size: 9px; }
table { border-collapse: collapse; margin: 6px 0; font-size: 9.5px; }
th, td { border: 1px solid #c9d3df; padding: 3px 6px; text-align: left; }
th { background: #eef2f7; color: #0b1f3a; }
"""

# Common Chrome/Chromium/Edge locations across platforms.
_CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
]
_CHROME_NAMES = [
    "google-chrome", "google-chrome-stable", "chromium", "chromium-browser",
    "chrome", "microsoft-edge", "brave-browser",
]


def find_chrome():
    for path in _CHROME_CANDIDATES:
        if os.path.exists(path):
            return path
    for name in _CHROME_NAMES:
        found = shutil.which(name)
        if found:
            return found
    return None


def md_to_html(md_text):
    """Markdown -> full HTML document. Uses the `markdown` lib, with a tiny
    inline fallback so the script still produces a (plainer) PDF if it's absent."""
    try:
        import markdown  # type: ignore
        body = markdown.markdown(md_text, extensions=["extra", "sane_lists"])
    except ImportError:
        import html as _html
        import re
        # Minimal fallback: headings, bold/italic/code, hr, bullet lists.
        out, in_list = [], False
        for raw in md_text.splitlines():
            line = _html.escape(raw)
            line = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", line)
            line = re.sub(r"\*(.+?)\*", r"<em>\1</em>", line)
            line = re.sub(r"`(.+?)`", r"<code>\1</code>", line)
            if line.startswith("## "):
                if in_list: out.append("</ul>"); in_list = False
                out.append(f"<h2>{line[3:]}</h2>")
            elif line.startswith("# "):
                if in_list: out.append("</ul>"); in_list = False
                out.append(f"<h1>{line[2:]}</h1>")
            elif line.strip() == "---":
                if in_list: out.append("</ul>"); in_list = False
                out.append("<hr>")
            elif line.startswith("- "):
                if not in_list: out.append("<ul>"); in_list = True
                out.append(f"<li>{line[2:]}</li>")
            elif line.strip():
                if in_list: out.append("</ul>"); in_list = False
                out.append(f"<p>{line}</p>")
        if in_list: out.append("</ul>")
        body = "\n".join(out)
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>{CSS}</style></head><body>{body}</body></html>"""


def render_pdf(html, out_pdf):
    """Write `html` to a temp file and render it to `out_pdf`. Returns the
    backend name used, or raises RuntimeError if none is available."""
    fd, html_path = tempfile.mkstemp(suffix=".html")
    os.close(fd)
    with open(html_path, "w") as fh:
        fh.write(html)
    try:
        chrome = find_chrome()
        if chrome:
            subprocess.run(
                [chrome, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                 f"--print-to-pdf={out_pdf}", html_path],
                check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )
            return "headless Chrome"
        try:
            from weasyprint import HTML  # type: ignore
            HTML(string=html).write_pdf(out_pdf)
            return "weasyprint"
        except ImportError:
            pass
        if shutil.which("wkhtmltopdf"):
            subprocess.run(["wkhtmltopdf", "--quiet", html_path, out_pdf], check=True)
            return "wkhtmltopdf"
        raise RuntimeError(
            "No PDF backend found. Install one of: Google Chrome/Chromium, "
            "`pip install weasyprint`, or `brew install wkhtmltopdf`."
        )
    finally:
        os.remove(html_path)


def main():
    ap = argparse.ArgumentParser(description="Render an FX positioning note (.md) to a styled PDF.")
    ap.add_argument("input", nargs="?", help="Markdown note (default: newest fx_positioning_note_*.md in CWD).")
    ap.add_argument("-o", "--output", help="Output PDF path (default: alongside the .md).")
    args = ap.parse_args()

    md_path = args.input
    if not md_path:
        notes = sorted(glob.glob("fx_positioning_note_*.md"))
        if not notes:
            sys.exit("No input given and no fx_positioning_note_*.md found in this directory.")
        md_path = notes[-1]
    if not os.path.exists(md_path):
        sys.exit(f"Input not found: {md_path}")

    out_pdf = args.output or os.path.splitext(md_path)[0] + ".pdf"
    out_pdf = os.path.abspath(out_pdf)

    with open(md_path) as fh:
        html = md_to_html(fh.read())
    backend = render_pdf(html, out_pdf)
    size = os.path.getsize(out_pdf)
    print(f"Wrote {out_pdf} ({size:,} bytes) via {backend}.")


if __name__ == "__main__":
    main()
