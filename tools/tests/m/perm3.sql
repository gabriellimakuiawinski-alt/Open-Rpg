\set M 'aaaaaaaa-0000-0000-0000-000000000001'
\set A 'bbbbbbbb-0000-0000-0000-000000000002'
\set J 'cccccccc-0000-0000-0000-000000000003'
\set K 'dddddddd-0000-0000-0000-000000000004'
\set X 'eeeeeeee-0000-0000-0000-000000000005'
\pset tuples_only on
\pset format unaligned
create or replace function public.chk(nome text, cond boolean) returns text language sql as $$ select case when coalesce(cond,false) then '  ok   ' else '  XX   ' end || nome $$;
create or replace function public.erro(nome text, q text) returns text language plpgsql as $$
begin execute q; return '  XX   '||nome||' (deveria dar erro)'; exception when others then return '  ok   '||nome||'  ['||left(sqlerrm,70)||']'; end $$;
create or replace function public.linhas(nome text, q text, n int) returns text language plpgsql as $$
declare c int; begin execute q; get diagnostics c = row_count; return case when c=n then '  ok   ' else '  XX   ' end||nome||' ('||c||' linhas, esperado '||n||')';
exception when others then return '  XX   '||nome||' ERRO: '||sqlerrm; end $$;
insert into auth.users(id,email,raw_user_meta_data) values (:'M','m@x','{"nome":"Mestre"}'),(:'A','a@x','{"nome":"Admin"}'),(:'J','j@x','{"nome":"Jogador"}'),(:'K','k@x','{"nome":"Kay"}'),(:'X','x@x','{"nome":"Estranho"}');

-- ===== Campanha, convite, papéis =====
set role authenticated; select set_config('request.jwt.claim.sub',:'M',false) \gset
insert into public.campanhas(nome,mestre_id) values ('Camp',:'M');
select public.erro('ninguem cria campanha em nome de outro', format('insert into public.campanhas(nome,mestre_id) values (%L,%L)','x',:'J'));
select public.chk('criador vira mestre da campanha', (select papel from public.campanha_membros where user_id=:'M')='mestre');
reset role;
select id as camp, codigo as cod from public.campanhas \gset
set role authenticated; select set_config('request.jwt.claim.sub',:'A',false) \gset
select public.entrar_na_campanha(:'cod') is not null as _ \gset
select public.erro('codigo invalido de campanha', $q$select public.entrar_na_campanha('ZZZZZZ')$q$);
reset role;
set role authenticated; select set_config('request.jwt.claim.sub',:'J',false) \gset
select public.entrar_na_campanha(:'cod') is not null as _ \gset
select public.linhas('jogador NAO promove a si mesmo', format('update public.campanha_membros set papel=%L where user_id=%L','admin',:'J'), 0);
select public.chk('jogador ve os 3 membros da campanha', (select count(*) from public.campanha_membros)=3);
reset role;
set role authenticated; select set_config('request.jwt.claim.sub',:'X',false) \gset
select public.chk('estranho nao ve campanha', (select count(*) from public.campanhas)=0);
select public.chk('estranho nao ve membros', (select count(*) from public.campanha_membros)=0);
reset role;
set role authenticated; select set_config('request.jwt.claim.sub',:'M',false) \gset
select public.linhas('mestre promove A a admin', format('update public.campanha_membros set papel=%L where user_id=%L','admin',:'A'), 1);
select public.erro('mestre nao cria outro mestre', format('update public.campanha_membros set papel=%L where user_id=%L','mestre',:'J'));
reset role;
set role authenticated; select set_config('request.jwt.claim.sub',:'A',false) \gset
select public.linhas('admin NAO promove ninguem', format('update public.campanha_membros set papel=%L where user_id=%L','admin',:'J'), 0);
select public.linhas('admin NAO muda nome da campanha', format('update public.campanhas set nome=%L where id=%L','hack',:'camp'), 0);
reset role;

