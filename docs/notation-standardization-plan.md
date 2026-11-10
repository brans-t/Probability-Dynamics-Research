# 全文数学符号统一方案（2026-11-08 批准修订版）

2026-11-09 更新：取消 RSFS 手写花体。仿射外加项恢复为 `B_t`；轨迹算子使用 `\mathsf D_A`，Picard 算子使用 `\mathsf Q`，标量泛函使用普通字母 `S`、`F`、`H_{m_{\mathrm{ref}}}`、`L_{\mathrm{log}}`，观测量 Banach 空间记为 `X_{\mathrm{obs}}`。标量布朗运动记为 `W_t^{\mathrm{red}}` 或投影构造中的 `W_t^\xi`，避免与外加项重名。以下映射及正文、符号表、幻灯片已同步。

审阅范围：`paper/main.tex` 全文，包括正文五个主题节、ODE 附录的五节，以及 `paper/preamble.tex`。当前主文件共 5396 个物理行；它只加载共享导言区，没有其他正文子文件。以下行号仅用于定位本次审阅快照，实施后会改变。另检查了现有项目校验脚本及 Hamiltonian 绘图入口，以确定后续同步范围。

本方案已纳入作者的八项补充要求。实施按主题分段，每段完成数学等价性、完整编译与引用检查后，再进入下一段；不得改变物理假设、结论、实验数据或证明逻辑。

实施状态：已完成。最终前置符号表分 Global Notation 与 Topic-specific Notation 两层，共 99 个条目、6 张分组长表，位于 PDF 的 ii–ix 页；Introduction 位于 x 页。具体旧新映射、保留的局部约定及检查记录见 [实施报告](notation-standardization-report-2026-11-08.md)。以下保留经批准的规划依据。

按后续修订要求，符号章保存在独立的 [paper/notation.tex](../paper/notation.tex)，由主文件 `\input{notation}` 引入，现移至正文及附录之后、参考文献之前。自定义乘法算子和 Picard 算子分别统一为 `\mathsf M_A` 和 `\mathsf Q_{s,x}`；标准数学记号保留。下文的前置安排及页码为初次实施记录，以本段和当前源码为准。

## 一、总体规则及理由

采用三层约定：**全文核心符号固定、主题符号在主题内固定、临时变量在首次出现时定义并限定作用域**。

全文固定数学对象的身份，不要求每一个字母在所有局部证明中只出现一种意义。例如 Hamiltonian 的位置、动量 `q,p`，与信息论中已明确声明的密度 `p,q`，可以保留各自的标准用法；不允许同一流推导中的 `J_{s,t}` 一会儿表示矩阵、一会儿表示行列式。

在本笔记中，帽子通常表示数值近似或统计估计；横线通常表示已定义的约化/闭合模型；波浪号通常表示明确给出的变换或修正对象。这些是本笔记的常用约定，不是跨领域的绝对规则；例外必须就地定义（例如 Gaussian 上尾函数的横线）。精确解析公式的数值评价、从精确概率律抽样、模型近似和时间离散，不视为同一种近似。

字形帮助区分对象，但不把全部矩阵改成粗体，也不声称所有花体字母都属于同一类型。保留正文已有的算子字形 `\mathcal{K},\mathsf T,\mathsf P`，并通过定义域、值域和下标进一步确认类型。

## 二、已发现的问题与处理决定

