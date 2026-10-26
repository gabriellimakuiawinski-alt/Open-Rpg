# Etapa 8: pedido ao mestre quando a patente não permite a modificação
from lib2 import *
d=seed()
CID=ids(9,1)
with sync_playwright() as p:
    b=p.chromium.launch()
    pg=abre_pg(b,'J','ficha.html?id='+d['fJ']);pg.wait_for_timeout(2000);ev=pg.evaluate
    pg.click('[data-tab=i]');pg.click('[data-act="op-cat"]');pg.wait_for_timeout(400)
    pg.fill('#catq','katana');pg.locator('#md .cat-i:has-text("Katana")').click();pg.wait_for_timeout(300)
    pg.click('[data-act="op-cat"]');pg.click('#md [data-ab="modificacao"]');pg.locator('#md .cat-i:has-text("Certeira")').click();pg.wait_for_timeout(300)
    pg.locator('#md .cat-i:has-text("Katana")').click();pg.wait_for_timeout(400)
    chk("patente bloqueia e oferece pedido",pg.locator('#md [data-env]').count()==1)
    pg.click('#md [data-env]');pg.wait_for_timeout(800)
    chk("pedido gravado como pendente",q("select to_jsonb(count(*)) from public.pedidos where estado='pendente' and autor='%s'"%U['J'])==1)
    chk("ficha mostra o pedido esperando",'esperando o mestre' in pg.inner_text('body'))
    chk("arma ainda sem modificação",ev("curF().inv.items.find(i=>i.n=='Katana').mods===undefined||curF().inv.items.find(i=>i.n=='Katana').mods.length==0"))
    r=pgx.run(U['J'],"update public.pedidos set estado='aprovado' returning 1")
    chk("jogador não consegue aprovar o próprio pedido",bool(r.get('error')),r)
    r=pgx.run(U['K'],"select coalesce(jsonb_agg(id),'[]'::jsonb) from public.pedidos")
    chk("outro jogador não vê o pedido",r.get('data')==[],r)
    # mestre decide
    pm=abre_pg(b,'M','index.html#/c/'+CID);pm.wait_for_timeout(2500)
    pm.click('[data-t="pedidos"]');pm.wait_for_timeout(400)
    chk("mestre vê o pedido",pm.locator('#corpo:has-text("Certeira em Katana")').count()==1)
    pm.fill('[id^="pr-"]','Pode, mas só essa.');pm.click('[data-v="aprovado"]');pm.wait_for_timeout(900)
    chk("pedido aprovado no banco",q("select to_jsonb(count(*)) from public.pedidos where estado='aprovado' and resposta='Pode, mas só essa.'")==1)
    # ficha do jogador aplica sozinha ao abrir
    pg.reload();pg.wait_for_timeout(2500);pg.click('[data-tab=i]');pg.wait_for_timeout(1200)
    chk("ficha aplica a modificação aprovada",ev("curF().inv.items.find(i=>i.n=='Katana').mods.some(m=>m.n=='Certeira')"))
    chk("pedido marcado como aplicado",q("select to_jsonb(count(*)) from public.pedidos where estado='aplicado'")==1)
    chk("sem erros",not pg.errs and not pm.errs,(pg.errs,pm.errs))
    b.close()
report()
