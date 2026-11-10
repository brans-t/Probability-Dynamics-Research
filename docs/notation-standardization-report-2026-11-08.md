# 全文数学符号规范化实施报告（2026-11-08）

2026-11-09 字形修订：仿射外加项恢复为 `B_t`，取消 RSFS 手写花体。算子改用 `\mathsf D_A`、`\mathsf Q`；标量泛函使用 `S`、`F`、`H_{m_{\mathrm{ref}}}`、`L_{\mathrm{log}}`，观测量 Banach 空间使用 `X_{\mathrm{obs}}`。标量布朗运动改记为 `W_t^{\mathrm{red}}`，投影构造使用 `W_t^\xi`。正文、符号表、附录、注释中暂缓的推导、幻灯片和 TikZ 图同步更新。

修改对象：[LaTeX 原稿](../paper/main.tex)。完整 PDF 可通过 `python scripts/build.py` 生成到 `build/paper/main.pdf`。本轮依据 [批准后的方案](notation-standardization-plan.md) 及作者的八项补充要求实施。

后续文件整理及记号修订：符号章保存在 [notation.tex](../paper/notation.tex)，主文件通过 `\input{notation}` 引入，现位于正文及附录之后、参考文献之前。自定义乘法算子统一为 `\mathsf M_A`，Picard 算子统一为 `\mathsf Q_{s,x}`，局部限制及其缩写为 `\mathsf Q_\delta`、`\mathsf Q`；正文、图示及符号表同步修改，标准数学记号保留。检查脚本同时读取符号子文件及其交叉引用。下文的前置安排及页码为初次实施记录，以本段和当前源码为准。

## 完成结果

- 前置顺序为：标题页、目录、Notation and Conventions、Introduction、Source Index、正式正文。
- Notation and Conventions 位于罗马页码 **ii–ix**，PDF 物理页 **3–10**；Introduction 从 **x** 页开始。完整 PDF 共 **105** 页。
- 符号表分为 **Global Notation** 和 **Topic-specific Notation** 两层，共 **99** 个条目、**6** 张可跨页长表，说明对象类型、定义和适用范围。
- 帽子、横线和波浪号被表述为本笔记的常用约定，并说明 Gaussian 上尾等局部例外，不作为跨领域绝对规则。
- 概率测度弱收敛使用 `\xrightarrow{\mathrm w}`，函数空间弱收敛使用 `\rightharpoonup`，逻辑蕴含使用 `\Longrightarrow`。
- 增加 SDE 数值近似状态 `\widehat X_k`；概率流速度的商式只在正密度区域定义。
- Hamiltonian 表达式依具体模型及假设给出。当前机械例子保留原有单位质量假设，没有推广成全篇 Hamiltonian 的统一定义。
- Hamiltonian Hessian 直接写作 `\nabla^2H(z_t)`，不引入与解算映射 `S_t` 有联系的新别名。

## 实际采用的旧新符号映射

