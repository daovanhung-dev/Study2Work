# ST-03 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `ST-03-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Form chỉnh sửa fullname/phone/bio/avatar, theo dõi upload/save riêng.
- Gate/status (giữ nguyên): **M**; **BLOCK:** API #13/#14 chưa wired; avatar, bio, phone contract xung đột
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

### Trích từ DD nguồn: F. Bảo mật, riêng tư và ràng buộc

1. Chỉ gửi Bearer token qua Authorization header theo API source; không đặt token hoặc PII trong URL.
2. Backend API #04/#13/#14 kiểm tra Student role từ JWT trước thao tác profile. Source dùng roles claim và sub; không kiểm tra DB role/status freshness.
3. #04 response là allowlist an toàn, không bao gồm password_hash. Không tự đưa permissions/bio vào UI.
4. #13 nhận ảnh base64 nên request có thể lớn; server cap 5 MiB sau decode, kiểm MIME/byte signature, upload dùng fixed per-user key. Client encoding/memory/preview policy chưa có.
5. #14 cho phép nullable phone/avatar_url, nhưng đó không giải quyết product policy; avatar URL không được kiểm tra URI/ownership. Không coi arbitrary URL là trusted image source.
6. Không có transaction xuyên object storage và database. #13 có thể ghi/ghi đè object trước khi #14 fail; cleanup, rollback, replacement history và retry chưa được xác định.
7. Email readonly theo mockup; đây là design constraint, không phải backend policy được #14 chứng minh.
8. Footer “WCAG 2.1 AA Compliant” là nội dung ảnh; chưa có accessibility audit. Dù các control trong HTML dùng min-height 44px, không có evidence bàn phím/contrast/screen reader ở runtime.

### Trích từ DD nguồn: G. Discrepancies và blockers

| ID | Mâu thuẫn / thiếu quyết định | Nguồn | Cần chốt |
|---|---|---|---|
| G-03 / API #13 | Mockup nói multipart/CDN và “halted”; current route nhận Data URL JSON, ghi S3-compatible object và trả AvatarUploadResult. | list_screen.md, mockup/HTML, list_api.md, #13 route/module/DD | Owner xác nhận client encoding, asset URL/public access, replace/overwrite và error/retry policy; cập nhật diagnostic design. |
| G-03 / API #14 | Catalog/AC đòi bio, non-null phone và avatar URI; current model chỉ có full_name/phone/avatar_url, phone/avatar nullable, extra bio bị bỏ qua, URI không validate. | list_api.md, AC-11 index/diagram, #14 source, DDL | Chốt bio persistence, phone nullable/format policy, avatar URL trust/reference/validation và required fields; cập nhật API/DB contract. |
| Refresh sequence | Inventory yêu cầu GET #04 sau PUT; #14 đã trả UserProfile từ UPDATE RETURNING. | list_screen.md, AC-11, #14 view/query | Quyết định dùng PUT response hay gọi lại #04, cache invalidation và ST-02 sync. |
| Upload/update consistency | #13 external storage mutation không cùng transaction với #14 DB update. Fixed key ghi đè. | #13 view/provider và #14 view | Chốt compensation, retry/idempotency, orphan/old-object handling và UX khi chỉ một bước thành công. |
| UI runtime | Study Web package/router/API client không có; controls disabled và links fragment-only. | Checkout hiện tại / code.html | Cần frontend app wiring, approved loaded/error states, session handoff và destinations. |
| DDL/live schema | Checked-in DDL không có bio; phone/avatar nullable; live schema chưa kiểm. | infra/postgres/study-server/DB.sql, API source | Xác nhận migration/schema thực tế trước mở gate. |

**Trạng thái:** DD BLOCKED vì contract bio/phone/avatar và save/reload sequence chưa thống nhất, nên tài liệu chưa thể hướng dẫn implementation không cần suy đoán. IMPLEMENTATION BLOCKED vì Study Web chưa có app runtime và thiết kế đang khóa các thao tác chính. RUNTIME NOT VERIFIED vì không chạy UI/API end-to-end, không truy cập live database hoặc Object Storage.

## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
