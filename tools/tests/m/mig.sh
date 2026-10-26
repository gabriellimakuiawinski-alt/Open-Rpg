#!/bin/bash
P="psql -h /tmp/pgtest -p 54329 -U postgres -v ON_ERROR_STOP=1 -q"
D="$(cd "$(dirname "$0")" && pwd)"; T="$D/.."
R="$(cd "$D/../../.." && pwd)"
$P -d postgres -c "drop database if exists mig" -c "create database mig" || exit 1
for f in $T/t/stub.sql $R/schema.sql $R/schema_etapa2.sql $R/schema_etapa2b.sql; do $P -d mig -f $f >/tmp/mig.out 2>&1 || { echo ERRO $f; cat /tmp/mig.out; exit 1; }; done
$P -d mig <<'SQL'
insert into auth.users(id,email,raw_user_meta_data) values
 ('aaaaaaaa-0000-0000-0000-000000000001','m@x','{"nome":"Mestre"}'),
 ('bbbbbbbb-0000-0000-0000-000000000002','a@x','{"nome":"Admin"}'),
 ('cccccccc-0000-0000-0000-000000000003','j@x','{"nome":"Jogador"}');
insert into public.mesas(id,nome,mestre_id) values ('11111111-0000-0000-0000-000000000001','Mesa Antiga','aaaaaaaa-0000-0000-0000-000000000001'),('11111111-0000-0000-0000-000000000002','Outra','bbbbbbbb-0000-0000-0000-000000000002');
insert into public.membros(mesa_id,user_id,papel) values ('11111111-0000-0000-0000-000000000001','bbbbbbbb-0000-0000-0000-000000000002','admin'),('11111111-0000-0000-0000-000000000001','cccccccc-0000-0000-0000-000000000003','jogador');
insert into public.personagens(id,user_id,mesa_id,nome,privada) values ('22222222-0000-0000-0000-000000000001','cccccccc-0000-0000-0000-000000000003','11111111-0000-0000-0000-000000000001','Heroi',true),('22222222-0000-0000-0000-000000000002','cccccccc-0000-0000-0000-000000000003',null,'Solta',false);
insert into public.cenas(id,mesa_id,nome) values ('33333333-0000-0000-0000-000000000001','11111111-0000-0000-0000-000000000001','C');
insert into public.tokens(id,cena_id,nome,x,y,criado_por,personagem_id) values ('44444444-0000-0000-0000-000000000001','33333333-0000-0000-0000-000000000001','Heroi tk',1,1,'aaaaaaaa-0000-0000-0000-000000000001','22222222-0000-0000-0000-000000000001');
SQL
codigo_antes=$($P -d mig -At -c "select codigo from public.mesas where nome='Mesa Antiga'")
$P -d mig -f $R/schema_etapa3.sql >/tmp/mig.out 2>&1 || { echo ERRO etapa3; cat /tmp/mig.out; exit 1; }
$P -d mig -f $R/schema_etapa3.sql >/tmp/mig.out 2>&1 || { echo ERRO etapa3 2a vez; cat /tmp/mig.out; exit 1; }
# nova mesa avulsa depois da migracao NAO pode virar campanha numa 3a execucao
$P -d mig -c "insert into public.mesas(nome,mestre_id) values ('Avulsa','aaaaaaaa-0000-0000-0000-000000000001')"
$P -d mig -f $R/schema_etapa3.sql >/tmp/mig.out 2>&1 || { echo ERRO 3a; cat /tmp/mig.out; exit 1; }
q(){ $P -d mig -At -c "$1"; }
chk(){ [ "$2" = "$3" ] && echo "  ok   $1" || echo "  XX   $1 (obtido '$2', esperado '$3')"; }
chk "2 campanhas migradas (avulsa nao vira campanha)" "$(q 'select count(*) from public.campanhas')" 2
chk "codigo de convite preservado" "$(q "select codigo from public.campanhas where nome='Mesa Antiga'")" "$codigo_antes"
chk "membros da campanha = membros da mesa antiga (3)" "$(q "select count(*) from public.campanha_membros where campanha_id='11111111-0000-0000-0000-000000000001'")" 3
chk "papeis preservados" "$(q "select string_agg(papel,',' order by papel) from public.campanha_membros where campanha_id='11111111-0000-0000-0000-000000000001'")" "admin,jogador,mestre"
chk "mesa antiga aponta para a campanha" "$(q "select campanha_id from public.mesas where nome='Mesa Antiga'")" "11111111-0000-0000-0000-000000000001"
chk "mesa avulsa continua sem campanha" "$(q "select campanha_id is null from public.mesas where nome='Avulsa'")" t
chk "ficha ligada migrou" "$(q "select campanha_id from public.personagens where nome='Heroi'")" "11111111-0000-0000-0000-000000000001"
chk "ficha solta continua solta" "$(q "select campanha_id is null from public.personagens where nome='Solta'")" t
chk "token continua ligado a ficha" "$(q "select personagem_id from public.tokens")" "22222222-0000-0000-0000-000000000001"
chk "membros da mesa intactos (3 + 1 da avulsa)" "$(q 'select count(*) from public.membros')" 5
