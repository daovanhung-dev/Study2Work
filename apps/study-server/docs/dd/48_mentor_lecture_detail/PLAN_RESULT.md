# Plan Result — API #48 Tải lecture của Mentor

## Kết quả plan trước authoring

- Task docs, scope server-study; không có dependency cross-scope.
- API #48 là bước GET lại lecture sau API #47 theo AC-21; AC-22 Content là workflow riêng.
- Contract được giữ nguyên: GET /api/v1/mentor/lectures/{lecture_id}, Mentor Bearer JWT, lecture_id:int64!, ApiEnvelope<Lecture>, HTTP 200 và chỉ errors 401/403/404/500.
- Candidate query dùng legacy lessons LEFT JOIN courses; V1-PILOT UUID schema không được gộp; live schema chưa xác minh.
- Candidate authorization thống nhất direct owner với #46/#47; assignment và Mentor identity mapping chưa có nguồn.
- Không áp dụng PUBLISHED filter để đọc được candidate DRAFT vừa tạo bởi #47.
- Lecture.assets[] và các field con là SOURCE_REQUIRED; API #34 chưa có asset ID/persistence/lookup, resources không đủ UploadAsset fields.
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
| API #47 DD | Prior DD | legacy lesson create candidate; DRAFT read-after-create; assets unresolved | DERIVED / SOURCE_REQUIRED |
| API #34 DD | Prior DD | upload metadata ID/persistence/lookup absent | SOURCE_REQUIRED |
| API #9/#26 DDs | Prior DDs | lessons mapping and resources boundary | DESIGN_ONLY precedent |
| Current router/auth/response source | Runtime | no #48 route; current auth helper Student-only; error helper defaults data to {} | CURRENT_BEHAVIOR |
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
| Authorization | Header | 0 | Bearer JWT and Mentor role | Supplies principal for ownership check | Mentor guard and numeric/UUID identity binding unresolved |
| lecture_id | Path | 1/2 | Required int64; no extra positive-only rule | Q1 lessons.id; data.id | Invalid/overflow path error not declared; no 422 in catalog |
| Body | N/A | N/A | N/A | N/A | No body in catalog |
| Query | N/A | N/A | N/A | N/A | No query in catalog |

## Query Matrix

| Query | Type | Candidate source | Query item | Rule | Evidence status |
|---|---|---|---|---|---|
| Q1 | SELECT | lessons AS l | l.id | Lecture ID | Legacy candidate; live schema unknown |
| Q1 | SELECT | lessons AS l | l.course_id | Required course ID | Legacy DDL allows NULL; guide says required |
| Q1 | SELECT | lessons AS l | l.name | Map to title | Legacy candidate; API #9 precedent |
| Q1 | SELECT | lessons AS l | l.content | Preserve stored text | Legacy nullable candidate; null rule unresolved |
| Q1 | SELECT | lessons AS l | l.sort_order | Map to order | Legacy candidate; API #9 precedent |
| Q1 | SELECT | lessons AS l | l.status | Return stored status | Enum members unknown |
| Q1 | LEFT JOIN | courses AS c | c.id | c.id = l.course_id | Candidate parent check |
| Q1 | SELECT | courses AS c | c.mentor_id | Candidate direct-owner comparison | Assignment relation absent |
| Q1 | WHERE | lessons AS l | l.id = :lecture_id | No row → candidate 404 | DERIVED from declared code set |
| Q1 | CHECK | courses AS c | c.mentor_id = :mentor_id | Owner mismatch → candidate 403 | DERIVED; principal mapping unresolved |
| Q1 | FILTER | N/A | No PUBLISHED filter | Candidate DRAFT from #47 remains readable | DERIVED from AC-21 read-after-create flow |
| Q2 | N/A | N/A | Asset metadata lookup | No approved registry/query exists | SOURCE_REQUIRED; no guessed query |

## Mutation Matrix

| Operation | Target | Condition | Fields | Status |
|---|---|---|---|---|
| None | N/A | Read-only endpoint | No INSERT/UPDATE/DELETE | N/A — READ-ONLY API |

## Response Source Matrix

| Response field | Contract type | Candidate source | Transform/null rule | Status |
|---|---|---|---|---|
| data.id | int64 | lessons.id | Direct candidate | Legacy candidate |
| data.course_id | int64 | lessons.course_id | Required; NULL blocks mapping | DDL/guide discrepancy |
| data.title | string | lessons.name | Alias name → title | Legacy candidate |
| data.content | string? | lessons.content | Preserve text; NULL omit/null unresolved | Legacy candidate |
| data.assets[] | UploadAsset[] | No approved source | Do not fabricate empty array or asset records | SOURCE_REQUIRED; blocks full response mapping |
| data.assets[].id | int64 | N/A | No source/generator/lookup | SOURCE_REQUIRED |
| data.assets[].name | string | N/A | No persistent metadata source | SOURCE_REQUIRED |
| data.assets[].url | uri | N/A | URL policy/source unresolved | SOURCE_REQUIRED |
| data.assets[].content_type | string | N/A | Metadata source unresolved | SOURCE_REQUIRED |
| data.assets[].size_bytes | int64 | N/A | Metadata source unresolved | SOURCE_REQUIRED |
| data.assets[].status | UploadStatus | N/A | Enum/lifecycle unresolved | SOURCE_REQUIRED |
| data.order | int32 | lessons.sort_order | Alias sort_order → order | Legacy candidate |
| data.status | LessonStatus | lessons.status | Return stored status; no publish filter | Enum values unresolved |
| businessCode | string | API catalog | Exact branch code | DIRECT |
| meta | object | API guideline/helper | Expected error data:null; current helper defaults {} | DISCREPANCY |
| traceId | uuid | Request context | Propagate request trace | API guideline convention |

## Macro review AC-21 APIs #46–#48

| Check | Kết quả | Trạng thái |
|---|---|---|
| #46 selection → #47 create → #48 reload | Endpoint order matches AC-21; #48 reads one Lecture by the ID created by #47. | PASS |
| Course access | #46/#47/#48 use the same direct-owner candidate; assigned-course support and Mentor ID mapping remain open. | CONSISTENT / SOURCE_REQUIRED |
| Publish/status behavior | #46 does not impose public PUBLISHED behavior; #47 candidate may create DRAFT; #48 does not filter status so read-after-create remains possible. | CONSISTENT / DERIVED |
| Schema | Group keeps legacy BIGINT candidates separate from V1-PILOT UUID/versioned artifacts. | CONSISTENT / LIVE_SCHEMA_NOT_VERIFIED |
| Lecture payload | #47 and #48 use the same Lecture fields; content null behavior and LessonStatus values remain open. | CONSISTENT / NEEDS_CONFIRMATION |
| Assets | #34 → #47 refs → #48 assets[] has no source-backed ID/metadata persistence or resolver. No guessed resources/file_objects mapping was added. | BLOCKING SOURCE_REQUIRED |
| Error envelope | All three DDs keep guideline data:null separate from current helper data:{} behavior. | CONSISTENT / DISCREPANCY |
| AC-22 Content | Content CRUD stays separate; #48 remains a Lecture read endpoint. | PASS |

## Kết luận

DD #48 giữ đúng catalog và AC-21. Candidate legacy read/query phù hợp để thảo luận implementation nhưng không xác nhận live schema. API #48 chưa được lập trình; required assets[] chưa có nguồn nên success mapping đầy đủ vẫn bị chặn bởi SOURCE_REQUIRED. Macro review #46–#48 hoàn tất với các gap được ghi rõ; không tự hợp thức hóa assignment, schema, status hay asset semantics.

