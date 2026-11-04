# 项目阅读与研究导览

本导览依据当前[文稿](../paper/main.tex)、[基础库](../src/probflow/gaussian.py)、[实验脚本](../experiments/run_benchmarks.py)及仓库内保存的数据整理。它是项目导航与一致性核对记录，不是对全部数学证明的独立审定。

## 研究主线

项目把三个层次接在一起：微观状态如何运动、概率分布如何演化、降低维数或引入近似之后哪些性质仍然成立。

```text
状态与可观测量
    → 确定性流 / 随机过程及生成元
    → 推前测度、连续性方程 / Fokker–Planck 方程
    → 条件测度、自由能与有效系数
    → Markov 边缘匹配 / 条件速度与 score 回归
    → 数值结构检查与动力学统计比较
```

这条主线中的几类对象需要区分：

| 对象 | 在项目中的作用 | 需要保留的区别 |
|---|---|---|
| 状态 `x`、可观测量 `f`、概率律 `μ` | 对应同一系统的微观、观测和统计描述 | 流作用于状态，组合算子作用于函数，推前作用于测度 |
| `L` 与 `L*` | 可观测量生成元与分布演化的伴随算子 | backward 与 forward 方程承担不同角色 |
| 反应坐标 `ξ` 和条件律 | 将微观问题投影到低维 | 连续变量的条件律不能通过零概率事件直接相除 |
| 平衡自由能与动态条件系数 | 分别描述平衡分布和时刻相关的投影动力学 | 非平衡时不能直接替换成平衡条件律 |
| 单时刻边缘与路径统计 | 分别验证分布和动力学 | 相同边缘不保证相关函数、首次通过时间或路径律相同 |
| 回归总体最优解与有限数据模型 | 连接条件期望与可训练模型 | 采样、表达能力、优化和动力学闭合误差需要分别评价 |

## 建议阅读顺序

### 当前目录分组

主要 subsection 从 24 个整合为 14 个。五个主 section 保留，目录显示到 subsection；推导步骤保留为正文内的小标题。

| 主节 | 原 subsection 数 | 现 subsection 数 | 分组依据 |
|---|---:|---:|---|
| 1.1 基础对象 | 6 | 3 | 状态与可观测量 → 概率律 → 变换及其对偶作用；研究路线作为节末总结 |
| 1.2 动力学与概率输运 | 7 | 4 | 状态流几何、可观测量/概率演化、Hamiltonian 应用、熵与自由能 |
| 1.3 条件概率与有效动力学 | 2 | 2 | 条件几何与动态投影是两个清楚区分的层次，保留 |
| 1.4 学习流与离散近似 | 5 | 3 | 速度场及条件回归、输运映射的变分构造、保概率离散化 |
| 1.5 OU 算例 | 4 | 2 | 精确模型及闭合诊断，与数值/学习验证分开 |

1.2 的合并关系为：

| 现标题 | 原内容 | 在论证中的角色 |
|---|---|---|
| 1.2.1 State flows and their geometry | 原 1.2.1–1.2.2 | 先构造流，再研究线性化、Jacobian、体积与数值误差 |
| 1.2.2 Observable evolution and probability transport | 原 1.2.3–1.2.4 | 同一状态流在函数与测度上的对偶作用；生成元连接弱前向方程 |
| 1.2.3 Hamiltonian dynamics: a geometric application | 原 1.2.5 | 流几何的物理应用，明确不是熵理论的额外前提 |
| 1.2.4 Entropy, variational principles, and free energy | 原 1.2.6–1.2.7 | 概率律的函数泛函、凸对偶及统计/热力学应用 |

熵部分内部也按概念重新归组：Stein 恒等式放在 score 之后；两种密度的 KL 演化和 KL 链式法则放在 KL 定义之后；Gibbs、Donsker–Varadhan、`f`-divergence 与 minimax 归入凸对偶；密度比估计、分布优化及热力学自由能分别作为应用。公式、定理、证明、习题、Notice 和图表的内容均保留。`equation` 中的 `label` 继续位于结束环境的上一行。

### 阅读路线

