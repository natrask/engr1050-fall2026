#!/usr/bin/env python3
"""Pre-push vetting for indexing / numbering errors.

The Fall 2025 -> 2026 migration renumbered every lecture by one and left the
numbering inside the content pointing at the old sequence. That class of bug is
silent -- the site builds fine and every link resolves, but a notebook opens
with the wrong lecture number. These checks catch it mechanically.

Exit code 0 = clean, 1 = something to look at.
"""
from __future__ import annotations
import datetime, json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import yaml
import update_schedule as us

REPO = Path(__file__).resolve().parent.parent
NEW = REPO / "NewMaterial"
DATED = re.compile(r"Lecture\d{2}_[A-Z][a-z]{2}\d{2}")
STALE = {
    "PIMILab/ENGR1050": "last year's GitHub repo",
    "1881448": "Fall 2025 Canvas course id",
    "84852": "Fall 2025 Ed Discussion id",
}
# these intentionally document the Fall 2025 archive
STALE_EXEMPT = {"NewMaterial/_shared/README.md"}
problems: list[str] = []


def fail(msg):
    problems.append(msg)


def main():
    course = yaml.safe_load((REPO / "course.yml").read_text(encoding="utf-8"))
    schedule = course["schedule"]
    lectures = [e for e in schedule if e.get("num")]

    # 1. folder names carry no date -- dates belong in course.yml only
    for e in lectures:
        f = e.get("folder")
        if f and DATED.search(f):
            fail(f"course.yml: folder '{f}' encodes a date; use Lecture{e['num']:02d}")

    # 2. folder number matches the lecture number
    for e in lectures:
        f = e.get("folder")
        if f and (m := re.fullmatch(r"Lecture(\d{2})", f)) and int(m.group(1)) != e["num"]:
            fail(f"course.yml: lecture {e['num']} points at folder {f}")

    # 3. every referenced file exists
    for e in lectures:
        if not (f := e.get("folder")):
            continue
        slides = e.get("slides") or []
        for fn in ([slides] if isinstance(slides, str) else slides):
            if not (NEW / f / fn).exists():
                fail(f"missing file: NewMaterial/{f}/{fn}")
        for key in ("notebook", "notes"):
            if (fn := e.get(key)) and not (NEW / f / fn).exists():
                fail(f"missing file: NewMaterial/{f}/{fn}")
    for hw in course.get("homeworks", []):
        if (pdf := hw.get("pdf")) and not (REPO / pdf).exists():
            fail(f"missing file: {pdf}")
    for ch in course.get("textbook", {}).get("chapters", []):
        p = f"NewMaterial/Textbook/Ch{ch['num']:02d}_{ch['slug']}/chapter.html"
        if not (REPO / p).exists():
            fail(f"missing file: {p}")

    # 4. notebook filename and H1 title agree with the lecture number
    for nb_path in sorted(NEW.glob("Lecture*/lec*.ipynb")):
        folder_num = int(re.fullmatch(r"Lecture(\d{2})", nb_path.parent.name).group(1))
        file_num = int(re.fullmatch(r"lec(\d+)\.ipynb", nb_path.name).group(1))
        if file_num != folder_num:
            fail(f"{nb_path.parent.name}/{nb_path.name}: filename number != folder number")
        nb = json.loads(nb_path.read_text(encoding="utf-8"))
        for c in nb["cells"]:
            if c["cell_type"] != "markdown":
                continue
            hit = next((re.match(r"#\s+Lecture\s+(\d+)\s*:", l) for l in c["source"]
                        if re.match(r"#\s+Lecture\s+(\d+)\s*:", l)), None)
            if hit:
                if int(hit.group(1)) != folder_num:
                    fail(f"{nb_path.parent.name}/{nb_path.name}: title says "
                         f"'Lecture {hit.group(1)}' but lives in Lecture{folder_num:02d}")
                break

    # 5. schedule dates are sane
    seen = {}
    for e in schedule:
        d = e["date"]
        if isinstance(d, str):
            d = datetime.date.fromisoformat(d)
        if d.weekday() not in (0, 2):
            fail(f"schedule: {d} is a {d.strftime('%A')}, not a Monday or Wednesday")
        if d in seen:
            fail(f"schedule: two entries share {d}")
        seen[d] = e
    nums = [e["num"] for e in lectures]
    if nums != sorted(nums):
        fail("schedule: lecture numbers are out of order")

    # 6. index.html matches what course.yml renders
    html = (REPO / "index.html").read_text(encoding="utf-8")
    for start, end, render in ((us.SCHED_START, us.SCHED_END, us.render_schedule),
                               (us.HW_START, us.HW_END, us.render_homeworks),
                               (us.EXTRAS_START, us.EXTRAS_END, us.render_extras)):
        m = re.search(re.escape(start) + r"\n(.*?)\n\s*" + re.escape(end), html, re.DOTALL)
        if not m:
            fail(f"index.html: {start} block not found")
        elif m.group(1).strip() != render(course).strip():
            fail(f"index.html: {start} block is stale -- run update_schedule.py")

    # 7. no leftover references to last semester
    for f in [REPO / "index.html", *NEW.rglob("*.ipynb"), *NEW.rglob("*.md")]:
        rel = f.relative_to(REPO).as_posix()
        if rel in STALE_EXEMPT:
            continue
        text = f.read_text(encoding="utf-8", errors="ignore")
        for needle, what in STALE.items():
            if needle in text:
                fail(f"{f.relative_to(REPO).as_posix()}: still references {what} ({needle})")
        if DATED.search(text):
            fail(f"{f.relative_to(REPO).as_posix()}: references a dated lecture folder")

    if problems:
        print(f"{len(problems)} problem(s) found:\n")
        for p in problems:
            print("  x " + p)
        return 1
    print(f"clean: {len(lectures)} lectures, all links resolve, numbering consistent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
