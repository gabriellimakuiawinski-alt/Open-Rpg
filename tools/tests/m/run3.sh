#!/bin/bash
P="psql -h /tmp/pgtest -p 54329 -U postgres -v ON_ERROR_STOP=1 -q"
D="$(cd "$(dirname "$0")" && pwd)"; R="$(cd "$D/../../.." && pwd)"; T="$D/.."
$P -d postgres -c "drop database if exists p3" -c "create database p3" 2>/dev/null
for f in $T/t/stub.sql $R/schema.sql $R/schema_etapa2.sql $R/schema_etapa2b.sql $R/schema_etapa3.sql; do $P -d p3 -f $f >/tmp/p3.out 2>&1 || { echo ERRO $f; cat /tmp/p3.out; exit 1; }; done
psql -h /tmp/pgtest -p 54329 -U postgres -d p3 -X -q -f $T/m/perm3.sql 2>&1 | tee /tmp/perm3.out | grep -v '^$'
echo "ok: $(grep -c '^  ok' /tmp/perm3.out) falhas: $(grep -c '^  XX' /tmp/perm3.out)"
