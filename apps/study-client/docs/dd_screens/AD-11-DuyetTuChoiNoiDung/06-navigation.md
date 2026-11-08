# AD-11 — Navigation

## 1. Route definition
- Current route in inventory: `/admin/content/:contentId/review`
- Status: candidate/design route; Study Web `UNWIRED` unless source code proves otherwise.
- Route params/types: `contentId` (type/validation: see source DD; CẦN_XÁC_NHẬN if absent)
- Query params/defaults: preserve the inventory route string; detailed parsing rules only from source DD.
- Route guards: see source DD/API contract; do not create role policy.

## 2. Điểm vào
| From screen/route | Trigger | Params | Guard / fallback |
|---|---|---|---|
| [AD-10](../AD-10-HangDoiKiemDuyetNoiDung/00-overview.md) | Theo DD nguồn/inventory | Theo source; không suy diễn | Xem source DD; route chưa xác nhận runtime |

## 3. Điểm ra
| Destination | Trigger | Params | Điều kiện |
|---|---|---|---|
| [AD-10](../AD-10-HangDoiKiemDuyetNoiDung/00-overview.md) | Source event/inventory navigation | Theo source DD | Expected links; runtime chưa verify |

## 4. Back / refresh / deep link
- Back behavior: xem source DD; không mặc định browser history.
- Preserve filters/scroll/form state: chỉ nếu source có nêu, nếu không `CẦN_XÁC_NHẬN`.
- Refresh/direct URL: route trong inventory không chứng minh runtime.
- Invalid/missing ID: theo source DD/backend contract; không tự tạo validation.
- Not authenticated/authorized: theo source role guard; xem [Business Rules](05-business-rules.md).

## 5. Diagram
```mermaid
flowchart LR
  S0["AD-11 Duyệt/từ chối nội dung"] --> S1["AD-10"]
```

## Source navigation and flow detail

### Trích từ DD nguồn: E. Ma trận trạng thái và điều hướng

| State | Điều kiện | UI/data cần biểu diễn | Chuyển tiếp / giới hạn |
|---|---|---|---|
| `UNWIRED` | Current checkout thiếu Study Web source/router/client. | Chỉ có prototype static; không có request/runtime. | Current status. Runtime state chỉ được xác nhận sau khi frontend wire và verify riêng. |
| `loading-detail` | Route hợp lệ, GET #79 pending (target). | Loading shell/content; không hiển thị metadata cũ của Content khác. | 200→`ready`; auth/not-found/service error→error state. Client chưa wire. |
| `ready` | #79 trả Content shape hợp lệ. | Hiển thị field được hỗ trợ; author/version/preview unavailable cho tới khi có contract. | Approve→`approving`; reject form→`rejecting`; back action chưa route. |
| `preview-unavailable` | Payload không có schema/asset access contract. | Giữ placeholder/error có thông tin; không khẳng định secure renderer đã chạy. | Recovery behavior/content-type copy cần chốt. |
| `approving` | mutation action đang gọi PATCH #80 (bodyless). | Disable duplicate submit; preserve current item context. | 200→`decision-success`; 401/403/404/422/500/network→error state. Pending UI chưa có. |
| `rejecting` | Required reason đã nhập và PATCH #81 đang chạy. | Disable duplicate submit; body string exact; không clear reason khi lỗi nếu policy duyệt. | 200→`decision-success`; body/path/status 422, 401/403,404,500/network→error state. |
| `decision-success` | #80 200 status APPROVED hoặc #81 200 status REJECTED. | Show returned Content/status accurately; do not call #80 “published”. | AC-33 expects queue reload; route/cache behavior TBD. |
| `not-found/deleted` | #79 404; current source treats missing/tombstone alike. | Message and return path TBD; do not reveal deleted-row details. | Return AD-10/history semantics TBD. |
| `stale-or-not-pending` | #80/#81 422 non-pending, or resource was deleted. | Could represent changed/previously reviewed Content; exact cause/status payload is not guaranteed by screen contract. | Reload detail/queue vs conflict message TBD; no stale revision 409 exists. |
| `unauthorized` | 401 from auth helper. | Session/login flow not specified here. | Do not retry mutations automatically; auth-interceptor behavior not verified for Study Web. |
| `forbidden` | 403 shared role or future moderation authorization. | Access denied state; details must not expose policy internals. | Route/back behavior TBD. |
| `validation-error` | 422 #80 path/state, #81 body/path/state. | Correct field only for known #81 body validation; state/path cause is not reliably classified by current UI contract. | Preserve input where safe; exact mapping/codes require contract review. |
| `service/network-error` | 500 or transport failure. | Safe message; trace ID policy belongs to app-wide client convention. | Manual retry and mutation-uncertain handling TBD; no idempotency key. |

