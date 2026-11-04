# 整理记录 — 2026-11-04

本轮后续数学审校按用户新提供的综合提示词执行，允许修正数学错误和假设缺口。详见 [审查报告](manuscript_audit.md) 与 [逐项审查清单](manuscript_statement_review.csv)。下文纯排版保真、71 页、未重训等结论是前一轮工作的历史记录；当前文稿、页数与完整复跑结果以新报告为准。

本次以整理开始时的本地工作区为基准，未覆盖已有论文和实验修改。

- 根目录统一使用 README；将可点击索引说明合入原题映射，scope 合入研究导览，两份未来计划合入 roadmap。旧变更与验证记录保留在本文件。
- 实验脚本统一使用 `_paths.py`，CSV/JSON 移至 `results/benchmarks/`，论文图统一输出到 `paper/figures/`。
- 删除正文未使用的五份 PNG 预览，以及与 `results.json` 内容一致的 `reproduction.log`；保留全部六张论文 PDF 图、实验数据、原题 PDF 及文献文件。
- 分离 `preamble.tex` 与文稿正文，移除未使用的代码语言模板，统一公式行距和上下间距，对 16 组长公式分行对齐；保留原公式编号、标签、正文和引用。修复前置页重复页锚点。
- 修正构建脚本的工作目录，提供 PowerShell 与 Bash 入口；依赖统一从 `pyproject.toml` 安装。
- 整理前的完整快照：本地 `build/reorganization/before.zip`。正文内容保真与文件路径检查：`scripts/check_project.py`。

## 本次验证

- 内容保真核对通过：去除排版标记后的正文和公式完全一致；编号环境、标题、266 个标签与 8 个文献键保持一致。23 份基础源码、数据及保留素材与整理前逐字节相同。
- PowerShell、Git Bash 两个入口均成功完成 XeLaTeX → Biber → XeLaTeX × 2 编译，输出 71 页 A4 PDF。最终 LaTeX 日志无未定义引用、文献或 Overfull 警告；仍有 21 处 Underfull 提示。
- PDF 的 45 个原题入口及 7 个 HNN 附录入口均指向对应标签。全 71 页已渲染检查缩略图，另检查了 4 张重点公式页的高清预览。
- 4 项 OU 基础测试通过。Project 11 在隔离目录复跑的 701 行数据与保存结果一致至浮点舍入量级（最大差约 `3.6e-15`）；Hamiltonian 的 1001 行数据与摘要一致。
- Python 语法、文档路径、索引表及图片引用检查通过，`git diff --check` 通过。
- 本次未执行完整神经重训，已有训练结果保留。详细本地核对记录位于 `build/reorganization/verification.json`。

正文排版保真指内容与整理前版本一致，不是对数学证明的重新审定。历史数据迁移未覆盖论文中的实验结果。

---

# Change log — 2026-11-03

## Revised scope

Retained the user-uploaded complete chapter as the canonical base (no replacement by an abbreviated summary). Expanded Project 11 from items 1, 5, 6, 7, 8 to **all items 1–13**. Retained all previous Projects 8–10 and 12–14 content and existing figure/experiment assets.

## New mathematical work

- **11.2:** proved KL asymmetry using unequal-variance Gaussians.
- **11.3:** derived the truncated-standard-normal distribution, exact KL formula, derivative, conditional quadratic moment, globally monotone constrained objective, and unique minimizer; produced a reproducible curve and CSV.
- **11.4:** proved joint and separate KL convexity via the perspective/Jensen argument and established the precise finite-entropy Bregman representation.
- **11.6:** added the reverse Fenchel--Legendre identity for the log-partition functional, its convexity proof via Hölder, and optimizer uniqueness.
- **11.9:** defined general f-divergence and convex conjugate, proved joint convexity and a conditional exact variational representation, then specialized to KL.
- **11.10:** proved the exponential Fenchel identity and KL variational formula; derived the source's minimax expression via an explicit saddle point on finite positive discrete spaces, and explained the limitations of formal infinite-dimensional minimax interchanges.
- **11.11:** derived Donsker--Varadhan from the exponential formula by exact optimization over additive constants.
- **11.12:** solved the population logistic classification problem, derived the log-density-ratio optimum and Jensen--Shannon minimum-risk identity, and qualified finite-data assertions.
- **11.13:** proved existence and uniqueness of reward-regularized law optimization under hypotheses, derived the exponential fixed-point necessary condition, and worked a nonlinear self-consistency example.

## Independent HNN supplementary appendix

Restored the previously planned Hamiltonian Neural Network discussion as Appendix A without changing the main chapter's theorem dependency order: canonical equivalence of spring and small-angle pendulum, HNN structural constraints, parameter/coordinate transfer, nonlinear error scaling, proposed falsifiable tests, and flow conjugacy. Added a distinct clickable supplementary index, and an HNN primary literature reference. The appendix reports no new numerical transfer result.

## Project packaging

Moved the existing clickable Source Index to the front matter after the table of contents, indexed all 13 problems, updated the assessment-to-chapter map, added `experiments/project11_kl_benchmarks.py` and new figure/CSV, and refreshed README and build instructions. Preserved the primary assessment PDF and bibliography.

## Verification

- XeLaTeX/Biber compilation succeeded; the PDF has 71 A4 pages.
- No unresolved LaTeX references reported in the final build.
- The 13 Project 11 item hyperlinks and seven HNN supplementary links have non-empty internal PDF destinations.
- The new truncated-normal script ran and asserted its analytic boundary values.
- Selected PDF pages, mathematical displays, source-index pages, figure, and bibliography were visually checked.

The pre-existing finite-data neural experiment is carried forward from the prior source package rather than rerun in this edit. The broader 33-page problem portfolio still contains projects not selected for this one-chapter manuscript.

## 历史验证记录：2026-11-03


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
