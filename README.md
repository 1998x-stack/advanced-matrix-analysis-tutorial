# 高级矩阵分析 · Matrix Atlas

一个以**几何直觉 → 严格定义 → 图解 → 可复算实验 → 应用边界**组织的 28 章矩阵分析教程。

- [课程首页](https://1998x-stack.github.io/advanced-matrix-analysis-tutorial/)
- [从第 01 章开始](https://1998x-stack.github.io/advanced-matrix-analysis-tutorial/chapters/01.html)
- [Olah-style-posts 创作规范](https://github.com/1998x-stack/Olah-style-posts)

## 内容架构

| 模块 | 章节 | 主要内容 |
|---|---|---|
| I · 基础结构 | 01–07 | 线性空间、特殊矩阵、范数、特征值、Jordan、矩阵函数 |
| II · 分解与稳定性 | 08–14 | LU/QR、谱定理、SVD、广义逆、扰动理论 |
| III · 优化与应用 | 15–21 | 矩阵微分、流形优化、Kronecker、NMF、稀疏 |
| IV · 高阶扩展 | 22–28 | 随机矩阵、张量分解、矩阵在深度学习中的应用 |

**改造状态**：01–15 章为三批独立重构的图解版（原生 MathML、原创 SVG、可重复数值实验）；16–28 保留原内容待逐章升级。请勿将“已迁移路径”与“已完成深度内容审校”混为一谈。

## 仓库结构

```text
index.html                    # GitHub Pages 首页
chapters/01.html ... 28.html  # 全部课程文章，01–15 深度重构
assets/css/site.css           # 首页与新文章共用的设计系统
assets/js/labs.js             # 无依赖、可渐进增强的互动实验
assets/figures/*.svg          # 独立原创教学插图
courses.json                  # 章节数据与维护状态
scripts/build_site.py         # 生成 _site/ 静态发布目录
scripts/validate_site.py      # 检查章节、链接、关键语义
.github/workflows/            # 持续集成与 GitHub Pages Actions 部署
docs/                         # 教学证据与迁移说明
AGENTS.md                     # 作者和自动化代理须遵守的内容标准
01.html ... 28.html           # 旧链接兼容跳转（请不要删除）
```

## 本地预览与构建

需要 Python 3.10+，无需 Node.js、服务端框架或网络依赖：

```bash
python scripts/validate_site.py
python scripts/build_site.py
python -m http.server 8000
```

浏览器打开 `http://localhost:8000/`。构建结果写入 `_site/`，仅包含可公开页面、样式、图解、数据与兼容跳转。

## GitHub Pages

推荐使用仓库 **Settings → Pages → Build and deployment → GitHub Actions**，部署工作流为 `.github/workflows/pages.yml`，在推送 `main` 时构建 `_site/` 并部署。若当前 Pages 仍采用 `main/(root)` 分支发布，根目录 `index.html` 与所有旧章节重定向仍可使用；需在更改来源后检查实际站点 URL 与资源链接。创建工作流不等于已更改 Pages 设置或完成部署。

## 审校原则

1. 每一篇独立可理解，不假设读者看过“上一讲”。
2. 先核对数学条件，再绘图；矩阵维度、实数/复数域、定理前提不能省略。
3. 内嵌代码与实验需标示数值是示例，不得把示意图当定理证明。
4. 图必须写明问题、对象、箭头含义和可独立阅读的图注。
5. 参见 [AGENTS.md](AGENTS.md) 与 [参考资料](docs/references.md)。

## 引用与许可

核心阅读参考 MIT 18.06/18.065 公开课程与标准矩阵分析结论，详见各章节底部及 `docs/evidence.json`；原创网页和图示不直接复制第三方课程配图。保留原内容作者已有署名、引用及相关许可信息。

## 三批深度重构（01–15）

- **01–05**：线性映射、秩-零化度、结构矩阵、范数与内积、特征值与谱半径。
- **06–10**：Jordan 链、矩阵指数、带部分主元 LU、Householder QR、对称谱定理与 Rayleigh 商。
- **11–15**：奇异值分解与低秩逼近、实/复 Schur 与 QZ、最小范数伪逆、Weyl/Davis–Kahan/Bauer–Fike、矩阵微分与梯度核对。
- 每章都有独立的学习问题、数学条件、原生 MathML、单独 SVG 与标准库 Python 算例；旧章节仍保留原路径兼容入口。
- [各章审校依据](docs/references.md) · [数学例子自动化测试](scripts/test_examples.py)

> 浏览器截图和 360/390px 移动端逐页验收需单独执行；静态结构检查不能代替真实浏览器审校。

## 第三批可验证知识边界

- 每篇包含可复算输入、预期输出、局限与资料链接；新增 9 幅独立 SVG（累计 21 幅）。
- SVD 按奇异值范数讨论最优 rank-k 逼近，未将“保留能量”误称为泛化效果。
- QZ 使用齐次特征值 (α,β) 解释无穷远值，避免对奇异 B 直接求逆。
- Moore–Penrose 伪逆同时解决最小残差与最小范数；与 Tikhonov 正则化的偏差区别明确。
- Davis–Kahan 需谱隔离，Bauer–Fike 要求可对角化；对非正规矩阵保留反例。
- 矩阵梯度遵守 Frobenius 内积和尺寸约定，可用中心差分独立检验。
