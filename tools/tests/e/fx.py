from lib import *
d=seed()
errs=[]
with sync_playwright() as p:
    b=p.chromium.launch()
    pg=abre(b,'M',d);pg.on('pageerror',lambda e:errs.append(str(e)));pg.wait_for_timeout(900)
    chk("camada fx criada",pg.locator('#fx').count()==1)
    pg.evaluate(f"(()=>{{sel=S.tok.find(t=>t.id=='{d['tGob']}');draw()}})()")
    pg.click('#dcb');pg.wait_for_timeout(120);pg.screenshot(path=S+'/fx_painel.png')
    pg.wait_for_timeout(400)
    pg.click('#dc [data-d="20"]');pg.wait_for_timeout(500);pg.screenshot(path=S+'/fx_dado.png')
    pg.evaluate("MesaFX.onda(400,300,60);MesaFX.burst(400,300,20)");pg.wait_for_timeout(200);pg.screenshot(path=S+'/fx_onda.png')
    chk("dado mostra resultado animado",pg.locator('.fx-dado').count()>=1)
    chk("sem erros de script",not errs,errs)
report()