### Điều hướng và dữ liệu handoff

| Từ | Hành động | Đến | Data | Bằng chứng |
|---|---|---|---|---|
| AD-10 | Chọn một pending Content | AD-11 `/admin/content/:contentId/review` | Candidate `Content.id:int64` → `contentId`; không version | Inventory + AC-33 expected; current route/click absent. |
| AD-11 | Load detail | #79 | `content_id` path | Catalog + local route; local detail does not require pending status. |
| AD-11 | Approve | #80 | `content_id`; bodyless | Catalog/source. Local result `APPROVED`; not publish. |
| AD-11 | Reject | #81 | `content_id`, `reason:string` | Catalog/source. Local result `REJECTED`; no revision-request distinction. |
| AD-11 | Decision success | Reload AD-10/#78 | Current filters/page should be considered; no approved preservation rule | AC-33 expected; client not wired. |
| AD-11 | Back/browser history | AD-10 candidate | Potential Content ID, prior queue URL/filter/page | Mock link is `#`; no behavior source. |

Deep link with malformed/missing route param, empty detail, reload, queue return state, scroll/focus restoration, unsaved reason confirmation, action duplication, and permission redirect remain implementation decisions. Do not add a frontend flow until response cardinality, revision identity, permission and decision-state rules are resolved.

### Trích từ DD nguồn: B. Luồng tổng quát

```mermaid
flowchart TD
    A[AD-10 chọn Content] -->|candidate Content.id → contentId| B[AD-11 route đề xuất]
    B --> C{Admin session/permission}
    C -->|missing/invalid| E[401/403; UI chưa được wire]
    C -->|được phép| D[GET #79 detail]
    D -->|200 Content hiện tại| F[Render 8 field local; author/version/preview unavailable]
    D -->|404/500/network| G[Not-found hoặc error state; client policy chưa có]
    F --> H{Admin chọn quyết định}
    H -->|Approve| I[PATCH #80 path-only]
    H -->|Reject| J[PATCH #81 + required reason]
    I -->|200 APPROVED| K[AC-33 kỳ vọng reload #78]
    J -->|200 REJECTED + reason audit| K
    I -->|422 non-pending / 404 / 500| L[Decision error; UI treatment TBD]
    J -->|422 body/path/state / 404 / 500| L
    K --> M[AD-10 queue]
```

Luồng trên tách **expected navigation** khỏi **current endpoint evidence**. Chưa có client để xác minh route guards, selection handoff, form state, disabled-state release, success notification, query preservation, cache invalidation hay queue refresh.

### Source trace

```text
Expected: AD-10 #78 item → Content.id → AD-11 contentId → GET #79
          → PATCH #80 OR PATCH #81(reason) → reload AD-10/#78 (AC-33)
Current: no Study Web caller; #79 reads active Content row → direct Content;
         #80 PENDING_REVIEW→APPROVED + audit; #81 PENDING_REVIEW→REJECTED
         + reason-bearing audit row. No revision token connects read to mutation.
```

Nguồn chính: [inventory](../../list_screen.md), [API catalog](../../../../../docs/lists/list_api.md), [AC-33 diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio), [router #79–#81](../../../../study-server/app/api/v1.py), [#79 module](../../../../study-server/app/modules/admin/api_79_admin_content_detail), [#80 module](../../../../study-server/app/modules/admin/api_80_admin_content_approve), [#81 module](../../../../study-server/app/modules/admin/api_81_admin_content_reject).