| 当前用法及定位 | 拟采用的处理 | 理由 |
|---|---|---|
| Euler 推导中 `x_k` 表示数值状态，约 1585、1740、1800 行 | 全部按上下文改为 `\widehat x_k`；网格点精确值仍为 `x_{t_k}` | 使精确轨迹与数值轨迹在求值点、链式法则、误差和余项中始终可区分 |
| 附录约 5065 行用 `J_{s,t}` 表示导数矩阵 | 改为正文已有的 `M_{s,t}`；`J_{s,t}:=\det M_{s,t}` | 这是与拟定全局约定直接相反的类型冲突，必须处理 |
| 状态空间 `V` 与势能 `V(x)`，条件几何又改用 `U(x)` | 空间保留 `V`；势能统一为 `\mathcal V(x)`；抽象 Gibbs 倾斜代价用 `c(x)` | 连接 Hamiltonian、Langevin、coarea 和 OU 中的势能，同时保留基本解矩阵 `U(t,s)`；不把无量纲倾斜代价直接等同于物理能量 |
| Hamiltonian 辛矩阵 `J`；概率流 `J_t`；Jacobian `J` | 辛矩阵用 `\mathbb J_n`，概率流用 `\boldsymbol j_t`，`J` 保留给 Jacobian 行列式 | 三者类型、维数和功能均不同，不能靠所在章节猜测 |
| `K` 同时为步数和 OU 矩阵，约 1940、4660 行 | `K` 固定为时间步数；OU 正定矩阵用 `A_{\mathrm{OU}}`，漂移仍写成 `-A_{\mathrm{OU}}R_t` | 避免在数值算法中把矩阵参数误读为步数；保留矩阵的正定性和原有负号 |
| `h` 表示时间步长、空间格宽、重加权函数和初值扰动 | 分别用 `h`、`\Delta x`、`w(x)`、`\delta x` | 使误差估计中的极限参数及其量纲明确 |
| `x_i` 同时表示空间分量、样本、格点 | 分量用 `x^i`，样本用 `x^{(\ell)}`，空间格点用 `x_i` | 消除同一数值公式里时间、坐标、样本编号之间的歧义；粒子编号另作局部说明 |
| `\mathcal A` 是观测量代数，也是轨迹上的矩阵乘法算子，约 357、643 行 | 保留 `\mathcal A=B_b(V)`；乘法算子用 `\mathsf M_A` | 这两个对象连定义域和值域都不同，应分开命名 |
| `\mathcal L` 是轨迹 ODE 算子、生成元、logistic 风险 | 生成元保留 `\mathcal L_t`；轨迹 ODE 算子用 `\mathsf D_A`；风险用 `L_{\mathrm{log}}` | 区分“对轨迹作微分”“对观测量作演化”“给函数打分” |
| `\mathcal X` 既是轨迹空间又是观测量 Banach 空间 | 轨迹空间保留 `\mathcal X`；观测量空间用 `X_{\mathrm{obs}}` | 两类函数的自变量、值域及范数不同 |
| `D` 同时为状态导数、时间微分算子、散度上界、扩散常数 | 状态导数保留 `D_x`；轨迹时间导数用 `\partial_t`；散度上界用 `B_{\mathrm{div}}`；扩散常数用 `D_{\mathrm{diff}}` | 防止在同一误差/PDE 推导中出现同形而异类的量 |
| `\mathcal F` 是概率空间的 sigma-algebra，又是自由能泛函 | sigma-algebra 保留 `\mathcal F`；自由能泛函用 `F` | 该冲突原稿已用文字提醒，改名后不再需要读者反复记忆例外 |
| `F` 是一般状态变换，也是平均力势 | 一般变换保留 `F`；平均力势用 `F_\xi` | 标明自由能依赖于所选集体变量及参考体积 |
| `\rho_t` 为密度，`\rho_k(h,x)` 却是对数余项 | 后者改为 `r_k^{\log}(h,x)` | 避免将余项误认为离散密度；保留此前已建立的余项分解 |
| `\Sigma_t` 为协方差，`\Sigma_z` 为水平集 | 协方差保留 `\Sigma_t`；水平集用 `\mathcal M_z:=\xi^{-1}(\{z\})` | 条件 Gaussian 和 coarea 公式中会同时出现两者，应区分几何集合与矩阵 |
| 附录 `\xi_t` 表示参考轨迹，正文 `\xi` 是集体变量 | 附录参考轨迹改用 `x_t=\Phi_{s,t}(x)` | 保留 `\xi` 给约化映射，避免把轨迹误读为反应坐标 |
| 附录 `e_t(h)` 是两条精确轨迹之差 | 改为 `\Delta_t(\delta x)` | `e_k` 专门表示数值状态误差；精确解的初值敏感性不是离散误差 |
| `S_t` 同时为解算映射和 Hessian，`H(t)` 还表示积分矩阵 | 解算映射 `S_t` 保留局部定义；Hessian 使用带对象标记的记号；积分矩阵用 `B_A(t,s)` | 不让 Hamiltonian `H`、解算映射和二阶导数共享未经说明的名字 |
| `\Omega` 是样本空间，也用于运动区域 `\Omega_t` | 样本空间保留 `\Omega`；运动区域用 `\mathcal D_t` | 将概率空间与物理积分区域分开 |
| `\mathcal T` 既表示时间排序又表示 Picard 映射 | 时间排序保留 `\mathcal T`；Picard 映射用 `\mathsf Q_{s,x}` | 两者在同一 ODE 附录中出现，运算性质不同 |
| 传输例子中 `T_1` 既为时刻 1 的映射又为三角映射第一分量 | 传输映射用 `F_{\mathrm{tr}}`，时间插值用 `F_t^{\mathrm{tr}}`，分量用 `F_{\mathrm{tr}}^i` | 同一例子内也必须区分时间指标与坐标指标 |

