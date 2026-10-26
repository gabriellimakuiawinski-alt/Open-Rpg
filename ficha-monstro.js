/* ficha-monstro.js — ficha de MONSTRO (Ordem Paranormal, classe oculta "criatura").
   Visual de ficha de ameaça: PV com barra, testes e ataques com botão de rolar, habilidades em cartões.
   Usa as funções da ficha.html (esc, num, inp, toast, touch, render, curF) e as regras de sistemas.js. */
(function () {
  'use strict';
  const S = window.SIS, n0 = S.n0;
  const sinal = v => (v > 0 ? '+' : '') + v;
  const COR = { Sangue: '#c0392b', Morte: '#8d939c', Conhecimento: '#d6a419', Energia: '#9b59d0', Medo: '#e8e2d0', Outro: '#6b7a8f' };
  const ACOES = ['Padrão', 'Movimento', 'Completa', 'Reação', 'Livre', 'Passiva'];
  const TABS = [['g', 'Monstro'], ['n', 'Notas']];
  const info = (f, k) => ((f.info || []).find(x => x.n == k) || {}).v || '';
  const av = (f, id) => { const a = (f.attrs || []).find(a => a.id == id); return a ? n0(a.v) : 0 };
  const dado = (f, id, b) => { const q = av(f, id); return (q > 0 ? q : 2) + 'd20' + (q > 0 ? '' : '↓') + (b ? ' ' + sinal(b) : '') };

  /* separa a ficha em partes: ataques (armas), habilidades (poderes) e anotações (resistências etc.) */
  function partes(f) {
    const notas = {}, habs = [];
    (f.poderes || []).forEach(p => {
      if (p.n == 'Anotações do inimigo' || p.n == 'Anotações do inventário') {
        String(p.desc || '').split('\n').forEach(l => { const m = l.match(/^(Resistências|Vulnerabilidades|Sentidos):\s*(.*)$/); if (m) notas[m[1]] = m[2]; else if (l.trim()) notas.txt = (notas.txt ? notas.txt + '\n' : '') + l });
        return;
      }
      const m = String(p.desc || '').match(/^(Padrão|Movimento|Completa|Reação|Livre|Passiva)\.\s*([\s\S]*)$/);
      habs.push({ i: (f.poderes || []).indexOf(p), n: p.n, acao: m ? m[1] : 'Passiva', desc: m ? m[2] : (p.desc || '') });
    });
    return { notas, habs, atqs: (f.inv.items || []).map((it, i) => ({ it, i })).filter(x => x.it.tipo == 'arma') };
  }
  const bonusSk = (f, D, s) => n0(s.t) + n0(s.o) + n0(D.per[s.n]) + (['Fortitude', 'Reflexos', 'Vontade'].includes(s.n) ? D.res : 0);

  function vMonstro(f) {
    const D = window.OP.calc(f).D, { notas, habs, atqs } = partes(f), el = info(f, 'Elemento') || 'Outro', vd = info(f, 'VD'), tam = info(f, 'Tamanho');
    const cor = COR[el] || COR.Outro, i = f.stats.findIndex(s => s.id == 'pv'), pv = f.stats[i] || { cur: 0, max: 0 };
    const machucado = pv.max > 0 && pv.cur <= pv.max / 2;
    const sk = n => f.skills.find(s => s.n == n);
    const teste = n => { const s = sk(n); if (!s) return ''; const b = bonusSk(f, D, s);
      return `<button class="mt" data-act="mon-rolar" data-sk="${esc(n)}"><small>${esc(n)}</small><b>${dado(f, s.a, b)}</b></button>` };
    const extra = f.skills.filter(s => !['Fortitude', 'Reflexos', 'Vontade', 'Iniciativa', 'Percepção', 'Luta', 'Pontaria'].includes(s.n) && (n0(s.o) || n0(s.t)));
    return `<section class="mon" style="--el:${cor}">
<div class="mon-topo"><span class="mon-el">${esc(el)}</span>${vd ? `<span class="mon-vd">VD <b>${esc(vd)}</b></span>` : ''}${tam ? `<span class="mon-tam">${esc(tam)}</span>` : ''}</div>
<input class="mon-nome" data-p="nome" value="${esc(f.nome)}" placeholder="Nome do monstro">
<div class="mon-pv${machucado ? ' mach' : ''}"><div class="mon-pvh"><b>PV</b><span class="m">${machucado ? 'machucado' : ''}</span><span class="sp"></span><span class="m">máx. <span data-d="mx-pv">${n0(pv.max)}</span></span></div>
<div class="bar"><i id="sb${i}"></i></div>
<div class="ctl"><button data-act=sd data-i=${i} data-d=-10 class="b5">−10</button><button data-act=sd data-i=${i} data-d=-1>−</button>${num(`stats.${i}.cur`, pv.cur, 'min=0')}<button data-act=sd data-i=${i} data-d=1>+</button><button data-act=sd data-i=${i} data-d=10 class="b5">+10</button></div></div>
<div class="mon-g4"><div class="mt"><small>Defesa</small><b data-d="def">${D.def}</b></div><div class="mt"><small>Desloc.</small><b data-d="desloc">${D.desloc}m</b></div>${teste('Iniciativa')}${teste('Percepção')}</div>
<div class="mon-g3">${teste('Fortitude')}${teste('Reflexos')}${teste('Vontade')}</div>
<div class="mon-atr">${S.ATR.map(([id, ab]) => `<div><small>${ab}</small><b>${av(f, id)}</b></div>`).join('')}</div>
${notas['Resistências'] || notas['Vulnerabilidades'] || notas['Sentidos'] ? `<div class="mon-chips">${notas['Resistências'] ? `<p><b>Resistências</b> ${esc(notas['Resistências'])}</p>` : ''}${notas['Vulnerabilidades'] ? `<p class="vul"><b>Vulnerabilidades</b> ${esc(notas['Vulnerabilidades'])}</p>` : ''}${notas['Sentidos'] ? `<p><b>Sentidos</b> ${esc(notas['Sentidos'])}</p>` : ''}</div>` : ''}
</section>
${atqs.length ? `<section class="mon-sec" style="--el:${cor}"><h3>Ataques</h3>${atqs.map(({ it, i }) => { const ef = S.armaEf(it), s = sk((it.arma || {}).per || 'Luta') || { a: 'for' };
      return `<div class="mon-atq"><div class="mon-atqn"><b>${esc(it.n)}</b><small>${esc((it.arma || {}).alc || '')}</small></div>
<div class="mon-atqb"><button data-act="mon-atk" data-i="${i}"><small>Atacar</small><b>${dado(f, s.a, bonusSk(f, D, s) + ef.atk)}</b></button><button data-act="mon-dano" data-i="${i}"><small>Dano</small><b>${esc(ef.dano || '—')}</b></button></div></div>` }).join('')}</section>` : ''}
${extra.length ? `<section class="mon-sec" style="--el:${cor}"><h3>Perícias</h3><div class="mon-g3">${extra.map(s => teste(s.n)).join('')}</div></section>` : ''}
${habs.length ? `<section class="mon-sec" style="--el:${cor}"><h3>Habilidades</h3>${habs.map(h => `<div class="mon-hab"><div class="mon-habn"><b>${esc(h.n)}</b><span class="mon-ac">${esc(h.acao)}</span></div><p>${esc(h.desc)}</p></div>`).join('')}</section>` : ''}
<details class="mon-aj"><summary>Ajustar números do monstro</summary>
<p class="m" style="font-size:12px;margin:6px 0">Mudar o atributo muda PV e Defesa de acordo com a regra. Estes ajustes somam por cima.</p>
<div class="g3">${[['pv', 'PV'], ['def', 'Defesa'], ['desloc', 'Desloc. (m)']].map(([k, l]) => `<label class=fld>${l}${num('op.bonus.' + k, (f.op.bonus || {})[k] || 0, 'data-rr')}</label>`).join('')}</div>
<div class="g3">${S.ATR.map(([id, ab]) => { const j = f.attrs.findIndex(a => a.id == id); return `<label class=fld>${ab}${num(`attrs.${j}.v`, f.attrs[j].v, 'min=0 data-rr')}</label>` }).join('')}</div>
</details>`;
  }

  function acao(a, d, f) {
    const D = window.OP.calc(f).D, nome = esc(f.nome || 'Monstro');
    if (a == 'mon-rolar') { const s = f.skills.find(x => x.n == d.sk); if (!s) return true; const b = bonusSk(f, D, s), r = S.teste(av(f, s.a), b);
      toast(`${nome} · ${esc(s.n)}: [${r.r}] → ${r.d}${b ? ' ' + sinal(b) : ''} = <b>${r.total}</b>`); return true }
    if (a == 'mon-atk') { const it = f.inv.items[+d.i]; if (!it) return true; const ar = it.arma || {}, s = f.skills.find(x => x.n == (ar.per || 'Luta')) || { a: 'for' }, ef = S.armaEf(it),
        b = bonusSk(f, D, s) + ef.atk, r = S.teste(av(f, s.a), b);
      toast(`${nome} · ${esc(it.n)}: [${r.r}] → ${r.d}${b ? ' ' + sinal(b) : ''} = <b>${r.total}</b>${ef.crit ? ' (crít. ' + esc(ef.crit) + ')' : ''}`); return true }
    if (a == 'mon-dano') { const it = f.inv.items[+d.i]; if (!it) return true; const dn = S.armaEf(it).dano, r = S.rolar(dn);
      if (!r) { toast('Esse ataque está sem dano.'); return true } toast(`${nome} · ${esc(it.n)} dano ${esc(dn)}: ${r.txt} = <b>${r.total}</b>`); return true }
    return false;
  }
  window.MON = { TABS, views: { g: vMonstro }, acao, ehMonstro: f => !!f && !!f.op && f.op.classe == 'criatura' };
})();
