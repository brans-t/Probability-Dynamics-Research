# Probability Dynamics Lab

围绕**随机动力学、粗粒化与学习概率流**的研究笔记与可复现实验。

论文总题为 *A Unified Framework for Stochastic Dynamics, Coarse-Graining, and Learned Probability Flows*。当前正文只有一个编号章节：*From Algebraic Structures to Probability Dynamics and Learned Flows*，包含五个主要节，以及证明、习题、数值实验、原题索引和参考文献。

核心问题是：如何从微观状态的演化得到概率分布与有效动力学，以及数值模型、回归模型分别保留了哪些结构？贯穿项目的区别是：**匹配所有单时刻边缘分布，不等于匹配时间相关性或路径分布。**

## 从哪里开始

- **读理论**：[论文源码](paper/main.tex)；编译后的 PDF 位于 `paper/Tmp/main.pdf`。
- **理解项目**：[阅读与研究导览](docs/project_guide.md)，包含数学主线、代码职责、已有结果与当前限制。
- **运行项目**：[安装、测试与复现](docs/reproduction.md)。
- **对照原题**：[题目与正文映射](docs/source_mapping.md)；正文末尾还有可点击的 *Source Index and Direct Links*。
- **查看范围与计划**：[当前研究范围](docs/scope.md)、[未纳入主线的项目](docs/remaining_projects.md)、[后续研究模块](docs/future_research_modules.md)。

## 正文结构

| 节 | 标题 | 内容 |
|---|---|---|
| 1.1 | State Spaces, Observables, and Probability Evolution | 状态、可观测量、概率测度、推前与对偶关系 |
| 1.2 | Dynamical Flows and Probability Transport | ODE 流、非交换矩阵演化、Jacobian、连续性方程、Hamiltonian 动力学、熵与 KL |
| 1.3 | Conditional Probability and Effective Dynamics | 条件测度、coarea、平均力、Itô 投影和 Markov 边缘匹配 |
| 1.4 | Learned Flows and Structure-Preserving Approximation | 随机插值、条件速度与 score、变分输运、保概率离散化 |
| 1.5 | A Coupled OU Benchmark: Exact, Numerical, and AI Results | 耦合 Ornstein–Uhlenbeck 模型、精确解、条件回归与数值核对 |

正文整合了 Project 9 的 1–15 题、Project 10 的 1–4 题，以及 Projects 8、11–14 的选定题目。Project 9.15 给出指定终端泛函后的形式驻点条件；非线性双阱扩展仍是研究方案。完整题目清单与限定条件见[映射说明](docs/source_mapping.md)。

题源为随附的 [Student Assessment Exercise](docs/StudentAssessmentExercise_unlocked.pdf)。现有题源记录未确认作者与出版年份，因此不补写这两项。正文通过 `\sourcecredit{project}{item}` 标注题源，通过末尾的映射表和可点击索引保留原题编号。

## 目录

```text
.
├── paper/
│   ├── main.tex                 # 主文稿；唯一的正文维护入口
│   ├── ref.bib                  # 外部文献数据库
│   ├── figures/                 # 正文使用的 5 组 PDF/PNG 图
│   └── Tmp/                     # 编译产物，已忽略
├── src/probflow/
│   ├── gaussian.py             # 耦合 OU 精确矩、条件漂移与 Gaussian KL
│   ├── projected.py            # 投影矩方程及平衡自由能闭合
│   └── learning.py             # 仿射条件回归基线
├── experiments/
│   ├── run_benchmarks.py        # 矩阵 ODE、OU、仿射/神经回归、Markov 离散化
│   ├── hamiltonian_benchmark.py # Euler 与 velocity Verlet 对照
│   └── *.csv, *.json, *.log     # 已保存的实验数据与历史运行输出
├── tests/test_ou.py             # 4 个 OU 数学回归测试
├── docs/                       # 阅读、复现、范围和原题说明；含原题 PDF
├── results/                    # 预留目录；当前脚本不向此处输出论文数据
├── .vscode/settings.json       # XeLaTeX → Biber → XeLaTeX ×2
├── pyproject.toml              # Python 包与可选依赖
└── requirements.txt            # 完整实验依赖的另一种安装入口
```

