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

另一种安装方式是 `python -m pip install -r requirements.txt`，它安装完整实验所需依赖，但不安装本地 `probflow` 包及 pytest；需要运行测试时再执行 `python -m pip install -e ".[dev]"`。

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
python experiments/hamiltonian_benchmark.py
python experiments/run_benchmarks.py
```

脚本根据自身位置确定仓库根目录，不依赖启动时的当前目录。上面的相对脚本路径需要从仓库根目录调用。

| 脚本 | 生成的数据（`experiments/`） | 生成的图（`paper/figures/`） |
|---|---|---|
| `hamiltonian_benchmark.py` | `hamiltonian_energy.csv`、`hamiltonian_summary.json` | `hamiltonian_energy`、`hamiltonian_phase`，各含 PDF/PNG |
| `run_benchmarks.py` | `jacobian_convergence.csv`、`conditional_regression.csv`、`affine_regression.csv`、`markov_semidiscrete.csv`、`results.json` | `jacobian_convergence`、`ou_correlation`、`conditional_regression`，各含 PDF/PNG |

重跑会覆盖这些结果。历史文件 `experiments/reproduction.log` 不会自动更新；保存新日志时使用新文件名，例如 PowerShell 中：

```powershell
python experiments/run_benchmarks.py > experiments/run_benchmarks.local.log
```

两种脚本使用 Matplotlib 的 `Agg` 后端，不弹出图形窗口。综合脚本在写入结果之前导入 PyTorch，缺少该依赖时会提前报错。

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

输入是 [main.tex](../paper/main.tex)、[ref.bib](../paper/ref.bib) 和 `paper/figures/` 中的 5 张 PDF 图。仓库已保存这些图，因此阅读和编译已有结果不要求先运行神经训练。

推荐从仓库根目录运行：

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

字体优先使用 Times New Roman 和 Consolas；缺少时尝试 Tinos、DejaVu Sans Mono。还需安装文稿中使用的宏包，包含 `amsmath`、`amsthm`、`tikz`、`tcolorbox`、`biblatex` 等。

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

本次整理的实际执行范围见[验证记录](project_guide.md#验证状态2026-11-03)。
