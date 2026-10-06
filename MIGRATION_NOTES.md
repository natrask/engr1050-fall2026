# Migration notes (Fall 2025 -> Fall 2026)

Generated during the bulk move and renumber pass. Items below need Nat's review.

## Files that were not migrated to the new repo

| Path in Fall 2025 repo                                 | Disposition           | Reason                                                  |
|--------------------------------------------------------|-----------------------|---------------------------------------------------------|
| `slides/lecture21/`                                    | dropped               | Orphan Beamer subfolder, not linked from any schedule slot |
| `virtualLectures/`                                     | dropped               | 2023 audio/video, unrelated to ENGR 1050                |
| `texput.log`                                            | dropped               | Stray LaTeX log at repo root                            |
| `.vscode/`                                             | dropped               | Editor settings, not deployed content                   |
| `grades/`                                              | move to private repo  | Contains anonymized but identifiable grade data         |
| `exams/`                                               | stays gitignored      | Already excluded from public repo                       |
| `notebooks/Data/SecretSquirrel/`                       | dropped               | Folder name implies non-public                          |
| `notebooks/FastfoodData/CHAT_TRANSCRIPT.md`            | dropped               | Verbatim instructor / AI chat history                   |
| `notebooks/lec02.ipynb`                                | dropped               | Empty stub for Labor Day in 2025 schedule               |
| `materials/lec02.md`                                   | dropped               | Same                                                    |
| `materials/lec10.md`, `lec11.md`, `lec15.md`, `lec17.md`-`lec26.md`, `lec28.md`, `lec29.md` | dropped | All "Topic TBD" stubs from 2025; will be authored fresh |

## Cloud-only files that need a sync sweep before publishing

The session sandbox did not have on-disk copies of the following OneDrive-virtualized files. Before publishing, open Windows Explorer to `C:\Users\nattr\OneDrive\Desktop\GitRepos\ENGR1050`, right-click the folder, choose "Always keep on this device", then run the copy block in `NewMaterial/_shared/README.md`.

- Slide PPTX originals for Lectures 1 and 7 (only the PDFs would not download as binary): currently the new repo has `Lecture01/Lecture_01.pdf` was not produced because no PDF existed in 2025. Same for the in-class exercise lecture (was Lec 8). Nat will need to export PPTX → PDF and drop those PDFs into the respective lecture folders.
- All image files under `_shared/Images/` (lab PNGs, breadboard, ball bearing, NIST figures).
- All data files under `_shared/Data/` (NIST CSVs, anonymized exam grades, pickled student datasets, `.mat` bearing data). Many notebooks also pull these over HTTP, so this is convenience caching.
- All Thonny scripts under `_shared/ThonnyScripts/`.
- `_shared/FastfoodData/` aggregation notebooks and CSV.
- Figure PNG/JPG files inside the Beamer subfolders for Lectures 11, 12, 13, 15, 17. The PDFs are self-contained for viewing; the figures are only needed if the `.tex` is recompiled.

## Slide PDFs flagged for relabeling

The schedule renumbering shifted lectures back by one in several places. The PDF *contents* (cover pages, footers, "Lecture N" titles) still show the 2025 numbering. PDFs cannot be edited in place; Nat needs to recompile from the `.tex` source (where available) or re-export from PowerPoint.

| New file (in new repo)                            | PDF cover currently says   | Should say        |
|---------------------------------------------------|----------------------------|-------------------|
| `Lecture05/Lecture_05.{pdf,pptx}`           | Lecture 6                  | Lecture 5         |
| `Lecture06/Lecture_06.{pdf,pptx}`           | Lecture 7                  | Lecture 6         |
| `Lecture07/Lecture_07.pptx`                 | Lecture 8                  | Lecture 7         |
| `Lecture11/Lecture_11.{pdf,tex}`            | Lecture 12                 | Lecture 11        |
| `Lecture12/Lecture_12.{pdf,tex}` (footer says Lecture 12) | Lecture 13 title, Lecture 12 footer | Lecture 12 throughout |
| `Lecture13/Lecture_13.{pdf,tex}` (footer says Lecture 12) | Lecture 13 title, Lecture 12 footer | Lecture 13 throughout |
| `Lecture15/Lecture_15.{pdf,tex}`            | Lecture 16                 | Lecture 15        |
| `Lecture17/Lecture_17.{pdf,tex}`            | Lecture 18                 | Lecture 17        |
| `Lecture20/Lecture_20.{pdf,pptx}`           | Lecture 20 (originally for old Lec 21 slot, content matches "AI-assisted coding") | Lecture 20 — content matches, title is fine |
| `Lecture21/Lecture_21.{pdf,pptx}`           | Lecture 21 (was Lecture_22 in 2025) | Lecture 21 — content matches; cover title says "Lecture 21" already since the 2025 file said "Lecture 21" on its cover |
| `Lecture22/Lecture_22.{pdf,pptx}`           | Lecture 23                 | Lecture 22        |
| `Lecture23/Lecture_23.{pdf,pptx}`           | Lecture 24                 | Lecture 23        |
| `Lecture24/Lecture_24.{pdf,pptx}`           | Lecture 25                 | Lecture 24        |

## Notebook prose self-references that may need scrubbing

