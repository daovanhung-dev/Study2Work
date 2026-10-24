# VERIFICATION_REPORT — Study API #59

## Kết quả

- DD status: `Draft — Needs Confirmation`.
- Tài liệu: `VERIFIED_STATIC_ONLY`; physical mapping và access policy vẫn là open questions.
- Runtime API #59: `UNWIRED / NOT_FOUND`; không khẳng định runtime behavior.
- Scope: Markdown DD và worklog; không sửa source, test, schema, catalog, diagram hoặc context pages.

## Deliverable manifest

| Nhóm | File |
|---|---|
| Sheets | `00_Cover.md`, `01_Lich_su.md`, `02_Overview.md`, `03_Request.md`, `04_Response.md`, `05_Data_Mapping.md`, `06_Error.md`, `07_table.md` |
| Reports | `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md` |
| Tổng | 11 Markdown files; không tạo ZIP theo Study workflow. |

## Kiểm tra

| Check | Kết quả | Trạng thái |
|---|---|---|
| Skill/template registry | `createDD-markdown` được wire cho `server-study`; 8 template Markdown và SHA-256 đã đối chiếu. | PASS |
| Template appendix | Appendix cả 8 sheet trùng template tương ứng byte-for-byte. | PASS |
| Front matter | Tám sheet có `dd_id: "59"` và `Draft — Needs Confirmation`. | PASS |
| API contract | GET path, Mentor Bearer, required int64 path, no body/query, singleton response, 200 success và đúng 4 error codes khớp catalog. | PASS |
| Response coverage | Đủ 24 field SupportRequest/UserSummary/SupportMessage/UploadAsset trong response matrix. | PASS |
| JSON examples | Success/error code fences parse JSON hợp lệ; enum placeholders được ghi rõ. | PASS |
| Markdown | 34 relative links/anchors tồn tại; table widths, code fences và whitespace đạt; `git diff --check` không báo lỗi. | PASS |
| Scope/runtime | Không thay source/runtime; tests không chạy vì docs-only và API #59 chưa wired. | NOT_RUN |
| AC-24 macro-review | Đã review cùng #58/#60/#61: GET thread nằm đúng giữa list và reply; projection/access blockers giữ mở. | VERIFIED_WITH_OPEN_QUESTIONS |

## Open implementation blockers

- Approved support schema and int64/UUID contract.
- Mentor principal/assignment scope and 403-vs-404 privacy order.
- Course association, author identity projection and attachment URL/status resolver.
- Message visibility, ordering, count bounds, empty behavior and optional-field serialization.
- Malformed path error contract and future middleware allowlist integration.

## Kết quả macro-review AC-24 #58–#61

`VERIFIED_WITH_OPEN_QUESTIONS`. #59 là bước read-only lấy một request/thread trước #60 reply và #61 resolve; response shape không đổi. Physical ID/model, Mentor principal/scope, message ordering/visibility/bounds và author/attachment projection chưa có nguồn được duyệt. Xem [macro-review tổng hợp](../61_mentor_support_resolve/PLAN_RESULT.md#macro-review-ac-24-58-61).

Xem [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md) và [PLAN_RESULT.md](./PLAN_RESULT.md).
