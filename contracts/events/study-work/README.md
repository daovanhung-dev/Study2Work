# Study to Work Events

Study publishes evidence events after the source transaction commits. Work verifies transport headers, validates the JSON Schema, applies idempotency, and stores local snapshots.

Required headers:

```text
X-S2W-Event-Id: <uuid>
X-S2W-Event-Type: study.evidence.upserted.v1
X-S2W-Event-Version: 1
X-S2W-Timestamp: 2026-07-05T10:00:00Z
X-S2W-Signature: sha256=<hmac>
X-Correlation-Id: <uuid>
```

Work must reject invalid signatures before using the business payload.
