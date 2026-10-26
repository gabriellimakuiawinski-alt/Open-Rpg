from lib import *
d=seed();M=q
with sync_playwright() as p:
    b=p.chromium.launch()
    # a) mesa sem cenas: o mestre abre e a cena 1 nasce ativa
    pgx.admin("delete from public.cenas")
    pm=abre(b,'M',d);ev=pm.evaluate;pm.wait_for_timeout(1200)
    chk("mesa vazia: cria 'Cena 1'",M("select to_jsonb(count(*)) from public.cenas")==1)
    cid=M("select to_jsonb(id::text) from public.cenas limit 1")
    chk("mesa vazia: cena 1 ja e a ativa",M("select to_jsonb(cena_ativa::text) from public.mesas")==cid,M("select to_jsonb(cena_ativa::text) from public.mesas"))
    chk("mesa vazia: painel de assets abre",ev("dkx")==True)
    # b) jogador entra antes de existir cena ativa -> espera -> mestre ativa -> carrega
    pgx.admin("update public.mesas set cena_ativa=null")
    pj=abre(b,'J',d)
    chk("jogador sem cena ativa ve a espera",pj.evaluate("getComputedStyle(document.getElementById('espera')).display")=='flex')
    pgx.run(U['M'],f"select public.ativar_cena('{cid}')");emit(pj,'mesas','UPDATE',d['m']);pj.wait_for_timeout(900)
    chk("jogador sai da espera quando o mestre ativa",pj.evaluate("getComputedStyle(document.getElementById('espera')).display")=='none' and pj.evaluate("S.cur")==cid,pj.evaluate("[S.cur,getComputedStyle(document.getElementById('espera')).display]"))
    # c) excluir a cena ativa: outra assume
    ev("sedit(null)");pm.fill('#e_n','Segunda');pm.click('[data-a=e_ok]');pm.wait_for_timeout(1000)
    ev(f"loadScene('{cid}')");pm.wait_for_timeout(300)
    ev(f"edit('{cid}')");pm.click('[data-a=e_del]');pm.wait_for_timeout(1500)
    chk("excluir cena ativa: some do banco",M(f"select to_jsonb(count(*)) from public.cenas where id='{cid}'")==0)
    chk("excluir cena ativa: outra vira ativa",M("select to_jsonb(cena_ativa is not null) from public.mesas")==True,M("select to_jsonb(cena_ativa::text) from public.mesas"))
    chk("excluir cena ativa: sem erros",not pm.errs,pm.errs)
    # d) janela do espectador
    pv=pm.ctx.new_page();pv.errs=[];pv.on("pageerror",lambda e:pv.errs.append(str(e)))
    # reabrir com dados completos
    d=seed()
    pm.goto(URL+"?mesa="+d['m']);pm.wait_for_function("document.getElementById('cs')&&/salvo/.test(document.getElementById('cs').textContent)",timeout=15000);pm.wait_for_timeout(800)
    pv.goto(URL+"#view");pv.wait_for_timeout(1800)
    chk("espectador: biblioteca carregada",pv.evaluate("LIB.size")>=3,pv.evaluate("LIB.size"))
    pm.evaluate(f"(()=>{{const t=S.tok.find(t=>t.id=='{d['tGob']}');t.x=555;save()}})()");pv.wait_for_timeout(900)
    chk("espectador: recebe o movimento do mestre",pv.evaluate("(S.tok||[]).some(t=>t.x==555)"),pv.evaluate("JSON.stringify((S.tok||[]).map(t=>t.x))"))
    chk("espectador: nao grava nada",not [c for c in pv.evaluate("__calls") if c.split()[0] in('insert','upsert','update','delete')],pv.evaluate("__calls"))
    chk("espectador sem erros",not pv.errs,pv.errs)
    b.close()
report()
