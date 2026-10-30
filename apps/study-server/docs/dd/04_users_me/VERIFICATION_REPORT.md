# VERIFICATION_REPORT — Study API #04

**Endpoint:** `GET /api/v1/users/me`

**DD status:** `Draft — Needs Confirmation`

**Source status:** route, view, query, model và focused test source hiện diện; task DD không chạy tests hoặc runtime.

## Phạm vi và nguồn đã kiểm tra

- [Catalog API #04 và reusable schemas](../../../../../docs/lists/list_api.md).
- [AC-02 diagram](../../diagrams/AC_UNICA/AC_01_GUEST_ACCOUNT.drawio), [AC-11 diagram](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio), và [AC/API index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md).
- Current [router](../../../app/api/v1.py), [API #04 view](../../../app/modules/guest/api_04_users_me/view.py), [query](../../../app/modules/guest/api_04_users_me/query.py), [model](../../../app/modules/guest/api_04_users_me/models.py), [auth](../../../app/utils/auth.py), [trace](../../../app/core/trace.py), và [response helpers](../../../app/core/responses.py).
- [API #04 focused test source](../../../tests/modules/guest/api_04_users_me/test_users_me.py) được đọc, không chạy.
- API #03 connected [DD](../03_auth_login/PLAN_RESULT.md) và current login source được đối chiếu.
- API #13 [DD](../13_users_me_avatar/PLAN_RESULT.md) cùng current upload view được đối chiếu.
- API #14 [plan](../14_users_me_profile/PLAN_RESULT.md), [verification report](../14_users_me_profile/VERIFICATION_REPORT.md), route/module/query/model và test-file presence được đối chiếu; test không chạy.
- [`DB.sql` candidate](../../../../../infra/postgres/study-server/DB.sql) được đọc để xác nhận các field `users` có trong artifact và `bio` không có; live schema chưa kiểm tra.
- Registry-wired [createDD-markdown skill](../../../../../.agents/skills/create_dd_api/docs/dd/createDD_MARKDOWN_SKILL.md), [8-file template](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/), và [Study Markdown workflow](../../../../../.agents/server-study/workflows/README.md).

## Package checks

| Check | Result | Status |
|---|---|---|
| File manifest | 11 Markdown files: 8 core sheets + `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md`; không có ZIP mới. | PASS — STATIC |
| Front matter và sheet structure | 8/8 sheet có YAML front matter; đúng prefix `00`–`07`; mỗi sheet giữ appendix đối chiếu workbook nguồn. | PASS — STATIC |
| Catalog contract | Method/path, một Bearer header, `ApiEnvelope<UserProfile>`, HTTP 200 `DESIGN_RESOURCE_RETRIEVED` và đúng lỗi 401/403/500 được giữ. | VERIFIED_STATIC_ONLY |
| Diagram/source boundary | AC-02 claim wording và permissions; AC-11 avatar/profile sequence; current #03/#04/#13/#14 source được ghi riêng, không reconcile bằng suy đoán. | VERIFIED_STATIC_ONLY |
| JSON examples | 4/4 block `json` parse được. | PASS |
| Links/anchors | 63 local links; mọi file/path/anchor resolve. | PASS — STATIC |
| Tables, fences, whitespace | 33 bảng, 384 dòng dữ liệu; 450 dòng Markdown dạng bảng gồm header/separator; độ rộng nhất quán; fences cân bằng; mọi file có final newline; không trailing whitespace. | PASS — STATIC |
| Fingerprints | Baseline từng file được ghi dưới đây; output fingerprint tính trên 8 sheet + `PLAN_RESULT.md` + `OPEN_QUESTIONS.md`, bỏ `VERIFICATION_REPORT.md`: `3a49273b98ec9b9e287ff2807107a34852a1453cbf2f5f8ab9f8e0b44d35eb08`. | PASS — STATIC |
| `git diff --check` | Đã chạy trên thay đổi tracked thuộc API #04, hai API #14 reports và worklogs; không diagnostics. File mới được kiểm tra bằng hygiene scanner. | PASS |
| Application tests/runtime/live DB | Không chạy; không tuyên bố runtime, deployment, production hoặc live schema verification. | NOT_RUN |

## Connected API review

- **AC-02, #03 → #04:** #03 current source trả profile cơ bản cùng token; diagram tiếp tục gọi #04 để lấy profile/role/permissions. Current claim shape `sub`/`roles` khác diagram `user_id`/`role`; #04 response không có permissions. Lý do fetch lại và claim contract được giữ trong [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).
- **AC-11, #04/#13/#14:** #13 upload Object Storage và chỉ trả URL; #14 cập nhật `full_name`, `phone`, `avatar_url`; #14 source bỏ qua `bio`; #04 reload cũng không trả `bio`. Upload storage và update DB là hai request riêng, chưa có compensation được xác nhận.
- API #14 report cũ ghi route/module/test `NOT_FOUND`; macro-review đã cập nhật source status thành `SOURCE_PRESENT`. Có test file không chứng minh tests pass; lần review này không chạy test.

## Runtime và dữ liệu

- API #04 source xác thực Student từ JWT `roles`, SELECT `users` bằng numeric `sub`, không lọc `status` hoặc đối chiếu `users.role`.
- Row không tồn tại trả 401 theo source; SQLAlchemy query failure rollback và trả 500; lỗi `UserProfile` mapping trả 500 an toàn.
- `avatar_url`/`phone` None được serialize thành JSON `null`; `bio` và permissions không có trong current response model.
- Candidate DDL cho phép `users.status` NULL trong khi model yêu cầu string; nếu giá trị NULL, mapping lỗi thành 500. Live schema chưa xác minh.
- DDL trong repository là candidate artifact; live DB/schema, deployment và end-to-end behavior chưa xác minh.

## Template fingerprint — registered Markdown baseline

| File | SHA-256 |
|---|---|
| `00_Cover.md` | `fd5f568c5329d3069fbaff617a6f4ed3b5ffaf050e042c95b7c9100a05f79e63` |
| `01_Lich_su.md` | `d1cec6573433a9551812bf47552f8a44d7c533d790341941047c410e1d57771e` |
| `02_Overview.md` | `c2879c2f0e007395558dfee4167484786c5aadb3fdd63ab135ca111e7c5f8aa6` |
| `03_Request.md` | `37aaa1e9d7f3e83329e81ab38d922c9dff959284d5b7b3ae353878798dd4b7aa` |
| `04_Response.md` | `5bcb43ba5eb487302dd5d5efde4383b9f452f9fed2149f55315d64ff78a19ab8` |
| `05_Data_Mapping.md` | `11bc77bc0522d3af27b9499114991c8819046ac32bde5c1efdc841be088dcc5b` |
| `06_Error.md` | `e0160ea07fdbc74f2cafebd6ed3b21e60029662d28d67f5f6a0b4d95ba72be9b` |
| `07_table.md` | `4c9a0e037872333210aaf44ba9fbf00a0e63343a69d55250e537d2c3c5e2d356` |

**Output fingerprint:** `3a49273b98ec9b9e287ff2807107a34852a1453cbf2f5f8ab9f8e0b44d35eb08`.
