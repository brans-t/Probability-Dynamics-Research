# Source-to-Manuscript Mapping

The source is the supplied [Student Assessment Exercise](StudentAssessmentExercise_unlocked.pdf). The current manuscript is [paper/main.tex](../paper/main.tex), its bibliography is [paper/ref.bib](../paper/ref.bib), and the compiled PDF is `paper/Tmp/main.pdf`.

The manuscript has one numbered chapter and five sections. Its **Source Index and Direct Links** is near the end, after the detailed assessment-to-chapter table and before References. Original project/item numbers below are not manuscript section numbers. There are 37 index entries: item 9.4 has separate analytic and numerical links.

| Original source | Integrated as | Current location and LaTeX target |
|---|---|---|
| 8, main task | Markov generator theorem, detailed balance and entropy dissipation | §1.4; `src:p8main` |
| 8.1 | Worked analysis of the centered scheme and its boundary limitations | §1.4; `src:p8q1` |
| 9.1 | Scalar integrating factor and matrix variation of constants | §1.2; `src:p9q1` |
| 9.2 | Composition, inverse and time reversal of flows | §1.2; `src:p9q2` |
| 9.3 | Variational equation and noncommuting-matrix correction | §1.2; `src:p9q3` |
| 9.4 | Liouville–Jacobi determinant theorem | §1.2; `src:p9q4` |
| 9.4, numerics | Euler / higher-order Jacobian analysis | §1.2; `src:p9q4discrete`; experiment in §1.5 |
| 9.5 | Transported volume identity | §1.2; `src:p9q5` |
| 9.6 | Minimum weighted kinetic-action path and velocity nonuniqueness | §1.2; `src:p9q6` |
| 9.7 | Continuity equation | §1.2; `src:p9q7` |
| 9.8 | Density change of variables | §1.2; `src:p9q8` |
| 9.9 | Material derivative and transport theorem | §1.2; `src:p9q9` |
| 9.10 | Differential entropy balance | §1.2; `src:p9q10` |
| 9.11 | Score dynamics, Hessian extension and long-time counterexample | §1.2; `src:p9q11` |
| 9.12 | Relative-entropy rate with sign check | §1.2; `src:p9q12` |
| 9.13 | First variation of transported KL | §1.4; `src:p9q13` |
| 9.14 | Quantile / triangular transport and sample-only limitations | §1.4; `src:p9q14` |
| 9.15 | Formal kinetic optimality system for a specified terminal functional | §1.4; `src:p9q15` |
| 10.1 | Hamilton equations | §1.2 Hamiltonian application; `src:p10q1` |
| 10.2 | Conservation of autonomous Hamiltonian energy | §1.2; `src:p10q2` |
| 10.3 | Reversed curves versus momentum-reflected trajectories | §1.2; `src:p10q3` |
| 10.4 | Symplecticity and phase-volume preservation | §1.2; `src:p10q4` |
| 11.1 | Nonnegativity of KL | §1.2; `src:p11q1` |
| 11.5 | Gibbs variational identity | §1.2; `src:p11q5` |
| 11.6 | Donsker–Varadhan representation | §1.2; `src:p11q6` |
| 11.7 | KL disintegration and data processing | §1.2; `src:p11q7` |
| 11.8 | Stein integration-by-parts identity | §1.2; `src:p11q8` |
| 12.1 | Gaussian conditional law on a hyperplane | §1.3; `src:p12q1` |
| 12.2 | Noisy conditioning and the sharp-level limit | §1.3; `src:p12q2` |
| 12.3 | Coarea and projected free energy | §1.3; `src:p12q3` |
| 12.4 | Conditional mean force and geometric correction | §1.3; `src:p12q4` |
| 13.1 | Total covariance and coordinate-selection discussion | §1.3; `src:p13q1` |
| 13.2 | Itô formula under projection | §1.3; `src:p13q2` |
| 13.3 | Matching time marginals under existence / uniqueness assumptions | §1.3; `src:p13q3` |
| 14.1 | Gaussian interpolant single- and two-time statistics | §1.4; `src:p14q1` |
| 14.2 | Conditional interpolation velocity | §1.4; `src:p14q2` |
| 14.3 | Conditional score identity | §1.4; `src:p14q3` |

## Not conflating claims

- Matching **one-time marginal distributions** does not establish Markovianity of the original projected process or equality of path laws.
- The projected drift can depend on time through the conditional law of the unreduced process.
- A regularizer or neural loss is not itself proof of a globally correct PDE solution.
- An `Exercise` may have an accompanying `solution`; read its local status rather than treating the environment name alone as an unresolved-work marker. A `planned extension` remains an unexecuted research item.
- Project 9.15 supplies formal stationarity conditions, not a general existence / uniqueness theorem for an optimizer.
- The double-well equilibrium formulas are present, but its proposed nonlinear numerical study has not been executed in the supplied scripts.

## Text and attribution rules for future edits

Add `\sourcecredit{<project>}{<question>}` followed by a unique `\phantomsection\label{src:p<project>q<question>}` at the relevant statement. Then add a matching `\sourceindexrow{<project>}{<item>}{<label>}{<description>}` in the Source Index, and update the detailed source table and this file. For unnumbered prompts use a mnemonic label, as for Project 8's main task (`src:p8main`). Project 10 uses a shared credit marker for items 1–4 and individual target labels within that application.

Use the complete XeLaTeX / Biber build from [reproduction.md](reproduction.md), including repeated XeLaTeX passes for resolved links and page numbers.


All mapped results and exercises reside within Chapter 1. The assessment record in `paper/ref.bib` does not invent an author or year. Its note retains an incoming filename (`StudentAssessmentExercise_unlocked(1).pdf`); the copy currently stored in this repository is `docs/StudentAssessmentExercise_unlocked.pdf`. These names refer to source-file provenance, not to separate works.
