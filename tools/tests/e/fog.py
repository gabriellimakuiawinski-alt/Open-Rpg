from lib import *
import json
d=seed()
cena=pgx.aj(f"select to_jsonb(cena_ativa) from public.mesas where id='{d['m']}'")
pgx.admin(f"update public.cenas set escuro=true, escuridao=.9, nevoa='[{{\"t\":\"r\",\"x\":400,\"y\":200,\"w\":300,\"h\":200}}]'::jsonb, paredes='[{{\"x1\":300,\"y1\":100,\"x2\":300,\"y2\":400,\"d\":0,\"o\":0}}]'::jsonb where id='{cena}'")
pgx.admin(f"update public.personagens set dados=jsonb_set(dados,'{{inv}}','{{\"items\":[{{\"n\":\"Lampião\",\"luz\":{{\"t\":\"l\",\"m\":6}},\"qtd\":1}}]}}') where id=(select personagem_id from public.tokens where cena_id='{cena}' and nome='Heroi')")  # luz vem do inventário
pgx.admin(f"update public.tokens set dados = dados || '{{\"lo\":1,\"lz\":4}}'::jsonb where cena_id='{cena}' and nome='Heroi'")
print(pgx.aj(f"select to_jsonb(nome||':'||dados::text) from public.tokens where cena_id='{cena}' limit 4"))
with sync_playwright() as p:
    b=p.chromium.launch()
    for u in ['J','M']:
        pg=abre(b,u,d);pg.wait_for_timeout(1200);pg.screenshot(path=S+f'/fog_{u}.png')
        print(u,pg.evaluate("[S.nt,S.dl,S.fg.length,S.walls.length,pv,S.tok.filter(t=>t.lo).length]"))
    b.close()
