/* Mapas de interior (etapa 16)
   O mestre marca um local num mapa e liga a ele outro mapa (o interior).
   Com o telhado ligado (t=1) o interior fica escondido; ao tirar o telhado (t=0) o mapa
   de dentro aparece no lugar marcado. Cada interior: {id, i (arquivo do mapa), x, y, w, h, t, p (1 = manter proporção)}.
   Fica em S.ints, é salvo na cena (cenas.interiores) e vai para os jogadores como o resto da cena.
   Enxerga as variáveis do tabletop (S, LIB, GER, VIEW, pv, tool, drag, hit, mip, save, draw, sync, ED, $, esc, uid, toast, opts). */
(function(){
const INT=window.INT={sel:null,cur:null,ld:0};
const list=()=>S.ints||(S.ints=[]);
const nome=o=>(LIB.get(o.i)||{}).n||'Interior';
const imgDe=o=>(LIB.get(o.i)||{}).img;
const snap=n=>{const q=(S.gs||50)/2;return Math.round(n/q)*q};
const sel=()=>{if(!INT.sel)return null;const L=list();if(L.includes(INT.sel))return INT.sel;INT.sel=L.find(q=>q.id==INT.sel.id)||null;return INT.sel};
const mapas=()=>[...LIB.values()].filter(i=>i.k=='map').sort((a,b)=>(a.n||'').localeCompare(b.n||''));

/* desenho do interior (chamado no render, logo depois dos mapas) */
INT.draw=function(x,v,Q,X0,Y0,X1,Y1){
 for(const o of list()){
  if(o.t)continue;
  if(o.x>X1||o.y>Y1||o.x+o.w<X0||o.y+o.h<Y0)continue;
  if(!LIB.has(o.i)&&!INT.ld){INT.ld=1;Promise.resolve(loadLib()).catch(()=>{}).then(()=>setTimeout(()=>{INT.ld=0},4000))}
  const im=imgDe(o);
  if(im&&im.complete&&im.width){
   let rx=o.x,ry=o.y,rw=o.w,rh=o.h;
   if(o.p){const k=Math.min(rw/im.width,rh/im.height),a=im.width*k,b=im.height*k;x.fillStyle='#14161f';x.fillRect(o.x,o.y,o.w,o.h);rx+=(rw-a)/2;ry+=(rh-b)/2;rw=a;rh=b}
   x.drawImage(mip(im,rw*v.z*Q),rx,ry,rw,rh)
  }else{x.fillStyle='#242941';x.fillRect(o.x,o.y,o.w,o.h)}
 }
};

/* marcas só para o mestre (nunca na prévia do jogador nem na janela do espectador) */
INT.marks=function(x,v){
 if(VIEW||!GER||pv)return;
 const L=list(),s=sel(),z=v.z;
 if(!L.length&&!INT.cur)return;
 x.save();x.lineCap='round';
 for(const o of L){
  const on=o===s&&tool=='int';
  x.strokeStyle=o.t?'#ffb347':'#6dd36d';x.globalAlpha=tool=='int'?1:.55;x.lineWidth=(on?3.5:2)/z;x.setLineDash([8/z,6/z]);x.strokeRect(o.x,o.y,o.w,o.h);x.setLineDash([]);
  const f=Math.max(11,Math.min(16,(S.gs||50)*.3*z))/z,t=nome(o)+(o.t?' · telhado':' · aberto');
  x.font=`bold ${f}px sans-serif`;x.textAlign='left';x.fillStyle='#000';x.fillText(t,o.x+5/z+1/z,o.y+f+3/z+1/z);x.fillStyle=o.t?'#ffb347':'#6dd36d';x.fillText(t,o.x+5/z,o.y+f+3/z);
  if(on){const h=14/z;x.fillStyle='#bb99ff';x.fillRect(o.x+o.w-h/2,o.y+o.h-h/2,h,h)}
 }
 if(INT.cur&&drag&&drag.k=='int'){const c=INT.cur;x.globalAlpha=1;x.strokeStyle='#bb99ff';x.lineWidth=2/z;x.setLineDash([8/z,6/z]);x.strokeRect(c.x,c.y,c.w,c.h)}
 x.restore()
};

/* ponteiro (ferramenta Interior) */
INT.down=function(p,dbl){
 const h=14/S.v.z,s=sel();
 INT.cur=null;
 if(s&&Math.abs(p.x-(s.x+s.w))<h&&Math.abs(p.y-(s.y+s.h))<h){drag={k:'int',m:'rs',o:s};draw();return}
 const o=[...list()].reverse().find(q=>hit(q,p));
 if(o){
  INT.sel=o;
  if(dbl&&o===s){alterna(o);return}
  drag={k:'int',m:'mv',o,dx:p.x-o.x,dy:p.y-o.y,sx:p.x,sy:p.y,moved:0};opts();draw();return
 }
 INT.sel=null;INT.cur={x:p.x,y:p.y,w:0,h:0};drag={k:'int',m:'new',a:p};opts();draw()
};
INT.move=function(p){
 const d=drag;if(!d||d.k!='int')return;
 if(d.m=='new'){const c=INT.cur;if(!c)return;c.x=Math.min(d.a.x,p.x);c.y=Math.min(d.a.y,p.y);c.w=Math.abs(p.x-d.a.x);c.h=Math.abs(p.y-d.a.y)}
 else if(d.m=='rs'){d.o.w=Math.max(S.gs/2,snap(p.x)-d.o.x);d.o.h=Math.max(S.gs/2,snap(p.y)-d.o.y);sync()}
 else if(d.m=='mv'){if(!d.moved&&Math.hypot(p.x-d.sx,p.y-d.sy)>6/S.v.z)d.moved=1;if(d.moved){d.o.x=snap(p.x-d.dx);d.o.y=snap(p.y-d.dy);sync()}}
};
INT.up=function(d,p){
 if(d.m=='new'){
  const c=INT.cur;INT.cur=null;
  if(c&&c.w>=S.gs*.5&&c.h>=S.gs*.5){const x=snap(c.x),y=snap(c.y);dialogo({x,y,w:Math.max(S.gs/2,snap(c.x+c.w)-x),h:Math.max(S.gs/2,snap(c.y+c.h)-y)})}
  else{opts();draw()}
  return
 }
 if(d.m=='mv'&&!d.moved){opts();draw();return}
 save();opts();draw()
};

/* ações */
function alterna(o){
 o.t=o.t?0:1;save();opts();draw();
 toast(o.t?'Telhado posto: o interior ficou escondido.':'Telhado tirado: o interior apareceu.')
}
function dialogo(st){
 ED={int:st};
 const ms=mapas();
 $('ew').innerHTML=`<h3>${st.id?'Trocar o mapa do interior':'Mapa do interior'}</h3><p class=m style="margin:0;font-size:13px">Escolha o mapa que aparece dentro do local marcado quando o telhado for tirado.</p><div style="max-height:42vh;overflow:auto">${ms.map(i=>`<label><span style="display:flex;align-items:center;gap:8px"><img src="${i.th||i.url||''}" style="width:44px;height:44px;object-fit:cover;border-radius:8px">${esc(i.n)}</span><input type=radio name=int_m value="${i.id}" ${st.i==i.id?'checked':''}></label>`).join('')||'<p class=m>Nenhum mapa importado. Importe na aba Mapas e volte aqui.</p>'}</div><label><input type=checkbox id=int_p ${st.p?'checked':''}> Manter a proporção do mapa (sem esticar)</label><div class=ra><span class=sp></span><button data-int=no>Cancelar</button><button class=add data-int=ok>Salvar</button></div>`;
 $('ed').classList.remove('hid')
}
function agir(a,id){
 const L=list(),s=sel();
 if(a=='no'){ED=null;$('ed').classList.add('hid');opts();draw();return}
 if(a=='ok'){
  const r=document.querySelector('#ew input[name=int_m]:checked'),st=ED&&ED.int;
  if(!st)return;if(!r)return toast('Escolha um mapa.');
  const prop=$('int_p')&&$('int_p').checked?1:0;
  if(st.id){const o=L.find(q=>q.id==st.id);if(o){o.i=r.value;o.p=prop}}
  else{const o={id:uid(),i:r.value,x:st.x,y:st.y,w:st.w,h:st.h,t:1,p:prop};L.push(o);INT.sel=o;toast('Interior marcado. Está com telhado: toque duas vezes nele para tirar.')}
  ED=null;$('ed').classList.add('hid');save();opts();draw();return
 }
 if(a=='sel'){INT.sel=L.find(q=>q.id==id)||null;opts();draw();return}
 if(a=='roof'&&s){alterna(s);return}
 if(a=='swap'&&s){dialogo({id:s.id,i:s.i,p:s.p});return}
 if(a=='del'&&s){if(!confirm('Remover este interior? O mapa continua na biblioteca.'))return;S.ints=L.filter(q=>q!==s);INT.sel=null;save();opts();draw();return}
 if(a=='off'||a=='on'){L.forEach(q=>q.t=a=='on'?1:0);save();opts();draw();toast(a=='on'?'Todos os telhados postos.':'Todos os telhados tirados.');return}
}
INT.opts=function(){
 const L=list(),s=sel(),B=(k,l,on,id)=>`<button data-int=${k} ${id?`data-iid="${id}"`:''} class="${on?'on':''}">${l}</button>`;
 return `<h5>Interiores</h5><p class=m style="font-size:12px">Arraste no mapa para marcar um local e escolher o mapa de dentro. Toque numa marca para selecionar (arraste para mover; o quadrado do canto muda o tamanho). Dois toques tiram ou põem o telhado.</p>`
  +(L.length?`<div class=g2 style="grid-template-columns:1fr">${L.map(o=>B('sel',esc(nome(o))+(o.t?' (telhado)':' (aberto)'),o===s,o.id)).join('')}</div>`:'<p class=m>Nenhum interior nesta cena.</p>')
  +(s?`<h5>Selecionado</h5><div class=g2 style="grid-template-columns:1fr">${B('roof',s.t?'Tirar o telhado':'Pôr o telhado',!s.t)}</div><div class=g2>${B('swap','Trocar mapa')}${B('del','Remover')}</div>`:'')
  +(L.length>1?`<h5>Todos</h5><div class=g2>${B('off','Tirar todos')}${B('on','Pôr todos')}</div>`:'')
};

document.addEventListener('click',e=>{
 const b=e.target.closest&&e.target.closest('[data-int]');
 if(!b||(!b.closest('#opt')&&!b.closest('#ew')))return;
 e.stopPropagation();agir(b.dataset.int,b.dataset.iid)
},true);
})();