The H1 title at the top of each `notes.md` file was rewritten safely to match the new lecture number. The notebook H1 titles ("# Lecture N: Title") and any prose self-references like "in Lecture 4 we showed..." were left alone, since some of them are real cross-references that need their target updated (Lecture 4 in 2025 -> Lecture 3 in 2026, etc.). The full list of unique self-references that the renumbering disturbed is:

- `Lecture02/lec02.ipynb` H1 still says "Lecture 3"
- `Lecture03/lec03.ipynb` H1 still says "Lecture 4"
- `Lecture04/lec04.ipynb` H1 still says "Lecture 5"
- `Lecture06/lec06.ipynb` H1 still says "Lecture 7"; prose has "Lecture 3" and "Lecture 4" references that map to new Lectures 2 and 3
- `Lecture07/lec07.ipynb` H1 still says "Lecture 8"
- `Lecture09/lec09.ipynb` (the whack-a-mole lab, moved from the 9/23 slot to 9/28) H1 now says "Lecture 9"
- `Lecture11/lec11.ipynb` H1 still says "Lecture 12"
- `Lecture12/lec12.ipynb` H1 still says "Lecture 13"
- `Lecture13/lec13.ipynb` H1 still says "Lecture 14"
- `Lecture14/lec14.ipynb` H1 still says "Lecture 15"
- `Lecture15/lec15.ipynb` H1 still says "Lecture 16"
- `Lecture16/lec16.ipynb` H1 still says "Lecture 17"
- `Lecture17/lec17.ipynb` H1 still says "Lecture 18"
- `Lecture21/lec21.ipynb` H1 still says "Lecture 22"; prose references "Lecture 4" (NIST stress-strain) that maps to new Lecture 3
- `Lecture22/lec22.ipynb` H1 still says "Lecture 23"
- `Lecture23/lec23.ipynb` H1 still says "Lecture 24"
- `Lecture24/lec24.ipynb` H1 still says "Lecture 25"
- `Lecture25/lec25.ipynb` H1 still says "Lecture 26"; the review-lecture body cross-references Lectures 20, 21, 22, 23, 24 from the 2025 numbering, all of which need a mechanical -1 shift

A safe scrub for the notebook H1 lines is a one-line sed; the prose cross-references inside the review notebook (Lecture 25) deserve a careful read.

## Other items flagged in Phase 1 that survive into Fall 2026

- Stale Canvas course ID `1881448` and assignment IDs scattered across notebook markdown and the HW `.tex` files. Will be replaced once Nat sets up Fall 2026 Canvas.
- Stale Ed Discussion course ID `84852`.
- `homeworks/HW*/hw*.tex` titles and due dates still reference 2025. The proposed semester reset script (`scripts/render_hw_titles.py`) was scoped but not yet built; for now, edit each `.tex` by hand or wait for Nat's Phase 4 follow-up.

## October 2026 shift: whack-a-mole lab postponed, Lectures 11+ renumbered

The 9/28 lab was not set up and ran on 10/5 instead, as Lecture 11. Every lecture
from the old Lecture 11 on moved one slot later and one number higher (folders,
notebook filenames, notebook H1 titles, Colab badges, slide filenames). The 11/30
"Final projects" workday was dropped to absorb the shift, so Exam 3 (12/2) and the
presentations (12/7) keep their dates; Exam 2 moved from 10/28 to 11/2.

This supersedes the slide table above for Lectures 11 and later. Most covers
carried the 2025 number, which was one too high, so the shift made them right:

| File                         | PDF cover says | Status                                         |
|------------------------------|----------------|------------------------------------------------|
| `Lecture12/Lecture_12.pdf`   | Lecture 12     | correct (recompiled, dated for 2026)           |
| `Lecture13/Lecture_13.pdf`   | Lecture 13     | correct (recompiled, dated for 2026)           |
| `Lecture14/Lecture_14.pdf`   | Lecture 14     | correct (recompiled, dated for 2026)           |
| `Lecture16/Lecture_16.pdf`   | Lecture 16     | correct                                        |
| `Lecture18/Lecture_18.pdf`   | Lecture 18     | correct                                        |
| `Lecture21/Lecture_21.pdf`   | Lecture 20     | re-export from PowerPoint as Lecture 21        |
| `Lecture22/Lecture_22.pdf`   | Lecture 21     | re-export from PowerPoint as Lecture 22        |
| `Lecture23/Lecture_23.pdf`   | Lecture 23     | correct                                        |
| `Lecture24/Lecture_24.pdf`   | Lecture 24     | correct                                        |
| `Lecture25/Lecture_25.pdf`   | Lecture 25     | correct                                        |

The covers from Lecture 16 on still carry Fall 2025 dates. Figures for the Beamer decks are not in `OldMaterial/`; copy them from `slides/lectureNN/` in the Fall 2025 repo, and compile with `pdflatex -shell-escape` (the decks use minted).

Prose pointers updated in this pass: the "Lecture 9 lab" reference in the Exam 1
extra prep notebooks (now Lecture 11), the topic list in `Lecture26/lec26.ipynb`,
and textbook chapters 2, 6, 8, 9 and 12. Not touched, and worth a read: textbook
Ch. 6 "mirrors Lecture 13", Ch. 9 "Lecture 18 touches on this", Ch. 11 "controlled
pendulum (Lecture 16)", and `Lecture24/lec24.ipynb`, whose intro still describes
the previous lecture as Newton's method. The `_shared/Images/lec19_*` files keep
their old names; `Lecture20/lec20.ipynb` references them by those names.
