/* ===================== NUVEM (Supabase) =====================
   Troca o armazenamento local (IndexedDB/localStorage) pela nuvem:
   biblioteca -> tabela "arquivos" + Storage; cenas/mapas/tokens -> tabelas;
   quem pode o quê é decidido pelo banco (RLS); aqui só escondemos o que não vale. */
let noDB=false;const NODB='';
const MX=window.Mesa,sb=MX&&MX.db,BUCKET='mesa-arquivos';
let ME=null,MESA=null,ROLE='jogador',GER=false,DONO=false,PERS=new Map,CLOUD=false,LIBOK=false;
const K2T={map:'mapa',chr:'chr',prop:'prop',mnt:'mnt',aud:'aud'},T2K={mapa:'map',chr:'chr',prop:'prop',mnt:'mnt',aud:'aud'};
const UUID=/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i,isU=v=>typeof v=='string'&&UUID.test(v);
const ss=o=>JSON.stringify(o,(k,v)=>v&&typeof v=='object'&&!Array.isArray(v)?Object.keys(v).sort().reduce((a,q)=>(a[q]=v[q],a),{}):v);
const r2n=v=>Math.round((+v||0)*100)/100,DUMMY={width:0,height:0,complete:false};
const LAST={t:new Map,m:new Map,s:new Map,f:new Map,p:new Map,n:null};
const canEditTok=t=>!!ME&&(GER||t.cb===ME.id||!!(t.pj&&(PERS.get(t.pj)||{}).user_id===ME.id)),
canDelTok=t=>!!ME&&(GER||t.cb===ME.id),
canMove=t=>GER||(!t.lk&&!!MESA&&!!MESA.jogadores_movem);
let FITQ=false;
const mapasProntos=()=>S.maps.length>0&&S.maps.every(m=>{const im=(LIB.get(m.i)||{}).img;return !!(im&&im.complete&&im.width)});
function tentaFit(){if(FITQ&&mapasProntos()){FITQ=false;fit();draw()}}
function pedeFit(){FITQ=S.maps.length>0;tentaFit()}
const cs=(t,bad)=>{const e=document.getElementById('cs');if(e){e.textContent=t;e.style.color=bad?'#ff8a8a':'#9aa0bd'}};
const nerr=(e,pre)=>toast((pre||'Erro')+': '+((e&&e.message)||e));

/* ---------- biblioteca (arquivos + Storage) ---------- */
const OKMIME=new Set(['image/png','image/jpeg','image/webp','image/gif','image/avif','audio/mpeg','audio/mp3','audio/mp4','audio/x-m4a','audio/aac','audio/ogg','audio/wav','audio/x-wav','audio/wave','audio/webm','audio/flac','audio/opus','video/mp4','application/ogg']);
const EXTM={'image/png':'png','image/jpeg':'jpg','image/webp':'webp','image/gif':'gif','image/avif':'avif','audio/mpeg':'mp3','audio/mp3':'mp3','audio/mp4':'m4a','audio/x-m4a':'m4a','audio/aac':'aac','audio/ogg':'ogg','application/ogg':'ogg','audio/wav':'wav','audio/x-wav':'wav','audio/wave':'wav','audio/webm':'webm','audio/flac':'flac','audio/opus':'opus','video/mp4':'mp4'};
function mimeDe(b,n){let t=b.type||'';if(!t){const e=((n||'').match(/\.([a-z0-9]+)$/i)||[])[1];t=({png:'image/png',jpg:'image/jpeg',jpeg:'image/jpeg',webp:'image/webp',gif:'image/gif',avif:'image/avif',mp3:'audio/mpeg',m4a:'audio/mp4',mp4:'video/mp4',ogg:'audio/ogg',wav:'audio/wav',opus:'audio/opus',webm:'audio/webm',flac:'audio/flac'})[(e||'').toLowerCase()]||''}return t}
async function paraImagemOk(f){const t=mimeDe(f,f.name||'');if(OKMIME.has(t))return f.type===t?f:new Blob([f],{type:t});
 try{const bm=await createImageBitmap(f),c=document.createElement('canvas');c.width=bm.width;c.height=bm.height;c.getContext('2d').drawImage(bm,0,0);return await new Promise(r=>c.toBlob(r,'image/webp',.92))}catch(e){return null}}
const arqRec=a=>({id:a.id,k:T2K[a.tipo]||'chr',n:a.nome,fid:a.pasta_id||null,fx:a.efeito?1:0,ky:a.atalho||'',path:a.path,mime:a.mime,by:a.criado_por,th:a.miniatura||undefined,_k0:T2K[a.tipo]||'chr'});
function lazyImg(r){if(r.k=='aud'||Object.getOwnPropertyDescriptor(r,'img'))return;let im=null;
 Object.defineProperty(r,'img',{configurable:true,enumerable:false,set(v){im=v},get(){
  if(!im&&r.url){im=new Image;im.crossOrigin='anonymous';im.onload=()=>{tentaFit();draw();dockQ();mkThumb(r)};im.onerror=()=>{if(im.crossOrigin){const u=im.src;im.crossOrigin=null;im.src=u}};im.src=r.url}
  return im||DUMMY}})}
