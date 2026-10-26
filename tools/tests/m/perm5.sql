\set M 'aaaaaaaa-0000-0000-0000-000000000001'
\set J 'cccccccc-0000-0000-0000-000000000003'
\set K 'dddddddd-0000-0000-0000-000000000004'
\set X 'eeeeeeee-0000-0000-0000-000000000005'
\pset tuples_only on
\pset format unaligned
create or replace function public.chk(nome text, cond boolean) returns text language sql as $$ select case when coalesce(cond,false) then '  ok   ' else '  XX   ' end||nome $$;
insert into auth.users(id,email,raw_user_meta_data) values (:'M','m@x','{"nome":"Mestre"}'),(:'J','j@x','{"nome":"Jogador"}'),(:'K','k@x','{"nome":"Outro"}'),(:'X','x@x','{"nome":"Fora"}');
set role authenticated; select set_config('request.jwt.claim.sub',:'M',false) \gset
insert into public.campanhas(id,nome,mestre_id) values ('99999999-9999-9999-9999-999999999999','Camp',:'M');
reset role;
select codigo as cod from public.campanhas \gset
set role authenticated; select set_config('request.jwt.claim.sub',:'J',false) \gset
select public.entrar_na_campanha(:'cod') is not null as _ \gset
select set_config('request.jwt.claim.sub',:'K',false) \gset
select public.entrar_na_campanha(:'cod') is not null as _ \gset
select set_config('request.jwt.claim.sub',:'M',false) \gset
insert into public.mesas(id,nome,mestre_id,campanha_id) values ('11111111-1111-1111-1111-111111111111','Mesa',:'M','99999999-9999-9999-9999-999999999999');
insert into public.cenas(id,mesa_id,nome,ordem) values ('33333333-3333-3333-3333-333333333333','11111111-1111-1111-1111-111111111111','Cena',0);
select set_config('request.jwt.claim.sub',:'J',false) \gset
insert into public.personagens(id,user_id,campanha_id,nome,dados) values
 ('44444444-4444-4444-4444-444444444441',:'J','99999999-9999-9999-9999-999999999999','Heroi','{"stats":[{"id":"pv","n":"PV","cur":14,"max":20},{"id":"pe","n":"PE","cur":3,"max":12},{"id":"san","n":"SAN","cur":9,"max":15},{"id":"x1","n":"Outra","cur":1,"max":2}]}'),
 ('44444444-4444-4444-4444-444444444442',:'J','99999999-9999-9999-9999-999999999999','SemSan','{"stats":[{"id":"pv","n":"PV","cur":5,"max":5}]}');
select set_config('request.jwt.claim.sub',:'M',false) \gset
insert into public.tokens(id,cena_id,nome,x,y,criado_por,personagem_id,dados) values
 ('55555555-5555-5555-5555-555555555551','33333333-3333-3333-3333-333333333333','Heroi',0,0,:'M','44444444-4444-4444-4444-444444444441','{"hp":1,"pv":1,"mn":1,"mm":1}'),
 ('55555555-5555-5555-5555-555555555552','33333333-3333-3333-3333-333333333333','SemSan',0,0,:'M','44444444-4444-4444-4444-444444444442','{}');
