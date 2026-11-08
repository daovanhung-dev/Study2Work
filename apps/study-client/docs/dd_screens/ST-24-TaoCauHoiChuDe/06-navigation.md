# ST-24 — Navigation

## 1. Route definition
- Current route in inventory: `/student/discussions/new`
- Status: candidate/design route; Study Web `UNWIRED` unless source code proves otherwise.
- Route params/types: Không có route param được biểu diễn trong inventory string; route runtime vẫn chưa xác minh.
- Query params/defaults: preserve the inventory route string; detailed parsing rules only from source DD.
- Route guards: see source DD/API contract; do not create role policy.

## 2. Điểm vào
| From screen/route | Trigger | Params | Guard / fallback |
|---|---|---|---|
| [ST-23](../ST-23-DanhSachThaoLuan/00-overview.md) | Theo DD nguồn/inventory | Theo source; không suy diễn | Xem source DD; route chưa xác nhận runtime |

## 3. Điểm ra
| Destination | Trigger | Params | Điều kiện |
|---|---|---|---|
| [ST-23](../ST-23-DanhSachThaoLuan/00-overview.md), [ST-25](../ST-25-ChiTietThreadVaPhanHoi/00-overview.md) | Source event/inventory navigation | Theo source DD | Expected links; runtime chưa verify |

## 4. Back / refresh / deep link
- Back behavior: xem source DD; không mặc định browser history.
- Preserve filters/scroll/form state: chỉ nếu source có nêu, nếu không `CẦN_XÁC_NHẬN`.
- Refresh/direct URL: route trong inventory không chứng minh runtime.
- Invalid/missing ID: theo source DD/backend contract; không tự tạo validation.
- Not authenticated/authorized: theo source role guard; xem [Business Rules](05-business-rules.md).

## 5. Diagram
```mermaid
flowchart LR
  S0["ST-24 Tạo câu hỏi / chủ đề"] --> S1["ST-23"]
  S0["ST-24 Tạo câu hỏi / chủ đề"] --> S2["ST-25"]
```

## Source navigation and flow detail

### Trích từ DD nguồn: E. Ma trận trạng thái và điều hướng

### E.1. State matrix

| State | Điều kiện vào | Data/UI behavior | Chuyển tiếp / giới hạn |
|---|---|---|---|
| `unavailable` | Current `code.html` static content. | Chỉ báo form chưa sẵn sàng và back link; không phải API error/runtime result. | Back destination chỉ là prototype href; no form entry transition. |
| `design-sample` | Current `screen.png` populated design artifact. | Hiển thị sample course/lesson/title/tags/body/semester/SLA/mentor; các value không phải current data. | Không suy ra state transition từ ảnh. |
| `draft` | Expected after a wired form is initialized. | Inventory state; field defaults/course options/retention chưa được định nghĩa. | Input actions pending UI source. |
| `invalid` | Expected validation state. | Catalog required/type yields 422 at API boundary; title max, blank rules, tags, course options and field-level message unresolved. | Corrected input may return to draft only after validation policy exists. |
| `preview` | Expected click Xem trước. | Screenshot shows tab; renderer/GFM/security behavior not defined. | Return to compose behavior and state preservation unresolved. |
| `submitting` | Expected create request starts. | Inventory state only; no visible CTA, request serializer, duplicate prevention or loading UI. | 201→created; 401/403/422/500 or transport→error if implemented. |
| `created` | Expected #40 HTTP 201 success. | Response is `Page<Discussion>` but title/author/comments/page mapping unresolved. | Inventory expects ST-23 and #39 refresh; exact ordering/redirect data unresolved. |
| `error` | Auth/access/API/transport/parse failure. | Must be distinct from unavailable and success; current screen has no error panel/copy. | Retry/re-auth/back behavior not defined. |

No route guard, form editing, preview, validation, API call, state transition, or navigation is runtime-verified. `IMPLEMENTATION BLOCKED` and `RUNTIME NOT VERIFIED` remain separate from this DD state.

### E.2. Navigation and handoff matrix

| Origin/action | Expected target | Data / authorization | Current evidence |
|---|---|---|---|
| ST-23 create action | ST-24 `/student/discussions/new` | Student; selected course context expected, but no route/query contract. | Inventory/F07 only; ST-23 HTML source has no create control/runtime. |
| ST-24 back/forum breadcrumb | ST-23 `/student/discussions` | No draft preservation or return query defined. | HTML fallback href exists; no Study Web router. |
| ST-24 successful create | ST-23 then refresh via #39 (inventory expectation) | Candidate created data from #40; response/page mapping and sequencing open. | API #40 not runnable; no submit CTA. |
| ST-23 topic selection after refresh | ST-25 `/student/discussions/:discussionId` | Requires server-backed discussion ID and approved access. | Separate inventory flow; no direct ST-24 → ST-25 navigation is specified. |
| Header/home anchors | Other routes | Role/route target unknown. | Most screenshot links are static/prototype only. |

Do not pass lesson ID, tags, user ID, file URLs or editor encoding unless a canonical contract adds those fields. `course_id` must be selected from an approved source and authorized by server policy.

### Trích từ DD nguồn: B. Luồng hoạt động tổng thể

1. **Mở route:** inventory đề xuất `/student/discussions/new`, thường từ ST-23. Không có Study Web router/caller nên route, deep-link handling, query state và back stack chưa được xác minh. Screenshot không chứng minh route thực tế.
2. **Authentication/authorization:** expected Student session theo AC-19 và Bearer contract #40. User ID không nhập ở form. Course participation policy còn mở; không tự chọn enrollment status/access fallback.
3. **Khởi tạo form/options:** inventory yêu cầu course đã ghi danh. Screenshot có course selector và module/lesson selector, nhưng không tìm thấy API/options contract cho dữ liệu dropdown trong ST-24. API #39 trả discussions, không phải nguồn danh sách course/module. Không gán sample course/lesson thành defaults.
4. **Nhập metadata:** title là `string` required theo catalog; counter `74/150` và title sample chỉ là ảnh. Max length, empty/trim/normalization chưa được API DD hoặc inventory chốt. Tags và gợi ý tag không có trường trong request #40.
5. **Nhập nội dung:** editor hiển thị Markdown/code và GFM hint; không có renderer, sanitizer, source text contract hoặc attachment mapping được tìm thấy. Text editor không thể chuyển thành `int64` theo suy đoán.
6. **Preview/ảnh log:** screenshot có mode “Xem trước”, formatting controls và “Ảnh chụp log”. Current HTML/runtime không có handler, preview policy hoặc upload API được xác định. Không gọi API #34 vì contract upload đó thuộc flow khác và chưa có liên kết từ AC-19.
7. **Create:** expected trigger chưa xuất hiện trên screenshot. Nếu owner bổ sung trigger và giải quyết blockers, API catalog yêu cầu POST #40 với đúng body types, Student Bearer và HTTP 201. API DD hiện chưa quyết định content conversion, transaction, author/status/page mapping nên chưa thể mô tả request/commit thành logic chạy được.
8. **Sau response:** inventory kỳ vọng quay về ST-23 và refresh #39. Không biết dùng response của #40, GET #39 hay navigation state như thế nào; không tạo thread/detail ID hoặc direct route ST-25 từ proposals chưa duyệt.
9. **Lỗi:** giữ riêng 401/403/422/500 theo catalog. Mạng/timeout/response parse là client transport/data failure, không gán business code. UI error copy, retry, rollback và duplicate-submit policy chưa có nguồn.
