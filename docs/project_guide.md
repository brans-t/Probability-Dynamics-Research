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

1. **先看模型和结论。** 读第 1.5 节的 OU 平衡、时间依赖条件均值、相关函数反例，再看现有实验数据。明确项目需要解释的现象。
2. **补上动力学语言。** 读第 1.1–1.2 节，理解推前与对偶、非自治流、矩阵基本解和 Jacobian。Hamiltonian 应用展示保体积、辛性和数值能量误差之间的关系。
3. **理解降维为何需要条件概率。** 读第 1.3 节：Gaussian 条件律 → coarea → 平均力 → Itô 投影 → 带适定性前提的边缘匹配。
4. **再读学习与离散化。** 读第 1.4 节，区分条件速度、score、推前 KL 变分与保概率 Markov 离散化。
5. **按原题回查。** 使用[题目映射](source_mapping.md)及正文末尾的可点击索引；原题编号不是正文节号。

熵与 KL 的内容目前属于第 1.2 节内的段落，有效动力学属于第 1.3 节内的段落，保结构数值方法属于第 1.4 节内的段落。部分 LaTeX 标签仍使用历史前缀 `ch:`，其实际引用位置以正文为准。

## 代码职责与参数

| 文件 | 提供的对象或操作 | 对应正文 |
|---|---|---|
| [gaussian.py](../src/probflow/gaussian.py) | `CoupledOU`、Gaussian KL、精确矩、条件漂移、平衡时间协方差 | 1.3、1.5 |
| [projected.py](../src/probflow/projected.py) | `solve_projected_moments` 与平衡闭合矩；比较非平衡边缘 | 1.3、1.5 |
| [learning.py](../src/probflow/learning.py) | 仿射最小二乘条件回归与有效漂移换算 | 1.4、1.5 |
| [test_ou.py](../tests/test_ou.py) | 平衡条件结构、动态矩匹配、相关性反例、回归漂移 | 基础库的 4 个测试 |
| [run_benchmarks.py](../experiments/run_benchmarks.py) | 矩阵 ODE、OU 协方差、仿射/神经回归、Markov 半离散化 | 1.2、1.4、1.5 |
| [hamiltonian_benchmark.py](../experiments/hamiltonian_benchmark.py) | 谐振子的显式 Euler 与 velocity Verlet | 1.2 的 Hamiltonian 应用 |

基础库中的势能为

\[
V(x,y)=\frac a2x^2+\frac c2(y-\kappa x)^2,
\qquad
K=\begin{pmatrix}a+c\kappa^2&-c\kappa\\-c\kappa&c\end{pmatrix}.
\]

`CoupledOU` 的默认参数是 `(a,c,kappa,beta)=(1,2,1.5,1.5)`。正文及综合实验使用 `(0.8,1.7,1.1,1)`，非平衡初始均值为 `(1,-0.8)`，协方差为 `diag(0.12,0.25)`。比较两套实现时必须显式传入后一组参数。

基础库命名 Hessian 矩阵为 `H`，正文和综合实验命名为 `K`，表达的是同一个矩阵。两个实验脚本目前直接实现相应公式，没有调用基础库；减少重复实现是后续维护任务。

## 数据与图的来源

| 结果 | 保存数据 | 图文件名（位于 `paper/figures/`） |
|---|---|---|
| Euler / RK4 行列式收敛 | [jacobian_convergence.csv](../experiments/jacobian_convergence.csv)、[results.json](../experiments/results.json) | `jacobian_convergence.pdf/.png` |
| OU 平衡时间协方差反例 | [results.json](../experiments/results.json) 的 `OU_Cfull_t1`、`OU_Cclosure_t1`；曲线由解析公式生成 | `ou_correlation.pdf/.png` |
| 神经条件回归 | [conditional_regression.csv](../experiments/conditional_regression.csv) | `conditional_regression.pdf/.png` |
| 仿射 Gaussian 基线 | [affine_regression.csv](../experiments/affine_regression.csv) | 与神经结果在正文表格中对照 |
| Markov 质量、正性和 KL | [markov_semidiscrete.csv](../experiments/markov_semidiscrete.csv) | 正文表格；当前无独立图 |
| Hamiltonian 能量和相轨迹 | [hamiltonian_energy.csv](../experiments/hamiltonian_energy.csv)、[hamiltonian_summary.json](../experiments/hamiltonian_summary.json) | `hamiltonian_energy.pdf/.png`、`hamiltonian_phase.pdf/.png` |

