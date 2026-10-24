# Kết quả plan — API #71

## Phạm vi

Tạo DD Markdown cho `PATCH /api/v1/admin/users/{user_id}/status` theo catalog và AC-31. Chỉ tạo tài liệu; không sửa source, schema, catalog hoặc diagram; không tạo ZIP. Khi tạo #71, macro-review AC-31 chờ DD #72; document-level review đã hoàn tất sau khi tạo #72.

## Plan đã thực hiện

| Bước | Kết quả |
|---|---|
| Phân loại task | docs; scope server-study; không có dependency cross-scope. |
| Worklog preflight | Selector chọn #48/#49/#50; đọc đủ ba worklog trước khi inspect sâu. |
| Context và skill | Đọc router/context-map, server-study scope, manifest registry và `createDD-markdown`; Study workflow yêu cầu Markdown. |
| Catalog/diagram | Đối chiếu API #71 row, UserProfile/UserStatus, toàn bộ AC-31 STATUS branch và edges tới reload list/detail. |
| Source/session trace | API #3 login/refresh status check, refresh-token revocation, current access JWT helper, API #4 UserProfile và legacy/pilot DDL đã đối chiếu. |
| Prior DD consistency | #68 list, #69 detail, #70 profile/role boundaries và open questions được đọc; #71 chỉ sở hữu account status. |
| Plan-before-authoring | Requirement/request/query/mutation/response-source matrices được ghi vào worklog trước khi tạo folder DD. |
| Authoring | Tạo 8 template sheets và 3 reports; body/status values/session revocation candidates gắn DERIVED. |
| Macro-review | Đã rà document-level nhóm #68–#72; status/session/delete boundaries còn policy gaps. |

## Quyết định tài liệu

- Giữ direct method/path/auth/path type/response/status/error set chính xác theo catalog.
- Body `{status:UserStatus!}` là DERIVED; `ACTIVE`/`SUSPENDED` chỉ là candidate lock/unlock, không phải enum contract.
- Candidate status update dựa trên legacy `users.status`; live schema chưa xác minh và V1-PILOT UUID model giữ riêng.
- Chỉ đề xuất revoke `refresh_tokens` khi khóa nếu owner xác nhận. Source login/refresh từ chối status khác ACTIVE; current access JWT helper không tra status/revocation nên access token đã phát hành có thể còn hiệu lực tới expiry.
- Không thêm audit, self-lock rule, last-admin protection, status 409, soft delete hoặc access-token blacklist.
- Admin guard, body/enum, live schema, immediate access revocation và no-op semantics còn mở.

## Trạng thái

Draft — Needs Confirmation. Chưa implementation-ready cho tới khi body/status policy, Admin authorization, live schema và session/access-token effects được chốt.
