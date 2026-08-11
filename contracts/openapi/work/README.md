# Work OpenAPI

[`openapi.json`](openapi.json) is the canonical, versioned Work API baseline.
It currently defines the unauthenticated liveness and readiness endpoints served
by `apps/work-server`, plus the public API root:

- `GET /api/v1`
- `GET /health/live`
- `GET /health/ready`

Both responses use the standard success envelope and return the same trace ID in
the `X-Trace-Id` response header and `traceId` body field. The Work browser app
in `apps/work-client/web` calls the API through `VITE_WORK_API_URL`; it is not
part of this API contract.

When the database check cannot complete, `/health/ready` returns a `503`
`DEPENDENCY_UNAVAILABLE` error envelope with the same trace propagation.

The public Work domain surface remains governed by
[`docs/BD/04_DAC_TA_API.md`](../../../docs/BD/04_DAC_TA_API.md). Add each
implemented endpoint to this document rather than deriving a contract from the
legacy server-rendered application.
