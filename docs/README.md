# Technical guide

Installation, experiment commands, and manuscript compilation are documented in
the [root README](../README.md).

## Responsibilities and data flow

| Location | Responsibility |
|---|---|
| `src/probflow/gaussian.py` | Exact coupled OU moments, Gaussian conditionals, projected drift, and correlations |
| `src/probflow/projected.py` | Projected moment ODE and equilibrium free-energy closure |
| `src/probflow/learning.py` | Affine conditional regression and drift conversion |
| `experiments/run_benchmarks.py` | Combined benchmark orchestration and summary JSON |
| `experiments/matrix_flow.py` | Noncommuting matrix IVP and determinant convergence |
| `experiments/conditional_regression.py` | OU comparison, sampling, affine baseline, and optional neural training |
| `experiments/markov.py` | No-flux Markov generator, mass, positivity, and relative entropy |
| `experiments/_paths.py` | Explicit output configuration and CSV writing |
| `experiments/hamiltonian_benchmark.py` | Euler/velocity-Verlet oscillator comparison |
| `experiments/project11_kl_benchmarks.py` | Exact truncated-normal KL curve |

Reusable model formulas belong in `src/probflow`; benchmark parameters, plots,
and reporting belong in `experiments`. Importing experiment modules does not
run a benchmark, create output directories, or start neural training.

Every entry point supports `--output-root PATH`. Outputs mirror the repository:
`PATH/results/benchmarks/` and `PATH/paper/figures/`. With no argument,
`PATH` is the repository root. Paths are resolved independently of the current
working directory.

## Experiments and outputs

| Entry point | CSV/JSON outputs | PDF figures |
|---|---|---|
| `hamiltonian_benchmark.py` | `hamiltonian_energy.csv`, `hamiltonian_summary.json` | `hamiltonian_energy.pdf`, `hamiltonian_phase.pdf` |
| `project11_kl_benchmarks.py` | `project11_truncated_gaussian_kl.csv` | `project11_truncated_gaussian_kl.pdf` |
| `run_benchmarks.py` | `jacobian_convergence.csv`, `affine_regression.csv`, `conditional_regression.csv`, `markov_semidiscrete.csv`, `results.json` | `jacobian_convergence.pdf`, `ou_correlation.pdf`, `conditional_regression.pdf` |

The combined runner uses seed `20261102`. In `--skip-neural` mode,
`results.json` contains an empty `ML` list; the neural CSV and figure are not
written. Use a fresh output root for a partial run to avoid mixing old and new
artifacts.

### OU parameters and interpretation

The potential is `V(x,y) = a*x^2/2 + c*(y-kappa*x)^2/2`.
The library calls its Hessian `H`; the manuscript calls it `K`.
The benchmark explicitly uses `(a,c,kappa,beta) = (0.8,1.7,1.1,1)`,
initial mean `(1,-0.8)`, and initial covariance `diag(0.12,0.25)`.
Library defaults describe another valid model and are not benchmark parameters.

Matching one-time marginals does not imply matching path laws or temporal
correlations. Conditional-mean RMSE, projected-drift RMSE, and noisy-label RMSE
measure different quantities. Affine and neural fits share the held-out test
set but use separately sampled training sets. Training normalization uses only
the training data. The original experiment does not save model weights.

### Reproduction status

The checked-in data and figures are the manuscript's canonical results.
The historical [comparison](../results/audit-2026-11-04/comparison.json) and
[environment record](../results/audit-2026-11-04/environment.json) describe a
separate full rerun, including neural training. Deterministic results and affine
regression agreed to floating-point precision. Neural conditional-mean RMSE was:

| Training samples | Saved result | Historical rerun |
|---|---:|---:|
| 512 | 0.0742657483 | 0.0742657706 |
| 4096 | 0.0991135389 | 0.0931584165 |

The original environment was not fully frozen. A fixed seed does not establish
bitwise equality across dependency versions or platforms. Record the commit,
Python/dependency versions, seed, command, and output directory for new runs.
Historical source hashes in the comparison describe the code at that audit,
before the subsequent code reorganization.

## Manuscript organization and sources

The five main sections cover state/observable/probability language, deterministic
transport and entropy, conditional/effective dynamics, learned flows and numerical
structure, and a coupled OU benchmark. HNN transfer is retained only as a short
prospective paragraph beside the Hamiltonian application; its former appendix
and supplementary navigation have been removed.

Section 1.2 follows four themes: state-flow geometry; observable and probability
transport; Hamiltonian mechanics as an application; entropy, variational principles,
and free energy. Local derivation headings remain in the text. The main chapter
contains 14 subsections, grouped as 3/4/2/3/2 across its five sections.

