# PLAN_RESULT

## API result

| Thuộc tính | Giá trị |
|---|---|
| API ID | `14` |
| API name | `Cập nhật hồ sơ` |
| Endpoint | `PUT /api/v1/users/me/profile` |
| Status | `PARTIALLY COMPLETED` |
| Decision status | `NEEDS USER DECISION` |
| Output folder | `apps/study-server/docs/dd/14_users_me_profile/` |
| Basis | `DIRECT — approved design contract + AC-11; current source dùng để ghi discrepancy.` |
| Runtime status | `UNWIRED / NOT_FOUND — chưa có route/module/test API #14` |
| Tables read | `users` — safe profile reload theo AC-11/API #4 projection |
| Tables write | `users` — `full_name`, `phone`, `avatar_url`, `updated_at` |
| Business code delta | `N/A — dùng DESIGN_RESOURCE_UPDATED và DESIGN_* codes đã có trong design contract; không tạo code mới.` |

## Sources

- [`docs/lists/list_api.md`](../../../../../docs/lists/list_api.md).
- [`AC_02_STUDENT_LEARNING.drawio`](../../../docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio).
- [`00_AC_API_INDEX.md`](../../../docs/diagrams/AC_UNICA/00_AC_API_INDEX.md).
- [`DB.sql`](../../../../../infra/postgres/study-server/DB.sql).
- [`API #4 current-user query`](../../../app/modules/guest/api_04_users_me/query.py).
- [`API #4 current-user view`](../../../app/modules/guest/api_04_users_me/view.py).
- [`code_http.md`](../../business_code/code_http.md).
- [`createDD-markdown skill`](../../../../../.agents/skills/create_dd_api/docs/dd/createDD_MARKDOWN_SKILL.md).

## Locked decisions

- Giữ endpoint/method/API ID và success/error status đúng `list_api.md`.
- Giữ `bio` trong request/response contract nhưng đánh dấu `SOURCE_REQUIRED`.
- Không tự thêm `users.bio`, migration, shadow field hoặc JSON fallback.
- Giữ literal `avatar_url...:uri!` trong ghi chú và mở question về requiredness/nullable semantics.
- Chỉ map DB mutation cho `full_name`, `phone`, `avatar_url`, `updated_at`.
- Scope update bằng numeric `JWT.sub`; không nhận `user_id` từ client.

## Open gaps

- Persistence source và schema decision cho `bio`.
- Requiredness/nullable/blank semantics của `avatar_url`.
- Contract requiredness của `phone` so với current nullable column.
- PUT full-replacement semantics và quy tắc clear/null cho `bio`, `phone`, `avatar_url`.
- Cách trả đầy đủ `UserProfile` khi current profile projection không có `bio`.

## Verification result

- 8 baseline sheet files được author theo template và giữ thứ tự.
- Request/Query/Mutation/Response Source matrices được ghi trong Data Mapping.
- Static Markdown, JSON và relative-link checks được ghi trong `VERIFICATION_REPORT.md`.
- Không có runtime test API #14 vì endpoint chưa wired.
