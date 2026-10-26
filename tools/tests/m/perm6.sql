-- Etapa 5: sistema, dinheiro, lojas, catálogo e luz automática.
-- Rodar num banco recém-criado: bash tools/tests/t/mkdb.sh && psql ... -d e2e -f tools/tests/m/perm6.sql
\set M 'a6000000-0000-0000-0000-000000000001'
\set J 'c6000000-0000-0000-0000-000000000003'
\set K 'd6000000-0000-0000-0000-000000000004'
\set C '96000000-0000-0000-0000-000000000009'
\set FJ '46000000-0000-0000-0000-000000000001'
\set FK '46000000-0000-0000-0000-000000000002'
\set T1 '56000000-0000-0000-0000-000000000001'
\pset tuples_only on
\pset format unaligned
create or replace function public.chk(nome text, cond boolean) returns text language sql as $$ select case when coalesce(cond,false) then '  ok   ' else '  XX   ' end||nome $$;
create or replace function public.falha(sql text) returns boolean language plpgsql as $$ begin execute sql; return false; exception when others then return true; end $$;
insert into auth.users(id,email,raw_user_meta_data) values (:'M','m6@x','{"nome":"Mestre"}'),(:'J','j6@x','{"nome":"Jog"}'),(:'K','k6@x','{"nome":"Outro"}');
set role authenticated; select set_config('request.jwt.claim.sub',:'M',false) \gset
insert into public.campanhas(id,nome,mestre_id) values (:'C','Camp6',:'M');
reset role;
select codigo as cod from public.campanhas where id=:'C' \gset
select public.chk('campanha nova nasce em Ordem Paranormal', (select sistema='op' from public.campanhas where id=:'C'));
set role authenticated;
select set_config('request.jwt.claim.sub',:'J',false) \gset
select public.entrar_na_campanha(:'cod') is not null as _ \gset
select set_config('request.jwt.claim.sub',:'K',false) \gset
select public.entrar_na_campanha(:'cod') is not null as _ \gset

-- fichas
select set_config('request.jwt.claim.sub',:'J',false) \gset
insert into public.personagens(id,user_id,campanha_id,nome,dados,dinheiro) values (:'FJ',:'J',:'C','Heroi','{"inv":{"items":[]}}',999);
select public.chk('jogador não cria ficha já com dinheiro', (select dinheiro=0 from public.personagens where id=:'FJ'));
select public.chk('jogador NÃO muda o próprio dinheiro', public.falha($$update public.personagens set dinheiro=500 where id='46000000-0000-0000-0000-000000000001'$$));
with x as (update public.campanhas set sistema='modular' where id='96000000-0000-0000-0000-000000000009' returning 1) select public.chk('jogador NÃO muda o sistema da campanha', (select count(*)=0 from x));
select set_config('request.jwt.claim.sub',:'K',false) \gset
insert into public.personagens(id,user_id,campanha_id,nome,dados) values (:'FK',:'K',:'C','Outro','{}');
select set_config('request.jwt.claim.sub',:'M',false) \gset
update public.personagens set dinheiro=100 where id=:'FJ';
select public.chk('mestre dá dinheiro', (select dinheiro=100 from public.personagens where id=:'FJ'));
select public.chk('dinheiro não fica negativo', public.falha($$update public.personagens set dinheiro=-1 where id='46000000-0000-0000-0000-000000000001'$$));

-- lojas
insert into public.lojas(id,campanha_id,nome,aberta) values ('76000000-0000-0000-0000-000000000001',:'C','Arsenal',false),('76000000-0000-0000-0000-000000000002',:'C','Mercado',true);
insert into public.loja_itens(id,loja_id,item,preco,estoque) values
 ('86000000-0000-0000-0000-000000000001','76000000-0000-0000-0000-000000000001','{"n":"Fuzil","tipo":"arma"}',50,null),
 ('86000000-0000-0000-0000-000000000002','76000000-0000-0000-0000-000000000002','{"n":"Lanterna tática","tipo":"geral","luz":{"t":"c","m":18}}',30,2),
 ('86000000-0000-0000-0000-000000000003','76000000-0000-0000-0000-000000000002','{"n":"Caro"}',1000,null);
select set_config('request.jwt.claim.sub',:'J',false) \gset
select public.chk('jogador NÃO vê loja fechada', (select count(*)=1 from public.lojas where campanha_id=:'C'));
select public.chk('jogador NÃO vê itens da loja fechada', (select count(*)=2 from public.loja_itens));
select public.chk('jogador NÃO cria loja', public.falha($$insert into public.lojas(campanha_id,nome) values ('96000000-0000-0000-0000-000000000009','X')$$));
with x as (update public.loja_itens set preco=0 where id='86000000-0000-0000-0000-000000000002' returning 1) select public.chk('jogador NÃO muda preço', (select count(*)=0 from x));
select public.chk('comprar em loja fechada falha', public.falha($$select public.comprar('86000000-0000-0000-0000-000000000001','46000000-0000-0000-0000-000000000001',1)$$));
select public.chk('comprar sem dinheiro falha', public.falha($$select public.comprar('86000000-0000-0000-0000-000000000003','46000000-0000-0000-0000-000000000001',1)$$));
select public.chk('comprar para ficha de outro falha', public.falha($$select public.comprar('86000000-0000-0000-0000-000000000002','46000000-0000-0000-0000-000000000002',1)$$));
select public.comprar('86000000-0000-0000-0000-000000000002',:'FJ',1);
select public.chk('compra desconta o dinheiro', (select dinheiro=70 from public.personagens where id=:'FJ'));
select public.chk('item comprado vai para o inventário (com ref e luz)', (select dados->'inv'->'items'->0->>'n'='Lanterna tática' and dados->'inv'->'items'->0->>'ref'='86000000-0000-0000-0000-000000000002' and (dados->'inv'->'items'->0->'luz'->>'m')::numeric=18 from public.personagens where id=:'FJ'));
select public.chk('estoque diminui', (select estoque=1 from public.loja_itens where id='86000000-0000-0000-0000-000000000002'));
select public.comprar('86000000-0000-0000-0000-000000000002',:'FJ',1);
select public.chk('mesmo item soma a quantidade', (select jsonb_array_length(dados->'inv'->'items')=1 and (dados->'inv'->'items'->0->>'qtd')::int=2 and dinheiro=40 from public.personagens where id=:'FJ'));
select public.chk('estoque esgotado bloqueia', public.falha($$select public.comprar('86000000-0000-0000-0000-000000000002','46000000-0000-0000-0000-000000000001',1)$$));
select public.chk('jogador vê as próprias compras', (select count(*)=2 from public.loja_compras));
select set_config('request.jwt.claim.sub',:'K',false) \gset
select public.chk('outro jogador não vê compras alheias', (select count(*)=0 from public.loja_compras));

