# DB Admin security and audit context

- `app/core/security.py` validates OIDC/JWKS or controlled local development
  auth; local JWTs stay in frontend memory.
- `app/core/runtime.py` selects configured database targets and audit runtime.
- `app/services/audit.py` keeps bounded in-memory/structured-log fallback and
  persists to `db_admin.admin_audit_events` when a configured target supports
  the control-plane table.
- `sql/db_admin/001_bootstrap.sql` creates the independent DB Admin control
  schema; it does not prove that a live Neon target has been bootstrapped.
- `scripts/bootstrap_access.py` is the operator path for access bootstrap and
  password reset; it must not write plaintext credentials to source or logs.

Status: `AUDIT_RUNTIME=VERIFIED_WITH_TARGET_DEPENDENCY` and
`LIVE_BOOTSTRAP=NOT_VERIFIED_HERE`.
