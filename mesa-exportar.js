/* mesa-exportar.js — "Exportar mesa": baixa as cenas, tokens e a lista de arquivos (só o mestre) */
(function(){
if(typeof sb==='undefined')return;
function baixar(nome,obj){const u=URL.createObjectURL(new Blob([JSON.stringify(obj,null,2)],{type:'application/json'})),l=document.createElement('a');l.href=u;l.download=nome.replace(/[^\w\-]+/g,'_')+'.json';document.body.append(l);l.click();l.remove();setTimeout(()=>URL.revokeObjectURL(u),5000)}
async function exporta(){
  toast('Preparando o arquivo…');
  try{
    const m=MESA.id,qs=t=>sb.from(t).select('*').eq('mesa_id',m);
    const[ce,ar,pa,pl,nt]=await Promise.all([qs('cenas'),qs('arquivos'),qs('pastas'),qs('playlists'),sb.from('notas').select('texto').eq('mesa_id',m).maybeSingle()]);
    for(const r of[ce,ar,pa,pl])if(r.error)throw r.error;
    const ids=ce.data.map(c=>c.id);
    const[tk,mp]=await Promise.all([ids.length?sb.from('tokens').select('*').in('cena_id',ids):{data:[]},ids.length?sb.from('mapas_cena').select('*').in('cena_id',ids):{data:[]}]);
    if(tk.error)throw tk.error;if(mp.error)throw mp.error;
    baixar('mesa_'+MESA.nome+'_'+new Date().toISOString().slice(0,10),{formato:'open-rpg',versao:1,tipo:'mesa',exportado_em:new Date().toISOString(),
      mesa:{nome:MESA.nome},cenas:ce.data.map(c=>({...c,tokens:tk.data.filter(t=>t.cena_id==c.id),mapas:mp.data.filter(t=>t.cena_id==c.id)})),
      pastas:pa.data,playlists:pl.data,arquivos:ar.data.map(({miniatura,...r})=>r),notas:(nt.data&&nt.data.texto)||'',
      aviso:'Os arquivos (mapas, imagens, músicas) não vão dentro deste arquivo: só a lista deles.'});
    toast('Mesa exportada.')
  }catch(e){toast('Não consegui exportar: '+(e.message||e))}}
const t=setInterval(()=>{
  if(typeof MESA==='undefined'||!MESA||typeof DONO==='undefined')return;
  clearInterval(t);if(!DONO)return;
  const mm=document.getElementById('mm');if(!mm||mm.querySelector('[data-mx-exp]'))return;
  const b=document.createElement('button');b.setAttribute('data-mx-exp','1');
  b.innerHTML='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12M7 10l5 5 5-5M5 20h14"/></svg> Exportar mesa';
  b.onclick=()=>{mm.classList.add('hid');exporta()};
  const alvo=mm.querySelector('[data-a=m_vw]');alvo?alvo.before(b):mm.append(b)},300);
})();
