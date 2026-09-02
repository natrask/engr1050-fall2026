#!/usr/bin/env python3
"""Regenerate schedule, homeworks, and extras blocks in index.html from course.yml."""
from __future__ import annotations
import datetime, re, sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.stderr.write("PyYAML required: pip install pyyaml\n")
    sys.exit(1)

REPO_ROOT = Path(__file__).resolve().parent.parent
COURSE_YML = REPO_ROOT / "course.yml"
INDEX_HTML = REPO_ROOT / "index.html"

SCHED_START, SCHED_END = "<!-- SCHEDULE:START -->", "<!-- SCHEDULE:END -->"
HW_START, HW_END = "<!-- HOMEWORKS:START -->", "<!-- HOMEWORKS:END -->"
EXTRAS_START, EXTRAS_END = "<!-- EXTRAS:START -->", "<!-- EXTRAS:END -->"


def fmt_date(d):
    if isinstance(d, str):
        d = datetime.date.fromisoformat(d)
    return d.strftime("%b %d").replace(" 0", " ")


def colab_url(repo, path):
    return f"https://colab.research.google.com/github/{repo}/blob/main/{path}"


SLIDE_LABELS = {".pdf": "Slides (PDF)", ".pptx": "Slides (PPT)", ".ppt": "Slides (PPT)"}


def slide_label(filename):
    return SLIDE_LABELS.get(Path(filename).suffix.lower(), "Slides")


def render_entry(entry, repo):
    date_str = fmt_date(entry["date"])
    topic = entry["topic"]
    kind = entry.get("kind")
    folder = entry.get("folder")
    num = entry.get("num")
    # exams and no-class days carry no lecture number
    title_html = f"<h3>{topic}</h3>" if num is None or kind == "exam" else f"<h3>Lecture {num}: {topic}</h3>"
    resources = []
    if folder:
        base = f"NewMaterial/{folder}"
        slides = entry.get("slides")
        if slides:
            for fn in ([slides] if isinstance(slides, str) else slides):
                resources.append(f'<li><a href="{base}/{fn}">{slide_label(fn)}</a></li>')
        notebook = entry.get("notebook")
        if notebook:
            resources.append(f'<li><a href="{base}/{notebook}">Notebook</a></li>')
            resources.append(f'<li><a href="{colab_url(repo, base + "/" + notebook)}" target="_blank">Open in Colab</a></li>')
        notes = entry.get("notes")
        if notes:
            resources.append(f'<li><a href="{base}/{notes}">Lecture notes</a></li>')
    exercise = entry.get("exercise")
    if exercise:
        resources.append(f'<li><a href="{exercise}" target="_blank">Exercise submission</a></li>')
    for link in entry.get("links", []):
        resources.append(f'<li><a href="{link["url"]}" target="_blank">{link["label"]}</a></li>')
    rb = ""
    if resources:
        rb = '            <ul class="resources">\n' + "\n".join(f"                {r}" for r in resources) + "\n            </ul>"
        if not entry.get("visible", False):
            rb = "            <!-- resources hidden until lecture is released; uncomment to release\n" + rb + "\n            -->"
    parts = ['        <div class="lecture-item">',
             f'          <div class="lecture-date">{date_str}</div>',
             '          <div class="lecture-content">',
             f'            {title_html}']
    if rb:
        parts.append(rb)
    parts.append('          </div>')
    parts.append('        </div>')
    return "\n".join(parts)


def render_schedule(course):
    repo = course["semester"].get("github_repo", "")
    return "\n".join(render_entry(e, repo) for e in course["schedule"])


def render_homeworks(course):
    cards = []
    for hw in course.get("homeworks", []):
        num = hw["num"]
        title = hw.get("title", f"Homework {num}")
        pdf = hw.get("pdf")
        due_str = fmt_date(hw["due"]) if hw.get("due") else "TBD"
        # an unpublished homework shows as "(coming)" even when its PDF exists
        link = f'<a href="{pdf}">PDF</a>' if pdf and hw.get("visible") else "(coming)"
        cards.append("\n".join([
            '        <div class="lecture-item">',
            f'          <div class="lecture-date">Due {due_str}</div>',
            '          <div class="lecture-content">',
            f'            <h3>HW {num}: {title}</h3>',
            '            <ul class="resources">',
            f'                <li>{link}</li>',
            '            </ul>',
            '          </div>',
            '        </div>',
        ]))
    return "\n".join(cards)


def render_extras(course):
    repo = course["semester"].get("github_repo", "")
    cards = []
    for site in course.get("external_practice", []):
        cards.append("\n".join([
            '        <div class="lecture-item">',
            '          <div class="lecture-date">Practice</div>',
            '          <div class="lecture-content">',
            f'            <h3>{site["name"]}</h3>',
            f'            <p>{site["description"].strip()}</p>',
            '            <ul class="resources">',
            f'                <li><a href="{site["url"]}" target="_blank">{site.get("label", site["url"])}</a></li>',
            '            </ul>',
            '          </div>',
            '        </div>',
        ]))
    for ch in course.get("textbook", {}).get("chapters", []):
        num, slug, title = ch["num"], ch["slug"], ch["title"]
        base = f"NewMaterial/Textbook/Ch{num:02d}_{slug}"
        colab = colab_url(repo, f"{base}/chapter.ipynb")
        cards.append("\n".join([
            '        <div class="lecture-item">',
            f'          <div class="lecture-date">Ch {num}</div>',
            '          <div class="lecture-content">',
            f'            <h3>{title}</h3>',
            '            <ul class="resources">',
            f'                <li><a href="{base}/chapter.html">Chapter</a></li>',
            f'                <li><a href="{colab}" target="_blank">Open in Colab</a></li>',
            '            </ul>',
            '          </div>',
            '        </div>',
        ]))
    return "\n".join(cards)


def replace_block(html, start, end, inner):
    pat = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    if not pat.search(html):
        raise SystemExit(f"Sentinels {start}/{end} missing in index.html")
    return pat.sub(f"{start}\n{inner}\n        {end}", html)


def main():
    course = yaml.safe_load(COURSE_YML.read_text(encoding="utf-8"))
    html = INDEX_HTML.read_text(encoding="utf-8")
    html = replace_block(html, SCHED_START, SCHED_END, render_schedule(course))
    html = replace_block(html, HW_START, HW_END, render_homeworks(course))
    html = replace_block(html, EXTRAS_START, EXTRAS_END, render_extras(course))
    INDEX_HTML.write_text(html, encoding="utf-8")
    print(f"Wrote schedule={len(course['schedule'])}, "
          f"homeworks={len(course.get('homeworks', []))}, "
          f"chapters={len(course.get('textbook', {}).get('chapters', []))}")


if __name__ == "__main__":
    main()
