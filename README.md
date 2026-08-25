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
  - `build_newmaterial.py` - populates `NewMaterial/` from `OldMaterial/`, driven by `course.yml`
  - `convert_lectures.py`, `convert_md.py` - render lecture notes markdown into HTML (KaTeX template)
- `NewMaterial/` - the live content stream. **Everything `index.html` links to lives here.**
  - `LectureNN_MmmDD/` - per-lecture folder with slides, notebook, notes
  - `_shared/` - images, data, Thonny scripts shared by notebooks
  - `Homeworks/HWN/` - homework LaTeX source and PDF
  - `Textbook/ChNN_slug/` - optional mini-textbook chapters
- `OldMaterial/` - local-only archive of last semester's content (gitignored, so it
  never reaches GitHub). Never linked from the site; copy what you need forward into
  `NewMaterial/` instead of linking into it. Keep a local copy if you plan to re-run
  `build_newmaterial.py`.

## Local development

```
python scripts/build_newmaterial.py      # copy OldMaterial -> NewMaterial for every scheduled lecture
python scripts/update_schedule.py        # rewrite schedule block in index.html from course.yml
python scripts/convert_lectures.py       # rebuild lecture notes HTML from markdown sources
```

`build_newmaterial.py` is idempotent and never overwrites an existing `NewMaterial`
file unless you pass `--force`, so it is safe to re-run after adding a lecture to
`course.yml`. Lectures with no prior material get an empty folder with a `.gitkeep`.

Open `index.html` in a browser to preview.

## Publishing

GitHub Pages, deploy from `main` branch, root folder. The `.nojekyll` marker keeps Pages from running Jekyll.
