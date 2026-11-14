# Chapter 2: Neural PDE solvers (provisional)

Chapter 1 includes Sections 1.1–1.5. The provisional neural PDE extension is
a separate Chapter 2, with Sections 2.1–2.6, in
[paper/main.tex](../paper/main.tex), directly after Chapter 1. Existing proofs, deferred
solutions, equation anchors, experiment tables, figures, and saved OU evidence
are retained. Restoring sections does not complete individually pending proofs.
The Source Index has 47 entries: all 45 earlier entries plus Projects 2 and 3.

## Mathematical contract

- SDE: `dX = b_f dt + sqrt(2 epsilon) dW`, `b_f = -grad(V_f)`.
- Backward committor PDE: `epsilon Delta q + b_f . grad q = 0` outside A and B.
- Forward density PDE: `p_t = -div(b_f p) + epsilon Delta p`.
- Periodic domain: `[-L/2,L/2)^d`, default `L=20`; no IC for the stationary
  committor. Dirichlet values are 0 on A and 1 on B.
- B centers are required arguments. The smoke test explicitly passes the source's
  repeated `[[1,1],[1,1]]`. Their union is one ball, with radius 0.5.
- Fourier phases are `2*pi*k.x/L`; canonical integer modes exclude duplicate
  or opposite mode pairs. Parseval normalization is exact.
- The source's constraint is **L2(f)/volume <= 0.1**, not an RMS bound and not
  a squared-norm constraint. The sampler saturates a chosen radius; it does not
  claim uniform sampling of the function-space ball.

The printed `-epsilon Delta q + b_f.grad q=0` instead corresponds to SDE drift
`-b_f`. Which equation the source intended remains unresolved. All implemented
solvers use the standard backward equation stated above.

The exact source Gaussian potential is available as `potential(x,f)` and its
drift as `drift(x,f)`. It is not a smooth periodic function on a finite box.
The periodic benchmark explicitly uses Gaussian lattice sums, evaluated using
the separable Fourier expansion in Section 2.5. Passing `periodize=True` and
the same `length` to potential and drift selects this model. The reference
solver always selects it. Its Fourier cutoff has first omitted coefficient
below 1e-15; this is not a dimension-independent total-error guarantee.

## Implementation and validation

[neural_pde_solver.py](../src/probflow/neural_pde_solver.py) contains the field
interface and sampler, Euclidean/periodic potentials, autodifferentiated drift,
pointwise AD committor residual, constraint losses, ball masks, sparse periodic
reference solver, 2D spectral convolution and FNO, joint training, and the
analytic heat-equation sampling counterexample.

The sparse reference uses nonnegative outgoing rates
`epsilon/h^2 + max(±b_j,0)/h`. Its rows sum to zero. Absorbing nodes have prescribed
values; the interior sparse system satisfies a discrete maximum principle.
The grid residual used in FNO training is exactly this operator. It is a
first-order drift approximation; the continuum AD residual is a separate
interface for coordinate networks with independent rows. Neither an algebraic
residual nor a grid loss certifies continuum accuracy.

The FNO receives f plus four periodic position channels to locate the fixed
absorbing geometry. A sigmoid bounds raw output; a hard mask imposes absorbing
grid values. The BC loss remains on raw outputs, while the PDE uses hard values
and excludes absorbing nodes. Off-grid boundary-exact decoding is not implemented.

[tests](../tests/test_neural_pde_solver.py) check Parseval norms and periodicity
through d=10, independent finite-difference drift gradients, a Gaussian lattice
sum against the periodic implementation, polynomial AD residuals including the
drift sign, BC/range/periodic wrap, sparse versus tensor residuals, an analytic
strip committor at three resolutions, manufactured-function consistency, a known
spectral multiplier, parameter updates, and the cutoff counterexample.

Standard reproduction with the optional dependencies installed:

```powershell
python -m pip install -e ".[dev,experiments]"
python -m pytest -q
python experiments/neural_pde_smoke.py
python scripts/build.py
python scripts/check_project.py
python scripts/check_manuscript_audit.py
```

The local validation environment already had PyTorch in the `vae` Python 3.11
environment, SciPy/Matplotlib in `manimgl`, and pytest in the base Anaconda
environment. No packages or global settings were changed. A disposable workspace
virtual environment at `build/neural-pde-revision/venv` adds these existing package
directories through a local `.pth` file, so subprocess tests inherit the same
dependencies. Validation used:

```powershell
& 'build/neural-pde-revision/venv/Scripts/python.exe' -m pytest -q
& 'D:/App/Anaconda/envs/vae/python.exe' -c "import sys,runpy; sys.path.extend(['D:/App/Anaconda/envs/manimgl/Lib/site-packages','D:/App/Anaconda/Lib/site-packages']); runpy.run_path('experiments/neural_pde_smoke.py',run_name='__main__')"
```

This environment arrangement is a local execution detail, not an imported path
dependency in production code. Other installations should use the project extras.
The checks require SciPy and torch; the new test module skips if torch is absent,
so a skipped run alone is insufficient validation of this extension.
The full suite passed all 31 tests, including all 16 new PDE tests; no test was skipped.
Ruff checks and formatting checks passed for the three new Python files.

