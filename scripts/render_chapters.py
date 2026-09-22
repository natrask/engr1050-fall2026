#!/usr/bin/env python3
"""Convert each NewMaterial/Textbook/Ch*/chapter.md to chapter.html.

Tiny KaTeX HTML wrapper styled to match the lecture HTML.
Run from any directory:
    python scripts/render_chapters.py
"""
from __future__ import annotations

import html as html_mod
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
COURSE_YML = REPO_ROOT / "course.yml"
TEXTBOOK_DIR = REPO_ROOT / "NewMaterial" / "Textbook"

TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} - ENGR 1050</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"></script>
<style>
 body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        line-height: 1.6; color: #333; max-width: 900px; margin: 0 auto; padding: 20px; }}
 h1 {{ color: #011F5B; border-bottom: 3px solid #990000; padding-bottom: 10px; margin-top: 30px; }}
 h2 {{ color: #011F5B; margin-top: 30px; border-bottom: 2px solid #e0e0e0; padding-bottom: 5px; }}
 h3 {{ color: #011F5B; margin-top: 20px; }}
 p {{ text-align: left; margin-bottom: 15px; }}
 code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; font-family: ui-monospace, Menlo, Consolas, monospace; }}
 pre {{ background: #f4f4f4; padding: 12px; border-radius: 6px; overflow-x: auto; }}
 blockquote {{ border-left: 4px solid #82AFD3; padding: 4px 12px; background: #f8f9fa; margin: 12px 0; }}
 a {{ color: #4a90e2; }} a:hover {{ color: #990000; }}
 pre code {{ background: none; padding: 0; }}
 li {{ margin-bottom: 6px; }}
 li p {{ margin: 6px 0; }}
 li pre {{ margin: 8px 0; }}
 .nav {{ font-size: 0.9rem; margin-bottom: 1rem; display: flex; flex-wrap: wrap; gap: 0.5rem; align-items: center; }}
 .nav a.button {{ background: #6c757d; color: #fff; padding: 0.3rem 0.8rem; border-radius: 4px; text-decoration: none; font-weight: 600; }}
 .nav a.button:hover {{ background: #990000; color: #fff; }}
</style>
</head>
<body>
<p class="nav"><a href="../../../index.html#extras">&larr; Back to Extras</a>
<a class="button" href="{colab}" target="_blank">Open in Colab</a></p>
{body}
<script>
document.addEventListener("DOMContentLoaded", function() {{
  if (window.renderMathInElement) {{
    renderMathInElement(document.body, {{
      delimiters: [
        {{left: "$$", right: "$$", display: true}},
        {{left: "$", right: "$", display: false}},
      ],
    }});
  }}
}});
</script>
</body>
</html>
'''


_CODE_SPAN = re.compile(r'(`+)(.+?)\1')
_BOLD = re.compile(r'\*\*(.+?)\*\*')
_URL = re.compile(r'(https?://[^\s<]+[^\s<.,;:!?)])')
_LIST_MARKER = re.compile(r'^(\s*)([-*]|\d+\.)\s+')


def inline(text: str) -> str:
    """Escape, then render `code` spans, **bold**, and bare URLs.

    Bold and URLs are only applied outside code spans, so `2 ** 10` and
    `**` survive as code rather than turning into emphasis.
    """
    text = html_mod.escape(text)
    out = []
    pos = 0
    for m in _CODE_SPAN.finditer(text):
        out.append(_inline_plain(text[pos:m.start()]))
        out.append('<code>' + m.group(2).strip() + '</code>')
        pos = m.end()
    out.append(_inline_plain(text[pos:]))
    return ''.join(out)


def _inline_plain(text: str) -> str:
    text = _BOLD.sub(r'<strong>\1</strong>', text)
    return _URL.sub(r'<a href="\1">\1</a>', text)


def _is_fence(line: str) -> bool:
    return line.lstrip().startswith('```')


def md_to_html(md: str) -> str:
    """Tiny markdown subset: headings, paragraphs, lists, fenced code, blockquotes.

    List items may carry indented continuation lines, including fenced code
    blocks. Those render as a real <pre> inside the <li>; a fence is never
    flattened into paragraph text, where it reads like a shell command.
    """
    return '\n'.join(_blocks(md.splitlines()))


def _blocks(lines):
    out = []
    para = []
    i = 0

    def flush():
        if para:
            out.append('<p>' + inline(' '.join(s.strip() for s in para)) + '</p>')
            para.clear()

    while i < len(lines):
        line = lines[i]

        if _is_fence(line):
            flush()
            indent = len(line) - len(line.lstrip())
            i += 1
            code = []
            while i < len(lines) and not _is_fence(lines[i]):
                raw = lines[i]
                # drop the fence's own indentation, keep the code's
                code.append(raw[indent:] if raw[:indent].strip() == '' else raw.lstrip())
                i += 1
            i += 1  # closing fence
            out.append('<pre><code>' + html_mod.escape('\n'.join(code)) + '</code></pre>')
            continue

        m = re.match(r'^(#+)\s+(.*)$', line)
        if m:
            flush()
            level = min(len(m.group(1)), 6)
            out.append(f'<h{level}>{inline(m.group(2))}</h{level}>')
            i += 1
            continue

        if line.startswith('> '):
            flush()
            quote = []
            while i < len(lines) and lines[i].startswith('>'):
                quote.append(lines[i][1:].strip())
                i += 1
            out.append('<blockquote>' + inline(' '.join(quote)) + '</blockquote>')
            continue

        lm = _LIST_MARKER.match(line)
        if lm and lm.group(1) == '':
            flush()
            ordered = lm.group(2) not in '-*'
            tag = 'ol' if ordered else 'ul'
            out.append(f'<{tag}>')
            while i < len(lines):
                lm = _LIST_MARKER.match(lines[i])
                if not (lm and lm.group(1) == '' and (lm.group(2) not in '-*') == ordered):
                    break
                width = lm.end()
                item = [lines[i][width:]]
                i += 1
                in_fence = False
                while i < len(lines):
                    nxt = lines[i]
                    if in_fence:
                        pass
                    elif nxt.strip() == '':
                        # a blank line stays in the item only if indented text follows
                        j = i
                        while j < len(lines) and lines[j].strip() == '':
                            j += 1
                        if j >= len(lines) or not lines[j].startswith('  '):
                            break
                    elif not nxt.startswith('  '):
                        break
                    if _is_fence(nxt):
                        in_fence = not in_fence
                    strip = min(width, len(nxt) - len(nxt.lstrip()))
                    item.append(nxt[strip:])
                    i += 1
                inner = _blocks(item)
                if len(inner) == 1 and inner[0].startswith('<p>') and inner[0].endswith('</p>'):
                    inner = [inner[0][3:-4]]
                out.append('<li>' + '\n'.join(inner) + '</li>')
                # skip blank lines between items of the same list
                j = i
                while j < len(lines) and lines[j].strip() == '':
                    j += 1
                nm = _LIST_MARKER.match(lines[j]) if j < len(lines) else None
                if nm and nm.group(1) == '' and (nm.group(2) not in '-*') == ordered:
                    i = j
            out.append(f'</{tag}>')
            continue

        if line.strip() == '':
            flush()
            i += 1
            continue

        para.append(line)
        i += 1

    flush()
    return out


def github_repo() -> str:
    """Repo slug for Colab links; course.yml is the single source of truth."""
    import yaml
    course = yaml.safe_load(COURSE_YML.read_text(encoding="utf-8"))
    return course["semester"]["github_repo"]


def main():
    if not TEXTBOOK_DIR.is_dir():
        sys.exit(f"Textbook directory not found: {TEXTBOOK_DIR}")
    repo = github_repo()
    colab_base = f"https://colab.research.google.com/github/{repo}/blob/main/NewMaterial/Textbook"
    n = 0
    for sub in sorted(TEXTBOOK_DIR.iterdir()):
        if not sub.is_dir():
            continue
        md_path = sub / "chapter.md"
        html_path = sub / "chapter.html"
        if not md_path.exists():
            print(f"  skip {sub.name} (no chapter.md)")
            continue
        md = md_path.read_text(encoding="utf-8")
        first = next((l for l in md.splitlines() if l.startswith('# ')), '# Chapter')
        title = first.lstrip('# ').strip()
        body = md_to_html(md)
        html_path.write_text(
            TEMPLATE.format(title=html_mod.escape(title), body=body,
                            colab=f"{colab_base}/{sub.name}/chapter.ipynb"),
            encoding="utf-8",
        )
        size = html_path.stat().st_size
        print(f"  wrote {sub.name}/chapter.html ({size} bytes)")
        n += 1
    print(f"Rendered {n} chapter file(s) under {TEXTBOOK_DIR}")


if __name__ == "__main__":
    main()