1. **先看模型和结论。** 读第 1.5 节的 OU 平衡、时间依赖条件均值、相关函数反例，再看现有实验数据。明确项目需要解释的现象。
2. **补上动力学语言。** 读第 1.1–1.2 节，理解推前与对偶、非自治流、矩阵基本解和 Jacobian。Hamiltonian 应用展示保体积、辛性和数值能量误差之间的关系。
3. **理解降维为何需要条件概率。** 读第 1.3 节：Gaussian 条件律 → coarea → 平均力 → Itô 投影 → 带适定性前提的边缘匹配。
4. **再读学习与离散化。** 读第 1.4 节，区分条件速度、score、推前 KL 变分与保概率 Markov 离散化。
5. **按原题回查。** 使用[题目映射](source_mapping.md)及目录后的可点击索引；原题编号不是正文节号。

熵与 KL、有效动力学、保结构数值方法现分别位于对应主 section 下的独立 subsection。正文引用使用与层级一致的 `sec:`/`subsec:` 标签；旧 `ch:` 标签作为兼容别名保留在正确的编号与锚点上。

## 代码职责与参数

| 文件 | 提供的对象或操作 | 对应正文 |
|---|---|---|
| [gaussian.py](../src/probflow/gaussian.py) | `CoupledOU`、Gaussian KL、精确矩、条件漂移、平衡时间协方差 | 1.3、1.5 |
| [projected.py](../src/probflow/projected.py) | `solve_projected_moments` 与平衡闭合矩；比较非平衡边缘 | 1.3、1.5 |
| [learning.py](../src/probflow/learning.py) | 仿射最小二乘条件回归与有效漂移换算 | 1.4、1.5 |
| [test_ou.py](../tests/test_ou.py) | 平衡条件结构、动态矩匹配、相关性反例、回归漂移 | 基础库的 4 个测试 |
| [run_benchmarks.py](../experiments/run_benchmarks.py) | 矩阵 ODE、OU 协方差、仿射/神经回归、Markov 半离散化 | 1.2、1.4、1.5 |
| [hamiltonian_benchmark.py](../experiments/hamiltonian_benchmark.py) | 谐振子的显式 Euler 与 velocity Verlet | 1.2 的 Hamiltonian 应用 |
| [project11_kl_benchmarks.py](../experiments/project11_kl_benchmarks.py) | 截断标准正态的精确 KL 曲线、边界最优值核对 | 1.2 的 Project 11.3 |

基础库中的势能为

\[
V(x,y)=\frac a2x^2+\frac c2(y-\kappa x)^2,
\qquad
K=\begin{pmatrix}a+c\kappa^2&-c\kappa\\-c\kappa&c\end{pmatrix}.
\]

`CoupledOU` 的默认参数是 `(a,c,kappa,beta)=(1,2,1.5,1.5)`。正文及综合实验使用 `(0.8,1.7,1.1,1)`，非平衡初始均值为 `(1,-0.8)`，协方差为 `diag(0.12,0.25)`。比较两套实现时必须显式传入后一组参数。

基础库命名 Hessian 矩阵为 `H`，正文和综合实验命名为 `K`，表达的是同一个矩阵。三个实验脚本目前直接实现相应公式，没有调用基础库；减少重复实现是后续维护任务。

## 数据与图的来源

| 结果 | 保存数据 | 图文件名（位于 `paper/figures/`） |
|---|---|---|
| Euler / RK4 行列式收敛 | [jacobian_convergence.csv](../results/benchmarks/jacobian_convergence.csv)、[results.json](../results/benchmarks/results.json) | `jacobian_convergence.pdf` |
| OU 平衡时间协方差反例 | [results.json](../results/benchmarks/results.json) 的 `OU_Cfull_t1`、`OU_Cclosure_t1`；曲线由解析公式生成 | `ou_correlation.pdf` |
| 神经条件回归 | [conditional_regression.csv](../results/benchmarks/conditional_regression.csv) | `conditional_regression.pdf` |
| 仿射 Gaussian 基线 | [affine_regression.csv](../results/benchmarks/affine_regression.csv) | 与神经结果在正文表格中对照 |
| Markov 质量、正性和 KL | [markov_semidiscrete.csv](../results/benchmarks/markov_semidiscrete.csv) | 正文表格；当前无独立图 |
| Hamiltonian 能量和相轨迹 | [hamiltonian_energy.csv](../results/benchmarks/hamiltonian_energy.csv)、[hamiltonian_summary.json](../results/benchmarks/hamiltonian_summary.json) | `hamiltonian_energy.pdf`、`hamiltonian_phase.pdf` |
| 截断正态 KL 与约束目标 | [project11_truncated_gaussian_kl.csv](../results/benchmarks/project11_truncated_gaussian_kl.csv) | `project11_truncated_gaussian_kl.pdf` |

