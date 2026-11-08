# AD-25 — Navigation

## 1. Route definition
- Current route in inventory: `/admin/reports/export`
- Status: candidate/design route; Study Web `UNWIRED` unless source code proves otherwise.
- Route params/types: Không có route param được biểu diễn trong inventory string; route runtime vẫn chưa xác minh.
- Query params/defaults: preserve the inventory route string; detailed parsing rules only from source DD.
- Route guards: see source DD/API contract; do not create role policy.

## 2. Điểm vào
| From screen/route | Trigger | Params | Guard / fallback |
|---|---|---|---|
| [SH-07](../SH-07-TheoDoiTacVuBatDongBo/00-overview.md), [AD-24](../AD-24-BaoCaoTacDongCongDong/00-overview.md) | Theo DD nguồn/inventory | Theo source; không suy diễn | Xem source DD; route chưa xác nhận runtime |

## 3. Điểm ra
| Destination | Trigger | Params | Điều kiện |
|---|---|---|---|
| [AD-24](../AD-24-BaoCaoTacDongCongDong/00-overview.md), [SH-07](../SH-07-TheoDoiTacVuBatDongBo/00-overview.md) | Source event/inventory navigation | Theo source DD | Expected links; runtime chưa verify |

## 4. Back / refresh / deep link
- Back behavior: xem source DD; không mặc định browser history.
- Preserve filters/scroll/form state: chỉ nếu source có nêu, nếu không `CẦN_XÁC_NHẬN`.
- Refresh/direct URL: route trong inventory không chứng minh runtime.
- Invalid/missing ID: theo source DD/backend contract; không tự tạo validation.
- Not authenticated/authorized: theo source role guard; xem [Business Rules](05-business-rules.md).

## 5. Diagram
```mermaid
flowchart LR
  S0["AD-25 Xuất báo cáo và theo dõi tiến trình"] --> S1["AD-24"]
  S0["AD-25 Xuất báo cáo và theo dõi tiến trình"] --> S2["SH-07"]
```

## Source navigation and flow detail

### Trích từ DD nguồn: E. Trạng thái, điều hướng và yêu cầu phi chức năng

### E.1. Ma trận trạng thái

| State | Bằng chứng hiện tại | Điều kiện/transition kỳ vọng còn cần quyết định |
|---|---|---|
| `INITIAL_STATIC` | Trang tĩnh với CSV, hai scope, month, placeholder ID/status/result và disabled Download. | Route/auth resolution, nguồn Admin identity, filter query restore và loading state. |
| `CONFIGURING_LOCAL` | Native radio/checkbox state thay đổi trong browser. | Scope/date/format validation, defaults, state persistence và custom date controls. |
| `SUBMIT_BLOCKED_CURRENT` | Submit event bị `preventDefault()`; không có side effect. | Không được đổi thành `SUBMITTING` cho đến khi GET acceptance/retry và validation contracts được duyệt. |
| `ACCEPTED` (proposed) | Không có current representation. Inventory/API catalog dự kiến 202 acceptance; body lại mâu thuẫn Report/Operation. | Chốt payload có operation ID; chỉ hiển thị accepted sau khi parse response hợp lệ. 202 không có nghĩa ready/completed. |
| `PROCESSING` (proposed) | Progress/status card hiện static, không phản ánh server. | Chốt #18 producer edge, status enum and mapping; polling/refresh frequency and stop condition. Inventory states differ from SH-07 states. |
| `READY_WITH_ARTIFACT` (proposed) | Không có current artifact; Download disabled. | Chốt terminal state, ExportAsset result, link/endpoint, access/expiry and ready UI. |
| `FAILED` / `EXPIRED` (proposed) | Không có current error/expired state. | Chốt Operation error schema, artifact expiration, recovery, re-export and whether operation remains queryable. |
| `UNAUTHORIZED` / `FORBIDDEN` (proposed) | No route guard or API request currently. | Chốt AC report permission ↔ JWT role/claim mapping and safe shell recovery behavior. |

Các state “proposed” chỉ phản ánh inventory/AC intent; chúng không phải state enum đã được API #18 xác nhận. Không đồng nhất `ready` với `succeeded`, hay `processing` với `running`, trước khi có mapping.

### E.2. Điều hướng và giữ ngữ cảnh

| From / action | Candidate target | Current source | Gate |
|---|---|---|---|
| AD-24 export CTA | `/admin/reports/export` | Inventory candidate; AD-24 prototype link không gửi query. | Chốt tên/query schema cho date, segment và format; giữ filter chỉ khi được approve. |
| AD-25 back link | AD-24 candidate `/admin/reports/community-impact` | `href="#"`. | Chốt query restore và behavior khi không có prior state. |
| Operation handoff | SH-07 `/operations/:operationId` | Callout không interactive; không có ID. | AC-38 edge, API #103 response field, ID type, owner/access rule, state mapping. |
| Shell/footer | Shared route destinations | Placeholder anchors/buttons. | Shared shell/router owns destination and notification behavior; not specified here. |

