# condições do livro: página de regras e marcar condição na ficha
from lib2 import *
d=seed()
with sync_playwright() as p:
    b=p.chromium.launch()
    pr=abre_pg(b,'J','regras.html');pr.wait_for_timeout(2500)
    chk("36 condições listadas",pr.locator('.rg').count()==36,pr.locator('.rg').count())
    pr.fill('#q','sangrando');pr.wait_for_timeout(300)
    chk("busca acha Sangrando",pr.locator('.rg').count()==1 and 'Vigor' in pr.inner_text('.rg'))
    pr.fill('#q','');pr.click('[data-t="perigo"]');pr.wait_for_timeout(300)
    chk("perigos agrupados",pr.locator('h2').count()>=4,pr.locator('h2').all_inner_texts())
    pr.click('[data-t="regra"]');pr.wait_for_timeout(300)
    chk("aba Cálculos",pr.locator('.rg').count()==9,pr.locator('.rg').count())
    pg=abre_pg(b,'J','ficha.html?id='+d['fJ']);pg.wait_for_timeout(2000);ev=pg.evaluate
    pg.click('[data-tab=c]');pg.click('[data-act="op-cond"]');pg.wait_for_timeout(600)
    pg.locator('#md .cat-i[data-n="Vulnerável"]').click();pg.wait_for_timeout(500)
    chk("condição marcada",ev("curF().op.cond.join()")=='Vulnerável')
    chk("texto da regra aparece na ficha",'Defesa' in pg.inner_text('.card:has(h2:text-is("Condições"))'))
    pg.locator('[data-act="op-cond-x"]').click();pg.wait_for_timeout(400)
    chk("remover condição",ev("(curF().op.cond||[]).length")==0)
    chk("sem erros",not pr.errs and not pg.errs,(pr.errs,pg.errs))
    b.close()
report()
