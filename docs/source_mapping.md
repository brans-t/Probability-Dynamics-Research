# 原题映射与 PDF 导航

原题：[Student Assessment Exercise](StudentAssessmentExercise_unlocked.pdf)。
文稿：[main.tex](../paper/main.tex)；参考文献：[ref.bib](../paper/ref.bib)；编译输出：`paper/Tmp/main.pdf`。

目录之后的 **Source Index and Direct Links** 提供 45 个原题入口，名称和页码均可点击，包含 Project 11 的全部 13 题。
**Supplementary Index and Direct Links** 另有 7 个 HNN 附录入口。原题编号与论文章节编号彼此独立。
主章含五节，另有独立 HNN 附录；附录的计算协议是研究计划，不是已有实验结果。

以下表格对应 [source_index.tsv](source_index.tsv)，以 `main.tex` 中的 `\sourceindexrow` 为依据；运行 `python scripts/check_project.py` 可核对三者与目标标签。

| Project | Item | Placement | LaTeX target |
|---|---|---|---|
| 8 | Main task | Positive and mass-conserving Markov semidiscretization | `src:p8main` |
| 8 | 1 | Centered-difference scheme and its limitations | `src:p8q1` |
| 9 | 1 | Affine ODE and variation of constants | `src:p9q1` |
| 9 | 2 | Composition, inverse, and time-reversal of flows | `src:p9q2` |
| 9 | 3 | Variational matrix and noncommuting-matrix correction | `src:p9q3` |
| 9 | 4 | Liouville--Jacobi determinant theorem | `src:p9q4` |
| 9 | 4 (numerics) | Euler/RK4 Jacobian error and convergence order | `src:p9q4discrete` |
| 9 | 5 | Volume transport and Reynolds-type identity | `src:p9q5` |
| 9 | 6 | Minimum-energy path and optimal velocity | `src:p9q6` |
| 9 | 7 | Pushforward dynamics and continuity equation | `src:p9q7` |
| 9 | 8 | Density change-of-variables formula | `src:p9q8` |
| 9 | 9 | Material derivative and transport theorem | `src:p9q9` |
| 9 | 10 | Differential-entropy evolution | `src:p9q10` |
| 9 | 11 | Score evolution and Hessian extension | `src:p9q11` |
| 9 | 12 | Relative-entropy evolution for two flows | `src:p9q12` |
| 9 | 13 | First variation of transported KL divergence | `src:p9q13` |
| 9 | 14 | Transport from a Gaussian to a target law | `src:p9q14` |
| 9 | 15 | Measure-valued kinetic optimal-control problem | `src:p9q15` |
| 10 | 1 | Hamilton equations from the mechanical Hamiltonian | `src:p10q1` |
| 10 | 2 | Energy conservation along trajectories | `src:p10q2` |
| 10 | 3 | Time reversal and momentum reflection | `src:p10q3` |
| 10 | 4 | Symplecticity and preservation of phase volume | `src:p10q4` |
| 11 | 1 | Nonnegativity of relative entropy | `src:p11q1` |
| 11 | 2 | KL asymmetry and unequal-variance Gaussians | `src:p11q2` |
| 11 | 3 | Truncated Gaussian: KL curve and quadratic constrained minimum | `src:p11q3` |
| 11 | 4 | Joint convexity, separate convexity, and Bregman structure | `src:p11q4` |
| 11 | 5 | Gibbs variational identity and exponential tilt | `src:p11q5` |
| 11 | 6 | Donsker--Varadhan dual representation | `src:p11q6` |
| 11 | 7 | Chain rule for relative entropy | `src:p11q7` |
| 11 | 8 | Stein identity and its operator | `src:p11q8` |
| 11 | 9 | $f$-divergence, joint convexity, and NWJ variational form | `src:p11q9` |
| 11 | 10 | Exponential Fenchel dual and finite-state saddle proof | `src:p11q10` |
| 11 | 11 | Shift optimization recovering Donsker--Varadhan | `src:p11q11` |
| 11 | 12 | Logistic classification and density-ratio optimality | `src:p11q12` |
| 11 | 13 | Reward-guided measure optimization and mean-field tilt | `src:p11q13` |
| 12 | 1 | Gaussian conditional distribution | `src:p12q1` |
| 12 | 2 | Noisy conditioning and level-set approximation | `src:p12q2` |
| 12 | 3 | Coarea formula and effective free energy | `src:p12q3` |
| 12 | 4 | Conditional mean-force formula | `src:p12q4` |
| 13 | 1 | Conditional-variance identity and reaction coordinates | `src:p13q1` |
| 13 | 2 | It\^o equation for a collective variable | `src:p13q2` |
| 13 | 3 | Markovian matching of time marginals | `src:p13q3` |
| 14 | 1 | Gaussian stochastic-interpolant statistics | `src:p14q1` |
| 14 | 2 | Conditional interpolant velocity field | `src:p14q2` |
| 14 | 3 | Conditional-score identity | `src:p14q3` |

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
