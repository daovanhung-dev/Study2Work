# VERIFICATION_REPORT — Study API #63

## Kết quả

- DD status: `Draft — Needs Confirmation`. Catalog fields/types/status/errors remain direct; CSV parsing, common-course scope, legacy mapping, outbox and ID handoff are marked DERIVED in the DD.
- Deliverable: 8 template sheets and 3 Markdown reports. All 8 sheets remain Draft; Excel source appendices were preserved.
- Runtime API #63: route/module/test are wired locally and pass HTTP tests with fake DB sessions. This does not verify live schema or deployment.
- Macro-review AC-25 #62–#64 + API #18: `VERIFIED_WITH_OPEN_QUESTIONS`; the local #64 ID handoff is documented, while contract gaps remain explicit.

## Kiểm tra

| Check | Kết quả | Trạng thái |
|---|---|---|
| Skill/template | `createDD-markdown` được registry wire; fingerprints của 8 template và appendix template khớp ở lần authoring. | VERIFIED_STATIC_ONLY |
| Manifest/front matter | Đủ 11/11 file; 8/8 sheet có `dd_id: 63` và trạng thái Draft. | VERIFIED_STATIC_ONLY |
| Contract/request/error | 4 body field/type trực tiếp; HTTP 202 `ApiEnvelope<Operation>`; 5 error code catalog, không thêm mã. | VERIFIED_STATIC_ONLY |
| AC-25 trace | Flow #62 → #63 → Push/Email → #64 được đối chiếu; API #18 không có edge trực tiếp trên diagram. | VERIFIED_STATIC_ONLY |
| Local mapping | Legacy per-recipient BIGINT notification rows, shared Operation UUID, QUEUED delivery outbox and `meta.notification_ids` are documented as DERIVED. | VERIFIED_DERIVED_LOCAL_MAPPING |
| Focused HTTP tests | API #63: 23 passed; linked #62–#63 regression: 41 passed; one upstream Starlette/httpx deprecation warning. Fake DB sessions only. | PASS_LOCAL_HTTP |
| Full Study suite | 638 passed; one upstream Starlette/httpx deprecation warning. | PASS_LOCAL |
| Ruff | Focused API #63 source/test check passed. | PASS |
| Migration/deployment | Migration 009 and `DB.sql` are checked-in source only; not applied or live-verified. | NOT_VERIFIED_HERE |
| Delivery worker/provider | No consumer or Push/Email provider is wired; accepted outbox rows remain `QUEUED`. | NOT_IMPLEMENTED |
| Context validator | Node is unavailable; Deno fallback reports the repository's existing missing DB Admin context/source paths. Full drift mode also reports source changes against the old repository source commit across existing scopes. | BASELINE_FAILURE_OUTSIDE_SCOPE |

## Giới hạn còn mở

- API contract still does not specify recipient/channel encoding, course scope, message text type, or an Operation-to-notification ID handoff; current behavior is a DERIVED local fallback.
- The body has no `course_id`, so common-course membership cannot prove that recipients came from the exact course selected in the UI.
- HTTP tests use fake DB results. Live PostgreSQL schema, migration deployment, worker/provider delivery, API #64 runtime compatibility, and API #18 polling remain unverified.

Xem [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md) và [PLAN_RESULT.md](./PLAN_RESULT.md).