| 原符号与上下文 | 新符号或保留决定 |
|---|---|
| Euler 数值状态 `x_k` | `\widehat x_k`；精确网格点值仍为 `x_{t_k}` |
| 数值流 `\widehat\Phi_K` | `\widehat\Phi_{h,K}`；一般第 k 步的规范为 `\widehat\Phi_{h,k}` |
| 数值 Jacobian `\widehat M_K,\widehat J_K` | `\widehat M_{h,K},\widehat J_{h,K}` |
| 附录的导数矩阵 `J_{s,t}` | `M_{s,t}=D_x\Phi_{s,t}` |
| 流的行列式 | `J_{s,t}:=\det M_{s,t}`；`J_1` 明确为 `J_{0,1}` 的局部缩写 |
| coarea Jacobian `J_\xi` | 保留，定义为 `\sqrt{\det(D\xi D\xi^\top)}`，明确区别于流 Jacobian |
| Markov 核 `K_{s,t}` | `\mathsf K_{s,t}` |
| 线性系数 `A(t)` | `A_t`；常矩阵 A 仍按其局部定义使用 |
| 仿射外加项 `B(t)` | `B_t` |
| 基本解矩阵 `U(t,s)` | 保留传统“终止、起始”顺序，表中明确与 `\Phi_{s,t}` 对应 |
| 轨迹空间上的乘法算子 `\mathcal A` | `\mathsf M_A`；观测量代数仍为 `\mathcal A=B_b(V)` |
| 轨迹 ODE 算子 `\mathcal L` | `\mathsf D_A=\partial_t-\mathsf M_A`；生成元保留 `\mathcal L_t` |
| 观测量 Banach 空间 `\mathcal X` | `X_{\mathrm{obs}}`；轨迹空间保留 `\mathcal X` |
| 物理势能 `V(x)`、条件几何势能 `U(x)` | `\mathcal V(x)`；状态空间保留 V |
| 抽象 Gibbs 倾斜代价 U | c，及对应的 `Z_c,\nu_c`；不自动等同于物理势能 |
| 辛矩阵 J | `\mathbb J_n`；构型维数为 n、相空间维数为 d=2n |
| Hamiltonian Hessian `S_t` | 直接使用 `\nabla^2H(z_t)` |
| Verlet 状态 `q_n,p_n,p_{n+1/2}` | `\widehat q_k,\widehat p_k,\widehat p_{k+1/2}` |
| 数值能量 `H_n` | `\widehat H_k:=H(\widehat q_k,\widehat p_k)`；修正能量保留 `\widetilde H_h` |
| 物理运动区域 `\Omega_t` | `\mathcal D_t`；样本空间保留 `\Omega` |
| 冷却温度 `T(t)` | `T_t`；终止时间保留 T |
| 加权作用量的累计函数 `W(t)` | `\Theta_w(t)`；Brownian 运动仍使用 `W_t` |
| 散度上界 D、导数界 M | `B_{\mathrm{div}}`、`L_v`；相应统一常数变为 `C_{d,L_v}` |
| 对数余项 `\rho_k` | `r_k^{\log}`；密度仍为 `\rho_t` |
| 数值参考矩阵 `\widetilde U` | `\widehat U_{\mathrm{ref}}`，保留原有求解容差说明 |
| score `s_t`、log-density Hessian `S_t` | `s_t^\rho`、`H_t^\rho`；多密度时使用密度标记 |
| 自由能泛函 `\mathcal F` | `F`；概率空间的 sigma-algebra 保留 `\mathcal F` |
| 负熵参考测度 m | `m_{\mathrm{ref}}`，负熵泛函记为 `H_{m_{\mathrm{ref}}}` |
| 凸混合权重 `\theta` | `\vartheta`；模型参数仍使用 `\theta` |
| 截断 Gaussian 目标 `J_\alpha` | `\mathcal J_\alpha` |
| logistic 风险 `\mathcal L(g)` | `L_{\mathrm{log}}(g)` |
| 有限状态 minimax 正权重 s、鞍点函数 F | r、`\mathcal J_{\mathrm{saddle}}` |
| 约化空间 Z | `\mathcal Z`；随机变量和过程仍为 `Z,Z_t` |
| 条件几何全维数 n | d；约化维数仍为 m，Brownian 维数为 `d_W` |
| 水平集 `\Sigma_z`、Gram 矩阵 G | `\mathcal M_z`、`G_\xi`；协方差保留 `\Sigma_t` |
| 平均力势 F、提升向量场 `B_i` | `F_\xi`、`B_i^\xi` |
| 投影系数 `b(t,z),a(t,z)` | `b_t(z),a_t(z)` |
| 概率流 `J_t` | `\boldsymbol j_t`；仅在 `\rho_t>0` 处取商定义 current velocity |
| 插值条件速度 `v_t` | `v_t^{\mathrm{int}}`，区别于 current velocity `v_t^{\mathrm{cur}}` |
| 回归族 `g_\theta(t,z)` | `g_{\theta,t}(z)`，表中登记与网络接口的等价写法 |
| 拟合参数、已训练函数 | `\widehat\theta`、`g_{\widehat\theta,t}`，并定义 `\widehat g_t` 和 `\widehat b_t` 的身份 |
| 目标重权函数 h | w，及相应 `Z_w,\rho_w` |
| 传输映射 T、时间插值 `T_t`、三角分量 `T_i` | `F_{\mathrm{tr}}`、`F_t^{\mathrm{tr}}`、`F_{\mathrm{tr}}^i` |
| 源样本 `x_i`、样本数 N | `x^{(\ell)}`、`N_{\mathrm{samp}}`；经验测度记为 `\widehat\mu_{w,N_{\mathrm{samp}}}` |
| 控制问题乘子 `\phi_t` | `\psi_t`；自治流保留 `\phi_t` |
| 空间格宽 h、单元数 N、扩散常数 D | `\Delta x,N_x,D_{\mathrm{diff}}` |
| 跳率 `k_{i,j}`、质量生成矩阵 Q | `q_{i\to j}^{\Delta x}`、`Q^{\Delta x}`；固定网格内声明跳率缩写 |
| 半离散质量 `m_i(t)` | 说明它是 `m_i^{\Delta x}(t)` 的固定网格缩写，时间仍连续 |
| OU 矩阵 K、均值 `m_t` | `A_{\mathrm{OU}}`、`m_t^{\mathrm{OU}}`；漂移仍为负号 |
| 附录参考轨迹 `\xi_t` | `x_t=\Phi_{s,t}(x)`，集体变量专用 `\xi` |
| 附录初值扰动 h、精确轨迹差 `e_t(h)` | `\delta x`、`\Delta_t(\delta x)` |
| 附录 Taylor 余项 `R_t(h)` | `R_t^{\mathrm{lin}}(\delta x)` |
| Picard 时间半径 h、积分映射 `\mathcal T` | `\delta_{\mathrm{loc}}`、`\mathsf Q_{s,x}`；时间排序保留 `\mathcal T` |
| Picard 序号 `\gamma_n,U_n` | `\gamma^{[n]},U^{[n]}`，不误读为时间步 |
| 指数证明中的积分矩阵 `H(t)` | `B_A(t,s)`，不与 Hamiltonian 共用名称 |

## 分主题实施及数学核对

