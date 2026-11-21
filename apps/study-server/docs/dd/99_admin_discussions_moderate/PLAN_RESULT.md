# PLAN_RESULT — Study API #99

**Status:** Draft — Needs Confirmation
**Endpoint:** `PATCH /api/v1/admin/discussions/{discussion_id}/moderate`

| Thuộc tính | Giá trị |
|---|---|
| Output folder | `apps/study-server/docs/dd/99_admin_discussions_moderate/` |
| Basis | Catalog #99 and AC-37; direct contract, logical audit/state update |
| Table read | Candidate legacy `discussions` target/projection source |
| Table read | Candidate `users` author projection source |
| Table read | Candidate child `discussions` comment source |
| Table read gap | Report relation/key unresolved; no report query added to #99 |
| Logical write | Moderation state update; physical target unresolved |
| Logical write | Moderation audit append; physical target unresolved |
| Assumption | `hide`, `lock`, and `warn` request tokens are `DERIVED` examples only |
| Assumption | One-item Page metadata is a `DERIVED` proposal only |
| Conflict | Legacy Discussion lacks title/audit relation; pilot audit schema uses incompatible UUID identifiers |
| Verification | Static Markdown/contract checks passed; no application tests run |

## Sources

- [Catalog #99](../../../../../docs/lists/list_api.md).
- [AC-37 index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) and [activity diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio).
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) and [V1-PILOT audit DDL](../../../../../infra/postgres/02_study_db.sql).
- [Current router](../../../app/api/v1.py), [auth helper](../../../app/utils/auth.py), and [middleware](../../../app/core/middleware.py).
- Prior DDs [#97](../97_admin_discussions_reported/00_Cover.md), [#98](../98_admin_discussions_detail/00_Cover.md), and [#42](../42_discussions_detail/00_Cover.md).

## Kết quả theo plan

| Plan item | Result | Evidence/status |
|---|---|---|
| Giữ catalog method/path/auth/input/response/status/errors | Hoàn thành | #99 catalog row được giữ nguyên; không đổi response sang `ActionResult` |
| Review AC-37 moderation sequence | Hoàn thành | Diagram xác nhận #99 cập nhật moderation state + audit; quyết định delete chuyển sang API #100 |
| Phân biệt action reason với report filter | Hoàn thành | Body `reason` #99 là lý do action; query `reason` #97 là report filter |
| Xác định action/state values | Chưa thể chốt | Diagram nêu ý nghĩa ẩn/khóa/cảnh báo; token, enum, casing và transition `SOURCE_REQUIRED` |
| Xác định persistence state + audit | Chưa thể chốt | Legacy Discussion status là candidate; không có legacy audit relation; pilot audit UUID schema không map được bằng evidence hiện có |
| Giữ response schema | Hoàn thành | Dùng `ApiEnvelope<Page<Discussion>>`; one-item Page được đánh dấu `DERIVED` |
| Tạo output Markdown | Hoàn thành | 8 sheets và 3 reports; không tạo ZIP hoặc sửa runtime/schema |
| Cross-review AC-37 #97–#100 | Hoàn thành sau khi tạo #100 | Thứ tự flow nhất quán; state/audit, projection/report và deleted visibility vẫn là open questions |

## Kết luận

DD #99 ghi đầy đủ contract trực tiếp, luồng AC-37, candidate legacy Discussion và gap về action/state, audit, Admin auth, response projection. Macro-review #97–#100 hoàn tất về tính nhất quán luồng; các quyết định nguồn còn mở nên DD vẫn là `Draft — Needs Confirmation` và chưa implementation-ready.
