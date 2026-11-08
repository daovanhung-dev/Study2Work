# AD-23 — Data Flow & State

## 1. Nguồn dữ liệu
| Field / object | Type | Source | Destination | Cập nhật khi |
|---|---|---|---|---|
| Chỉ liệt kê theo bằng chứng trong excerpt bên dưới | Theo DD/API source | API/inventory/design; status phải giữ nguyên | UI/state nêu ở DD nguồn | Theo event source |

## 2. State model

> Không tạo DTO/ViewModel mới khi chưa có contract. State, DTO và mapping được trích nguyên ngữ cảnh từ DD nguồn bên dưới.

## 3. API DTO → ViewModel mapping

### Trích từ DD nguồn: B. Mô tả luồng hoạt động tổng thể

### Luồng dự kiến theo AC/catalog

1. Admin chọn một Discussion từ AD-22. Expected handoff is a Discussion ID; exact URL/state transfer, selected report context and root-versus-reply target are not specified.
2. Candidate AD-23 route is entered. A future client would need to validate the path value before requesting #98. The catalog requires `discussion_id:int64!`; it does not define frontend parsing or route fallback.
3. Expected API call #98 is `GET /api/v1/admin/discussions/{discussion_id}` with Bearer JWT and Admin role. Direct catalog response is `ApiEnvelope<Page<Discussion>>`. AC expects reports in addition to discussion/comments, but the catalog response shape does not identify report fields.
4. If #98 returns successfully, AC expects Admin to inspect thread and report context. Local source currently returns a Discussion plus direct comments only, with a one-item page; it cannot populate report reason/severity/reporter/count/timestamp. The current prototype does not render returned data.
5. AC-37 has a no-violation path saying dismiss report, but no API or action mapping is listed. This branch is blocked.
6. For a violation, AC describes hide, lock or warn. Candidate #99 is `PATCH /api/v1/admin/discussions/{discussion_id}/moderate` with required string fields `action` and `reason`, Bearer JWT/Admin, and `ApiEnvelope<Page<Discussion>>` response. Exact action values, status transitions, validation, audit storage and atomicity are unresolved. Do not fabricate request values or success UI.
7. AC allows conditional deletion after moderation using separate #100 `DELETE /api/v1/admin/discussions/{discussion_id}`. Catalog has no body/query and returns `ApiEnvelope<DeleteResult>`. AC says soft delete and preserve audit; deletion eligibility, physical state/timestamp, repeat behavior and audit linkage are unresolved. The prototype's delete radio is not a valid mapping to this separate endpoint.
8. Expected navigation returns to AD-22 and the inventory links describe refresh through #97. No cache invalidation, preserved filters/page, retry or redirect-on-error contract is specified. Prototype links are fragment-only and do not perform navigation.

### Current static behavior

1. Prototype opens with unresolved Discussion ID, unloaded summary fields, empty thread state and safety-lock banner.
2. All four radio options, reason textarea and apply button are disabled. No event handler or request runs.
3. Header button, empty-state CTA and cancel link point to fragment `#ad-22`; navigation shell/footer links are `#`; bell has no handler.
4. No success, processing, resolved, conflict, API error, session-expired or server-empty state is implemented in this HTML.

### Trích từ DD nguồn: E. Ma trận trạng thái và điều hướng

### State matrix