async function signAll(rs){const need=rs.filter(r=>r.path&&!r.url);
 for(let i=0;i<need.length;i+=150){const ch=need.slice(i,i+150);try{const{data,error}=await sb.storage.from(BUCKET).createSignedUrls(ch.map(r=>r.path),86400);if(error||!data)continue;const mp=new Map(data.map(d=>[d.path,d.signedUrl]));ch.forEach(r=>{const u=mp.get(r.path);if(u)r.url=u})}catch(e){}}}
async function loadLib(){if(!MESA)return;const{data,error}=await sb.from('arquivos').select('*').eq('mesa_id',MESA.id);
 if(error){nerr(error,'Erro ao carregar a biblioteca');return}
 const ids=new Set(data.map(a=>a.id));LIB.forEach((v,k)=>{if(!ids.has(k)&&!v._pend)LIB.delete(k)});
 const novos=[];data.forEach(a=>{const ex=LIB.get(a.id);if(ex){if(!ex._pend){ex.n=a.nome;ex.fid=a.pasta_id||null;ex.fx=a.efeito?1:0;ex.ky=a.atalho||'';ex.k=T2K[a.tipo]||ex.k;ex._k0=ex.k}}else{const r=arqRec(a);LIB.set(r.id,r);novos.push(r)}});
 await signAll(novos);novos.forEach(lazyImg);LIBOK=true;draw();dockQ()}
const addLib=r=>{r.url=URL.createObjectURL(r.b);if(r.k!='aud'){r.img=new Image;r.img.onload=()=>{draw();dockQ();mkThumb(r)};r.img.src=r.url}r._k0=r.k;LIB.set(r.id,r)};
const imgReady=r=>new Promise(ok=>{const im=r.img;if(!im||(im.complete&&im.width))return ok();im.addEventListener('load',()=>ok());im.addEventListener('error',()=>ok());setTimeout(ok,15000)});
let UPQ=Promise.resolve(),UPN=0;
function enviar(r){UPN++;toast('Enviando '+UPN+' arquivo(s)…');UPQ=UPQ.then(()=>enviar1(r)).catch(e=>nerr(e,'Falha no envio')).then(()=>{UPN--;if(!UPN)toast('Envio concluído.')});return UPQ}
async function enviar1(r){
 const falha=m=>{toast(m);LIB.delete(r.id);try{URL.revokeObjectURL(r.url)}catch(e){}dockQ();if(typeof mgrid2=='function')mgrid2()};
 const t=mimeDe(r.b,r.b.name||r.n||'');
 if(!OKMIME.has(t))return falha('"'+r.n+'": formato não aceito.');
 if(r.b.size>52428800)return falha('"'+r.n+'" passa de 50 MB.');
 if(r.k!='aud'){await imgReady(r);mkThumb(r)}
 const path=MESA.id+'/'+r.id+'.'+(EXTM[t]||'bin');
 const row={id:r.id,mesa_id:MESA.id,tipo:K2T[r.k],nome:r.n||'',pasta_id:r.fid||null,path,mime:t,tamanho:r.b.size,efeito:!!r.fx,atalho:r.ky||'',criado_por:ME.id,miniatura:r.th||null};
 let a=await sb.from('arquivos').insert(row);
 if(a.error&&/miniatura/i.test(a.error.message)){delete row.miniatura;a=await sb.from('arquivos').insert(row)}
 if(a.error)return falha('Não consegui enviar "'+r.n+'": '+a.error.message);
 const u=await sb.storage.from(BUCKET).upload(path,r.b,{contentType:t,upsert:false});
 if(u.error){await sb.from('arquivos').delete().eq('id',r.id);return falha('Não consegui enviar "'+r.n+'": '+u.error.message)}
 r.path=path;r.by=ME.id;r._pend=0;r._k0=r.k;cloudQ();dockQ()}
const sv=async i=>{if(i._pend)return;await cloudFlush();const u={nome:i.n,pasta_id:i.fid||null,efeito:!!i.fx,atalho:i.ky||''};if(i._k0&&i.k!=i._k0)u.tipo=K2T[i.k];
 const{error}=await sb.from('arquivos').update(u).eq('id',i.id);if(error){nerr(error,'Não consegui salvar');if(u.tipo)i.k=i._k0}else i._k0=i.k};
const del=async id=>{const r=LIB.get(id);if(!r)return;const p=r.path;
 S.scenes.forEach(s=>{for(let j=s.maps.length;j--;)if(s.maps[j].i==id){LAST.m.delete(s.maps[j].id);s.maps.splice(j,1)}s.tok.forEach(t=>{if(t.i==id)t.i=null;if(t.di==id)t.di=null;if(t.alts)t.alts=t.alts.filter(q=>q!=id)})});
 try{if(p){const a=await sb.storage.from(BUCKET).remove([p]);if(a.error)throw a.error}const{error}=await sb.from('arquivos').delete().eq('id',id);if(error)throw error}catch(e){nerr(e,'Não consegui excluir')}
 WV++;draw();cloudQ()};
const all=async()=>[...LIB.values()];