## 三、拟固定的符号清单

### A. 状态、空间、时间及编号

| 符号 | 数学对象 | 定义和适用约定 |
|---|---|---|
| `V=\mathbb R^d` | Euclidean 状态空间 | `d` 为完整状态维数；一般可测空间另用 `E` |
| `(E,\mathcal S)` | 一般可测空间 | 不默认具有线性结构；有拓扑时明确所用 Borel 结构 |
| `\mathcal Z=\mathbb R^m` | 约化状态空间 | `m\le d`；不再用裸 `Z` 表示这个集合 |
| `x,y\in V` | 任意确定性状态 | 积分哑变量及一般输入；不自动表示轨迹 |
| `x_t` | 精确确定性轨迹 | `x_t=\Phi_{s,t}(x)` 且 `x_s=x`；起点为 0 时写 `x_t=\Phi_{0,t}(x_0)` |
| `X_t` | 随机状态/过程 | 包括随机初值经确定性流传播及真正的 SDE；随机性来源在模型处说明 |
| `x^i,X_t^i` | 状态的第 i 分量 | 向量为列向量；分量上标不是幂，由首次定义及索引说明区分 |
| `x^{(\ell)},X^{(\ell)}` | 样本实现、随机样本 | 圆括号上标为样本编号，不是时间或空间分量 |
| `s,t,r,\tau` | 连续时间及积分变量 | `s` 为起始时间，`t` 为终止/当前时间；积分变量可局部更换 |
| `T>0` | 固定终止时间 | `[0,1]` 例子继续保持 `T=1`，不为统一符号而改动结论或数值 |
| `K,h,t_k` | 时间网格 | `h=T/K,\ t_k=kh`；起点非 0 时明确 `t_k=s+kh,\ h=(T-s)/K` |
| `N_x,\Delta x,x_i` | 空间网格 | `N_x` 个单元、宽度 `\Delta x`、中心 `x_i`；可与连续时间并存 |
| `N_{\mathrm{samp}}` | 样本量 | 与时间步数 `K`、格点数 `N_x` 分开 |
| `n` 或上标 `[n]` | 迭代/级数编号 | Picard 迭代与级数项均在局部声明，不解释为时间步 |
| `\delta x` | 初值的向量扰动 | 与标量时间步长 `h`、标量空间宽度 `\Delta x` 分开 |
| `\xi:V\to\mathcal Z` | 集体变量 | `Z_t=\xi(X_t)`；几何公式中声明光滑性及满秩条件 |
| `\mathcal M_z` | 水平集 | `\{x:\xi(x)=z\}`；不是协方差矩阵 |

Hamiltonian 部分用 `n` 表示构型自由度，`q,p\in\mathbb R^n`，相空间维数为 `d=2n`。粒子引言中的 `q_i,p_i` 保留为第 i 个粒子的三维位置/动量，明确它们的下标是粒子编号。Brownian 维数用 `d_W`，避免与约化维数 `m` 混用。

### B. 连续流、数值流及导数

