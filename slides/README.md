# Project 9.1 and 9.2 slides

Editable Beamer source: [project9_exercises1_2.tex](project9_exercises1_2.tex).
The deck has 21 slides: a title page, a contents page, 10 main slides,
and 9 appendix slides.

The footer counts the main presentation separately: `1 / 12` through
`12 / 12`, including the title and contents pages (the title page hides its
footer). Appendix pages use `A-1 / 9` through `A-9 / 9`; they do not increase
the main total. The PDF still contains 21 physical pages. Both totals are
calculated automatically by Beamer after two compilation passes.

The main presentation follows:

1. Euclidean state space, vector operations, the endomorphism algebra,
   the Euclidean norm, and the role of continuity and differentiability.
2. The manuscript's fluid-motion background, the general ODE initial-value
   problem, and the mapping forms of the velocity field and a trajectory.
3. Project 9.1 through the trajectory operator, its kernel, evaluation maps,
   the homogeneous evolution operator, and the affine solution formula.
4. Project 9.2 through general state flows, evaluation bijections, composition,
   inverses, autonomous flows, a nonlinear example, and time reversal.
5. The induced evolution operator on the observable algebra.

The general-flow discussion allows nonlinear velocity fields. Probability
transport and the Hamiltonian momentum-reflection question remain outside
this deck. Two-column layouts, bullet lists, and numbered derivations
organize the content. Thirteen editable TikZ diagrams show state-space geometry,
evaluation maps, affine solution sets, and flow laws.
Each slide displays its manuscript or assessment reference.
Detailed algebra operations, continuation arguments, evaluation proofs,
variation of constants, solution verification, autonomy, and time reversal
are collected in the appendix. Internal links connect the main results to
their derivations and return to the corresponding main slide. The contents
page links directly to the three main sections and the appendix.
The opening section has two content slides. The first pairs algebra operations
with a large state-space diagram; continuity and differentiability are mentioned
without limit definitions. Its ODE slide uses a single
column, with a centered initial-value system and a left brace. The observable
algebra is introduced with pullback evolution; its detailed operations and
diagrams appear in Appendix A1. Introductory body text is 9 pt on Beamer's
12.8 cm canvas, approximately equivalent in relative size to 18 pt on a
standard 10-inch-wide presentation.
Slide 11 embeds the manuscript's 61-frame nonlinear-flow animation at 20 FPS,
with playback controls, looping, and a static first-frame preview. The PNG
frames are reused directly from `paper/figures/flow_deformation/`; they are not
duplicated. Playback requires a PDF viewer with animation support. Other
viewers retain the static preview.
The shared [template style](template_style.tex) retains the supplied Madrid
palette, 4:3 format, and serif typography. Beamer manages the title bar,
section footer, columns, and content spacing. TikZ is used for diagrams;
page content is not positioned with absolute overlay coordinates.

From the repository root:

```powershell
python scripts/build_slides.py
```

The script runs XeLaTeX twice and writes the PDF to
`output/slides/project9_exercises1_2.pdf`. This is the only published slide output;
auxiliary files stay in `build/slides/`. Biber is not needed.

In VS Code LaTeX Workshop, select the **XeLaTeX x2 (Beamer)** recipe for this
source. The recipe compiles into `build/slides/` and copies only the PDF to
`output/slides/`. Use **XeLaTeX -> Biber -> XeLaTeX x2** for `paper/main.tex`;
its outputs stay in `build/paper/`, and the completed PDF is also copied to
`output/paper/main.pdf`. These settings apply only to this project.

For direct compilation, run `xelatex project9_exercises1_2.tex` twice from
this source directory. Keep `template_style.tex` beside the main source,
and preserve the `diagrams/project9/` folder. Use the build script above to
keep generated files outside the source directory.
The Beamer source inputs the editable TikZ fragments directly, so a separate
diagram compilation step is not required.

TikZ source is in `slides/diagrams/project9/`. Only diagrams referenced by
the current deck are retained. Previous slide versions, PowerPoint exports,
source ZIPs, and presentation templates have been removed.

The problem source is the supplied `docs/StudentAssessmentExercise_unlocked.pdf`,
Project 9, items 1–2, page 12, together with the corresponding solutions in
`paper/main.tex`. The assessment PDF stays local and is excluded from Git.
Project 9.1 starts directly with its general ODE and initial condition.
No publication author or year is inferred.