The initial section-based version passed the full XeLaTeX/Biber build and
manuscript audit (140 pages, 230 live labels, 47 assessment links, and 63 numbered
statements). The extension has since been promoted to Chapter 2, with section,
equation, and statement numbering reset by the existing chapter conventions.
Existing labels remain available for cross-references; `ch:neural-pde` identifies
the new chapter, and the former `sec:neural-pde` remains a compatibility anchor.
The chapter-based build passed the manuscript and PDF navigation audits:
141 pages, 231 live labels, 47 assessment links, and 63 numbered statements.
Chapter 2's six section anchors resolve to 2.1–2.6, with chapter-based equation
and proposition numbers. Visual review confirmed the chapter opening and running
header. All PDE equations, proofs, and existing labels are unchanged by this move.

A turn-start snapshot comparison in `build/neural-pde-revision/` verified all
208 old labels, all old display math, all six original image inclusions
(including deferred material), and all source credits. All 14 deferred-solution
blocks in that snapshot remain intact. The dimension index and random-variable
names exposed in restored Project 12.1/13.1 were corrected; older source
credits, equations, and proofs were not replaced from the PDF. Existing tracked
code, tests, figures, benchmark data, and slides were unchanged.

The checker validates the inline Chapter 2 and expects Projects 2–3. The former
separate `paper/neural_pde.tex` has been merged into `paper/main.tex`; legacy
include expansion remains available for historical archives. Its
previous slide-diagram check only read the deck entry point despite existing
section includes; it now follows those includes and accounts explicitly for
the three retained alternate diagrams. This changes validation only, with no
slide edits. The existing snapshot-only `--baseline` modes still deliberately
reject substantive mathematical revisions and are not used as revision approval.

## Executed smoke test, 15 November 2026

The [raw report](../results/neural_pde/smoke.json) records Python 3.11.15,
NumPy 2.4.4, SciPy 1.17.1, and PyTorch 2.11.0+cu128, executed on CPU.
It saves all six input coefficient vectors, the split, losses, and parameters.
Seed 20261115, N=32, L=20, epsilon=0.5, radius=0.5, repeated B center (1,1),
four training and two held-out fields, width 8, depth 2, four spectral modes per
band, 12 Adam steps at 0.003, and loss weights (1,0.01,1,1) match the manuscript.

The joint training loss changed from 0.6604660 to 0.6093471; held-out RMSE was
0.2864835. The largest sparse interior residual across the six reference solves
was 4.885e-15. Successive reference-grid RMSEs on shared nodes for 32→64 and
64→128 were 0.0409333 and 0.0292760. Ball voxelization changes with resolution;
these numbers do not establish an asymptotic order or label accuracy.
The held-out error is substantial and the sample size tiny: this run proves
integration, not a successful committor surrogate.

The heat diagnostic (T=1, epsilon=1, amplitude=0.5, k=64, 11 fixed times) had
zero empirical residual, mass error 1.11e-16, and maximum positive-time error
0.0720047. Its true continuum residual grows with k. This is an analytic
function-class counterexample with numerical verification, not a trained PINN.

## Open work

The intended printed sign and second B center need source clarification. The
periodic completion is explicit but is a modeling choice. Multi-seed accuracy,
independent continuum error estimates, PINN/FNO cost comparisons, epsilon and
geometry conditioning, resolution-transfer experiments, and reference-label
convergence are planned. The completed finite-sampling proof makes no claim
about adaptive or indefinitely refreshed samples.

The field callable, Fourier evaluation, potential, drift, and pointwise AD
residual accept general dimensions. The reference solver and FNO are **2D**.
No factorized FNO, sparse operator learner, low-rank decoder, high-dimensional
label generator, or d>=10 training result is implemented. A full N^d grid and
the dimension-dependent amplitude permitted by the literal norm constraint
must be addressed before scaling the study.

## Source verification and software attribution

The local assessment was checked on PDF pages 4–5 for Projects 2–3. New
bibliography keys `e2006transition`, `raissi2017pinn`, and `li2020fno` were
checked on the authors' paper and arXiv full text/metadata on 15 November 2026:

- [E and Vanden-Eijnden, Towards a Theory of Transition Paths](https://web.math.princeton.edu/~weinan/pdf%20files/theory%20transition.pdf),
  Journal of Statistical Physics 123(3), 503–523 (2006), DOI 10.1007/s10955-005-9003-9.
- [Raissi, Perdikaris, and Karniadakis, Physics Informed Deep Learning (Part I)](https://arxiv.org/abs/1711.10561),
  arXiv:1711.10561 (2017).
- [Li et al., Fourier Neural Operator for Parametric Partial Differential Equations](https://arxiv.org/abs/2010.08895),
  arXiv:2010.08895 (2020; revised 2021).

The scientific-writing skill informed the separation of mathematical results,
executed evidence, and planned work. Software/procedure attribution:
[Kassis, Agarwal, He, Patel, and Brueckner, Scientific Agent Skills: A Library of Procedural Knowledge for Research Agents](https://arxiv.org/abs/2609.00065)
(2026), DOI 10.48550/arXiv.2609.00065. These records were checked by the agent;
author approval and independent human verification are not implied.
