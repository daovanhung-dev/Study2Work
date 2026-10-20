#!/usr/bin/env bash
set -euo pipefail

PSQL="${PSQL:-psql}"
PGUSER="${PGUSER:-postgres}"
PGHOST="${PGHOST:-127.0.0.1}"
PGPORT="${PGPORT:-5432}"

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

"$PSQL" -v ON_ERROR_STOP=1 -U "$PGUSER" -h "$PGHOST" -p "$PGPORT" -d postgres -f "$BASE_DIR/00_bootstrap_databases.sql"
"$PSQL" -v ON_ERROR_STOP=1 -U "$PGUSER" -h "$PGHOST" -p "$PGPORT" -d identity_db -f "$BASE_DIR/01_identity_db.sql"
"$PSQL" -v ON_ERROR_STOP=1 -U "$PGUSER" -h "$PGHOST" -p "$PGPORT" -d study_db -f "$BASE_DIR/02_study_db.sql"
"$PSQL" -v ON_ERROR_STOP=1 -U "$PGUSER" -h "$PGHOST" -p "$PGPORT" -d work_db -f "$BASE_DIR/03_work_db.sql"

echo "Study2Work V1-PILOT databases created."
