/* mesa-dados.js — rolagens compartilhadas: todos veem o que cada um rolou (o mestre pode rolar em segredo) */
(function(){
if(typeof sb==='undefined')return;
const esc=s=>String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
let nome=null;
async function meuNome(){
  if(nome)return nome;
  try{const{data}=await sb.from('profiles').select('nome').eq('id',ME.id).maybeSingle();nome=(data&&data.nome)||(ME.email||'').split('@')[0]||'Alguém'}catch(e){nome='Alguém'}
  return nome}
const secreto=()=>{const c=document.getElementById('dsec');return !!(c&&c.checked)};
window.DadoHook=async function(html){
  if(!window.CHM||secreto())return;
  try{window.CHM.send({type:'broadcast',event:'dado',payload:{n:await meuNome(),h:html}})}catch(e){}};
window.DadoRx=function(p){
  if(!p||!p.h||typeof logm!=='function')return;
  logm(`<span class="dn">${esc(p.n||'Alguém')}</span> ${p.h}`,1)};
// interruptor "rolagem secreta" (só quem gerencia a mesa)
const t=setInterval(()=>{
  if(typeof MESA==='undefined'||!MESA||typeof GER==='undefined')return;
  clearInterval(t);
  if(!GER)return;
  const dc=document.getElementById('dc'),log=document.getElementById('log');if(!dc||!log||document.getElementById('dsec'))return;
  const l=document.createElement('label');l.className='mrow dsec';l.innerHTML='<input type="checkbox" id="dsec"> <span>Rolagem secreta: só eu vejo</span>';
  log.before(l)},300);
})();