-- ===== Mesa de campanha: o grupo entra junto =====
set role authenticated; select set_config('request.jwt.claim.sub',:'M',false) \gset
insert into public.mesas(nome,mestre_id,campanha_id) values ('Mesa da camp',:'M',:'camp');
reset role;
select id as mesa, codigo as mcod from public.mesas where campanha_id is not null \gset
select public.chk('mesa de campanha: 3 membros automaticos', (select count(*) from public.membros where mesa_id=:'mesa')=3);
select public.chk('papel de A na mesa = admin', (select papel from public.membros where mesa_id=:'mesa' and user_id=:'A')='admin');
set role authenticated; select set_config('request.jwt.claim.sub',:'J',false) \gset
select public.erro('jogador NAO cria mesa na campanha', format('insert into public.mesas(nome,mestre_id,campanha_id) values (%L,%L,%L)','x',:'J',:'camp'));
select public.erro('jogador NAO cria mesa em nome do mestre', format('insert into public.mesas(nome,mestre_id,campanha_id) values (%L,%L,%L)','x',:'M',:'camp'));
select public.erro('NAO entra em mesa de campanha pelo codigo da mesa', format('select public.entrar_na_mesa(%L)',:'mcod'));
select public.linhas('NAO sai sozinho da mesa de campanha', format('delete from public.membros where mesa_id=%L and user_id=%L',:'mesa',:'J'), 0);
select public.linhas('jogador NAO altera a mesa', format('update public.mesas set campanha_id=null where id=%L',:'mesa'),0);
reset role;
set role authenticated; select set_config('request.jwt.claim.sub',:'M',false) \gset
select public.erro('nem o mestre troca a campanha da mesa', format('update public.mesas set campanha_id=null where id=%L',:'mesa'));
select public.linhas('mestre NAO muda papel direto na mesa de campanha', format('update public.membros set papel=%L where mesa_id=%L and user_id=%L','admin',:'mesa',:'J'), 0);
reset role;
-- K entra na campanha depois: aparece na mesa
set role authenticated; select set_config('request.jwt.claim.sub',:'K',false) \gset
select public.entrar_na_campanha(:'cod') is not null as _ \gset
reset role;
select public.chk('entrou depois: entra nas mesas da campanha', (select papel from public.membros where mesa_id=:'mesa' and user_id=:'K')='jogador');
set role authenticated; select set_config('request.jwt.claim.sub',:'M',false) \gset
select public.linhas('promover na campanha promove na mesa', format('update public.campanha_membros set papel=%L where user_id=%L','admin',:'K'), 1);
reset role;
select public.chk('K virou admin na mesa', (select papel from public.membros where mesa_id=:'mesa' and user_id=:'K')='admin');
set role authenticated; select set_config('request.jwt.claim.sub',:'M',false) \gset
select public.linhas('rebaixar volta a jogador', format('update public.campanha_membros set papel=%L where user_id=%L','jogador',:'K'), 1);
reset role;
select public.chk('K voltou a jogador na mesa', (select papel from public.membros where mesa_id=:'mesa' and user_id=:'K')='jogador');

-- ===== Mesa avulsa: sem fichas =====
set role authenticated; select set_config('request.jwt.claim.sub',:'M',false) \gset
insert into public.mesas(nome,mestre_id) values ('Avulsa',:'M');
reset role;
select id as av, codigo as avcod from public.mesas where campanha_id is null \gset
set role authenticated; select set_config('request.jwt.claim.sub',:'X',false) \gset
select public.entrar_na_mesa(:'avcod') is not null as _ \gset
select public.chk('mesa avulsa: entra pelo codigo', (select count(*) from public.mesas where id=:'av')=1);
select public.chk('estranho nao ve a mesa da campanha', (select count(*) from public.mesas where id=:'mesa')=0);
reset role;

-- ===== Fichas =====
set role authenticated; select set_config('request.jwt.claim.sub',:'J',false) \gset
insert into public.personagens(id,user_id,campanha_id,nome) values
  ('f0000000-0000-0000-0000-000000000001',:'J',:'camp','Heroi J'),
  ('f0000000-0000-0000-0000-000000000002',:'J',:'camp','Segredo J'),
  ('f0000000-0000-0000-0000-000000000003',:'J',null,'Solta J');
