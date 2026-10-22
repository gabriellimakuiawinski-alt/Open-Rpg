/* mesa-fx.js — efeitos animados do tabletop (camada por cima do mapa; não mexe na lógica) */
(function(){
try{
if(matchMedia('(prefers-reduced-motion: reduce)').matches)return;
const cvm=document.getElementById('c');if(!cvm)return;
const fx=document.createElement('canvas');fx.id='fx';
fx.style.cssText='position:fixed;inset:0;width:100%;height:100%;pointer-events:none;z-index:1';
cvm.after(fx);const g2=fx.getContext('2d');
const FITA='220,198,106',RED='210,58,44';
let W=0,H=0,DPR=1;
function size(){DPR=Math.min(devicePixelRatio||1,2);W=innerWidth;H=innerHeight;fx.width=W*DPR;fx.height=H*DPR}
size();addEventListener('resize',size);

/* ---------- partículas ---------- */
const P=[],R=[]; // P: faíscas/poeira; R: ondas
const rnd=(a,b)=>a+Math.random()*(b-a);
function onda(x,y,r,cor,dur){R.push({x,y,r,cor:cor||FITA,t:0,dur:dur||650})}
function burst(x,y,n,cor){for(let i=0;i<n;i++){const a=rnd(0,6.283),s=rnd(40,160);P.push({x,y,vx:Math.cos(a)*s,vy:Math.sin(a)*s-30,l:0,d:rnd(450,900),s:rnd(1.5,3.6),c:cor||FITA})}}
/* poeira ambiente: partículas lentas, bem discretas */
const M=[];for(let i=0;i<28;i++)M.push({x:Math.random()*W,y:Math.random()*H,v:rnd(4,12),a:rnd(.05,.22),s:rnd(.8,2),p:rnd(0,6.28)});

/* ---------- conversão mundo -> tela ---------- */
const sx=x=>x*S.v.z+S.v.x,sy=y=>y*S.v.z+S.v.y;
function rectTok(t){const b=t.z*S.gs;return{x:sx(t.x),y:sy(t.y),w:b*S.v.z,h:b*S.v.z}}

/* ---------- observa fichas/tokens ---------- */
let known=null,pos=new Map(),quiet=new Map(),cena=null,sw=false;
function observar(now){
  if(typeof S==='undefined'||!S.tok)return;
  const ids=new Set();
  S.tok.forEach(t=>{ids.add(t.id);
    const r=rectTok(t),c=[r.x+r.w/2,r.y+r.h/2];
    if(known&&!known.has(t.id)&&!(typeof VIEW!=='undefined'&&VIEW&&t.hid)){
      onda(c[0],c[1],Math.max(r.w*.75,26),FITA,800);onda(c[0],c[1],Math.max(r.w*.5,18),FITA,560);burst(c[0],c[1],14)}
    const p=pos.get(t.id);
    if(p&&(p.x!=t.x||p.y!=t.y))quiet.set(t.id,now);
    pos.set(t.id,{x:t.x,y:t.y});
    const q=quiet.get(t.id);
    if(q&&now-q>140){quiet.delete(t.id);if(known)onda(c[0],c[1]+r.h*.35,Math.max(r.w*.55,20),'200,190,160',420)}
  });
  if(known)[...known].forEach(id=>{if(!ids.has(id)&&pos.has(id)){ // token removido: fumaça onde estava
    const p=pos.get(id);burst(sx(p.x+S.gs/2),sy(p.y+S.gs/2),10,'190,180,150');pos.delete(id)}});
  known=ids;
  if(S.cur!==cena){if(cena!==null)trocaCena();cena=S.cur}
}
function trocaCena(){
  let o=document.getElementById('fx-cena');
  if(!o){o=document.createElement('div');o.id='fx-cena';document.body.append(o)}
  o.classList.remove('go');void o.offsetWidth;o.classList.add('go')}

/* ---------- seleção: anel pulsante e cantos ---------- */
function selecao(now){
  if(typeof VIEW!=='undefined'&&VIEW)return;
  const o=(typeof sel!=='undefined'&&sel)||(typeof selM!=='undefined'&&selM);if(!o||typeof RC!=='function')return;
  let r;try{r=RC(o)}catch(e){return}
  const x=sx(r.x),y=sy(r.y),w=r.w*S.v.z,h=r.h*S.v.z,p=(Math.sin(now/260)+1)/2;
  g2.save();g2.lineWidth=2;
  g2.strokeStyle=`rgba(${FITA},${.25+p*.35})`;g2.shadowColor=`rgba(${FITA},.8)`;g2.shadowBlur=8+p*12;
  g2.strokeRect(x-4-p*2,y-4-p*2,w+8+p*4,h+8+p*4);
  g2.shadowBlur=0;g2.strokeStyle=`rgba(${FITA},.95)`;g2.lineWidth=3;
  const L=Math.min(14,w/3,h/3);
  [[x-4,y-4,1,1],[x+w+4,y-4,-1,1],[x-4,y+h+4,1,-1],[x+w+4,y+h+4,-1,-1]].forEach(([a,b,dx,dy])=>{g2.beginPath();g2.moveTo(a+dx*L,b);g2.lineTo(a,b);g2.lineTo(a,b+dy*L);g2.stroke()});
  g2.restore()}

/* ---------- laço ---------- */
let last=performance.now();
function frame(now){
  requestAnimationFrame(frame);
  if(document.hidden)return;
  const dt=Math.min(.05,(now-last)/1000);last=now;
  g2.setTransform(DPR,0,0,DPR,0,0);g2.clearRect(0,0,W,H);
  observar(now);
  /* poeira */
  g2.fillStyle='#f3ecd8';
  M.forEach(m=>{m.y-=m.v*dt;m.x+=Math.sin(now/2600+m.p)*6*dt;if(m.y<-4){m.y=H+4;m.x=Math.random()*W}
    g2.globalAlpha=m.a*(.6+.4*Math.sin(now/900+m.p));g2.beginPath();g2.arc(m.x,m.y,m.s,0,6.283);g2.fill()});
  g2.globalAlpha=1;
  /* ondas */
  for(let i=R.length-1;i>=0;i--){const o=R[i];o.t+=dt*1000;const k=o.t/o.dur;if(k>=1){R.splice(i,1);continue}
    const e=1-Math.pow(1-k,3);g2.strokeStyle=`rgba(${o.cor},${(1-k)*.9})`;g2.lineWidth=3*(1-k)+.5;
    g2.beginPath();g2.arc(o.x,o.y,o.r*(.35+e*.9),0,6.283);g2.stroke()}
  /* faíscas */
  for(let i=P.length-1;i>=0;i--){const q=P[i];q.l+=dt*1000;if(q.l>=q.d){P.splice(i,1);continue}
    q.vy+=120*dt;q.x+=q.vx*dt;q.y+=q.vy*dt;q.vx*=.97;const k=1-q.l/q.d;
    g2.fillStyle=`rgba(${q.c},${k})`;g2.beginPath();g2.arc(q.x,q.y,q.s*k+.4,0,6.283);g2.fill()}
  selecao(now);
}
requestAnimationFrame(frame);
window.MesaFX={onda,burst};

/* ---------- resultado de dados: sobe do centro, gira e some ---------- */
const log=document.getElementById('log');
if(log)new MutationObserver(ms=>{
  const n=ms.flatMap(m=>[...m.addedNodes]).filter(x=>x.nodeType==1||x.textContent.trim());
  if(!n.length)return;
  const first=log.firstElementChild||log.firstChild;const txt=(first&&first.textContent||'').trim();if(!txt)return;
  const el=document.createElement('div');el.className='fx-dado';
  const num=(txt.match(/=\s*(-?\d+)\s*$/)||txt.match(/(-?\d+)\s*$/)||[])[1];
  el.innerHTML=`<b>${num??'🎲'}</b><small>${txt.replace(/</g,'&lt;').slice(0,60)}</small>`;
  document.body.append(el);setTimeout(()=>el.remove(),2200);
  if(window.MesaFX)MesaFX.burst(W/2,H/2,18,RED)
}).observe(log,{childList:true});
}catch(e){console.warn('mesa-fx',e)}
})();
