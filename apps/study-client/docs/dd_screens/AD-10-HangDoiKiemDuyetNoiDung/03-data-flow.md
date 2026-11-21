# AD-10 — Data Flow & State

## 1. Nguồn dữ liệu
| Field / object | Type | Source | Destination | Cập nhật khi |
|---|---|---|---|---|
| Chỉ liệt kê theo bằng chứng trong excerpt bên dưới | Theo DD/API source | API/inventory/design; status phải giữ nguyên | UI/state nêu ở DD nguồn | Theo event source |

## 2. State model

> Không tạo DTO/ViewModel mới khi chưa có contract. State, DTO và mapping được trích nguyên ngữ cảnh từ DD nguồn bên dưới.

## 3. API DTO → ViewModel mapping

### Trích từ DD nguồn: B. Mô tả luồng hoạt động tổng thể (snapshot trước khi Angular route/page/API caller được thêm)

1. Admin mở route đề xuất từ vùng kiểm duyệt. Route, shell navigation và auth integration chưa được triển khai trong Study Web.
2. Khi có client, gửi Bearer token theo API #78. Current server guard kiểm tra authentication và role `ADMIN` trước query validation/DB; điều kiện AC-33 về permission moderation riêng vẫn cần quyết định.
3. Khởi tạo queue bằng GET `/api/v1/admin/content/pending`; query ban đầu có thể bỏ `type`/`course` và dùng `page=1` theo local fallback. Không có body. Mapping các giá trị `all`/slug của prototype sang query chưa được duyệt.
4. Current #78 parse raw `type` như chuỗi exact-match; parse `course` signed int64 và `page` positive int32. Local default page là 1. Invalid numeric value trả local 422 `DESIGN_VALIDATION_ERROR`, dù catalog hiện chỉ nêu 401/403/500.
5. Local query đếm và lấy cùng predicate trên active `contents` (`deleted_at IS NULL`, `status='PENDING_REVIEW'`), filters tùy chọn, order `id ASC`, limit 20 và offset theo page. Đây là source hiện tại với một số lựa chọn DERIVED trong API DD; không chứng minh schema live.
6. Local success response là envelope với `data.items` và `data.pagination` (`page`, `size`, `total`, `total_pages`). Map tám field Content có sẵn; không tạo dữ liệu cho course title, author, submitted time hoặc version. Catalog/AC vẫn quy định singular Content nên client contract cần được owner đồng bộ trước khi wire.
7. `items=[]` biểu diễn empty/no-match/out-of-range page trong local source. `items` có dữ liệu không đủ để render toàn bộ cột mockup hoặc xác nhận version còn pending tại thời điểm chuyển sang AD-11.
8. Chọn row theo AC-33 sẽ chuyển `content_id` đến AD-11/#79. Khi DD/API revision contract chưa được giải quyết, chỉ `Content.id` là candidate identity; không tự đính kèm version/author.
9. Sau #80/#81, AC-33 yêu cầu reload queue; quyết định đó được thực hiện từ flow AD-11. Điều hướng quay lại, giữ filter/page, cache invalidation và stale-row conflict chưa có client policy.
10. Lỗi auth/role/query/DB/network hiển thị theo trạng thái; không tự retry request GET hoặc tạo thông báo nghiệp vụ khi chưa có client convention. Local 500 dùng envelope an toàn, không lộ SQL/stack.

**Quan hệ màn hình:** AD-10 là queue trước AD-11. AD-11 đọc #79, ra quyết định bằng #80/#81, rồi AC-33 quay lại/refresh AD-10. Route/history và payload duy trì filter chưa được wire hoặc chốt. AD-10 không thực hiện approve/reject.

### Trích từ DD nguồn: E. Ma trận trạng thái và điều hướng

