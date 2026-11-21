# VERIFICATION_REPORT — Study API #01

**Trạng thái:** Package DD được kiểm tra tĩnh; contract còn câu hỏi mở
**Phạm vi:** API #01 Markdown và worklog/inventory; không sửa runtime, tests, schema, catalog, diagram hoặc client. Không chạy application tests.

## Nguồn và fingerprint

- Đối chiếu catalog API #01/UserProfile và business codes; index + diagram AC-01; DB ERD/table guide; legacy Study DDL; V1-PILOT schema; current router/module/validation/query/response/middleware/password source; test source #01; DD #01; DD #02 và current verify-email route/view/provider.
- Skill `createDD-markdown` có registry wiring; Study workflow yêu cầu Markdown folder + reports, không yêu cầu ZIP.
- Fingerprint template (SHA-256 trên basename có thứ tự + NUL + byte file + NUL cho 8 sheet): `3dc7fd2242dd1ed1bd9faba50aadad913a31b97ebf1392d6144bb905c5208137`.
- Fingerprint output (cùng phép tính trên 8 sheet output, `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`; bỏ report này): `6a7839acb858aa0a4ed36bd2a7724e699e7575f01d180d917fdf43bebad9d7d4`.

## Kiểm tra package

| Kiểm tra | Kết quả | Trạng thái |
|---|---|---|
| Manifest/front matter | Đúng 11 file Markdown: 8 sheet và 3 report; 8 sheet có front matter. | PASS |
| Appendix template | Tám appendix output khớp chính xác registered template (sheet 07 dùng template `07_table.md`). | PASS — 8/8 |
| Catalog contract | Public POST, 3 body fields, `ApiEnvelope<UserProfile>`, HTTP 201 và errors 422/409/500 được giữ đúng. | VERIFIED_STATIC_ONLY |
| JSON examples | Ba ví dụ request/success/error parse hợp lệ. | PASS — 3 |
| Markdown tables | 426 table rows nhất quán số cột. | PASS |
| Links/anchors | 36 local links resolve; không còn link file hoặc anchor nội bộ hỏng. | PASS |
| Fences/whitespace | Code fences cân bằng; không trailing whitespace; mọi file có final newline. | PASS |
| Existing DD repair | Hai source links trong `02_Overview.md` sửa; leading whitespace ở `05_Data_Mapping.md` bỏ; bốn appendix tails đồng bộ với template. | PASS |
| AC-01 macro-review | #01→#02 flow được đối chiếu: #01 không gọi #02; #02 gọi provider đồng bộ, exception trả 500, default stub không gửi email và không có retry worker. | VERIFIED_STATIC_ONLY |
| Inventory sau #01 | 103 catalog IDs/folders/core DDs; 92 full 11-file packages; #02–#12 còn core-only; không thiếu folder. Route+matching-view source: 12 IDs, 91 IDs chưa có cặp. | VERIFIED_STATIC_ONLY |
| `git diff --check` | Không có diagnostics; Markdown mới cũng đã qua custom whitespace/table/link/fence checks. | PASS |
| API #01 tests | Test source được đọc; không chạy tests trong task docs-only này. | NOT_RUN |

## Expected behavior và current-source boundary

AC-01 kỳ vọng sau khi tạo account sẽ dispatch API #02 để gửi verification; provider failure sau acceptance được log/retry. Current #01 chỉ ghi log `verification_dispatch_pending` sau commit. API #02 current view gọi provider đồng bộ; exception thành HTTP 500; provider mặc định chỉ trả accepted và không gửi email. Đây là `DISCREPANCY`, không phải thay đổi contract.

Current #01 source kiểm tra email trùng, hash Argon2id, INSERT/commit `users`, trả profile an toàn và rollback/ánh xạ lỗi theo code. ERD/API model còn chênh về profile mặc định và `UserProfile.bio`; live DB chưa được xác nhận. Chi tiết câu hỏi nằm trong [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md); DD giữ `Draft — Needs Confirmation`.