/* ---------- conversões linha <-> objeto do app ---------- */
const TK=new Set(['id','n','k','i','di','alts','x','y','z','r','lk','hid','dn','rol','pj','cb']);
function rowTok(t,cena){const d={};for(const k in t)if(!TK.has(k)&&t[k]!==undefined)d[k]=t[k];
 return{id:t.id,cena_id:cena,nome:String(t.n==null?'':t.n),categoria:['chr','prop','mnt'].includes(t.k)?t.k:'chr',imagem_id:isU(t.i)?t.i:null,imagem_caido_id:isU(t.di)?t.di:null,alts:(t.alts||[]).filter(isU),x:r2n(t.x),y:r2n(t.y),tam:+t.z||1,rot:r2n(t.r),travado:!!t.lk,oculto:!!t.hid,caido:!!t.dn,personagem_id:isU(t.pj)?t.pj:null,rol:t.rol==null?null:Math.round(t.rol),dados:d,criado_por:t.cb===undefined?ME.id:t.cb}}
const tokFrom=r=>({...(r.dados||{}),id:r.id,n:r.nome,k:r.categoria,i:r.imagem_id,di:r.imagem_caido_id,alts:r.alts||[],x:+r.x,y:+r.y,z:+r.tam,r:+r.rot,lk:r.travado?1:0,hid:r.oculto?1:0,dn:r.caido?1:0,rol:r.rol==null?undefined:r.rol,pj:r.personagem_id,cb:r.criado_por});
const sceneRow=(s,i)=>({id:s.id,mesa_id:MESA.id,nome:s.n||'Cena',ordem:i,escuro:!!s.nt,escuridao:s.dl==null?.92:s.dl,grade_px:s.gs||50,grade_m:s.gm==null?1.5:s.gm,grade_visivel:s.grid!==false,nevoa:s.fg||[],nevoa_cor:s.fcol||'#000000',nevoa_opacidade:s.fa==null?.6:s.fa,paredes:s.walls||[]});
const sceneFrom=c=>({id:c.id,n:c.nome,maps:[],tok:[],fg:c.nevoa||[],walls:c.paredes||[],nt:c.escuro?1:0,dl:+c.escuridao,gs:+c.grade_px,gm:+c.grade_m,grid:c.grade_visivel!==false,fcol:c.nevoa_cor||'#000000',fa:+c.nevoa_opacidade,ver:c.versao||0});
const mapRow=(m,sc,i)=>({id:m.id,cena_id:sc,arquivo_id:m.i,x:r2n(m.x),y:r2n(m.y),escala:+m.s||1,travado:!!m.l,ordem:i}),
mapFrom=r=>({id:r.id,i:r.arquivo_id,x:+r.x,y:+r.y,s:+r.escala,l:r.travado?1:0});
const folderRow=f=>({id:f.id,mesa_id:MESA.id,tipo:K2T[f.k]||'chr',nome:f.n||''}),plRow=p=>({id:p.id,mesa_id:MESA.id,nome:p.n||'',faixas:(p.t||[]).filter(isU)});
function applyScene(s){S.cur=s.id;S.tok=s.tok;S.fg=s.fg;S.maps=s.maps;S.walls=s.walls||(s.walls=[]);S.nt=s.nt||0;S.dl=s.dl==null?.92:s.dl;S.gs=s.gs||50;S.gm=s.gm==null?1.5:s.gm;S.grid=s.grid!==false;S.fcol=s.fcol||'#000000';S.fa=s.fa==null?.6:s.fa;WV++}
const tkSnap=(t,sc)=>{const r=rowTok(t,sc);return{s:sc,k:ss(r),kb:ss({...r,x:0,y:0})}};
function snapLast(){LAST.s.clear();LAST.m.clear();LAST.t.clear();LAST.f.clear();LAST.p.clear();
 S.scenes.forEach((s,i)=>{LAST.s.set(s.id,ss(sceneRow(s,i)));s.maps.forEach((m,j)=>LAST.m.set(m.id,{s:s.id,k:ss(mapRow(m,s.id,j))}));s.tok.forEach(t=>LAST.t.set(t.id,tkSnap(t,s.id)))});
 S.fl.forEach(f=>LAST.f.set(f.id,ss(folderRow(f))));S.pls.forEach(p=>LAST.p.set(p.id,ss(plRow(p))));LAST.n=S.notes}

