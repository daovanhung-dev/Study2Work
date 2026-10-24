---
title: "Overview"
order: 2
dd_id: "71"
api_name: "Khóa/mở khóa user Conditional"
source_sheet: "Overview"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | #71 |
| Module | ADMIN / SYSTEM MANAGEMENT — AC-31 |
| Method | PATCH |
| Endpoint | /api/v1/admin/users/{user_id}/status |
| Purpose | Admin khóa hoặc mở khóa user bằng cách cập nhật account status. |
| Consumer/Actor | Admin có quyền quản lý user theo precondition AC-31. |
| Authentication | Bearer JWT |
| Authorization | Role Admin; quyền user-management theo AC-31. Current Study chưa có Admin guard/policy. |
| Direct request | `path{user_id:int64!}`; body chưa được đặc tả. |
| Direct response | `ApiEnvelope<UserProfile>`; 200 `DESIGN_RESOURCE_UPDATED`. |
| Direct errors | 401/403/404/422/500 với đúng mã `DESIGN_*` trong catalog. |
| Basis | Method/path/auth/path type/response/status/errors DIRECT; body/status values/query/mutations DERIVED hoặc SOURCE_REQUIRED. |
| Status | Draft — Needs Confirmation |
| Current runtime state | UNWIRED / NOT_FOUND — route, module và focused test chưa có. |
| Transaction | Candidate transaction gộp status update và conditional refresh-token revoke; chưa có API #71 source. |
| Side effects | Direct diagram intent: update account status; session revoke “nếu cần”. Candidate chỉ revoke refresh token khi khóa; không chứng minh revoke access JWT. |

## Sources

- [Catalog và reusable schemas](../../../../../docs/lists/list_api.md) — API #71, ApiEnvelope, UserProfile, UserStatus.
- [AC-31 index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) và [activity diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — Admin STATUS branch; update status, optional revoke session, reload list/detail.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) — `users.status` VARCHAR và refresh token rows; live schema chưa xác minh.
- [V1-PILOT DDL](../../../../../infra/postgres/02_study_db.sql) — UUID `identity_projections.account_status` enum gồm ACTIVE/SUSPENDED và lifecycle values; model không tương đương legacy users.
- [API #3 query](../../../app/modules/guest/api_03_auth_login/query.py) và [view](../../../app/modules/guest/api_03_auth_login/view.py) — login/refresh kiểm tra ACTIVE; hiện revoke từng refresh token.
- [Current auth helper](../../../app/utils/auth.py) — current access guard parse JWT claims/roles nhưng không tra DB status hoặc revoked session.
- [API #4 UserProfile model](../../../app/modules/guest/api_04_users_me/models.py) — status hiện là string, không dùng enum đã định nghĩa.
- [API #68 Overview](../68_admin_users_list/02_Overview.md), [API #69 Overview](../69_admin_user_detail/02_Overview.md), [API #70 Overview](../70_admin_user_update/02_Overview.md) — cùng AC-31, chia riêng list/detail/profile/status.

## Tables read

| Relation | Fields candidate | Basis/status |
|---|---|---|
| Legacy users | id, full_name, email, role, avatar_url, phone, status, created_at, updated_at | Candidate theo DB.sql và UserProfile projection; live schema chưa xác minh. |
| Legacy refresh_tokens | id, user_id, revoked_at, expires_at | Candidate session rows theo DB.sql/API #3; bulk revoke cho #71 chưa có source. |
| V1-PILOT identity_projections | UUID subject, account_status, identity_version | Schema khác; enum chỉ gợi ý status candidate, không map trực tiếp vào int64 users. |

## Tables write

| Relation | Candidate fields | Basis/status |
|---|---|---|
| Legacy users | status, updated_at | `DERIVED CANDIDATE` từ STATUS intent và DDL/API #3 status check. |
| Legacy refresh_tokens | revoked_at | Conditional `DERIVED CANDIDATE` nếu owner yêu cầu revoke phiên khi khóa; hiện API #3 revoke theo một token ID. |

## Mục chú ý

- Catalog và diagram chỉ nêu path; `{status:UserStatus!}` là body suy ra, không phải direct contract.
- `ACTIVE`/`SUSPENDED` là candidate cặp mở khóa/khóa; reusable `UserStatus` không có enum member list. V1-PILOT account_status không chứng minh legacy `users.status` constraint.
- Login và refresh hiện từ chối status khác `ACTIVE`; đổi status thành `SUSPENDED` sẽ chặn các lần đăng nhập/refresh tiếp theo nếu cùng schema được dùng.
- Access JWT guard hiện chỉ kiểm tra Bearer/JWT claims/roles; không tra `users.status`, refresh_tokens hoặc revocation list. Existing access JWT có thể tiếp tục dùng đến expiry theo source hiện tại.
- Revoke refresh-token rows không revoke access JWT đã phát hành. Cần policy/token mechanism riêng nếu yêu cầu khóa có hiệu lực tức thời trên mọi request.
- API #70 không đổi status; API #72 là soft-delete/anonymize. Không gộp các mutation này vào #71.

## Candidate mapping — DERIVED

Candidate body có một field `status`; cho use case khóa/mở khóa, đề xuất `SUSPENDED` để khóa và `ACTIVE` để mở. Khi chuyển sang `SUSPENDED`, phương án đơn giản là cùng transaction cập nhật user status và `revoked_at` cho các refresh-token rows chưa revoke và chưa hết hạn. Khi mở khóa, không khôi phục refresh tokens đã revoke; user đăng nhập lại. Cả enum mapping, body, transaction và điều kiện revoke đều cần xác nhận; access JWT hiện tại vẫn không bị thu hồi tức thì.

## Conflicts

- Request body/status values vắng mặt trong catalog/diagram nhưng operation/path yêu cầu đổi status: contract gap, không phải nguồn cho exact JSON.
- Legacy `users.status` là VARCHAR; V1-PILOT `account_status` là ENUM trên UUID projection. Không coi enum pilot là enum của legacy users.
- Diagram “revoke session nếu cần” để policy conditional; current source chỉ có refresh-token revocation theo một token ID và stateless access JWT guard.
- Current source login/refresh kiểm tra account ACTIVE, nhưng access-token protected request không kiểm tra account status; khóa tài khoản không bảo đảm thu hồi ngay access token.
- API #68 response cardinality, UserProfile.bio và UserRole/UserStatus gaps còn mở ở các DD liên quan; #71 không tự sửa chúng.

## Security note

- Authenticate/authorize Admin và quyền user management trước khi lookup/update; current Student guard không phù hợp.
- Không trả password hash, refresh-token hash hoặc token secrets trong UserProfile.
- Revoke refresh-token hashes/rows chỉ theo policy đã duyệt; không tuyên bố access JWT invalidation nếu không có denylist/version check.
- Không cho phép trạng thái `DELETION_PENDING`/`ANONYMIZED` từ API #71 chỉ vì chúng tồn tại trong pilot enum; đó là lifecycle #72/schema concern.

## Performance note

Status update theo user primary key và optional refresh-token revoke theo `user_id` dự kiến xử lý ít hàng, nhưng index/row count và live schema chưa xác minh. Không tạo index/migration trong DD.

## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `Overview`
- Dimension: `A1:BA10`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `4`
- Số vùng merge: `0`

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 1 | `A1` | 【Khái quát】 |  |
| 3 | `B3` | Get thông tin…. |  |
| 5 | `A5` | 【Mục chú ý】 |  |
| 7 | `B7` | Không có |  |

</details>
