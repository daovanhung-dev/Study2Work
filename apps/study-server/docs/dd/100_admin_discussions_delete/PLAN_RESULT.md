# PLAN_RESULT — Study API #100

**Status:** Draft — Needs Confirmation
**Endpoint:** `DELETE /api/v1/admin/discussions/{discussion_id}`

| Thuộc tính | Giá trị |
|---|---|
| Output folder | `apps/study-server/docs/dd/100_admin_discussions_delete/` |
| Basis | Catalog #100, reusable `DeleteResult`, AC-37 |
| Logical operation | Soft delete + preserve audit trail |
| Candidate table | Legacy `discussions`; không khẳng định live schema |
| Candidate update | `status` + `updated_at`; token và timestamp mapping là DERIVED |
| Audit write | Physical relation/key/append policy chưa xác định |
| Runtime | `UNWIRED / NOT_FOUND`; không có route/module/test #100 |
| Verification | Static DD checks; không chạy application tests |

## Kết quả theo plan

| Plan item | Result | Evidence/status |
|---|---|---|
| Giữ contract method/path/actor/input/response/errors | Hoàn thành | Catalog #100 giữ nguyên; exact 5 error codes được liệt kê |
| Đọc luồng AC-37 | Hoàn thành | #97 queue → #98 detail → #99 state + audit → optional #100 soft delete → reload queue |
| Đối chiếu schema và runtime | Hoàn thành | Legacy DDL có `status`/`updated_at` nhưng không có `deleted_at`/audit relation; route/module/test không có |
| Ghi đề xuất logic ngoài sơ đồ | Hoàn thành có giới hạn | `status='DELETED'` và `updated_at` timestamp chỉ là DERIVED proposal; không được coi là approved |
| Tạo output Markdown | Hoàn thành | 8 sheets + 3 reports; không ZIP/runtime/schema/catalog/diagram edits |
| Validate DD | Hoàn thành | See [VERIFICATION_REPORT.md](./VERIFICATION_REPORT.md); static only |
| Macro-review #97–#100 | Hoàn thành | Chi tiết bên dưới; unresolved source gaps được giữ lại |

## AC-37 macro-review #97–#100

| API | Vai trò trong flow | Kết quả rà soát |
|---|---|---|
| #97 | Queue reported discussions | Contract `Page<Discussion>` không mang report fields; physical report relation, queue grain/filter/pagination và deleted-item predicate còn mở. |
| #98 | Discussion/thread/report detail | Read-only step đúng vị trí sau queue; report relation, root/reply scope, `Page<Discussion>` semantics và Discussion projection còn mở. |
| #99 | Moderate | Tách đúng khỏi delete; `reason` là action reason khác query filter `reason` #97; action/state/audit persistence và Page response còn mở. |
| #100 | Soft delete | Nối đúng nhánh sau quyết định delete; không hard-delete/cascade; deleted timestamp/audit write/child visibility/already-deleted behavior còn mở. |

### Nhất quán nhóm

- Sequence của bốn API thống nhất với diagram AC-37; #99 không gộp thao tác #100.
- Catalog actor là Admin cho cả nhóm, nhưng current Study auth helper chưa có Admin guard/claim policy. Cả bốn API vẫn `UNWIRED / NOT_FOUND`.
- #97 `reason` query là report filter; #99 `reason` body là moderation explanation; #100 không nhận reason.
- #97/#98 đọc report theo diagram nhưng catalog `Discussion` không có report fields và legacy DDL không có report relation. Đây là contract/data discrepancy, chưa reconcile.
- #99 yêu cầu logical state update + audit; #100 yêu cầu giữ audit trail. Legacy Discussion schema không có audit relation; pilot audit tables dùng UUID, không map trực tiếp Discussion BIGINT. Audit semantics và storage vẫn open.
- Soft delete phải ảnh hưởng hàng đợi/detail visibility, nhưng diagram không xác định predicate hoặc cách giữ report history; không tự sửa #97/#98 behavior.
- `Discussion.title` thiếu trong legacy DDL; `course_id`/`user_id` nullable trong DDL nhưng required trong reusable response. Đây là projection gap xuyên suốt #97–#99.
- #99/#100 response payload lần lượt là `Page<Discussion>` và `DeleteResult`; giữ nguyên catalog dù persistence/projection chưa đủ để implement.

### Macro-review disposition

Không phát hiện thứ tự API hoặc phân biệt request field sai giữa bốn DD. Các vấn đề trên là source/contract gaps cần owner xác nhận; không thay catalog, diagram, schema hoặc runtime trong task docs-only này. Các `OPEN_QUESTIONS.md` của từng API giữ các quyết định chưa được duyệt.
