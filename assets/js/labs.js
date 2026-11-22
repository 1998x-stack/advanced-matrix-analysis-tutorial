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
    } else if (kind === 'svd-gap') {
      const gap = n, next = 2-gap;
      output.textContent = 'Δ=' + gap.toFixed(1)
        + '：σ₂=2，σ₃=' + next.toFixed(1) + '；'
        + (gap > 1e-9
          ? '截断位置有间隙，最佳 rank-2 近似唯一。'
          : '截断处并列，最佳 rank-2 近似不唯一。');
    } else if (kind === 'svt') {
      const tau = n, s = [5,2,.5].map(v => Math.max(v-tau,0));
      const kept = s.filter(v => v>0).map(v => v.toFixed(2));
      output.textContent = 'τ=' + tau.toFixed(2) + '：保留奇异值 ['
        + kept.join(', ') + ']，输出秩为 ' + kept.length + '。';
    } else if (kind === 'stiefel') {
      const defect = n*n*Math.sqrt(25.25**2 + 36.25**2 + 2*30**2);
      output.textContent = 'η=' + n.toFixed(2)
        + '：试探点 Gram 误差 ‖XtrialᵀXtrial−I‖F≈'
        + defect.toFixed(4) + '；QR retraction 后为数值零。';
    } else if (kind === 'sylvester') {
      const x = 1/n;
      output.textContent = 'δ=' + n.toFixed(1)
        + '：标量 Sylvester 子问题 δx=1 的解 x='
        + x.toFixed(3) + '；δ 越接近 0，解对扰动越敏感。';
    } else if (kind === 'nmf') {
      const V=[[2,1,0],[1,2,1],[0,1,2]];
      let W=[[1,.2],[.2,1],[.5,.5]];
      let H=[[1,.5,.2],[.2,.5,1]];
      const mul=(A,B)=>A.map(row=>B[0].map((_,j)=>row.reduce((s,v,k)=>s+v*B[k][j],0)));
      const tr=A=>A[0].map((_,j)=>A.map(row=>row[j]));
      const objective=()=>{const R=mul(W,H);return .5*R.reduce((s,row,i)=>s+row.reduce((z,v,j)=>z+(V[i][j]-v)**2,0),0);};
      const initial=objective();
      for(let k=0;k<n;k++){
        const Wt=tr(W), numH=mul(Wt,V), denH=mul(mul(Wt,W),H);
        H=H.map((row,i)=>row.map((v,j)=>denH[i][j]===0?0:v*numH[i][j]/denH[i][j]));
        const Ht=tr(H), numW=mul(V,Ht), denW=mul(mul(W,H),Ht);
        W=W.map((row,i)=>row.map((v,j)=>denW[i][j]===0?0:v*numW[i][j]/denW[i][j]));
      }
      output.textContent=n+' 轮完整 H/W 更新：损失 '
        +objective().toFixed(6)+'（初始 '+initial.toFixed(6)+'），因子保持非负。';
    }
  }
  field.addEventListener('input', show);
  field.addEventListener('change', show);
  show();
});