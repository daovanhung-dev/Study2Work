# DB Admin database boundary

`app/core/database.py` and `app/core/runtime.py` create request-isolated
SQLAlchemy/psycopg3 connections for backend-owned named targets. Catalog reads
use `information_schema` and `pg_catalog`; SQL, DDL and row mutations validate
identifiers/schema and apply transaction rules.

The checked-in `sql/db_admin/001_bootstrap.sql` is an independent control-plane
bootstrap for `db_admin` metadata, access bindings and audit events. It is not a
Study or Work business migration, and its presence does not establish live
database state.
