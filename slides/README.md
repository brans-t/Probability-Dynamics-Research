# Section 1.2: framework and algebraic solution

Entry point: [project9_exercises1_2.tex](project9_exercises1_2.tex).
The stable filename preserves the existing build commands and PDF links.

The presentation has **30 main slides, including the title and contents pages,
plus 14 appendix slides** (44 PDF pages). The title page hides its footer.
Main pages use `2 / 30` through `30 / 30`; appendices use `A-1 / 14` through
`A-14 / 14`. Beamer calculates both totals after two compilation passes.

## Narrative and selection

The main thread is the state–observable–probability framework, the algebraic
constructions it supplies, and the research that those constructions support.
Questions are selected to illustrate the framework rather than to cover every
assessment item.

| Main pages | Role |
|---|---|
| 1–2 | Title and linked outline |
| 3–6 | States, observables, laws, their algebraic structures, and compatible induced evolutions |
| 7–11 | Affine ODEs through kernels and translates, evaluation isomorphisms, and composition of nonlinear flows |
| 12–18 | Variational matrices, noncommutative evolution, trace/determinant reduction, the nonlinear-flow animation, and density transport |
| 19–23 | Observable algebra, duality, generators, Markov extension, and entropy |
| 24–26 | Hamiltonian conservation and Gibbs change of measure as structural applications |
| 27–30 | Algebraic tools, conditional projection, conditional learning, and a research/validation programme |

The selected problems are the affine initial-value problem, flow composition,
Jacobian/density transport, Hamiltonian geometric conservation, and Gibbs
variational optimization. The final four slides connect these constructions to
subsequent work. Projection and learning are explicitly presented as research
directions based on manuscript Sections 1.3–1.5, not as newly completed results.

Euler/RK4 convergence, Verlet benchmarks, separate volume transport,
time-reversal variants, time-dependent observables, KL transport, and KL
convexity are outside this focused presentation. Their manuscript content,
experiment code, and saved results are unchanged. Problems with `Proof to be
completed.` or `To be completed.` remain deferred.

## Source modules and appendix

- [Framework](sections/framework.tex): objects, algebras, ODE, and induced evolution.
- [Algebraic solution](sections/algebraic_flows.tex): evaluation, kernels, affine solutions, and flow composition.
- [Geometry](sections/geometry.tex): matrix evolution, Jacobians, animation, and transport.
- [Observable evolution](sections/probability.tex): duality, generators, Markov extension, and entropy.
- [Applications](sections/applications.tex): Hamiltonian structure and Gibbs tilting.
- [Research](sections/research.tex): conditional projection, learning, and proposed validation tasks.
- [Appendix](sections/appendix_transport.tex): 14 derivations supporting the selected constructions.

Appendices A1–A7 cover algebra operations, existence, evaluation, the affine
family, variation of constants, solution verification, and general composition.
A8–A14 cover the determinant equation, Koopman time derivatives, density change
of variables, weak continuity, symplecticity, entropy, and Gibbs tilting.
Main pages link to the corresponding derivations and the appendix links back.

## Style, animation, and build

The original [template](template_style.tex) keeps its blue Madrid palette,
4:3 canvas, serif typography, and separate main/appendix counters. Existing
TikZ fragments remain editable under `diagrams/project9/`.

Main slide 16 retains the 61-frame nonlinear-flow animation at 20 FPS,
with playback controls, looping, and a static first-frame preview. It loads
frames from `paper/figures/flow_deformation/`. A compatible PDF viewer is
needed for playback; other viewers retain the static preview.

From the repository root:

```powershell
python scripts/build_slides.py
```

The script runs XeLaTeX twice and publishes only
`output/slides/project9_exercises1_2.pdf`. Build files and previews stay under
the ignored `build/slides/` directory. Biber is unnecessary.
In VS Code LaTeX Workshop, select **XeLaTeX x2 (Beamer)**.
Direct compilation also works from `slides/`; preserve `sections/`,
`diagrams/project9/`, `template_style.tex`, and the manuscript figure paths.

The deliverables follow the established editable Beamer/PDF workflow.
Slide footers identify manuscript sections and relevant assessment questions.
The local assessment source remains `docs/StudentAssessmentExercise_unlocked.pdf`.
