'use strict';
document.querySelectorAll('[data-lab]').forEach(lab=>{
const kind=lab.dataset.lab,field=lab.querySelector('input,select'),output=lab.querySelector('output');
if(!field||!output)return;
function render(){
const raw=field.value,n=Number(raw);
if(kind==='area'){const inv=(1/n).toFixed(3);output.textContent='变换 A = diag('+n.toFixed(1)+', '+inv+')：面积倍率 det(A)=1；最大长度倍率 '+n.toFixed(1)+'；条件数 '+(n*n).toFixed(2);}
if(kind==='rank'){output.textContent=raw==='full'?'A = [[1,0,1],[0,1,1]]：rank(A)=2，nullity(A)=1；零空间由 (-1,-1,1) 张成。':'A = [[1,2,3],[2,4,6]]：rank(A)=1，nullity(A)=2；两行不独立。';}
if(kind==='spd'){output.textContent=raw==='positive'?'A = [[2,0],[0,1]]：特征值 2、1；对所有非零 x，xᵀAx > 0。':'A = [[2,0],[0,-1]]：特征值 2、−1；取 x=(0,1) 得 xᵀAx = −1，不是正定矩阵。';}
if(kind==='norm'){const val=raw==='inf'?4:raw==='1'?7:Math.sqrt(25);output.textContent='x=(3,4) 的 ‖x‖'+(raw==='inf'?'∞':raw)+' = '+val.toFixed(3)+'；单位球边界由相应范数确定。';}
if(kind==='power'){const a=Math.pow(3,n),b=1,den=Math.hypot(a,b),x=a/den,y=b/den,ray=3*x*x+y*y;output.textContent='迭代 '+n+' 次：归一化方向 ≈ ('+x.toFixed(4)+', '+y.toFixed(4)+')；Rayleigh 商 ≈ '+ray.toFixed(4)+'（极限为 3）。';}
}
field.addEventListener('input',render);field.addEventListener('change',render);render();
});