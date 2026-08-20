# ENGR 1050 - Introduction to Scientific Computing

**Fall 2026**, University of Pennsylvania
Instructor: Prof. Nat Trask

## Course website

[https://natrask.github.io/engr1050-fall2026/](https://natrask.github.io/engr1050-fall2026/)

## Repository layout

- `index.html`, `styles.css` - the deployed Pages site
- `.nojekyll` - disables Jekyll on Pages
- `course.yml` - single source of truth for semester, schedule, homeworks, instructor block
- `scripts/` - local-only helpers
  - `update_schedule.py` - regenerates the schedule block in `index.html` from `course.yml`
  - `convert_lectures.py`, `convert_md.py` - render lecture notes markdown into HTML (KaTeX template)
- `NewMaterial/LectureNN_MmmDD/` - per-lecture folder with slides, notebook, notes
- `NewMaterial/_shared/` - images, data, Thonny scripts shared by notebooks
- `NewMaterial/Homeworks/HWN/` - homework LaTeX source and PDF
- `NewMaterial/Textbook/ChNN_slug/` - optional mini-textbook chapters

## Local development

```
python scripts/update_schedule.py        # rewrite schedule block in index.html from course.yml
python scripts/convert_lectures.py       # rebuild lecture notes HTML from markdown sources
```

Open `index.html` in a browser to preview.

## Publishing

GitHub Pages, deploy from `main` branch, root folder. The `.nojekyll` marker keeps Pages from running Jekyll.
