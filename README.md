# Probability Dynamics Lab

A LaTeX manuscript and reproducible experiments on stochastic dynamics,
coarse-graining, and learned probability flows.

## Read the current draft

| Document | Compiled PDF | Editable source |
|---|---|---|
| Manuscript | [Read the manuscript](output/paper/main.pdf) | [paper/main.tex](paper/main.tex) |
| Section 1.2 slides | [Read the slides](output/slides/project9_exercises1_2.pdf) | [slides/project9_exercises1_2.tex](slides/project9_exercises1_2.tex) |

The PDFs in `output/paper/` and `output/slides/` are tracked in Git.
LaTeX auxiliary files and previews remain under the ignored `build/` directory.
Embedded flow animations require a compatible PDF viewer; other viewers show
the static preview.

## Current manuscript scope

The current PDF includes Chapter 1, a provisional Chapter 2, and Appendix A:

- **1.1 — State Algebra, Probability Spaces, and Observables:** states,
  measurable structures, observable algebras, probability laws, and duality.
- **1.2 — Dynamical Equations, Flow Maps, and Probability Transport:** ODE flows, Jacobians,
  density transport and the continuity equation, Hamiltonian dynamics,
  entropy, and variational principles.
- **1.3 — Conditional Probability and Effective Dynamics:** disintegration,
  mean force, exact projection, and assumptions behind Markovian closure.
- **1.4 — Learned Probability Flows and Structure-Preserving Approximation:**
  conditional learning, variational transport, and Markov discretization.
- **1.5 — A Coupled OU Benchmark: Exact, Numerical, and AI Results:** the
  existing exact formulas, diagnostics, and saved numerical evidence.
- **Chapter 2 — Neural PDE Solvers (provisional), Sections 2.1–2.6:** Fokker–Planck duality, committors,
  a proved finite-sampling counterexample, FNO, and a computational roadmap.
- **Appendix A:** ODE existence, uniqueness, continuation, and linear evolution.

Individual deferred proofs and solutions remain explicitly pending. The neural
PDE module separates proved statements, executed integration checks, and planned
accuracy/high-dimensional experiments. See its [research guide](docs/neural-pde-research.md).

The opening Source Index links assessment questions to manuscript results.
A superscript **⋆** marks an incomplete solution, proof, or extension,
including entries whose proof reads *Proof to be completed.* The index
contains 47 live entries, including Assessment Projects 2 and 3.
This is a working draft with pending proofs.

## Project layout

```text
paper/                  Manuscript, shared preamble, bibliography, and PDF figures
slides/                 Editable Beamer sources and shared slide style
output/paper/           Tracked manuscript PDF
output/slides/          Tracked slide PDF
build/                  Regenerable build files, manuscript PDF, and previews
src/probflow/           Reusable Gaussian dynamics, projection, and regression
experiments/            Benchmark entry points and experiment-specific modules
results/benchmarks/     Saved CSV/JSON results used by the manuscript
results/audit-2026-11-04/  Historical validation and statement-review records
tests/                  Numerical and experiment regression tests
scripts/                Manuscript build and project validation
docs/                   Technical guide, reviews, and assessment source index
```

Main files: [manuscript](paper/main.tex), [preamble](paper/preamble.tex),
[bibliography](paper/ref.bib), [technical guide](docs/README.md).
The original assessment PDF is kept locally and excluded from Git;
question provenance is recorded in [docs/source_index.tsv](docs/source_index.tsv).

## Install and test

Python 3.10+:

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
```

For neural experiments, install `python -m pip install -e ".[experiments]"`.

## Run experiments

```bash
python experiments/hamiltonian_benchmark.py
python experiments/project11_kl_benchmarks.py
python experiments/scalar_jacobian.py
python experiments/run_benchmarks.py
python experiments/neural_pde_smoke.py
```

The combined benchmark covers noncommuting matrix flows, coupled OU
correlations, affine/neural conditional regression, and Markov discretization.
Use `--skip-neural` to run it without PyTorch.

The neural PDE smoke test writes `results/neural_pde/smoke.json` and trains only
a tiny 2D FNO. Other default runs update `results/benchmarks/` and `paper/figures/`.
For an isolated rerun, append `--output-root build/rerun` to any command.

## Build the manuscript

Install XeLaTeX and Biber through TeX Live or MiKTeX, then run:

```bash
python scripts/build.py
```

Output: `build/paper/main.pdf`, also copied to `output/paper/main.pdf` after
successful compilation. Auxiliary files stay in `build/paper/`.
Use `python scripts/build.py --publish-only` to copy an already compiled PDF.
Saved figures are included; running experiments or training is not required
to compile.

Build the Section 1.2 Beamer slides with `python scripts/build_slides.py`.
The deck has 30 main slides and 14 appendix slides, organized around the
state/observable/probability framework, selected algebraic solutions, and
subsequent research directions. Pending proofs remain deferred.
Only the current PDF is published to `output/slides/`; auxiliary files stay
in `build/slides/`. Slide source and TikZ diagrams are in `slides/`.
Continuation sources are grouped under `slides/sections/`.
VS Code LaTeX Workshop uses the same output directories through the
project's `.vscode/settings.json`; global VS Code settings are unaffected.

## Manuscript checks

```bash
python scripts/check_project.py
python scripts/check_manuscript_audit.py
```

These are strict checks of repository consistency, manuscript references,
numbering, and PDF navigation. The PDF audit also requires Poppler tools
(`pdfinfo`, `pdftotext`, and `pdftohtml`) on PATH and a manuscript build in
`build/paper/`.

Source-index checks distinguish live links from explicitly omitted entries and
verify that omitted source labels remain preserved in the commented source.
The full checks also enforce repository and formatting conventions; successful
compilation does not certify mathematical correctness or completion of the proofs.

See the [technical guide](docs/README.md) for benchmark parameters,
reproduction limits, and source provenance, and the [slide guide](slides/README.md)
for presentation structure and viewer requirements.
