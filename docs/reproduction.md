# 安装、测试与复现

以下路径均以仓库根目录为起点。项目有两种独立运行需求：Python 数值实验，以及 XeLaTeX 文稿编译；读取已有实验数据不需要安装 PyTorch。

## Python 环境

包元数据要求 Python 3.10+；现有实验脚本原始说明使用 Python 3.11，仓库没有完整的锁定环境文件。基础依赖为 NumPy、SciPy、Matplotlib；pytest 和 PyTorch 分别属于 `dev`、`experiments` 可选依赖。

Windows PowerShell 可创建项目内虚拟环境，并直接调用其中的 Python，无需激活脚本：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe -m pytest -q
```

下文使用 `python` 表示所选环境的解释器；若没有激活该环境，用 `.\.venv\Scripts\python.exe` 替代。

完整实验安装：

```bash
python -m pip install -e ".[dev,experiments]"
```

另一种安装方式是 `python -m pip install -r requirements.txt`，它通过 `pyproject.toml` 安装本地包与完整实验依赖；需要运行测试时再执行 `python -m pip install -e ".[dev]"`。

完整实验使用 CPU 上的 PyTorch 网络，不要求 CUDA。检查依赖是否在**同一个解释器**下可导入：

```bash
python -c "import numpy, scipy, matplotlib, torch; print(torch.__version__)"
```

## 测试基础库

```bash
python -m pytest -q
```

当前 4 个测试覆盖：平衡协方差与条件结构、时间依赖投影的均值/方差匹配、平衡闭合的时间相关性差异、仿射回归得到的有效漂移。它们不覆盖全部正文证明、神经训练、Hamiltonian 和 Markov 实验。

若不安装本地包，也可以在 PowerShell 临时指定源码路径运行已有测试：

```powershell
$env:PYTHONPATH = (Join-Path (Get-Location) 'src')
python -m pytest -q
```

## 运行实验

```bash
python experiments/project11_kl_benchmarks.py
python experiments/hamiltonian_benchmark.py
python experiments/run_benchmarks.py
```

脚本根据自身位置确定仓库根目录，不依赖启动时的当前目录。上面的相对脚本路径需要从仓库根目录调用。

| 脚本 | 生成的数据（`results/benchmarks/`） | 生成的图（`paper/figures/`） |
|---|---|---|
| `hamiltonian_benchmark.py` | `hamiltonian_energy.csv`、`hamiltonian_summary.json` | `hamiltonian_energy`、`hamiltonian_phase`，PDF |
| `project11_kl_benchmarks.py` | `project11_truncated_gaussian_kl.csv` | `project11_truncated_gaussian_kl.pdf` |
| `run_benchmarks.py` | `jacobian_convergence.csv`、`conditional_regression.csv`、`affine_regression.csv`、`markov_semidiscrete.csv`、`results.json` | `jacobian_convergence`、`ou_correlation`、`conditional_regression`，PDF |

重跑会覆盖对应的 CSV/JSON 与 PDF 图。三份脚本共用 `experiments/_paths.py` 中的输出位置，不再生成根目录 `figures/` 或 PNG 副本。
历史 `reproduction.log` 与综合摘要相同，已删除重复文件。需要保存新日志时可运行：

```powershell
python experiments/run_benchmarks.py > results/benchmarks/run_benchmarks.local.log
```

三种脚本使用 Matplotlib 的 `Agg` 后端。综合脚本需要 PyTorch，Project 11 与 Hamiltonian 脚本无需 PyTorch。

### 综合实验参数

- 随机种子：`20261102`，分别设置 NumPy generator 与 PyTorch seed。
- OU 参数：`a=0.8, c=1.7, kappa=1.1, beta=1`。
- 非平衡初值：均值 `(1,-0.8)`，协方差 `diag(0.12,0.25)`；回归时刻为 `0.25, 0.5, 1, 2`。
- 训练量：512 / 4096；测试量：12,000。时刻标签随机抽取，不保证各时刻严格等样本数。
- 网络：输入 `(t,x)`，两层各 48 个 Tanh 隐藏单元；Adam，学习率 `0.008`，260 epochs，batch size 256，CPU 线程数 2。
- 特征和输出标准化仅使用对应神经训练集的均值和标准差。
- 仿射基线：每个离散时刻分别拟合截距和斜率；训练样本与神经模型独立抽取，测试样本相同。
- Markov：`D=0.5`，区间 `[0,1]`，60 单元，矩阵指数传播。该项没有时间步离散，也没有在当前脚本中执行网格加密。

### Hamiltonian 参数

一维谐振子 `omega=1`，初值 `(q0,p0)=(1,0)`，`h=0.1`，1000 步，`T=100`；对照显式 Euler 和 kick–drift–kick velocity Verlet。能量曲线显示至 `T=100`，相轨迹显示至 `T=20`。

## 编译文稿

输入是 [main.tex](../paper/main.tex)、[ref.bib](../paper/ref.bib)、共享排版配置 [preamble.tex](../paper/preamble.tex) 和 `paper/figures/` 中的 6 张 PDF 图。仓库已保存这些图，因此阅读和编译已有结果不要求先运行神经训练。

从仓库根目录一键编译：

```powershell
.\build.ps1
```

macOS / Linux / Git Bash：

```bash
bash build.sh
```

两种入口均生成 `paper/Tmp/main.pdf`，参考文献由 Biber 处理。也可直接运行：

```bash
latexmk -cd -xelatex -outdir=Tmp -synctex=1 -interaction=nonstopmode -halt-on-error paper/main.tex
```

`-cd` 使编译在 `paper/` 中进行，`Tmp` 相对于该目录；`latexmk` 按需调用 Biber 及重复 XeLaTeX。输出是 `paper/Tmp/main.pdf`。

### 手动编译

PowerShell 中从仓库根目录执行：

```powershell
Push-Location paper
New-Item -ItemType Directory -Force Tmp | Out-Null
xelatex -output-directory=Tmp -synctex=1 -interaction=nonstopmode -halt-on-error main.tex
biber --output-directory=Tmp main
xelatex -output-directory=Tmp -synctex=1 -interaction=nonstopmode -halt-on-error main.tex
xelatex -output-directory=Tmp -synctex=1 -interaction=nonstopmode -halt-on-error main.tex
Pop-Location
```

每一步成功后再执行下一步。文稿使用 `biblatex` 的 Biber 后端；BibTeX 不能替代这一步。`main.bcf` 与 `main.bbl` 都位于 `Tmp`，所以 Biber 的输出目录需要匹配 XeLaTeX。

### VS Code

在 VS Code 打开整个仓库根目录，安装 LaTeX Workshop 后打开 `paper/main.tex`，执行 Build LaTeX project。项目的 [.vscode/settings.json](../.vscode/settings.json) 将默认 recipe 设为 `XeLaTeX -> Biber -> XeLaTeX x2`，输出目录为 `%DIR%/Tmp`。

正文字体优先 Times New Roman，缺少时使用 Tinos；等宽字体优先 Consolas，缺少时使用 DejaVu Sans Mono。还需安装文稿中使用的宏包，包含 `amsmath`、`amsthm`、`tikz`、`tcolorbox`、`biblatex` 等。

## 常见问题

| 现象 | 检查方法 |
|---|---|
| `No module named probflow` | 从仓库根目录执行可编辑安装，确认安装与 pytest 使用同一 Python |
| `No module named torch` | 在运行实验的 Python 中安装 `.[experiments]`；仅运行 OU 测试时不需要该依赖 |
| 图片更新后论文仍使用旧图 | 确认输出位于 `paper/figures/`，而不是根目录的 `figures/`，随后重新编译 |
| 所有引用未定义或参考文献为空 | 检查 `paper/Tmp/main.blg` 与 `.bbl`，使用完整 Biber 编译链 |
| 改用 pdfLaTeX 后 `fontspec` 报错 | 按项目配置使用 XeLaTeX |
| 神经误差不等于保存的末位数值 | 记录 Python、NumPy、SciPy、PyTorch 和平台版本；固定 seed 并不提供跨版本逐位一致性 |

## 保存一次可追溯的运行

保留代码版本、Python 与依赖版本、命令、seed、生成数据和对应图片。可运行 `python -m pip freeze` 导出当前环境清单；它描述这次环境，不等于仓库已经提供跨平台锁文件。区分条件均值 RMSE、漂移 RMSE 和对噪声标签的 RMSE，勿混用指标。

## 项目结构与内容核对

```bash
python scripts/check_project.py
```

本轮审查前快照存在时，编译 PDF 后还可核对来源、编号、保留素材及实际跳转目标：

```bash
python scripts/check_manuscript_audit.py --baseline build/manuscript-audit/before.zip
```

可选的精确代数检查：

```bash
python -m pip install -e ".[audit]"
python scripts/check_math_identities.py
```

本轮实际执行了三个实验脚本，包括神经网络训练。原始 `results/benchmarks/` 和论文图没有覆盖；本轮单独的环境与比较记录位于 `results/audit-2026-11-04/`。512 样本神经误差吻合至约 `2.3e-8`，4096 样本神经误差从原记录 `0.09911` 变为本次 `0.09316`，尚未建立逐位复现。完整范围见 [数学与复现审查报告](manuscript_audit.md)，历史整理见 [整理记录](CHANGELOG.md)。
