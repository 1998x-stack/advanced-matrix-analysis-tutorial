# 数学资料与示例审校索引

本教程从问题出发组织叙述，所有图示独立原创，不直接复刻第三方讲义插图。每章底部保留引用；验证要区分“数学定理证明”“低维数值示例”“数值实现经验”。

| 章 | 核查主轴 | 首要资料 |
|---|---|---|
| 01 | 线性变换、行列式、误差放大 | [MIT 18.06](https://www.mit.edu/~18.06/) |
| 02 | 子空间、秩与零化度 | [MIT 18.06](https://github.com/mitmath/1806) |
| 03 | 正交、对称、正定矩阵 | [MIT 18.065](https://github.com/mitmath/18065) |
| 04 | 诱导算子范数与奇异值 | [MIT 18.065](https://ocw.mit.edu/courses/18-065-matrix-methods-in-data-analysis-signal-processing-and-machine-learning-spring-2018/) |
| 05 | 特征值、谱半径与幂迭代 | [MIT 18.06](https://www.mit.edu/~18.06/) |
| 06 | Jordan 链、广义特征向量 | [MIT Generalized Eigenvectors Notes](https://web.mit.edu/18.06/www/Spring09/generalized-eigenvectors.pdf) |
| 07 | 矩阵指数、缩放平方算法 | [Higham, SIAM 2005](https://eprints.maths.manchester.ac.uk/634/) |
| 08 | PA=LU 与部分主元选取 | [LAPACK DGESV](https://www.netlib.org/lapack/explore-html/d8/da6/group__gesv_ga831ce6a40e7fd16295752d18aed2d541.html) |
| 09 | Householder QR | [LAPACK DGEQRF](https://www.netlib.org/lapack/explore-html/d0/da1/group__geqrf_gade26961283814bb4e62183d9133d8bf5.html) |
| 10 | Rayleigh、Courant–Fischer | [MMiDS Textbook](https://mmids-textbook.github.io/chap05_specgraph/03_extremal/roch-mmids-specgraph-extremal.html) |

## 不可混淆的数学前提

- Jordan 标准形的“总是存在”结论默认在复数域；直接数值求 Jordan 形对扰动敏感。
- 标准 QR 用 Q 的列正交（矩形时 QᵀQ=I），不默认 QQᵀ=I。
- 实对称 / 复 Hermitian 是正交/酉谱分解的关键假设。
- Cholesky 要求严格正定（标准无主元版本）；PLU 的行交换必须同步作用于右端项。
- 范数界与数值算法实际前向误差不是同一个断言。
- 讲义中的 Python 示例特意保持在小规模固定数组上，不能代替经验证的工业级数值库。
