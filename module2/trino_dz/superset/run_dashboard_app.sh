#!/usr/bin/env bash
set -euo pipefail

readonly SUPERSET_HOST="0.0.0.0"
readonly SUPERSET_PORT="8088"
readonly SOURCE_CONFIG="/app/bootstrap/analytics_database.yaml"

admin_user="${SUPERSET_ADMIN_USER:-admin}"
admin_password="${SUPERSET_ADMIN_PASSWORD:-admin}"
admin_email="${SUPERSET_ADMIN_EMAIL:-admin@example.com}"

echo "superset: upgrade metadata"
superset db upgrade

echo "superset: create admin if missing"
superset fab create-admin \
  --username "${admin_user}" \
  --firstname Admin \
  --lastname Admin \
  --email "${admin_email}" \
  --password "${admin_password}" || true

superset init

if [[ -f "${SOURCE_CONFIG}" ]]; then
  echo "superset: import ${SOURCE_CONFIG}"
  superset import-datasources -p "${SOURCE_CONFIG}" || true
fi

exec superset run -h "${SUPERSET_HOST}" -p "${SUPERSET_PORT}" --with-threads --reload --debugger
