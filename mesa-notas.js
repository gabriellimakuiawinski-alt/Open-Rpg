/* mesa-notas.js — "Meu caderno": notas privadas do jogador dentro da mesa (nem o mestre lê) */
(function(){
if(typeof sb==='undefined')return;
const esc=s=>String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
let ov=null,ta=null,st=null,tm=0,carregado=false,sujo=false;
const IC='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 4h11l3 3v13H5Z"/><path d="M9 10h6M9 14h6M9 18h3"/></svg>';
async function carrega(){
  const{data,error}=await sb.from('notas_jogador').select('texto').eq('mesa_id',MESA.id).eq('user_id',ME.id).maybeSingle();
  if(error){st.textContent='Rode o SQL da etapa 4 no Supabase para usar o caderno ('+error.message+')';return false}
  ta.value=(data&&data.texto)||'';carregado=true;st.textContent='';return true}
async function salva(){
  if(!carregado||!sujo)return;sujo=false;st.textContent='salvando…';
  const{error}=await sb.from('notas_jogador').upsert({mesa_id:MESA.id,user_id:ME.id,texto:ta.value,atualizado_em:new Date().toISOString()},{onConflict:'mesa_id,user_id'});
  st.textContent=error?'não salvou: '+error.message:'salvo'}
function abre(){
  if(!ov){
    ov=document.createElement('div');ov.id='mx-notas';ov.className='hid';
    ov.innerHTML='<div class="folha-n" role="dialog" aria-label="Meu caderno"><div class="cab-n"><b>Meu caderno</b><small>só você lê isto</small><span class="sp"></span><button class="fx" title="Fechar" data-fecha>✕</button></div><textarea placeholder="Pistas, nomes, suspeitas, o que o mestre disse…" spellcheck="false"></textarea><div class="rod-n"><span class="st"></span></div></div>';
    document.body.append(ov);ta=ov.querySelector('textarea');st=ov.querySelector('.st');
    ov.addEventListener('click',e=>{if(e.target===ov||e.target.closest('[data-fecha]'))fecha()});
    ta.addEventListener('input',()=>{sujo=true;st.textContent='…';clearTimeout(tm);tm=setTimeout(salva,900)});
    addEventListener('beforeunload',()=>{if(sujo)salva()});
    addEventListener('keydown',e=>{if(e.key=='Escape'&&!ov.classList.contains('hid'))fecha()})}
  ov.classList.remove('hid');setTimeout(()=>ta.focus(),60);
  if(!carregado)carrega()}
function fecha(){clearTimeout(tm);salva();ov.classList.add('hid')}
const t=setInterval(()=>{
  if(typeof MESA==='undefined'||!MESA||typeof DONO==='undefined'||!ME)return;
  clearInterval(t);
  if(DONO)return;
  const mm=document.getElementById('mm');if(!mm||mm.querySelector('[data-mx-notas]'))return;
  const b=document.createElement('button');b.setAttribute('data-mx-notas','1');b.innerHTML=IC+' Meu caderno';
  b.onclick=()=>{mm.classList.add('hid');abre()};
  mm.prepend(b)},300);
})();
