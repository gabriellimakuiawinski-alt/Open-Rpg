/* Luzes fixas coloridas (etapa 17)
   Só o mestre/admin põe. Agem como lampiões (todas as direções) ou lanternas (cone) paradas no mapa,
   com cor, alcance e intensidade, e só valem com a cena escura ligada. Respeitam as paredes (inclusive a borda dos interiores).
   Cada luz: {id, x, y, R (quadrados), c (cor), a (intensidade), t ('l' lampião | 'c' lanterna), la (abertura do cone), d (direção em graus, 0 = direita)}.
   Ficam em S.luzes e são salvas em cenas.luzes. Entram em lightsData() (escuridão) e ganham um brilho colorido por cima. */
(function(){
const LUZ=window.LUZ={sel:null,def:{c:'#ffb84d',R:6,a:.9,t:'l',la:60,d:0},cache:new Map};
const list=()=>S.luzes||(S.luzes=[]);
const sel=()=>{if(!LUZ.sel)return null;const L=list();if(L.includes(LUZ.sel))return LUZ.sel;LUZ.sel=L.find(q=>q.id==LUZ.sel.id)||null;return LUZ.sel};
const snap=n=>{const q=(S.gs||50)/4;return Math.round(n/q)*q};
const COR=[['Lampião','#ffb84d'],['Vela','#ff8a3c'],['Fria','#9fd0ff'],['Verde','#6dff9f'],['Vermelha','#ff4d4d'],['Roxa','#b980ff'],['Branca','#ffffff']];
const rgb=h=>{const m=/^#?([0-9a-f]{6})$/i.exec(h||'');const n=m?parseInt(m[1],16):0xffb84d;return[n>>16&255,n>>8&255,n&255]};

/* luzes fixas no formato de lightsData() */
LUZ.fixas=function(){
 const g=S.gs;
 return list().map(o=>{
  const R=Math.max(.5,+o.R||1)*g,key=[o.x,o.y,R,g,WV].join();
  let c=LUZ.cache.get(o.id);
  if(!c||c.k!=key){c={k:key,p:vis(o.x,o.y,R,S.walls)};LUZ.cache.set(o.id,c)}
  return{cx:o.x,cy:o.y,R,la:o.t=='c'?(o.la>0&&o.la<360?o.la:60):360,ld:(o.d||0)*Math.PI/180,p:c.p,c:o.c||'#ffb84d',a:o.a==null?1:o.a}
 })
};

/* brilho colorido por cima da escuridão */
LUZ.tint=function(x,v,Q,lg){
 const T=lg.filter(L=>L.c);if(!T.length)return;
 x.save();x.setTransform(v.z*Q,0,0,v.z*Q,v.x*Q,v.y*Q);x.globalCompositeOperation='screen';
 for(const L of T){
  const[r,g,b]=rgb(L.c),a=L.a==null?1:L.a;
  x.save();
  if(L.la<360){const h=L.la*Math.PI/360;x.beginPath();x.moveTo(L.cx,L.cy);x.arc(L.cx,L.cy,L.R*1.02,L.ld-h,L.ld+h);x.closePath();x.clip()}
  x.beginPath();L.p.forEach((q,i)=>i?x.lineTo(q[0],q[1]):x.moveTo(q[0],q[1]));x.closePath();x.clip();
  const gr=x.createRadialGradient(L.cx,L.cy,L.R*.05,L.cx,L.cy,L.R);
  gr.addColorStop(0,`rgba(${r},${g},${b},${.6*a})`);gr.addColorStop(.55,`rgba(${r},${g},${b},${.28*a})`);gr.addColorStop(1,`rgba(${r},${g},${b},0)`);
  x.fillStyle=gr;x.fillRect(L.cx-L.R,L.cy-L.R,L.R*2,L.R*2);
  x.restore()
 }
 x.restore()
};

/* marcas do mestre */
LUZ.marks=function(x,v){
 if(VIEW||!GER||pv)return;
 const L=list();if(!L.length||(!S.nt&&tool!='lz'))return;
 const z=v.z,s=sel();
 x.save();
 for(const o of L){
  const on=o===s&&tool=='lz',r=(on?11:8)/z;
  x.globalAlpha=tool=='lz'?1:.7;
  if(on){x.strokeStyle=o.c;x.lineWidth=1.5/z;x.setLineDash([6/z,5/z]);x.beginPath();x.arc(o.x,o.y,Math.max(.5,+o.R||1)*S.gs,0,7);x.stroke();x.setLineDash([])}
  if(o.t=='c'){const l=Math.max(.5,+o.R||1)*S.gs*.4,a=(o.d||0)*Math.PI/180;x.strokeStyle=o.c;x.lineWidth=2.5/z;x.beginPath();x.moveTo(o.x,o.y);x.lineTo(o.x+Math.cos(a)*l,o.y+Math.sin(a)*l);x.stroke()}
  x.fillStyle=o.c;x.strokeStyle='#000';x.lineWidth=3/z;x.beginPath();x.arc(o.x,o.y,r,0,7);x.stroke();x.strokeStyle='#fff';x.lineWidth=1.5/z;x.stroke();x.fill()
 }
 x.restore()
};

/* ponteiro (ferramenta Luz fixa) */
LUZ.down=function(p){
 const h=Math.max(16/S.v.z,S.gs*.3);
 const o=[...list()].reverse().find(q=>Math.hypot(q.x-p.x,q.y-p.y)<h);
 if(o){LUZ.sel=o;drag={k:'lz',o,dx:p.x-o.x,dy:p.y-o.y,moved:0,sx:p.x,sy:p.y};opts();draw();return}
 const d=LUZ.def,n={id:uid(),x:snap(p.x),y:snap(p.y),R:d.R,c:d.c,a:d.a,t:d.t,la:d.la,d:d.d};
 list().push(n);LUZ.sel=n;save();opts();draw();
 if(!S.nt)toast('Luz colocada. Ligue a "Cena escura" no painel para ver o efeito.')
};
LUZ.move=function(p){
 const d=drag;if(!d||d.k!='lz')return;
 if(!d.moved&&Math.hypot(p.x-d.sx,p.y-d.sy)>6/S.v.z)d.moved=1;
 if(d.moved){d.o.x=snap(p.x-d.dx);d.o.y=snap(p.y-d.dy);sync()}
};
LUZ.up=function(d){if(d.moved)save();opts();draw()};

/* painel */
LUZ.opts=function(){
 const s=sel(),v=s||LUZ.def,n=list().length;
 const B=(k,l,on,x)=>`<button data-lz=${k} ${x||''} class="${on?'on':''}">${l}</button>`;
 const R=(k,l,min,max,st,u)=>`<label>${l}: <b>${+(+v[k]).toFixed(2)}${u||''}</b> <input type=range min=${min} max=${max} step=${st} value=${v[k]} data-lzi=${k}></label>`;
 return `<h5>Luzes fixas</h5><p class=m style="font-size:12px">Toque no mapa para pôr uma luz. Toque numa luz para editar (arraste para mover). Só valem com a cena escura ligada.</p>`
  +`<div class=g2 style="grid-template-columns:1fr">${B('night','Cena escura: '+(S.nt?'ligada':'desligada'),S.nt,'data-o=night')}</div>`
  +`<h5>Cor</h5><div class=g2>${COR.map(([l,c])=>B('cor',l,(v.c||'').toLowerCase()==c,`data-v="${c}" style="border-left:12px solid ${c}"`)).join('')}</div><label>Outra cor <input type=color value="${v.c||'#ffb84d'}" data-lzi=c></label>`
  +`<h5>Tipo</h5><div class=g2>${B('tipo','Lampião',v.t!='c','data-v=l')}${B('tipo','Lanterna',v.t=='c','data-v=c')}</div>`
  +R('R','Alcance',1,30,.5,' quadrados')+R('a','Intensidade',.2,1,.05)
  +(v.t=='c'?R('la','Abertura',15,180,5,'°')+R('d','Direção',0,359,5,'°'):'')
  +(s?`<h5>Luz selecionada</h5><div class=g2>${B('del','Remover')}${B('dup','Duplicar')}</div>`:'')
  +(n?`<h5>${n} ${n==1?'luz':'luzes'} na cena</h5><div class=g2>${B('clr','Remover todas')}</div>`:'')
};

function aplica(k,val){
 const s=sel(),num=k!='c'&&k!='t';
 if(num)val=parseFloat(val);
 LUZ.def[k]=val;if(s)s[k]=val;
 sync();draw()
}
document.addEventListener('click',e=>{
 const b=e.target.closest&&e.target.closest('[data-lz]');
 if(!b||!b.closest('#opt'))return;
 const a=b.dataset.lz,s=sel();
 if(a=='night')return;
 e.stopPropagation();
 if(a=='cor'){aplica('c',b.dataset.v);save();opts();return}
 if(a=='tipo'){aplica('t',b.dataset.v);save();opts();return}
 if(a=='del'&&s){S.luzes=list().filter(q=>q!==s);LUZ.sel=null;save();opts();draw();return}
 if(a=='dup'&&s){const n={...s,id:uid(),x:s.x+S.gs/2,y:s.y+S.gs/2};list().push(n);LUZ.sel=n;save();opts();draw();return}
 if(a=='clr'){if(!confirm('Remover todas as luzes fixas desta cena?'))return;S.luzes=[];LUZ.sel=null;save();opts();draw();return}
},true);
/* o botão da cena escura usa o tratador do tabletop (data-o=night); aqui só deixamos passar */
document.addEventListener('input',e=>{
 const t=e.target;if(!t.dataset||!('lzi' in t.dataset)||!t.closest('#opt'))return;
 e.stopPropagation();aplica(t.dataset.lzi,t.value)
},true);
document.addEventListener('change',e=>{
 const t=e.target;if(!t.dataset||!('lzi' in t.dataset)||!t.closest('#opt'))return;
 e.stopPropagation();save();opts()
},true);
})();
