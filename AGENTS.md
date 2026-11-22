# AGENTS.md — 高级矩阵分析教程的内容与工程契约

> 所有参与写作、审校、SVG 绘制、代码生成与发布的贡献者均适用。

## 目标
以独立可读、数学正确、可复算的长文章解释高级矩阵分析。使用 [Olah-style Paper Posts](https://github.com/1998x-stack/Olah-style-posts/blob/main/skills/olah-style-paper-posts/SKILL.md) 的“问题→机制→公式→实验→边界”路径，原创绘图，勿复制 Colah 或 MIT 的图文。

## 目录边界
- 唯一课程目录源：`courses.json`。章节正文放在 `chapters/NN.html`，01–28 编号稳定。
- 根目录 `NN.html` 是历史入口的兼容重定向，禁止移除。
- 新版 CSS 放在 `assets/css/site.css`；新增交互逻辑集中 `assets/js/labs.js`；插图放在 `assets/figures`。
- 06–28 的旧版仍依赖 `chapters/theme.css`；没有逐篇审校前不能标为“深度图解”。
- 在 `docs/evidence.json` 记录有来源支持的陈述及日期；课内题目必须有清楚假设。

## 每篇文章必须满足
1. 一个 H1，按逻辑顺序使用 H2；开头给具体问题，不写“本讲介绍/上一章已经”。
2. 说明 `A∈F^{m×n}` 等对象定义，区分实域/复域、方阵/矩形、可逆/奇异。
3. 关键公式使用离线可渲染的 MathML（`mfrac`、`msup`、`msub`、`mtable` 等），不依赖远程 MathJax/KaTeX；禁止 Unicode 伪分式。
4. SVG 具备 `xmlns`、`viewBox`、`title`、`desc`，主标签在标称尺寸下 ≥13px，解释颜色与箭头；图注须提出可验证观察。
5. 至少一个完整算例：给定输入、预期输出、可复算步骤/代码，并给出边界条件或失败模式。
6. 交互可键盘操作、默认状态无需 JS 可理解、`output` 与输入关联；禁用动效时不损害内容。
7. 正文列真实参考来源；没有核查的指标或结论不能写成确定事实。

## 验收清单
- `python scripts/validate_site.py` 与 `python scripts/build_site.py` 成功。
- 1440px desktop 与 390/360px mobile 浏览；正文和 MathML 无页面横向溢出，图中文字可读。
- 检查缺失资源、站内链接、JS 控制台错误、交互输出、焦点可见与打印样式。
- 代码示例实际运行；截图或浏览器 QA 未执行时明确注明“未验证”。
- 发布前核对 diff、CI、Pages 设置和公开 URL；不要把工作流提交等同于上线。

## 首批数学高风险审计
- 01 章：面积倍率是 `|det(A)|`；条件数需指明范数。
- 02 章：秩-零化度是定义域维数 `n`，不是值域维数 `m`。
- 03 章：实对称与复 Hermitian 区分；正定要求 Hermitian 并在非零向量上正二次型。
- 04 章：`‖A‖₂`（算子谱范数）与 `‖A‖F` 不可混淆；`p<1` 非范数。
- 05 章：复特征值与“实方向不变”不能混为一谈；特征多项式采用 `det(λI−A)` 时次高项为 `−tr(A)`。

## 维护流程
先搜标准教材/原始资料 → 写 claim/evidence 表 → 组织图解与 MathML → 实验与静态检查 → 浏览器验收 → PR 合并。单篇文章不应包含“使用了何种工具生成”等生产过程说明。

## 第二轮风险检查（06–10）
- **06 Jordan**：区分代数/几何重数；复数域 Jordan 形与数值敏感性。
- **07 指数**：时间流 e^{tA} 和元素级指数不同；不可交换矩阵不满足一般的指数拆分。
- **08 LU**：统一记号 PA=LU、右端 Pb；有限精度下主元策略与条件数分开。
- **09 QR**：精简 Q 的尺寸为 m×n；矩形时 QᵀQ=I，但 QQᵀ 不必等于 I。
- **10 谱定理**：实对称/复 Hermitian 才保证正交/酉特征基；Rayleigh 商和 Courant–Fischer 先写排序约定。
- CI 除 HTML/SVG 本地检查外执行 `python scripts/test_examples.py`；若没有真实浏览器 QA，不能标记该项通过。

## 第三批风险审计（11–15）
- **11 SVD**：A 为 m×n，U/V 空间不同；零奇异值不能求倒数；rank-k 在谱/Frobenius 范数最优。
- **12 Schur/QZ**：复 Schur 真上三角，实 Schur 可有 2×2 共轭块；广义无限特征值用 α/β 与 regular pencil 前提。
- **13 伪逆**：四个 Penrose 条件必须包含两个对称/厄米条件；优先最小残差，再选最小范数；阈值反映数值秩。
- **14 扰动**：Weyl 用 Hermitian/实对称，Davis–Kahan 明确谱隔离，Bauer–Fike 限可对角化；示意圆盘非真实特征轨迹。
- **15 导数**：必须声明分子/分母布局或 Frobenius 梯度；伴随变换和微分乘积次序不能混淆。
- 第 11–15 章新增实验必须在 `scripts/test_examples.py` 有确定性验证。
