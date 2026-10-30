# Plan Result — API #48 Tải lecture của Mentor

## Kết quả plan trước authoring

- Task docs, scope server-study; không có dependency cross-scope.
- API #48 là bước GET lại lecture sau API #47 theo AC-21; AC-22 Content là workflow riêng.
- Contract được giữ nguyên: GET /api/v1/mentor/lectures/{lecture_id}, Mentor Bearer JWT, lecture_id:int64!, ApiEnvelope<Lecture>, HTTP 200 và chỉ errors 401/403/404/500.
- Candidate query dùng legacy lessons LEFT JOIN courses; V1-PILOT UUID schema không được gộp; live schema chưa xác minh.
- Candidate authorization thống nhất direct owner với #46/#47; assignment và Mentor identity mapping chưa có nguồn.
- Không áp dụng status filter; local API #47 explicitly writes `PUBLISHED` and #48 returns stored status.
- The initial docs-only plan lacked an asset resolver. API #34/#47 source now provides persisted `uploads` metadata and ordered `lesson_uploads` links for API #48; live schema remains unverified.
- Output là 8 sheet Markdown + 3 report; 07_table.md giữ read-only pattern; không tạo ZIP hoặc sửa runtime/schema/catalog/diagram.

## Source inventory và coverage

| Source | Loại | Bằng chứng dùng | Trạng thái |
|---|---|---|---|
| docs/lists/list_api.md | Contract | API #48, Lecture, UploadAsset, exact status/error set | DIRECT |
| AC_UNICA/00_AC_API_INDEX.md | Workflow | AC-21 Mentor owns/assigned precondition; sequence #46/#34/#47/#48 | DIRECT |
| AC_03_MENTOR_TEACHING.drawio | Diagram | Upload/Object Storage → #47 INSERT Lecture/Content → #48 read detail; #22 Content riêng | DIRECT; write target #47 remains ambiguous |
| DB_UNICA_TABLES.md / DB_UNICA_ERD.drawio | Schema design | lessons/course relationship; resources metadata; no uploads entity | DESIGN_ONLY |
| infra/postgres/study-server/DB.sql | Legacy DDL | BIGINT lessons/courses; lesson projection columns; resources lacks UploadAsset fields | Artifact only; live DB unknown |
| infra/postgres/02_study_db.sql | V1-PILOT DDL | UUID courses/lessons, content_blocks, file_objects | Separate schema; not combined |
| API #46 DD | Prior DD | direct owner candidate; assignment/schema gaps; no Mentor PUBLISHED filter | DERIVED / needs confirmation |
| API #47 implementation | Prior API | ordered `asset_refs` resolved from uploads and written with lesson into `lesson_uploads`; status `PUBLISHED` | LOCAL_SOURCE_BACKED; live DB unknown |
| API #34 implementation | Prior API | UploadAsset metadata persisted in legacy `uploads` artifact | LOCAL_SOURCE_BACKED; live DB unknown |
| API #9/#26 DDs | Prior DDs | lessons mapping and resources boundary | DESIGN_ONLY precedent |
| Current router/auth/response source | Runtime | #48 route/module wired; shared Mentor guard available; error helper defaults data to null | CURRENT_BEHAVIOR |
| createDD-markdown + DD_API_Template_MD | Authoring | Registry wire, 8 Markdown templates and appendix suffixes | WIRED to server-study |

## API Requirement Matrix

| API ID | Contract item | Giá trị | Basis/status |
|---|---|---|---|
| #48 | Method/path | GET /api/v1/mentor/lectures/{lecture_id} | Catalog + AC-21; DIRECT |
| #48 | Actor/auth | Mentor / Bearer JWT | Catalog + AC-21; DIRECT |
| #48 | Path | lecture_id:int64! | Catalog + AC-21; DIRECT |
| #48 | Body/query | Không khai báo | Catalog; DIRECT |
| #48 | Success | HTTP 200 DESIGN_RESOURCE_RETRIEVED; ApiEnvelope<Lecture> | Catalog + AC-21; DIRECT |
| #48 | Error | 401 DESIGN_AUTHENTICATION_REQUIRED | Catalog; DIRECT |
| #48 | Error | 403 DESIGN_ACCESS_DENIED | Catalog; DIRECT |
| #48 | Error | 404 DESIGN_RESOURCE_NOT_FOUND | Catalog; DIRECT |
| #48 | Error | 500 DESIGN_INTERNAL_ERROR | Catalog; DIRECT |

## Request Usage Matrix

| Request field | Source | Data Mapping step | Validate/use | Query/response use | Gap |
|---|---|---:|---|---|---|
| Authorization | Header | 0 | Bearer JWT and Mentor role | Supplies principal for ownership check | Shared guard is wired; deployed identity mapping/assignment unresolved |
| lecture_id | Path | 1/2 | Required int64; no extra positive-only rule | Q1 lessons.id; data.id | Runtime maps malformed/overflow to 404 as an implementation decision; confirm with contract owner |
| Body | N/A | N/A | N/A | N/A | No body in catalog |
| Query | N/A | N/A | N/A | N/A | No query in catalog |

