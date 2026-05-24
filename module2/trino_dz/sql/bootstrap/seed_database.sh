#!/usr/bin/env bash
set -euo pipefail

readonly SQL_DIR="/sql/init"
readonly DB_ARGS=(
  -v ON_ERROR_STOP=1
  --username "${POSTGRES_USER}"
  --dbname "${POSTGRES_DB}"
)

run_sql() {
  local filename="$1"
  local full_path="${SQL_DIR}/${filename}"

  echo "seed: ${filename}"
  psql \
    "${DB_ARGS[@]}" \
    --file "${full_path}"
}

run_sql "task1ddl (1).sql"
run_sql "1task (1).sql"
run_sql "task2ddl (1).sql"
run_sql "2task (1).sql"
run_sql "task3ddl (1).sql"
run_sql "task3 (1).sql"
run_sql "tak4ddl (1).sql"
run_sql "task4 (1).sql"
run_sql "oil_station (1).sql"
