# LaTeX 文稿审查与修订记录 — 2026-11-04

本轮依据用户提供的 **Comprehensive LaTeX Manuscript Audit and Revision** 提示词，直接修改现有英文笔记。保留五个主 section、独立 HNN 附录、所有习题、Notice、证明、来源编号、图表与原始实验数据；允许修正确认的数学错误和假设缺口。

审查基准是本轮开始时的本地工作区，快照为 `build/manuscript-audit/before.zip`。本记录区分证明审查、结构检查和实际计算；编译通过不等于数学正确性的证明。

后续已按内容联系整合目录：主要 subsection 从 24 个减少为 14 个，目录缩至一页。1.2 从七组合并为四组，并调整 Stein、KL 演化及链式法则的位置。所有公式、陈述、证明、习题、Notice 与图表内容逐块比较保持一致；当前分组与合并理由见[项目导览](project_guide.md#当前目录分组)。目录调整前另有本地快照 `build/structure-consolidation/before.zip`。

## 数学错误与证明缺口

| 位置 | 修订与判断 |
|---|---|
| Picard 与流定理 | 补充闭球内连续曲线空间的完备性、重叠区间唯一性、反向时间、增长估计和有限时间延拓。用差商余项与 Gronwall 证明空间可微性，避免先假定流可微再对其求导的循环。 |
| 基本解矩阵 | 删除错误的“令 `r=t` 即得逆矩阵”的代入说明。分别把 `(a,b,c)` 取为 `(s,t,s)` 和 `(t,s,t)`，从 `U(a,b)U(b,c)=U(a,c)` 得到左右逆。补充 Peano–Baker 导数级数的收敛界。 |
| 非交换性 | 保留原有修正 Notice；另给出两个幂零矩阵的分段常值反例，精确比较有序乘积与普通指数，避免仅凭非零交换子便断言某个具体终点不等。 |
| 生成元 | 指明光滑测试函数、局部一致极限与所选 Banach 空间的范数定义域。用平移作用于指标函数的反例说明 `B_b(V)` 上不能默认强连续。区分终端时间导数与初始时间的 backward equation。 |
| 熵、score、Hessian、KL 微分 | 明确正密度、混合导数、局部时间可积支配和边界条件。先证明 Jacobian 行列式为正再取对数。检查 score/Hessian 的转置、张量项及 KL 速率符号。 |
| KL 对偶及链式法则 | 补全无限 KL 的截断论证；区分有界测试类内的最优解与扩大测试类后的公式。链式法则显式构造条件密度比，说明负部可积，避免无依据地对无限积分使用 Fubini；补上乘积律的加性结论。 |
| 凸性与变分定义域 | 处理混合权重端点和 `0 × ∞` 约定；说明 Bregman 方向导数的可行方向与支配条件。`f`-divergence 的取得最优值仍限于明示的正密度、可积 discriminator 条件。有限状态 minimax 仍通过已验证鞍点证明。 |
| 奖励依赖于分布的优化 | 给出 KL 子水平集紧性的显式估计及弱下半连续的理由。非线性奖励例子增加单调标量固定点论证和精确的“KL + 平方项”目标差恒等式，补上正密度和自洽公式的论证。 |
| 条件几何与 noisy limit | 条件面测度只在正且有限的切片归一化处定义。不能仅凭 regular value 便断言指定点的 noisy posterior 极限；现给出切片连续性的充分条件，并用 Gaussian approximate identity 证明。补充 mean-force 积分与 cutoff 条件。 |
| Markovian projection | 明确条件矩的联合可测版本、漂移/方差可积性、选定的 Markov 弱解及前向方程唯一性类别。结论仅为一时刻边缘相同，不推断路径律相同。 |
| 随机插值 | 用 `mu_t = Law(I_t)` 表示测度，并证明测度值弱连续性方程；只有绝对连续时才引入密度 `rho_t`。加入 Dirac 反例，说明一般插值未必有密度，也不自动产生全局 ODE 流。 |
| 输运与形式最优性 | 密度的 pushforward 明确写成测度等式；全局 quantile flow 增加 onto、正导数及可逆性假设。形式最优性系统以存在光滑乘子为条件，并保留质量约束产生的时间 gauge 和终端常数。 |
| 数值、OU 与 HNN | 展开 Markov 指数矩阵正性与逐边熵耗散的证明。OU 正定性使用二次型，不只使用行列式；通过显式解证明不变概率律唯一。HNN 的摆坐标映射限定为局部角坐标或 universal cover，并说明有限时间三阶误差估计的前提。 |

逐项审查清单见 [manuscript_statement_review.csv](manuscript_statement_review.csv)：共 80 项，含 72 个编号陈述及 8 个 Notice。44 个 proof 和 8 个 solution 全部保留。清单记录的是在明示假设下的推理审查，不是形式化证明证书。

## 符号、环境与结构

- 基础框架统一为 `V = R^d`、`B(V)`、`A = B_b(V)`、`P(V)`；一般可测空间 `E` 仅在明确引入的随机/信息论语境使用。开球与 open set 在 Borel 定义之前解释。
- `mathsf U` 作用于 observables，`mathsf T` 推前概率测度，`mathsf P` 表示 Markov transition；基本解矩阵仍为 `U(t,s)`，变分矩阵仍为 `M_{s,t}(x)`。定义中写明作用空间和复合顺序。
- 微分熵改为 `mathscr S(rho)`，与 Hamiltonian `H(q,p)` 区分。局部势能 `V(x)`、free-energy functional 与样本空间 sigma-algebra 的含义明确说明。
- 所有 Definition 统一为同一个绿色盒子环境。Theorem、Proposition、Corollary、Definition、Example、Exercise、Remark 等共享一个按 chapter 重置的计数器；PDF 中 `1.1–1.72` 连续且各出现一次。
- 无编号展示公式全部为 `equation*`，多行嵌套 `aligned`；不再使用 `\[...\]`、`align*` 或 `\qquad`。行内公式使用 `$...$`，标题的 `\\[5pt]` 保留。
- 原有 145 个公式编号全部保留。四组确实分别编号的 `align` 保留：Itô 投影、投影系数、OU 矩、OU 两个协方差；其余单编号多行公式改为 `equation + aligned`。
- 第一节保持必要基础链；Markov kernel/generator 位于 ODE 之后，条件概率、反应坐标与路径统计区分位于条件动力学节。主 subsection 现按主题整合为 3/4/2/3/2 组，局部推导用正文内小标题承接；五个主 section 和附录六个 section 不变。
- 新增与层级匹配的 `sec:`/`subsec:` 标签，原来的 `ch:` 等标签作为兼容别名保留在正确计数器上；修正误称 Chapter 的引用。全部 266 个原标签和原来源索引条目保留。
- 对 52 个入口进一步核对实际 destination 坐标及其邻近正文。Project 9.6 和 9.13 的旧落点跨页后错过标题，现改为与对应 Example/Theorem 共用起始锚点；来源标记增加了禁止在正文开头前分页的约束。

## 实际验证

| 项目 | 结果 |
|---|---|
| 整体构建 | PowerShell、Bash 两个入口均成功完成 XeLaTeX / Biber 构建；当前 PDF 78 页 A4。Biber 仅在其调用期间使用 `LC_ALL=C`，修复继承 locale 的 Perl 警告，随后恢复环境。 |
| 引用与编号 | 275 个唯一标签、8 个文献键；72 个陈述编号连续且唯一；145 个原公式编号未丢失。 |
| PDF 导航 | 实际解析 PDF 链接和目标页，45 个原题入口、7 个 HNN 入口均与标签对应；层级锚点也检查了 section/subsection 类型。 |
| 内容保留 | 22 份原始数据、基础源码、图像、文献和原题/索引文件逐字节未变；六张 PDF 图、图表环境、所有 sourcecredit/citation 均保留。 |
| 公式检查 | [check_math_identities.py](../scripts/check_math_identities.py) 的 26 项 SymPy 1.14.0 精确代数检查通过，包括 Verlet 不变量、Hessian 张量式、OU 协方差、logistic/JS 和非交换反例。 |
| 基础测试 | 4 项 OU pytest 测试通过。 |
| 实验复跑 | 三份实验脚本全部在隔离目录执行，包括完整 PyTorch 训练；没有覆盖原论文数据或图片。环境为 Python 3.11.15、NumPy 2.4.4、SciPy 1.17.1、Matplotlib 3.10.9、PyTorch 2.11.0+cu128，训练使用 CPU。 |
| 历史与新数据 | 确定性计算、OU、Markov、仿射回归及 Hamiltonian 结果吻合至浮点误差。神经网络 4096 样本 RMSE 有差异，见下节。 |
| 原题核对 | 33 页原 PDF 可读取；重点视觉核对第 17 页，确认 11.3 的约束为 `b >= 0`。原来源编号和未署名/年份不明的状态不变。 |
| 编译诊断 | 无 undefined references、missing citations、duplicate labels/destinations、missing character 或 Overfull；保留 22 处 Underfull 提示，须结合视觉检查解释。 |

视觉检查覆盖整本文稿缩略图及重点定义、长公式、索引、表格和附录页；渲染与详细机器记录保存在本地 `build/manuscript-audit/`。

## 神经复现差异与未验证事项

| 训练样本数 | 原保存神经 RMSE | 本次完整复跑神经 RMSE |
|---|---:|---:|
| 512 | 0.0742657483 | 0.0742657706 |
| 4096 | 0.0991135389 | 0.0931584165 |

原表格和原图保留，正文新增了复核说明。本次环境使用已有 `vae` Python，并仅在隔离子进程中追加另一套同为 CPython 3.11 的现有 SciPy 路径；没有安装包或永久修改环境。环境与比较数据见 [comparison.json](../results/audit-2026-11-04/comparison.json) 和 [environment.json](../results/audit-2026-11-04/environment.json)。原训练环境未完整冻结，不能据本次差异断定唯一原因，也不能声称原神经数值已经逐位复现。

一般无限维 minimax、奇异测度的全套 `f`-divergence 变分取得条件，以及超出本文明示假设的全局适定性，不属于现有有限证明的结论。非线性双阱数值研究、HNN 迁移实验、多种子训练及其不确定性分析仍未执行。新给出的充分条件不声称是最弱条件；研究用途仍需人工复核具体模型是否满足它们。

## 文献与来源核对范围

未新增或杜撰文献；[ref.bib](../paper/ref.bib) 保持不变，全部引用键可解析。以下原始论文或出版方页面用于核对元数据及文中定位，不表示已逐句审定这些外部全文：

- [Stochastic Interpolants，JMLR 正式出版页](https://jmlr.org/papers/v26/23-1605.html)：作者、题名、2025、26(209)、1–80。
- [Flow Matching，ICLR 2023 原论文](https://openreview.net/pdf?id=PqvMRDCJT9t)：作者、题名及会议；保留现有可解析的作者姓名写法。
- [Hamiltonian Neural Networks，作者 arXiv 记录](https://arxiv.org/abs/1906.01563)：作者、题名与 NeurIPS 2019 说明。
- [Gyöngy 1986，出版方记录](https://link.springer.com/article/10.1007/BF00699039)：题名、期刊、卷页与 DOI；正文的投影定理仍按本文明示条件单独论证。
- [JKO，SIAM 出版页](https://epubs.siam.org/doi/10.1137/S0036141096303359)、[Villani，Springer 出版页](https://link.springer.com/book/10.1007/978-3-540-71050-9)、[Pavliotis，Springer 出版页](https://link.springer.com/book/10.1007/978-1-4939-1323-7)：原有书目信息及主题对应。
- 原 assessment 的本地 PDF 只作为 Project/item 来源；不推断未提供的作者、年份或出版信息。

## 重复运行检查

```bash
python scripts/check_project.py
python scripts/check_manuscript_audit.py --baseline build/manuscript-audit/before.zip
python scripts/check_math_identities.py
python -m pytest -q
```

数学恒等式脚本需要 `python -m pip install -e ".[audit]"`；基础测试需要可编辑安装本地包及 `dev` 依赖。编译仍使用根目录的 `build.ps1` 或 `build.sh`。`check_project.py --baseline` 的严格逐字数学内容模式只适用于纯排版变更；本轮有已审查数学修订，保留检查应使用上面的独立 audit checker。
