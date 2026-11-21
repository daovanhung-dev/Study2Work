# ST-12 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `ST-12-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Tài nguyên theo lesson, xem/tải an toàn và quay lại vị trí học.
- Current status — 2026-11-20: **DD BLOCKED; IMPLEMENTATION PARTIAL; RUNTIME NOT VERIFIED.** #26 and the ST-12 caller exist; #26 checks Student/ACTIVE enrollment and published lesson/course, and returns a resources list without URL. GS-07 owns #12. #47 writes `lesson_uploads` while #26 reads `resources`; no writer for the latter was found. This source gap prevents claiming end-to-end resource data availability.
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

### Trích từ DD nguồn: F. Quy tắc nghiệp vụ, bảo mật và tiếp cận

1. Không xem `href`, `data-path`, badge `Valid Spec`, tên người học hay security copy trong mockup là bằng chứng route/session/policy.
2. Catalog #26 yêu cầu Student Bearer nhưng không có source thực thi entitlement. Mỗi endpoint phải có access rule riêng sau khi được chốt; không coi một lần kiểm tra phía client là authorization.
3. API #12 uses T041 access policy: PUBLIC direct HTTP(S); PRIVATE requires Student auth, published parent and ACTIVE enrollment, then a 300-second signed URL.
4. Use backend-provided `visibility`; do not infer it from the course or URL. Live schema mapping remains unverified.
5. Không hiển thị tên file, extension, dung lượng, URL, download action hay preview khi backend chưa cung cấp payload được duyệt.
6. Study Web design target yêu cầu ocean-primary `#0B5F8A`, focus-visible, keyboard order, contrast WCAG AA, semantic link/button, text alternative phù hợp, responsive reflow 320px và target điều khiển ≥44px. Ảnh 1600×1504 chỉ là desktop design; WCAG claim trong ảnh chưa được kiểm chứng.
7. HTML lấy font/Tailwind từ CDN. Tailwind config dùng `#004AC6`/`#2563EB` cho primary, trong khi design guide dùng `#0B5F8A`; cần đồng nhất khi có frontend source, không thay đổi asset nguồn trong task này.

### Trích từ DD nguồn: G. Discrepancy và blocker

| ID | Discrepancy/blocker | Bằng chứng | Ảnh hưởng |
|---|---|---|---|
| ST12-B01 | Study Web route/runtime không có trong checkout. | `.agents/web-work/study/INDEX.md`; không có `apps/study-client/src`, package hoặc router. | Không thể xác minh auth, request, route, UI state hoặc runtime. |
| ST12-B02 | API #26 khai báo `ApiEnvelope<Lesson>` nhưng use case cần Resource collection. | `docs/lists/list_api.md`, AC-15 diagram, API #26 DD Q-26-01. | Không thể map item, empty state hoặc `resource_id`. |
| ST12-B03 | API #26 không có route/module/query/test source. | Search `apps/study-server/app` và `tests`; `.agents/server-study/apis/declared-routes.md`. | API catalog là declaration, không phải runnable endpoint. |
| ST12-B04 | #26 list semantics/access còn mở. | API #26 Q-26-02..07: cardinality/order/empty, Student entitlement, visibility, URL/signer, 404/error, path/schema. | Chặn screen data flow và error-state decisions. |
| ST12-B05 | API #12 source public/direct URL khác signed/private expectation. | Route/view/query/model/test #12; current source không auth/visibility/signer; trả `resources.url`. | Chặn safe expose/open/download từ ST-12 hoặc GS-07. |
| ST12-B06 | Mockup trạng thái #12 “Pending Auth” không khớp source/catalog public/no Bearer. | Catalog/API #12 route. | Cần sửa copy hoặc chốt contract; không được mô tả như current auth. |
| ST12-B07 | Mockup security/refresh/compliance claims chưa được chứng minh. | HTML tĩnh, không timer/guard/test evidence; #12 trả URL/metadata. | Claims không được ghi thành behavior đã triển khai. |
| ST12-B08 | Không có danh sách resource hoặc trigger chọn item, mặc dù inventory định tuyến #26 → #12. | `screen.png`/`code.html`. | Không có `resource_id` hợp lệ để gọi #12; cần loaded-state design/contract. |
| ST12-B09 | Back, discussion, header/footer destinations chưa wire/context. | HTML `href="#"`, `data-path`; ST-11/GS-07 DD. | Không xác định lesson position, course discussion hay return destination. |
| ST12-B10 | Candidate schema/contract khác nhau; live schema chưa xác minh. | Resource contract có `visibility`; legacy `DB.sql` không có field đó và `lesson_id` nullable; V1-PILOT UUID model không có `resources` table declaration. | Không suy đoán visibility, mandatory parent, schema mapping hoặc production DB behavior. |
| ST12-B11 | API #12 DD cover nói chưa có runtime/OpenAPI verification, không phản ánh route/test source hiện tại. | Current `app/api/v1.py`, API #12 module và focused test source có route/response/OpenAPI-path assertion; API DD vẫn Draft; test chưa chạy. | Giữ `SOURCE_BACKED LOCALLY` khác với DD approval/test/runtime verification; không dùng stale cover làm trạng thái source. |

**Phân loại cuối:** `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`. Tài liệu này ghi trace hiện có và quyết định còn thiếu; không tuyên bố đạt DD READY.

## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
