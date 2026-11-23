/* sfl-regras.js — regras do Search For Light (SFL 2), sistema próprio do mestre.
   Estende window.SIS (sistemas.js) e usa os dados de sfl-dados.js (window.SFLD).
   Teste: rola N d20 (N = atributo), fica o maior; o atributo NÃO soma. Resultado = maior dado + treino da perícia.
   Valores marcados [PROPOSTA] nos documentos (docs/sfl/) são ponto de partida e podem mudar. */
(function () {
  'use strict';
  const S = window.SIS, D = window.SFLD || { classes: [], origens: [], poderes: [], armas: [], mods: [], limites: {}, receitas: [], itens: [] }, n0 = S.n0;
  S.SISTEMAS.sfl = { n: 'Search For Light', d: 'Ficha automática: atributo dá os dados, perícia soma o treino, Vida, Fôlego, Medo e Infecção.' };

  const ATR = [['cor', 'Corpo', 'COR'], ['ref', 'Reflexo', 'REF'], ['men', 'Mente', 'MEN'], ['pre', 'Presença', 'PRE']];
  const PERICIAS = [['Atletismo', 'cor'], ['Furtividade', 'ref'], ['Parkour', 'ref'], ['Percepção', 'men'], ['Investigação', 'men'], ['Técnica', 'men'], ['Medicina', 'men'], ['Sobrevivência', 'men'],
    ['Persuasão', 'pre'], ['Intimidação', 'pre'], ['Vontade', 'pre'], ['Contundente', 'cor'], ['Cortante', 'cor'], ['Arremesso', 'ref'], ['Tiro', 'ref']];
  const TREINO = [[0, 'Leigo'], [3, 'Treinado +3'], [6, 'Veterano +6'], [9, 'Expert +9']];
  const FAIXAS = [[0, 'Controlado', 'sem efeitos'], [3, 'Inquieto', 'sintomas leves; poderes +2 no teste'], [6, 'Instável', 'ao usar poder, teste de Vontade DT 18'], [9, 'Limiar', 'o Ódio assume']];
  const faixaInf = v => FAIXAS.filter(f => v >= f[0]).pop();
  const BENEFICIOS = [['atr', '+1 atributo (máximo 5)'], ['per', 'Subir uma perícia de nível'], ['arma', 'Treinar uma arma especial (ou subir o treino)'], ['vida', '+1 de Vida máxima por ponto de Corpo']];
  const classe = id => D.classes.find(c => c.id == id) || null;
  const origem = id => D.origens.find(o => o.id == id) || null;
  const linha = id => D.poderes.find(p => p.id == id) || null;
  const familia = n => /^Arco/.test(n) ? 'Arco' : /^Besta/.test(n) ? 'Besta' : n;
  const ESPECIAIS = [...new Set(D.armas.filter(a => a.cat == 'especial').map(a => familia(a.n)))];

  /* ---------- crítico: "19–20 ×2" -> {m:19, x:2}; "n/a" -> null ---------- */
  function critDe(txt) {
    const m = /(\d+)(?:\s*[–-]\s*\d+)?\s*×\s*(\d+)/.exec(String(txt || ''));
    return m ? { m: +m[1], x: +m[2] } : null;
  }

  /* garante a estrutura de uma ficha SFL sem apagar nada que já exista */
  function preparar(f) {
    if (!f.sfl || typeof f.sfl != 'object') f.sfl = {};
    const s = f.sfl;
    if (s.classe === undefined) s.classe = ''; if (s.origem === undefined) s.origem = ''; if (s.trilha === undefined) s.trilha = '';
    s.marco = Math.max(0, Math.min(8, Math.round(n0(s.marco))));
    if (!Array.isArray(s.perClasse)) s.perClasse = [];
    if (!Array.isArray(s.esc)) s.esc = [];
    if (!Array.isArray(s.armas)) s.armas = [];            // treinos de arma especial [{f:'Arco', t:3}]
    if (!s.bonus || typeof s.bonus != 'object') s.bonus = {};
    if (s.linha === undefined) s.linha = '';
    /* ficha vinda de outro sistema: guarda o que havia e começa com o modelo do SFL */
    if (!Array.isArray(f.attrs)) f.attrs = [];
    if (!ATR.every(([id]) => f.attrs.some(a => a.id == id))) {
      if (f.attrs.length && !f.altSis) f.altSis = { attrs: f.attrs, skills: f.skills, stats: f.stats };
      f.attrs = ATR.map(([id, n]) => ({ id, n, v: 1 }));
    } else f.attrs = ATR.map(([id, n]) => f.attrs.find(a => a.id == id) || { id, n, v: 1 });
    if (!Array.isArray(f.skills) || !PERICIAS.every(([n]) => f.skills.some(k => k.n == n))) f.skills = PERICIAS.map(([n, a]) => ({ id: S.uid(), n, a, t: 0, o: 0 }));
    const antes = Array.isArray(f.stats) ? f.stats : [];
    const mk = (id, n, c, ex) => antes.find(x => x.id == id) || Object.assign({ id, n, cur: 0, max: 0, c }, ex || {});
    f.stats = [mk('pv', 'Vida', '#ee4444'), mk('pe', 'Fôlego', '#e8b53a'), mk('medo', 'Medo', '#8a8f98'), mk('inf', 'Infecção', '#8bd04a')];
    f.stats[0].n = 'Vida'; f.stats[1].n = 'Fôlego';
    if (!f.inv || !Array.isArray(f.inv.items)) f.inv = { items: [] };
    if (!Array.isArray(f.poderes)) f.poderes = [];
    s.impulso = Math.max(0, Math.min(3, Math.round(n0(s.impulso))));
    s.pers = Math.max(0, Math.min(6, Math.round(n0(s.pers))));
    s.adren = Math.max(0, Math.round(n0(s.adren)));
    atualizaItens(f);
    return f;
  }

  /* itens: regras do catálogo (livro V1.2) entram nos itens que já estavam na ficha; munição comprada em pilha vira unidades */
  const norm = x => String(x || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').trim();
  function atualizaItens(f) {
    const L = f.inv.items;
    L.forEach(it => {
      if (!it || typeof it != 'object') return;
      if (it.lote && !it.lotOk) { it.qtd = n0(it.qtd === undefined ? 1 : it.qtd) * n0(it.lote); it.lotOk = 1; it.ref = 'sfl:' + it.n }
      const c = it.cv == CV ? null : CATn.get(norm(it.n)) || (String(it.ref || '').startsWith('sfl:') ? CATn.get(norm(String(it.ref).slice(4))) : null);
      if (c) { ['esp', 'pilha', 'bolso', 'preco', 'rar', 'fab', 'g', 'tags', 'lim', 'sub', 'red', 'redTiro', 'desvVest', 'mochila', 'prontos', 'bandoleira', 'luz', 'uv', 'uso'].forEach(k => { if (c[k] !== undefined) it[k] = JSON.parse(JSON.stringify(c[k])) });
        if (c.usos !== undefined && it.usos === undefined) it.usos = c.usos;
        if (c.arma && it.arma) ['g', 'tags'].forEach(k => { if (c.arma[k] !== undefined) it.arma[k] = c.arma[k] }) }
      if (c || it.cv === undefined) it.cv = CV;
      if (it.tipo == 'arma' && it.eq && it.pronto === undefined) { it.pronto = true; it.eq = false }
      if (!Array.isArray(it.mods) && it.tipo == 'arma') it.mods = [];
    });
    /* mochila nova já vai para as costas (se nenhuma estiver em uso); só uma mochila vale por vez */
    const mochs = L.filter(it => it && it.tipo == 'mochila' && !it.eqv);
    if (mochs.length && !L.some(it => it && it.tipo == 'mochila' && it.eq)) mochs.sort((x, y) => n0(y.mochila) - n0(x.mochila))[0].eq = true;
    mochs.forEach(it => it.eqv = 1);
    /* junta pilhas iguais de munição, material e consumível */
    for (let i = L.length - 1; i > 0; i--) {
      const x = L[i]; if (!x || !['municao', 'material', 'consumivel'].includes(x.tipo) || x.usos !== undefined) continue;
      const j = L.findIndex((y, k) => k < i && y && y.tipo == x.tipo && norm(y.n) == norm(x.n) && y.usos === undefined);
      if (j >= 0) { L[j].qtd = n0(L[j].qtd === undefined ? 1 : L[j].qtd) + n0(x.qtd === undefined ? 1 : x.qtd); L.splice(i, 1) }
    }
  }

  const atr = (f, id) => { const a = (f.attrs || []).find(a => a.id == id); return a ? n0(a.v) : 0 };

  /* habilidade que o personagem já tem (escolha de marco ou trilha liberada) */
  function tem(f, nome) {
    const s = f.sfl, C = classe(s.classe), T = C && C.trilhas.find(t => t.id == s.trilha), nt = Math.ceil(s.marco / 2);
    return s.esc.some(e => e.k == 'hab' && e.n == nome) || !!(T && T.habs.some((h, i) => i < nt && h.n == nome));
  }
  const qtdDe = it => it.qtd === undefined ? 1 : n0(it.qtd);
  const ehBolso = it => n0(it.esp) == 0 && (it.bolso || it.tipo == 'arma') && it.tipo != 'mochila';
  const temMod = (it, id) => Array.isArray(it.mods) && it.mods.includes(id);
  /* espaços que um item ocupa (sem contar os de bolso, tamanho 0) */
  function espItem(it) {
    const q = qtdDe(it); if (q <= 0) return 0;
    if (it.tipo == 'mochila') return 0;
    if (it.tipo == 'armadura' && it.sub != 'escudo') return n0(it.esp) * (it.eq ? q - 1 : q);   // vestida não ocupa espaço
    if (ehBolso(it)) return 0;
    let e = n0(it.esp); if (temMod(it, 'alca-leve') && e >= 2) e -= 1;
    return it.pilha ? Math.ceil(q / n0(it.pilha)) * e : e * q;
  }
  const bolsoUn = it => qtdDe(it) <= 0 || !ehBolso(it) ? 0 : it.pilha ? Math.ceil(qtdDe(it) / n0(it.pilha)) : qtdDe(it);

  /* tudo que a ficha calcula sozinha */
  function derivar(f) {
    const s = f.sfl, C = classe(s.classe), O = origem(s.origem), b = s.bonus || {};
    const cor = atr(f, 'cor'), ref = atr(f, 'ref');
    const pvMax = Math.max(1, 10 + cor * 2 + (C && C.id == 'combatente' ? 4 : 0) + n0(b.pv) + s.esc.filter(e => e.k == 'vida').reduce((t, e) => t + n0(e.n), 0));
    const folMax = Math.max(0, 5 + ref + (C && C.id == 'batedor' ? 2 : 0) + n0(b.fol) - n0(s.adren));
    const itens = ((f.inv && f.inv.items) || []).filter(it => it && qtdDe(it) > 0);
    const moch = itens.filter(it => it.tipo == 'mochila' && it.eq).sort((x, y) => n0(y.mochila) - n0(x.mochila))[0];
    const slots = Math.max(0, 5 + 3 * Math.max(0, cor - 1) + (C && C.id == 'tecnico' ? 2 : 0) + (moch ? n0(moch.mochila) : 0) + n0(b.slots));
    const bolso = itens.reduce((t, it) => t + bolsoUn(it), 0), espBolso = Math.ceil(Math.max(0, bolso - 5) / 5);
    const usado = itens.reduce((t, it) => t + espItem(it), 0) + espBolso;
    const prontosMax = 2 + (moch ? n0(moch.prontos) : 0) + itens.filter(it => it.tipo != 'mochila' && n0(it.prontos)).reduce((t, it) => t + n0(it.prontos) * Math.min(1, qtdDe(it)), 0);
    const prontos = itens.filter(it => it.pronto).length;
    const arm = itens.filter(it => it.tipo == 'armadura' && it.sub != 'escudo' && it.eq).sort((x, y) => n0(y.red) - n0(x.red))[0];
    const escudo = itens.find(it => it.tipo == 'armadura' && it.sub == 'escudo' && (it.eq || it.pronto) && !it.quebrada);
    const desvArm = !arm ? [] : (Array.isArray(arm.desvVest) ? arm.desvVest : arm.sub == 'pesada' ? ['Parkour', 'Furtividade'] : []).filter(x => !(arm.sub == 'pesada' && tem(f, 'Armadura de campo') && (x == 'Parkour' || x == 'Furtividade') && !/sucata/i.test(arm.n || '')));
    const sobre = usado > slots, excesso = usado > slots + 3;
    const nTrilha = Math.ceil(s.marco / 2), nEsc = Math.floor(s.marco / 2);
    const extrasAtr = s.esc.filter(e => e.k == 'atr').length;
    const pontos = f.attrs.reduce((t, a) => t + n0(a.v), 0);
    const nivelPoder = !s.linha ? 0 : s.marco >= 8 ? 3 : s.marco >= 4 ? 2 : 1;
    const fonte = new Set([...(O ? O.pericias : []), ...s.perClasse]);
    const inf = n0((f.stats.find(x => x.id == 'inf') || {}).cur);
    const fol = n0((f.stats.find(x => x.id == 'pe') || {}).cur);
    const armasMax = 1 + (s.origem == 'militar' ? 1 : 0);
    /* movimento: 9 m; Pé na estrada +3; Impulso +2/+4 (não somam: vale o maior); sobrecarregado −3 m */
    const impulso = sobre ? 0 : s.impulso, peEstrada = tem(f, 'Pé na estrada') ? 3 : 0;
    const mov = 9 + Math.max(peEstrada, IMPULSO[impulso][1]) - (sobre ? 3 : 0);
    return { C, O, pvMax, folMax, slots, usado, sobre, excesso, bolso, espBolso, prontos, prontosMax, mochila: moch || null,
      armadura: arm ? n0(arm.red) : 0, armaduraNome: arm ? arm.n : '', armaduraTiro: arm && arm.redTiro ? n0(arm.redTiro) : 0, desvArm, escudo: escudo || null,
      nTrilha, nEsc, escPend: nEsc - s.esc.length, pontos, pontosMax: 10 + extrasAtr, nivelPoder, fonte, inf, fol, faixa: faixaInf(inf), armasMax,
      impulso, mov, peEstrada, trilha: C && C.trilhas.find(t => t.id == s.trilha) || null };
  }

  /* desvantagem automática de uma perícia: sobrecarga, armadura vestida, Fôlego 0 (esforço físico) e Medo 3+ */
  function desvAuto(f, D, nome) {
    const medo = n0((f.stats.find(x => x.id == 'medo') || {}).cur), L = [];
    if (D.sobre && (nome == 'Parkour' || nome == 'Furtividade')) L.push('sobrecarregado');
    if (D.desvArm.includes(nome)) L.push(D.armaduraNome || 'armadura');
    if (D.fol <= 0 && (nome == 'Parkour' || nome == 'Atletismo')) L.push('sem Fôlego');
    if (medo >= 3 && (nome == 'Vontade' || nome == 'Tiro' || nome == 'Arremesso')) L.push('Medo 3+');
    return L;
  }

  /* aplica a regra: máximos, perícias vindas de origem e classe. Devolve mensagens curtas. */
  function aplicar(f) {
    preparar(f);
    const s = f.sfl, msg = [];
    if (s.classeUlt !== undefined && s.classeUlt !== s.classe) { s.perClasse = []; s.trilha = ''; s.esc = s.esc.filter(e => e.k != 'hab') }
    s.classeUlt = s.classe;
    const D_ = derivar(f);
    const ult = s.ult || {}, alvo = { pv: D_.pvMax, pe: D_.folMax, medo: 5, inf: 10 };
    Object.entries(alvo).forEach(([id, mx]) => {
      const st = f.stats.find(x => x.id == id); if (!st) return;
      const antes = ult[id] === undefined ? n0(st.max) : n0(ult[id]);
      if (n0(st.max) != mx || ult[id] === undefined) {
        const novo = ult[id] === undefined && !n0(st.max) && !n0(st.cur), dif = mx - antes;
        if (novo) st.cur = (id == 'medo' || id == 'inf') ? 0 : mx;
        else if (dif > 0 && id != 'medo' && id != 'inf') { st.cur = n0(st.cur) + dif; if (ult[id] !== undefined) msg.push(`+${dif} ${st.n} máximo`) }
        else if (n0(st.cur) > mx) st.cur = mx;
        st.max = mx;
      }
      ult[id] = mx;
    });
    s.ult = ult;
    f.skills.forEach(k => { if (D_.fonte.has(k.n) && n0(k.t) < 3) k.t = 3 });
    return { D: D_, msg };
  }

  /* ---------- testes ---------- */
  const d20 = () => 1 + Math.floor(Math.random() * 20);
  /* atributo + dados extras (vantagem +1, desvantagem -1); reserva < 1 rola 2 e fica com o menor */
  function teste(at, extra, bonus) {
    const pool = n0(at) + n0(extra), q = pool >= 1 ? pool : 2, r = Array.from({ length: q }, d20), d = pool >= 1 ? Math.max(...r) : Math.min(...r);
    return { r, d, total: d + n0(bonus), q, baixo: pool < 1 };
  }
  const treinoDe = (f, nome) => { const k = f.skills.find(x => x.n == nome); return k ? n0(k.t) + n0(k.o) : 0 };
  const treinoArma = (f, fam) => { const a = (f.sfl.armas || []).find(x => x.f == fam); return a ? n0(a.t) : 0 };

  const PUNHOS = f => ({ n: 'Punhos', tipo: 'arma', virtual: 1, arma: { dano: f.sfl.origem == 'lutador-clandestino' ? '1d6' : '1d4', crit: '20 ×2', cat: 'contundente', traco: 'n/a',
    efeito: f.sfl.origem == 'lutador-clandestino' ? 'n/a (Lutador clandestino: o primeiro acerto desarmado da cena derruba)' : 'n/a' }, mods: [] });
  const modsDe = it => (Array.isArray(it.mods) ? it.mods : []).map(id => D.mods.find(m => m.id == id)).filter(Boolean);
  /* ataque de uma arma do inventário: dados, bônus, margem de crítico (com modificações) */
  function ataque(f, it, mirando) {
    const a = it.arma || {}, cat = a.cat || 'contundente', esp = cat == 'especial', fam = a.fam || familia(it.n || '');
    const melee = cat == 'contundente' || cat == 'cortante', M = modsDe(it);
    const dados = atr(f, melee ? 'cor' : 'ref');
    const nome = { contundente: 'Contundente', cortante: 'Cortante', arremesso: 'Arremesso', tiro: 'Tiro' }[cat];
    const treinada = !esp || (f.sfl.armas || []).some(x => x.f == fam);
    let bonus = esp ? treinoArma(f, fam) : treinoDe(f, nome);
    if (M.some(m => m.auto.dual)) bonus = Math.max(treinoDe(f, 'Contundente'), treinoDe(f, 'Cortante'));
    const c = critDe(a.crit), cm = /(\d+)\s*[–-]\s*\d+\s*ao mirar/.exec(a.crit || '');
    let crit = c ? { m: c.m, x: c.x } : null;
    if (crit && mirando && cm) crit.m = Math.min(crit.m, +cm[1]);
    if (crit && M.some(m => m.auto.crit)) crit.m -= 1;                        // Fio afiado: margem +1
    const mira = mirando && M.some(m => m.auto.mira) ? 1 : 0;                 // Mira: +1 dado depois de mirar
    const fx = [a.efeito && a.efeito != 'n/a' ? a.efeito : ''].concat(M.filter(m => m.auto.fx).map(m => m.auto.fx)).filter(Boolean);
    return { dados: dados + (treinada ? 0 : -1) + mira, bonus: treinada ? bonus : 0, treinada, crit, melee, rotulo: esp ? fam : nome, mira, fx, mods: M,
      podeMirar: !!cm || M.some(m => m.auto.mira), quebra: melee && !it.virtual && !(f.sfl.origem == 'lenhador' && (it.arma.tags || []).includes('machado')) };
  }

  function danoRolar(f, it, crit) {
    const a = it.arma || {}, c = critDe(a.crit), mult = crit ? Math.max(1, c ? c.x : 2) : 1, M = modsDe(it);
    const m = /(\d*)d(\d+)\s*([+-]\s*\d+)?/.exec(String(a.dano || '')); if (!m) return null;
    const extraD = M.some(x => x.auto.dados) ? 1 : 0;                         // Cano serrado: +1 dado
    const q = ((+m[1] || 1) + extraD) * mult, fc = +m[2], fixo = (m[3] ? +m[3].replace(/\s+/g, '') : 0) + M.reduce((t, x) => t + n0(x.auto.dano), 0);
    const r = Array.from({ length: Math.min(100, q) }, () => 1 + Math.floor(Math.random() * fc));
    const corpo = (a.cat == 'contundente' || a.cat == 'cortante') ? atr(f, 'cor') : 0;
    return { r, soma: Math.max(0, r.reduce((t, x) => t + x, 0) + fixo + corpo), corpo, fixo, q, fc, mult };
  }

  /* ---------- modificações de arma (livro V1.2, 13.4) ---------- */
  const tagsDe = it => { const t = new Set(((it.arma || {}).tags) || []), c = (it.arma || {}).cat;
    if (c == 'contundente' || c == 'cortante' || it.sub == 'escudo') t.add('corpo'); if (c == 'contundente' || it.sub == 'escudo') t.add('cont'); if (c == 'cortante') t.add('cort');
    if (n0(it.esp) >= 2) t.add('grande'); return t };
  const limiteMods = it => it.sub == 'escudo' ? D.limites.escudo : n0(D.limites[(it.arma || {}).g] || 0);
  function modServe(it, m) {
    const t = tagsDe(it);
    return m.pp.every(p => p[0] == '!' ? !t.has(p.slice(1)) : true) && m.pp.filter(p => p[0] != '!').some(p => t.has(p))
      && (m.id != 'contrapeso' || t.has('corpo'));
  }
  const modsPossiveis = it => D.mods.filter(m => modServe(it, m));

  /* ---------- materiais no inventário ---------- */
  const casa = (it, chave) => chave.split('|').some(k => { const a = norm(it.n), b = norm(k); return a == b || a.startsWith(b + ' ') || a.startsWith(b + ' (') });
  const temMat = (f, chave) => f.inv.items.filter(it => it && casa(it, chave)).reduce((t, it) => t + qtdDe(it), 0);
  const faltaMat = (f, mat) => Object.entries(mat || {}).filter(([k, q]) => temMat(f, k) < q).map(([k, q]) => `${q - temMat(f, k)} ${k.split('|')[0]}`);
  function gastaMat(f, mat, frac) {
    Object.entries(mat || {}).forEach(([k, q]) => {
      let falta = frac ? Math.ceil(q * frac) : q;
      for (const it of f.inv.items.filter(x => x && casa(x, k))) { if (falta <= 0) break; const u = Math.min(falta, qtdDe(it)); it.qtd = qtdDe(it) - u; falta -= u }
    });
    f.inv.items = f.inv.items.filter(it => !it || it.tipo == 'arma' || it.tipo == 'armadura' || qtdDe(it) > 0 || !['municao', 'material', 'consumivel'].includes(it.tipo));
  }
  /* põe um item do catálogo no inventário (junta com a pilha que já existe) */
  function poeItem(f, nome, q) {
    const c = CATn.get(norm(nome)) || CAT.find(x => norm(x.n).startsWith(norm(nome)));
    const igual = c && ['municao', 'material', 'consumivel'].includes(c.tipo) && f.inv.items.find(it => it && norm(it.n) == norm(c.n) && it.usos === undefined);
    if (igual) { igual.qtd = qtdDe(igual) + q; return igual }
    const it = c ? JSON.parse(JSON.stringify(c)) : { n: nome, tipo: 'material', esp: 1, pilha: 5 };
    delete it.lote; it.id = S.uid(); it.qtd = c && c.tipo == 'arma' ? 1 : q; it.eq = false; it.cv = CV; if (it.tipo == 'arma') it.mods = [];
    f.inv.items.push(it);
    for (let i = 1; c && c.tipo == 'arma' && i < q; i++) { const o = JSON.parse(JSON.stringify(it)); o.id = S.uid(); f.inv.items.push(o) }
    return it;
  }

  /* ---------- parkour (livro V1.0, cap. 12) ---------- */
  const IMPULSO = [[0, 0, 'Normal'], [1, 2, '+2 m de movimento'], [2, 4, '+4 m de movimento'], [3, 4, '+4 m e vantagem no próximo teste de Parkour']];
  const MOVIMENTOS = [['Passar por um obstáculo baixo', 0, 0], ['Deslizar por baixo de um obstáculo', 10, 0], ['Escalar um muro de 2 m', 12, 1], ['Saltar entre telhados próximos', 15, 1],
    ['Correr alguns passos pela parede', 18, 1], ['Escalar uma fachada difícil', 20, 2], ['Saltar entre prédios distantes', 22, 2]];
  const ESTAGIOS = ['', 'Alcançado', 'Muito perto', 'Perto', 'Distância média', 'Longe', 'Escapou'];
  function parkourResultado(total, dt) {
    const m = total - dt;
    if (m >= 0) return { ok: true, k: 0, t: 'Sucesso: faz o movimento.' };
    if (m >= -4) return { ok: true, k: 1, t: 'Falha por 1 a 4: consegue, mas perde tempo ou 1 Fôlego a mais.' };
    if (m >= -9) return { ok: false, k: 2, t: 'Falha por 5 a 9: não completa (fica preso, faz barulho ou muda de rota).' };
    return { ok: false, k: 3, t: 'Falha por 10 ou mais: complicação grave (queda, ferimento). Falha não é queda automática.' };
  }

  /* ---------- catálogo (loja e inventário): armas, munição, armaduras, carga, exploração, médicos, comida, ferramentas e materiais ---------- */
  const CV = 2;   // versão das regras de item (livro V1.2)
  const limpa = o => { Object.keys(o).forEach(k => (o[k] === undefined || o[k] === null) && delete o[k]); return o };
  const CAT = D.armas.filter(a => a.n != 'Punhos').map(a => limpa({ ref: 'sfl:' + a.n, n: a.n, tipo: 'arma', esp: a.esp === undefined ? (/2 mãos/.test(a.n) ? 2 : 1) : a.esp, pilha: a.pilha,
    bolso: a.esp === 0 ? 1 : undefined, qtd: 1, preco: a.preco, rar: a.rar, fab: a.fab, desc: a.traco === 'n/a' ? '' : a.traco, mods: [],
    arma: { dano: a.dano, crit: a.crit, cat: a.cat, fam: a.cat == 'especial' ? familia(a.n) : '', traco: a.traco, efeito: a.efeito, esp: a.cat == 'especial', g: a.g, tags: a.tags } }))
    .concat([limpa({ ref: 'sfl:Escudo', n: 'Escudo (policial ou improvisado)', tipo: 'armadura', sub: 'escudo', red: 0, esp: 2, qtd: 1, preco: 60, rar: 'Incomum', mods: [], desc: 'Bloqueio com escudo usa ÷3 do teste. Só quebra com 1 natural num bloqueio que falhou.' })])
    .concat(D.itens.map(x => limpa(Object.assign({ ref: 'sfl:' + x.n, qtd: x.lote || 1, desc: x.d }, x, { d: undefined }))))
    .concat([['Armadura leve', 1, 1, 'leve'], ['Armadura média', 2, 2, 'média'], ['Armadura pesada', 3, 3, 'pesada']].map(([n, e, r, sub]) =>
      ({ ref: 'sfl:' + n, n, tipo: 'armadura', esp: e, red: r, sub, qtd: 1, desc: 'Armadura genérica: reduz ' + r + ' de dano' + (sub == 'pesada' ? '; desvantagem em Parkour e Furtividade.' : '.') })));
  const CATn = new Map(CAT.map(x => [norm(x.n), x]));
  S.CATALOGO.sfl = CAT;
  const GRUPOS = [['arma', 'Armas'], ['municao', 'Munição e combustível'], ['armadura', 'Armaduras e escudo'], ['mochila', 'Mochilas'], ['geral', 'Equipamento'], ['consumivel', 'Médicos e comida'], ['material', 'Materiais']];
  const dinTxt = v => v === undefined || v === null ? '' : v.toLocaleString('pt-BR') + ' €';
  /* etiquetas curtas de um item: espaços, pilha, raridade, preço */
  function etiquetas(it) {
    const e = n0(it.esp), L = [];
    if (it.tipo == 'mochila') L.push('+' + n0(it.mochila) + ' espaços');
    else if (ehBolso(it)) L.push('bolso (tamanho 0)' + (it.pilha ? ' · pilha de ' + it.pilha : ''));
    else if (it.tipo == 'armadura' && it.sub != 'escudo') L.push('vestida: 0 · carregada: ' + e + ' esp.');
    else L.push(e + ' esp.' + (it.pilha ? ' por pilha de ' + it.pilha : ''));
    if (n0(it.prontos)) L.push('+' + it.prontos + ' item pronto');
    if (it.rar) L.push(it.rar + (it.fab && it.rar != 'Fabricável' ? ' · fabricável' : ''));
    if (it.preco) L.push(dinTxt(it.preco) + (it.lote ? ' a pilha' : ''));
    return L;
  }

  /* símbolo do dinheiro: SFL usa euro, a moeda da Estônia, a não ser que o mestre escolha outro */
  S.moedaDe = camp => { const m = camp && camp.config && camp.config.moeda; return camp && camp.sistema == 'sfl' ? (m && m != 'R$' ? m : '€') : (m || 'R$') };

  S.sfl = { ATR, PERICIAS, TREINO, FAIXAS, faixaInf, BENEFICIOS, ESPECIAIS, classe, origem, linha, familia, critDe, preparar, derivar, aplicar, teste, treinoDe, treinoArma, ataque, danoRolar, atr, CAT, dados: D,
    tem, espItem, desvAuto, PUNHOS, modsDe, modsPossiveis, modServe, limiteMods, temMat, faltaMat, gastaMat, poeItem, IMPULSO, MOVIMENTOS, ESTAGIOS, parkourResultado, GRUPOS, etiquetas, dinTxt, norm, qtdDe };
})();
