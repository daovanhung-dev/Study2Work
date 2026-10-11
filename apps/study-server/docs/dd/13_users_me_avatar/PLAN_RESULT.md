# PLAN_RESULT

## API result

| Thuộc tính | Giá trị |
|---|---|
| API ID | `13` |
| API name | `Upload avatar nếu có` |
| Endpoint | `POST /api/v1/users/me/avatar` |
| Status | `IMPLEMENTED AND LOCALLY VERIFIED` |
| Decision status | `USER-APPROVED IMPLEMENTATION PLAN` |
| Output folder | `docs/dd/13_users_me_avatar/` |
| Basis | `DIRECT — approved design contract + AC-11` |
| Runtime status | `VERIFIED — route and local tests present; external storage was not contacted` |
| Tables read | `N/A — không có DB read được source xác nhận` |
| Tables write | `N/A — upload-only; không có DB mutation` |
| External side effect | `S3-compatible upload to avatars/{user_id}; same-user upload overwrites the existing object` |
| Business code delta | `N/A — dùng DESIGN_* code đã có` |

## Sources

- [`docs/lists/list_api.md`](../../../../../docs/lists/list_api.md).
- [`AC_02_STUDENT_LEARNING.drawio`](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio).
- [`00_AC_API_INDEX.md`](../../diagrams/AC_UNICA/00_AC_API_INDEX.md).
- [`DB_UNICA_ERD.drawio`](../../diagrams/DB_UNICA_ERD.drawio).
- [`createDD_MARKDOWN_SKILL.md`](../../../../../.agents/skills/create_dd_api/docs/dd/createDD_MARKDOWN_SKILL.md).

## Locked decisions

- Giữ body field `image:string`; chỉ nhận JSON Data URL Base64 cho PNG/JPEG/WebP.
- Từ chối chữ ký không khớp, Base64 sai, field dư và payload giải mã trên 5 MiB.
- API #13 chỉ upload Object Storage; API #14 tiếp tục cập nhật `users.avatar_url`.
- Success response là `ApiEnvelope<AvatarUploadResult>`; `data` chỉ có `avatar_url`.
- Storage env: `OBJECT_STORAGE_BUCKET`, `OBJECT_STORAGE_REGION`, `OBJECT_STORAGE_ACCESS_KEY_ID`, `OBJECT_STORAGE_SECRET_ACCESS_KEY`, `OBJECT_STORAGE_PUBLIC_BASE_URL`; `OBJECT_STORAGE_ENDPOINT_URL` là tùy chọn.
- Object key `avatars/{user_id}`; connect timeout 5 giây, read timeout 30 giây, một attempt; không retry/cleanup riêng.

## Open gaps

- Không còn câu hỏi triển khai trong Q-13-01..04; các lựa chọn được ghi trong DD và source.
- Credentials, bucket policy, public access và storage connectivity chưa được kiểm tra từ xa theo scope đã chốt.

## Verification result

- API #13 đã được đối chiếu với `list_api.md` và AC-11.
- Route, parser, provider S3-compatible và dependency injection được triển khai.
- Chi tiết pytest, Ruff, mypy, route/import và context validation nằm trong [`VERIFICATION_REPORT.md`](./VERIFICATION_REPORT.md).