/* ---------- carregar dados da mesa ---------- */
async function carregarTudo(keep){
 if(MESA.campanha_id&&SISM===undefined){try{const q=await sb.from('campanhas').select('*').eq('id',MESA.campanha_id);SISM=(q.data&&q.data[0]&&q.data[0].sistema)||null}catch(e){SISM=null}}
 const[c,pa,pe]=await Promise.all([sb.from('cenas').select('*').eq('mesa_id',MESA.id).order('ordem').order('criado_em'),sb.from('pastas').select('*').eq('mesa_id',MESA.id),(MESA.campanha_id?sb.from('personagens').select('id,user_id,nome,npc,privada,dados').eq('campanha_id',MESA.campanha_id):Promise.resolve({data:[]}))]);
 if(c.error)throw c.error;
 PERS=new Map((pe.data||[]).map(p=>[p.id,{...p,inv:(p.dados||{}).inv}]));
 const ids=c.data.map(x=>x.id);let mp={data:[]},tk={data:[]};
 if(ids.length){[mp,tk]=await Promise.all([sb.from('mapas_cena').select('*').in('cena_id',ids).order('ordem'),sb.from('tokens').select('*').in('cena_id',ids).order('criado_em')]);if(mp.error)throw mp.error;if(tk.error)throw tk.error}
 const sc=c.data.map(sceneFrom);
 mp.data.forEach(r=>{const s=sc.find(x=>x.id==r.cena_id);if(s)s.maps.push(mapFrom(r))});
 tk.data.forEach(r=>{const s=sc.find(x=>x.id==r.cena_id);if(s)s.tok.push(tokFrom(r))});
 S.scenes=sc;S.fl=(pa.data||[]).map(p=>({id:p.id,n:p.nome,k:T2K[p.tipo]||'chr'}));
 if(DONO){const[pl,nt]=await Promise.all([sb.from('playlists').select('*').eq('mesa_id',MESA.id),sb.from('notas').select('texto').eq('mesa_id',MESA.id).maybeSingle()]);
  S.pls=(pl.data||[]).map(p=>({id:p.id,n:p.nome,t:p.faixas||[]}));S.notes=(nt.data&&nt.data.texto)||'';if(S.mp.pl&&!S.pls.some(p=>p.id==S.mp.pl))S.mp.pl=S.pls.length?S.pls[0].id:null}
 snapLast()}

/* ---------- salvar (só o que mudou) ---------- */
let cBusy=null,cAgain=0,cTimer=0;
const pendImg=t=>[t.i,t.di].some(i=>i&&LIB.get(i)&&LIB.get(i)._pend);
function diffs(){
 const rb=[],SL=(m,id,v)=>{const had=m.has(id),old=m.get(id);rb.push(()=>had?m.set(id,old):m.delete(id));m.set(id,v)},DL=(m,id)=>{if(!m.has(id))return;const old=m.get(id);rb.push(()=>m.set(id,old));m.delete(id)};
 const o={fo:[],sc:[],mp:[],tk:[],tu:[],mv:[],dm:[],dt:[],ds:[],df:[],pl:[],dp:[],nt:null,bad:0,rb};
 if(GER){S.fl.forEach(f=>{const r=folderRow(f),k=ss(r);if(LAST.f.get(f.id)!==k){o.fo.push(r);SL(LAST.f,f.id,k)}});
  LAST.f.forEach((v,id)=>{if(!S.fl.some(f=>f.id==id)){o.df.push(id);DL(LAST.f,id)}});
  const cur=new Set(S.scenes.map(s=>s.id));
  LAST.s.forEach((v,id)=>{if(!cur.has(id)){o.ds.push(id);DL(LAST.s,id)}});
  LAST.m.forEach((v,id)=>{if(!cur.has(v.s))DL(LAST.m,id)});LAST.t.forEach((v,id)=>{if(!cur.has(v.s))DL(LAST.t,id)})}
 const allM=new Set,allT=new Set;
 S.scenes.forEach((s,i)=>{
  if(GER){const r=sceneRow(s,i),k=ss(r);if(LAST.s.get(s.id)!==k){o.sc.push(r);SL(LAST.s,s.id,k)}
   s.maps.forEach((m,j)=>{allM.add(m.id);if(LIB.get(m.i)&&LIB.get(m.i)._pend)return;const mr=mapRow(m,s.id,j),k2=ss(mr),L=LAST.m.get(m.id);if(!L||L.k!==k2){o.mp.push(mr);SL(LAST.m,m.id,{s:s.id,k:k2})}})}
  s.tok.forEach(t=>{allT.add(t.id);if(pendImg(t))return;const L=LAST.t.get(t.id),sn=tkSnap(t,s.id);if(L&&L.k===sn.k)return;
   if(!L){o.tk.push(rowTok(t,s.id));SL(LAST.t,t.id,sn)}
   else if(GER||canEditTok(t)){o.tu.push(rowTok(t,s.id));SL(LAST.t,t.id,sn)}
   else if(L.kb===sn.kb){o.mv.push({id:t.id,x:r2n(t.x),y:r2n(t.y)});SL(LAST.t,t.id,sn)}
   else o.bad=1})});
 LAST.m.forEach((v,id)=>{if(!allM.has(id)&&GER){o.dm.push(id);DL(LAST.m,id)}});
 LAST.t.forEach((v,id)=>{if(!allT.has(id)){const sc=S.scenes.find(s=>s.id==v.s);if(sc){o.dt.push(id)}DL(LAST.t,id)}});
 if(DONO){S.pls.forEach(p=>{const r=plRow(p),k=ss(r);if(LAST.p.get(p.id)!==k){o.pl.push(r);SL(LAST.p,p.id,k)}});LAST.p.forEach((v,id)=>{if(!S.pls.some(p=>p.id==id)){o.dp.push(id);DL(LAST.p,id)}});if(LAST.n!==S.notes){o.nt=S.notes;{const old=LAST.n;rb.push(()=>{LAST.n=old});LAST.n=S.notes}}}
 return o}