综合实验摘要统一保存在 `results/benchmarks/results.json`；原 `reproduction.log` 的 JSON 与其一致，已删除重复副本。脚本没有保存神经网络权重、训练曲线或完整采样数据。

## 已有结果如何解读

- **非交换性会影响矩阵解。** 综合结果记录了普通指数与数值基本解之间约 `0.09927` 的 Frobenius 误差；行列式仍可用 Liouville 公式精确计算。
- **几何结构会影响长期数值行为。** 谐振子算例中，Euler 的能量增长明显；Verlet 的真实能量误差有界，修改能量漂移接近舍入量级。这是指定算例与步长下的观察，不能直接推广到任意势能或步长。
- **边缘分布不决定动态相关。** OU 反例在平衡下具有相同的 `X` 边缘方差 `1.25`，但滞后 1 的协方差分别约为 `0.798008` 与 `0.561661`。
- **Gaussian 结构是有用的回归基线。** 现有神经 RMSE 为 `0.07427` / `0.09911`，仿射 RMSE 为 `0.07414` / `0.03552`，对应训练量 512 / 4096。两种模型使用相同测试集，但脚本分别抽取训练集；这不是同一训练样本上的配对比较，也不是多种子结论。
- **数值结构检查有明确范围。** Markov 数据验证了记录时刻的质量、正性及 KL 趋势；当前脚本没有执行空间网格加密研究，不能据此声称已经验证空间收敛阶。

## 本次整理的验证

整理前的完整文件快照位于本地 `build/reorganization/before.zip`；该目录不纳入版本控制。
当前文稿的原题索引有 45 项，覆盖 Project 11 的全部 13 题；HNN 附录另有 7 个导航目标。
本轮数学审查前的快照另存于 `build/manuscript-audit/before.zip`。数学修订、全局符号、编号体系、独立公式规范及完整神经复跑的差异见 [manuscript_audit.md](manuscript_audit.md)；使用 `scripts/check_manuscript_audit.py` 核对来源与内容保留。原有纯排版逐字比较不能用来判断经授权的数学修订是否正确。
目录整理及 2026-11-03 的历史验证记录保留于 [CHANGELOG.md](CHANGELOG.md)。

## 后续工作顺序

先完善复现记录：在一个环境中安装完整依赖，记录版本与运行命令，保存神经网络权重和多种子误差。再统一代码中的 OU 参数与重复公式，为矩阵 ODE、Hamiltonian 和 Markov 实验补充独立检查。随后执行非线性双阱研究，并报告时间步、采样误差、相关时间和首次通过统计的不确定性。

双阱势的平衡自由能在正文中已有解析表达式，但其非平衡条件漂移与完整投影过程的转移统计仍需数值研究。更远期的主题见[后续研究计划](roadmap.md)。

## Current scope and acceptance criteria

### Mathematical backbone