update public.personagens set privada=true where id='f0000000-0000-0000-0000-000000000002';
select public.erro('ficha NAO entra em campanha alheia', format('insert into public.personagens(user_id,campanha_id,nome) values (%L,%L,%L)',:'J',gen_random_uuid(),'x'));
select public.erro('NAO cria ficha para outro', format('insert into public.personagens(user_id,campanha_id,nome) values (%L,%L,%L)',:'K',:'camp','x'));
reset role;
set role authenticated; select set_config('request.jwt.claim.sub',:'M',false) \gset
insert into public.personagens(id,user_id,campanha_id,nome,npc) values ('f0000000-0000-0000-0000-000000000009',:'M',:'camp','Vilao NPC',true);
reset role;
set role authenticated; select set_config('request.jwt.claim.sub',:'K',false) \gset
select public.chk('K ve a ficha publica do J', (select count(*) from public.personagens where nome='Heroi J')=1);
select public.chk('K NAO ve ficha privada', (select count(*) from public.personagens where nome='Segredo J')=0);
select public.chk('K NAO ve NPC', (select count(*) from public.personagens where nome='Vilao NPC')=0);
select public.chk('K NAO ve ficha solta do J', (select count(*) from public.personagens where nome='Solta J')=0);
select public.linhas('K NAO edita ficha do J', format('update public.personagens set nome=%L where id=%L','hack','f0000000-0000-0000-0000-000000000001'),0);
reset role;
set role authenticated; select set_config('request.jwt.claim.sub',:'A',false) \gset
select public.chk('admin ve ficha publica, nao privada nem NPC', (select count(*) from public.personagens)=1);
select public.linhas('admin edita ficha publica', format('update public.personagens set nome=%L where id=%L','Heroi J (rev)','f0000000-0000-0000-0000-000000000001'),1);
select public.linhas('admin NAO edita ficha privada', format('update public.personagens set nome=%L where id=%L','x','f0000000-0000-0000-0000-000000000002'),0);
reset role;
set role authenticated; select set_config('request.jwt.claim.sub',:'M',false) \gset
select public.chk('mestre ve fichas publica, privada e NPC (3)', (select count(*) from public.personagens)=3);
select public.chk('mestre NAO ve ficha solta', (select count(*) from public.personagens where nome='Solta J')=0);
select public.linhas('mestre edita ficha privada', format('update public.personagens set nome=%L where id=%L','Segredo J','f0000000-0000-0000-0000-000000000002'),1);
reset role;
set role authenticated; select set_config('request.jwt.claim.sub',:'J',false) \gset
select public.linhas('dono muda a propria ficha de campanha (privada)', format('update public.personagens set privada=false where id=%L','f0000000-0000-0000-0000-000000000002'),1);
select public.erro('dono NAO move ficha para campanha onde nao esta', format('update public.personagens set campanha_id=%L where id=%L',gen_random_uuid(),'f0000000-0000-0000-0000-000000000003'));
select public.linhas('dono poe ficha solta na campanha', format('update public.personagens set campanha_id=%L where id=%L',:'camp','f0000000-0000-0000-0000-000000000003'),1);
reset role;

