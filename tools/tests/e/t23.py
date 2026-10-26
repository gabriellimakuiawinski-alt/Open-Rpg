# Aba "Criadas" do seletor de habilidades
from lib2 import *
d=seed()
# uma habilidade criada em OUTRA ficha do mesmo jogador
pgx.admin("""insert into public.personagens(id,user_id,campanha_id,nome,dados) values ('%s','%s','%s','Outra ficha do J',
  '{"poderes":[{"id":"x1","n":"Golpe Sombrio","tipo":"homebrew","desc":"Meu golpe","pe":2,"ef":[]}]}')"""%(ids(5,2),U['J'],ids(9,1)))
with sync_playwright() as p:
    b=p.chromium.launch()
    pg=abre_pg(b,'J','ficha.html?id='+d['fJ']);pg.wait_for_timeout(2000);ev=pg.evaluate
    pg.click('[data-tab=h]');pg.click('[data-act="op-livro"]');pg.wait_for_timeout(500)
    abas=pg.locator('#md [data-f^="gr:"]').all_inner_texts()
    chk("Criadas é a última aba",abas[-1]=='Criadas',abas)
    pg.click('#md [data-f="gr:criadas"]');pg.wait_for_timeout(300)
    chk("lista tem 'Criar habilidade nova' e a habilidade de outra ficha",pg.locator('#md .cat-i:has-text("Criar habilidade nova")').count()==1 and pg.locator('#md .cat-i:has-text("Golpe Sombrio")').count()==1)
    pg.locator('#md .cat-i:has-text("Golpe Sombrio")').click();pg.wait_for_timeout(500)
    chk("reutilizar copia a habilidade para esta ficha",ev("curF().poderes.some(p=>p.n=='Golpe Sombrio'&&p.pe==2&&!p.ref)"))
    pg.click('[data-act="op-livro"]');pg.click('#md [data-f="gr:criadas"]');pg.wait_for_timeout(300)
    chk("marca como já na ficha",'já na ficha' in pg.locator('#md .cat-i:has-text("Golpe Sombrio")').inner_text())
    pg.locator('#md .cat-i:has-text("Criar habilidade nova")').click();pg.wait_for_timeout(600)
    chk("criar nova abre uma habilidade em branco na aba Habilidades",ev("curF().poderes.some(p=>p.n==''&&p.tipo=='poder')") and pg.locator('#md').count()==0)
    chk("sem erros",not [e for e in pg.errs if 'net::' not in e],pg.errs)
    b.close()
report()
