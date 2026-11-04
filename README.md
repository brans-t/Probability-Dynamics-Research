# Probability Dynamics Lab

概率动力学、粗粒化与学习概率流的研究文稿和可复现实验。

正文为 *A Unified Framework for Stochastic Dynamics, Coarse-Graining, and Learned Probability Flows*。主章含五节，覆盖 Project 9 的 1–15 题、Project 10 的 1–4 题、Project 11 的全部 13 题，以及 Projects 8、12、13、14 的选定题目。独立 HNN 附录讨论振子与摆的结构迁移，其中计算协议是研究计划。

## 项目入口

| 内容 | 位置 |
|---|---|
| 论文正文 | [paper/main.tex](paper/main.tex) |
| 字体、定理环境、公式和页面排版 | [paper/preamble.tex](paper/preamble.tex) |
| 参考文献 | [paper/ref.bib](paper/ref.bib) |
| 论文图片 | [paper/figures/](paper/figures/)：六张 PDF，均被正文使用 |
| 基础库与测试 | [src/probflow/](src/probflow/)、[tests/](tests/) |
| 实验源码 | [experiments/](experiments/) |
| 保存的实验数据 | [results/benchmarks/](results/benchmarks/)：CSV 和 JSON |
| 原始题目 | [StudentAssessmentExercise_unlocked.pdf](docs/StudentAssessmentExercise_unlocked.pdf) |
| 阅读顺序、结果解读与研究范围 | [项目导览](docs/project_guide.md) |
| 安装、测试、实验和编译 | [复现说明](docs/reproduction.md) |
| 原题映射与 PDF 导航 | [原题映射](docs/source_mapping.md)、[机器可读索引](docs/source_index.tsv) |
| 后续研究计划 | [研究计划](docs/roadmap.md) |
| 整理和历史验证记录 | [变更记录](docs/CHANGELOG.md) |
| 数学、符号、结构与复现审查 | [本轮审查报告](docs/manuscript_audit.md)、[逐项清单](docs/manuscript_statement_review.csv) |

## 编译论文

需要 XeLaTeX、Biber 及文稿使用的宏包。从仓库根目录运行：

```powershell
.\build.ps1
```

macOS / Linux / Git Bash：

```bash
bash build.sh
```

输出为 `paper/Tmp/main.pdf`。编译不需要先重跑实验；论文图片已保留。PDF 目录后的 Source Index 包含 45 个原题入口，Supplementary Index 另有 7 个 HNN 附录入口。

## 测试与实验

Python 3.10+；基础依赖统一维护于 [pyproject.toml](pyproject.toml)。

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
python scripts/check_project.py
```

Project 11 和 Hamiltonian 实验仅需基础依赖；综合实验还需要 PyTorch：

```bash
python -m pip install -e ".[experiments]"
python experiments/project11_kl_benchmarks.py
python experiments/hamiltonian_benchmark.py
python experiments/run_benchmarks.py
```

实验共用 [输出路径配置](experiments/_paths.py)：数据写入 `results/benchmarks/`，论文图写入 `paper/figures/`。重跑会覆盖相应结果。`requirements.txt` 也从同一份包元数据安装完整实验依赖。

## 范围与内容保留

原始 33 页题集的所有题目尚未全部完成。已有神经回归数据不是多种子结论，非线性双阱数值实验和 HNN 迁移协议仍属于后续研究。

目录整理前的本地快照位于 `build/reorganization/before.zip`；本轮数学审查前的快照位于 `build/manuscript-audit/before.zip`。两者均未纳入版本控制。本轮按审查提示修正了数学问题和假设，保留原有习题、推导、索引、附录及实验数据；详细变化和神经复跑差异见审查报告。

完成 PDF 编译后，可运行以下命令检查内容保留、编号和实际 PDF 链接：

```bash
python scripts/check_manuscript_audit.py --baseline build/manuscript-audit/before.zip
```