| 符号 | 数学对象 | 定义和适用约定 |
|---|---|---|
| `v_t(x)` | 确定性速度场 | `\dot x_t=v_t(x_t)`；有多个构造时使用 `v_t^{\mathrm{cur}}`、`v_t^{\mathrm{int}}` 等说明性上标 |
| `b_t(x),\sigma_t(x)` | SDE 漂移及噪声矩阵 | `\mathrm dX_t=b_t(X_t)\mathrm dt+\sigma_t(X_t)\mathrm dW_t`；不能把漂移一律当作概率流速度 |
| `\Phi_{s,t}` | 精确两时流映射 | 参数顺序固定为“起始、终止”；只在已明确的自治情形允许 `\phi_t=\Phi_{0,t}` |
| `A_t` | 线性系统系数矩阵 | 将 `A(t)` 规范为 `A_t`；变分系统中明确 `A_t=D_xv_t(x_t)` |
| `B_t` | 仿射系统的外加项 | 原 `B(t)`；与完整 SDE 漂移、Brownian `B_t` 和紧集 `B` 分开 |
| `U(t,s)` | 线性基本解矩阵 | 保留既有传统参数顺序“终止、起始”；满足 `\Phi_{s,t}(x)=U(t,s)x`（齐次线性情形） |
| `D_xF(x)` | 状态映射的导数矩阵 | `D` 省略 `x` 仅在自变量无歧义时允许；`(D_xF)_{ij}=\partial F^i/\partial x^j` |
| `M_{s,t}(x)` | 精确流的 Jacobian 矩阵 | `D_x\Phi_{s,t}(x)`；矩阵初值为 `I_d` |
| `J_{s,t}(x)` | 精确流的 Jacobian 行列式 | `\det M_{s,t}(x)`；标量初值为 1；`J_t:=J_{0,t}` 需先声明缩写 |
| `V_k(x)` | Euler 单步映射 | `x+hv_{t_k}(x)`；大小写 `V_k` 与 `v_t` 的区别保留 |
| `\widehat x_k` | 数值状态 | `\widehat x_{k+1}=V_k(\widehat x_k),\ \widehat x_0=x_0`；精确值是 `x_{t_k}` |
| `\widehat\Phi_{h,k}` | 从初始点到第 k 网格点的数值流 | `V_{k-1}\circ\cdots\circ V_0`；在单一固定网格的例子中允许声明缩写 `\widehat\Phi_K:=\widehat\Phi_{h,K}` |
| `\widehat M_{h,k},\widehat J_{h,k}` | 数值 Jacobian 矩阵及行列式 | 分别为数值流的导数和该导数的行列式；写明依赖的初始状态；比较的终止时间为 `t_k` |
| 方法上标 `\mathrm E,\mathrm{RK4},\mathrm{VV}` | 数值方法标签 | 同时比较多方法时标记；Verlet 半步也使用帽子和时间步索引 k |
| `\widehat U_{\mathrm{ref}}(t,s)` | 数值参考基本解 | 取代当前数值参考 `\widetilde U`；仍报告容差，不把参考值写成解析真解 |
| `\operatorname{id}_V,I_d` | 恒等映射及单位矩阵 | 对一般映射用前者，对矩阵计算用后者；维数明确时才省下标 |

所有初始状态及参数固定时才省略相关自变量。不能把 `M_t` 的矩阵演化与 `J_t` 的标量演化混写。保留 `U(t,s)` 是一个明确登记的传统写法，并不会把它和 `\Phi_{s,t}` 的参数机械交换。

### C. 可观测量、概率及演化算子

| 符号 | 数学对象 | 定义和适用约定 |
|---|---|---|
| `(\Omega,\mathcal F,\mathbb P)` | 概率空间 | `\Omega` 为样本空间；不与运动物理区域共享名称 |
| `\mu_t,\nu_t` | 概率律 | 完整状态与约化状态并列时分别为 `\operatorname{Law}(X_t)`、`\operatorname{Law}(Z_t)` |
| `\rho_t(x)` | 完整状态的 Lebesgue 密度 | 仅在绝对连续时写 `\mu_t(\mathrm dx)=\rho_t(x)\mathrm dx` |
| `p_{\xi,t}(z)` | 约化律的密度 | 若存在，`\nu_t(\mathrm dz)=p_{\xi,t}(z)\mathrm dz`；平衡密度缩写必须先声明 |
| `\mu_{t,z}` | 正则条件概率核 | `\operatorname{Law}(X_t\mid\xi(X_t)=z)`；平衡/静态情形可声明 `\mu_z` |
| `\pi,\rho_{\mathrm{eq}}` | 平衡概率律及其密度 | `\pi(\mathrm dx)=\rho_{\mathrm{eq}}(x)\mathrm dx`；不直接把概率律当作密度函数 |
| `P,Q` 与 `p,q` | 信息论局部概率律与密度 | 保留标准双测度写法，并在该节明确参考测度；不强改 Hamiltonian 的动量符号 |
| `\mathbb E_\mu,\operatorname{Law},\operatorname{Cov},\operatorname{Var}` | 概率运算 | 写明所涉概率律；在概率空间已固定时允许省略期望下标 |
| `\langle f,\mu\rangle` | 函数—测度积分配对 | `\int f\,\mathrm d\mu`，与 Euclidean 内积分开 |
| `f,g,\varphi` | 可观测量/测试函数 | 定义域及可积性按所在结论声明；不是所有这些函数都属于 `B_b` |
| `\mathcal A=B_b(V)` | 有界可测观测量代数 | 不再用这个符号表示其他算子 |
| `\mathcal{K}_F,\mathcal{K}_{s,t}` | Koopman 算子 | 作用于函数；`\mathcal{K}_{s,t}f=f\circ\Phi_{s,t}` |
| `\mathsf T_F,\mathsf T_{s,t}` | 推前作用 | 作用于概率律；`\mathsf T_{s,t}\mu=(\Phi_{s,t})_\#\mu` |
| `\mathsf K_{s,t}(x,\mathrm dy)` | Markov 转移核 | 使用算子字形并保留两时下标，与裸 `K` 步数明确区分 |
| `\mathsf P_{s,t}` | Markov 可观测量演化算子 | 确定性情形等于 `\mathcal{K}_{s,t}`；不改动现有复合顺序 |
| `\mathcal L_t` | 可观测量生成元 | 定义域、值域、极限拓扑按具体结论声明；对确定性流、扩散和跳过程分别给表达式 |
| `X_{\mathrm{obs}}` | 选择的观测量 Banach 空间 | 与轨迹空间 `\mathcal X` 分开；生成元定义域可写 `\operatorname{Dom}(\mathcal L_t)` |
| `\boldsymbol j_t(x)` | 概率流密度 | 连续性形式为 `\partial_t\rho_t+\nabla\cdot\boldsymbol j_t=0`；只有在 `\rho_t(x)>0` 的区域定义 `v_t^{\mathrm{cur}}=\boldsymbol j_t/\rho_t` |
| `W_t,B_t` | 已说明维数的 Brownian 运动 | `W_t` 用于完整系统，`B_t` 用于标量约化；二者是否耦合必须明确，不能由字母推断 |

