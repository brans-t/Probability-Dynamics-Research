# Probability Dynamics Lab

A LaTeX manuscript and reproducible experiments on stochastic dynamics,
coarse-graining, and learned probability flows.

## Project layout

```text
paper/                  Manuscript, shared preamble, bibliography, and PDF figures
slides/                 Editable Beamer sources and shared slide style
output/paper/           Current manuscript PDF copy
output/slides/          Current slide PDF only
build/                  Regenerable build files, manuscript PDF, and previews
src/probflow/           Reusable Gaussian dynamics, projection, and regression
experiments/            Benchmark entry points and experiment-specific modules
results/benchmarks/    Saved CSV/JSON results used by the manuscript
results/audit-2026-11-04/  Historical validation and statement-review records
tests/                  Numerical and experiment regression tests
scripts/                Manuscript build and project validation
docs/                   Technical guide, original assessment, and source index
```

Main files: [manuscript](paper/main.tex), [preamble](paper/preamble.tex),
[bibliography](paper/ref.bib), [technical guide](docs/README.md).

## Install and test

Python 3.10+:

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
python scripts/check_project.py
```

For neural experiments, install `python -m pip install -e ".[experiments]"`.

## Run experiments

```bash
python experiments/hamiltonian_benchmark.py
python experiments/project11_kl_benchmarks.py
python experiments/run_benchmarks.py
```

The combined benchmark covers noncommuting matrix flows, coupled OU
correlations, affine/neural conditional regression, and Markov discretization.
Use `--skip-neural` to run it without PyTorch.

Default runs update `results/benchmarks/` and `paper/figures/`.
For an isolated rerun, append `--output-root build/rerun` to any command.

## Build the manuscript

Install XeLaTeX and Biber through TeX Live or MiKTeX, then run:

```bash
python scripts/build.py
```

Output: `build/paper/main.pdf`, also copied to `output/paper/main.pdf` after
successful compilation. Auxiliary files stay in `build/paper/`.
Use `python scripts/build.py --publish-only` to copy an already compiled PDF.
Saved figures are included; training is not
required to compile. Run `python scripts/check_manuscript_audit.py` afterward
to validate numbering, references, and PDF navigation.

Build the Beamer slides with `python scripts/build_slides.py`.
Only the current PDF is published to `output/slides/`; auxiliary files stay
in `build/slides/`. Slide source and TikZ diagrams are in `slides/`.
VS Code LaTeX Workshop uses the same output directories through the
project's `.vscode/settings.json`; global VS Code settings are unaffected.
