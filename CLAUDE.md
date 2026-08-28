# ENGR 1050 course site - working notes

Static GitHub Pages site. `course.yml` is the single source of truth; `index.html`
is generated from it between sentinel comments. Never hand-edit inside
`<!-- SCHEDULE:START -->`, `<!-- HOMEWORKS:START -->`, or `<!-- EXTRAS:START -->` --
edit `course.yml` and re-run `scripts/update_schedule.py`.

## Vet before every push

Course material is adapted year over year, and the numbering is the fragile part.
The Fall 2025 -> 2026 migration shifted every lecture back by one and left the
numbering *inside* the content pointing at the old sequence: notebooks opened with
the wrong lecture number, slide covers disagreed with the schedule, and prose said
"in Lecture 4 we showed..." about material that had become Lecture 3. None of this
breaks the build. Every link resolves. It is only visible by reading.

So: **before any push, run the checker and resolve everything it reports.**

```
python scripts/check_consistency.py
```

It verifies that lecture numbers agree across `course.yml`, folder names, notebook
filenames, and notebook H1 titles; that every file referenced by `course.yml`
exists; that schedule dates are Mondays/Wednesdays with no duplicates; that
`index.html` is in sync with `course.yml`; and that no prior-semester Canvas
course, Ed Discussion, or GitHub repo references survive. Exit 0 means clean.

### What the checker cannot see

These need a human read. Nat revises decks before pushing and catches most of them
there, but flag anything noticed in passing:

- **Slide deck covers and footers.** The lecture number is baked into the PDF.
  `MIGRATION_NOTES.md` tracks which decks still show the old number and need
  recompiling from `.tex` or re-exporting from PowerPoint.
- **Prose cross-references inside notebooks and notes.** "In Lecture 4 we showed..."
  is a real pointer whose target may have shifted. A blind decrement breaks the
  ones that are already correct, so read them in context.
- **Whether a lecture's content actually matches its slot.** Renumbering moves
  labels, not meaning.

## Conventions

- **Folder names carry no dates.** `NewMaterial/LectureNN/`, numbered by sequence
  only. The date lives in `course.yml` and nowhere else, so folders carry forward
  to the next offering without renaming. The checker rejects a dated folder name.
- **Slides ship as both PPT and PDF** where a PowerPoint source exists. List both
  under `slides:` in `course.yml` (PPT first); they render as "Slides (PPT)" and
  "Slides (PDF)". Nat downloads the PPT onto the lecture-room machine; the PDF is
  what students view in the browser. Regenerate stale PDFs with
  `powershell -File scripts/pptx_to_pdf.ps1`.
- **Lectures are released one at a time.** `visible: true` on a schedule entry
  publishes its resource links; without it they render inside an HTML comment.
  Unfreeze a lecture when it is taught, not before.
- **`OldMaterial/` is a local, gitignored archive** of the previous offering. It is
  never linked from the site. Copy material forward into `NewMaterial/` rather than
  linking into it, so there is a single stream of content per lecture.

## Layout

```
course.yml                  semester, schedule, homeworks, textbook chapters
index.html, styles.css      the deployed site
NewMaterial/LectureNN/      slides, notebook, notes for one lecture
NewMaterial/Homeworks/HWN/  homework LaTeX source and PDF
NewMaterial/Textbook/       mini-textbook chapters
scripts/                    local-only helpers, not deployed
```