### D. 能量、熵、几何及学习

| 符号 | 数学对象 | 定义和适用约定 |
|---|---|---|
| `\mathcal V` | 势能/指定的能量函数 | 各模型在首次出现时给出表达式；不同模型不默认是同一个函数 |
| `c(x)` | 抽象 Gibbs 倾斜代价 | `Z_c=\int e^{-c}\mathrm d\nu`；仅在热力学模型明确指定时令 `c=\beta\mathcal V`，不遗漏逆温度因子 |
| `H(q,p)` | Hamiltonian | 表达式及假设由具体模型给出；单位质量机械模型才使用 `\tfrac12\|p\|^2+\mathcal V(q)`，不推广为全局定义 |
| `\mathbb J_n` | 标准辛矩阵 | `2n\times2n`；`\left(\begin{smallmatrix}0&I_n\\-I_n&0\end{smallmatrix}\right)` |
| `\widetilde H_h` | 修正 Hamiltonian | Verlet 的确定性修正能量；波浪号不是数值状态帽子的替代品 |
| `\beta` | 逆温度 | 全文同义；物理温度与终止时间 `T` 分开 |
| `Z_{\beta,\mathcal V}` 等 | 配分/归一化常数 | 用说明性下标表明依赖对象；`Z_t` 作为随机约化过程时不读作配分常数 |
| `S(\rho)` | 微分熵 | 保留已有定义和符号 |
| `H_{m_{\mathrm{ref}}}` | 固定参考测度下的负熵泛函 | Bregman 段落明确参考测度；避免与 Hamiltonian `H` 及约化维数 `m` 混淆 |
| `D_{\mathrm{KL}}` | KL 散度 | 保留已有 `\KL` 宏及参数顺序；密度记法须声明为测度记法的缩写 |
| `\ell_t,s_t^\rho` | 对数密度、score | `\ell_t=\log\rho_t,\ s_t^\rho=\nabla\ell_t`；与时间 s 通过对象标记区分 |
| `H_t^\rho` | 对数密度 Hessian | `\nabla^2\ell_t`；Hamiltonian Hessian 直接写 `\nabla^2H(z_t)`，不引入 S 类别名 |
| `F_\xi(z)` | 平均力势 | `-\beta^{-1}\log p_\xi(z)`，其中 `p_\xi` 是该小节指定的静态 Gibbs 边缘密度；注明参考体积及加法常数约定，不额外断言某个未指定动力学的不变性 |
| `F(\rho)` | 热力学自由能泛函 | 与 sigma-algebra `\mathcal F`、标量平均力势 `F_\xi` 分开 |
| `G_\xi,J_\xi` | Gram 矩阵、coarea Jacobian | `G_\xi=D\xi D\xi^\top,\ J_\xi=\sqrt{\det G_\xi}`；这是满秩约化映射的体积因子，区别于方形流导数的行列式 `J_{s,t}` |
| `B_i^\xi` | coarea/平均力公式的提升向量场 | `D\xi B_i^\xi=e_i`；不与 Brownian 运动 `B_t` 混淆 |
| `\Sigma_t` | 协方差矩阵 | OU 平衡值 `\Sigma_\infty`；不再用于水平集 |
| `\gamma` | 端点耦合概率律，限插值小节 | 在该节声明 `\gamma\in\mathcal P(V\times V)`；其他节的确定性路径 `\gamma` 保留局部定义 |
| `I_t,\alpha_t,\lambda_t` | 随机插值及确定性系数 | `I_t=\alpha_tX_0+\lambda_tX_1`；单位矩阵始终写带维数的 `I_d` |
| `g_{\theta,t}(z)` | 参数化回归函数族 | 可首次说明它等价于网络接口 `g_\theta(t,z)`；固定主文记法 |
| `\widehat\theta,\widehat g_t,\widehat b_t` | 拟合参数及学习得到的函数 | `\widehat g_t=g_{\widehat\theta,t}`；参数族本身不因可用计算机评价就自动加帽子 |
| `L_{\mathrm{log}},L_{\mathrm{reg}}` | logistic 风险、回归损失 | 只在确有需要时引入对应记号；与生成元 `\mathcal L_t` 分开 |
| `\mathcal R,\mathcal J,\mathcal E,\mathfrak L` | 奖励泛函、目标、终端代价、Lagrangian | 保留各自数学角色；截断 Gaussian 目标 `J_\alpha` 改为 `\mathcal J_\alpha` |
| `f,f^*,\partial f` | f-divergence 的凸函数、共轭、次微分 | 局部明确 f 是标量凸函数；与一般观测量 f 的合法局部用法分开登记 |
| `\Lambda_Q,\Psi_Q` | log-partition 及指数积分泛函 | 保留已建立的不同共轭对及其自然定义域 |
| `r=\mathrm dP/\mathrm dQ` | 密度比 | 有限状态对应 `r_i=p_i/q_i`；minimax 中目前的正权重 s 可改为 r，以体现同一角色 |
| `\psi_t` | Hamilton--Jacobi/Lagrange 乘子 | 替换控制问题中的 `\phi_t`，保留 `\phi_t` 给自治流 |

