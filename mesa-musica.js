/* mesa-musica.js — música compartilhada: o mestre toca, os jogadores ouvem.
   Estado vai por Realtime (broadcast, sem banco); o acesso ao arquivo é liberado pelo banco
   só para a faixa que está tocando (mesas.musica_id). */
(function(){
if(typeof sb==='undefined'||typeof AU==='undefined')return;
const uuidOk=v=>/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(v||'');
const ls={get:k=>{try{return localStorage.getItem(k)}catch(e){return null}},set:(k,v)=>{try{localStorage.setItem(k,v)}catch(e){}}};
const esc=s=>String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
let pronto=false,ult=null;
const send=p=>{if(!pronto||!window.CHM)return;try{window.CHM.send({type:'broadcast',event:'musica',payload:p})}catch(e){}};

/* ======================= MESTRE ======================= */
let tx=ls.get('mesa_transmitir')!=='0',idPub=null,tm=0;
function estado(){const id=(typeof Q!=='undefined'&&Q[qi])||null,t=id&&LIB.get(id);
  return{id,n:t?t.n:'',playing:!AU.paused&&!AU.ended,pos:AU.currentTime||0,vol:1}}
async function publicar(){
  if(!tx||!MESA||!DONO)return;
  const e=estado();if(!e.id||!uuidOk(e.id))return;
  if(e.id!==idPub){ // libera o arquivo para os jogadores antes de avisar
    const{error}=await sb.from('mesas').update({musica_id:e.id}).eq('id',MESA.id);
    if(error){if(!publicar.av){publicar.av=1;toast('Os jogadores não vão ouvir: rode o SQL da música no Supabase ('+error.message+')')}return}
    idPub=e.id}
  send(e)}
function agenda(){clearTimeout(tm);tm=setTimeout(publicar,120)}
function mestre(){
  ['play','pause','seeked','ended','loadedmetadata'].forEach(ev=>AU.addEventListener(ev,agenda));
  setInterval(()=>{if(tx&&!AU.paused)publicar()},4000);
  // interruptor no painel de música
  const mp=document.getElementById('mp');
  if(mp){const l=document.createElement('label');l.className='mrow mtx';l.innerHTML='<input type="checkbox" id="mtx"> <span>Transmitir aos jogadores</span>';
    const alvo=document.getElementById('mpn');(alvo?alvo.after(l):mp.prepend(l));
    const c=l.querySelector('input');c.checked=tx;
    c.onchange=async()=>{tx=c.checked;ls.set('mesa_transmitir',tx?'1':'0');
      if(!tx){send({parar:1});idPub=null;await sb.from('mesas').update({musica_id:null}).eq('id',MESA.id)}else{idPub=null;publicar()}}}
}

/* ======================= JOGADOR ======================= */
const PA=new Audio();PA.preload='auto';let cur=null,urls=new Map,pill=null,bloq=false,vol=+(ls.get('mesa_vol_musica')??.8),mudo=ls.get('mesa_mudo')==='1';
PA.volume=mudo?0:vol;
function ui(){
  if(!pill){pill=document.createElement('div');pill.id='mx-musica';pill.className='hid';
    pill.innerHTML='<span class="eq"><i></i><i></i><i></i><i></i></span><span class="nm"></span><button class="mm" title="Silenciar"></button><input type="range" min="0" max="1" step="0.05" aria-label="Volume da música"><button class="tocar">Tocar</button>';
    document.body.append(pill);
    const r=pill.querySelector('input');r.value=vol;
    r.oninput=()=>{vol=+r.value;mudo=vol==0;PA.volume=vol;ls.set('mesa_vol_musica',vol);ls.set('mesa_mudo',mudo?'1':'0');ico()};
    pill.querySelector('.mm').onclick=()=>{mudo=!mudo;PA.volume=mudo?0:vol;ls.set('mesa_mudo',mudo?'1':'0');ico()};
    pill.querySelector('.tocar').onclick=()=>{bloq=false;PA.play().then(ui).catch(()=>{})};
    ico()}
  const tocando=!!cur&&!PA.paused;
  pill.classList.toggle('hid',!cur);pill.classList.toggle('on',tocando);pill.classList.toggle('bloq',bloq);
  pill.querySelector('.nm').textContent=cur?cur.n||'Música da mesa':''}
function ico(){const b=pill.querySelector('.mm');b.innerHTML=mudo?'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 10v4h4l6 4V6L7 10Z"/><path d="m17 9 5 6M22 9l-5 6"/></svg>':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 10v4h4l6 4V6L7 10Z"/><path d="M16 9a4 4 0 0 1 0 6M18.5 6.5a8 8 0 0 1 0 11"/></svg>'}
async function urlDe(id){
  const c=urls.get(id);if(c&&c.exp>Date.now())return c;
  const{data,error}=await sb.from('arquivos').select('id,nome,path').eq('id',id).maybeSingle();
  if(error||!data)throw new Error('sem acesso à faixa');
  const s=await sb.storage.from('mesa-arquivos').createSignedUrl(data.path,3600);
  if(s.error||!s.data)throw new Error('sem link');
  const o={url:s.data.signedUrl||s.data.signedURL,n:data.nome,exp:Date.now()+50*60*1000};urls.set(id,o);return o}
let seq=0;
async function rx(p){
  if(p&&p.pedir){if(DONO&&tx)publicar();return}
  if(!p||GER||(typeof VIEW!=='undefined'&&VIEW))return;
  if(p.parar){PA.pause();cur=null;ui();return}
  if(!p.id)return;
  const meu=++seq;
  try{
    if(!cur||cur.id!==p.id){
      const o=await urlDe(p.id);if(meu!==seq)return;
      cur={id:p.id,n:o.n||p.n};PA.src=o.url;
      await new Promise(ok=>{const f=()=>{PA.removeEventListener('loadedmetadata',f);ok()};PA.addEventListener('loadedmetadata',f);setTimeout(ok,4000)})}
    if(meu!==seq)return;
    if(p.playing){
      if(Math.abs(PA.currentTime-p.pos)>2.5)try{PA.currentTime=p.pos}catch(e){}
      if(PA.paused){try{await PA.play();bloq=false}catch(e){bloq=true}}
    }else{PA.pause();if(Math.abs(PA.currentTime-p.pos)>.5)try{PA.currentTime=p.pos}catch(e){}}
  }catch(e){console.warn('música',e.message)}
  ui()}
PA.addEventListener('pause',ui);PA.addEventListener('playing',()=>{bloq=false;ui()});

window.MusicaSync={rx,
  conectou(){pronto=true;if(DONO&&!mestre.ok){mestre.ok=1;mestre()}if(DONO)publicar();else if(!GER)send({pedir:1})}};
})();
