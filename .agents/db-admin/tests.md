# DB Admin tests and verification

The backend test suite covers access, bootstrap, catalog, DDL, HTTP, identifier
safety, password/security contracts and SQL execution. The current baseline is
`45 passed` in `apps/db-admin-server/.venv`.

Frontend verification uses the package `build` and `test` scripts when the Node
and browser toolchain is available. No live Neon mutation is part of the
verified local suite.
