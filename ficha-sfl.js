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
    if (!s.origem) L.push('Escolha a <b>origem</b> (a vida até os 25 anos).');
    if (s.classe && s.perClasse.length < 2) L.push(`Escolha <b>2 perícias</b> da classe (${s.perClasse.length}/2).`);
    if (s.classe && s.marco >= 1 && !s.trilha) L.push('O marco 1 chegou: escolha a <b>trilha</b>.');
    if (D.escPend > 0) L.push(`Você tem <b>${D.escPend}</b> escolha${D.escPend > 1 ? 's' : ''} de marco (habilidade da classe ou benefício geral). <button class="mini" data-act="sfl-esc" type="button">Escolher</button>`);
    if (s.armas.length < D.armasMax && s.classe) L.push(`Treine sua <b>arma especial</b> inicial na aba Habilidades (${s.armas.length}/${D.armasMax}).`);
    if (!s.linha) L.push('Escolha sua <b>linha de poder</b> na aba Habilidades.');
    if (D.pontos > D.pontosMax) L.push(`Atributos: ${D.pontos} pontos usados, o limite é ${D.pontosMax}.`);
    if (f.attrs.some(a => n0(a.v) > 5)) L.push('Atributo máximo é 5.');
    if (D.sobre) L.push('Inventário acima da capacidade: carga demais.');
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
<div class="selos"><div class="selo"><b>${D.pvMax}</b><small>Vida</small></div><div class="selo"><b>${D.folMax}</b><small>Fôlego</small></div><div class="selo"><b data-d="arm">${D.armadura}</b><small>Armadura</small></div><div class="selo"><b>${D.slots}</b><small>Espaços</small></div></div>
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

  function vCombate(f) {
    const D = ULT, s = f.sfl, its = f.inv.items, armas = its.map((it, i) => [it, i]).filter(([it]) => it.tipo == 'arma' && n0(it.qtd === undefined ? 1 : it.qtd) > 0);
    const ref = R.atr(f, 'ref'), cor = R.atr(f, 'cor');
    return `<section class="card"><h2>Rolagens</h2>${vdBar()}
<div class="res"><button class="btn-res" data-act="sfl-ini" type="button"><b>Iniciativa</b><small>${ref + (s.classe == 'batedor' ? 1 : 0)}d20</small></button>
<button class="btn-res" data-act="sfl-esq" type="button"><b>Esquiva</b><small>${ref}d20 ${sinal(Math.max(R.treinoDe(f, 'Parkour'), R.treinoDe(f, 'Atletismo')))} · −1 Fôlego</small></button>
<button class="btn-res" data-act="sfl-blq" type="button"><b>Bloqueio</b><small>${cor}d20 ${sinal(Math.max(R.treinoDe(f, 'Contundente'), R.treinoDe(f, 'Cortante')))}</small></button>
<button class="btn-res" data-act="sfl-ctr" type="button"><b>Contra-ataque</b><small>${cor}d20 ${sinal(Math.max(R.treinoDe(f, 'Contundente'), R.treinoDe(f, 'Cortante')))}</small></button></div>
<p class="m" style="font-size:12px;margin:8px 0 0">Não existe Defesa fixa: quem é atacado rola a reação. Armadura equipada reduz <b>${D.armadura}</b> de dano${D.armaduraNome ? ' (' + esc(D.armaduraNome) + ')' : ''}.</p></section>
<section class="card"><h2>Ataques</h2>${armas.map(([it, i]) => { const a = it.arma || {}, at = R.ataque(f, it);
      return `<div class="arma"><div class="ar-n"><b>${esc(it.n || 'Arma')}</b><small>${esc([a.dano && 'dano ' + a.dano + (at.melee ? ' +Corpo' : ''), a.crit && 'crít. ' + a.crit, a.traco && a.traco != 'n/a' ? a.traco : '', a.efeito && a.efeito != 'n/a' ? 'crít.: ' + a.efeito : ''].filter(Boolean).join(' · '))}${at.treinada ? '' : ' · SEM TREINO (−1 dado)'}</small></div>
<button class="roll" data-act="sfl-atk" data-i="${i}" title="Atacar (${esc(at.rotulo)})">Atacar</button><button class="mini" data-act="sfl-dano" data-i="${i}">Dano</button><button class="mini" data-act="sfl-dano" data-i="${i}" data-c="1">Dano crít.</button></div>` }).join('') || '<p class="m">Nenhuma arma no inventário. Adicione em <b>Inventário</b>.</p>'}
<p class="m" style="font-size:12px;margin:8px 0 0">Crítico é tirar um número alto no dado, e nem todo crítico acerta: o ataque ainda precisa vencer a reação. No crítico que acerta, o efeito da arma acontece e os dados de dano são multiplicados.</p></section>`;
  }

  function vPericias(f) {
    return `<section class="card per-sec"><h2>Perícias</h2>${vdBar()}<p class="m" style="margin:0 0 8px;font-size:13px">Role o número do atributo em d20 e fique com o maior. O atributo não soma: só o treino. Perícias de origem e classe nascem treinadas.</p>
${f.skills.map((k, i) => `<div class="sk"><button class="roll" data-act="roll" data-i="${i}" title="Rolar">Rolar</button><span class="sn">${esc(k.n)}${ULT.fonte.has(k.n) ? ' <small class="m">(origem/classe)</small>' : ''}</span><select data-p="skills.${i}.t" data-n title="Treino">${R.TREINO.map(([v, l]) => `<option value=${v} ${k.t == v ? 'selected' : ''}>${l}</option>`).join('')}</select><select data-p="skills.${i}.a" title="Atributo">${attrOpts(f, k.a)}</select><b id="sk${i}"></b></div>`).join('')}
</section>`;
  }

  function itemCard(f, it, i) {
    const M = podeMec(f), tipo = it.tipo || 'geral', eqv = tipo == 'arma' || tipo == 'armadura', a = it.arma || {};
    return `<div class="it op-it ${it.eq ? 'eq' : ''}"><div class="itr">${inp(`inv.items.${i}.n`, it.n, 'placeholder="Nome do item" class=in')}${eqv ? `<button class="eqb ${it.eq ? 'on' : ''}" data-act="sfl-eq" data-i="${i}">${it.eq ? 'Equipado' : 'Equipar'}</button>` : ''}<button class=x data-act=del data-l=items data-i=${i}>Remover</button></div>
<div class="itr"><label class=sm>Quantidade${num(`inv.items.${i}.qtd`, it.qtd === undefined ? 1 : it.qtd, 'min=0 data-rr')}</label><label class=sm>Espaços${num(`inv.items.${i}.esp`, it.esp, 'min=0 step=.5 data-rr' + (M ? '' : ' disabled'))}</label>
<label class=sm>Tipo ${sel(`inv.items.${i}.tipo`, [['geral', 'Geral'], ['arma', 'Arma'], ['armadura', 'Armadura'], ['consumivel', 'Consumível']], tipo, 'data-rr' + (M ? '' : ' disabled'))}</label></div>
${tipo == 'arma' ? `<p class="m it-res">${esc([a.dano, a.crit && 'crít. ' + a.crit, a.traco && a.traco != 'n/a' ? a.traco : '', a.efeito && a.efeito != 'n/a' ? 'efeito no crítico: ' + a.efeito : ''].filter(Boolean).join(' · '))}</p>` : ''}
${tipo == 'armadura' ? `<p class="m it-res">Reduz ${n0(it.red)} de dano</p>` : ''}
${inp(`inv.items.${i}.desc`, it.desc || '', 'placeholder="Descrição e notas"')}
${M && tipo == 'arma' ? `<details class="mec"><summary>Regras da arma</summary><div class="itr"><label class=sm>Dano ${inp(`inv.items.${i}.arma.dano`, a.dano || '', 'style="width:80px" placeholder=1d8')}</label><label class=sm>Crítico ${inp(`inv.items.${i}.arma.crit`, a.crit || '', 'style="width:90px" placeholder="20 ×2"')}</label><label class=sm>Categoria ${sel(`inv.items.${i}.arma.cat`, [['contundente', 'Contundente'], ['cortante', 'Cortante'], ['arremesso', 'Arremesso'], ['tiro', 'Tiro'], ['especial', 'Especial']], a.cat || 'contundente', 'data-rr')}</label></div>
<div class="itr"><label class=sm>Treino da arma especial ${inp(`inv.items.${i}.arma.fam`, a.fam || '', 'style="width:110px" placeholder="Arco"')}</label></div></details>` : ''}
${M && tipo == 'armadura' ? `<details class="mec"><summary>Regras da armadura</summary><label class=sm>Reduz dano ${num(`inv.items.${i}.red`, it.red || 0, 'min=0 data-rr')}</label></details>` : ''}</div>`;
  }

  function vInv(f) {
    const D = ULT, din = f._din, eM = mestre(f), pct = D.slots > 0 ? Math.min(100, D.usado / D.slots * 100) : 100;
    return `<section class="card"><h2>Carga e dinheiro</h2><div class="bar"><i style="width:${pct}%;background:${D.sobre ? '#e44' : 'var(--a)'}"></i></div>
<div class="${D.sobre ? 'over' : 'm'}" id="ct">${n0(D.usado)} / ${D.slots} espaços${D.sobre ? ' — sobrecarregado' : ''}</div>
<div class="carteira">${din === undefined ? '<span class="m">Dinheiro: peça ao mestre para rodar o SQL da etapa 5.</span>' : eM ? `<label class=sm>Dinheiro (${esc(moeda(f))}) <input type=number data-din value="${n0(din)}" min=0 step="0.01" style="width:110px"></label>` : `<b>${esc(moeda(f))} ${n0(din).toLocaleString('pt-BR', { maximumFractionDigits: 2 })}</b>`}
${f._camp ? `<a class="tl loja-l" href="loja.html?camp=${f._camp}&ficha=${f.id}">Loja</a>` : ''}</div></section>
<section class="card"><h2>Itens</h2>${f.inv.items.map((it, i) => itemCard(f, it, i)).join('') || '<p class=m>Inventário vazio.</p>'}
<div class="g2b"><button class=add data-act=add data-l=items>＋ Item próprio</button><button class=add data-act="sfl-cat" type="button">＋ Do catálogo</button></div></section>`;
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
    const ct = document.getElementById('ct'); if (ct) { ct.textContent = `${n0(D.usado)} / ${D.slots} espaços` + (D.sobre ? ' — sobrecarregado' : ''); ct.className = D.sobre ? 'over' : 'm' }
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
    const abas = [['arma', 'Armas'], ['armadura', 'Armaduras'], ['geral', 'Equipamento'], ['consumivel', 'Consumíveis']];
    janela('Catálogo', '', abas.map(([t, l]) => `<p class="m" style="margin:8px 0 2px"><b>${l}</b></p>` + R.CAT.map((it, i) => [it, i]).filter(([it]) => it.tipo == t).map(([it, i]) => botao(String(i), it.n, (it.arma ? it.arma.dano + ' · crít. ' + it.arma.crit : it.desc || ''), false)).join('')).join(''),
      (b, fecha) => { const it = JSON.parse(JSON.stringify(R.CAT[+b.dataset.k])); it.id = S.uid(); it.eq = false; f.inv.items.push(it); fecha(); calc(f); touch(f); render(); toast(esc(it.n) + ' adicionado.') });
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
      if (it.eq && it.tipo == 'armadura') f.inv.items.forEach(o => { if (o !== it && o.tipo == 'armadura' && o.eq && ((o.sub == 'escudo') == (it.sub == 'escudo'))) o.eq = false });
      calc(f); touch(f); render(); return true }
    if (a == 'sfl-ini') { rola(f, 'Iniciativa', R.atr(f, 'ref'), 0, s.classe == 'batedor' ? 1 : 0, s.classe == 'batedor' ? 'Batedor: +1 dado' : ''); return true }
    if (a == 'sfl-esq') { const b = Math.max(R.treinoDe(f, 'Parkour'), R.treinoDe(f, 'Atletismo')), fol = f.stats.find(x => x.id == 'pe');
      if (fol && n0(fol.cur) < 1) toast('Sem Fôlego para esquivar.'); else gasta(f, 'pe', 1); rola(f, 'Esquiva', R.atr(f, 'ref'), b, 0, '−1 Fôlego'); return true }
    if (a == 'sfl-blq') { const b = Math.max(R.treinoDe(f, 'Contundente'), R.treinoDe(f, 'Cortante')), r = rola(f, 'Bloqueio', R.atr(f, 'cor'), b, 0);
      toast(`Bloqueio ${r.total}: bloqueia <b>${Math.floor(r.total / 5)}</b> de dano com a mão ou <b>${Math.floor(r.total / 3)}</b> com arma ou escudo. A armadura reduz o resto.`); return true }
    if (a == 'sfl-ctr') { const b = Math.max(R.treinoDe(f, 'Contundente'), R.treinoDe(f, 'Cortante')); rola(f, 'Contra-ataque', R.atr(f, 'cor'), b, 0, 'se vencer o atacante, evita o golpe e causa dano'); return true }
    if (a == 'sfl-atk') { const it = f.inv.items[+d.i], at = R.ataque(f, it), r = R.teste(Math.max(0, at.dados), VD, at.bonus), crit = at.crit && r.d >= at.crit.m;
      toast(`${rotuloR(f)} · ${esc(it.n)} (${esc(at.rotulo)}): [${r.r}] → ${r.d}${at.bonus ? ' ' + sinal(at.bonus) : ''} = <b>${r.total}</b>${at.treinada ? '' : ' · sem treino'}${crit ? ` · <b>CRÍTICO ×${at.crit.x}</b> (se acertar: efeito ${esc((it.arma || {}).efeito || 'n/a')})` : ''}`); return true }
    if (a == 'sfl-dano') { const it = f.inv.items[+d.i], r = R.danoRolar(f, it, !!d.c);
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
    const k = f.skills[i], at = R.atr(f, k.a), b = n0(k.t) + n0(k.o), medo = n0((f.stats.find(x => x.id == 'medo') || {}).cur);
    const vont = k.n == 'Vontade' && medo >= 3, dist = (k.n == 'Tiro' || k.n == 'Arremesso') && medo >= 3;
    rola(f, k.n, at, b, (vont || dist) ? -1 : 0, vont || dist ? 'Medo 3+: desvantagem' : '');
  }

  window.SFL = { TABS, views: { g: vFicha, c: vCombate, p: vPericias, i: vInv, h: vHab, n: vNotas }, calc, derive, depois, acao, dinheiro, podeMec, mestre, rolarPericia };
})();
