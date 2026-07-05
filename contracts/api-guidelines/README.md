# API Guidelines

New Study and Work APIs use:

- Standard envelope with `success`, `businessCode`, `message`, `data` or `errors`, optional `meta`, and `traceId`.
- `X-Trace-Id` request and response propagation.
- `/api/v1` for public APIs.
- `/internal/v1` for service-to-service APIs.
- `Idempotency-Key` for retryable mutations.
- Stable error codes and safe client messages.
