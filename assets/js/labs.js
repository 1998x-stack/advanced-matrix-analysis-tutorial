'use strict';
document.querySelectorAll('[data-lab]').forEach(lab => {
  const kind = lab.dataset.lab;
  const field = lab.querySelector('input,select');
  const output = lab.querySelector('output');
  if (!field || !output) return;
  function show() {
    const raw = field.value, n = Number(raw);
    if (kind === 'area') {
      output.textContent = 'A = diag(' + n.toFixed(2) + ', ' + (1/n).toFixed(3)
        + ')：行列式 1；最大伸缩率 ' + n.toFixed(2) + '；κ₂ = ' + (n*n).toFixed(3);
    } else if (kind === 'rank') {
      output.textContent = raw === 'full'
        ? 'A=[[1,0,1],[0,1,1]]：rank=2，nullity=1；ker 由 (-1,-1,1) 张成。'
        : 'A=[[1,2,3],[2,4,6]]：rank=1，nullity=2；第二行与第一行线性相关。';
    } else if (kind === 'spd') {
      output.textContent = raw === 'positive'
        ? 'diag(2,1)：特征值均正；任意非零 x 均有 xᵀAx > 0。'
        : 'diag(2,−1)：取 x=(0,1)，二次型为 −1；矩阵不定。';
    } else if (kind === 'norm') {
      const value = raw === '1' ? 7 : raw === 'inf' ? 4 : 5;
      output.textContent = 'x=(3,4)，‖x‖' + (raw === 'inf' ? '∞' : raw)
        + ' = ' + value.toFixed(3) + '。';
    } else if (kind === 'power') {
      const a = 3**n, length = Math.hypot(a, 1);
      const x = a/length, y = 1/length;
      const ray = 3*x*x + y*y;
      output.textContent = 'k=' + n + '；方向 ≈ (' + x.toFixed(4)
        + ', ' + y.toFixed(4) + ')；Rayleigh 商 ≈ ' + ray.toFixed(5) + '。';
    } else if (kind === 'jordan') {
      const diagonal = 2**n, upper = n===0 ? 0 : n * 2**(n-1);
      output.textContent = 'J^' + n + '：对角元 ' + diagonal
        + '，右上元 ' + upper + '，左下元 0。';
    } else if (kind === 'expm') {
      const e = Math.exp(2*n);
      output.textContent = 't=' + n.toFixed(2) + '：x(t)=e^(2t)(t,1)≈('
        + (e*n).toFixed(4) + ', ' + e.toFixed(4) + ')。';
    } else if (kind === 'pivot') {
      output.textContent = raw === 'swap'
        ? '交换两行：PA=[[1,3],[0,2]]，L=I，U=PA；主元为 1。'
        : '不交换：A 首主元为 0，不能直接进行标准无主元 LU 消元。';
    } else if (kind === 'qr') {
      output.textContent = raw === 'original'
        ? 'A 的两列是 (3,4) 和 (1,0)，第一列长度为 5。'
        : raw === 'reflect'
          ? 'H=[[0.6,0.8],[0.8,−0.6]]；H(3,4)=(5,0)。'
          : 'Q=H，R=[[5,0.6],[0,0.8]]；QᵀQ=I 且 QR=A。';
    } else if (kind === 'rayleigh') {
      const cosine = Math.cos(n*Math.PI/180), r = 1+2*cosine*cosine;
      output.textContent = 'θ=' + n + '°：R_A(x)=' + r.toFixed(4)
        + '（范围 [1,3]；θ 从主特征方向计量）。';
    } else if (kind === 'svd-rank') {
      const k = Number(raw), error = k === 0 ? Math.sqrt(29) : k === 1 ? 2 : 0;
      const kept = k === 0 ? '[]' : k === 1 ? '[5]' : '[5,2]';
      const fraction = k === 0 ? 0 : k === 1 ? 25/29 : 1;
      output.textContent = 'k=' + k + '：保留 ' + kept + '；Frobenius 误差 '
        + error.toFixed(4) + '；能量比例 ' + (fraction*100).toFixed(2) + '%。';
    } else if (kind === 'qz-beta') {
      output.textContent = raw === 'finite'
        ? 'α=2，β=1：λ=α/β=2，有限广义特征值。'
        : 'α=3，β=0：齐次广义特征值在无穷远，不可直接求 B⁻¹A。';
    } else if (kind === 'ridge') {
      const x = 4/(4+n);
      output.textContent = 'λ=' + n.toFixed(2)
        + '：xλ=(' + x.toFixed(4) + ',0)；预测 Ax=('
        + (2*x).toFixed(4) + ',0)。';
    } else if (kind === 'gap') {
      const theta = 0.5*Math.atan(2*n)*180/Math.PI;
      const bound = n/(1-n);
      output.textContent = 'ε=' + n.toFixed(2)
        + '：实际旋转 ' + theta.toFixed(3)
        + '°；由原间隙得到的保守 sinθ 界 '
        + bound.toFixed(3) + '。';
    } else if (kind === 'gradient') {
      const h = 10**(-n), plus = (1-h)**2, minus = (1+h)**2;
      const central = (plus-minus)/(2*h);
      output.textContent = 'h=1e−' + n + '；中心差分 '
        + central.toFixed(8) + '；解析方向导数 −2.00000000。';
    } else if (kind === 'kron-dim') {
      const size = [10, 100, 1000][Number(raw)];
      const elems = size * size * size * size, bytes = elems * 8;
      const fmt = bytes >= 1e12 ? (bytes/1e12).toFixed(2) + ' TB'
        : bytes >= 1e9 ? (bytes/1e9).toFixed(2) + ' GB'
        : bytes >= 1e6 ? (bytes/1e6).toFixed(2) + ' MB' : bytes + ' B';
      output.textContent = 'A、B 均为 ' + size + '×' + size + '：A⊗B 为 '
        + (size*size) + '×' + (size*size) + '，元素数 n⁴='
        + elems.toExponential(2) + '，float64 约 ' + fmt + '。';
    } else if (kind === 'nmf-rank') {
      const r = Number(raw);
      output.textContent = r === 1
        ? 'r=1：残差 ‖A−WH‖_F = 0.3660；相对误差 6.68%。'
        : 'r=2：残差 0.0000；相对误差 0.00%（W=A、H=I 即精确重建）。';
    } else if (kind === 'shrink') {
      const lam = n, y = 0.3;
      const l1 = Math.max(y - lam, 0);
      const l2 = y / (1 + 2 * lam);
      output.textContent = 'λ=' + lam.toFixed(2) + '（固定 y=0.3）：ℓ₁ 解='
        + l1.toFixed(4) + '，ℓ₂ 解=' + l2.toFixed(4) + '。';
    } else if (kind === 'mp-gamma') {
      const g = n, s = Math.sqrt(g);
      const a = (1 - s) * (1 - s), b = (1 + s) * (1 + s);
      const mass = g > 1 ? '；λ=0 处 δ 峰质量 ' + (1 - 1 / g).toFixed(3) : '；无 0 处 δ 峰';
      output.textContent = 'γ=' + g.toFixed(2) + '：MP 支撑 [' + a.toFixed(3)
        + ', ' + b.toFixed(3) + ']' + mass + '。';
    } else if (kind === 'unfold') {
      const dims = [2, 3, 2];
      const n0 = Number(raw);
      const rows = dims[n0 - 1];
      const cols = dims.reduce((a, b) => a * b, 1) / rows;
      output.textContent = 'T∈R^{2×3×2}，模-' + n0 + '展开 T_(' + n0
        + ')∈R^{' + rows + '×' + cols + '}；元素总和 78，平方和 650。';
    }
  }
  field.addEventListener('input', show);
  field.addEventListener('change', show);
  show();
});