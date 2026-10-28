# SFL: criar campanha com o sistema, moeda euro por padrão, catálogo SFL na loja
from lib2 import *
d=seed()
with sync_playwright() as p:
    b=p.chromium.launch()
    pg=abre_pg(b,'M','index.html',sess=True);pg.wait_for_timeout(2800)
    pg.evaluate("setTimeout(novaCamp,0)");pg.wait_for_timeout(500)
    chk("opção Search For Light",'Search For Light' in pg.inner_text('#jan select[name=sistema]'))
    pg.select_option('#jan select[name=sistema]','sfl');pg.wait_for_timeout(200)
    chk("complementos de Ordem somem",not pg.locator('#jan fieldset.comps').is_visible())
    pg.fill('#jan input[name=nome]','Camp SFL');pg.click('#jan [type=submit]');pg.wait_for_timeout(1800)
    r=pgx.aj("select to_jsonb(c) from public.campanhas c where nome='Camp SFL'")
    chk("sistema sfl gravado",r and r['sistema']=='sfl',r)
    chk("moeda € por padrão",r and r['config'].get('moeda')=='€',r)
    chk("sem erros",not pg.errs,pg.errs)
    cid=r['id']
    pg2=abre_pg(b,'M','loja.html?camp='+cid);pg2.wait_for_timeout(2200)
    chk("loja usa € como moeda",pg2.evaluate("moeda()")=='€',pg2.evaluate("moeda()"))
    chk("sem erros na loja",not pg2.errs,pg2.errs)
    n=pg2.evaluate("SIS.CATALOGO.sfl.length")
    chk("catálogo SFL com 58 itens",n==58,n)
    b.close()
report()
