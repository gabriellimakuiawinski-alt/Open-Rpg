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
    '<input type="file" id="fob" multiple webkitdirectory hidden>\n<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>\n<script src="comum.js"></script>\n<script>')
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
rep("else body=R('hid','🙈','Invisível na mesa')+", "else body=(GER?R('hid','🙈','Invisível na mesa')+R('lk','🔒','Travado para os jogadores')+fichaSel(t):'')+")
rep("<div class=q><button data-k=dup>⎘ Duplicar</button><button data-k=del>🗑 Excluir</button></div>`;",
    "<div class=q>${GER||MESA.jogadores_adicionam?'<button data-k=dup>⎘ Duplicar</button>':''}${canDelTok(t)?'<button data-k=del>🗑 Excluir</button>':''}</div>`;")
rep("const c={...sel,id:uid(),x:sel.x+S.gs,", "const c={...sel,id:uid(),cb:ME.id,pj:GER?sel.pj:null,lk:GER?sel.lk:0,hid:GER?sel.hid:0,x:sel.x+S.gs,")
rep("sel[k]=k=='n'?v:+v}save();draw()}", "sel[k]=k=='n'?v:k=='pj'?(v||null):+v}save();draw()}")

# ---- adicionar mapa / token ----
rep("function addMap(id,px,py){const first=", "function addMap(id,px,py){if(!GER)return;const first=")
rep("function addTok(id,px,py){const i=LIB.get(id),g=S.gs,v=S.v;", "function addTok(id,px,py){if(!GER&&!MESA.jogadores_adicionam)return toast('O mestre não permitiu adicionar tokens.');const i=LIB.get(id),g=S.gs,v=S.v;")
rep("const t={id:uid(),i:id,k:i.k,n:i.n,z:1,", "const t={id:uid(),cb:ME.id,i:id,k:i.k,n:i.n,z:1,")

# ---- biblioteca / dock ----
rep("return{id:s.id,n:s.n,url:im&&(im.th||im.url),sc:1}", "return{id:s.id,n:(s.id==MESA.cena_ativa?'📢 ':'')+s.n,url:im&&(im.th||im.url),sc:1}")
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

FONTS='<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Caveat:wght@500;700&family=Hanken+Grotesk:wght@400;500;700&family=Special+Elite&display=swap" rel="stylesheet"><link rel="stylesheet" href="tema.css?v=8"><link rel="stylesheet" href="tema-mesa.css?v=8">'
s=s.replace("</head>",FONTS+"</head>",1)
s=s.replace("</body>",'<script src="mesa-fx.js?v=8"></script><script src="mesa-icones.js?v=8"></script><script src="mesa-musica.js?v=8"></script><script src="mesa-dados.js?v=8"></script><script src="mesa-notas.js?v=8"></script><script src="mesa-exportar.js?v=8"></script></body>',1)
open(OUT, "w", encoding="utf-8").write(s)
print("mesa.html gerado:", len(s), "bytes")
