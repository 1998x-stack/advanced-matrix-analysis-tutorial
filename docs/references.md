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

| 11 | 奇异值、截断低秩最优性 | [LAPACK DGESVD](https://www.netlib.org/lapack/explore-html/d1/d7f/group__gesvd_gac6bd5d4e645049e49bb70691180abf07.html) |
| 12 | 复/实 Schur、广义 QZ | [DGEES](https://netlib.org/lapack/explore-html/d5/d38/group__gees_gab48df0b5c60d7961190d868087f485bc.html) · [DGGES](https://www.netlib.org/lapack/explore-html/d7/d25/group__gges_ga556be4f39b39e5008c8eb36814aa7e20.html) |
| 13 | 秩亏最小二乘、最小范数伪逆 | [LAPACK DGELSD](https://www.netlib.org/lapack/explore-html/d9/d67/group__gelsd_ga0bee7e1b9e7e43f59ecf2419b2759c42.html) |
| 14 | Weyl、Davis–Kahan、Bauer–Fike | [Cornell CS 6210](https://www.cs.cornell.edu/courses/cs6210/2025fa/lec/2025-11-03.html) · [Eigenvalue Perturbation](https://tbetcke.github.io/math0058_lecture_notes/eigenvalues_perturbation_theory.html) |
| 15 | 微分、迹技巧与梯度约定 | [The Matrix Cookbook](https://www2.imm.dtu.dk/pubdb/pubs/3274-full.html) |

## 不可混淆的数学前提

- Jordan 标准形的“总是存在”结论默认在复数域；直接数值求 Jordan 形对扰动敏感。
- 标准 QR 用 Q 的列正交（矩形时 QᵀQ=I），不默认 QQᵀ=I。
- 实对称 / 复 Hermitian 是正交/酉谱分解的关键假设。
- Cholesky 要求严格正定（标准无主元版本）；PLU 的行交换必须同步作用于右端项。
- 范数界与数值算法实际前向误差不是同一个断言。
- 讲义中的 Python 示例特意保持在小规模固定数组上，不能代替经验证的工业级数值库。

| 16 | 迹微分、谱函数与奇异值导数 | [MIT 18.S096 Matrix Calculus](https://ocw.mit.edu/courses/18-s096-matrix-calculus-for-machine-learning-and-beyond-january-iap-2023/pages/lecture-notes-and-readings/) · [MIT 18.065 Lecture 16](https://ocw.mit.edu/courses/18-065-matrix-methods-in-data-analysis-signal-processing-and-machine-learning-spring-2018/resources/lecture-16-derivatives-of-inverse-and-singular-values/) · [Lewis (1996)](https://doi.org/10.1287/moor.21.3.576) |
| 17 | 近端方法、核范数 SVT 与 ADMM | [Boyd et al. ADMM](https://www.nparikh.org/publications/admm/) · [Cai–Candès–Shen SVT](https://doi.org/10.1137/080738970) · [Beck–Teboulle FISTA](https://doi.org/10.1137/080716542) |
| 18 | Stiefel/Grassmann、切空间与 retraction | [Pymanopt Manifolds](https://pymanopt.org/docs/stable/manifolds.html) · [Absil–Mahony–Sepulchre](https://press.princeton.edu/books/hardcover/9780691132983/optimization-algorithms-on-matrix-manifolds) · [Boumal (2023)](https://www.nicolasboumal.net/book/) |
| 19 | vec 恒等式、Sylvester 与 Lyapunov 方程 | [Cornell CS 6210](https://www.cs.cornell.edu/~bindel/class/cs6210-f16/lec/2016-11-02.pdf) · [SciPy solve_sylvester](https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.solve_sylvester.html) · [SciPy solve_continuous_lyapunov](https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.solve_continuous_lyapunov.html) |
| 20 | NMF 乘性更新、求解器与可辨识性 | [Lee–Seung (2001)](https://www.cs.cornell.edu/courses/cs6241/2020sp/readings/Lee-Seung-2001-NMF.pdf) · [scikit-learn NMF](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.NMF.html) · [Gillis, NMF](https://epubs.siam.org/doi/book/10.1137/1.9781611976410) |