select public.chk('token novo assume PV da ficha', (select (dados->>'hp')::int=14 and (dados->>'pv')::int=20 from public.tokens where id='55555555-5555-5555-5555-555555555551'));
select public.chk('token novo assume PE e SAN da ficha', (select (dados->>'mn')::int=3 and (dados->>'mm')::int=12 and (dados->>'sn')::int=9 and (dados->>'sm')::int=15 from public.tokens where id='55555555-5555-5555-5555-555555555551'));
select public.chk('ficha sem SAN: token sem SAN, sem erro', (select dados->'sn' is null and (dados->>'hp')::int=5 from public.tokens where id='55555555-5555-5555-5555-555555555552'));
-- dono da ficha mexe no token (precisa de permissao de editar o token: mestre faz)
update public.tokens set dados = dados || '{"hp":7,"mn":2,"sn":4}' where id='55555555-5555-5555-5555-555555555551';
reset role;
select public.chk('token -> ficha: PV/PE/SAN atualizam', (select (dados->'stats'->0->>'cur')::int=7 and (dados->'stats'->1->>'cur')::int=2 and (dados->'stats'->2->>'cur')::int=4 from public.personagens where id='44444444-4444-4444-4444-444444444441'));
select public.chk('token -> ficha: outras barras e maximos intactos', (select (dados->'stats'->3->>'cur')::int=1 and (dados->'stats'->0->>'max')::int=20 from public.personagens where id='44444444-4444-4444-4444-444444444441'));
set role authenticated; select set_config('request.jwt.claim.sub',:'J',false) \gset
update public.personagens set dados = jsonb_set(dados,'{stats,0,cur}','11') where id='44444444-4444-4444-4444-444444444441';
update public.personagens set dados = jsonb_set(dados,'{stats,2,max}','18') where id='44444444-4444-4444-4444-444444444441';
reset role;
select public.chk('ficha -> token: PV e max de SAN chegam ao token', (select (dados->>'hp')::int=11 and (dados->>'sm')::int=18 from public.tokens where id='55555555-5555-5555-5555-555555555551'));
-- outro jogador (K) mexendo no token ligado a ficha do J: ficha NAO muda
set role authenticated; select set_config('request.jwt.claim.sub',:'K',false) \gset
update public.tokens set dados = dados || '{"hp":1}' where id='55555555-5555-5555-5555-555555555551';
reset role;
select public.chk('quem nao pode editar a ficha nao altera PV por token', (select (dados->'stats'->0->>'cur')::int=11 from public.personagens where id='44444444-4444-4444-4444-444444444441'));
-- religar token em outra ficha: assume os valores dela
set role authenticated; select set_config('request.jwt.claim.sub',:'M',false) \gset
update public.tokens set personagem_id='44444444-4444-4444-4444-444444444442' where id='55555555-5555-5555-5555-555555555551';
reset role;
select public.chk('religar: ficha anterior intacta e token assume a nova', (select (dados->'stats'->0->>'cur')::int=11 from public.personagens where id='44444444-4444-4444-4444-444444444441') and (select (dados->>'hp')::int=5 from public.tokens where id='55555555-5555-5555-5555-555555555551'));
-- efeitos sonoros / musica
insert into public.arquivos(id,mesa_id,tipo,nome,path,efeito,criado_por) values
 ('66666666-6666-6666-6666-666666666661','11111111-1111-1111-1111-111111111111','aud','Porta','11111111-1111-1111-1111-111111111111/66666666-6666-6666-6666-666666666661-a.mp3',true,:'M'),
 ('66666666-6666-6666-6666-666666666662','11111111-1111-1111-1111-111111111111','aud','Tema','11111111-1111-1111-1111-111111111111/66666666-6666-6666-6666-666666666662-b.mp3',false,:'M');
set role authenticated; select set_config('request.jwt.claim.sub',:'J',false) \gset
select public.chk('jogador ve os EFEITOS e nao as musicas', (select string_agg(nome,',') from public.arquivos where tipo='aud')='Porta');
select set_config('request.jwt.claim.sub',:'X',false) \gset
select public.chk('quem nao e da mesa nao ve efeitos', (select count(*) from public.arquivos where tipo='aud')=0);
-- notas do jogador
select set_config('request.jwt.claim.sub',:'J',false) \gset
insert into public.notas_jogador(mesa_id,user_id,texto) values ('11111111-1111-1111-1111-111111111111',:'J','segredo do J');
select set_config('request.jwt.claim.sub',:'M',false) \gset
select public.chk('nem o mestre le as notas do jogador', (select count(*) from public.notas_jogador)=0);
select set_config('request.jwt.claim.sub',:'K',false) \gset
select public.chk('outro jogador nao le as notas', (select count(*) from public.notas_jogador)=0);
do $$ begin begin insert into public.notas_jogador(mesa_id,user_id,texto) values ('11111111-1111-1111-1111-111111111111','cccccccc-0000-0000-0000-000000000003','x'); raise notice '  XX   K escreveu nota em nome do J'; exception when others then raise notice '  ok   nao escreve nota em nome de outro'; end; end $$;
select set_config('request.jwt.claim.sub',:'J',false) \gset
select public.chk('o dono le a propria nota', (select texto from public.notas_jogador)='segredo do J');
