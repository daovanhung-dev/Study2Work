# DB Admin API context

`apps/db-admin-server/app/api/routes.py` owns the `/api/v1/admin` surface for
auth, databases, catalog, DDL, SQL, rows and access/audit operations. Request
models and response types are defined in `app/core/contracts.py` and use the
local canonical envelope.

Runtime safety boundaries are server-side: target/schema validation,
permission dependencies, transaction-local search path, blocked SQL control
statements and single-use confirmation for destructive operations. The UI must
not be treated as an authorization boundary.

Legacy DDL/row routes may remain backend-compatible even when the simplified
Angular UI does not expose them; mark that distinction as `CURRENT_BEHAVIOR`.
