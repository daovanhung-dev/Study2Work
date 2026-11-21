# VERIFICATION_REPORT — Study API #103

**Trạng thái:** Draft đã kiểm tra tĩnh; còn quyết định contract mở
**Phạm vi:** DD Markdown, worklog, inventory và macro-review AC-38; không sửa runtime/schema/catalog/diagram/client. Không chạy application tests.

## Nguồn và fingerprint

- Đã đọc: catalog row #103 và Operation tracking paragraph; Report/Operation/ExportAsset schema; index và toàn bộ diagram AC-38; Study DB ERD/table guide cùng legacy/V1-PILOT DDL; DD #18/#93/#101/#102; router/auth/storage source và test search; ba worklog docs được selector chọn; registry/skill createDD-markdown và workflow Markdown-only của Study.
- Fingerprint template (SHA-256 trên basename có thứ tự + NUL + byte file + NUL của 8 sheet): `3dc7fd2242dd1ed1bd9faba50aadad913a31b97ebf1392d6144bb905c5208137`.
- Fingerprint output (cùng cách tính trên 8 sheet, PLAN_RESULT.md và OPEN_QUESTIONS.md; bỏ report này): `444ddc2e767d91ef2301e805121256d8f5e404c38fb77a37e0c57c6248152295`.
- Appendix của cả 8 sheet khớp chính xác template đã đăng ký.

| Kiểm tra | Kết quả | Trạng thái |
|---|---|---|
| Context/preflight | Đọc router/context/scope/registry; selector docs chọn #100/#101/#102 và cả ba worklog được đọc; plan lưu trước khi tạo folder. | VERIFIED |
| Catalog contract | Method/path, Bearer Admin, query, no body/path, HTTP 202, `DESIGN_OPERATION_ACCEPTED` và bốn error code được giữ nguyên; Report/Operation conflict được ghi rõ. | VERIFIED_STATIC_ONLY |
| AC-38 | Nhánh export/view-only, CSV/XLSX/PDF, job, temporary storage có điều kiện, UI download và API #18 poll được đối chiếu. | VERIFIED_STATIC_ONLY |
| Manifest/front matter | Đúng 11 Markdown file: 8 sheet và 3 report; 8 sheet có front matter. | PASS |
| Template suffix | Phụ lục 8/8 sheet giống registered template. | PASS — 8/8 |
| Request/response/mapping | Field/query, hai response payload, mapping candidate và SOURCE_REQUIRED gaps được thể hiện; không thêm physical table/column. | VERIFIED_STATIC_ONLY |
| JSON examples | 3 khối JSON parse thành công. | PASS — 3 |
| Markdown structure | Bảng đúng số cột, code fence cân bằng, link/anchor nội bộ hợp lệ, không trailing whitespace và mọi file có final newline. | PASS |
| Error set | Bốn mã #103 khớp catalog: 401, 403, 503, 500; không thêm mapping chưa duyệt cho invalid filter/format hoặc post-accept failure. | VERIFIED_STATIC_ONLY |
| AC-38 macro-review | #101 → #102 → optional #103 flow đã review; date type mismatch, response conflict và API #18 gaps còn mở; cập nhật #101/#102 reports/open questions/worklogs. | VERIFIED_STATIC_ONLY |
| Inventory after #103 | Catalog 103; 103 folders/8 core sheets; 91 full 11-file packs; #01–#12 core-only; 12 source route+view APIs, 91 without pair. | VERIFIED_STATIC_ONLY |
| `git diff --check` | Không có diagnostics; DD mới đã qua dedicated whitespace/fence/table/link scan. | PASS |
| Runtime/application tests | Không chạy; docs-only. #103 remains `UNWIRED / NOT_FOUND`. | NOT_RUN |

## Defect phát sinh

Không khẳng định runtime behavior. Payload lựa chọn, Operation ID/result, filters/format, quyền, storage/expiry, retry và worker error lifecycle tiếp tục nằm trong [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md). #103 vẫn ở trạng thái Draft — Needs Confirmation cho tới khi contract owner quyết định.
