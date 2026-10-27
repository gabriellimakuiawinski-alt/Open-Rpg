# complementos (SaH): escolha na campanha filtra o catálogo; etiqueta; equipar item com bônus; aliado; Bateria Potente
from lib2 import *
d=seed()
camp=ids(9,1)
def cfg(j): pgx.admin(f"update public.campanhas set config='{j}'::jsonb, sistema='op' where id='{camp}'")
def abre_cat(b):
    pg=abre_pg(b,'J','ficha.html?id='+d['fJ']);pg.wait_for_timeout(2000)
    pg.click('[data-tab=g]');pg.evaluate("document.querySelectorAll('details.mais').forEach(d=>d.open=true)");pg.fill('[data-p="op.pp"]','200');pg.press('[data-p="op.pp"]','Tab');pg.wait_for_timeout(400)
    pg.click('[data-tab=i]');pg.click('[data-act="op-cat"]');pg.wait_for_timeout(600)
    return pg
with sync_playwright() as p:
    b=p.chromium.launch()
    cfg('{}')
    pg=abre_cat(b);abas=pg.locator('#md [data-ab]').all_inner_texts()
    chk("sem complemento: não há aba Medicamentos",'Medicamentos' not in abas,abas)
    pg.fill('#catq','shuriken');chk("sem complemento: Shuriken não aparece",pg.locator('#md .cat-i').count()==0)
    pg.fill('#catq','celular');chk("sem complemento: Celular genérico continua",pg.locator('#md .cat-i').count()==1 and 'sah' not in pg.inner_text('#md').lower())
    pg.close()
    cfg('{"complementos":["sah"]}')
    pg=abre_cat(b);abas=pg.locator('#md [data-ab]').all_inner_texts()
    chk("com SaH: aba Medicamentos",'Medicamentos' in abas,abas)
    pg.click('#md [data-ab="medicamento"]');pg.wait_for_timeout(300)
    chk("8 medicamentos",pg.locator('#md .cat-i').count()==8,pg.locator('#md .cat-i').count())
    chk("etiqueta SaH no catálogo",pg.locator('#md .compt').count()>=8)
    pg.fill('#catq','celular');pg.wait_for_timeout(200)
    chk("Celular do SaH substitui o genérico",pg.locator('#md .cat-i').count()==1 and 'sah' in pg.inner_text('#md').lower(),pg.inner_text('#md .catl'))
    pg.fill('#catq','amuleto');pg.locator('#md .cat-i:has-text("Amuleto Sagrado")').click();pg.wait_for_timeout(400)
    A="curF().inv.items.find(i=>i.n=='Amuleto Sagrado')"
    chk("item guarda comp=sah",ev_:=pg.evaluate(A+".comp")=='sah')
    chk("etiqueta SaH no inventário",pg.locator('.op-it .compt').count()>=1)
    rel="SIS.aplicar(curF(),SIS.cfgDe(CAMPS.find(c=>c.id==curF()._camp))).D.per['Religião']||0"
    chk("sem vestir: sem bônus",pg.evaluate(rel)==0,pg.evaluate(rel))
    chk("botão Equipar aparece",pg.locator('.op-it:has(input[value="Amuleto Sagrado"]) [data-act="op-eq"]').count()==1)
    pg.locator('.op-it:has(input[value="Amuleto Sagrado"]) [data-act="op-eq"]').click();pg.wait_for_timeout(300)
    chk("vestido: +2 em Religião",pg.evaluate(rel)==2,pg.evaluate(rel))
    # aliado + item: soma; Cão Adestrado
    pg.click('[data-act="op-cat"]');pg.wait_for_timeout(300);pg.fill('#catq','cão');pg.locator('#md .cat-i:has-text("Cão Adestrado")').click();pg.wait_for_timeout(300)
    inv="SIS.aplicar(curF(),SIS.cfgDe(CAMPS.find(c=>c.id==curF()._camp))).D.per['Investigação']||0"
    chk("Cão Adestrado: +2 em Investigação",pg.evaluate(inv)==2,pg.evaluate(inv))
    # Bateria Potente no celular
    pg.click('[data-act="op-cat"]');pg.wait_for_timeout(300);pg.fill('#catq','celular');pg.locator('#md .cat-i:has-text("Celular")').click();pg.wait_for_timeout(300)
    C="curF().inv.items.find(i=>i.n=='Celular')"
    chk("Celular tem luz de 4,5 m",pg.evaluate(C+".luz.m")==4.5)
    pg.click('[data-act="op-cat"]');pg.wait_for_timeout(300);pg.click('#md [data-ab="modificacao"]')
    nomes=pg.locator('#md .cat-i b').all_inner_texts();chk("modificações do SaH listadas",any('Bateria' in x for x in nomes) and any('Carregador' in x for x in nomes) and any('Lente' in x for x in nomes),nomes)
    pg.locator('#md .cat-i:has-text("Bateria Potente")').click();pg.wait_for_timeout(400)
    pg.locator('#md .cat-i[data-i]:has-text("Celular")').first.click();pg.wait_for_timeout(600)
    chk("Bateria Potente dobra a luz",pg.evaluate(C+".luz.m")==9,pg.evaluate(C+".luz.m"))
    # medicamento no inventário
    chk("sem erros",not pg.errs,pg.errs)
    b.close()
report()
