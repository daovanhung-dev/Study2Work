# ST-03 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `ST-03-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Form chỉnh sửa fullname/phone/bio/avatar, theo dõi upload/save riêng.
- Current status: Study Web calls #04/#13/#14 for source-supported fields. Bio remains gated because API #04/#14 and checked-in DB do not provide persistence. The original Gate G-03 mockup remains a design/current-source discrepancy, not a runtime feature flag.
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

### Trích từ DD nguồn: F. Bảo mật, riêng tư và ràng buộc

1. Chỉ gửi Bearer token qua Authorization header theo API source; không đặt token hoặc PII trong URL.
2. Backend API #04/#13/#14 kiểm tra Student role từ JWT trước thao tác profile. Source dùng roles claim và sub; không kiểm tra DB role/status freshness.
3. #04 response là allowlist an toàn, không bao gồm password_hash. Không tự đưa permissions/bio vào UI.
4. #13 nhận ảnh base64 nên request có thể lớn; server cap 5 MiB sau decode, kiểm MIME/byte signature, upload dùng fixed per-user key. Client dùng FileReader Data URL, giới hạn MIME và kích thước trước upload; hủy upload và giới hạn bộ nhớ chưa có.
5. #14 cho phép nullable phone/avatar_url, nhưng đó không giải quyết product policy; server không kiểm tra URI/ownership. Client chỉ nhận URL HTTP(S) từ response #13; không suy ra URL tùy ý là trusted image source.
6. Không có transaction xuyên object storage và database. #13 có thể ghi/ghi đè object trước khi #14 fail; cleanup, rollback, replacement history và retry chưa được xác định.
7. Email readonly theo mockup; đây là design constraint, không phải backend policy được #14 chứng minh.
8. Footer “WCAG 2.1 AA Compliant” là nội dung ảnh; chưa có accessibility audit. Dù các control trong HTML dùng min-height 44px, không có evidence bàn phím/contrast/screen reader ở runtime.

### Trích từ DD nguồn: G. Discrepancies và blockers

| ID | Mâu thuẫn / thiếu quyết định | Nguồn | Cần chốt |
|---|---|---|---|
| G-03 / API #13 | Mockup nói multipart/CDN và “halted”; current route nhận Data URL JSON, ghi object storage và trả AvatarUploadResult. | list_screen.md, mockup/HTML, list_api.md, #13 route/module/DD and ST-03 caller | Client uses the current JSON Data URL contract. Public URL behavior, overwrite/cleanup and retry policy remain unverified or unresolved; do not claim upload and profile update are atomic. |
| G-03 / API #14 | Current model updates full_name/phone/avatar_url; phone/avatar are nullable; extra bio is ignored and avatar URI is not validated. | list_api.md, AC-11, #14 source, DDL | Bio remains unavailable until API/DB supports it. Product policy for phone formatting and trusted avatar references remains unresolved. |
| Refresh sequence | Inventory requires GET #04 after PUT; current client performs that read after #14. | list_screen.md, AC-11, #14 view/query, ST-03 page | Source now follows the inventory sequence; browser/runtime behavior is not verified. |
| Upload/update consistency | #13 external storage mutation is not in the #14 DB transaction; the provider uses a fixed per-user key. | #13 view/provider and #14 view | Upload may take effect before profile save and is not compensated if #14 fails. No retry, cleanup or rollback behavior is added. |
| UI runtime | Angular route and API caller exist; the original Stitch still depicts a static Gate G-03 and disabled controls. | Current Study Web source and screen_stitch assets | Source supports loading, validation, upload, save and read-retry states. The visual/design gate mismatch remains open; browser/runtime is unverified. |
| DDL/live schema | Checked-in DDL không có bio; phone/avatar nullable; live schema chưa kiểm. | infra/postgres/study-server/DB.sql, API source | Xác nhận migration/schema thực tế trước mở gate. |

**Trạng thái:** DD PARTIAL/BLOCKED for Bio and the original Gate G-03/design discrepancy. IMPLEMENTATION PARTIAL: #04/#13/#14 are called for supported fields; Bio is not sent or persisted. RUNTIME NOT VERIFIED because browser, live database and Object Storage were not exercised.

## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