const hasWork=o=>o.fo.length||o.sc.length||o.mp.length||o.tk.length||o.tu.length||o.mv.length||o.dm.length||o.dt.length||o.ds.length||o.df.length||o.pl.length||o.dp.length||o.nt!==null||o.bad;
async function runDiff(o){const E=[],ck=(r,l)=>{if(r&&r.error){const e=r.error;E.push({m:l+': '+(e.message||e),net:!e.code&&!r.status&&/fetch|network|timeout|load failed|conex/i.test(e.message||'')})}},ch=(a,n)=>{const r=[];for(let i=0;i<a.length;i+=n)r.push(a.slice(i,i+n));return r};
 if(o.fo.length)ck(await sb.from('pastas').upsert(o.fo),'pastas');
 if(o.sc.length)ck(await sb.from('cenas').upsert(o.sc),'cenas');
 for(const c of ch(o.mp,100))ck(await sb.from('mapas_cena').upsert(c),'mapas');
 for(const c of ch(o.tk,100))ck(await sb.from('tokens').upsert(c),'tokens');
 // token que já existe: UPDATE (o upsert exigiria ser o criador, e o dono da ficha / admin não é)
 for(const c of ch(o.tu,8))(await Promise.all(c.map(r=>{const{id,cena_id,criado_por,...rest}=r;return sb.from('tokens').update(rest).eq('id',id)}))).forEach(r=>ck(r,'tokens'));
 for(const m of o.mv)ck(await sb.rpc('mover_token',{p_id:m.id,p_x:m.x,p_y:m.y}),'mover');
 if(o.dm.length)ck(await sb.from('mapas_cena').delete().in('id',o.dm),'mapas');
 if(o.dt.length)ck(await sb.from('tokens').delete().in('id',o.dt),'tokens');
 if(o.ds.length)ck(await sb.from('cenas').delete().in('id',o.ds),'cenas');
 if(o.df.length)ck(await sb.from('pastas').delete().in('id',o.df),'pastas');
 if(o.pl.length)ck(await sb.from('playlists').upsert(o.pl),'playlists');
 if(o.dp.length)ck(await sb.from('playlists').delete().in('id',o.dp),'playlists');
 if(o.nt!==null)ck(await sb.from('notas').upsert({mesa_id:MESA.id,texto:o.nt}),'notas');
 return E}
function cloudSave(){if(!CLOUD||VIEW||!MESA)return Promise.resolve();if(cBusy){cAgain=1;return cBusy}
 cBusy=(async()=>{let falhou=0,o=null;try{do{cAgain=0;o=diffs();if(!hasWork(o))continue;cs('salvando…');const E=o.bad?[{m:'sem permissão',net:false}]:await runDiff(o);if(E.length){falhou=1;cAgain=0;if(E.every(e=>e.net)){o.rb.reverse().forEach(f=>f());cs('sem conexão',1);toast('Sem conexão com a nuvem. Tentarei de novo.');setTimeout(cloudQ,5000);break}toast('Não consegui salvar: '+E[0].m);cs('não salvo',1);await resync();break}}while(cAgain);if(!falhou)cs('salvo');await garanteAtiva()}catch(e){if(o&&o.rb)o.rb.reverse().forEach(f=>f());cs('sem conexão',1);toast('Sem conexão com a nuvem. Tentarei de novo.');setTimeout(cloudQ,5000)}finally{cBusy=null}})();return cBusy}
const cloudQ=()=>{if(!CLOUD)return;clearTimeout(cTimer);cTimer=setTimeout(cloudSave,350)},cloudFlush=()=>{clearTimeout(cTimer);return cloudSave()};
document.addEventListener('visibilitychange',()=>{if(document.hidden&&CLOUD)cloudFlush()});

/* ---------- cena ativa (o que os jogadores veem) ---------- */
async function ativarCena(id){if(!GER||!id)return;await cloudFlush();const{error}=await sb.rpc('ativar_cena',{p_cena:id});if(error)return nerr(error,'Não consegui mostrar a cena');
 MESA.cena_ativa=id;nuvemPanel();dockQ();ui();toast('Os jogadores agora veem esta cena.')}
async function garanteAtiva(){if(!GER||!S.scenes.length)return;if(!S.scenes.some(s=>s.id==MESA.cena_ativa)){MESA.cena_ativa=null;{const{error}=await sb.rpc('ativar_cena',{p_cena:S.scenes[0].id});if(!error){MESA.cena_ativa=S.scenes[0].id;nuvemPanel();dockQ();ui()}}}}
function esperaJogador(on){let e=document.getElementById('espera');if(!e){e=document.createElement('div');e.id='espera';e.textContent='Aguardando o mestre mostrar uma cena…';document.body.append(e)}e.style.display=on?'flex':'none'}
async function carregarAtiva(){await carregarTudo();await loadLib();const s=scene(MESA.cena_ativa);sel=selM=null;tmOpen=false;
 if(s){esperaJogador(0);applyScene(s);HS=[snapJ()];RD=[];FK=DK=null;autoFit=true;fit();pedeFit();ui();draw();dock();sync()}
 else{S.scenes=[];S.tok=[];S.fg=[];S.maps=[];S.walls=[];WV++;esperaJogador(1);ui();draw()}}
async function resync(){try{const keep=S.cur;await carregarTudo();await loadLib();const s=scene(keep)||scene(MESA.cena_ativa)||S.scenes[0];sel=selM=null;if(s){applyScene(s);HS=[snapJ()];RD=[];ui();dock();draw();sync()}else if(!GER)esperaJogador(1)}catch(e){cs('sem conexão',1)}}