## Query Matrix

| Query | Type | Source | Query item | Rule | Evidence status |
|---|---|---|---|---|---|
| Q1 | SELECT | lessons AS l | id, course_id, name, content, sort_order, status | Lecture fields | Checked-in legacy DDL; live schema not verified |
| Q1 | LEFT JOIN | courses AS c | c.id = l.course_id | Parent course and owner | Checked-in legacy relation; live schema not verified |
| Q1 | WHERE | lessons AS l | l.id = :lecture_id | No row → 404 | Runtime/API contract |
| Q1 | CHECK | courses AS c | c.mentor_id = :mentor_id | Owner mismatch → 403 | Runtime matches #46/#47; assigned course unsupported |
| Q1 | FILTER | lessons.status | Excludes `DELETED` | Return stored status for other values | Local API #86 tombstone visibility |
| Q2 | SELECT | lesson_uploads LEFT JOIN uploads | Ordered linked metadata with owner/purpose/course scope | API #48 asset projection | Migration 005 and current source; live DB unknown |

## Mutation Matrix

| Operation | Target | Condition | Fields | Status |
|---|---|---|---|---|
| None | N/A | Read-only endpoint | No INSERT/UPDATE/DELETE | N/A — READ-ONLY API |

## Response Source Matrix

| Response field | Contract type | Candidate source | Transform/null rule | Status |
|---|---|---|---|---|
| data.id | int64 | lessons.id | Direct | Legacy DDL; live schema unknown |
| data.course_id | int64 | lessons.course_id | Required; NULL blocks mapping | DDL/guide discrepancy; runtime returns 500 |
| data.title | string | lessons.name | Alias name → title | Checked-in legacy mapping |
| data.content | string? | lessons.content | Preserve text; SQL NULL serializes as JSON null | Current model and tests |
| data.assets[] | UploadAsset[] | lesson_uploads + uploads | Ordered linked metadata; no links returns [] | Current source and tests; live schema unknown |
| data.assets[].id | int64 | uploads.id | Direct | API #34 local persistence |
| data.assets[].name | string | uploads.file_name | Alias file_name to name | API #34 local persistence |
| data.assets[].url | uri | uploads.url | Direct | API #34 local persistence |
| data.assets[].content_type | string | uploads.content_type | Direct | API #34 local persistence |
| data.assets[].size_bytes | int64 | uploads.size_bytes | Direct | API #34 local persistence |
| data.assets[].status | UploadStatus | uploads.status | Return stored string | Enum values remain unspecified |
| data.order | int32 | lessons.sort_order | Alias sort_order → order | Checked-in legacy mapping |
| data.status | LessonStatus | lessons.status | Return stored status; no filter | Enum values remain unspecified |
| businessCode | string | API catalog | Exact branch code | DIRECT |
| meta | object | API guideline/helper | Error helper returns `data: null` and empty meta | CONSISTENT |
| traceId | uuid | Request context | Propagate request trace | API guideline convention |

## Macro review AC-21 APIs #46–#48

| Check | Kết quả | Trạng thái |
|---|---|---|
| #46 selection → #47 create → #48 reload | Endpoint order matches AC-21; #48 reads one Lecture by the ID created by #47. | PASS |
| Course access | #46/#47/#48 use the same direct-owner candidate; assigned-course support and Mentor ID mapping remain open. | CONSISTENT / SOURCE_REQUIRED |
| Publish/status behavior | #46 is Mentor management; #47 inserts `PUBLISHED`; #48 returns stored status without filtering. | CONSISTENT / LOCAL_SOURCE_BACKED |
| Schema | Group keeps legacy BIGINT candidates separate from V1-PILOT UUID/versioned artifacts. | CONSISTENT / LIVE_SCHEMA_NOT_VERIFIED |
| Lecture payload | #47 and #48 use the same nullable Lecture content model; #48 returns stored status without filtering. Catalog enum values remain open. | CONSISTENT / LOCAL_SOURCE_BACKED |
| Assets | #34 uploads metadata → #47 ordered lesson_uploads links → #48 ordered lookup. Legacy resources/V1-PILOT file_objects are not mixed in. | LOCAL_SOURCE_BACKED / LIVE_SCHEMA_NOT_VERIFIED |
| Error envelope | Shared helper defaults error data to null; #48 uses that helper. | CONSISTENT |
| AC-22 Content | Content CRUD stays separate; #48 remains a Lecture read endpoint. | PASS |

## Kết luận

API #48 is wired locally and reads the ordered asset relation written atomically by API #47. Focused HTTP coverage verifies success, access, missing/broken relations, nullable content, catalog errors and OpenAPI. DD remains Draft — Needs Confirmation because the live legacy schema/migration state, assigned-course authorization, identity mapping, enum semantics and malformed-path contract remain unconfirmed. Macro review #46–#48 is consistent for the local implementation; no claim is made about live deployment.

