from lib import *
d=seed()
with sync_playwright() as p:
    b=p.chromium.launch()
    pm=abre(b,'M',d);pm.wait_for_timeout(600)
    pm.click("[data-a=rm]");pm.evaluate(f"(()=>{{sel=S.tok.find(t=>t.id=='{d['tGob']}');tmOpen=true;ui();place()}})()");pm.wait_for_timeout(300)
    pm.screenshot(path=S+'/s_mestre.png')
    pj=abre(b,'J',d);pj.wait_for_timeout(600);pj.screenshot(path=S+'/s_jogador.png')
    # sem cena ativa
    pgx.admin(f"update public.mesas set cena_ativa=null where id='{d['m']}'")
    pj2=abre(b,'K',d);pj2.wait_for_timeout(500);pj2.screenshot(path=S+'/s_espera.png')
    # escolha de mesa: usuario sem mesa e usuario com 2 mesas
    pgx.admin(f"insert into public.mesas(nome,mestre_id) values ('Outra Mesa','{U['J']}')")
    ctx=b.new_context(viewport={"width":420,"height":800});ctx.route("**/@supabase/supabase-js@2",lambda r:r.fulfill(status=200,content_type="application/javascript",body=MOCK))
    ctx.add_init_script("localStorage.setItem('me','%s')"%U['J']);ctx.expose_function("pgcall",lambda s:json.dumps(pgx.handle(json.loads(s)),default=str))
    pg=ctx.new_page();pg.goto(URL);pg.wait_for_selector('#mx-pick');pg.screenshot(path=S+'/s_escolha.png')
    chk("escolha de mesa lista as 2 mesas",pg.locator('#mx-pick [data-m]').count()==2)
    pg.click('#mx-pick [data-m] >> nth=0');pg.wait_for_function("document.getElementById('cs')&&/salvo/.test(document.getElementById('cs').textContent)",timeout=10000)
    chk("escolher mesa abre e lembra",pg.evaluate("localStorage.mesa_atual")!=None)
    ctx2=b.new_context();ctx2.route("**/@supabase/supabase-js@2",lambda r:r.fulfill(status=200,content_type="application/javascript",body=MOCK))
    ctx2.add_init_script("localStorage.setItem('me','%s')"%U['X']);ctx2.expose_function("pgcall",lambda s:json.dumps(pgx.handle(json.loads(s)),default=str))
    px=ctx2.new_page();px.goto(URL);px.wait_for_selector('#mx-pick');chk("usuario sem mesa ve orientacao","nenhuma mesa" in px.inner_text('#mx-pick'))
    b.close()
report()