概率律与密度、有限样本估计与总体目标、学习出的精确模型流与它的数值积分，均各自区分。例如 `\bar X_t` 表示约化模型本身的连续时间解，不因为该模型近似原系统就改成 `\widehat X_k`；真正对该 SDE 作时间积分时才使用后者。

### E. 误差、余项和通用运算

| 符号 | 数学对象 | 定义和适用约定 |
|---|---|---|
| `e_k` | 数值状态误差向量 | `\widehat x_k-x_{t_k}`；误差范数与误差向量不混写 |
| `E_{\mathrm{state}},E_J,E_{\mathrm{traj}},E_{\mathrm{quad}}` | 指定的误差量 | 按需要定义；有符号误差分量与绝对误差在定义中区分 |
| `R_A^{\det}(h)` | 行列式多项式余项 | 保留现有具体定义及统一上界 |
| `r_{\log}(u)` | 标量对数 Taylor 余项 | 保留 `\log(1+u)-u` |
| `r_k^{\log}(h,x)` | 单步组合对数余项 | 取代当前 `\rho_k(h,x)`；沿数值轨迹求值时写明代入 `x=\widehat x_k` |
| `r_k^{\mathrm{quad}}(h)` | 单个时间区间的求积余项 | 保留现有定义及累积过程 |
| `R_t^{\mathrm{lin}}(\delta x)` | 初值微分证明中的 Taylor 余项 | 与行列式、对数余项区分 |
| `O(h^p),o(h^p)` | 渐近数量级 | 声明 `h\to0` 及固定对象；不是具有唯一身份的具体余项函数 |
| `O((\Delta x)^q)` | 空间渐近数量级 | 不与时间离散阶混用；不新增尚未证明的空间收敛结论 |
| `C,C_E,C_{\log},C_*` 等 | 局部估计常数 | 首次出现说明来源、固定参数及不依赖变量；未明确表示相同者不宣称数值相同 |
| `L_v,L_x,L_t,B_{\mathrm{div}}` | 导数、Lipschitz 及散度界 | 用对象说明性下标；Euler 中 `B_{\mathrm{div}}=dL_v` 可作为可用上界 |
| `\|x\|,\|A\|,\|A\|_{\mathrm F}` | Euclidean、诱导矩阵、Frobenius 范数 | 全文默认前两者，Frobenius 必须加 F；函数空间范数带空间或指数下标 |
| `|a|,|A|` | 标量绝对值、集合体积 | 后者仅在已声明的物理可测区域使用；不再用同一竖线省略矩阵范数类型 |
| `\nabla,\nabla^2,\Delta,\nabla\cdot` | 空间微分运算 | 梯度为列向量；散度统一写作 `\nabla\cdot v`，PDE 的通量散度同样采用此符号 |
| `\mathrm d,\partial_t,D_x,\delta` | 积分/SDE 微分、偏导、状态导数、变分 | 保留 `\dd` 宏，按对象说明导数意义 |
| `^\top,\#,\mathbf1_A,\delta_x` | 转置、推前、示性函数、Dirac 概率律 | Dirac delta 的形式密度记号须明确是在积分下解释 |
| `\ll,\sim` | 绝对连续、分布/测度等价 | `X\sim\mu` 与 `P\sim Q` 的意义按两侧对象分别说明 |
| `\mu_n\xrightarrow{\mathrm w}\mu` | 概率测度弱收敛 | 在声明的拓扑空间上以有界连续测试函数刻画 |
| `f_n\rightharpoonup f` | 函数空间弱收敛 | 必须说明所在 Banach/Hilbert 空间及其对偶；不等同于测度弱收敛 |
| `\Longrightarrow` | 逻辑蕴含 | 不再用此箭头兼指弱收敛 |

