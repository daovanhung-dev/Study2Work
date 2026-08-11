# API Guidelines

New Study and Work APIs use:

- Standard envelope with `success`, `businessCode`, `message`, `data`, `meta`, and `traceId`.
- Error responses set `data` to `null` and place safe field-level details in
  `meta.fieldErrors`; they do not expose a top-level `errors` field.
- `X-Trace-Id` request and response propagation.
- `/api/v1` for public APIs.
- `/internal/v1` for service-to-service APIs.
- `Idempotency-Key` for retryable mutations.
- Stable error codes and safe client messages.