The original assessment is kept locally as `docs/StudentAssessmentExercise_unlocked.pdf`
and is excluded from Git. The [machine-readable source index](source_index.tsv)
preserves Project/item provenance in the repository.
The manuscript's Source Index provides 45 clickable entries, including all 13
Project 11 items. It is the single question-to-location table. Source numbers
are independent of manuscript section numbers. A linked entry need not be an
unrestricted solution: the [current review](manuscript-review-2026-11-06.md)
records original PDF pages, answer scope, corrections, and remaining gaps.
The assessment has no inferred author or publication year.

The prior review addressed flow existence/differentiability, noncommuting
fundamental matrices, generator domains, entropy/score/KL differentiation,
convex duality, conditional geometry, Markovian projection assumptions,
transport stationarity, discrete entropy dissipation, and local HNN coordinates.
The [statement review](../results/audit-2026-11-04/statement_review.csv) records
72 numbered statements and eight Notices under their stated scope. Its line
numbers refer to the reviewed manuscript; it is not a formal proof certificate.

General ODE existence, uniqueness, continuation, and flow-regularity proofs
are collected in Appendix A. The main text states their assumptions and
links to those proofs before solving Project 9.1. Its worked solution is
not repeated in a separate appendix derivation.

The manuscript keeps the assessment as its main thread. The linear ODE answer
retains the algebraic interpretation and a complete variation-of-constants
derivation, with repeated explanations and diagrams removed. Three orange
"Later thought" panels retain the HNN idea, conditional geometry, and a nonlinear
OU extension. Previously proposed checks already covered by the experiments
are no longer labeled pending. Source identifiers and canonical figures/data
are preserved; the assessment bibliography entry now uses its actual filename.
The historical statement-review counts and line numbers above describe the
earlier reviewed version, rather than the current shortened manuscript.
Within each numbered `equation`, the label remains immediately before
`\\end{equation}`.

## Validation and maintenance

```bash
python -m pytest -q
python scripts/check_project.py
python scripts/build.py
python scripts/check_manuscript_audit.py
```

The project checker uses only the standard library and checks Python syntax,
local Markdown links, manuscript labels/citations, source-index consistency, and
saved artifact locations. The PDF audit additionally requires Poppler tools
(`pdfinfo`, `pdftotext`, and `pdftohtml`) on PATH.

For optional symbolic checks:

```bash
python -m pip install -e ".[audit]"
python scripts/check_math_identities.py
```

The exact algebra checks supplement mathematical review; they do not validate
all proofs. Some historical checks concern the removed HNN discussion. The optional `--baseline ZIP` modes on the checkers are for historical
snapshots and deliberately require protected source/data files to remain
byte-identical. They are not appropriate for validating an editorial or mathematical revision.

VS Code's LaTeX Workshop recipe is configured in
[settings.json](../.vscode/settings.json). Use XeLaTeX because the manuscript uses
`fontspec`; bibliography processing uses Biber. Build outputs and local snapshots
are ignored under `output/` and `build/`. The output directory contains only
the current manuscript PDF in `output/paper/` and slide PDF in `output/slides/`;
all LaTeX auxiliary files stay in `build/`. The manuscript PDF is generated at
`build/paper/main.pdf` and copied to `output/paper/main.pdf` after compilation.
The manuscript and slide build scripts use the same directories as the
workspace settings; global VS Code settings are not changed.

The Liouville--Jacobi example embeds the 61 supplied PNG frames,
stored in `paper/figures/flow_deformation/`,
using `animategraphics` at 20 FPS. A PDF viewer supporting embedded PDF
animations is needed for playback; the first frame remains the static preview.
To regenerate the frames and an optional GIF without changing the originals, run:

```bash
python scripts/flow_deformation_source.py
```

The generator writes to `build/flow_deformation/`; use `--output-dir PATH`
to choose another destination, or `--skip-gif` to generate only the frames.
It requires NumPy, Matplotlib, and Pillow. The GIF is a separate preview;
the manuscript embeds the PNG sequence directly.

Remaining research includes multi-seed uncertainty estimates, saved neural models,
nonlinear double-well dynamics, HNN transfer experiments, and spatial refinement.
Unselected assessment topics remain outside the completed manuscript:
numerical PDE/PINN analysis, committors, rare events, mean-field/colored-noise
limits, Feynman--Kac, Jarzynski relations, diffusion bridges, and a full
Wasserstein/JKO treatment.