/* ---------- tempo real ---------- */
const semFoco=()=>!(document.activeElement&&document.activeElement.closest&&document.activeElement.closest('#tm'));
function aplicaTok(row){const sc=scene(row.cena_id);if(!sc)return;const n=tokFrom(row),ex=sc.tok.find(t=>t.id==n.id),L=LAST.t.get(n.id);
 if(ex){if(L&&ss(rowTok(ex,sc.id))!==L.k)return;if(L&&L.k===ss(rowTok(n,sc.id)))return;if(drag&&drag.k=='tok'&&sel===ex)return;
  Object.keys(ex).forEach(k=>{if(!(k in n))delete ex[k]});Object.assign(ex,n)}else sc.tok.push(n);
 const t=ex||n;LAST.t.set(t.id,tkSnap(t,sc.id));
 if(sc.id==S.cur){if((t.i&&!LIB.has(t.i))||(t.di&&!LIB.has(t.di)))loadLib();WV++;sync();draw();if(sel===t&&semFoco())ui()}}
function rtTok(p){const e=p.eventType;if(e=='DELETE'){const id=p.old&&p.old.id;S.scenes.forEach(s=>{const i=s.tok.findIndex(t=>t.id==id);if(i>=0){if(sel===s.tok[i]){sel=null;ui()}s.tok.splice(i,1)}});LAST.t.delete(id);WV++;draw();sync();return}aplicaTok(p.new)}
function aplicaCena(c){const s=scene(c.id),n=sceneFrom(c);
 if(!s){if(GER){n.ord=0;S.scenes.push(n);LAST.s.set(n.id,ss(sceneRow(n,S.scenes.length-1)));dockQ()}else if(c.id==MESA.cena_ativa)carregarAtiva();return}
 const idx=S.scenes.indexOf(s),L=LAST.s.get(s.id),mine=ss(sceneRow(s,idx));
 if(!GER&&(c.versao||0)!==(s.ver||0)){s.ver=c.versao||0;refetchTok(s)}
 if(L&&mine!==L)return;const nr=ss(sceneRow({...n,tok:[],maps:[]},idx));if(L===nr)return;
 s.n=n.n;s.nt=n.nt;s.dl=n.dl;s.gs=n.gs;s.gm=n.gm;s.grid=n.grid;s.fcol=n.fcol;s.fa=n.fa;s.fg=n.fg;s.walls=n.walls;LAST.s.set(s.id,ss(sceneRow(s,idx)));
 if(s.id==S.cur){applyScene(s);FK=DK=null;ui();dockQ();draw();sync()}else dockQ()}
async function refetchTok(s){const{data,error}=await sb.from('tokens').select('*').eq('cena_id',s.id).order('criado_em');if(error)return;const ids=new Set(data.map(r=>r.id));
 for(let i=s.tok.length;i--;)if(!ids.has(s.tok[i].id)){if(sel===s.tok[i]){sel=null;ui()}LAST.t.delete(s.tok[i].id);s.tok.splice(i,1)}
 data.forEach(aplicaTok);if(!LIBOK||data.some(r=>(r.imagem_id&&!LIB.has(r.imagem_id))))await loadLib();WV++;draw();sync()}
function rtCena(p){const e=p.eventType;if(e=='DELETE'){const id=p.old&&p.old.id,i=S.scenes.findIndex(s=>s.id==id);if(i<0)return;const was=S.cur==id;S.scenes.splice(i,1);LAST.s.delete(id);if(was){if(S.scenes.length)loadScene(S.scenes[0].id);else carregarAtiva()}dockQ();return}aplicaCena(p.new)}
function rtMapa(p){if(p.eventType=='DELETE'){const id=p.old&&p.old.id;S.scenes.forEach(s=>{const i=s.maps.findIndex(m=>m.id==id);if(i>=0){if(selM===s.maps[i])selM=null;s.maps.splice(i,1)}});LAST.m.delete(id);WV++;draw();dockQ();return}
 const r=p.new,s=scene(r.cena_id);if(!s)return;const n=mapFrom(r),ex=s.maps.find(m=>m.id==n.id),L=LAST.m.get(n.id),k=ss(mapRow(n,s.id,r.ordem||0));
 if(ex){if(L&&ss(mapRow(ex,s.id,r.ordem||0))!==L.k)return;if(L&&L.k===k)return;Object.assign(ex,n)}else s.maps.push(n);
 LAST.m.set(n.id,{s:s.id,k});if(!LIB.has(n.i))loadLib();WV++;draw();dockQ()}
function rtMesa(p){const n=p.new,antes=MESA.cena_ativa,mov=MESA.jogadores_movem,add=MESA.jogadores_adicionam;Object.assign(MESA,n);
 if(!GER&&n.cena_ativa!==antes)carregarAtiva();
 if(!GER&&n.jogadores_movem!==mov)toast(n.jogadores_movem?'O mestre liberou o movimento.':'O mestre travou o movimento dos jogadores.');
 if(!GER&&n.jogadores_adicionam!==add)toast(n.jogadores_adicionam?'Agora você pode enviar imagens.':'O mestre bloqueou o envio de imagens.');
 nuvemPanel();dockQ();ui()}