| State | Source/status | Entry/transition | UI treatment and next step |
|---|---|---|---|
| Static placeholder / unloaded | **Current prototype** | Initial HTML render. | ID invalid/unloaded message, summary placeholders, empty thread, safety banner and disabled controls. No network request. |
| Loading detail | **Expected by inventory; not implemented** | Would follow future page entry / #98 request. | No spinner/timeout/retry contract defined. Do not equate the static “Chờ nạp bản ghi” badge with a running request. |
| Reviewing detail | **Expected by AC; blocked by projection gap** | Would require #98 success and enough approved detail data. | Current #98 lacks report fields, so full report review cannot be shown. No report-specific UI mapping may be invented. |
| Empty/missing target | **Local #98 evidence / expected handling not wired** | Invalid or missing ID/Discussion produces 404 in local #98. | Current HTML has only placeholder; not a live 404 view. Client response mapping/return behavior is undefined. |
| Unauthorized / forbidden | **Catalog and local #98 guard evidence** | Catalog 401/403; local #98 checks `ADMIN`. | UI message, re-auth, access-denied route and AC permission mapping are unspecified. |
| Decision selected / ready | **Not reachable in current prototype** | Radios and reason input would need an approved contract; controls are disabled. | Do not enable or infer values/validation. |
| Processing | **Inventory expected state; #99/#100 unwired** | Would follow an approved PATCH/DELETE submit. | No local mutation endpoint or processing UI. Duplicate-submit and retry behavior unresolved. |
| Resolved / updated | **AC/catalog expected only** | #99 200 `DESIGN_RESOURCE_UPDATED` or #100 200 `DESIGN_RESOURCE_DELETED`. | Response mapping, audit confirmation, destination and #97 refresh invalidation need approval. |
| Conflict / stale state | **Inventory expected state only** | Trigger and API code are not present; catalog #99/#100 do not list 409. | Do not claim conflict detection or design recovery behavior as implemented. |
| Server/network failure | **Catalog partially defines server errors; network unspecified** | #98/#99/#100 catalogued 500; #99/#100 also 422. | No current error UI, retry, offline or network handling exists. Do not invent policy. |

### Navigation and data handoff

| From / to | Expected link | Data | Current status |
|---|---|---|---|
| AD-22 → AD-23 | Select a reported Discussion and open candidate detail route. | Discussion ID is needed by #98; report ID, report reason and root/reply semantics are not specified by the API path. | Inventory/AC expectation; Study Web route absent. Current AD-22 evidence does not establish a complete report detail handoff. |
| AD-23 → AD-22 via #13/#29/#41 | Return to the report queue; inventory links queue refresh to #97. | Whether to preserve filters/page/current row is unspecified. | HTML fragment `#ad-22`; no route transition or #97 call. |
| AD-23 → #99 | Submit approved moderation action and reason. | `discussion_id:int64`, `action:string`, `reason:string`. | Catalog/Draft only; no local route or action mapping. |
| AD-23 → #100 | Conditional separate delete after review. | `discussion_id:int64`; catalog declares no body/query. | Catalog/Draft only; no local route and no approved trigger/confirmation semantics. |

### Security, privacy and usability constraints

- Treat the page as Admin-only in the design, but do not equate AC permission with local `ADMIN` without an approved mapping. Server authorization remains mandatory even if UI is eventually enabled.
- Do not expose discussion/report content until target ownership, requester permission and report visibility are established. No report data exists in the current #98 projection.
- Reason content may be sensitive and AC expects audit, but retention, actor identity, access to audit, masking and atomicity are not defined; avoid promising storage/security properties from static banner copy.
- Disabled controls are the current prototype state. Accessible reason text, radio names/labels, focus order, keyboard operation and announcement of server errors need implementation and review after contracts are settled.
- Responsive behavior, truncation, long-thread pagination and comment visibility are not described by available artifacts; no behavior is specified here.

## 4. Luồng đọc (Read)
- Orchestration từ inventory: GET #98 → PATCH #99 với action/reason hoặc DELETE #100 → refresh #97.
- Chi tiết current/source mapping: xem [API Integration](04-api-integration.md) và DD nguồn.

## 5. Luồng ghi (Write)
- Chỉ mô tả mutation được DD/API source nêu; không thêm endpoint hoặc side effect.
- Source trace: [AD-23](../../screen_stitch/05_admin/AD-23_dieu-tra-kiem-duyet-thao-luan/AD-23.md)

## 6. Cache / concurrency / lifecycle
- Cache, race, cleanup, pagination: xem các section source bên dưới; nếu không có bằng chứng thì để `CẦN_XÁC_NHẬN`.

## 7. Data errors & security
- Theo error/security/source-status section của DD nguồn; không coi state trong mockup là runtime behavior.

## 8. Trace
[Events](02-events.md) · [API](04-api-integration.md) · [Rules](05-business-rules.md)