| Trạng thái | Điều kiện vào | Hành vi/UI hiện được xác nhận | Chuyển tiếp |
|---|---|---|---|
| `UNWIRED` (historical pre-implementation state) | Original DD snapshot before Angular route/page/API source was added. | This historical row is superseded by the current-source audit below; browser/runtime remains unverified. | Do not treat as current checkout status. |
| `loading` | Target state khi route client được wire và GET #78 đang chạy. | Không tồn tại trong current app source; spinner #21 chỉ local 700 ms. | Success→`ready`/`empty`; auth/validation/server/network failure→`error` (client policy cần chốt). |
| `empty` | Local response có `items=[]` (contract cardinality cần đồng bộ). | Screenshot hiện static empty illustration/copy, count 0/0; chưa bind API. | Refresh/filter/page theo contract; không có row để đi AD-11. |
| `ready` | Response hợp lệ có item sau khi response contract và các cột được chốt. | Prototype không có row; API projection hiện thiếu course title/author/time. | Chọn item→AD-11 với candidate `content_id`; #80/#81 xong thì AC-33 reload queue. |
| `error-auth` | 401 từ API. | Không có error UI source. | Session/login handling chưa được quy định cho Study Web. |
| `error-forbidden` | 403 từ shared role guard hoặc permission policy. | Không có error UI source; ADMIN vs moderation permission open. | Chặn route/action; redirect/inline behavior chưa quyết định. |
| `error-validation` | 422 numeric query từ local current source. | Catalog chưa liệt kê; không có error UI source. | Không gửi request lặp lại nếu query chưa sửa; field feedback convention chưa chốt. |
| `error-service/network` | 500 hoặc lỗi transport/timeout. | Angular `adminQueryState` now renders the shared safe error state; the user can retry through manual refresh. Timeout and retained-data policies remain undocumented. |
| `stale-item` | Content thay đổi/xóa/không còn pending giữa queue và #79/#80/#81. | Không có revision token trong #78; stale policy open. | #79–#81 conflict/reload behavior cần owner quyết định. |

### Điều hướng và dữ liệu handoff

| Từ | Hành động | Đến | Dữ liệu | Trạng thái |
|---|---|---|---|---|
| Admin workspace | Mở kiểm duyệt | AD-10 `/admin/content/pending` | Bearer/session; Angular Admin route and navigation link are source-present. | Browser/deployment runtime `NOT VERIFIED`; permission mapping remains open. |
| AD-10 | Chọn Content | AD-11 `/admin/content/:contentId/review` | Candidate numeric `Content.id` → `content_id`; revision/version không có. | AC-33 expected; local Page-vs-catalog mismatch và stale policy open. |
| AD-11 | Hoàn tất #80/#81, reload queue | AD-10 | Candidate reload list/filter/page; preservation chưa quy định. | AC-33 reload expected; exact route/cache/ordering chưa approved. |

Back/browser history, query persistence, focus restoration, session-expiry route, authorization redirect và cache invalidation chưa được xác định bởi Study Web source. Không tự thêm behavior.

## 4. Luồng đọc (Read)
- Orchestration từ inventory: GET #78 → chọn content_id mở AD-11.
- Chi tiết current/source mapping: xem [API Integration](04-api-integration.md) và DD nguồn.

## 5. Luồng ghi (Write)
- Chỉ mô tả mutation được DD/API source nêu; không thêm endpoint hoặc side effect.
- Source trace: [AD-10](../../screen_stitch/05_admin/AD-10_hang-doi-kiem-duyet-noi-dung/AD-10.md)

## 6. Cache / concurrency / lifecycle
- Cache, race, cleanup, pagination: xem các section source bên dưới; nếu không có bằng chứng thì để `CẦN_XÁC_NHẬN`.

## 7. Data errors & security
- Theo error/security/source-status section của DD nguồn; không coi state trong mockup là runtime behavior.

## 8. Trace
[Events](02-events.md) · [API](04-api-integration.md) · [Rules](05-business-rules.md)


## Current Study Web source re-audit — 2026-11-20

- Admin route → AD10Page → AD10ApiService → `STUDY_SERVER_APIS.API_078` → AdminApiService GET. The page initializes `{page: 1}`, omits empty `type/course` values, submits exact raw filters, and uses response pagination to bound next/previous navigation.
- Manual refresh clones the applied query signal to trigger one GET #78 again; the shared `adminQueryState` switches to loading and cancels a stale request. No timer/polling or write side effect is present.
- The server's local contract is `ApiEnvelope<Page<Content>>`; the catalog still says singular `Content`. The client follows current local Page source but this is a contract discrepancy, not final API acceptance. Runtime/test boundaries remain as stated above.

## Current Study Web source re-audit — 2026-11-21

- The response mapper requires DESIGN_RESOURCE_RETRIEVED, the requested page echo, fixed size 20, a valid Content projection, and total_pages consistent with safe totals. Null parent_id may be omitted by the server serializer.
- With accepted page metadata, the page checks the expected row count for that page. A mismatch retains rows, shows a synchronization warning, hides total/page controls, and blocks page navigation until manual retry. Empty out-of-range responses retain a page-1 recovery action; matching zero-result responses remain empty.
