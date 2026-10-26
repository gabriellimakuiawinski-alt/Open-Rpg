/* ficha-op.js — ficha de Ordem Paranormal (automática). Usa as funções da ficha.html
   (inp, num, esc, toast, touch, render, curF, CAMPS, meuPapel...) e as regras de sistemas.js. */
(function () {
  'use strict';
  const S = window.SIS, n0 = S.n0;
  const campDe = f => CAMPS.find(c => c.id == f._camp) || null;
  const cfgDe = f => S.cfgDe(campDe(f));
  const mestre = f => !!f._camp && meuPapel(f._camp) == 'mestre';
  /* números de regra (defesa, luz, efeitos de item) só o mestre muda; sem campanha, o dono */
  const podeMec = f => f._camp ? mestre(f) : f._dono == ME.id;
  const idxAt = (f, id) => f.attrs.findIndex(a => a.id == id);
  const sinal = v => (v > 0 ? '+' : '') + v;
  const moeda = f => (cfgDe(f).moeda || 'R$');
  const dinheiroTxt = (f, v) => moeda(f) + ' ' + (n0(v)).toLocaleString('pt-BR', { maximumFractionDigits: 2 });
  let ULT = null; // última derivação, para mostrar sem recalcular

  const TABS = [['g', 'Agente'], ['c', 'Combate'], ['p', 'Perícias'], ['i', 'Inventário'], ['h', 'Habilidades'], ['n', 'Documentos']];
  const TIPOS_HAB = [['poder', 'Poder'], ['ritual', 'Ritual'], ['trilha', 'Trilha'], ['classe', 'Classe'], ['origem', 'Origem'], ['paranormal', 'Paranormal'], ['homebrew', 'Homebrew']];
  const ELEM = ['', 'Sangue', 'Morte', 'Conhecimento', 'Energia', 'Medo'];

  function calc(f) { const r = S.aplicar(f, cfgDe(f)); ULT = r.D; return r }

  /* ---------- pedaços ---------- */
  const sel = (p, opts, v, ex = '') => `<select data-p="${p}" ${ex}>${opts.map(([k, l]) => `<option value="${esc(k)}" ${String(k) == String(v) ? 'selected' : ''}>${esc(l)}</option>`).join('')}</select>`;
  const anel = (pct, txt, sub) => { const r = 44, c = 2 * Math.PI * r, p = Math.max(0, Math.min(1, pct));
    return `<svg class="anel" viewBox="0 0 100 100" aria-hidden="true"><circle cx="50" cy="50" r="${r}" class="a0"/><circle cx="50" cy="50" r="${r}" class="a1" stroke-dasharray="${c * p} ${c}" transform="rotate(-90 50 50)"/>
<text x="50" y="${sub ? 50 : 58}" text-anchor="middle" class="at1">${esc(txt)}</text>${sub ? `<text x="50" y="68" text-anchor="middle" class="at2">${esc(sub)}</text>` : ''}</svg>` };
  const sigilo = `<svg class="sigilo" viewBox="0 0 200 200" aria-hidden="true"><circle cx="100" cy="100" r="92"/><circle cx="100" cy="100" r="70"/><path d="M100 8 L180 146 L20 146 Z M100 192 L20 54 L180 54 Z"/><circle cx="100" cy="100" r="22"/><path d="M100 30v140M30 100h140"/></svg>`;

  function avisos(f) {
    const L = f.op.avisos || [], livro = temLivro(f.op.classe);
    const faltaTrilha = livro && nexDe(f) >= 10 && !f.op.trilha && !L.some(a => a.k == 'trilha');
    if (!L.length && !faltaTrilha) return '';
    const atr = S.ATR.map(([id, ab]) => `<button class="mini" data-act="op-atr" data-at="${id}">${ab} +1</button>`).join('');
    const rot = a => !livro ? '＋ Adicionar habilidade' : a.k == 'trilha' ? (f.op.trilha ? 'Ver habilidades da trilha' : 'Escolher trilha') : a.k == 'poder' ? 'Escolher poder' : a.k == 'vers' ? 'Escolher (poder ou outra trilha)' : '＋ Ver habilidade de classe';
    const obrig = a => a.k == 'trilha' && livro && !f.op.trilha;          // sem trilha não dá para dispensar
    return `<section class="card aviso-nex"><h2>Novidades do personagem</h2>${faltaTrilha ? `<div class="av-l"><div class="av-t"><b>NEX ${nexDe(f)}%</b> — Você precisa escolher uma trilha de ${esc((S.CLASSES[f.op.classe] || {}).n || 'sua classe')}.</div>
<div class="av-b"><button class="mini" data-act="op-trilha">Escolher trilha</button></div></div>` : ''}${L.map(a => `<div class="av-l" data-aviso="${a.id}">
<div class="av-t"><b>${f.op.classe == 'sobrevivente' ? 'Estágio ' + a.nv : 'NEX ' + nexAviso(a) + '%'}</b> — ${esc(a.t)}</div>
<div class="av-b">${a.k == 'atr' ? atr : a.k == 'grau' ? `<button class="mini" data-act="op-grau" data-av="${a.id}">Ir para perícias</button>` : `<button class="mini" data-act="op-hab" data-av="${a.id}">${rot(a)}</button>`}${obrig(a) ? '' : `<button class="mini fino" data-act="op-dispensa" data-av="${a.id}">Dispensar</button>`}</div></div>`).join('')}
<p class="m" style="font-size:12px;margin:8px 0 0">Ao subir de NEX os PV, PE e SAN já aumentam sozinhos. Aqui ficam só as escolhas que são suas.</p></section>`;
  }

  function barras(f, D) {
    const ids = D.determinacao ? ['pv', 'pe'] : ['pv', 'pe', 'san'];
    return ids.map(id => { const i = f.stats.findIndex(s => s.id == id), s = f.stats[i]; if (i < 0) return '';
      return `<div class="st op-st st-${id}"><div class="sth"><b class="k">${esc(s.n)}</b><span class="sp"></span><span class="m" data-d="max-${id}">máx. ${n0(s.max)}</span></div>
<div class="bar"><i id="sb${i}"></i></div>
<div class="ctl"><button data-act=sd data-i=${i} data-d=-5 class="b5">−5</button><button data-act=sd data-i=${i} data-d=-1>−</button>${num(`stats.${i}.cur`, s.cur, 'min=0')}<span class=m>/ <span data-d="mx-${id}">${n0(s.max)}</span></span><button data-act=sd data-i=${i} data-d=1>＋</button><button data-act=sd data-i=${i} data-d=5 class="b5">+5</button></div></div>` }).join('');
  }

  function pentagono(f) {
    const pos = { agi: [50, 9], for: [90, 38], int: [75, 86], pre: [25, 86], vig: [10, 38] };
    return `<div class="penta"><svg viewBox="0 0 100 100" aria-hidden="true"><circle cx="50" cy="52" r="40"/><polygon points="50,12 88,40 74,86 26,86 12,40"/><polygon points="50,12 74,86 12,40 88,40 26,86"/></svg>
${S.ATR.map(([id, ab, nome]) => { const i = idxAt(f, id), [x, y] = pos[id];
      return `<label class="pn" style="left:${x}%;top:${y}%" title="${nome}"><span>${ab}</span>${num(`attrs.${i}.v`, f.attrs[i].v, 'min=0 max=6 class=big data-rr')}</label>` }).join('')}</div>`;
  }

  /* ---------- telas ---------- */
  function vAgente(f) {
    const D = ULT, op = f.op, C = D.classe, meu = f._dono == ME.id, pp = meuPapel(f._camp);
    const nexOpts = S.NEX.map(x => [x, x + '%']), cls = Object.entries(S.CLASSES).map(([k, c]) => [k, c.n]);
    return `${meu ? '' : `<p class=m style="margin:0 0 10px;color:var(--giz2)">Ficha de <b>${esc(f._donoNome || 'outro jogador')}</b>. ${podeEditar(f) ? 'Você a edita como ' + (pp == 'mestre' ? 'mestre' : 'admin') + ' da campanha.' : 'Somente leitura.'}</p>`}${avisos(f)}
<section class="card dossie">${sigilo}<div class="carimbo-op">Arquivo de agente</div>
<label class=fld>Nome do personagem${inp('nome', f.nome)}</label>
<div class="g3"><label class=fld>Classe${sel('op.classe', cls, op.classe, 'data-rr')}</label>
${C.estagio ? `<label class=fld>Estágio${sel('op.estagio', [1, 2, 3, 4, 5].map(x => [x, 'Estágio ' + x]), op.estagio || 1, 'data-n data-rr')}</label>` : `<label class=fld>NEX${sel('op.nex', nexOpts, op.nex || 5, 'data-n data-rr')}</label>`}
<label class=fld>Origem${inp('op.origem', op.origem || '', 'placeholder="Ex.: Policial"')}${meu && temLivro(op.classe) ? '<button class="mini" data-act="op-livro" data-g="origem" type="button">Escolher do livro</button>' : ''}</label>
<label class=fld>Trilha${inp('op.trilha', op.trilha || '', 'placeholder="Escolha no NEX 10%"')}</label>
<label class=fld>Jogador${inp('op.jogador', op.jogador || f._donoNome || '', '')}</label>
<label class=fld>Pontos de prestígio${num('op.pp', op.pp || 0, 'min=0 data-rr')}</label></div>
<div class="selos">
<div class="selo-nex">${anel(C.estagio ? D.n / 5 : (D.nex || 5) / 100, C.estagio ? 'E' + D.n : (D.nex || 5) + '%', C.estagio ? 'estágio' : 'NEX')}</div>
<div class="selo"><b data-d="def">${D.def}</b><small>Defesa</small></div>
<div class="selo"><b data-d="desloc">${D.desloc}m</b><small>Desloc.</small></div>
<div class="selo"><b data-d="lim">${D.limPE}</b><small>PE/turno</small></div>
<div class="selo larga"><b>${esc(D.patente[1])}</b><small>Patente · crédito ${esc(D.patente[2].toLowerCase())}</small></div></div>
${f._camp ? `<p class="m mini-l">Campanha: <b>${esc((campDe(f) || {}).nome || '')}</b> · Sistema <b>Ordem Paranormal</b>${cfgDe(f).determinacao ? ' · regra de Determinação' : ''}</p>` : ''}
${meu ? `<label class=fld>Campanha<select data-camp><option value="">— nenhuma (só você vê) —</option>${CAMPS.filter(c => c.id == f._camp || meuPapel(c.id)).map(c => `<option value="${c.id}" ${c.id == f._camp ? 'selected' : ''}>${esc(c.nome)}</option>`).join('')}</select></label>` : ''}
${!f._camp && meu ? `<label class=fld>Sistema da ficha<select data-sis>${Object.entries(S.SISTEMAS).map(([k, s]) => `<option value="${k}" ${k == 'op' ? 'selected' : ''}>${s.n}</option>`).join('')}</select></label>` : ''}
${meu || pp == 'mestre' ? `<label class=sm style="font-size:14px;margin:0 0 6px"><input type=checkbox data-flag=_priv ${f._priv ? 'checked' : ''}> Ficha privada (só o dono e o mestre veem)</label>` : ''}
${pp == 'mestre' ? `<label class=sm style="font-size:14px;margin:0 0 6px"><input type=checkbox data-flag=_npc ${f._npc ? 'checked' : ''}> NPC (só o mestre vê)</label>` : ''}
</section>
<section class="card"><h2>Condição</h2>${barras(f, D)}
<details class="ajuste"><summary>Ajustes manuais nos máximos</summary><p class="m" style="font-size:13px;margin:6px 0">Para efeitos que o sistema ainda não conhece. Habilidades com efeito automático já somam sozinhas.</p>
<div class="g3">${[['pv', 'PV'], ['pe', D.determinacao ? 'PD' : 'PE'], ['san', 'SAN'], ['def', 'Defesa'], ['desloc', 'Desloc.'], ['carga', 'Carga']].filter(([k]) => !(D.determinacao && k == 'san')).map(([k, l]) => `<label class=sm>${l} ${num('op.bonus.' + k, (op.bonus || {})[k] || 0, 'data-rr')}</label>`).join('')}</div></details></section>
<section class="card"><h2>Atributos</h2>${pentagono(f)}<p class="m" style="font-size:12px;margin:4px 0 0;text-align:center">Mudar um atributo recalcula PV, PE, Defesa e carga na hora.</p></section>`;
  }

  function vCombate(f) {
    const D = ULT, its = f.inv.items, armas = its.map((it, i) => [it, i]).filter(([it]) => it.tipo == 'arma' && S.n0(it.qtd === undefined ? 1 : it.qtd) > 0);
    const res = [['Fortitude', 'vig'], ['Reflexos', 'agi'], ['Vontade', 'pre']];
    return `<section class="card"><h2>Defesa</h2><div class="defesa"><div class="escudo-d"><b data-d="def">${D.def}</b><small>Defesa</small></div>
<ul class="det">${D.defDet.map(([n, v]) => `<li><span>${esc(n)}</span><b>${sinal(v)}</b></li>`).join('')}</ul></div>
${D.pesadaSemProf ? '<p class="alerta">Proteção pesada sem a habilidade Proteção Pesada: −2 dados em testes de Força e Agilidade.</p>' : ''}
<p class="m" style="font-size:13px;margin:8px 0 0">Equipe proteções no <b>Inventário</b>: a Defesa muda sozinha.</p></section>
<section class="card"><h2>Ataques</h2>${armas.map(([it, i]) => { const a = it.arma || {}, per = a.per || 'Luta', sk = f.skills.find(s => s.n == per);
      return `<div class="arma"><div class="ar-n"><b>${esc(it.n || 'Arma')}</b><small>${esc([a.dano, a.crit && 'crít. ' + a.crit, a.alc, a.td].filter(Boolean).join(' · '))}</small></div>
<button class="roll" data-act="op-atk" data-i="${i}" title="Atacar (${esc(per)})">🎲</button><button class="mini" data-act="op-dano" data-i="${i}">Dano</button></div>` }).join('') || '<p class="m">Nenhuma arma no inventário.</p>'}</section>
<section class="card"><h2>Resistências</h2><div class="res">${res.map(([n]) => { const i = f.skills.findIndex(s => s.n == n); return i < 0 ? '' : `<button class="btn-res" data-act="roll" data-i="${i}"><b>${n}</b><small id="rs${i}"></small></button>` }).join('')}</div>
${D.res ? `<p class="m" style="font-size:13px">Habilidades: ${sinal(D.res)} em testes de resistência (já somado).</p>` : ''}</section>`;
  }

  function vPericias(f) {
    return `<section class="card"><h2>Perícias</h2><p class="m" style="margin:0 0 8px;font-size:12px">Rola d20 igual ao atributo e fica com o maior (atributo 0: dois dados, fica o menor). O bônus automático vem de itens e habilidades.</p>
${f.skills.map((s, i) => `<div class="sk"><button class="roll" data-act="roll" data-i="${i}" title="Rolar">🎲</button><span class="sn">${esc(s.n)}</span><select data-p="skills.${i}.a">${attrOpts(f, s.a)}</select><select data-p="skills.${i}.t" data-n>${S.TREINO.map(([v, l]) => `<option value=${v} ${s.t == v ? 'selected' : ''}>${l}</option>`).join('')}</select>${num(`skills.${i}.o`, s.o, 'title="Outros bônus"')}<b id="sk${i}"></b></div>`).join('')}
</section>`;
  }

  function itemCard(f, it, i) {
    const M = podeMec(f), tipo = it.tipo || 'geral', luzT = it.luz ? (it.luz.t == 'c' ? 'Lanterna (cone)' : 'Lampião (raio)') + ' ' + n0(it.luz.m) + ' m' : '';
    const eqv = tipo == 'protecao' || tipo == 'arma';
    const tag = [tipo == 'protecao' ? 'Defesa ' + sinal(n0(it.def)) : '', luzT].filter(Boolean);
    return `<div class="it op-it ${it.eq ? 'eq' : ''}"><div class="itr">${inp(`inv.items.${i}.n`, it.n, 'placeholder="Nome do item" class=in')}${eqv ? `<button class="eqb ${it.eq ? 'on' : ''}" data-act="op-eq" data-i="${i}">${it.eq ? '✓ Equipado' : 'Equipar'}</button>` : ''}<button class=x data-act=del data-l=items data-i=${i}>✕</button></div>
<div class="itr"><label class=sm>Tipo ${sel(`inv.items.${i}.tipo`, S.TIPOS_ITEM, tipo, 'data-rr' + (M ? '' : ' disabled'))}</label><label class=sm>Cat. ${sel(`inv.items.${i}.catg`, [0, 1, 2, 3, 4].map(x => [x, S.ROMANO[x]]), Math.round(n0(it.catg)), 'data-n data-rr' + (M ? '' : ' disabled'))}</label><label class=sm>Esp.${num(`inv.items.${i}.esp`, it.esp, 'min=0 step=.5' + (M ? '' : ' disabled'))}</label><label class=sm>Qtd${num(`inv.items.${i}.qtd`, it.qtd === undefined ? 1 : it.qtd, 'min=0 data-rr')}</label></div>
${tag.length ? `<div class="tags">${tag.map(t => `<span>${esc(t)}</span>`).join('')}</div>` : ''}
${M ? `<details class="mec"><summary>Regras do item ${f._camp ? '(só o mestre)' : ''}</summary>
${tipo == 'protecao' ? `<div class="itr"><label class=sm>Proteção ${sel(`inv.items.${i}.sub`, [['leve', 'Leve'], ['pesada', 'Pesada'], ['escudo', 'Escudo']], it.sub || 'leve')}</label><label class=sm>Defesa ${num(`inv.items.${i}.def`, it.def || 0, 'data-rr')}</label></div>` : ''}
${tipo == 'arma' ? `<div class="itr"><label class=sm>Dano ${inp(`inv.items.${i}.arma.dano`, (it.arma || {}).dano || '', 'style="width:70px" placeholder=1d8')}</label><label class=sm>Crít. ${inp(`inv.items.${i}.arma.crit`, (it.arma || {}).crit || '', 'style="width:60px" placeholder=x2')}</label><label class=sm>Teste ${sel(`inv.items.${i}.arma.per`, [['Luta', 'Luta'], ['Pontaria', 'Pontaria']], (it.arma || {}).per || 'Luta')}</label></div>` : ''}
<div class="itr"><label class=sm>Luz ${sel(`inv.items.${i}.luz.t`, [['', 'nenhuma'], ['c', 'Lanterna (cone)'], ['l', 'Lampião (raio)']], (it.luz || {}).t || '', 'data-rr')}</label>${it.luz && it.luz.t ? `<label class=sm>Alcance ${num(`inv.items.${i}.luz.m`, it.luz.m || 0, 'step=1.5 min=0')} m</label>` : ''}</div>
<div class="efs">${(it.ef || []).map((e, j) => efLinha(`inv.items.${i}.ef.${j}`, e, 'items', i, j, false)).join('')}<button class="mini" data-act="op-ef+" data-l="items" data-i="${i}">＋ Bônus do item</button></div></details>` : ''}
${inp(`inv.items.${i}.desc`, it.desc || '', 'placeholder="Descrição e notas"')}</div>`;
  }
  const efLinha = (p, e, l, i, j, nv) => `<div class="ef">${sel(p + '.a', S.ALVOS, e.a || 'pv')}${num(p + '.v', e.v || 0, 'data-rr')}${nv ? `<label class=sm><input type=checkbox data-chk="${p}.nv" ${e.nv ? 'checked' : ''}> × nível</label>` : ''}<button class="x" data-act="op-ef-" data-l="${l}" data-i="${i}" data-j="${j}">✕</button></div>`;

  function vInv(f) {
    const D = ULT, pat = D.patente, pct = D.cap > 0 ? Math.min(100, D.usado / D.cap * 100) : 100;
    const din = f._din, eM = mestre(f);
    return `<section class="card"><h2>Carga e dinheiro</h2><div class="bar"><i style="width:${pct}%;background:${D.sobre ? '#e44' : 'var(--a)'}"></i></div>
<div class="${D.sobre ? 'over' : 'm'}" id="ct">${S.n0(D.usado)} / ${D.cap} espaços${D.sobre ? ' — sobrecarregado (−5 Defesa, −3 m)' : ''}${D.usado > D.maxCarga ? ' — acima do máximo!' : ''}</div>
<div class="carteira">${din === undefined ? '<span class="m">Dinheiro: peça ao mestre para rodar o SQL da etapa 5.</span>' : eM ? `<label class=sm>Dinheiro (${esc(moeda(f))}) <input type=number data-din value="${n0(din)}" min=0 step="0.01" style="width:110px"></label>` : `<b>${esc(dinheiroTxt(f, din))}</b>`}
${f._camp ? `<a class="tl loja-l" href="loja.html?camp=${f._camp}&ficha=${f.id}">🛒 Loja</a>` : ''}</div>
<p class="m" style="font-size:13px;margin:6px 0 0">Patente <b>${esc(pat[1])}</b>: até ${[1, 2, 3, 4].filter(c => pat[3][c - 1]).map(c => pat[3][c - 1] + '× cat. ' + S.ROMANO[c]).join(', ') || 'só categoria 0'}.</p>
${D.excesso.length ? `<p class="alerta">Acima do limite da patente: ${esc(D.excesso.join('; '))}.</p>` : ''}
<p class="m" style="font-size:13px;margin:6px 0 0">Luz para a mesa: ${D.luz.c ? `🔦 ${esc(D.luz.cn)} (${D.luz.c} m)` : '🔦 sem lanterna'} · ${D.luz.l ? `🏮 ${esc(D.luz.ln)} (${D.luz.l} m)` : '🏮 sem lampião'}</p></section>
<section class="card"><h2>Itens</h2>${f.inv.items.map((it, i) => itemCard(f, it, i)).join('') || '<p class=m>Inventário vazio.</p>'}
<div class="g2b"><button class=add data-act=add data-l=items>＋ Item próprio</button>${podeMec(f) || cfgDe(f).catalogoLivre !== false ? '<button class=add data-act="op-cat">＋ Do catálogo</button>' : ''}</div></section>`;
  }

  function vHab(f) {
    const D = ULT, pe = f.stats.find(s => s.id == 'pe');
    return `<section class="card"><h2>Habilidades, poderes e rituais</h2>
<p class="m" style="font-size:13px;margin:0 0 8px">PE: <b data-d="pecur">${n0(pe && pe.cur)}</b> · limite por turno <b>${D.limPE}</b> · DT de rituais <b>${D.dtRitual}</b></p>
${f.poderes.map((p, i) => { const t = p.tipo || 'poder', rit = t == 'ritual';
      return `<div class="po op-po t-${t} ${p.off ? 'off' : ''}"><div class="itr">${inp(`poderes.${i}.n`, p.n, 'placeholder=Nome class=in')}<button class=x data-act=del data-l=poderes data-i=${i}>✕</button></div>
<div class="itr"><label class=sm>Tipo ${sel(`poderes.${i}.tipo`, TIPOS_HAB, t, 'data-rr')}</label>${rit ? `<label class=sm>Círculo ${sel(`poderes.${i}.circ`, [1, 2, 3, 4].map(x => [x, x + 'º']), p.circ || 1, 'data-n data-rr')}</label><label class=sm>Elemento ${sel(`poderes.${i}.el`, ELEM.map(e => [e, e || '—']), p.el || '')}</label>` : ''}
<label class=sm>Custo ${num(`poderes.${i}.pe`, p.pe === undefined ? (rit ? S.CIRCULO_PE[p.circ || 1] : 0) : p.pe, 'min=0 style="width:54px"')} PE</label>
${n0(p.pe === undefined ? (rit ? S.CIRCULO_PE[p.circ || 1] : 0) : p.pe) > 0 ? `<button class="usar" data-act="op-usar" data-i="${i}">${rit ? 'Conjurar' : 'Usar'}</button>` : ''}</div>
<textarea data-p="poderes.${i}.desc" placeholder="Descrição">${esc(p.desc || '')}</textarea>
<details class="mec" ${(p.ef || []).length || t == 'homebrew' ? 'open' : ''}><summary>Efeito automático na ficha ${t == 'homebrew' ? '(homebrew)' : ''}</summary>
<label class=sm><input type=checkbox data-chk="poderes.${i}.off" ${p.off ? 'checked' : ''}> Desligado (não soma)</label>
${(p.ef || []).map((e, j) => efLinha(`poderes.${i}.ef.${j}`, e, 'poderes', i, j, true)).join('')}<button class="mini" data-act="op-ef+" data-l="poderes" data-i="${i}">＋ Efeito</button>
${f._camp && (t == 'homebrew' || p.ef && p.ef.length) ? `<button class="mini" data-act="op-share" data-i="${i}">Enviar para a campanha${mestre(f) ? '' : ' (o mestre aprova)'}</button>` : ''}</details></div>` }).join('') || '<p class="m">Nenhuma habilidade ainda.</p>'}
${temLivro(f.op.classe) ? `<div class="g2b"><button class=add data-act="op-livro">＋ Do livro</button></div>
<details style="margin-top:10px"><summary class="m">Criar habilidade própria (homebrew)</summary><div class="g2b"><button class=add data-act="op-nova" data-t="poder">＋ Habilidade</button><button class=add data-act="op-nova" data-t="ritual">＋ Ritual</button><button class=add data-act="op-nova" data-t="homebrew">＋ Homebrew</button>${f._camp ? '<button class=add data-act="op-camp">＋ Da campanha</button>' : ''}</div></details>`
: `<div class="g2b"><button class=add data-act="op-nova" data-t="poder">＋ Habilidade</button><button class=add data-act="op-nova" data-t="ritual">＋ Ritual</button><button class=add data-act="op-nova" data-t="homebrew">＋ Homebrew</button>${f._camp ? '<button class=add data-act="op-camp">＋ Da campanha</button>' : ''}</div>`}</section>`;
  }

  function vDocs(f) { return vDocsSec(f) + vNotasSec(f) }

  /* ---------- atualização sem redesenhar (mantém o foco no campo) ---------- */
  function derive(f) {
    const D = ULT || calc(f).D;
    f.stats.forEach((s, i) => { const e = document.getElementById('sb' + i); if (e) { e.style.width = (s.max > 0 ? Math.max(0, Math.min(100, s.cur / s.max * 100)) : 0) + '%'; e.style.background = s.c } });
    f.skills.forEach((s, i) => { const at = av(f, s.a), b = n0(s.t) + n0(s.o) + n0(D.per[s.n]) + (['Fortitude', 'Reflexos', 'Vontade'].includes(s.n) ? D.res : 0);
      const t = (at > 0 ? at : 2) + 'd20' + (at > 0 ? '' : '↓') + (b ? ' ' + sinal(b) : '') + (D.per[s.n] ? ' ★' : '');
      const e = document.getElementById('sk' + i); if (e) e.textContent = t; const r = document.getElementById('rs' + i); if (r) r.textContent = t });
    const set = (k, v) => document.querySelectorAll(`[data-d="${k}"]`).forEach(e => e.textContent = v);
    set('def', D.def); set('desloc', D.desloc + 'm'); set('lim', D.limPE);
    ['pv', 'pe', 'san'].forEach(id => { const s = f.stats.find(x => x.id == id); if (s) { set('mx-' + id, n0(s.max)); set('max-' + id, 'máx. ' + n0(s.max)) } });
    const pe = f.stats.find(s => s.id == 'pe'); if (pe) set('pecur', n0(pe.cur));
  }

  /* depois de qualquer edição: regra aplicada, mensagens e campos atualizados */
  function depois(f, rr) {
    const na = (f.op && f.op.avisos || []).length, { msg } = calc(f);
    if (msg.length) toast(msg.map(esc).join(' · '));
    if (rr || msg.length || (f.op.avisos || []).length != na) return true;
    patch(f); return false;
  }

  /* ---------- ações ---------- */
  function remAviso(f, id) { f.op.avisos = (f.op.avisos || []).filter(a => a.id != id) }
  async function acao(a, d, f) {
    if (a == 'op-atr') { const i = idxAt(f, d.at), v = n0(f.attrs[i].v); if (v >= 5) { toast('Atributo já está no máximo (5).'); return true }
      const av_ = d.av || (f.op.avisos.find(x => x.k == 'atr') || {}).id; f.attrs[i].v = v + 1; remAviso(f, av_); calc(f); touch(f); render(); toast(f.attrs[i].n + ' agora é ' + (v + 1) + '.'); return true }
    if (a == 'op-dispensa') { remAviso(f, d.av); touch(f); render(); return true }
    if (a == 'op-grau') { remAviso(f, d.av); touch(f); setTab('p'); toast('Suba o grau de 2 + INT perícias treinadas.'); return true }
    if (a == 'op-hab') { await doAviso(f, d.av); return true }
    if (a == 'op-trilha') { await escolherTrilha(f); return true }
    if (a == 'op-eq') { const it = f.inv.items[+d.i], antes = ULT.def; it.eq = !it.eq;
      if (it.eq && it.tipo == 'protecao') f.inv.items.forEach(o => { if (o !== it && o.tipo == 'protecao' && o.eq && ((o.sub == 'escudo') == (it.sub == 'escudo'))) o.eq = false });
      calc(f); touch(f); render(); if (it.tipo == 'protecao') toast(`Defesa ${antes} → <b>${ULT.def}</b>`); return true }
    if (a == 'op-ef+') { const o = d.l == 'items' ? f.inv.items[+d.i] : f.poderes[+d.i]; (o.ef = o.ef || []).push({ a: d.l == 'items' ? 'per:Percepção' : 'pv', v: 1 }); calc(f); touch(f); render(); return true }
    if (a == 'op-ef-') { const o = d.l == 'items' ? f.inv.items[+d.i] : f.poderes[+d.i]; o.ef.splice(+d.j, 1); calc(f); touch(f); render(); return true }
    if (a == 'op-nova') { f.poderes.push({ id: S.uid(), n: '', tipo: d.t, desc: '', ef: [], ...(d.t == 'ritual' ? { circ: 1, pe: 1 } : {}) }); touch(f); render(); setTimeout(() => { const l = document.querySelectorAll('.op-po'); const x = l[l.length - 1]; if (x) { x.scrollIntoView({ behavior: 'smooth', block: 'center' }); const i = x.querySelector('input'); i && i.focus() } }, 60); return true }
    if (a == 'op-usar') { const p = f.poderes[+d.i], custo = n0(p.pe === undefined ? (p.tipo == 'ritual' ? S.CIRCULO_PE[p.circ || 1] : 0) : p.pe), pe = f.stats.find(s => s.id == 'pe');
      if (!pe || n0(pe.cur) < custo) { toast(`PE insuficientes (precisa ${custo}).`); return true }
      if (custo > ULT.limPE) toast(`Atenção: custo ${custo} passa do limite de ${ULT.limPE} PE por turno.`);
      pe.cur = n0(pe.cur) - custo; touch(f); derive(f); const i = document.querySelector(`[data-p="stats.${f.stats.indexOf(pe)}.cur"]`); if (i) i.value = pe.cur;
      toast(`${esc(p.n || 'Habilidade')}: −${custo} ${esc(pe.n)} (restam ${pe.cur})${p.tipo == 'ritual' ? ` · DT ${ULT.dtRitual}` : ''}`); return true }
    if (a == 'op-atk') { const it = f.inv.items[+d.i], ar = it.arma || {}, sk = f.skills.find(s => s.n == (ar.per || 'Luta')) || { a: 'for', t: 0, o: 0 },
      at = av(f, sk.a), b = n0(sk.t) + n0(sk.o) + n0(ULT.per[sk.n]), r = S.teste(at, b);
      toast(`${esc(it.n)} · ataque (${esc(sk.n)}): [${r.r}] → ${r.d}${b ? ' ' + sinal(b) : ''} = <b>${r.total}</b>`); return true }
    if (a == 'op-dano') { const it = f.inv.items[+d.i], r = S.rolar((it.arma || {}).dano); toast(r ? `${esc(it.n)} · dano ${esc(it.arma.dano)}: ${r.txt} = <b>${r.total}</b>` : 'Preencha o dano da arma (ex.: 1d8).'); return true }
    if (a == 'op-cat') { catalogo(f); return true }
    if (a == 'op-camp') { await daCampanha(f); return true }
    if (a == 'op-livro') { await doLivro(f, d.g); return true }
    if (a == 'op-share') { await compartilhar(f, f.poderes[+d.i]); return true }
    return false;
  }
  function setTab(t) { const b = document.querySelector(`[data-tab="${t}"]`); if (b) b.click(); else render() }

  /* catálogo base + itens da campanha */
  async function catalogo(f) {
    let extra = [];
    if (f._camp) try { const r = await db.from('catalogo').select('id,tipo,nome,dados,aprovado').eq('campanha_id', f._camp).eq('tipo', 'item'); if (!r.error) extra = r.data.filter(x => x.aprovado).map(x => ({ ...x.dados, n: x.nome, ref: 'cat:' + x.id })) } catch (e) { }
    const L = extra.concat(S.CATALOGO.op);
    const o = document.createElement('div'); o.id = 'md';
    o.innerHTML = `<div class="mb"><h3>Catálogo</h3><input id="catq" placeholder="Buscar item"><div class="catl">${L.map((it, i) => `<button class="cat-i" data-k="${i}"><b>${esc(it.n)}</b><small>${esc([S.TIPOS_ITEM.find(t => t[0] == it.tipo)?.[1], 'Cat. ' + S.ROMANO[it.catg || 0], it.esp + ' esp.', it.def && 'Def +' + it.def, it.luz && (it.luz.t == 'c' ? 'cone ' : 'raio ') + it.luz.m + 'm', it.arma && it.arma.dano].filter(Boolean).join(' · '))}</small></button>`).join('')}</div>
<p class="m" style="font-size:12px;margin:0">${f._camp && !mestre(f) ? 'Você pega o item; o mestre confere a patente e pode remover.' : ''}</p><button data-x style="align-self:flex-end">Fechar</button></div>`;
    document.body.append(o);
    o.oninput = e => { if (e.target.id == 'catq') { const q = e.target.value.toLowerCase(); o.querySelectorAll('.cat-i').forEach((b, i) => b.style.display = L[i].n.toLowerCase().includes(q) ? '' : 'none') } };
    o.onclick = e => { if (e.target === o || e.target.closest('[data-x]')) { o.remove(); return }
      const b = e.target.closest('.cat-i'); if (!b) return; const it = JSON.parse(JSON.stringify(L[+b.dataset.k]));
      f.inv.items.push({ ...it, id: S.uid(), qtd: 1, eq: false, desc: it.desc || '' }); calc(f); touch(f); o.remove(); render(); toast(esc(it.n) + ' adicionado ao inventário.') };
  }
  async function daCampanha(f) {
    const r = await db.from('catalogo').select('id,tipo,nome,dados,aprovado,criado_por').eq('campanha_id', f._camp).eq('tipo', 'habilidade');
    if (r.error) { toast('Catálogo da campanha indisponível (o mestre precisa rodar o SQL da etapa 5).'); return }
    const L = r.data.filter(x => x.aprovado);
    const o = document.createElement('div'); o.id = 'md';
    o.innerHTML = `<div class="mb"><h3>Habilidades da campanha</h3><div class="catl">${L.map((x, i) => `<button class="cat-i" data-k="${i}"><b>${esc(x.nome)}</b><small>${esc((x.dados.tipo || 'homebrew') + ((x.dados.ef || []).length ? ' · efeito automático' : ''))}</small></button>`).join('') || '<p class="m">Nenhuma ainda. Crie um homebrew e envie para a campanha.</p>'}</div><button data-x style="align-self:flex-end">Fechar</button></div>`;
    document.body.append(o);
    o.onclick = e => { if (e.target === o || e.target.closest('[data-x]')) { o.remove(); return }
      const b = e.target.closest('.cat-i'); if (!b) return; const x = L[+b.dataset.k];
      f.poderes.push({ ...JSON.parse(JSON.stringify(x.dados)), id: S.uid(), n: x.nome, ref: 'cat:' + x.id }); calc(f); touch(f); o.remove(); render(); toast(esc(x.nome) + ' adicionada.') };
  }
  /* habilidades do livro (classe, poderes, trilhas) — tabela global livro_habilidades */
  let LIVRO = null;
  const CLS3 = [['combatente', 'Combatente'], ['especialista', 'Especialista'], ['ocultista', 'Ocultista']];
  const temLivro = c => CLS3.some(x => x[0] == c);
  const REPETE = ['Transcender', 'Treinamento em Perícia', 'Aprender Ritual', 'Resistir a <Elemento>'];           // o livro deixa escolher várias vezes
  const GENERICA = /^(Habilidade de Trilha|Poder de |Aumento de Atributo|Grau de Treinamento|Versatilidade)/;
  const nexDe = f => n0(f.op.nex) || 5;
  const nexAviso = a => a.nv >= 20 ? 99 : a.nv * 5;
  const jaTem = (f, x) => !REPETE.includes(x.nome) && f.poderes.some(p => p.ref == 'livro:' + x.ref);
  async function livroCarrega() {
    if (LIVRO) return true;
    const r = await db.from('livro_habilidades').select('ref,classe,grupo,trilha,nex,ordem,nome,dados,circulo,elemento').eq('sistema', 'op').order('ordem');
    if (r.error || !r.data.length) { toast('Habilidades do livro indisponíveis (rode o SQL schema_etapa6_livro.sql no Supabase).'); return false }
    LIVRO = r.data; return true;
  }
  const trilhasDe = cl => [...new Set(LIVRO.filter(x => x.classe == cl && x.grupo == 'trilha').map(x => x.trilha))];
  const resumo = (f, x) => {
    const d = x.dados || {}, sub = [x.grupo == 'ritual' ? (x.elemento || 'Elemento à escolha') : x.grupo == 'paranormal' ? (x.elemento || 'Geral') : '', x.grupo == 'ritual' ? x.circulo + 'º círculo' : '', x.grupo == 'origem' ? 'Poder: ' + x.nome + ' · ' + (d.pericias && d.pericias.length ? d.pericias.join(' e ') : 'perícias à escolha do mestre') : '', x.grupo == 'paranormal' && d.pre ? 'Pré-requisito: ' + d.pre : '', x.nex ? 'NEX ' + x.nex + '%' : '', d.pe ? d.pe + ' PE' : '', (d.ef || []).length ? 'efeito automático' : '', jaTem(f, x) ? 'já na ficha' : ''].filter(Boolean).join(' · ');
    return `<button class="cat-i" data-r="${esc(x.ref)}"><b>${esc(x.grupo == 'origem' ? d.origem : x.nome)}</b><small>${esc(sub)}</small><small style="white-space:normal">${esc(d.desc || '')}</small></button>`;
  };
  const titulo2 = t => `<p class="m" style="margin:10px 0 2px"><b>${esc(t)}</b></p>`;
  /* janela de escolha. corpo() -> [topo, lista]; aoEscolher(botão, fechar); aoFiltro(botão) muda o estado */
  function janela(titulo, corpo, aoEscolher, aoFiltro) {
    const o = document.createElement('div'); o.id = 'md';
    const tela = () => { const [topo, lista] = corpo(); o.innerHTML = `<div class="mb"><h3>${esc(titulo)}</h3>${topo || ''}<div class="catl">${lista}</div><button data-x style="align-self:flex-end">Fechar</button></div>` };
    tela(); document.body.append(o);
    o.onclick = e => {
      if (e.target === o || e.target.closest('[data-x]')) { o.remove(); return }
      const fl = aoFiltro && e.target.closest('[data-f]'); if (fl) { aoFiltro(fl.dataset.f); tela(); return }
      const b = e.target.closest('.cat-i'); if (b) aoEscolher(b, () => o.remove());
    };
    return o;
  }
  function addLivro(f, x) {
    f.poderes.push({ ...JSON.parse(JSON.stringify(x.dados)), id: S.uid(), n: x.nome, ref: 'livro:' + x.ref });
    if (x.grupo == 'trilha' && !f.op.trilha) f.op.trilha = x.trilha;
  }
  function fim(f, fecha, x, av) { if (av) remAviso(f, av); calc(f); touch(f); fecha(); render(); toast(esc(x.nome) + ' adicionada.') }
  const achar = b => LIVRO.find(y => y.ref == b.dataset.r);

  /* botão "＋ Do livro": navegar por classe / grupo */
  async function doLivro(f, g0) {
    if (!await livroCarrega()) return;
    let cl = temLivro(f.op.classe) ? f.op.classe : 'combatente', gr = g0 || 'trilha', ci = 0, el = '', pe = '';
    const mk = (k, v, t, on) => `<button class="mini" data-f="${k}:${v}" ${on ? 'style="outline:2px solid currentColor"' : ''}>${t}</button>`;
    const ELS = ['Conhecimento', 'Energia', 'Morte', 'Sangue', 'Medo'];
    const circMax = f.op.classe == 'ocultista' ? (nexDe(f) >= 85 ? 4 : nexDe(f) >= 55 ? 3 : nexDe(f) >= 25 ? 2 : 1) : 0;
    const dica = f.op.classe == 'ocultista' ? `Seu NEX libera rituais até o ${circMax}º círculo; a cada avanço de NEX você aprende um novo.` : 'Rituais vêm do poder paranormal Aprender Ritual (até seu Intelecto).';
    const ABAS = [['trilha', 'Trilhas'], ['poder', 'Poderes'], ['classe', 'Classe'], ['ritual', 'Rituais'], ['origem', 'Origens'], ['paranormal', 'Paranormal']];
    const abas = () => `<div class="g2b">${ABAS.map(g => mk('gr', g[0], g[1], g[0] == gr)).join('')}</div>`;
    janela('Habilidades do livro', () => {
      if (gr == 'origem') {
        const L = LIVRO.filter(x => x.grupo == 'origem');
        return [abas() + `<p class="m" style="margin:4px 0 0;font-size:12px">Toque na origem: você recebe as 2 perícias treinadas e o poder da origem. Origem atual: <b>${esc(f.op.origem || 'nenhuma')}</b>.</p>`, L.map(x => resumo(f, x)).join('')];
      }
      if (gr == 'paranormal') {
        const L = LIVRO.filter(x => x.grupo == 'paranormal' && (!pe || (pe == 'Geral' ? !x.elemento : x.elemento == pe)));
        return [abas() + `<div class="g2b">${[mk('pe', '', 'Todos', !pe)].concat(['Geral', ...ELS.slice(0, 4)].map(e => mk('pe', e, e, pe == e))).join('')}</div><p class="m" style="margin:4px 0 0;font-size:12px">Vêm do poder de classe Transcender (você não recebe a Sanidade daquele NEX). Confira os pré-requisitos na descrição.</p>`, L.map(x => resumo(f, x)).join('') || '<p class="m">Nenhum poder.</p>'];
      }
      if (gr == 'ritual') {
        const L = LIVRO.filter(x => x.grupo == 'ritual' && (!ci || x.circulo == ci) && (!el || !x.elemento || x.elemento == el));
        let h = '', ult = 0;
        L.forEach(x => { if (!ci && x.circulo != ult) { ult = x.circulo; h += titulo2(x.circulo + 'º círculo') } h += resumo(f, x) });
        return [`${abas()}
<div class="g2b">${[mk('ci', 0, 'Todos', !ci)].concat([1, 2, 3, 4].map(n => mk('ci', n, n + 'º', ci == n))).join('')}</div>
<div class="g2b">${[mk('el', '', 'Todos', !el)].concat(ELS.map(e => mk('el', e, e, el == e))).join('')}</div>
<p class="m" style="margin:4px 0 0;font-size:12px">${esc(dica)} Conjurar (exceto Medo) exige Ocultismo DT 20 + custo em PE; falhar custa Sanidade igual ao custo.</p>`, h || '<p class="m">Nenhum ritual com esse filtro.</p>'];
      }
      let L = LIVRO.filter(x => x.classe == cl && x.grupo == gr), ult = null, h = '';
      if (gr == 'trilha' && f.op.trilha) L = L.filter(x => x.trilha == f.op.trilha).concat(L.filter(x => x.trilha != f.op.trilha));
      L.forEach(x => {
        if (gr == 'trilha' && x.trilha != ult) { ult = x.trilha; h += titulo2(x.trilha + (f.op.trilha == x.trilha ? ' · sua trilha' : '')) }
        h += resumo(f, x);
      });
      return [`<div class="g2b">${CLS3.map(c => mk('cl', c[0], c[1], c[0] == cl)).join('')}</div>${abas()}`, h];
    }, (b, fecha) => {
      const x = achar(b); if (!x) return;
      if (x.grupo == 'origem') return escolherOrigem(f, x, fecha);
      if (jaTem(f, x)) { toast(esc(x.nome) + ' já está na ficha.'); return }
      addLivro(f, x); fim(f, fecha, x);
    }, k => { const i = k.indexOf(':'), a = k.slice(0, i), v = k.slice(i + 1); if (a == 'cl') cl = v; else if (a == 'gr') gr = v; else if (a == 'ci') ci = +v; else if (a == 'pe') pe = v; else el = v });
  }

  /* origem do livro: grava o nome, treina as 2 perícias e troca o poder de origem anterior */
  function escolherOrigem(f, x, fecha) {
    const on = x.dados.origem;
    if (f.op.origem == on && jaTem(f, x)) { toast(esc(on) + ' já é a sua origem.'); return }
    f.poderes = f.poderes.filter(p => !String(p.ref || '').startsWith('livro:op:origem:'));
    f.op.origem = on;
    ((x.dados || {}).pericias || []).forEach(n => { const k = (f.skills || []).find(y => y.n == n); if (k && n0(k.t) < 5) k.t = 5 });
    addLivro(f, x); calc(f); touch(f); fecha(); render();
    toast(esc(on) + ': perícias treinadas e poder adicionados.' + (on == 'Cultista Arrependido' ? ' Escolha agora um poder paranormal.' : ''));
  }

  /* NEX 10%: o personagem precisa escolher uma das 5 trilhas da classe (recebe a 1ª habilidade) */
  async function escolherTrilha(f, av) {
    if (!await livroCarrega()) return;
    const cl = f.op.classe, T = trilhasDe(cl);
    if (!T.length) { toast('Sem trilhas do livro para esta classe.'); return }
    janela('Escolha sua trilha', () => ['<p class="m" style="margin:0">Toque na trilha para ficar com ela. Você recebe a 1ª habilidade agora e as outras em NEX 40%, 65% e 99%.</p>',
      T.map(t => `<button class="cat-i" data-t="${esc(t)}"><b>${esc(t)}</b><small style="white-space:normal">${esc(LIVRO.filter(x => x.classe == cl && x.trilha == t).map(x => x.nome).join(' · '))}</small></button>`).join('')],
    (b, fecha) => {
      const t = b.dataset.t, x = LIVRO.find(y => y.classe == cl && y.trilha == t && y.nex == 10); if (!x) return;
      f.op.trilha = t; if (!jaTem(f, x)) addLivro(f, x);
      const a_ = av || ((f.op.avisos || []).find(y => y.k == 'trilha') || {}).id; fim(f, fecha, { nome: t + ' — ' + x.nome }, a_);
    });
  }

  /* clique no aviso de subida de NEX: leva direto às habilidades que o personagem pode pegar agora */
  async function doAviso(f, av) {
    const a = (f.op.avisos || []).find(x => x.id == av); if (!a) return;
    if (!temLivro(f.op.classe)) {                      // outras classes (sem dados do livro): cria em branco
      remAviso(f, av); f.poderes.push({ id: S.uid(), n: a.t, tipo: a.k == 'trilha' ? 'trilha' : a.k == 'classe' ? 'classe' : 'poder', desc: '', ef: [] });
      touch(f); setTab('h'); toast('Habilidade criada: preencha o nome e a descrição.'); return }
    if (!await livroCarrega()) return;
    const cl = f.op.classe, nx = nexAviso(a), nxF = nexDe(f);
    if (a.k == 'trilha') {
      if (!f.op.trilha) return escolherTrilha(f, av);
      const L = LIVRO.filter(x => x.classe == cl && x.grupo == 'trilha' && x.trilha == f.op.trilha && x.nex <= nxF && !jaTem(f, x));
      if (!L.length) { remAviso(f, av); touch(f); render(); toast('Você já tem todas as habilidades da sua trilha disponíveis neste NEX.'); return }
      janela('Trilha: ' + f.op.trilha, () => [`<p class="m" style="margin:0">Habilidade de trilha do NEX ${nx}%. Toque para adicionar.</p>`, L.map(x => resumo(f, x)).join('')],
        (b, fecha) => { const x = achar(b); if (!x) return; addLivro(f, x); fim(f, fecha, x, av) });
    } else if (a.k == 'poder') {
      const L = LIVRO.filter(x => x.classe == cl && x.grupo == 'poder' && !jaTem(f, x));
      janela('Poder de ' + (S.CLASSES[cl] || {}).n, () => ['<p class="m" style="margin:0">Veja os pré-requisitos na descrição. Toque para adicionar.</p>', L.map(x => resumo(f, x)).join('')],
        (b, fecha) => { const x = achar(b); if (!x) return; addLivro(f, x); fim(f, fecha, x, av) });
    } else if (a.k == 'vers') {
      const P = LIVRO.filter(x => x.classe == cl && x.grupo == 'poder' && !jaTem(f, x)), T = LIVRO.filter(x => x.classe == cl && x.grupo == 'trilha' && x.nex == 10 && x.trilha != f.op.trilha && !jaTem(f, x));
      janela('Versatilidade', () => ['<p class="m" style="margin:0">NEX 50%: escolha UM poder da classe ou o 1º poder de outra trilha.</p>', titulo2('Poderes da classe') + P.map(x => resumo(f, x)).join('') + titulo2('1º poder de outra trilha') + T.map(x => resumo(f, x)).join('')],
        (b, fecha) => { const x = achar(b); if (!x) return; f.poderes.push({ ...JSON.parse(JSON.stringify(x.dados)), id: S.uid(), n: x.nome, ref: 'livro:' + x.ref }); fim(f, fecha, x, av) });
    } else {                                             // 'classe': evolução de habilidade de classe
      const L = LIVRO.filter(x => x.classe == cl && x.grupo == 'classe' && !GENERICA.test(x.nome) && x.nex <= nxF && !jaTem(f, x));
      if (!L.length) { remAviso(f, av); touch(f); render(); toast('Sua habilidade de classe já está na ficha: só o custo e o bônus evoluíram (veja a descrição).'); return }
      janela('Habilidade de classe', () => [`<p class="m" style="margin:0">${esc(a.t)}</p>`, L.map(x => resumo(f, x)).join('')],
        (b, fecha) => { const x = achar(b); if (!x) return; addLivro(f, x); fim(f, fecha, x, av) });
    }
  }
  async function compartilhar(f, p) {
    if (!p.n) { toast('Dê um nome à habilidade antes.'); return }
    const { id, ref, off, ...dados } = p;
    const r = await db.from('catalogo').insert({ campanha_id: f._camp, tipo: 'habilidade', nome: p.n, dados, aprovado: mestre(f), criado_por: ME.id }).select('id');
    if (r.error) { toast('Não consegui enviar: ' + esc(r.error.message)); return }
    toast(mestre(f) ? 'Homebrew disponível para a campanha.' : 'Enviado! Aparece para todos quando o mestre aprovar (na Loja → Catálogo).');
  }

  /* mudar dinheiro (só mestre) */
  async function dinheiro(f, v) {
    const { data, error } = await db.from('personagens').update({ dinheiro: Math.max(0, n0(v)) }).eq('id', f.id).select('dinheiro');
    if (error || !data || !data.length) { toast('Não consegui mudar o dinheiro: ' + esc(error ? error.message : 'sem permissão')); return }
    f._din = +data[0].dinheiro; status('salvo ✓');
  }

  window.OP = { TABS, views: { g: vAgente, c: vCombate, p: vPericias, i: vInv, h: vHab, n: vDocs }, calc, derive, depois, acao, dinheiro, podeMec, mestre };
})();
