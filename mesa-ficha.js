/* mesa-ficha.js — ficha e inventário dentro do tabletop (campanha Ordem Paranormal).
   Token ligado a uma ficha: o dono e o mestre rolam perícias, atacam, equipam e usam itens pelo menu do token.
   Tudo usa os mesmos números e regras de sistemas.js (SIS), então bate com a ficha. */
(function(){
if(typeof sb==='undefined'||!window.SIS)return;
const S=window.SIS,n0=S.n0,esc=s=>String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const sinal=v=>v>0?'+'+v:String(v);
const pOf=t=>{try{return t&&t.pj&&PERS.get(t.pj)}catch(e){return null}};
const pode=p=>!!p&&p.dados&&(GER||p.user_id===ME.id);
const fDe=p=>{try{return S.prepararOP(JSON.parse(JSON.stringify(p.dados)))}catch(e){return null}};
const bonusPer=(f,D,s)=>n0(s.t)+n0(s.o)+n0(D.per[s.n])+(['Fortitude','Reflexos','Vontade'].includes(s.n)?D.res:0);
const av=(f,id)=>{const a=(f.attrs||[]).find(a=>a.id==id);return a?n0(a.v):0};
function html(t){
  const p=pOf(t);if(typeof SISM==='undefined'||SISM!=='op'||!pode(p))return '';
  const f=fDe(p);if(!f)return '';
  const D=S.derivar(f,{}),its=f.inv.items;
  const armas=its.filter(i=>i.tipo=='arma'&&(i.qtd===undefined||n0(i.qtd)>0));
  const opt=f.skills.map(s=>`<option>${esc(s.n)}</option>`).join('');
  const linha=(i,k)=>{const eqv=i.tipo=='arma'||i.tipo=='protecao',gast=i.tipo=='consumivel';
    return `<div class="q" style="align-items:center"><span class="m" style="flex:1">${esc(i.n||'Item')}${n0(i.qtd)>1?' x'+n0(i.qtd):''}</span>${eqv?`<button data-mf="eq" data-i="${k}" class="${i.eq?'on':''}" style="width:auto">${i.eq?'Equipado':'Equipar'}</button>`:''}${gast?`<button data-mf="usar" data-i="${k}" style="width:auto">Usar</button>`:''}</div>`};
  return `<h5>Ficha de ${esc(p.nome||'personagem')}</h5>
<div class="m">Defesa ${D.def} | Desloc. ${D.desloc} m | PE por turno ${D.limPE} | Carga ${D.usado}/${D.cap}</div>
<div class="q"><select data-mf-sel style="flex:1;min-width:0">${opt}</select><button data-mf="rolar" style="width:auto">Rolar</button><a class="m" href="ficha.html?id=${p.id}" target="_blank" rel="noopener" style="align-self:center">Abrir ficha</a></div>
${armas.length?`<h5>Armas</h5>${armas.map(a=>`<div class="q" style="align-items:center"><span class="m" style="flex:1">${esc(a.n)} (${esc(S.armaEf(a).dano||'?')})${(a.mods||[]).length?' · '+esc(a.mods.map(S.modNome).join(', ')):''}</span><button data-mf="atk" data-i="${its.indexOf(a)}" style="width:auto">Atacar</button><button data-mf="dano" data-i="${its.indexOf(a)}" style="width:auto">Dano</button></div>`).join('')}`:''}
<details class="inv" ${its.length?'open':''}><summary>Inventário (${its.length})</summary>${its.map((i,k)=>linha(i,k)).join('')||'<div class="m">Vazio.</div>'}</details>`;
}
async function grava(t,mut){
  const p=pOf(t);if(!p)return false;
  const r=await sb.from('personagens').select('dados').eq('id',p.id).maybeSingle();if(r.error||!r.data)return false;
  const f=S.prepararOP(r.data.dados);mut(f);S.aplicar(f,{});
  const u=await sb.from('personagens').update({dados:f}).eq('id',p.id);if(u.error){toast('Não consegui salvar a ficha: '+u.error.message);return false}
  p.dados=f;p.inv=f.inv;ui();return true}
document.addEventListener('click',async e=>{
  const b=e.target.closest('[data-mf]');if(!b||typeof sel==='undefined'||!sel)return;
  const t=sel,p=pOf(t);if(!pode(p))return;const f=fDe(p);if(!f)return;const D=S.derivar(f,{}),nome=p.nome||t.n||'Personagem',k=b.dataset.mf,i=+b.dataset.i;
  if(k=='rolar'){const sk=f.skills.find(s=>s.n==(document.querySelector('[data-mf-sel]')||{}).value);if(!sk)return;
    const bn=bonusPer(f,D,sk),r=S.teste(av(f,sk.a),bn);logm(`${esc(nome)} · ${esc(sk.n)}: [${r.r}] → ${r.d}${bn?' '+sinal(bn):''} = <b>${r.total}</b>`)}
  else if(k=='atk'){const it=f.inv.items[i];if(!it)return;const ar=it.arma||{},sk=f.skills.find(s=>s.n==(ar.per||'Luta'))||{a:'for',t:0,o:0,n:ar.per||'Luta'};
    const ef=S.armaEf(it),bn=bonusPer(f,D,sk)+ef.atk,r=S.teste(av(f,sk.a),bn);logm(`${esc(nome)} · ${esc(it.n)} ataque (${esc(sk.n)}): [${r.r}] → ${r.d}${bn?' '+sinal(bn):''} = <b>${r.total}</b>${ef.crit?' (crít. '+esc(ef.crit)+')':''}`)}
  else if(k=='dano'){const it=f.inv.items[i];if(!it)return;const dn=S.armaEf(it).dano,r=S.rolar(dn);if(!r)return toast('Essa arma está sem dano na ficha.');logm(`${esc(nome)} · ${esc(it.n)} dano ${esc(dn)}: ${r.txt} = <b>${r.total}</b>`)}
  else if(k=='eq'){const id=f.inv.items[i]&&f.inv.items[i].id;await grava(t,g=>{const it=g.inv.items.find(x=>x.id==id);if(!it)return;it.eq=!it.eq;
      if(it.eq&&it.tipo=='protecao')g.inv.items.forEach(o=>{if(o!==it&&o.tipo=='protecao'&&o.eq&&((o.sub=='escudo')==(it.sub=='escudo')))o.eq=false})})}
  else if(k=='usar'){const id=f.inv.items[i]&&f.inv.items[i].id,nm=f.inv.items[i]&&f.inv.items[i].n;
    if(await grava(t,g=>{const j=g.inv.items.findIndex(x=>x.id==id);if(j<0)return;const it=g.inv.items[j];if(n0(it.qtd)>1)it.qtd=n0(it.qtd)-1;else g.inv.items.splice(j,1)}))logm(`${esc(nome)} usou ${esc(nm||'um item')}.`)}
});
window.MesaFicha={html};
})();