-- ===== Tokens x fichas =====
set role authenticated; select set_config('request.jwt.claim.sub',:'M',false) \gset
insert into public.cenas(id,mesa_id,nome) values ('c0000000-0000-0000-0000-000000000001',:'mesa','C1'),('c0000000-0000-0000-0000-000000000002',:'av','C2');
select public.ativar_cena('c0000000-0000-0000-0000-000000000001') is null as _ \gset
select public.linhas('liga token a ficha da campanha', format('insert into public.tokens(id,cena_id,nome,x,y,criado_por,personagem_id) values (%L,%L,%L,0,0,%L,%L)','a0000000-0000-0000-0000-000000000001','c0000000-0000-0000-0000-000000000001','T',:'M','f0000000-0000-0000-0000-000000000001'),1);
select public.erro('NAO liga token a ficha solta de outro', format('insert into public.tokens(cena_id,nome,x,y,criado_por,personagem_id) values (%L,%L,0,0,%L,%L)','c0000000-0000-0000-0000-000000000001','T2',:'M',gen_random_uuid()));
select public.erro('mesa avulsa NAO liga ficha', format('insert into public.tokens(cena_id,nome,x,y,criado_por,personagem_id) values (%L,%L,0,0,%L,%L)','c0000000-0000-0000-0000-000000000002','T3',:'M','f0000000-0000-0000-0000-000000000001'));
select public.linhas('mesa avulsa aceita token sem ficha', format('insert into public.tokens(cena_id,nome,x,y,criado_por) values (%L,%L,0,0,%L)','c0000000-0000-0000-0000-000000000002','T4',:'M'),1);
reset role;
set role authenticated; select set_config('request.jwt.claim.sub',:'J',false) \gset
select public.chk('dono da ficha edita o token ligado', (select count(*) from (select 1 from public.tokens where id='a0000000-0000-0000-0000-000000000001') s)=1);
select public.linhas('dono da ficha atualiza o token', format('update public.tokens set nome=%L where id=%L','Heroi J','a0000000-0000-0000-0000-000000000001'),1);
reset role;
-- ficha sai da campanha -> solta do token
set role authenticated; select set_config('request.jwt.claim.sub',:'J',false) \gset
update public.personagens set campanha_id=null where id='f0000000-0000-0000-0000-000000000001';
reset role;
select public.chk('ficha fora da campanha desliga do token', (select personagem_id from public.tokens where id='a0000000-0000-0000-0000-000000000001') is null);

-- ===== Sair da campanha =====
set role authenticated; select set_config('request.jwt.claim.sub',:'J',false) \gset
select public.linhas('jogador sai da campanha', format('delete from public.campanha_membros where user_id=%L',:'J'),1);
reset role;
select public.chk('saiu da campanha: sai das mesas dela', (select count(*) from public.membros where mesa_id=:'mesa' and user_id=:'J')=0);
select public.chk('saiu da campanha: ficha fica sem campanha', (select count(*) from public.personagens where user_id=:'J' and campanha_id is not null)=0);
select public.chk('saiu da campanha: ficha continua existindo (3)', (select count(*) from public.personagens where user_id=:'J')=3);
set role authenticated; select set_config('request.jwt.claim.sub',:'M',false) \gset
select public.linhas('mestre remove K da campanha', format('delete from public.campanha_membros where user_id=%L',:'K'),1);
select public.linhas('mestre NAO se remove', format('delete from public.campanha_membros where user_id=%L',:'M'),0);
reset role;
select public.chk('K removido tambem da mesa', (select count(*) from public.membros where mesa_id=:'mesa' and user_id=:'K')=0);

-- ===== Nomes dos colegas e último acesso =====
set role authenticated; select set_config('request.jwt.claim.sub',:'A',false) \gset
select public.chk('admin ve o nome do mestre (divide campanha)', (select count(*) from public.profiles where id=:'M')=1);
select public.chk('admin NAO ve o estranho', (select count(*) from public.profiles where id=:'X')=0);
select public.marcar_acesso_mesa(:'mesa') is null as _ \gset
reset role;
select public.chk('ultimo acesso registrado', (select ultimo_acesso is not null from public.membros where mesa_id=:'mesa' and user_id=:'A'));
select public.chk('ultimo acesso so de quem abriu', (select ultimo_acesso is null from public.membros where mesa_id=:'mesa' and user_id=:'M'));

-- ===== Excluir campanha: a mesa continua, sem campanha =====
set role authenticated; select set_config('request.jwt.claim.sub',:'A',false) \gset
select public.linhas('admin NAO exclui campanha', format('delete from public.campanhas where id=%L',:'camp'),0);
reset role;
set role authenticated; select set_config('request.jwt.claim.sub',:'M',false) \gset
select public.linhas('mestre exclui campanha', format('delete from public.campanhas where id=%L',:'camp'),1);
reset role;
select public.chk('mesa sobrevive sem campanha', (select count(*) from public.mesas where id=:'mesa' and campanha_id is null)=1);
select public.chk('membros da mesa continuam (M e A)', (select count(*) from public.membros where mesa_id=:'mesa')=2);
select public.chk('fichas da campanha ficam sem campanha', (select count(*) from public.personagens where campanha_id is not null)=0);