/* ficha mudou (inventário): atualiza a luz disponível no menu do token */
function rtPers(p){const r=p.new;if(!r||!r.id)return;const o=PERS.get(r.id);if(!o)return;if(r.dados){o.dados=r.dados;if(r.dados.inv)o.inv=r.dados.inv}if(r.nome!==undefined)o.nome=r.nome;if(sel&&sel.pj==r.id&&semFoco())ui()}
function rtMemb(p){const r=p.new||p.old;if(!r||r.user_id!==ME.id)return;
 if(p.eventType=='DELETE'){alert('Você não faz mais parte desta mesa.');localStorage.removeItem('mesa_atual');location.href='ficha.html';return}
 if(p.new&&p.new.papel!==ROLE){toast('Seu papel mudou para '+p.new.papel+'. Recarregando…');setTimeout(()=>location.reload(),900)}}
async function rtArq(p){if(p.eventType=='DELETE'){LIB.delete(p.old.id);dockQ();draw();return}const a=p.new,ex=LIB.get(a.id);
 if(ex){if(!ex._pend){ex.n=a.nome;ex.fid=a.pasta_id||null;ex.fx=a.efeito?1:0;ex.ky=a.atalho||'';ex.k=T2K[a.tipo]||ex.k;ex._k0=ex.k;if(a.miniatura&&!ex.th)ex.th=a.miniatura}dockQ();return}
 const r=arqRec(a);await signAll([r]);lazyImg(r);LIB.set(r.id,r);dockQ()}
function ouvir(){if(!sb.channel)return;const T=(table,extra)=>({event:'*',schema:'public',table,...(extra||{})});
 (window.CHM=sb.channel('mesa:'+MESA.id)).on('broadcast',{event:'musica'},p=>{try{window.MusicaSync&&MusicaSync.rx(p.payload)}catch(e){}}).on('broadcast',{event:'dado'},p=>{try{window.DadoRx&&DadoRx(p.payload)}catch(e){}}).on('postgres_changes',T('tokens'),rtTok).on('postgres_changes',T('cenas',{filter:'mesa_id=eq.'+MESA.id}),rtCena).on('postgres_changes',T('mapas_cena'),rtMapa)
 .on('postgres_changes',{event:'UPDATE',schema:'public',table:'mesas',filter:'id=eq.'+MESA.id},rtMesa).on('postgres_changes',T('membros',{filter:'mesa_id=eq.'+MESA.id}),rtMemb)
 .on('postgres_changes',T('arquivos',{filter:'mesa_id=eq.'+MESA.id}),rtArq);if(MESA.campanha_id)window.CHM.on('postgres_changes',{event:'UPDATE',schema:'public',table:'personagens',filter:'campanha_id=eq.'+MESA.campanha_id},rtPers);window.CHM.subscribe(st=>{if(st=='SUBSCRIBED'){try{window.MusicaSync&&MusicaSync.conectou()}catch(e){}if(ouvir.ok)resync();ouvir.ok=1}else if(st=='CHANNEL_ERROR'||st=='TIMED_OUT')cs('tempo real caiu',1)})}

/* ---------- painel da sala e escolha da mesa ---------- */
function nuvemPanel(){const el=document.getElementById('pl');if(!el||!MESA)return;const a=scene(MESA.cena_ativa),pap={mestre:'GM',admin:'ADM',jogador:'JOG'}[ROLE];
 const r=[`<div class="pr"><span class="dot"></span><span>${esc(MESA.nome)}</span><span class="sp"></span><b class="gm">${pap}</b></div>`];
 if(GER){r.push(`<div class="pr"><span class="m">Jogadores veem:</span><b>${esc(a?a.n:'—')}</b></div><div class="pr"><button data-a="ativar">Mostrar esta cena aos jogadores</button></div>`)}
 if(DONO){r.push(`<label class="pr"><input type="checkbox" data-cfg="jogadores_movem" ${MESA.jogadores_movem?'checked':''}> Jogadores movem tokens</label><label class="pr"><input type="checkbox" data-cfg="jogadores_adicionam" ${MESA.jogadores_adicionam?'checked':''}> Jogadores enviam imagens</label><div class="pr"><span>Espectador</span><span class="sp"></span><button data-a="m_vw">Abrir</button></div>`)}
 if(DONO&&!MESA.campanha_id)r.push(`<div class="pr"><span class="m">Código da mesa</span><span class="sp"></span><b style="letter-spacing:.12em;color:#bb99ff">${esc(MESA.codigo)}</b></div>`);
 r.push(`<div class="pr"><a href="index.html" style="color:#bb99ff;text-decoration:none">Início</a></div>${MESA.campanha_id?`<div class="pr"><a href="ficha.html" style="color:#bb99ff;text-decoration:none">Fichas</a></div>`:''}<div class="pr"><button data-a="sair">Sair da conta</button></div>`);el.innerHTML=r.join('')}
document.addEventListener('change',async e=>{const c=e.target&&e.target.dataset&&e.target.dataset.cfg;if(!c||!DONO)return;const v=e.target.checked,{data,error}=await sb.from('mesas').update({[c]:v}).eq('id',MESA.id).select('id');
 if(error||!data||!data.length){e.target.checked=!v;return nerr(error||'sem permissão','Não consegui mudar')}MESA[c]=v;toast('Opção salva.')});