-- catálogo / homebrew
select set_config('request.jwt.claim.sub',:'J',false) \gset
select public.chk('jogador NÃO cria homebrew já aprovado', public.falha($$insert into public.catalogo(campanha_id,nome,aprovado,criado_por) values ('96000000-0000-0000-0000-000000000009','Trapaça',true,'c6000000-0000-0000-0000-000000000003')$$));
insert into public.catalogo(id,campanha_id,nome,dados,criado_por) values ('66000000-0000-0000-0000-000000000001',:'C','Vigor Extra','{"ef":[{"a":"pv","v":2,"nv":true}]}',:'J');
select public.chk('jogador NÃO aprova o próprio homebrew', public.falha($$update public.catalogo set aprovado=true where id='66000000-0000-0000-0000-000000000001'$$) or (select not aprovado from public.catalogo where id='66000000-0000-0000-0000-000000000001'));
select set_config('request.jwt.claim.sub',:'K',false) \gset
select public.chk('homebrew pendente não aparece para os outros', (select count(*)=0 from public.catalogo));
select set_config('request.jwt.claim.sub',:'M',false) \gset
update public.catalogo set aprovado=true where id='66000000-0000-0000-0000-000000000001';
select set_config('request.jwt.claim.sub',:'K',false) \gset
select public.chk('homebrew aprovado aparece para todos', (select count(*)=1 from public.catalogo));

-- luz automática
select set_config('request.jwt.claim.sub',:'M',false) \gset
insert into public.mesas(id,nome,mestre_id,campanha_id) values ('16000000-0000-0000-0000-000000000001','Mesa6',:'M',:'C');
insert into public.cenas(id,mesa_id,nome,ordem,grade_m) values ('36000000-0000-0000-0000-000000000001','16000000-0000-0000-0000-000000000001','Cena',0,1.5);
update public.mesas set cena_ativa='36000000-0000-0000-0000-000000000001' where id='16000000-0000-0000-0000-000000000001';
insert into public.tokens(id,cena_id,nome,personagem_id,criado_por,dados) values (:'T1','36000000-0000-0000-0000-000000000001','Heroi',:'FJ',:'M','{"lo":1,"lm":"c","lz":99}');
select public.chk('lanterna tática 18 m = 12 quadrados (jogador não escolhe o alcance)', (select (dados->>'lz')::numeric=12 and (dados->>'lo')::int=1 from public.tokens where id=:'T1'));
update public.tokens set dados=dados||'{"lm":"l","lo":1}' where id=:'T1';
select public.chk('sem lampião no inventário, o lampião não liga', (select (dados->>'lo')::int=0 from public.tokens where id=:'T1'));
select set_config('request.jwt.claim.sub',:'J',false) \gset
update public.tokens set dados=dados||'{"lm":"c","lo":1,"lz":50}' where id=:'T1';
select public.chk('jogador consegue ligar a lanterna do próprio token', (select (dados->>'lo')::int=1 from public.tokens where id=:'T1'));
select public.chk('jogador tenta aumentar a lanterna: volta ao alcance do item', (select (dados->>'lz')::numeric=12 from public.tokens where id=:'T1'));
update public.personagens set dados=jsonb_set(dados,'{inv,items}','[{"n":"Celular","luz":{"t":"c","m":4.5},"qtd":1}]') where id=:'FJ';
select public.chk('trocou a lanterna por celular: alcance cai sozinho (3 quadrados)', (select (dados->>'lz')::numeric=3 and (dados->>'lo')::int=1 from public.tokens where id=:'T1'));
update public.personagens set dados=jsonb_set(dados,'{inv,items}','[]') where id=:'FJ';
select public.chk('sem nenhuma luz no inventário: apaga', (select (dados->>'lo')::int=0 from public.tokens where id=:'T1'));
select set_config('request.jwt.claim.sub',:'M',false) \gset
update public.campanhas set sistema='modular' where id=:'C';
update public.tokens set dados=dados||'{"lm":"c","lo":1,"lz":7}' where id=:'T1';
select public.chk('campanha Modular: luz continua manual', (select (dados->>'lz')::numeric=7 and (dados->>'lo')::int=1 from public.tokens where id=:'T1'));
select public.chk('mestre muda o sistema', (select sistema='modular' from public.campanhas where id=:'C'));
reset role;
