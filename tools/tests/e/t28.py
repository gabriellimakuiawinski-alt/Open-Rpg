# excluir campanha, mesa e ficha pela tela inicial
from lib2 import *
d=seed()
CID=ids(9,1)
with sync_playwright() as p:
    b=p.chromium.launch()
    pj=abre_pg(b,'J','index.html');pj.wait_for_timeout(2800)
    pj.evaluate("location.hash='#/c/%s'"%CID);pj.wait_for_timeout(900)
    n0=q("select to_jsonb(count(*)) from public.personagens where id='%s'"%d['fJ'])
    chk("ficha do jogador tem botão Excluir",pj.locator('.fch .exc').count()>=1)
    chk("jogador não vê Excluir na campanha",pj.locator('.camp .exc').count()==0)
    pj.locator('.fch .exc').first.click();pj.wait_for_timeout(500)
    pj.click('button.perigo[type=submit]');pj.wait_for_timeout(1200)
    chk("ficha excluída no banco",q("select to_jsonb(count(*)) from public.personagens where id='%s'"%d['fJ'])==0)
    pm=abre_pg(b,'M','index.html');pm.wait_for_timeout(2800)
    pm.wait_for_timeout(1500)
    try: pm.locator('.camp .exc').first.wait_for(timeout=8000);ok=True
    except Exception: ok=False
    chk("mestre vê Excluir na campanha",ok)
    pm.locator('.camp .exc').first.click();pm.wait_for_timeout(500)
    pm.click('button.perigo[type=submit]');pm.wait_for_timeout(1200)
    chk("campanha excluída",q("select to_jsonb(count(*)) from public.campanhas where id='%s'"%CID)==0)
    chk("sem erros",not pj.errs and not pm.errs,(pj.errs,pm.errs))
    b.close()
report()
