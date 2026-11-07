# Project 9.1 slides

Editable Beamer source: [project9_exercise1.tex](project9_exercise1.tex).
The deck has exactly five content slides, with no separate cover.
Section 1 introduces state spaces, the two algebras, probability laws, and
observable--measure duality. Section 2 gives Project 9.1, its trajectory spaces,
the fundamental matrix, variation of constants, and verification. Cooling and
the longer time-ordering discussion remain in the manuscript.
The body uses 12pt text, with 17pt frame titles. The shared
[template style](template_style.tex) follows the user-provided
`output/presentations/main.tex`: Madrid, 4:3, serif fonts, blue title bars,
and the original footer layout. The supplied reference remains unchanged.

From the repository root:

```powershell
python scripts/build_slides.py
```

The script runs XeLaTeX twice and writes the PDF to
`output/slides/project9_exercise1.pdf`. Intermediate files also stay in
`output/slides/`. Biber is not needed for this slide deck.

In VS Code LaTeX Workshop, select the **XeLaTeX x2 (Beamer)** recipe for this
source. Use **XeLaTeX -> Biber -> XeLaTeX x2** for `paper/main.tex`.
The workspace settings also route compilation using the source's
`% !TeX program` comment to `output/slides/`. The manuscript uses
`output/paper/`. These settings apply only to this project.

For the standalone LaTeX source ZIP, extract all files into one folder and run
`xelatex project9_exercise1.tex` twice in that folder. Keep `template_style.tex`
beside the main source.

The problem source is the supplied `docs/StudentAssessmentExercise_unlocked.pdf`,
Project 9, item 1, page 12. No publication author or year is inferred.
