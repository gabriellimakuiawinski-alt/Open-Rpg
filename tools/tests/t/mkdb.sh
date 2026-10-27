#!/bin/bash
# recria o banco de teste "e2e" com o schema real
P="psql -h /tmp/pgtest -p 54329 -U postgres -v ON_ERROR_STOP=1 -q"
$P -d postgres -c "drop database if exists e2e" -c "create database e2e" || exit 1
D="$(cd "$(dirname "$0")" && pwd)"; S=$D; R="$(cd "$D/../../.." && pwd)"
for f in $S/stub.sql $R/schema.sql $R/schema_etapa2.sql $R/schema_etapa2b.sql $R/schema_etapa3.sql $R/schema_etapa3.sql $R/schema_etapa3b_musica.sql $R/schema_etapa4.sql $R/schema_etapa5.sql $R/schema_etapa6_livro.sql $R/schema_etapa6b_rituais.sql $R/schema_etapa6c_origens.sql $R/schema_etapa6d_itens.sql $R/schema_etapa7_quadro.sql $R/schema_etapa8_pedidos.sql $R/schema_etapa9_inimigos.sql $R/schema_etapa9b_bestiario.sql $R/schema_etapa9c_ameacas.sql $R/schema_etapa10_amaldicoados.sql $R/schema_etapa11_regras.sql; do
  $P -d e2e -f $f > /tmp/mkdb.out 2>&1 || { echo "ERRO em $f"; cat /tmp/mkdb.out; exit 1; }
done
echo "banco e2e pronto (schema 1 + 2 + 2b, 2b rodado duas vezes)"