### F. 特定小节的辅助记号

这些符号不提升为全文同一数学对象，但在符号表中标明位置和用途：

- 线性 ODE：`\mathcal X=C^1(I;V)`、`\mathcal Y=C(I;V)`、`\mathsf M_A`、`\mathsf D_A:=\partial_t-\mathsf M_A`、`\mathcal H=\ker\mathsf D_A`、评价映射 `E_t`、逆解算映射 `S_t`、零初值空间 `\mathcal K_s`、特解 `\gamma_{\mathrm p}`、齐次轨迹 `\eta` 和仿射解集。路径可在函数空间评价处写 `\gamma(t)`，与动力学式中的 `\gamma_t` 明确为同一取值，不混用时间与迭代指标。
- 冷却例子：温度用 `T_t`、环境温度 `T_{\mathrm{env}}`，与终止时间 T 分开；局部衰减率 `\lambda` 仍保留。
- 最小加权作用量：权重 `w_t`、作用量 `I[\gamma]`、累积重参数 `\Theta_w(t):=\int_0^t w_r^{-1}\mathrm dr`；后者替换 W(t)，避免与 Brownian 记号混淆。
- 截断 Gaussian：标准密度 `\varphi`、上尾 `\bar\Phi`、阈值 b、条件律 `\mu_b`、逆 Mills 比 `m(b)` 和 `\mathcal J_\alpha(b)`。阈值 b 不是 SDE 漂移函数，标出该例的作用域即可。
- 凸性证明：混合权重用 `\vartheta\in[0,1]`，将 `\theta` 留给学习参数；参考测度明确写出，不默认是 Lebesgue 测度。
- 传输构造：重权函数 `w`、对应 `\rho_w,Z_w`、CDF `F_0,F_w`、传输映射 `F_{\mathrm{tr}}`、三角分量 `F_{\mathrm{tr}}^i`、经验测度 `\widehat\mu_{w,N_{\mathrm{samp}}}`。
- 有限体积：`D_{\mathrm{diff}}`、转移率 `q_{i\to j}^{\Delta x}`、质量列向量的生成矩阵 `Q^{\Delta x}`、边通量 `j_{i+1/2}^{\Delta x}`、平衡质量 `\pi_i^{\Delta x}`。矩阵约定固定为 `\dot m=Q^{\Delta x}m`，其列和为零；可观测量生成矩阵是转置，不暗中更换行列约定。
- 半离散质量 `m_i^{\Delta x}(t)` 是有限维连续时间系统的精确解；上标标明空间近似。它与原 PDE 的精确单元积分不是恒等关系。若再数值积分该系统，才写 `\widehat m_{k,i}^{\Delta x}`。原题 ghost-cell 记号作为引文保留并给出本文对应记号，不篡改原题边界条件。
- OU：完整二维过程 `R_t`、正定矩阵 `A_{\mathrm{OU}}`、均值 `m_t^{\mathrm{OU}}`、协方差 `\Sigma_t`、闭合模型 `\bar X_t`、条件函数 `g_t`、完整/闭合自协方差 `C_{\mathrm{full}},C_{\mathrm{closure}}`。均值不与有限体积质量向量 m 共享裸记号。
- ODE 附录：局部存在时间半径用 `\delta_{\mathrm{loc}}`（避免被误读为随 t 变化的函数）；Picard 映射用 `\mathsf Q_{s,x}`，迭代用 `\gamma^{[n]}`；Peano--Baker 项用 `P_n(t,s)`，部分和用 `U^{[n]}(t,s)`；积分系数矩阵用 `B_A(t,s):=\int_s^t A_r\mathrm dr`；排序符号 `\mathcal T` 保留原有前向/后向区别。

