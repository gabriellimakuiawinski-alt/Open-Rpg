# ocultista aprende 1 ritual a cada NEX (livro p.33); círculo máximo por NEX
from lib2 import *
d=seed()
with sync_playwright() as p:
    b=p.chromium.launch()
    pg=abre_pg(b,'J','ficha.html?id='+d['fJ']);pg.wait_for_timeout(2000);ev=pg.evaluate
    ev("(()=>{const f=curF();f.op.classe='ocultista';f.op.nex=5;f.op.visto=1;f.op.avisos=[];f.poderes=[];render()})()");pg.wait_for_timeout(300)
    ev("(()=>{const f=curF();f.op.nex=10;OP.calc(f);touch(f);render()})()");pg.wait_for_timeout(500)
    ks=ev("curF().op.avisos.map(a=>a.k).join()")
    chk("subir para NEX 10 gera aviso de ritual",'ritual' in ks,ks)
    pg.locator('[data-act="op-hab"]:has-text("Escolher ritual")').first.click();pg.wait_for_timeout(700)
    H=pg.locator('#md .catl > p b').all_text_contents();chk("NEX 10: só rituais de 1º círculo",H==['1º círculo'],H)
    pg.locator('#md .cat-i').first.click();pg.wait_for_timeout(500)
    chk("ritual entra na ficha e o aviso some",ev("curF().poderes.some(p=>String(p.ref||'').startsWith('livro:op:ritual'))") and 'ritual' not in ev("curF().op.avisos.map(a=>a.k).join()"))
    ev("(()=>{const f=curF();f.op.nex=25;OP.calc(f);touch(f);render()})()");pg.wait_for_timeout(500)
    ev("OP.calc(curF())")
    pg.locator('[data-act="op-hab"]:has-text("Escolher ritual")').first.click();pg.wait_for_timeout(700)
    H=pg.locator('#md .catl > p b').all_text_contents();chk("NEX 25: aparece o 2º círculo",H==['1º círculo','2º círculo'],H)
    chk("sem erros",not pg.errs,pg.errs)
    b.close()
report()
