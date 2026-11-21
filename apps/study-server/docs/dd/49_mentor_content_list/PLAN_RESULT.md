# Plan Result — API #49 Lấy cây nội dung course

## Thực hiện theo plan coding

- Task: `coding`, scope `server-study`, secondary `test`/`docs`.
- Giữ nguyên các thay đổi worktree có sẵn cho API #34/#47/#48 và các context/worklog khác.
- Thêm API #49 route, Mentor direct-owner authorization, signed-int64 raw path mapping, Content response models, SQL constants, tree integrity mapping và API-level tests.
- Thêm legacy BIGINT `contents` table vào `DB.sql` và migration artifact `006_contents.sql`; migration không được chạy trên DB live.
- Chọn response phẳng `Content[]` với `parent_id`; đồng bộ API catalog và AC-22 diagram từ singular `Content` để biểu diễn nhiều node.
- Empty course trả 200 với `data: []`; invalid/out-of-range ID và missing course trả 404; owner mismatch trả 403. Không filter `status`, filter `deleted_at IS NULL`.
- DD API #49 cập nhật theo source hiện tại; vẫn giữ `Draft — Needs Confirmation` cho các quyết định response/persistence chưa được product/schema owner duyệt.

## Source inventory and boundaries

| Source | Evidence/status |
|---|---|
| `docs/lists/list_api.md` | `GET /api/v1/mentor/courses/{course_id}/content`; success/errors catalog giữ nguyên; response đồng bộ `ApiEnvelope<Content[]>`. |
| AC-22 activity diagram | GET → đọc cây → CRUD/publish; output schema đồng bộ `Content[]`. |
| `app/api/v1.py`, API #49 module, middleware | Route/source-backed locally; path có design error dispatch. |
| `contents` DDL/migration 006 | Local checked-in BIGINT model; không chứng minh live migration/schema. |
| V1-PILOT DDL | UUID/versioned `content_blocks` model khác; không dùng ở API #49. |
| Related DD #50–#53 | Shared `contents` base model now available as source artifact; version history, lifecycle and approval rules remain open. |

## Implementation mapping

| Concern | Current implementation |
|---|---|
| Authentication | `validate_current_user_request(..., role="MENTOR")`, numeric principal from current Study JWT guard. |
| Course access | `courses.id` lookup then direct `courses.mentor_id == principal_id`; assigned-course relation not checked. |
| Content query | `contents` rows for course with `deleted_at IS NULL`; all statuses returned; sort `parent_id NULLS FIRST, content_order, id`. |
| Tree projection | Flat response; strict typed fields; root `parent_id` omitted; rejects duplicate IDs, missing parents, cross-course rows and cycles. |
| Errors | 401 auth; 403 role/owner; 404 malformed/out-of-range/missing course; 500 DB/mapping; catalog code set unchanged. |
| Transactions | No commit; rollback on failed DB/mapping branches. |

## AC-22/AC-33 macro-review #49–#53

**Kết quả:** `VERIFIED_WITH_OPEN_QUESTIONS` — các API đã được đối chiếu sau khi có base Content DDL.

| Liên kết | Current source alignment | Open boundary |
|---|---|---|
| #49 read tree ↔ #50 create | `contents` provides course, type, title, payload, status, parent and order fields; #49 reads active rows. | Create root/order/status defaults, request validation and response contract remain DD owner decisions. |
| #50 create ↔ #51 update/version | Same base row is available for current Content fields. | #51 requires immutable revision/history model absent from `contents`; state transition open. |
| #51 update ↔ #52 publish | `status` column can store a state string. | Approval vs publish transitions, readiness and version selector remain open. |
| #52 publish ↔ #53 delete | `status` and `deleted_at` columns exist in local DDL. | Publish gates and delete eligibility remain proposals. |
| #49/#50/#51/#52 ↔ #53 hierarchy/delete | Same-course `parent_id` relation and `deleted_at` allow active-node filtering. | Policy for active child of deleted parent, cascade/blocking, audit/history remain open. |
| Shared auth/schema | Current Study Mentor guard and direct-owner pattern are source-backed; legacy BIGINT table mapping exists locally. | Assigned-course permission, enum/payload schemas, version history, live deployment and AC-33 approval/audit wiring remain unverified/open. |

No DD proposal is treated as approved business behavior. API #50–#53 remain unwired unless their current source proves otherwise.

## Remaining confirmation boundary

1. Confirm `Content[]` response vs original singular catalog design.
2. Approve ContentType/ContentStatus values and payload subtype schemas.
3. Decide whether direct owner alone is the policy and whether assigned Mentors are supported.
4. Define #51 version history, #52 approval/publish state transitions, #53 dependency behavior, and AC-33 audit integration.
5. Verify/apply migration 006 only through the authorized DB release process; this task does not claim live schema.

## Verification

Verification results are recorded in `VERIFICATION_REPORT.md` and the worklog. Live DB schema, migration deployment and service deployment were not probed.