## 四、前置符号表的具体安排

采用与 `book` 文档类一致的 `\chapter*{Notation and Conventions}`，加入目录但不参与正文、公式和定理编号。Introduction 含有实际内容介绍，虽属无编号前置章，按作者要求放在符号表之后。最终顺序：

**标题页 → 目录 → Notation and Conventions → Introduction → Source Index → 正式正文。**

理由：目录先提供导航；全局约定在引言及正式数学论述之前可查；Introduction 保持内容及无编号性质。

符号表分为 **Global Notation** 与 **Topic-specific Notation** 两层；前者列全文稳定对象及运算，后者按 ODE、Hamiltonian、信息论、条件几何、学习、Markov 离散与 OU 分组。使用可跨页的三列表格：`Symbol / Mathematical object / Definition and convention`，第三列注明局部作用域及定义小节。项目已有 `longtable` 和 `array`，无需增加依赖。表格页数由实际编译确定，不为压缩篇幅删去类型和作用域。

正文第一次出现时仍给定义；符号表是索引，不替代定理所需假设。表内可附到定义小节的链接，对尚无定位标签的定义只加不影响编号的锚点。不会在表内提前使用未说明的密度、条件律或生成元。

## 五、分节实施顺序

1. 建立旧记号 → 新记号 → 类型 → 作用域 → 首次定义位置的登记表，先锁定上面的核心决定。
2. 基础节：统一空间、分量、概率律和函数—测度配对，保留已有对偶及反序复合关系。
3. ODE 与几何：处理线性算子重名、A_t/外加项、M/J、帽子轨迹、运动区域、Hamiltonian 和能量表格；不删此前补充的分量推导与误差论证。
4. 熵与信息论：统一势能、自由能、score/Hessian、目标函数及参数；保留 KL 顺序、共轭对和取得极值的条件。
5. 条件/有效动力学：统一 d/m、水平集、coarea Jacobian、平衡与时变条件律、投影系数 b_t/a_t；保留原来的一时刻分布与路径律区别。
6. 学习及离散化：区分插值、模型、拟合与数值积分；处理重权函数、样本、空间网格、Markov 生成矩阵的行列约定。
7. OU 与附录：统一矩阵参数、均值、条件回归记号；修复附录 J/M、初值扰动和 Picard/时间排序的冲突。
8. 加入前置符号表，将图注、算法、表头、证明正文与公式一起核对，最后完善登记表及修改报告。

不会进行全局盲替换。对同形但不同身份的符号逐处判定；既有标签、引用键、Source Index 的 45 个入口和主要论证均保留。必要的纯记号调整不引入新定理、新假设或新的数值结论。

## 六、文件范围与验收

主要实施文件为 `paper/main.tex` 与 `paper/preamble.tex`。若拆出符号表子文件，需同步现有源码检查器的读取方式；更简单的初次方案是先内嵌前置符号表，不改项目结构。

当前 `scripts/check_manuscript_audit.py` 的历史 baseline 模式要求表格数量与旧稿相同。新增符号表后，应为明确新增的前置表作专门核对，同时继续检查全部原有数学表格和标签，不通过删除检查来掩盖差异。

图件只在可见数学标记与新规范不一致时修改标签及对应绘图源；实验算法、CSV/JSON 字段和既有数值结果不为排版重命名。若需重新导出图形，核对坐标数据与原版一致。独立的 Beamer 幻灯片不属于本轮“当前笔记”改稿范围，可另行沿用此规范。

验收内容：

- 每一个重要对象有定义、类型、作用域和可定位的首次定义；合法局部复用有明确说明。
- `x_k` 等疑似冲突只作为上下文检查线索；不依靠正则表达式自动判定数学含义。
- 全部原标签、交叉引用、定理/证明结构、数值表内容和来源入口保留。
- 检查导数矩阵维数、乘法次序、求值点、初末时刻及空间/时间网格尺度。
- 核对旧新版本的数学等价性，重点检查 Jacobian 乘积、相对误差、连续性方程、OU 公式及 Markov 矩阵约定。
- 执行源码检查、完整 XeLaTeX/Biber 编译及 PDF 导航检查；人工查看前置长表的跨页表头、宽度和数学排版。
- 最终提供按小节的改名清单、保留的局部约定、符号表位置和编译结果。

先向作者输出本修订版的最终核心规范与旧新映射，再按上述顺序实施。每一主题及其相关附录通过数学等价性检查、编译和引用检查后，才能进入下一主题。SDE 数值状态明确使用 `\widehat X_k`，且不把该约定误当作所有学科的统一规则。