function escolherMesa(ms,mb){return new Promise(ok=>{const o=document.createElement('div');o.id='mx-pick';
 o.innerHTML=`<div class="box"><h2>Escolha a mesa</h2>${ms.length?ms.map(m=>`<button data-m="${m.id}"><b>${esc(m.nome)}</b><small>${({mestre:'Mestre',admin:'Admin',jogador:'Jogador'})[(mb.find(x=>x.mesa_id==m.id)||{}).papel]||''}</small></button>`).join(''):'<p class="m">Você ainda não está em nenhuma mesa.</p>'}<p class="m" style="margin:10px 0 0"><a href="index.html" style="color:#bb99ff">Ir para o início</a> (lá você cria uma mesa ou entra com um código).</p><p class="m"><button data-x="1">Sair da conta</button></p></div>`;
 o.onclick=e=>{const b=e.target.closest('[data-m]');if(b){o.remove();ok(ms.find(m=>m.id==b.dataset.m)||null)}else if(e.target.closest('[data-x]'))MX.sair()};document.body.append(o)})}
function nuvemRole(){document.body.classList.add(ROLE=='mestre'?'mst':ROLE=='admin'?'adm':'jog');
 if(!GER){C.splice(0,2);dk=mk='chr';pv=true}
 const rm=document.getElementById('rm');if(rm&&!document.getElementById('cs')){const s=document.createElement('div');s.id='cs';s.className='m';s.style.cssText='font-size:11px;padding:0 10px 4px';rm.insertBefore(s,document.getElementById('pl'))}cs('carregando…')}
const ehMon=p=>!!(p&&p.dados&&p.dados.op&&p.dados.op.classe=='criatura');
const fichaSel=t=>{if(!MESA.campanha_id)return `<p class="m" style="margin:6px 0">Mesa sem campanha: não tem fichas.</p>`;
 const L=[...PERS.values()],op=p=>`<option value="${p.id}" ${t.pj==p.id?'selected':''}>${esc(p.nome||'Sem nome')}</option>`,g=(r,a)=>a.length?`<optgroup label="${r}">${a.map(op).join('')}</optgroup>`:'';
 return `<label class="m" style="display:block;margin:6px 0">Ficha vinculada <select data-f="pj" style="max-width:100%"><option value="">(nenhuma)</option>${g('Personagens',L.filter(p=>!p.npc&&!ehMon(p)))}${g('NPCs',L.filter(p=>p.npc&&!ehMon(p)))}${g('Monstros',L.filter(ehMon))}</select></label>`};

/* ---------- início ---------- */
async function nuvemMain(){
 const falta=m=>{document.body.insertAdjacentHTML('beforeend','<div id="espera" style="display:flex">'+m+'</div>')};
 if(!sb)return falta('Não consegui carregar o Supabase. Confira a internet e recarregue.');
 try{
  ME=await MX.exigirLogin();if(!ME)return;
  const[mb,ms]=await Promise.all([sb.from('membros').select('mesa_id,papel').eq('user_id',ME.id),sb.from('mesas').select('*')]);
  if(mb.error)throw mb.error;if(ms.error)throw ms.error;
  const q=new URLSearchParams(location.search).get('mesa')||localStorage.mesa_atual;let m=ms.data.find(x=>x.id==q);
  if(!m&&ms.data.length==1)m=ms.data[0];
  if(!m){if(VIEW)return falta('Abra primeiro o tabletop e escolha a mesa.');location.replace('index.html');return}
  localStorage.mesa_atual=m.id;MESA=m;ROLE=(mb.data.find(x=>x.mesa_id==m.id)||{}).papel||'jogador';GER=ROLE!='jogador';DONO=ROLE=='mestre';
  if(VIEW){await loadLib();CLOUD=false;try{recv(JSON.parse(localStorage.mesa3s).s)}catch(e){}bc.postMessage({hello:1});opts();ui();dock();upd();draw();mpr();return}
  nuvemRole();sb.rpc('marcar_acesso_mesa',{p_mesa:m.id}).then(()=>{},()=>{});
  await Promise.all([carregarTudo(),loadLib()]);
  if(GER&&!S.scenes.length){const s={id:uid(),n:'Cena 1',maps:[],tok:[],fg:[],walls:[],nt:0,dl:.92,gs:50,gm:1.5,grid:true,fcol:'#000000',fa:.6};S.scenes.push(s);CLOUD=true;await cloudFlush();CLOUD=false}
  const alvo=scene(GER?(localStorage['mesa_cena_'+m.id]||MESA.cena_ativa):MESA.cena_ativa)||(GER?S.scenes[0]:null);
  if(alvo){applyScene(alvo);HS=[snapJ()];if(!S.maps.length&&GER)dkx=true;if(S.maps.length){fit();pedeFit()}}else{esperaJogador(1)}
  CLOUD=true;ouvir();nuvemPanel();if(DONO)obRestore();opts();ui();dock();upd();draw();mpr();cs('salvo');await garanteAtiva();
 }catch(e){console.error(e);falta('Erro ao abrir a mesa: '+esc((e&&e.message)||e)+'<br><button onclick="location.reload()">Tentar de novo</button>')}}