Route strings are candidates from inventory only; Study Web contains no editable route source. Do not mark any handoff implemented.

### E.3. Access, privacy, accessibility and presentation

- AC-38 expected precondition is Admin with report/analytics permission. Catalog #103 says role Admin. Current shared auth helper accepting explicit roles and use of `ADMIN` by earlier Admin routes proves helper capability only, not #103 policy. Enforce server authorization after approval; do not rely on badge, hidden controls or static identity.
- Export filter choices and generated artifacts may expose report data. No data classification, minimization rule, owner policy, download audit requirement or storage control is approved for this screen. Do not state the mockup's RBAC L3, signed URL, checksum, audit/IP/session, browser cache or 24-hour deletion as implemented behavior.
- For implementation, follow `.agents/web-study/design.md`: semantic ocean tokens, Inter/system fonts, responsive layout, visible focus, keyboard operation, accessible names, error association and reduced motion. The mockup's cobalt palette, Plus Jakarta Sans and Tailwind CDN conflict with that guide; preserve the original image as evidence and treat design alignment as an implementation task.
- Radio/checkbox groups need programmatic labels and group names; status updates, if introduced after API contract approval, need a screen-reader announcement strategy. The current prototype provides native controls but does not define dynamic accessible status announcements. Do not fabricate progress percentages.
- The screenshot is 1368×1600 and `screen_annotated.png` is a 2× evidence render, not a responsive production specification.

### Trích từ DD nguồn: B. Mô tả luồng hoạt động tổng thể

### Expected flow theo inventory, AC-38 and API design

1. An Admin with approved report/analytics access reaches candidate `/admin/reports/export`, optionally from AD-24. Inventory expects filters to be retained, but neither screen has an approved query/state-transfer format.
2. The user chooses one file format, one or more report scopes, and a period preset in the prototype. API #103 declares only optional string query fields `filters` and `format`; it does not define how these controls map to them. The custom period option has no date inputs in the screenshot.
3. If API #103 contract is finalized, its direct row specifies `GET /api/v1/admin/reports/community-impact/export`, Bearer JWT/Admin, optional `filters?:string`, `format?:string`, no body, HTTP 202 `DESIGN_OPERATION_ACCEPTED`, and 401/403/503/500. It does not declare 400/422 for unsupported values.
4. At HTTP 202, response mapping is unresolved: the endpoint row specifies `ApiEnvelope<Report>`, while the same catalog's Operation-tracking paragraph specifies `data:Operation`. The #103 API DD records both and proposes Operation only as `DERIVED`.
5. AC-38 describes generating CSV/XLSX/PDF or an export job, temporary file storage if generated server-side, and showing the report/download result. It does not define a queue, worker, storage provider, accepted status state machine or download lifecycle.
6. The inventory conditionally expects GET #18/SH-07 when a confirmed operation ID exists. The #18 catalog row uses `int64`, while reusable Operation schema and AC use UUID; owner-only versus owner/Admin access and per-kind result are also unresolved. AC-38 contains an operation status node but no edge connects it to its export branch.
7. A completed export could expose an `ExportAsset` candidate, but reusable Operation currently says `result?:Payment`; download URL, authorization, expiry and cleanup are not agreed. Do not enable Download or route to SH-07 until these contracts are approved.
8. The user may return to AD-24, but the current back anchor is `#`; whether the effective filter set survives the round trip is open.

### Current static flow in `code.html`

1. Initial HTML paints CSV selected, course/learner scopes checked, community scope unchecked, month selected, a no-operation ID placeholder, a static “ready to start” label, empty result message and a disabled download button.
2. Radio and checkbox controls update only their native browser selection. The custom period has no associated date input, and the GMT+7 note is static.
3. Clicking “Bắt đầu tạo tác vụ xuất file” fires the form's inline `onsubmit="event.preventDefault();"`. It prevents form navigation and performs no other action; no API request, operation ID, progress state or error message is produced.
4. Download cannot be activated because the button is disabled; no result URL, anchor or download handler exists.
5. The SH-07 card is informational copy without an anchor/button. The AD-24 back link and shell/footer links use `href="#"`; the notification button has no listener.
6. Worker Node 04, Celery scheduling, “RBAC L3”, checksum verification, audit logging, URL expiry and file cleanup are static claims. No server, storage or telemetry call validates them.