每个阶段通过源码保护检查、完整 XeLaTeX/Biber 编译和 PDF 引用检查后，才进入下一阶段。

| 阶段 | 修改范围 | 数学核对重点 | 最终结果 |
|---|---|---|---|
| 1 | 状态空间、观测量与概率演化基础 | 集合/向量/函数/概率律类型，推前与反序复合 | 通过 |
| 2 | ODE、流与 Jacobian、数值 Jacobian、Hamiltonian，以及全部相关 ODE 附录 | 同一初始状态和终止时间、Jacobian 乘积次序、帽子求值点、正性、余项估计、辛结构、前向/后向排序 | 通过 |
| 3 | 熵、score、KL、凸对偶、自由能 | KL 方向和符号、密度标记、共轭对、扰动方向、倾斜归一化、既有可积性及边界条件 | 通过 |
| 4 | 条件律、coarea、平均力与投影模型 | d/m 维数、曲面测度、coarea 因子、条件均方噪声、原有存在唯一性和边缘律条件 | 通过 |
| 5 | 学习、传输构造、控制及 Markov 空间离散 | 正密度商式、样本与分量、时间插值与三角分量、零通量、质量列向量约定、详细平衡及熵耗散 | 通过 |
| 6 | OU 解析与学习基准 | 漂移负号、正定矩阵、传播子顺序、均值/协方差、条件均值及自协方差 | 通过 |
| 7 | 前置两层符号表及全文终检 | 章节顺序、表格跨页、定义/作用域、原有编号与导航、符号和正文一致性 | 通过 |

数值 Jacobian 的原结论保持不变：Euler 一阶全局误差 `O(h)`，高阶一致变分更新在既定正则性条件下为 `O(h^p)`，经典 RK4 对应四阶。没有通过改记号增大任何结论的适用范围。

## 保留的局部约定及理由

- `U(t,s)` 保留终止时间在前的标准基本解矩阵写法；表中明确它和 `\Phi_{s,t}` 的参数对应，不机械交换时间顺序。
- Hamiltonian 的 `q,p`、信息论密度 `p,q`、插值小节的耦合律 `\gamma`、路径问题的曲线 `\gamma` 都有独立作用域，保留各自常用写法。
- `\bar\Phi` 是 Gaussian 上尾；`\widetilde H_h` 是修正能量；`\bar X_t` 是闭合模型的连续解。它们不是同一类近似。
- 半离散质量仍随连续时间演化。若以后再作时间积分，应使用 `\widehat m_{k,i}^{\Delta x}`；本轮没有添加这样的数值实验。
- 原题 ghost-cell 公式中的 `p_i,N` 按原样保留，同时说明其与本文密度近似、`N_x` 的对应；原题边界条件未被篡改。
- 静态 coarea Gibbs 边缘记为 `p_\xi`，不额外断言未指定动力学的不变性；热力学段落已建立的不变律则明确区分 `\pi` 与其密度 `\rho_{\mathrm{eq}}`。
- 不因稿件改名而改动实验 CSV/JSON 字段。例如稿件 `A_{\mathrm{OU}}` 对应保存数据中既有的矩阵字段 K；数据兼容性保持不变。

## 检查证据

1. **原有 52 个编号公式全部通过改名对照。** 对每个公式使用该上下文已声明的旧新映射，消除纯空白及排版差异后，代数表达逐一一致。该检查验证表达式保留，另人工核对求值点、矩阵次序、类型及假设，不把字符对照当作形式化证明。
2. **187 个既有标签全部保留，标签编号未改变。** 新增符号表定位标签 `ch:notation`；原有 63 个章内编号数学陈述及 45 个来源跳转通过 PDF 检查。
3. **数值表中的小数及科学记数值未改。** `results/benchmarks` 和 `paper/figures` 下 77 个文件逐一 SHA-256 校验一致。加入参考文献和来源索引后，baseline 检查共验证 79 个受保护文件。
4. **原有物理和数学假设保留。** 没有修改单位质量机械模型、Langevin/OU 参数、Gibbs 温度因子、边界条件、条件律版本及投影定理的存在唯一性要求；没有重跑训练、替换数据或重画实验图。
5. **源码及完整编译通过。** 最终日志无 undefined、重复定义、缺字、Overfull 或 LaTeX Warning；原有轻微 Underfull 提示不影响数学和页面完整性。
6. **视觉检查完成。** 逐页查看符号表 ii–ix 页，检查目录和 Introduction 的次序、重复表头、列宽、数学字形及分页；抽查 Hamiltonian、平均力、Markov 和 OU 页面。修正了符号表孤立标题和一处因记号变长造成的超宽公式。
7. `paper/preamble.tex` 无需改动；原有 longtable、array、Needspace 和数学字体已经支持本轮排版。`scripts/check_manuscript_audit.py` 仅对明确标记的新增前置符号表作专门处理，继续检查全部原有数学陈述、科学图表、标签、来源入口和数据文件。

本轮工作材料及编译/检查结果曾保存在 `build/notation-audit/`，已在项目清理时移除。最终源码位置和符号规范以稿件中的 Notation and Conventions 为准，后续新增符号应先定义对象类型及作用范围，再检查冲突并按需补表。
