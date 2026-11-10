# Assessment 题目优先级调整报告（2026-11-09）

本次在 [主文稿](../paper/main.tex) 中调整题目优先级，保留原有章节层级、核心定义和理论顺序。Source Index 继续使用原有 `\sourceindexrow` 宏，45 个入口逐项标为 Core、Concise 或 Pending；[机器可读索引](source_index.tsv) 同步更新。

目录中用上标 `\star` 标记仍有待做内容的入口：14 个 Pending 项目，以及仍有暂缓扩展的 9.11 和 13.1，共 16 项。Core / Concise / Pending 分类及机器可读题号保持不变。

## 完整保留的核心题目：17 项

| Project | Core 题目 |
|---|---|
| 9 | 1、2、3、4（解析）、7、8、10 |
| 11 | 1、5、6、7 |
| 12 | 3、4 |
| 13 | 2、3 |
| 14 | 2、3 |

这些题目的陈述、主要推导和证明保留，覆盖 ODE 与流、Jacobian 与密度变换、KL 与 Gibbs/Donsker–Varadhan 结构、条件分解、Markovian projection 和条件学习速度。基础 ODE 附录及已有存在唯一性证明保留。

## 辅助题目：14 项

| Project | Concise 题目 |
|---|---|
| 8 | Main task |
| 9 | 4（numerics）、5、9、11、12、13 |
| 10 | 1、2、4 |
| 11 | 4 |
| 12 | 1 |
| 13 | 1 |
| 14 | 1 |

主要压缩如下：

- Euler Jacobian 保留一步公式、乘积公式、简洁误差论证和原有标量 Euler/RK4 表格与图；原来的展开计算及高阶技术分析注释保存，一步误差估计附录保留。
- 体积输运、KL 凸性和谐振子矩阵计算改用简洁论证，原推导注释保存；其余本已简短的辅助结果保留。
- score 演化方程及其证明保留；Hessian 和长期行为扩展改为待完善问题，原推导注释保存。
- total covariance、条件期望和 Gaussian reconstruction 保留；double-well 扩展保留模型与问题，解答注释保存。
- KL 的 Bregman 扩展暂存为注释，不影响保留的联合凸性与核心变分结构。

## 暂缓题目：14 项

| Project | Pending 题目 |
|---|---|
| 8 | 1 |
| 9 | 6、14、15 |
| 10 | 3 |
| 11 | 2、3、8、9、10、11、12、13 |
| 12 | 2 |

Question/solution 结构保留题目，解答用 `%` 行注释禁用，显示 `To be completed.`。对于原有 theorem/proposition，保留陈述和来源锚点，将证明注释并显示 `Proof to be completed.`。Project 11.3 的两个解答均已暂缓；Project 11.10 的额外 minimax 计算和 Project 12.2 的后续 sharp-level 推导也一并注释。

合并来源分别处理：Project 10 的 Hamilton 方程、能量守恒和辛结构仍保留；只有 10.3 的时间反演证明暂缓。Project 9.4 的解析和数值入口保持独立。

## 原稿保存与引用检查

- 27 个注释块均使用 `DEFERRED SOLUTION` / `END DEFERRED SOLUTION` 边界，能逐行还原到修改前的源码。
- 全部 46 个 `src:p...` 锚点、全部原始 `sourcecredit` 及表格的 `tab:source-map` 标签仍然有效；其中 45 个入口列入 Source Index。
- 全部 section、subsection、subsubsection 标题和次序保留。
- Introduction、Source Index 说明和末尾 Scope 已改为选择性完成的表述。
- 数值实验脚本、图片和已保存数据逐文件哈希一致；未重新生成任何实验结果。参考文献源文件未修改。
- 校验脚本仅作此次注释所需的引用处理：检查活动标签与链接，并继续确认被暂缓的图片源码及文件仍保留。

恢复某段推导时，去掉对应边界内各行最前面的 `% `，并撤下对应待完善提示。若同处已有精简版，应先选择保留精简版或恢复原版，避免同时启用重复公式标签。

## 编译与验证

已完成 XeLaTeX/Biber 全文编译，最终 PDF 为 95 页，最终日志无 LaTeX 警告或超宽公式。活动公式标签唯一，45 个题目索引链接和 31 个 PDF 书签有效；14 个 Pending 目标均核对到保留内容及完成提示。抽查了 Source Index、精简后的数值问题、Project 11.3、11.13、12.2 和 13.1 的排版及完成提示。

源码快照、保护文件哈希、逐段核对记录和编译日志曾保存在本地 `build/assessment-priorities-2026-11-09/`，已在项目清理时移除。正文中注释保留的原解和项目数据仍在源码目录中。
