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
    }
  }
  field.addEventListener('input', show);
  field.addEventListener('change', show);
  show();
});