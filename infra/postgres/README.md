# PostgreSQL Schema V1-PILOT

This directory contains the standalone initial PostgreSQL 16 schema for the
three physical databases defined by `docs/BD/03_THIET_KE_CO_SO_DU_LIEU.md`.
The scripts deliberately do not create databases, application LOGIN roles,
credentials, seed data, cross-database foreign keys, or event-broker assets.

| Target database | Initial script | Public tables | Scope |
| --- | --- | ---: | --- |
| `identity_db` | `identity_db/001_initial_schema.sql` | 20 | IAM identity, authentication, authorization, security audit and outbox |
| `study_db` | `study_db/001_initial_schema.sql` | 60 | Study domain and local projections of identity |
| `work_db` | `work_db/001_initial_schema.sql` | 98 | Work, University, AI and Payment domains and local projections |

## Preconditions

- PostgreSQL **16** with the `pg_trgm` and `btree_gist` extension packages
  installed.  The scripts create only the extensions needed by their target
  database.
- A newly provisioned target database.  Run the corresponding initial script
  once only; it is intentionally an initial-schema artifact, not a migration
  runner.
- The execution principal must be allowed to create NOLOGIN roles, extensions,
  schemas, tables, functions, policies and ownership changes.  It must be able
  to grant the resulting roles to the real LOGIN principals provisioned by the
  deployment environment.

The database names in this document are deployment names, not a mechanism for
cross-database access.  No foreign key, view, function, or query in these
scripts traverses from one of the three databases into another.

## Apply

Provision each database outside this repository, then run its script against
that database.  `ON_ERROR_STOP` ensures a failed statement aborts the script;
each script is wrapped in a single transaction so a failure rolls back its
schema changes.

```bash
psql -X -v ON_ERROR_STOP=1 -d identity_db -f infra/postgres/identity_db/001_initial_schema.sql
psql -X -v ON_ERROR_STOP=1 -d study_db    -f infra/postgres/study_db/001_initial_schema.sql
psql -X -v ON_ERROR_STOP=1 -d work_db     -f infra/postgres/work_db/001_initial_schema.sql
```

The scripts create four NOLOGIN group roles per database namespace:

| Database | Owner | Application | Worker | Read-only |
| --- | --- | --- | --- | --- |
| Identity | `s2w_identity_owner` | `s2w_identity_app` | `s2w_identity_worker` | `s2w_identity_readonly` |
| Study | `s2w_study_owner` | `s2w_study_app` | `s2w_study_worker` | `s2w_study_readonly` |
| Work | `s2w_work_owner` | `s2w_work_app` | `s2w_work_worker` | `s2w_work_readonly` |

Create the deployment's LOGIN principals and assign their membership outside
source control, for example:

```sql
GRANT s2w_study_app TO deployment_study_api_login;
```

No password, LOGIN capability, service secret, or credential is stored here.

## Row-level security contract

Tenant-scoped calls must begin a transaction and set both GUCs before querying
or mutating data.  The worker role follows the same tenant-context rule.

```sql
BEGIN;
SET LOCAL ROLE s2w_study_app;
SET LOCAL app.subject_id = '00000000-0000-0000-0000-000000000001';
SET LOCAL app.tenant_id  = '00000000-0000-0000-0000-000000000002';
-- application query or mutation
COMMIT;
```

`app.subject_id` is also used by subject-owned policies where the BD defines a
learner or candidate ownership boundary.  An omitted, malformed, or mismatched
context does not grant access.  Database owners and superusers can bypass RLS;
application connections must not be members of the owner role.

## Validate

Run the assertion script after applying the corresponding initial schema to a
fresh PostgreSQL 16 database:

```bash
psql -X -v ON_ERROR_STOP=1 -d identity_db -f infra/postgres/tests/identity_db_assertions.sql
psql -X -v ON_ERROR_STOP=1 -d study_db    -f infra/postgres/tests/study_db_assertions.sql
psql -X -v ON_ERROR_STOP=1 -d work_db     -f infra/postgres/tests/work_db_assertions.sql
```

The assertions check the public-table inventory, required schema elements,
tenant foreign-key shape, role grants and RLS configuration.  They also
exercise the invariants that can be verified without seed data.  The scripts
are diagnostic only: they roll back their fixture rows and do not seed a
database.

## Explicit source gaps retained as gaps

The following matters are documented in comments where they affect a schema
but are not modeled as new tables, fields or enum values.  They require a
source-design decision before an additive migration can be written:

- identity `authVersion` and MFA pending-enrollment state;
- Study onboarding draft/configured-question state, learner skills/history and
  evidence-to-file relationship;
- candidate-search consent history and public job slug;
- entitlement reservation/hold and refund-approval history, promotion raw
  event persistence and `PAYMENT_SETTLED` lifecycle clarification;
- AI evaluation-run and kill-switch execution model;
- Operations, University and other API/read-flow models not represented by an
  approved physical schema.

The schema reflects the approved BD03 data model only.  It does not attempt to
repair or infer any of these gaps.
