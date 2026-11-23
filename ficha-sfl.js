/* ficha-sfl.js — ficha do Search For Light (automática). Usa as funções da ficha.html
   (inp, num, esc, toast, touch, render, curF, CAMPS, meuPapel...) e as regras de sfl-regras.js (SIS.sfl). */
(function () {
  'use strict';
  const S = window.SIS, R = S.sfl, n0 = S.n0;
  const campDe = f => CAMPS.find(c => c.id == f._camp) || null;
  const mestre = f => !!f._camp && meuPapel(f._camp) == 'mestre';
  const podeMec = f => f._camp ? mestre(f) : f._dono == ME.id;     // marco, ajustes e regras de item
  const moeda = f => S.moedaDe(campDe(f));
  const sinal = v => (v > 0 ? '+' : '') + v;
  const idxAt = (f, id) => f.attrs.findIndex(a => a.id == id);
  let ULT = null;
  const TABS = [['g', 'Ficha'], ['c', 'Combate'], ['p', 'Perícias'], ['i', 'Inventário'], ['h', 'Habilidades'], ['n', 'Notas']];
  const sel = (p, opts, v, ex = '') => `<select data-p="${p}" ${ex}>${opts.map(([k, l]) => `<option value="${esc(k)}" ${String(k) == String(v) ? 'selected' : ''}>${esc(l)}</option>`).join('')}</select>`;
  let VD = 0;   // vantagem (+1 dado) ou desvantagem (-1) para as próximas rolagens
  function calc(f) { const r = R.aplicar(f); ULT = r.D; return r }

  /* ---------- janela de escolha ---------- */
  function janela(titulo, topo, lista, aoEscolher) {
    const o = document.createElement('div'); o.id = 'md';
    o.innerHTML = `<div class="mb"><h3>${esc(titulo)}</h3>${topo || ''}<div class="catl">${lista}</div><button data-x style="align-self:flex-end">Fechar</button></div>`;
    document.body.append(o);
    o.onclick = e => { if (e.target === o || e.target.closest('[data-x]')) { o.remove(); return } const b = e.target.closest('.cat-i'); if (b) aoEscolher(b, () => o.remove()) };
    return o;
  }
  const botao = (k, t, d, off) => `<button class="cat-i" data-k="${esc(k)}" ${off ? 'disabled' : ''}><b>${esc(t)}</b><small style="white-space:normal">${esc(d || '')}</small></button>`;

  /* ---------- pedaços ---------- */
  function barra(f, id) {
    const i = f.stats.findIndex(s => s.id == id), s = f.stats[i]; if (i < 0) return '';
    const extra = id == 'inf' ? `<span class="m" data-d="faixa"> · ${esc(ULT.faixa[1])}</span>` : '';
    return `<div class="st op-st st-${id}"><div class="sth"><b class="k">${esc(s.n)}</b>${extra}<span class="sp"></span><span class="m" data-d="max-${id}">máx. ${n0(s.max)}</span></div>
<div class="bar"><i id="sb${i}"></i></div>
<div class="ctl"><button data-act=sd data-i=${i} data-d=-1>−</button>${num(`stats.${i}.cur`, s.cur, 'min=0')}<span class=m>/ <span data-d="mx-${id}">${n0(s.max)}</span></span><button data-act=sd data-i=${i} data-d=1>＋</button></div></div>`;
  }
  function vdBar() {
    return `<div class="itr vd"><span class="m">Próximas rolagens:</span>${[[-1, 'Desvantagem'], [0, 'Normal'], [1, 'Vantagem']].map(([v, l]) => `<button class="mini ${VD == v ? 'on' : ''}" data-act="sfl-vd" data-v="${v}" type="button">${l}</button>`).join('')}</div>`;
  }

  function avisos(f, D) {
    const s = f.sfl, L = [];
    if (!s.classe) L.push('Escolha a <b>classe</b> (Combatente, Batedor, Técnico ou Voz).');
    if (!s.origem) L.push('Escolha a <b>origem</b> (o que o personagem fazia antes).');
    if (s.classe && s.perClasse.length < 2) L.push(`Escolha <b>2 perícias</b> da classe (${s.perClasse.length}/2).`);
    if (s.classe && s.marco >= 1 && !s.trilha) L.push('O marco 1 chegou: escolha a <b>trilha</b>.');
    if (D.escPend > 0) L.push(`Você tem <b>${D.escPend}</b> escolha${D.escPend > 1 ? 's' : ''} de marco (habilidade da classe ou benefício geral). <button class="mini" data-act="sfl-esc" type="button">Escolher</button>`);
    if (s.armas.length < D.armasMax && s.classe) L.push(`Treine sua <b>arma especial</b> inicial na aba Habilidades (${s.armas.length}/${D.armasMax}).`);
    if (!s.linha) L.push('Escolha sua <b>linha de poder</b> na aba Habilidades.');
    if (D.pontos > D.pontosMax) L.push(`Atributos: ${D.pontos} pontos usados, o limite é ${D.pontosMax}.`);
    if (f.attrs.some(a => n0(a.v) > 5)) L.push('Atributo máximo é 5.');
    if (D.excesso) L.push(`Carga: <b>${n0(D.usado)}</b> de ${D.slots} espaços. Passou mais de 3 do limite: <b>não dá para carregar</b>. Largue ou guarde itens.`);
    else if (D.sobre) L.push(`Sobrecarregado (${n0(D.usado)} de ${D.slots} espaços): −3 m de movimento, desvantagem em Parkour e Furtividade e sem Impulso.`);
    if (D.prontos > D.prontosMax) L.push(`Itens prontos: ${D.prontos} de ${D.prontosMax}. Tire algum da mão ou do cinto (aba Inventário).`);
    return L.length ? `<section class="card avisos"><h2>Pendências da ficha</h2>${L.map(x => `<p class="m aviso-l">${x}</p>`).join('')}</section>` : '';
  }

  function vFicha(f) {
    const D = ULT, s = f.sfl, meu = f._dono == ME.id, pp = meuPapel(f._camp), M = podeMec(f);
    const C = D.C, O = D.O;
    return `${meu ? '' : `<p class=m style="margin:0 0 10px">Ficha de <b>${esc(f._donoNome || 'outro jogador')}</b>. ${podeEditar(f) ? 'Você a edita como ' + (pp == 'mestre' ? 'mestre' : 'admin') + ' da campanha.' : 'Somente leitura.'}</p>`}${avisos(f, D)}
<section class="card dossie"><div class="carimbo-op">Search For Light</div>
<label class=fld>Nome do personagem${inp('nome', f.nome)}</label>
<div class="g2b"><label class=fld>Classe${sel('sfl.classe', [['', '— escolha —']].concat(R.dados.classes.map(c => [c.id, c.n])), s.classe, 'data-rr data-cls')}</label>
<label class=fld>Origem${sel('sfl.origem', [['', '— escolha —']].concat(R.dados.origens.map(o => [o.id, o.n])), s.origem, 'data-rr')}</label></div>
<div class="g2b"><label class=fld>Trilha${sel('sfl.trilha', [['', s.marco >= 1 ? '— escolha —' : 'no marco 1']].concat(C ? C.trilhas.map(t => [t.id, t.n + ' (' + t.t + ')']) : []), s.trilha, 'data-rr' + (s.marco >= 1 ? '' : ' disabled'))}</label>
<label class=fld>Marco (evolução)${M ? `<span class="ctl"><button data-act="sfl-marco" data-d="-1" type="button">−</button><b class="big" style="min-width:34px;text-align:center">${s.marco}</b><button data-act="sfl-marco" data-d="1" type="button">＋</button><span class="m">de 8</span></span>` : `<b class="big">${s.marco} de 8</b>`}</label></div>
${O ? `<p class="m" style="margin:4px 0"><b>${esc(O.n)}</b>: ${esc(O.traco)} <i>Peso: ${esc(O.peso)}</i></p>` : ''}
<div class="selos"><div class="selo"><b>${D.pvMax}</b><small>Vida</small></div><div class="selo"><b>${D.folMax}</b><small>Fôlego</small></div><div class="selo"><b data-d="arm">${D.armadura}</b><small>Armadura</small></div><div class="selo"><b>${D.slots}</b><small>Espaços</small></div><div class="selo"><b>${D.mov}</b><small>Movimento (m)</small></div></div>
<details class="mais"><summary>Mais dados do personagem</summary>
${f._camp ? `<p class="m mini-l">Campanha: <b>${esc((campDe(f) || {}).nome || '')}</b> · Sistema <b>Search For Light</b></p>` : ''}
${meu ? `<label class=fld>Campanha<select data-camp><option value="">— nenhuma (só você vê) —</option>${CAMPS.filter(c => c.id == f._camp || meuPapel(c.id)).map(c => `<option value="${c.id}" ${c.id == f._camp ? 'selected' : ''}>${esc(c.nome)}</option>`).join('')}</select></label>` : ''}
${!f._camp && meu ? `<label class=fld>Sistema da ficha<select data-sis>${Object.entries(S.SISTEMAS).map(([k, x]) => `<option value="${k}" ${k == 'sfl' ? 'selected' : ''}>${x.n}</option>`).join('')}</select></label>` : ''}
${meu || pp == 'mestre' ? `<label class=sm style="font-size:14px;margin:0 0 6px"><input type=checkbox data-flag=_priv ${f._priv ? 'checked' : ''}> Ficha privada (só o dono e o mestre veem)</label>` : ''}
${pp == 'mestre' ? `<label class=sm style="font-size:14px;margin:0 0 6px"><input type=checkbox data-flag=_npc ${f._npc ? 'checked' : ''}> NPC (só o mestre vê)</label>` : ''}
</details></section>
<section class="card"><h2>Condição</h2>${['pv', 'pe', 'medo', 'inf'].map(id => barra(f, id)).join('')}
<p class="m" style="font-size:13px;margin:6px 0 0" data-d="faixa-t">Infecção: <b>${esc(D.faixa[1])}</b> — ${esc(D.faixa[2])}. Medo 3 ou mais: desvantagem em Vontade e em ataques à distância. Medo 5: congela ou foge por uma rodada.</p>
<details class="ajuste"><summary>Ajustes manuais nos máximos</summary><p class="m" style="font-size:13px;margin:6px 0">Para efeitos que o sistema ainda não conhece.</p>
<div class="g3">${[['pv', 'Vida'], ['fol', 'Fôlego'], ['slots', 'Espaços']].map(([k, l]) => `<label class=sm>${l} ${num('sfl.bonus.' + k, (s.bonus || {})[k] || 0, 'data-rr')}</label>`).join('')}</div></details></section>
<section class="card"><h2>Atributos</h2><div class="ats">${R.ATR.map(([id, nome]) => { const i = idxAt(f, id); return `<div class=at><span class="k">${esc(nome)}</span>${num(`attrs.${i}.v`, f.attrs[i].v, 'min=0 max=5 class=big data-rr')}</div>` }).join('')}</div>
<p class="m" style="font-size:12px;margin:6px 0 0">O atributo é o número de dados d20 do teste (fica o maior). Ele não soma ao resultado. Pontos: <b data-d="pts">${D.pontos}</b> de ${D.pontosMax} (máximo 4 na criação, 5 com marco).</p></section>`;
  }

  const fxH = L => L.length ? `<span class="fx">${L.map(([k, v]) => `<span><i>${esc(k)}</i>${esc(v)}</span>`).join('')}</span>` : '';
  const itemDe = (f, i) => +i < 0 ? R.PUNHOS(f) : f.inv.items[+i];
  function linhaArma(f, it, i) {
    const a = it.arma || {}, at = R.ataque(f, it);
    const L = [['Dano', (a.dano || '') + (at.melee ? ' + Corpo' : '')], ['Crítico', a.crit || '']];
    if (a.traco && a.traco != 'n/a') L.push(['Traço', a.traco]);
    if (at.fx.length) L.push(['No crítico', at.fx.join('; ')]);
    if (at.mods.length) L.push(['Modificações', at.mods.map(m => m.n).join(', ')]);
    const onde = it.virtual ? '' : it.pronto ? ' · pronta' : ' · na mochila (sacar gasta o movimento)';
    return `<div class="arma"><div class="ar-n"><b>${esc(it.n || 'Arma')}${it.quebrada ? ' <span class="m">(quebrada)</span>' : ''}</b><small>${esc(at.rotulo)}${onde}${at.treinada ? '' : ' · SEM TREINO (−1 dado)'}</small>${fxH(L)}</div>
${it.quebrada ? `<button class="mini" data-act="sfl-conserta" data-i="${i}" type="button">Consertar</button>` : `<button class="roll" data-act="sfl-atk" data-i="${i}" title="Atacar (${esc(at.rotulo)})">Atacar</button>${at.podeMirar ? `<button class="mini" data-act="sfl-atk" data-i="${i}" data-mira="1" type="button">Mirar e atacar</button>` : ''}<button class="mini" data-act="sfl-dano" data-i="${i}">Dano</button><button class="mini" data-act="sfl-dano" data-i="${i}" data-c="1">Dano crít.</button>`}</div>`;
  }
  function vCombate(f) {
    const D = ULT, s = f.sfl, its = f.inv.items, armas = its.map((it, i) => [it, i]).filter(([it]) => it.tipo == 'arma' && n0(it.qtd === undefined ? 1 : it.qtd) > 0).sort((x, y) => (y[0].pronto ? 1 : 0) - (x[0].pronto ? 1 : 0));
    const ref = R.atr(f, 'ref'), cor = R.atr(f, 'cor'), blq = bloqueioCom(f);
    const imp = R.IMPULSO[D.impulso], est = s.pers;
    return `<section class="card"><h2>Rolagens</h2>${vdBar()}
<div class="res"><button class="btn-res" data-act="sfl-ini" type="button"><b>Iniciativa</b><small>${ref + (s.classe == 'batedor' ? 1 : 0)}d20</small></button>
<button class="btn-res" data-act="sfl-esq" type="button"><b>Esquiva</b><small>${ref}d20 ${sinal(Math.max(R.treinoDe(f, 'Parkour'), R.treinoDe(f, 'Atletismo')))} · −1 Fôlego</small></button>
<button class="btn-res" data-act="sfl-blq" type="button"><b>Bloqueio</b><small>${cor + blq.dado}d20 ${sinal(Math.max(R.treinoDe(f, 'Contundente'), R.treinoDe(f, 'Cortante')))} · ${esc(blq.rot)}</small></button>
<button class="btn-res" data-act="sfl-ctr" type="button"><b>Contra-ataque</b><small>${cor}d20 ${sinal(Math.max(R.treinoDe(f, 'Contundente'), R.treinoDe(f, 'Cortante')))}</small></button></div>
<p class="m" style="font-size:12px;margin:8px 0 0">Não existe Defesa fixa: quem é atacado rola a reação. Armadura vestida reduz <b>${D.armadura}</b> de dano${D.armaduraNome ? ' (' + esc(D.armaduraNome) + (D.armaduraTiro ? ', ' + D.armaduraTiro + ' contra tiro' : '') + ')' : ''}.</p></section>
<section class="card"><h2>Ataques</h2>${linhaArma(f, R.PUNHOS(f), -1)}${armas.map(([it, i]) => linhaArma(f, it, i)).join('')}
<p class="m" style="font-size:12px;margin:8px 0 0">Crítico é tirar um número alto no dado, e nem todo crítico acerta: o ataque ainda precisa vencer a reação. No crítico que acerta, o efeito acontece e os dados de dano são multiplicados. Arma corpo a corpo só quebra com <b>1 natural</b> num ataque que falhou. Você tem <b>${D.prontosMax}</b> itens prontos: sacar um item pronto é livre; tirar da mochila gasta o movimento.</p></section>
<section class="card"><h2>Movimento e parkour</h2>
<div class="selos"><div class="selo"><b>${D.mov} m</b><small>Movimento</small></div><div class="selo"><b>${n0(D.fol)}</b><small>Fôlego</small></div><div class="selo"><b>${D.impulso}</b><small>Impulso</small></div>${est ? `<div class="selo larga"><b>${est} · ${esc(R.ESTAGIOS[est])}</b><small>Perseguição</small></div>` : ''}</div>
<div class="itr"><span class="m">Impulso:</span><button class="mini" data-act="sfl-imp" data-d="-1" type="button">−</button><b>${D.impulso}</b><button class="mini" data-act="sfl-imp" data-d="1" type="button" ${D.sobre ? 'disabled' : ''}>＋</button><span class="m">${esc(imp[2])}${D.sobre ? ' · sobrecarregado: não ganha Impulso' : ''}${s.impVant && D.impulso == 3 ? ' · vantagem pronta' : ''}</span></div>
<div class="itr">${est ? `<span class="m">Perseguição:</span><button class="mini" data-act="sfl-pers" data-d="-1" type="button">−</button><b>${est}</b><button class="mini" data-act="sfl-pers" data-d="1" type="button">＋</button><button class="mini" data-act="sfl-pers" data-d="0" type="button">Terminar</button>` : `<button class="mini" data-act="sfl-pers" data-d="ini" type="button">Começar perseguição</button>`}</div>
<button class="add" data-act="sfl-pk" type="button">Teste de Parkour</button>
<p class="m" style="font-size:12px;margin:8px 0 0">Parkour livre (sem perigo) não pede teste nem Fôlego. No parkour de risco a ficha rola Reflexo + Parkour, gasta o Fôlego do movimento e diz a consequência. Em perseguição, superar o obstáculo dá +1 de Impulso (máx. 1 por rodada) e +1 estágio; falhar zera o Impulso e tira 1 estágio. Escapar = estágio 6 <b>e</b> romper o contato. Os metros do Impulso não somam com outros bônus de metros: vale o maior.</p></section>
<section class="card"><h2>Descanso</h2><div class="g2b"><button class="add" data-act="sfl-desc" data-t="curto" type="button">Descanso curto (10 min)</button><button class="add" data-act="sfl-desc" data-t="longo" type="button">Descanso longo (noite segura)</button></div>
<p class="m" style="font-size:12px;margin:6px 0 0">Curto: recupera todo o Fôlego. Longo: recupera 1d6 + Corpo de Vida, Medo −2 e Infecção −1${n0(s.adren) ? ', e tira o −' + s.adren + ' de Fôlego da adrenalina' : ''}.${s.origem == 'morador-de-rua' ? ' Morador de rua: o descanso longo em lugar improvisado conta como seguro para o Medo (não para a Infecção).' : ''}</p></section>`;
  }
  /* com o que o personagem bloqueia: escudo pronto, arma de corpo a corpo pronta ou a mão */
  function bloqueioCom(f) {
    const its = f.inv.items, esc_ = its.find(it => it.tipo == 'armadura' && it.sub == 'escudo' && (it.eq || it.pronto) && !it.quebrada && n0(it.qtd === undefined ? 1 : it.qtd) > 0);
    const arma = its.filter(it => it.tipo == 'arma' && it.pronto && !it.quebrada && ['contundente', 'cortante'].includes((it.arma || {}).cat)).sort((a, b) => (R.modsDe(b).some(m => m.auto.blq) ? 1 : 0) - (R.modsDe(a).some(m => m.auto.blq) ? 1 : 0))[0];
    const it = esc_ || arma || null, div = esc_ ? (R.tem(f, 'Escudo vivo') ? 2 : 3) : arma ? 3 : (R.tem(f, 'Mãos de ferro') ? 4 : 5);
    return { it, div, dado: it && R.modsDe(it).some(m => m.auto.blq) ? 1 : 0, rot: it ? 'com ' + it.n + ' (÷' + div + ')' : 'com a mão (÷' + div + ')' };
  }

  function vPericias(f) {
    return `<section class="card per-sec"><h2>Perícias</h2>${vdBar()}<p class="m" style="margin:0 0 8px;font-size:13px">Role o número do atributo em d20 e fique com o maior. O atributo não soma: só o treino. Perícias de origem e classe nascem treinadas.</p>
${f.skills.map((k, i) => `<div class="sk"><button class="roll" data-act="roll" data-i="${i}" title="Rolar">Rolar</button><span class="sn">${esc(k.n)}${ULT.fonte.has(k.n) ? ' <small class="m">(origem/classe)</small>' : ''}${R.desvAuto(f, ULT, k.n).length ? ` <small class="m">(desvantagem: ${esc(R.desvAuto(f, ULT, k.n).join(', '))})</small>` : ''}</span><select data-p="skills.${i}.t" data-n title="Treino">${R.TREINO.map(([v, l]) => `<option value=${v} ${k.t == v ? 'selected' : ''}>${l}</option>`).join('')}</select><select data-p="skills.${i}.a" title="Atributo">${attrOpts(f, k.a)}</select><b id="sk${i}"></b></div>`).join('')}
</section>`;
  }

  function itemCard(f, it, i) {
    const M = podeMec(f), tipo = it.tipo || 'geral', a = it.arma || {}, arm = tipo == 'armadura' && it.sub != 'escudo';
    const lim = tipo == 'arma' || it.sub == 'escudo' ? R.limiteMods(it) : 0, mods = R.modsDe(it);
    const tag = R.etiquetas(it), ocupa = R.espItem(it);
    const bt = [];
    if (arm) bt.push(`<button class="eqb ${it.eq ? 'on' : ''}" data-act="sfl-eq" data-i="${i}">${it.eq ? 'Vestida' : 'Vestir'}</button>`);
    else if (tipo == 'mochila') bt.push(`<button class="eqb ${it.eq ? 'on' : ''}" data-act="sfl-eq" data-i="${i}">${it.eq ? 'Nas costas' : 'Usar'}</button>`);
    else bt.push(`<button class="eqb ${it.pronto ? 'on' : ''}" data-act="sfl-pronto" data-i="${i}" title="Na mão, no cinto ou no coldre">${it.pronto ? 'Pronto' : 'Deixar pronto'}</button>`);
    if (it.uso) bt.push(`<button class="mini" data-act="sfl-usar" data-i="${i}" type="button">Usar</button>`);
    if (lim > 0 && !it.quebrada) bt.push(`<button class="mini" data-act="sfl-mod" data-i="${i}" type="button">Modificar</button>`);
    if (it.quebrada) bt.push(`<button class="mini" data-act="sfl-conserta" data-i="${i}" type="button">Consertar</button>`);
    return `<div class="it op-it ${it.eq || it.pronto ? 'eq' : ''}"><div class="itr">${inp(`inv.items.${i}.n`, it.n, 'placeholder="Nome do item" class=in')}${bt.join('')}<button class=x data-act=del data-l=items data-i=${i}>Remover</button></div>
<div class="itr"><label class=sm>Quantidade${num(`inv.items.${i}.qtd`, it.qtd === undefined ? 1 : it.qtd, 'min=0 data-rr')}</label><span class="m it-res">ocupa <b>${ocupa}</b> esp.${it.usos !== undefined ? ' · usos ' + n0(it.usos) : ''}${it.quebrada ? ' · <b>quebrada</b>' : ''}</span></div>
<div class="tags">${tag.map(x => `<span>${esc(x)}</span>`).join('')}${tipo == 'armadura' && it.sub != 'escudo' ? `<span>reduz ${n0(it.red)}${it.redTiro ? ' (' + it.redTiro + ' contra tiro)' : ''}</span>` : ''}</div>
${tipo == 'arma' ? fxH([['Dano', a.dano || ''], ['Crítico', a.crit || '']].concat(a.traco && a.traco != 'n/a' ? [['Traço', a.traco]] : []).concat(a.efeito && a.efeito != 'n/a' ? [['No crítico', a.efeito]] : [])) : ''}
${lim > 0 ? `<div class="mods">${mods.map(m => `<span class="modt">${esc(m.n)} <small>${esc(m.d)}</small> <button class="mini" data-act="sfl-modx" data-i="${i}" data-m="${esc(m.id)}">Remover</button></span>`).join('')}<small class="m">Modificações: ${mods.length} de ${lim}</small></div>` : ''}
${inp(`inv.items.${i}.desc`, it.desc || '', 'placeholder="Descrição e notas"')}
<details class="mec"><summary>Mais detalhes do item</summary><div class="itr"><label class=sm>Espaços${num(`inv.items.${i}.esp`, it.esp, 'min=0 step=.5 data-rr' + (M ? '' : ' disabled'))}</label><label class=sm>Pilha${num(`inv.items.${i}.pilha`, it.pilha || 0, 'min=0 data-rr' + (M ? '' : ' disabled'))}</label>
<label class=sm>Tipo ${sel(`inv.items.${i}.tipo`, [['geral', 'Geral'], ['arma', 'Arma'], ['armadura', 'Armadura'], ['mochila', 'Mochila'], ['municao', 'Munição'], ['consumivel', 'Consumível'], ['material', 'Material']], tipo, 'data-rr' + (M ? '' : ' disabled'))}</label></div>
${M && tipo == 'arma' ? `<div class="itr"><label class=sm>Dano ${inp(`inv.items.${i}.arma.dano`, a.dano || '', 'style="width:80px" placeholder=1d8')}</label><label class=sm>Crítico ${inp(`inv.items.${i}.arma.crit`, a.crit || '', 'style="width:90px" placeholder="20 ×2"')}</label><label class=sm>Categoria ${sel(`inv.items.${i}.arma.cat`, [['contundente', 'Contundente'], ['cortante', 'Cortante'], ['arremesso', 'Arremesso'], ['tiro', 'Tiro'], ['especial', 'Especial']], a.cat || 'contundente', 'data-rr')}</label></div>
<div class="itr"><label class=sm>Treino da arma especial ${inp(`inv.items.${i}.arma.fam`, a.fam || '', 'style="width:110px" placeholder="Arco"')}</label></div>` : ''}
${M && tipo == 'armadura' ? `<label class=sm>Reduz dano ${num(`inv.items.${i}.red`, it.red || 0, 'min=0 data-rr')}</label>` : ''}
${M && tipo == 'mochila' ? `<label class=sm>Espaços a mais ${num(`inv.items.${i}.mochila`, it.mochila || 0, 'min=0 data-rr')}</label>` : ''}</details></div>`;
  }

  function vInv(f) {
    const D = ULT, din = f._din, eM = mestre(f), lim = D.slots + 3, pct = lim > 0 ? Math.min(100, D.usado / lim * 100) : 100;
    const estado = D.excesso ? ' — passou do limite: não dá para carregar' : D.sobre ? ' — sobrecarregado (−3 m, desvantagem em Parkour e Furtividade, sem Impulso)' : '';
    return `<section class="card"><h2>Carga e dinheiro</h2><div class="bar"><i style="width:${pct}%;background:${D.excesso ? '#e44' : D.sobre ? '#e8b53a' : 'var(--a)'}"></i></div>
<div class="${D.sobre ? 'over' : 'm'}" id="ct">${n0(D.usado)} / ${D.slots} espaços${estado}</div>
<p class="m" style="font-size:13px;margin:4px 0">Espaços: 5 + 3 por ponto de Corpo a partir do 2${D.C && D.C.id == 'tecnico' ? ', +2 do Técnico' : ''}${D.mochila ? ', +' + n0(D.mochila.mochila) + ' da ' + esc(D.mochila.n) : ''}. Bolso: <b>${D.bolso}</b> itens de tamanho 0 (5 não ocupam espaço${D.espBolso ? '; os outros ocupam ' + D.espBolso : ''}). Itens prontos: <b>${D.prontos}</b> de ${D.prontosMax}. Armadura vestida não ocupa espaço.</p>
<div class="carteira">${din === undefined ? '<span class="m">Dinheiro: peça ao mestre para rodar o SQL da etapa 5.</span>' : eM ? `<label class=sm>Dinheiro (${esc(moeda(f))}) <input type=number data-din value="${n0(din)}" min=0 step="0.01" style="width:110px"></label>` : `<b>${esc(moeda(f))} ${n0(din).toLocaleString('pt-BR', { maximumFractionDigits: 2 })}</b>`}
${f._camp ? `<a class="tl loja-l" href="loja.html?camp=${f._camp}&ficha=${f.id}">Loja</a>` : ''}</div></section>
<section class="card"><h2>Itens</h2>${f.inv.items.map((it, i) => itemCard(f, it, i)).join('') || '<p class=m>Inventário vazio.</p>'}
<div class="g2b"><button class=add data-act=add data-l=items>＋ Item próprio</button><button class=add data-act="sfl-cat" type="button">＋ Do catálogo</button></div></section>
<section class="card"><h2>Fabricar</h2><p class="m" style="font-size:13px;margin:0 0 6px">Gasta 1 hora, os materiais do inventário e um teste (DT da receita). Falhar perde metade dos materiais. Fora da base, receitas químicas pedem kit de química.</p><button class="add" data-act="sfl-fab" type="button">Fabricar um item</button></section>`;
  }

  function vHab(f) {
    const D = ULT, s = f.sfl, C = D.C, O = D.O, L = R.linha(s.linha);
    const hab = (n, d, tag, extra) => `<div class="po"><div class="itr"><b class="in">${esc(n)}</b>${tag ? `<span class="m">${esc(tag)}</span>` : ''}${extra || ''}</div><p class="m" style="margin:2px 0 0">${esc(d)}</p></div>`;
    const escolhidas = s.esc.map((e, i) => {
      const x = `<button class="x" data-act="sfl-esc-x" data-i="${i}" type="button">Remover</button>`;
      return e.k == 'hab' ? hab(e.n, (C && C.habs.find(h => h.n == e.n) || {}).d || '', 'habilidade da classe', x)
        : hab(R.BENEFICIOS.find(b => b[0] == e.k)[1], e.n || '', 'benefício geral', x) });
    return `<section class="card"><h2>Origem e classe</h2>${O ? hab(O.n, O.traco, 'traço da origem') + `<p class="m" style="margin:2px 0 8px"><i>Peso: ${esc(O.peso)}</i></p>` : '<p class="m">Escolha a origem na aba Ficha.</p>'}
${C ? `<p class="m" style="margin:6px 0 2px"><b>Perícias da classe</b> (escolha 2 entre: ${esc(C.pericias.join(', '))}) · bônus: ${esc(C.bonus)}</p><div class="itr">${[0, 1].map(k => sel(`sfl.perClasse.${k}`, [['', '—']].concat(C.pericias.map(p => [p, p])), s.perClasse[k] || '', 'data-rr')).join('')}</div>${hab(C.ini.n, C.ini.d, 'habilidade inicial')}` : ''}</section>
<section class="card"><h2>Trilha${D.trilha ? ': ' + esc(D.trilha.n) : ''}</h2>${D.trilha ? D.trilha.habs.map((h, i) => i < D.nTrilha ? hab(h.n, h.d, 'marco ' + (i * 2 + 1)) : `<div class="po bloq"><p class="m" style="margin:0">🔒 Marco ${i * 2 + 1}: ainda não liberada.</p></div>`).join('') : '<p class="m">A trilha é escolhida no marco 1 (aba Ficha).</p>'}</section>
<section class="card"><h2>Escolhas de marco</h2>${escolhidas.join('') || '<p class="m">Nenhuma escolha ainda. Nos marcos 2, 4, 6 e 8 você escolhe uma habilidade da classe ou um benefício geral.</p>'}
${D.escPend > 0 ? `<button class="add" data-act="sfl-esc" type="button">＋ Fazer uma escolha (${D.escPend} pendente${D.escPend > 1 ? 's' : ''})</button>` : ''}</section>
<section class="card"><h2>Armas especiais treinadas (${s.armas.length}/${D.armasMax} iniciais)</h2><p class="m" style="font-size:13px;margin:0 0 6px">Cada arma especial tem treino próprio; variações (arco curto e composto, besta leve e pesada) dividem o mesmo treino. Sem treino: −1 dado e sem bônus. Treinos extras vêm dos marcos ou da história.</p>
${s.armas.map((a, i) => `<div class="itr"><b class="in">${esc(a.f)}</b>${sel(`sfl.armas.${i}.t`, R.TREINO.filter(x => x[0] > 0), a.t, 'data-n data-rr')}<button class="x" data-act="sfl-arma-x" data-i="${i}" type="button">Remover</button></div>`).join('')}
<button class="add" data-act="sfl-arma" type="button">＋ Treinar arma especial</button></section>
<section class="card"><h2>Linha de poder${L ? ': ' + esc(L.n) : ''}</h2>
<label class=fld>Linha ${sel('sfl.linha', [['', '— escolha —']].concat(R.dados.poderes.map(p => [p.id, p.n])), s.linha, 'data-rr')}</label>
${L ? `<p class="m" style="margin:2px 0 8px">${esc(L.t)}</p>${L.niveis.map(n => { const ok = n.nv <= D.nivelPoder;
      return ok ? `<div class="po"><div class="itr"><b class="in">N${n.nv} ${esc(n.n)}</b><span class="m">Infecção +${n.custo}</span><button class="roll" data-act="sfl-poder" data-nv="${n.nv}" type="button">Usar</button></div><p class="m" style="margin:2px 0 0">${esc(n.d)}</p></div>`
        : `<div class="po bloq"><p class="m" style="margin:0">🔒 Nível ${n.nv}: chega no marco ${n.nv == 2 ? 4 : 8}.</p></div>` }).join('')}
<p class="m" style="font-size:12px;margin:8px 0 0">Todo uso custa Infecção. Infecção 3–5: poderes +2 no teste. 6–8: teste de Vontade DT 18 ao usar (a ficha rola por você). 9–10: o Ódio assume. Poderes nunca zeram de graça: descanso longo baixa 1.</p>` : '<p class="m">Cada jogador escolhe uma linha na criação e começa com o Nível 1.</p>'}</section>`;
  }

  const vNotas = f => vDocsSec(f) + vNotasSec(f);

  /* ---------- atualização sem redesenhar ---------- */
  function derive(f) {
    const D = ULT || calc(f).D;
    f.stats.forEach((s, i) => { const e = document.getElementById('sb' + i); if (e) { e.style.width = (s.max > 0 ? Math.max(0, Math.min(100, s.cur / s.max * 100)) : 0) + '%'; e.style.background = s.c } });
    f.skills.forEach((k, i) => { const at = R.atr(f, k.a), b = n0(k.t) + n0(k.o), t = (at > 0 ? at : 2) + 'd20' + (at > 0 ? '' : '↓') + (b ? ' ' + sinal(b) : ''), e = document.getElementById('sk' + i); if (e) e.textContent = t });
    const set = (k, v) => document.querySelectorAll(`[data-d="${k}"]`).forEach(e => e.textContent = v);
    ['pv', 'pe', 'medo', 'inf'].forEach(id => { const s = f.stats.find(x => x.id == id); if (s) { set('mx-' + id, n0(s.max)); set('max-' + id, 'máx. ' + n0(s.max)) } });
    set('faixa', ' · ' + D.faixa[1]); set('pts', D.pontos);
    const ct = document.getElementById('ct'); if (ct) { ct.textContent = `${n0(D.usado)} / ${D.slots} espaços` + (D.excesso ? ' — passou do limite: não dá para carregar' : D.sobre ? ' — sobrecarregado (−3 m, desvantagem em Parkour e Furtividade, sem Impulso)' : ''); ct.className = D.sobre ? 'over' : 'm' }
  }
  function depois(f, rr) {
    const antes = ss(f.sfl), { msg } = calc(f);
    if (msg.length) toast(msg.map(esc).join(' · '));
    if (rr || msg.length || ss(f.sfl) != antes) return true;
    derive(f); return false;
  }

  /* ---------- rolagens ---------- */
  const rotuloR = f => esc(f.nome || 'Ficha');
  function rola(f, titulo, at, bonus, extra, nota) {
    const r = R.teste(at, VD + n0(extra), bonus), vd = VD + n0(extra);
    toast(`${rotuloR(f)} · ${esc(titulo)}${vd ? (vd > 0 ? ' (vantagem)' : ' (desvantagem)') : ''}: [${r.r}] → ${r.d}${bonus ? ' ' + sinal(bonus) : ''} = <b>${r.total}</b>${nota ? ' · ' + nota : ''}`);
    return r;
  }
  function gasta(f, id, v) { const s = f.stats.find(x => x.id == id); if (!s) return; s.cur = Math.max(0, n0(s.cur) - v); const i = document.querySelector(`[data-p="stats.${f.stats.indexOf(s)}.cur"]`); if (i) i.value = s.cur; touch(f); derive(f) }
  function sobe(f, id, v) { const s = f.stats.find(x => x.id == id); if (!s) return; s.cur = Math.min(n0(s.max), n0(s.cur) + v); const i = document.querySelector(`[data-p="stats.${f.stats.indexOf(s)}.cur"]`); if (i) i.value = s.cur; touch(f); derive(f) }

  function escolher(f) {
    const s = f.sfl, C = ULT.C; if (!C) { toast('Escolha a classe primeiro.'); return }
    const tem = n => s.esc.some(e => e.k == 'hab' && e.n == n);
    janela('Escolha de marco', '<p class="m" style="margin:0">Uma habilidade da classe <b>ou</b> um benefício geral.</p>',
      `<p class="m" style="margin:8px 0 2px"><b>Habilidades de ${esc(C.n)}</b></p>` + C.habs.map(h => botao('h:' + h.n, h.n, h.d, tem(h.n))).join('') +
      '<p class="m" style="margin:8px 0 2px"><b>Benefícios gerais</b></p>' + R.BENEFICIOS.map(b => botao('b:' + b[0], b[1], '', false)).join(''),
      (b, fecha) => { const k = b.dataset.k;
        if (k.startsWith('h:')) { s.esc.push({ k: 'hab', n: k.slice(2) }); fecha(); calc(f); touch(f); render(); return }
        const t = k.slice(2);
        if (t == 'atr') { fecha(); janela('Qual atributo?', '', R.ATR.map(([id, n]) => botao(id, n, 'valor atual ' + R.atr(f, id), R.atr(f, id) >= 5)).join(''), (b2, f2) => { const i = idxAt(f, b2.dataset.k); f.attrs[i].v = n0(f.attrs[i].v) + 1; s.esc.push({ k: 'atr', n: b2.dataset.k }); f2(); calc(f); touch(f); render() }); return }
        if (t == 'per') { fecha(); janela('Qual perícia?', '', f.skills.map((k2, i) => botao(String(i), k2.n, R.TREINO.find(x => x[0] == k2.t)[1], n0(k2.t) >= 9)).join(''), (b2, f2) => { const k2 = f.skills[+b2.dataset.k]; k2.t = n0(k2.t) + 3; s.esc.push({ k: 'per', n: k2.n }); f2(); calc(f); touch(f); render() }); return }
        if (t == 'arma') { fecha(); trocarArma(f, true); return }
        if (t == 'vida') { const v = R.atr(f, 'cor'); s.esc.push({ k: 'vida', n: String(v) }); fecha(); calc(f); touch(f); render(); toast(`+${v} de Vida máxima.`); return } });
  }
  function trocarArma(f, viaMarco) {
    const s = f.sfl;
    janela('Arma especial', '<p class="m" style="margin:0">Treino próprio para cada arma. Arco curto e composto dividem o mesmo treino; besta leve e pesada também.</p>',
      R.ESPECIAIS.map(n => botao(n, n, s.armas.some(a => a.f == n) ? 'já treinada: sobe um nível' : 'treino +3', false)).join(''),
      (b, fecha) => { const n = b.dataset.k, a = s.armas.find(x => x.f == n);
        if (a) { if (n0(a.t) >= 9) { toast('Já é expert.'); return } a.t = n0(a.t) + 3 } else s.armas.push({ f: n, t: 3 });
        if (viaMarco) s.esc.push({ k: 'arma', n }); fecha(); calc(f); touch(f); render() });
  }
  function catalogo(f) {
    const o = janela('Catálogo', '<input id="catq" placeholder="Buscar" style="width:100%">', R.GRUPOS.map(([t, l]) => `<p class="m cat-g" style="margin:8px 0 2px"><b>${l}</b></p>` + R.CAT.map((it, i) => [it, i]).filter(([it]) => it.tipo == t)
      .map(([it, i]) => botao(String(i), it.n, [it.arma ? it.arma.dano + ' · crít. ' + it.arma.crit : it.desc || ''].concat(R.etiquetas(it)).filter(Boolean).join(' · '), false)).join('')).join(''),
      (b, fecha) => { const c = R.CAT[+b.dataset.k], it = R.poeItem(f, c.n, n0(c.lote || 1));
        if (it.tipo == 'mochila' && !f.inv.items.some(x => x !== it && x.tipo == 'mochila' && x.eq)) it.eq = true;
        fecha(); calc(f); touch(f); render(); toast(esc(c.n) + ' adicionado.') });
    o.oninput = e => { const q = R.norm(e.target.value); o.querySelectorAll('.cat-i').forEach(b => b.style.display = R.norm(b.textContent).includes(q) ? '' : 'none') };
  }
  const cDT = (f, per) => { const k = f.skills.find(x => x.n == per); return { at: R.atr(f, k ? k.a : 'men'), b: R.treinoDe(f, per) } };
  /* pergunta onde a ação acontece: na base (oficina) ou fora */
  function ondeFaz(titulo, txtBase, txtFora, ok) {
    janela(titulo, '', botao('base', 'Na oficina da base', txtBase, false) + botao('fora', 'Fora da base', txtFora, false), (b, fecha) => { fecha(); ok(b.dataset.k == 'base') });
  }
  function modificar(f, i) {
    const it = f.inv.items[i], lim = R.limiteMods(it), M = it.mods || [], cheio = M.length >= lim;
    janela('Modificar: ' + (it.n || 'arma'), `<p class="m" style="margin:0">Limite desta arma: <b>${lim}</b> (tem ${M.length}). Cada modificação entra uma vez. Instalar leva 1 hora: na oficina da base sem teste; fora da base, Técnica DT 15 e kit de ferramentas.</p>`,
      R.modsPossiveis(it).map(m => { const falta = R.faltaMat(f, m.mat), ja = M.includes(m.id);
        return botao(m.id, m.n, `${m.d} · materiais: ${Object.entries(m.mat).map(([k, q]) => q + ' ' + k.split('|').join(' ou ')).join(', ')}${ja ? ' · já instalada' : falta.length ? ' · faltam ' + falta.join(', ') : ''}`, ja || cheio || (falta.length && !podeMec(f))) }).join('') || '<p class="m">Nenhuma modificação serve nesta arma.</p>',
      (b, fecha) => { const m = R.dados.mods.find(x => x.id == b.dataset.k), falta = R.faltaMat(f, m.mat); fecha();
        const instala = gasta => { if (gasta) R.gastaMat(f, m.mat); const alvo = f.inv.items.find(x => x === it); if (!alvo) return; alvo.mods = (alvo.mods || []).concat(m.id); calc(f); touch(f); render(); toast(`${esc(m.n)} instalada em ${esc(it.n)}.${gasta ? '' : ' (sem gastar materiais)'}`) };
        if (falta.length) { if (confirm(`Faltam ${falta.join(', ')}. Instalar mesmo assim, sem gastar materiais? (só o mestre)`)) instala(false); return }
        ondeFaz('Onde vai instalar?', 'Sem teste.', 'Técnica DT 15; precisa de kit de ferramentas.', base => {
          if (base) return instala(true);
          if (!R.temMat(f, 'Kit de ferramentas')) { toast('Fora da base precisa de um <b>kit de ferramentas</b> no inventário.'); return }
          const c = cDT(f, 'Técnica'), r = rola(f, 'Técnica (instalar ' + m.n + ')', c.at, c.b, 0, 'DT 15');
          if (r.total >= 15) instala(true); else toast(`Técnica ${r.total}: não conseguiu instalar ${esc(m.n)} (DT 15). Os materiais ficam; dá para tentar de novo.`) }) });
  }
  function fabricar(f) {
    janela('Fabricar', '<p class="m" style="margin:0">Escolha a receita. A ficha confere e gasta os materiais do inventário.</p>',
      R.dados.receitas.map((r, k) => { const falta = R.faltaMat(f, r.mat);
        return botao(String(k), r.n + (r.q > 1 ? ' (' + r.q + ')' : ''), `${Object.entries(r.mat).map(([m, q]) => q + ' ' + m).join(', ')} · ${r.dt ? r.per.join(' ou ') + ' DT ' + r.dt : 'sem teste'}${r.quim ? ' · química' : ''}${r.nota ? ' · ' + r.nota : ''}${falta.length ? ' · faltam ' + falta.join(', ') : ''}`, falta.length > 0) }).join(''),
      (b, fecha) => { const r = R.dados.receitas[+b.dataset.k]; fecha();
        const faz = base => {
          if (!base && r.quim && !R.temMat(f, 'Kit de química')) { toast('Receita química fora da base precisa de um <b>kit de química</b>.'); return }
          if (!r.dt) { R.gastaMat(f, r.mat); R.poeItem(f, r.n, r.q); calc(f); touch(f); render(); toast(`Fabricou ${esc(r.n)}.`); return }
          const per = r.per.slice().sort((x, y) => R.treinoDe(f, y) - R.treinoDe(f, x))[0], c = cDT(f, per), x = rola(f, per + ' (fabricar ' + r.n + ')', c.at, c.b, 0, 'DT ' + r.dt);
          if (x.total >= r.dt) { R.gastaMat(f, r.mat); R.poeItem(f, r.n, r.q); toast(`${esc(per)} ${x.total} (DT ${r.dt}): fabricou <b>${esc(r.n)}${r.q > 1 ? ' ×' + r.q : ''}</b>.`) }
          else { R.gastaMat(f, r.mat, 0.5); let t2 = `${esc(per)} ${x.total} (DT ${r.dt}): falhou e perdeu metade dos materiais.`;
            if (r.explode && r.dt - x.total >= 5) { const dn = 1 + Math.floor(Math.random() * 6); gasta(f, 'pv', dn); t2 += ` <b>Explodiu na mão: ${dn} de dano.</b>` }
            toast(t2) }
          calc(f); touch(f); render() };
        ondeFaz('Onde vai fabricar?', 'Na oficina da base.', r.quim ? 'Precisa de kit de química.' : 'Mesmo teste.', faz) });
  }
  function usar(f, i) {
    const it = f.inv.items[i], s = f.sfl, q = n0(it.qtd === undefined ? 1 : it.qtd); if (q <= 0) { toast('Acabou.'); return }
    const menos = () => { if (it.usos !== undefined) { it.usos = n0(it.usos) - 1; if (it.usos <= 0) { it.qtd = q - 1; it.usos = q - 1 > 0 ? 5 : 0 } } else it.qtd = q - 1;
      if (n0(it.qtd) <= 0) f.inv.items.splice(f.inv.items.indexOf(it), 1) };
    const fim = t2 => { calc(f); touch(f); render(); toast(t2) };
    if (it.uso == 'bandagem' || it.uso == 'kit') {
      const c = cDT(f, 'Medicina'), r = rola(f, 'Medicina (' + it.n + ')', c.at, c.b, it.uso == 'kit' ? 1 : 0, 'DT 15'); menos();
      if (r.total < 15) return fim(`Medicina ${r.total} (DT 15): não fez efeito. ${esc(it.n)} gasto.`);
      let cura = 1 + Math.floor(Math.random() * (R.tem(f, 'Remendo') ? 6 : 4)); if (s.origem == 'veterinario') cura = Math.max(0, cura - 1);
      sobe(f, 'pv', cura);
      return fim(`Medicina ${r.total}: <b>+${cura} Vida</b>${R.tem(f, 'Remendo') ? ' (Remendo: 1d6)' : ''}${s.origem == 'veterinario' ? ' (Veterinário: −1 em humanos)' : ''}; para o sangramento${it.uso == 'kit' ? ' (qualquer sangramento)' : ''}. Uma vez por ferimento. Se foi em outra pessoa, tire a Vida que subiu aqui e ajuste a dela.`) }
    if (it.uso == 'adrenalina') { menos(); s.adren = n0(s.adren) + 1; calc(f); sobe(f, 'pe', 3); return fim('Adrenalina: <b>+3 Fôlego</b> agora; −1 de Fôlego máximo até o descanso longo.') }
    if (it.uso == 'estabilizador') { const hoje = new Date().toISOString().slice(0, 10);
      if (s.estabDia == hoje && !confirm('Só 1 estabilizador por dia. Usar outro mesmo assim? (o mestre decide)')) return;
      menos(); s.estabDia = hoje; gasta(f, 'inf', 2); return fim('Estabilizador: <b>Infecção −2</b>. Só 1 por dia.') }
    if (it.uso == 'analgesico') { menos(); return fim('Analgésico: por uma cena ignora desvantagens de dor e ganha 2 PV temporários.') }
    menos(); fim(`${esc(it.n)} usado.${/ra[cç][aã]o|água/i.test(it.n || '') ? ' Um dia de ' + (/água/i.test(it.n) ? 'água' : 'comida') + '.' : ''}`);
  }
  function parkour(f) {
    const D = ULT, s = f.sfl;
    const o = janela('Teste de Parkour', `<p class="m" style="margin:0">Reflexo ${R.atr(f, 'ref')}d20 + Parkour ${sinal(R.treinoDe(f, 'Parkour'))}${s.pers ? ' · em perseguição (estágio ' + s.pers + ')' : ''}${s.impVant && D.impulso == 3 ? ' · Impulso 3: vantagem' : ''}.</p>
<label class="sm"><input type="checkbox" id="pkseq"> Sequência complexa (+2 na DT)</label> <label class="sm"><input type="checkbox" id="pkexi"> Esforço extra (+1 Fôlego)</label>
<div class="itr"><label class="sm">Outra DT <input type="number" id="pkdt" value="15" min="0" style="width:70px"></label><label class="sm">Fôlego <input type="number" id="pkfo" value="1" min="0" style="width:60px"></label></div><button class="cat-i" data-k="x"><b>Rolar com a DT acima</b><small>obstáculo que o mestre descreveu</small></button>`,
      R.MOVIMENTOS.map((m, k) => botao(String(k), m[0], m[1] ? `DT ${m[1]} · Fôlego ${m[2]}` : 'automático', false)).join(''),
      (b, fecha) => { const k = b.dataset.k, g = id => o.querySelector('#' + id);
        let dt, fo, nome; if (k == 'x') { dt = n0(g('pkdt').value); fo = n0(g('pkfo').value); nome = 'Obstáculo' } else { [nome, dt, fo] = R.MOVIMENTOS[+k] }
        if (g('pkseq').checked) dt += 2; if (g('pkexi').checked) fo += 1; fecha();
        if (!dt) { toast(`${esc(nome)}: automático, sem teste.`); return }
        const desv = R.desvAuto(f, D, 'Parkour'), vant = s.impVant && D.impulso == 3 ? 1 : 0;
        if (vant) s.impVant = false;
        const r = rola(f, 'Parkour: ' + nome, R.atr(f, 'ref'), R.treinoDe(f, 'Parkour'), (desv.length ? -1 : 0) + vant, `DT ${dt}${desv.length ? ' · desvantagem: ' + desv.join(', ') : ''}${vant ? ' · vantagem do Impulso' : ''}`);
        const res = R.parkourResultado(r.total, dt), custo = fo + (res.k == 1 ? 1 : 0);
        if (custo) gasta(f, 'pe', custo);
        let t2 = `Parkour ${r.total} (DT ${dt}): ${res.t}${custo ? ' Fôlego −' + custo + '.' : ''}`;
        if (s.pers) {
          if (res.k == 0) { if (!D.sobre && s.impulso < 3) { s.impulso++; if (s.impulso == 3) s.impVant = true } s.pers = Math.min(6, s.pers + 1); t2 += ` Impulso ${D.sobre ? '0 (sobrecarregado)' : s.impulso}; perseguição: ${R.ESTAGIOS[s.pers]}${s.pers == 6 ? ' (rompa o contato para fugir de vez)' : ''}.` }
          else if (res.k >= 2) { s.impulso = 0; s.impVant = false; s.pers = Math.max(1, s.pers - 1); t2 += ` Impulso zerado; perseguição: ${R.ESTAGIOS[s.pers]}.` }
        }
        calc(f); touch(f); render(); toast(t2) });
  }
  function descanso(f, tipo) {
    const s = f.sfl, st = id => f.stats.find(x => x.id == id);
    if (tipo == 'curto') { const fo = st('pe'); fo.cur = n0(fo.max); calc(f); touch(f); render(); toast('Descanso curto: Fôlego cheio.'); return }
    const cura = 1 + Math.floor(Math.random() * 6) + R.atr(f, 'cor'); s.adren = 0; s.impulso = 0; s.pers = 0; calc(f);
    const pv = st('pv'), m = st('medo'), inf = st('inf'), fo = st('pe');
    pv.cur = Math.min(n0(pv.max), n0(pv.cur) + cura); m.cur = Math.max(0, n0(m.cur) - 2); inf.cur = Math.max(0, n0(inf.cur) - 1); fo.cur = n0(fo.max);
    calc(f); touch(f); render(); toast(`Descanso longo: <b>+${cura} Vida</b> (1d6 + Corpo), Medo −2, Infecção −1. Fôlego cheio.`);
  }

  async function acao(a, d, f) {
    const s = f.sfl;
    if (a == 'sfl-vd') { VD = +d.v; render(); return true }
    if (a == 'sfl-marco') { s.marco = Math.max(0, Math.min(8, s.marco + +d.d)); calc(f); touch(f); render(); toast(`Marco ${s.marco}.`); return true }
    if (a == 'sfl-esc') { escolher(f); return true }
    if (a == 'sfl-esc-x') { const e = s.esc[+d.i]; if (!e) return true;
      if (e.k == 'atr') { const i = idxAt(f, e.n); f.attrs[i].v = Math.max(0, n0(f.attrs[i].v) - 1) }
      if (e.k == 'per') { const k = f.skills.find(x => x.n == e.n); if (k) k.t = Math.max(0, n0(k.t) - 3) }
      if (e.k == 'arma') { const x = s.armas.find(y => y.f == e.n); if (x) { x.t = n0(x.t) - 3; if (x.t < 3) s.armas = s.armas.filter(y => y !== x) } }
      s.esc.splice(+d.i, 1); calc(f); touch(f); render(); return true }
    if (a == 'sfl-arma') { trocarArma(f, false); return true }
    if (a == 'sfl-arma-x') { s.armas.splice(+d.i, 1); calc(f); touch(f); render(); return true }
    if (a == 'sfl-cat') { catalogo(f); return true }
    if (a == 'sfl-eq') { const it = f.inv.items[+d.i]; it.eq = !it.eq;
      if (it.eq && (it.tipo == 'armadura' || it.tipo == 'mochila')) f.inv.items.forEach(o => { if (o !== it && o.tipo == it.tipo && o.eq && ((o.sub == 'escudo') == (it.sub == 'escudo'))) o.eq = false });
      calc(f); touch(f); render(); return true }
    if (a == 'sfl-pronto') { const it = f.inv.items[+d.i]; it.pronto = !it.pronto; calc(f); touch(f); render();
      if (it.pronto && ULT.prontos > ULT.prontosMax) toast(`Itens prontos: ${ULT.prontos} de ${ULT.prontosMax}. Bolsa de cintura, coldre e mochila militar dão mais.`); return true }
    if (a == 'sfl-quebra') { const it = f.inv.items[+d.i]; if (it) { it.quebrada = true; it.pronto = it.pronto; calc(f); touch(f); render(); toast(esc(it.n) + ' quebrou. As modificações ficam; voltam ao consertar.') } return true }
    if (a == 'sfl-conserta') { const it = f.inv.items[+d.i]; if (!it) return true;
      if (R.tem(f, 'Reparo rápido')) { it.quebrada = false; calc(f); touch(f); render(); toast(`Reparo rápido: ${esc(it.n)} consertada (ação de movimento, sem teste).`); return true }
      const c = cDT(f, 'Técnica'), r = rola(f, 'Técnica (consertar ' + it.n + ')', c.at, c.b, 0, 'DT 15');
      if (r.total >= 15) { it.quebrada = false; calc(f); touch(f); render(); toast(`Técnica ${r.total}: ${esc(it.n)} consertada.`) } else toast(`Técnica ${r.total}: não conseguiu consertar (DT 15).`); return true }
    if (a == 'sfl-mod') { modificar(f, +d.i); return true }
    if (a == 'sfl-modx') { const it = f.inv.items[+d.i], m = R.dados.mods.find(x => x.id == d.m); if (!it || !m) return true;
      it.mods = (it.mods || []).filter(x => x != m.id); Object.entries(m.mat).forEach(([k, q]) => { const v = Math.floor(q / 2); if (v && !k.includes('|')) R.poeItem(f, k, v) });
      calc(f); touch(f); render(); toast(`${esc(m.n)} removida. Volta metade dos materiais.`); return true }
    if (a == 'sfl-usar') { usar(f, +d.i); return true }
    if (a == 'sfl-fab') { fabricar(f); return true }
    if (a == 'sfl-pk') { parkour(f); return true }
    if (a == 'sfl-imp') { if (ULT.sobre && +d.d > 0) { toast('Sobrecarregado não ganha Impulso.'); return true } const v = Math.max(0, Math.min(3, s.impulso + +d.d)); if (v == 3 && s.impulso < 3) s.impVant = true; if (v < 3) s.impVant = false; s.impulso = v; calc(f); touch(f); render(); return true }
    if (a == 'sfl-pers') { if (d.d == 'ini') s.pers = 3; else if (d.d == '0') { s.pers = 0; s.impulso = 0; s.impVant = false } else s.pers = Math.max(1, Math.min(6, s.pers + +d.d)); calc(f); touch(f); render(); return true }
    if (a == 'sfl-desc') { descanso(f, d.t); return true }
    if (a == 'sfl-ini') { rola(f, 'Iniciativa', R.atr(f, 'ref'), 0, s.classe == 'batedor' ? 1 : 0, s.classe == 'batedor' ? 'Batedor: +1 dado' : ''); return true }
    if (a == 'sfl-esq') { const b = Math.max(R.treinoDe(f, 'Parkour'), R.treinoDe(f, 'Atletismo')), fol = f.stats.find(x => x.id == 'pe');
      if (fol && n0(fol.cur) < 1) toast('Sem Fôlego para esquivar.'); else gasta(f, 'pe', 1); rola(f, 'Esquiva', R.atr(f, 'ref'), b, 0, '−1 Fôlego'); return true }
    if (a == 'sfl-blq') { const b = Math.max(R.treinoDe(f, 'Contundente'), R.treinoDe(f, 'Cortante')), B = bloqueioCom(f), r = rola(f, 'Bloqueio', R.atr(f, 'cor'), b, B.dado);
      const ix = B.it ? f.inv.items.indexOf(B.it) : -1;
      toast(`Bloqueio ${r.total} ${esc(B.rot)}: bloqueia <b>${Math.floor(r.total / B.div)}</b> de dano. A armadura reduz o resto.${r.d == 1 && ix >= 0 ? ` <b>1 natural:</b> se o bloqueio falhou, ${esc(B.it.n)} quebra. <button class="mini" data-act="sfl-quebra" data-i="${ix}">Marcar quebrada</button>` : ''}`); return true }
    if (a == 'sfl-ctr') { const b = Math.max(R.treinoDe(f, 'Contundente'), R.treinoDe(f, 'Cortante')); rola(f, 'Contra-ataque', R.atr(f, 'cor'), b, 0, 'se vencer o atacante, evita o golpe e causa dano'); return true }
    if (a == 'sfl-atk') { const it = itemDe(f, d.i); if (!it) return true; if (it.quebrada) { toast(esc(it.n) + ' está quebrada. Conserte antes.'); return true }
      const at = R.ataque(f, it, !!d.mira), medo = n0((f.stats.find(x => x.id == 'medo') || {}).cur), dist = !at.melee && medo >= 3 ? -1 : 0;
      const r = R.teste(Math.max(0, at.dados), VD + dist, at.bonus), crit = at.crit && r.d >= at.crit.m, nat1 = r.d == 1;
      let x = `${rotuloR(f)} · ${esc(it.n)} (${esc(at.rotulo)}${d.mira ? ', mirando' : ''}): [${r.r}] → ${r.d}${at.bonus ? ' ' + sinal(at.bonus) : ''} = <b>${r.total}</b>${at.treinada ? '' : ' · sem treino'}${at.mira ? ' · mira +1 dado' : ''}${dist ? ' · Medo 3+: desvantagem' : ''}`;
      if (crit) x += ` · <b>CRÍTICO ×${at.crit.x}</b> (se acertar${at.fx.length ? ': ' + esc(at.fx.join('; ')) : ''})`;
      if (nat1 && at.quebra) x += ` · <b>1 natural:</b> se o ataque falhou, a arma quebra. <button class="mini" data-act="sfl-quebra" data-i="${d.i}">Marcar quebrada</button>`;
      if (nat1 && /explode na mão em 1 natural/i.test((it.arma || {}).traco || '')) x += ' · <b>1 natural: explode na mão!</b>';
      toast(x); return true }
    if (a == 'sfl-dano') { const it = itemDe(f, d.i), r = R.danoRolar(f, it, !!d.c);
      toast(r ? `${rotuloR(f)} · ${esc(it.n)} dano${d.c ? ' crítico ×' + r.mult : ''}: [${r.r}]${r.fixo ? ' ' + sinal(r.fixo) : ''}${r.corpo ? ' +' + r.corpo + ' (Corpo)' : ''} = <b>${r.soma}</b>` : 'Preencha o dano da arma (ex.: 1d8).'); return true }
    if (a == 'sfl-poder') { const L = R.linha(s.linha), n = L && L.niveis.find(x => x.nv == +d.nv); if (!n) return true;
      const inf = f.stats.find(x => x.id == 'inf'); inf.cur = Math.min(n0(inf.max), n0(inf.cur) + n.custo); const i = document.querySelector(`[data-p="stats.${f.stats.indexOf(inf)}.cur"]`); if (i) i.value = inf.cur;
      touch(f); calc(f); derive(f);
      const fx = R.faixaInf(n0(inf.cur));
      let t = `${esc(n.n)}: Infecção +${n.custo} (agora ${inf.cur}, ${esc(fx[1])})`;
      if (fx[1] == 'Inquieto') t += ' · poder +2 no teste';
      if (fx[1] == 'Instável') { const r = R.teste(R.atr(f, 'pre'), VD, R.treinoDe(f, 'Vontade')); t += ` · Vontade DT 18: [${r.r}] → ${r.d}${R.treinoDe(f, 'Vontade') ? ' ' + sinal(R.treinoDe(f, 'Vontade')) : ''} = <b>${r.total}</b> ${r.total >= 18 ? '(mantém o controle)' : '(PERDE O CONTROLE por uma cena)'}` }
      if (fx[1] == 'Limiar') t += ' · <b>O Ódio assume.</b> O mestre conduz.';
      toast(t); render(); return true }
    return false;
  }

  /* mudar dinheiro (só mestre) */
  async function dinheiro(f, v) {
    const { data, error } = await db.from('personagens').update({ dinheiro: Math.max(0, n0(v)) }).eq('id', f.id).select('dinheiro');
    if (error || !data || !data.length) { toast('Não consegui mudar o dinheiro: ' + esc(error ? error.message : 'sem permissão')); return }
    f._din = +data[0].dinheiro; status('salvo ✓');
  }

  /* rolagem de perícia da ficha (botão Rolar) */
  function rolarPericia(f, i) {
    const k = f.skills[i], at = R.atr(f, k.a), b = n0(k.t) + n0(k.o), L = R.desvAuto(f, ULT || calc(f).D, k.n);
    rola(f, k.n, at, b, L.length ? -1 : 0, L.length ? 'desvantagem: ' + L.join(', ') : '');
  }

  window.SFL = { TABS, views: { g: vFicha, c: vCombate, p: vPericias, i: vInv, h: vHab, n: vNotas }, calc, derive, depois, acao, dinheiro, podeMec, mestre, rolarPericia };
})();
