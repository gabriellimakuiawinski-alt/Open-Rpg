#!/usr/bin/env python3
"""Gera mesa.html a partir do mesa-paranormal-v10.html (original, local) + camada de nuvem."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
SRC = os.path.join(HERE, "original", "mesa-paranormal-v10.html")
NUV = os.path.join(HERE, "nuvem.js")
OUT = os.path.join(ROOT, "mesa.html")

L = open(SRC, encoding="utf-8").read().split("\n")
nuv = open(NUV, encoding="utf-8").read().rstrip("\n")

def line(n, sig):
    assert sig in L[n - 1], f"linha {n} não contém {sig!r}: {L[n-1][:80]!r}"

# ---- cortes por linha (arquivo original fixo) ----
line(107, "armazenamento de imagens"); line(113, "async function loadLib")
line(118, "if(!VIEW){if(!S.scenes)"); line(119, "S.dl=s0.dl??.92}")
line(293, "function adopt"); line(305, "$('fbk').onchange")
line(430, "(async()=>{try{await loadLib()}")
new = L[:106]
new += [nuv]                      # 107-113 -> nuvem
new += L[113:117]                 # 114-117
new += ["S.scenes=[];S.cur=null;S.tok=[];S.fg=[];S.maps=[];S.walls=[];S.nt=0;S.dl=.92;S.fl=[];S.pls=[];S.notes='';"]  # 118-119
new += L[119:292]                 # 120-292
new += L[305:429]                 # 306-429 (sem backup)
new += ["nuvemMain();"]           # 430
new += L[430:]
s = "\n".join(new)

def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, f"esperava {n}x, achei {c}x: {a[:90]!r}"
    s = s.replace(a, b)

# ---- cabeçalho: scripts do Supabase ----
rep('<input type="file" id="fob" multiple webkitdirectory hidden>\n<script>',
    '<input type="file" id="fob" multiple webkitdirectory hidden>\n<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.118.0/dist/umd/supabase.js"></script>\n<script src="comum.js?v=2"></script>\n<script>')
rep("</style></head>", """body.jog #tb hr{display:none}
body.jog [data-t=fog],body.jog [data-t=wall],body.jog [data-a=pv],body.jog #undo,body.jog #redo,body.jog #mpb,body.jog #mp,body.jog [data-a=m_maps],body.jog [data-a=m_ord],body.jog [data-a=m_nt],body.jog [data-a=m_obs],body.jog [data-a=m_vw],body.jog .gonly,body.adm #mpb,body.adm #mp,body.adm [data-a=m_nt],body.adm [data-a=m_obs],body.adm [data-a=m_vw]{display:none!important}
#espera{position:fixed;inset:0;display:none;align-items:center;justify-content:center;flex-direction:column;gap:12px;text-align:center;padding:24px;color:var(--m);font-size:18px;pointer-events:none;z-index:1}#espera button{pointer-events:auto;background:#343954}
#mx-pick{position:fixed;inset:0;z-index:100;background:#1d2133;display:flex;align-items:center;justify-content:center;padding:16px}
#mx-pick .box{background:#2a2e44;border-radius:24px;padding:24px;width:min(420px,100%);display:flex;flex-direction:column;gap:10px;box-shadow:0 8px 32px #0009;max-height:90vh;overflow:auto}
#mx-pick h2{margin:0 0 4px;font-weight:500;font-size:24px}#mx-pick button[data-m]{justify-content:space-between;width:100%;background:#343954;padding:14px 16px;font-size:16px}#mx-pick small{color:var(--m)}
</style></head>""")

# ---- ids reais (uuid) ----
rep("const uid=()=>Math.random().toString(36).slice(2,9),esc=",
    "const uid=()=>(crypto.randomUUID?crypto.randomUUID():'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g,c=>{const r=Math.random()*16|0;return(c=='x'?r:r&3|8).toString(16)})),esc=")

# ---- salvar / cena / preferências locais ----
rep("s.nt=S.nt;s.dl=S.dl}WV++;const j=snapJ();", "s.nt=S.nt;s.dl=S.dl;s.gs=S.gs;s.gm=S.gm;s.grid=S.grid;s.fcol=S.fcol;s.fa=S.fa}WV++;const j=snapJ();")
rep("PR=1;if(!pt)pt=setTimeout(persist,600);sync()};", "PR=1;if(!pt)pt=setTimeout(persist,600);cloudQ();sync()};")
rep("S.cur=id;S.tok=s.tok;S.fg=s.fg;S.maps=s.maps;S.walls=s.walls||(s.walls=[]);S.nt=s.nt||0;S.dl=s.dl??.92;WV++;sel=selM=null;fit();",
    "applyScene(s);sel=selM=null;try{if(GER)localStorage['mesa_cena_'+MESA.id]=id}catch(e){}fit();pedeFit();")
rep("const{tok,fg,maps,sc,mid,walls,nt,dl,lg,...r}=S;try{localStorage.mesa3=JSON.stringify(r)}",
    "const r={q:S.q,mp:S.mp};try{localStorage.mesa3=JSON.stringify(r)}")

# ---- desenho: barras de vida e alças só para quem pode editar ----
rep("if(!VIEW&&t.bar){bar(t.x,by,bw,t.hp/t.pv,'#e44');bar(t.x,by+7,bw,t.mn/t.mm,'#4af')}else if(VIEW&&t.sv)bar(t.x,by,bw,t.hp/t.pv,'#e44');",
    "if(!VIEW&&t.bar&&(GER||canEditTok(t))){bar(t.x,by,bw,t.hp/t.pv,'#e44');bar(t.x,by+7,bw,t.mn/t.mm,'#4af')}else if((VIEW||!GER)&&t.sv)bar(t.x,by,bw,t.hp/t.pv,'#e44');")
rep("if(!VIEW){const o=sel||selM;if(o){const r=RC(o),hs=HZ/v.z;", "if(!VIEW){const o=(sel&&!canEditTok(sel))?null:(sel||selM);if(o){const r=RC(o),hs=HZ/v.z;")
rep("if(!o||tool!='sel'||!tmOpen||(drag&&drag.k!='rs'&&drag.k!='pan')){", "if(!o||tool!='sel'||!tmOpen||(sel&&!canEditTok(sel))||(drag&&drag.k!='rs'&&drag.k!='pan')){")

# ---- toque no tablado: mover != editar ----
rep("if(sel){const q=rotH(sel);if(Math.hypot(p.x-q.x,p.y-q.y)<HZ/S.v.z){drag={k:'rot'};draw();return}}const o=sel||(selM&&!selM.l?selM:null);",
    "if(sel&&canEditTok(sel)){const q=rotH(sel);if(Math.hypot(p.x-q.x,p.y-q.y)<HZ/S.v.z){drag={k:'rot'};draw();return}}const o=sel?(canEditTok(sel)?sel:null):(selM&&GER&&!selM.l?selM:null);")
rep("tmOpen=!!(dbl&&sel===t);sel=t;selM=null;drag={k:'tok',dx:p.x-t.x,dy:p.y-t.y};if(!HINT){HINT=1;toast('Dois toques rápidos no token abrem as configurações dele.')}}",
    "tmOpen=!!(dbl&&sel===t&&canEditTok(t));sel=t;selM=null;if(canMove(t))drag={k:'tok',dx:p.x-t.x,dy:p.y-t.y};else{drag=null;toast(t.lk?'Token travado pelo mestre.':'O mestre travou o movimento dos jogadores.')}if(!HINT&&canEditTok(t)){HINT=1;toast('Dois toques rápidos no token abrem as configurações dele.')}}")
rep("else{const m=[...S.maps].reverse().find(m=>hit(mrect(m),p));if(m&&dbl)", "else{const m=GER?[...S.maps].reverse().find(m=>hit(mrect(m),p)):null;if(m&&dbl)")

rep("cv.onpointerdown=e=>{PT.set(e.pointerId,e);", "cv.onpointerdown=e=>{FITQ=false;PT.set(e.pointerId,e);")
rep("cv.onwheel=e=>{e.preventDefault();", "cv.onwheel=e=>{FITQ=false;e.preventDefault();")
# ---- teclado ----
rep("if(e.ctrlKey||e.metaKey){if(k=='z')e.shiftKey?redo():undo();", "if(e.ctrlKey||e.metaKey){if(!GER)return;if(k=='z')e.shiftKey?redo():undo();")
rep("else if(k=='delete'&&sel){S.tok=S.tok.filter(t=>t!=sel);", "else if(k=='delete'&&sel&&canDelTok(sel)){S.tok=S.tok.filter(t=>t!=sel);")
rep("function setTool(t){tool=t;cur=null;", "function setTool(t){if(!GER&&(t=='fog'||t=='wall'))return;tool=t;cur=null;")

# ---- painel do token ----
rep("function ui(){const sn=(scene(S.cur)||{}).n||'Cena';$('rmb').innerHTML=I('cube')+`<span>${esc(sn)}</span>`;",
    "function ui(){const sn=(scene(S.cur)||{}).n||'Cena';$('rmb').innerHTML=I('cube')+`<span>${esc(sn)}</span>`+(GER&&MESA&&S.cur&&S.cur!==MESA.cena_ativa?' <small class=m>(oculta)</small>':'');")
rep("if(!t){m.classList.add('hid');return}", "if(!t||!canEditTok(t)){m.classList.add('hid');return}")
rep("else body=R('hid','','Invisível na mesa')+", "else body=(GER?R('hid','','Invisível na mesa')+R('lk','','Travado para os jogadores')+fichaSel(t):'')+")
rep("<div class=q><button data-k=dup>⎘ Duplicar</button><button data-k=del>Excluir</button></div>`;",
    "<div class=q>${GER||MESA.jogadores_adicionam?'<button data-k=dup>⎘ Duplicar</button>':''}${canDelTok(t)?'<button data-k=del>Excluir</button>':''}</div>`;")
rep("const c={...sel,id:uid(),x:sel.x+S.gs,", "const c={...sel,id:uid(),cb:ME.id,pj:GER?sel.pj:null,lk:GER?sel.lk:0,hid:GER?sel.hid:0,x:sel.x+S.gs,")
rep("sel[k]=k=='n'?v:+v}save();draw()}", "sel[k]=k=='n'?v:k=='pj'?(v||null):+v}save();draw()}")

# ---- adicionar mapa / token ----
rep("function addMap(id,px,py){const first=", "function addMap(id,px,py){if(!GER)return;const first=")
rep("function addTok(id,px,py){const i=LIB.get(id),g=S.gs,v=S.v;", "function addTok(id,px,py){if(!GER&&!MESA.jogadores_adicionam)return toast('O mestre não permitiu adicionar tokens.');const i=LIB.get(id),g=S.gs,v=S.v;")
rep("const t={id:uid(),i:id,k:i.k,n:i.n,z:1,", "const t={id:uid(),cb:ME.id,i:id,k:i.k,n:i.n,z:1,")

# ---- biblioteca / dock ----
rep("return{id:s.id,n:s.n,url:im&&(im.th||im.url),sc:1}", "return{id:s.id,n:(s.id==MESA.cena_ativa?'':'')+s.n,url:im&&(im.th||im.url),sc:1}")
rep("filter(i=>i.k==k&&(q?i.n.toLowerCase().includes(q):(!c||i.fid==c))).sort(srt)}", "filter(i=>i.k==k&&(GER||i.by===ME.id)&&(q?i.n.toLowerCase().includes(q):(!c||i.fid==c))).sort(srt)}")
rep("const chips=(k,c)=>k=='scn'?'':", "const chips=(k,c)=>k=='scn'||!GER?'':")
rep("function act(a,inM){\nif(a=='add'){if(mk=='scn')sedit(null);else{fk=mk;$('fi').click()}}else if(a=='nscn')sedit(null)",
    "function act(a,inM){\nif(a=='ativar')return ativarCena(S.cur);if(a=='trocar'){localStorage.removeItem('mesa_atual');location.href=location.pathname;return}if(a=='sair'){MX.sair();return}\nif(a=='add'){if(mk=='scn')sedit(null);else{if(!GER&&!MESA.jogadores_adicionam)return toast('O mestre não permitiu enviar imagens.');fk=mk;$('fi').click()}}else if(a=='nscn')sedit(null)")

# ---- diálogos de edição ----
rep("(isF?'':`<label>Categoria <select id=e_k>${C.slice(1).map(([k,l])=>`<option value=${k} ${o.k==k?'selected':''}>${l}</option>`).join('')}</select></label><label>Pasta <select id=e_f></select></label>`)",
    "(isF?'':`${['chr','prop','mnt'].includes(o.k)?`<label>Categoria <select id=e_k>${[['chr','Personagens'],['prop','Props'],['mnt','Montarias']].map(([k,l])=>`<option value=${k} ${o.k==k?'selected':''}>${l}</option>`).join('')}</select></label>`:''}${GER?'<label>Pasta <select id=e_f></select></label>':''}`)")
rep("if(!isF)fopt(o.k,o.fid)}", "if(!isF&&GER)fopt(o.k,o.fid)}")
rep("$('ew').onchange=e=>{if(e.target.id=='e_k')fopt(e.target.value,null)};", "$('ew').onchange=e=>{if(e.target.id=='e_k'&&$('e_f'))fopt(e.target.value,null)};")
rep("o.k=$('e_k').value;o.fid=$('e_f').value||null;sv(o)", "if($('e_k'))o.k=$('e_k').value;if($('e_f'))o.fid=$('e_f').value||null;sv(o)")
rep("s=nw?{id:uid(),n:'',maps:[],tok:[],fg:[]}:scene(ED.id);", "s=nw?{id:uid(),n:'',maps:[],tok:[],fg:[],walls:[],nt:0,dl:.92,gs:50,gm:1.5,grid:true,fcol:'#000000',fa:.6}:scene(ED.id);")
rep("else if(S.cur==s.id){S.maps=s.maps;fit();save();draw()}}", "else if(S.cur==s.id){S.maps=s.maps;fit();save();draw()}else cloudQ()}")

# ---- ajustes ----
rep("<h5>Grade</h5><label>Pixels por quadrado", "<div class=gonly><h5>Grade</h5><label>Pixels por quadrado")
rep("Mostrar grade</label><h5>Desempenho</h5>", "Mostrar grade</label></div><h5>Desempenho</h5>")
rep("""<h5>Backup</h5><p class=m style="font-size:12px">Salva num arquivo tudo que está na mesa: cenas, mapas, tokens, névoa, paredes, pastas, playlists e as imagens e músicas importadas.</p><label><input type=checkbox id=bk_a checked> Incluir músicas e efeitos</label><div class=q2 style="margin-top:6px"><button data-a=bk_exp>Exportar backup</button><button data-a=bk_imp>Importar backup</button></div>""",
    """<h5>Nuvem</h5><p class=m style="font-size:12px">Tudo é salvo automaticamente na nuvem, na sua conta. Não precisa baixar nem importar backup.</p>""")
rep("if(a=='bk_exp')backupExport();else if(a=='bk_imp')$('fbk').click();\nelse if(a=='ob_link')", "if(a=='ob_link')")

# ---- importar imagens e áudios ----
rep("""$('fi').onchange=async e=>{const L=[...e.target.files];e.target.value='';for(const q of L){const r={id:uid(),k:fk,n:q.name.replace(/\\.[^.]+$/,''),fid:cf[fk],b:q};addLib(r);await sv(r)}mgrid2();if(noDB)toast(NODB)};""",
    """$('fi').onchange=async e=>{const L=[...e.target.files];e.target.value='';if(!GER&&(fk=='map'||!MESA.jogadores_adicionam))return toast('O mestre não permitiu enviar imagens.');for(const q of L){const b=await paraImagemOk(q);if(!b){toast('Formato não aceito: '+q.name);continue}const r={id:uid(),k:fk,n:q.name.replace(/\\.[^.]+$/,''),fid:cf[fk],b,_pend:1};addLib(r);enviar(r);mgrid2()}};""")
rep("addLib(r);ids.push(r.id);await sv(r)}", "r._pend=1;addLib(r);ids.push(r.id);enviar(r)}")


# ---- etapa 4: SAN no token, barras coloridas como na ficha, dados compartilhados ----
rep("bar(t.x,by,bw,t.hp/t.pv,'#e44');bar(t.x,by+7,bw,t.mn/t.mm,'#4af')}", "bar(t.x,by,bw,t.hp/t.pv,'#e44');bar(t.x,by+7,bw,t.mn/t.mm,'#b980ff');if(t.sm>0)bar(t.x,by+14,bw,t.sn/t.sm,'#44aaff')}")
rep("N=(a,b,l)=>`${l} <input type=number data-f=${a} value=${t[a]}> / <input type=number data-f=${b} value=${t[b]}>`", "N=(a,b,l)=>`${l} <input type=number data-f=${a} value=${t[a]??0}> / <input type=number data-f=${b} value=${t[b]??0}>`")
rep("${N('mn','mm','Mana')}<br>", "${N('mn','mm','PE')}<br>${N('sn','sm','SAN')}<br>")
rep("const logm=s=>$('log').innerHTML=s+'<br>'+$('log').innerHTML,", "const logm=(s,r)=>{$('log').innerHTML=s+'<br>'+$('log').innerHTML;if(!r&&window.DadoHook)try{DadoHook(s)}catch(e){}},")

# ---- desempenho: mipmaps das imagens, só desenha o que está na tela, tokens leves no envio ----
rep("let rq=0;function draw(){",
    "const MIPC=new WeakMap;/* cópias reduzidas (metade, um quarto...) das imagens grandes: desenhar uma imagem 5000px em 300px a cada quadro trava celular */\n"
    "function mip(im,w){w=Math.max(w,24);if(!(im.width>w*2)||im.width<256)return im;let L=MIPC.get(im);if(!L){L=[im];MIPC.set(im,L)}let i=0,novo=0;"
    "while(L[i].width>w*2){if(!L[i+1]){if(novo){draw();break}const p=L[i],c=document.createElement('canvas');c.width=Math.max(1,p.width>>1);c.height=Math.max(1,p.height>>1);const q=c.getContext('2d');q.imageSmoothingQuality='high';q.drawImage(p,0,0,c.width,c.height);L.push(c);novo=1}i++}return L[i]}\n"
    "let rq=0;function draw(){")
rep("S.maps.forEach(m=>{const r=mrect(m),im=(LIB.get(m.i)||{}).img;if(im&&im.complete&&im.width)x.drawImage(im,r.x,r.y,r.w,r.h);",
    "const VX0=-v.x/v.z,VY0=-v.y/v.z,VX1=(cw-v.x)/v.z,VY1=(ch-v.y)/v.z;\nS.maps.forEach(m=>{const r=mrect(m),im=(LIB.get(m.i)||{}).img;if(r.x>VX1||r.y>VY1||r.x+r.w<VX0||r.y+r.h<VY0)return;if(im&&im.complete&&im.width)x.drawImage(mip(im,r.w*v.z*Q),r.x,r.y,r.w,r.h);")
rep("cx=t.x+bw/2,cy=t.y+bw/2,by=t.y+bw+3;x.globalAlpha=",
    "cx=t.x+bw/2,cy=t.y+bw/2,by=t.y+bw+3;if(t.x+bw<VX0-3*g||t.x>VX1+3*g||t.y+bw+24<VY0||t.y-g>VY1)return;x.globalAlpha=")
rep("x.drawImage(m.img,-a/2,-h/2,a,h)", "x.drawImage(mip(m.img,a*v.z*Q),-a/2,-h/2,a,h)")
rep("const b=await paraImagemOk(q);if(!b){toast('Formato não aceito: '+q.name);continue}",
    "let b=await paraImagemOk(q);if(!b){toast('Formato não aceito: '+q.name);continue}if(fk!='map')b=await reduzTok(b);")
rep("async function paraImagemOk(f){",
    "/* token não precisa de mais que 512px: arquivo menor = carrega mais rápido e gasta menos memória */\n"
    "async function reduzTok(b){try{if(b.type=='image/gif')return b;const bm=await createImageBitmap(b),k=512/Math.max(bm.width,bm.height);if(!(k<1)){bm.close&&bm.close();return b}const c=document.createElement('canvas');c.width=Math.max(1,Math.round(bm.width*k));c.height=Math.max(1,Math.round(bm.height*k));const q=c.getContext('2d');q.imageSmoothingQuality='high';q.drawImage(bm,0,0,c.width,c.height);bm.close&&bm.close();return await new Promise(r=>c.toBlob(x=>r(x&&x.size<b.size?x:b),'image/webp',.9))}catch(e){return b}}\n"
    "async function paraImagemOk(f){")

# ---- desempenho: névoa e escuridão em cache com margem (arrastar o mapa não redesenha tudo a cada quadro) ----
rep("let rq=0;function draw(){",
    "const CAM={f:{},d:{}};let CAMT=0;\n"
    "function camada(L,c,sig,k,cw,ch,v,paint){const X0=-v.x/v.z,Y0=-v.y/v.z,VW=cw/v.z,VH=ch/v.z;"
    "if(sig!==L.sig||!(v.z/L.z<1.25&&L.z/v.z<1.25)||X0<L.X||Y0<L.Y||X0+VW>L.X+L.W||Y0+VH>L.Y+L.H){"
    "L.sig=sig;L.z=v.z;L.X=X0-VW*.25;L.Y=Y0-VH*.25;L.W=VW*1.5;L.H=VH*1.5;let s=v.z*k;const mx=4096/Math.max(L.W*s,L.H*s);if(mx<1)s*=mx;L.s=s;"
    "const a=Math.max(1,Math.round(L.W*s)),b=Math.max(1,Math.round(L.H*s));if(c.width!=a||c.height!=b){c.width=a;c.height=b}paint(s,-L.X*s,-L.Y*s)}"
    "else if(L.z!=v.z){clearTimeout(CAMT);CAMT=setTimeout(()=>{CAM.f.sig=CAM.d.sig=null;draw()},200)}}\n"
    "let rq=0;function draw(){")
rep("sz(cv,Q);const rf=sz(fcv,QF),rd=sz(dcv,QD);", "sz(cv,Q);")
rep("sig=[cw,ch,QD,v.x,v.y,v.z,WV,lg.map(", "sig=[QD,WV,lg.map(")
rep("if(rd||sig!=DK){DK=sig;drawDarkLayer(lg,v,QD)}x.save();x.setTransform(1,0,0,1,0,0);x.globalAlpha=pv?S.dl:Math.min(S.dl,.6);x.drawImage(dcv,0,0,cv.width,cv.height);x.restore()}",
    "if(sig!==DK){DK=sig;CAM.d.sig=null}camada(CAM.d,dcv,sig,QD,cw,ch,v,(s,ox,oy)=>drawDarkLayer(lg,{z:s,x:ox,y:oy},1));const L=CAM.d;x.save();x.setTransform(v.z*Q,0,0,v.z*Q,v.x*Q,v.y*Q);x.globalAlpha=pv?S.dl:Math.min(S.dl,.6);x.drawImage(dcv,L.X,L.Y,dcv.width/L.s,dcv.height/L.s);x.restore()}")
rep("const fkey=[cw,ch,QF,v.x,v.y,v.z,WV,S.fcol].join();if(rf||fkey!=FK){FK=fkey;f.setTransform(1,0,0,1,0,0);f.globalCompositeOperation='source-over';f.clearRect(0,0,fcv.width,fcv.height);f.setTransform(v.z*QF,0,0,v.z*QF,v.x*QF,v.y*QF);S.fg.forEach(",
    "const fkey=[QF,WV,S.fcol].join();if(fkey!==FK){FK=fkey;CAM.f.sig=null}if(S.fg.length)camada(CAM.f,fcv,fkey,QF,cw,ch,v,(sc,ox,oy)=>{f.setTransform(1,0,0,1,0,0);f.globalCompositeOperation='source-over';f.clearRect(0,0,fcv.width,fcv.height);f.setTransform(sc,0,0,sc,ox,oy);S.fg.forEach(")
rep("else f.fill(P)})}\nif(S.fg.length){x.save();x.setTransform(1,0,0,1,0,0);x.globalAlpha=pv?1:S.fa;x.drawImage(fcv,0,0,cv.width,cv.height);x.restore()}",
    "else f.fill(P)})});\nif(S.fg.length){const L=CAM.f;x.save();x.globalAlpha=pv?1:S.fa;if(Math.abs(v.z*Q/L.s-1)<1e-6){x.setTransform(1,0,0,1,0,0);x.drawImage(fcv,Math.round((L.X*v.z+v.x)*Q),Math.round((L.Y*v.z+v.y)*Q))}else{x.setTransform(v.z*Q,0,0,v.z*Q,v.x*Q,v.y*Q);x.drawImage(fcv,L.X,L.Y,fcv.width/L.s,fcv.height/L.s)}x.restore()}")

rep("S.q=COARSE||(navigator.hardwareConcurrency||4)<=4?'l':'n';", "S.q=COARSE||window.LEVE||(navigator.hardwareConcurrency||4)<=4?'l':'n';")

# ---- etapa 5: luz do token pelo inventário da ficha (campanha de Ordem Paranormal) ----
LB = """<div class=q><button data-k=lc class="${t.lo&&isCone(t)?'on':''}">Lanterna</button><button data-k=ll class="${t.lo&&!isCone(t)?'on':''}">Lampião</button></div>"""
LC = """Luz: raio <input type=number data-f=lz value=${t.lz||0} min=0 step=.5 style="width:58px">q ${isCone(t)?`cone <input type=number data-f=la value=${t.la>0&&t.la<360?t.la:60} min=15 max=180 style="width:58px">°`:''}<br>"""
rep(LB, "${luzBotoes(t)}")
rep(LC, "${luzCampos(t)}")
rep("function isCone(t){",
    "/* Ordem Paranormal: token ligado a ficha usa a melhor luz do inventário (o banco também garante isso) */\n"
    "let SISM;const luzAuto=t=>SISM=='op'&&!!t.pj&&PERS.has(t.pj),luzInvM=t=>window.SIS?SIS.luz({inv:(PERS.get(t.pj)||{}).inv||{items:[]}}):{c:0,l:0,cn:'',ln:''};\n"
    "function luzInv(t,modo){return Math.round((luzInvM(t)[modo]||0)/(S.gm||1.5)*2)/2}\n"
    "function luzBotoes(t){if(!luzAuto(t))return `" + LB + "`;const c=luzInv(t,'c'),l=luzInv(t,'l');\n"
    " return `<div class=q><button data-k=lc class=\"${t.lo&&isCone(t)?'on':''}\" ${c||(t.lo&&isCone(t))?'':'disabled title=\"Sem lanterna no inventário\"'}>Lanterna</button><button data-k=ll class=\"${t.lo&&!isCone(t)?'on':''}\" ${l||(t.lo&&!isCone(t))?'':'disabled title=\"Sem lampião no inventário\"'}>Lampião</button></div>`}\n"
    "function luzCampos(t){if(!luzAuto(t))return `" + LC + "`;const L=luzInvM(t),its=((PERS.get(t.pj)||{}).inv||{}).items||[],ver=GER||(PERS.get(t.pj)||{}).user_id===ME.id;\n"
    " return `<span class=m>Luz pelo inventário:</span> Lanterna ${L.c?esc(L.cn)+' ('+L.c+' m)':'nenhuma'} · Lampião ${L.l?esc(L.ln)+' ('+L.l+' m)':'nenhum'}<br>${t.lo&&isCone(t)?`cone <input type=number data-f=la value=${t.la>0&&t.la<360?t.la:60} min=15 max=180 style=\"width:58px\">°<br>`:''}${ver&&window.MesaFicha?MesaFicha.html(t):''}`}\n"
    "function isCone(t){")
rep("else if(k=='lc'||k=='ll'){const m=k=='lc';if(sel.lo&&isCone(sel)==m)sel.lo=0;else{sel.lo=1;",
    "else if(k=='lc'||k=='ll'){const m=k=='lc';if(sel.lo&&isCone(sel)==m)sel.lo=0;else if(luzAuto(sel)){const z=luzInv(sel,m?'c':'l');if(!z){toast(m?'Sem lanterna no inventário da ficha.':'Sem lampião no inventário da ficha.');return}sel.lo=1;sel.lm=m?'c':'l';sel.lz=z;if(m&&!(sel.la>0&&sel.la<360))sel.la=60}else{sel.lo=1;")
rep("if(!sel.lz)sel.lz=m?10:6}}else if(k=='rl'", "if(!sel.lz)sel.lz=m?10:6}}else if(k=='rl'")
FONTS='<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Caveat:wght@500;700&family=Hanken+Grotesk:wght@400;500;700&family=Special+Elite&display=swap" rel="stylesheet"><link rel="stylesheet" href="tema.css?v=9"><link rel="stylesheet" href="tema-mesa.css?v=9">'
s=s.replace("</head>",FONTS+"</head>",1)
PWA='<link rel="manifest" href="manifest.webmanifest"><link rel="icon" href="icones/icone-192.png"><link rel="apple-touch-icon" href="icones/apple-touch-icon.png"><meta name="mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-capable" content="yes"><script src="pwa.js" defer></script>'
s=s.replace("</head>",PWA+"</head>",1)
s=s.replace("</body>",'<script src="sistemas.js?v=4"></script><script src="mesa-fx.js?v=9"></script><script src="mesa-musica.js?v=9"></script><script src="mesa-dados.js?v=9"></script><script src="mesa-ficha.js?v=3"></script><script src="mesa-notas.js?v=10"></script><script src="mesa-exportar.js?v=9"></script></body>',1)
open(OUT, "w", encoding="utf-8").write(s)
print("mesa.html gerado:", len(s), "bytes")