[reproduction.log](../experiments/reproduction.log) 保存了历史运行的 JSON 输出，没有依赖版本、命令时间或机器配置，不能单独作为完整复现环境记录。脚本没有保存神经网络权重、训练曲线或完整采样数据。

## 已有结果如何解读

- **非交换性会影响矩阵解。** 综合结果记录了普通指数与数值基本解之间约 `0.09927` 的 Frobenius 误差；行列式仍可用 Liouville 公式精确计算。
- **几何结构会影响长期数值行为。** 谐振子算例中，Euler 的能量增长明显；Verlet 的真实能量误差有界，修改能量漂移接近舍入量级。这是指定算例与步长下的观察，不能直接推广到任意势能或步长。
- **边缘分布不决定动态相关。** OU 反例在平衡下具有相同的 `X` 边缘方差 `1.25`，但滞后 1 的协方差分别约为 `0.798008` 与 `0.561661`。
- **Gaussian 结构是有用的回归基线。** 现有神经 RMSE 为 `0.07427` / `0.09911`，仿射 RMSE 为 `0.07414` / `0.03552`，对应训练量 512 / 4096。两种模型使用相同测试集，但脚本分别抽取训练集；这不是同一训练样本上的配对比较，也不是多种子结论。
- **数值结构检查有明确范围。** Markov 数据验证了记录时刻的质量、正性及 KL 趋势；当前脚本没有执行空间网格加密研究，不能据此声称已经验证空间收敛阶。

## 验证状态（2026-11-03）

本次整理只对下列可由本地文件和执行结果支持的项目给出状态；不将既有结果标为重新训练所得。

| 核对项 | 状态 |
|---|---|
| OU 基础库 | 现有 4 个 pytest 测试通过；使用 `src` 导入路径运行 |
| Hamiltonian 实验 | 在临时副本中运行完整脚本，1001 行 CSV 与摘要均与保存结果一致；确认图片写入 `paper/figures/` |
| 非神经数值部分 | 在隔离目录执行综合脚本中的矩阵 ODE、OU 和 Markov 源码段；重算结果与保存值一致，并核对基础库在显式参数下给出相同 OU 矩阵、协方差与时间协方差 |
| CSV / JSON 对应关系 | 4 份综合实验 CSV 与 `results.json` 对应一致；历史 `reproduction.log` 中的 JSON 与该结果一致 |
| 文献键、原题链接与编译 | 7 个引用键都有文献记录；37 个索引目标标签均存在且已列入映射文档；5 张正文图存在；README 所列 `latexmk` 命令成功生成 51 页 PDF，无未定义引用或空参考文献警告 |
| 文档和配置 | 本地 Markdown 路径与锚点检查通过；Python 语法、TOML 及 VS Code 编译配置解析通过 |
| 神经网络完整重训 | 未执行；本次测试环境缺少 PyTorch，另一现有 PyTorch 环境缺少 SciPy，没有找到可直接运行完整管线的单一环境 |
| 数学证明和外部参考文献 | 已整理正文陈述、限定条件及本地映射；未逐条完成独立证明审查或外部文献元数据核验 |

上述执行使用 Python 3.13.9、NumPy 2.3.5、SciPy 1.16.3、Matplotlib 3.10.6；pytest 版本为 8.4.2。这是本次基础测试与非神经核对环境，不能当作历史神经结果的训练环境。原有论文数据未被这些隔离重跑覆盖。可编辑安装所用的元数据已核对，本次没有执行新的依赖下载或环境安装。

编译还保留 `Underfull \hbox`、可断行盒子收缩及重复页锚点 `@page.i` 警告。它们属于后续排版和 PDF 导航检查事项；本次通过的是构建与引用解析检查，并非完整逐页视觉验收。

## 后续工作顺序

先完善复现记录：在一个环境中安装完整依赖，记录版本与运行命令，保存神经网络权重和多种子误差。再统一代码中的 OU 参数与重复公式，为矩阵 ODE、Hamiltonian 和 Markov 实验补充独立检查。随后执行非线性双阱研究，并报告时间步、采样误差、相关时间和首次通过统计的不确定性。

双阱势的平衡自由能在正文中已有解析表达式，但其非平衡条件漂移与完整投影过程的转移统计仍需数值研究。更远期的主题见[研究模块](future_research_modules.md)。