\(X_t\to\mathcal L,\mathcal L^*\to\rho_t\to\nu_t=\xi_\#\rho_t\to\mathbb E[\mathcal L(\varphi\circ\xi)\mid\xi(X_t)=z]\to(b_t,a_t)\to\) Markovian marginal projection. At equilibrium, disintegration of the Gibbs measure produces free energy \(F(z)\) and mean force. For gradient diffusions, relative entropy to Gibbs is a Lyapunov function. A probability-flow velocity converts a Fokker–Planck evolution into a continuity equation when density and coefficients are sufficiently regular.

### Current coverage

| Area | Material currently present | Remaining validation or extension |
|---|---|---|
| State / observable / measure language | Section 1.1 definitions and duality | Independent mathematical review |
| Deterministic transport and information identities | Project 9.1–9.15; Project 11.1–11.13 in §§1.2 and 1.4 | Review hypotheses; distinguish formal kinetic stationarity from an optimizer theorem |
| Hamiltonian application | Project 10.1–10.4, oscillator formulas, Euler / Verlet data and two figures in §1.2 | Broader potentials and step-size studies |
| Conditional geometry and effective dynamics | Project 12.1–12.4 and 13.1–13.3 in §1.3 | Review regularity, integrability and forward-equation well-posedness assumptions |
| Learned flow construction | Project 14.1–14.3 and a finite-sample conditional-regression experiment | Multi-seed training, saved models, dynamical validation |
| Numerical probability evolution | Project 8 generator / centered-scheme analysis, mass / positivity / KL data | Spatial refinement and an independent fine-grid reference |
| Coupled OU model | Exact Gaussian moments, projected drift, correlation counterexample, affine and neural regression | Unify experiment and library implementations; expand tests |
| Nonlinear double well | Analytic equilibrium free energy and a research protocol | Numerical experiment remains unexecuted |

The presence of a proof in the manuscript is recorded as manuscript coverage, not as independent verification of all mathematical claims. Existing Python tests cover the reusable OU core, not every area above.

### Next priorities

1. Establish and record one complete experiment environment, including PyTorch and SciPy; preserve code version, dependency versions and run outputs.
2. Add multiple seeds and uncertainty summaries to the conditional-regression comparison. The current neural error is not monotone in training size.
3. Reduce repeated OU formulas across the library and experiment script, with explicit shared parameters and checks for new numerical components.
4. Execute the nonlinear double-well benchmark. Validate known equilibrium free energy separately from nonstationary drift, correlations and transition statistics.
5. Develop specialized later modules only after selecting a concrete question; see [future research modules](roadmap.md).

### Proof checklist

- Specify stochastic basis, Brownian dimensions, coefficient regularity and growth conditions.
- Justify existence of the diffusion, any invariant measure, and differentiability/integrability exchanges.
- Use \(\mathcal L\) for observables and \(\mathcal L^*\) for distributions.
- Distinguish pushforward measure from a process with a Markov property.
- State precisely which boundary conditions give flux conservation.
- For mimicking, require sufficient conditions for weak solutions and uniqueness of the induced Fokker–Planck problem; the weak identity by itself does not ensure existence or uniqueness.
- For AI, compare conditional-mean regression to exact or high-accuracy estimators, and track probability error separately from trajectory error.

### Numerical checks

- Strong/weak convergence of the integrator as relevant; discrete mass conservation and positivity.
- Exact Gaussian time-marginal baselines before nonlinear models.
- Mean, covariance, stationary two-time covariance, and distributional distances.
- Initial states both at equilibrium and out of equilibrium.
- Error sources split by sampling, function approximation, time discretization, and model reduction.

### Deliverable format

`paper/main.tex` 保留全部文稿内容；`paper/preamble.tex` 集中字体、公式间距、定理环境与页面设置。
`paper/ref.bib` 保存参考文献，`paper/figures/` 保存文稿实际使用的 PDF 图。
`src/` 与 `tests/` 保存基础库和测试；`experiments/` 只保存实验源码，数据统一位于 `results/benchmarks/`。
编译产物位于 `paper/Tmp/`，本地整理快照及视觉检查位于 `build/reorganization/`，均被 Git 忽略。
运行命令统一见 [reproduction.md](reproduction.md)。

## Project 11: mathematical qualifications


- Project 11.3's optimum `b=0` assumes the original constraint `b >= 0` and potential `U(x)=alpha*x^2/2` with `alpha>0`.
- Project 11.6 proves both Fenchel conjugacy directions, and distinguishes bounded tests from unrestricted log ratios.
- Project 11.9 gives a fully explicit proof under positivity/integrability hypotheses, explaining the boundary/singular-measure qualification.
- Project 11.10 derives the minimax formula in a finite positive-state setting by finding a saddle point, rather than invoking Sion's theorem on noncompact function spaces without verifying its hypotheses.
- Project 11.13 proves existence and uniqueness under specific regularity hypotheses and then derives the mean-field exponential self-consistency formula under further positivity/differentiability conditions.
