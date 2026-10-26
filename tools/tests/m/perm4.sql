\set M 'aaaaaaaa-0000-0000-0000-000000000001'
\set J 'cccccccc-0000-0000-0000-000000000003'
\set X 'eeeeeeee-0000-0000-0000-000000000005'
\pset tuples_only on
\pset format unaligned
create or replace function public.chk(nome text, cond boolean) returns text language sql as $$ select case when coalesce(cond,false) then '  ok   ' else '  XX   ' end||nome $$;
insert into auth.users(id,email,raw_user_meta_data) values (:'M','m@x','{"nome":"Mestre"}'),(:'J','j@x','{"nome":"Jogador"}'),(:'X','x@x','{"nome":"Fora"}');
set role authenticated; select set_config('request.jwt.claim.sub',:'M',false) \gset
insert into public.mesas(id,nome,mestre_id) values ('11111111-1111-1111-1111-111111111111','Mesa',:'M');
reset role;
select codigo as cod from public.mesas \gset
set role authenticated; select set_config('request.jwt.claim.sub',:'J',false) \gset
select public.entrar_na_mesa(:'cod') is not null as _ \gset
reset role;
insert into public.arquivos(id,mesa_id,tipo,nome,path,criado_por) values
 ('22222222-2222-2222-2222-222222222221','11111111-1111-1111-1111-111111111111','aud','Tema','11111111-1111-1111-1111-111111111111/22222222-2222-2222-2222-222222222221-a.mp3',:'M'),
 ('22222222-2222-2222-2222-222222222222','11111111-1111-1111-1111-111111111111','aud','Segredo','11111111-1111-1111-1111-111111111111/22222222-2222-2222-2222-222222222222-b.mp3',:'M');
set role authenticated; select set_config('request.jwt.claim.sub',:'J',false) \gset
select public.chk('jogador nao ve musicas antes de tocar', (select count(*) from public.arquivos where tipo='aud')=0);
select set_config('request.jwt.claim.sub',:'M',false) \gset
update public.mesas set musica_id='22222222-2222-2222-2222-222222222221';
select public.chk('mestre define a faixa tocando', (select musica_id from public.mesas)='22222222-2222-2222-2222-222222222221');
select set_config('request.jwt.claim.sub',:'J',false) \gset
select public.chk('jogador ve SO a faixa que esta tocando', (select string_agg(nome,',') from public.arquivos where tipo='aud')='Tema');
select set_config('request.jwt.claim.sub',:'X',false) \gset
select public.chk('quem nao e da mesa nao ve a faixa', (select count(*) from public.arquivos where tipo='aud')=0);
select set_config('request.jwt.claim.sub',:'J',false) \gset
update public.mesas set musica_id='22222222-2222-2222-2222-222222222222';
select public.chk('jogador NAO muda a faixa', (select musica_id from public.mesas)='22222222-2222-2222-2222-222222222221');
select set_config('request.jwt.claim.sub',:'M',false) \gset
update public.mesas set musica_id=null;
select set_config('request.jwt.claim.sub',:'J',false) \gset
select public.chk('parou de transmitir: jogador perde acesso', (select count(*) from public.arquivos where tipo='aud')=0);
