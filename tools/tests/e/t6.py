from lib import *
d=seed();M=q
def xy(tid): return M(f"select to_jsonb(array[x,y]) from public.tokens where id='{tid}'")
with sync_playwright() as p:
    b=p.chromium.launch()
    for u,tid,mode,X,Y in (('M',d['tGob'],'upsert',420,330),('J',d['tGob'],'rpc',610,270)):
        pg=abre(b,u,d);ev=pg.evaluate
        x0=xy(tid)
        ev("window.__offline=true")
        ev(f"(()=>{{const t=S.tok.find(t=>t.id=='{tid}');t.x={X};t.y={Y};save()}})()");pg.wait_for_timeout(1500)
        chk(f"{u}: sem rede nao grava",xy(tid)==x0)
        chk(f"{u}: sem rede o aviso aparece","offline" in ev("document.getElementById('cs').textContent") or "conex" in ev("document.getElementById('cs').textContent"),ev("document.getElementById('cs').textContent"))
        chk(f"{u}: sem rede a tela mantem a mudanca local",ev(f"S.tok.find(t=>t.id=='{tid}').x")==X)
        ev("window.__offline=false");pg.wait_for_timeout(6500)
        chk(f"{u}: com a rede de volta, grava sozinho",xy(tid)==[X,Y],xy(tid))
        chk(f"{u}: e mostra salvo","salvo" in ev("document.getElementById('cs').textContent"))
        pg.ctx.close()
    # recusa do servidor NAO fica em loop de tentativas
    pg=abre(b,'J',d);ev=pg.evaluate
    ev("__calls.length=0")
    ev(f"S.tok.find(t=>t.id=='{d['tLacaio']}').x=900;save()");pg.wait_for_timeout(2500)
    n=len([c for c in ev("__calls") if c=='rpc mover_token'])
    chk("recusa do servidor: nao fica tentando de novo",n<=1,n)
    chk("sem erros de console",not pg.errs,pg.errs)
    b.close()
report()
