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
  - `pptx_to_pdf.ps1` - exports every `.pptx` under `NewMaterial/` to a sibling `.pdf`
  - `convert_lectures.py`, `convert_md.py` - render lecture notes markdown into HTML (KaTeX template)
- `NewMaterial/` - the live content stream. **Everything `index.html` links to lives here.**
  - `LectureNN/` - per-lecture folder with slides, notebook, notes. Named by
    lecture sequence only - dates live in `course.yml`, so the same folder
    carries forward to next semester without renaming.
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
powershell -File scripts/pptx_to_pdf.ps1 # export .pptx decks to sibling .pdf files
python scripts/update_schedule.py        # rewrite schedule block in index.html from course.yml
python scripts/convert_lectures.py       # rebuild lecture notes HTML from markdown sources
```

### Slides convention

Every lecture built from PowerPoint links **both** copies of its deck: the `.pptx`,
which Nat downloads onto the lecture-room machine, and a `.pdf`, which students can
view in the browser without downloading a large file. List both under `slides:` in
`course.yml` and `update_schedule.py` labels them "Slides (PPT)" and "Slides (PDF)"
in the order given:

```yaml
  - num: 1
    slides:
      - Lecture_01.pptx
      - Lecture_01.pdf
```

A single filename still works for lectures built from Beamer `.tex`, which are
PDF-only. After editing a deck, re-run `pptx_to_pdf.ps1` to refresh the PDF (it
skips decks whose PDF is already newer), then `update_schedule.py`.

`build_newmaterial.py` is idempotent and never overwrites an existing `NewMaterial`
file unless you pass `--force`, so it is safe to re-run after adding a lecture to
`course.yml`. Lectures with no prior material get an empty folder with a `.gitkeep`.

Open `index.html` in a browser to preview.

## Publishing

GitHub Pages, deploy from `main` branch, root folder. The `.nojekyll` marker keeps Pages from running Jekyll.