实验脚本直接实现正文的基准问题；`src/probflow` 是独立的可复用 OU 基础库，两者目前没有统一为一套调用接口。库的默认参数与正文实验参数不同，比较结果时需显式指定参数。

## 快速运行

基础库要求 Python 3.10+。建议在独立 Python 环境中执行以下命令，工作目录为仓库根目录。

仅运行基础库与测试，无需 PyTorch：

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
```

复现完整实验，需额外安装 PyTorch：

```bash
python -m pip install -e ".[dev,experiments]"
python experiments/hamiltonian_benchmark.py
python experiments/run_benchmarks.py
```

两个脚本会覆盖各自生成的 `experiments/*.csv`、`experiments/*.json` 和 `paper/figures/` 中的对应图片。需要保留一次运行结果时，请先复制这些文件。`experiments/reproduction.log` 是已有的历史输出，脚本不会自动更新它。

## 编译论文

需要包含 XeLaTeX、Biber 和文稿所用宏包的 TeX 发行版；命令行自动编译还需要 `latexmk`。

从仓库根目录运行：

```bash
latexmk -cd -xelatex -outdir=Tmp -synctex=1 -interaction=nonstopmode -halt-on-error paper/main.tex
```

输出为 `paper/Tmp/main.pdf`。也可在 VS Code 中打开仓库根目录，使用 LaTeX Workshop 编译 `paper/main.tex`；项目配置会执行完整的 Biber 编译链。

文稿使用 `fontspec`，需 XeLaTeX；文献使用 `biblatex` 的 `backend=biber`，需 Biber。仅运行一次 XeLaTeX 会留下未解析引用。没有 `latexmk` 时，按[手动编译步骤](docs/reproduction.md#手动编译)执行。

## 已保存的结果

以下数值来自仓库中现有的 [results.json](experiments/results.json) 和 [hamiltonian_summary.json](experiments/hamiltonian_summary.json)，不能将其视为每次运行都会精确相同的输出。

| 基准 | 现有记录 |
|---|---|
| 非交换矩阵 ODE | 精确行列式 `exp(-0.15)`；最细步长下 Euler / RK4 行列式误差约为 `4.142e-3` / `7.447e-12` |
| Hamiltonian 谐振子 | `h=0.1, T=100`；Euler 末态能量约 `10479.577819`；Verlet 最大能量绝对误差约 `0.00125` |
| OU 时间协方差 | 同样的平衡边缘分布下，滞后 1 的完整模型 / 闭合模型协方差约为 `0.798008` / `0.561661` |
| 条件均值回归 | 4096 个训练样本时，神经网络 / 仿射基线 RMSE 约为 `0.09911` / `0.03552` |
| Markov 半离散化 | 60 个网格单元；记录时刻的质量误差小于 `2e-13`，单元质量保持正值，离散 KL 下降 |

回归实验使用单个随机种子 `20261102` 和 12,000 个独立测试样本。神经网络在 4096 个训练样本时的误差高于 512 个样本时；现有结果不支持“样本越多神经网络就越准确”的结论。完整实验的依赖版本尚未锁定，跨环境复现应比较误差量级和结构性质，而非要求所有末位数字相同。

本次整理的核对记录与尚未执行的验证见[导览中的验证状态](docs/project_guide.md#验证状态2026-11-03)。

## 后续重点

1. 记录完整实验环境与多随机种子结果，扩充模型及数值方法的回归检查。
2. 减少实验脚本与 `src/probflow` 的重复公式，并显式统一参数。
3. 执行双阱基准，检查非平衡条件漂移、相关时间与首次通过统计。
4. 按独立研究模块推进 Jarzynski、Feynman–Kac、bridge 和 JKO 等主题。

代码仓库附有 [MIT License](LICENSE)。题源及原题编号的维护方式见[映射说明](docs/source_mapping.md)。
