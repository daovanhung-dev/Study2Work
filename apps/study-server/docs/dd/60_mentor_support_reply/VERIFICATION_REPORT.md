# VERIFICATION_REPORT — Study API #60

## Kết quả

- DD status: `Draft — Needs Confirmation`.
- Tài liệu: `VERIFIED_STATIC_ONLY`; support model/attachment resolver/authorization vẫn là blockers.
- Runtime API #60: `UNWIRED / NOT_FOUND`; không khẳng định runtime behavior.
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
| Skill/template registry | `createDD-markdown` được wire cho `server-study`; hash 8 template đối chiếu với registry source. | PASS |
| Template appendix | Appendix của cả 8 sheet trùng template tương ứng byte-for-byte. | PASS |
| Front matter | Tám sheet có dd_id 60 và `Draft — Needs Confirmation`. | PASS |
| API contract | POST path, Mentor Bearer, int64 path, body fields, 200 updated, SupportRequest và exact 401/403/404/422/500 khớp catalog. | PASS |
| Mutation/flow | #60 INSERT SupportMessage; resolve riêng qua #61; nhánh NO giữ OPEN theo AC-24. | PASS |
| Response coverage | Đủ 24 field SupportRequest/UserSummary/SupportMessage/UploadAsset. | PASS |
| JSON examples | Success/error examples parse JSON; attachment/status placeholders và proposal được ghi rõ. | PASS |
| Markdown | 42 relative links/anchors tồn tại; table widths, code fences, whitespace và `git diff --check` đạt. | PASS |
| Scope/runtime | Không đổi executable source; tests không chạy vì docs-only và endpoint chưa wired. | NOT_RUN |
| AC-24 macro-review | Đã review cùng #58/#59/#61: #60 chỉ INSERT reply; #61 sở hữu resolve; attachment/lifecycle gaps giữ mở. | VERIFIED_WITH_OPEN_QUESTIONS |

## Open implementation blockers

- Support table/ID model và Mentor principal/assignment predicate.
- API #34 UploadAsset registry, ID mapping, ownership/purpose/status validation và URL resolver.
- Wire key/encoding cho #35/#47/#60; pilot UUID attachment IDs không khớp contract int64.
- Blank/length validation, Mentor author type, learner visibility, reply sau resolve.
- Thread order/limit, transaction boundary và conditional error middleware wiring.

## Kết quả macro-review AC-24 #58–#61

`VERIFIED_WITH_OPEN_QUESTIONS`. Ranh giới mutation đúng diagram: #60 chỉ INSERT SupportMessage, còn #61 đổi status ở nhánh YES; nhánh NO giữ OPEN. Attachment reference chưa thống nhất với #34/#35/#47, và policy reply sau resolve/cancel, model/IDs, Mentor scope तथा response projection vẫn cần xác nhận. Xem [macro-review tổng hợp](../61_mentor_support_resolve/PLAN_RESULT.md#macro-review-ac-24-58-61).

Xem [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md) và [PLAN_RESULT.md](./PLAN_RESULT.md).
