# VERIFICATION_REPORT — Study API #61

## Kết quả

- DD status: `Draft — Needs Confirmation`.
- Tài liệu: `VERIFIED_STATIC_ONLY`; nhóm AC-24 #58–#61 `VERIFIED_WITH_OPEN_QUESTIONS`.
- Runtime API #61: `UNWIRED / NOT_FOUND`; không khẳng định runtime behavior.
- Scope: Markdown DD, worklog và macro-review reports; không sửa source, tests, schema, catalog, diagram hoặc context pages.

## Deliverable manifest

| Nhóm | Kết quả |
|---|---|
| Sheets | Đủ 8 file đăng ký: `00_Cover.md` đến `07_table.md`. |
| Reports | `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md`. |
| Tổng | 11 Markdown files; không tạo ZIP theo Study workflow. |

## Kiểm tra

| Check | Kết quả | Trạng thái |
|---|---|---|
| Skill/template registry | `createDD-markdown` được wire cho `server-study`; 8 template Markdown và hash registry đã đối chiếu. | PASS |
| Template appendix | Appendix của 8 sheet trùng template tương ứng byte-for-byte. | PASS |
| Front matter | Tám sheets có `dd_id: "61"` và `Draft — Needs Confirmation`. | PASS |
| API contract | PATCH path, Mentor Bearer, int64 path, no body/query, 200 updated, SupportRequest và exact 401/403/404/422/500 khớp catalog. | PASS |
| AC-24 boundary | #60 INSERT SupportMessage; YES gọi #61 để resolve; NO giữ OPEN; #61 không sửa messages. | PASS |
| Response coverage | Ma trận ghi đủ SupportRequest, UserSummary, SupportMessage và UploadAsset fields; unresolved physical projection được đánh dấu SOURCE_REQUIRED. | PASS |
| JSON/examples | JSON examples parse; error set và response fields đối chiếu catalog. | PASS |
| Markdown | Local links/anchors, table widths, code fences và whitespace đạt. | PASS |
| AC-24 macro-review | #58–#61 review đủ flow, mutation ownership, catalog discrepancy và shared blockers. | VERIFIED_WITH_OPEN_QUESTIONS |
| Runtime tests | Không chạy; docs-only và endpoint chưa wired. | NOT_RUN |
| Agent context validator | Không chạy; context pages không thay đổi. | NOT_APPLICABLE |

## Blockers còn mở

- #58 plural/list flow nhưng catalog giữ singleton `ApiEnvelope<SupportRequest>`.
- Support persistence, UUID/int64 mapping và course relation chưa được phê duyệt.
- Mentor principal, assignment scope và 403/404 privacy order chưa rõ.
- SupportStatus, transition rules, message visibility/order/bounds và attachment resolver chưa rõ.
- Response projection cho student/messages/assets chưa có source mapping tương thích.
- Support error routes chưa wired; helper `data={}` khác guideline `data:null`.

Xem [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md), [PLAN_RESULT.md](./PLAN_RESULT.md#macro-review-ac-24-58-61) và các report #58–#60.
