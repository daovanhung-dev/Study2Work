# Plan Result — API #47 Tạo lecture

## Kết quả plan trước authoring

- Task: docs; scope server-study; không có dependency cross-scope.
- Catalog là contract kỳ vọng; current route/module/test source không có API #47.
- AC-21 xác nhận thứ tự #46 → #34 upload/Object Storage → #47 tạo lecture → #48 đọc lại.
- Legacy lessons là mapping candidate; V1-PILOT UUID/versioned là schema khác. Live DB không được xác minh.
- Không ghi asset refs hoặc tạo resources/uploads mapping cho đến khi biết asset format, ID, metadata source và persistence.
- Trạng thái: Draft — Needs Confirmation; các câu hỏi asset/content/schema/quyền chặn việc coi DD là implementation-ready.

## Source inventory và coverage

| Source | Loại | Bằng chứng dùng trong DD | Trạng thái |
|---|---|---|---|
| docs/lists/list_api.md | Contract | API #47, #48–#50, Lecture, UploadAsset | DIRECT |
| AC_UNICA/00_AC_API_INDEX.md | Workflow | AC-21 actor, precondition, endpoint order | DIRECT |
| AC_03_MENTOR_TEACHING.drawio | Diagram | #34 upload, Object Storage, #47 INSERT Lecture/Content, #48 reload; AC-22 Content CRUD riêng | DIRECT; #47 write target còn mơ hồ |
| DB_UNICA_TABLES.md / DB_UNICA_ERD.drawio | Schema design | lessons/resources fields, no lectures/contents/uploads entity | DESIGN_ONLY |
| infra/postgres/study-server/DB.sql | Legacy DDL | BIGINT course/lesson, name/content/sort_order/status/timestamps | Artifact only; live schema not verified |
| infra/postgres/02_study_db.sql | V1-PILOT DDL | UUID course_versions/lessons/content_blocks/file_objects | Separate model; không gộp |
| API #46 DD | Prior DD | Direct owner predicate là candidate; no PUBLISHED gate | DERIVED / needs confirmation |
| API #34 DD | Prior DD | UploadAsset ID/persistence/lookup unresolved | SOURCE_REQUIRED |
| API #9 and #11 DDs | Prior DDs | Lesson name/order aliases; resources relation/read-only pattern | DESIGN_ONLY mapping precedent |
| Study router/auth/response helper | Current source | No #47 route; Student-only current guard; helper data fallback {} | CURRENT_BEHAVIOR |
| createDD-markdown + Markdown templates | Authoring workflow | 8 template sheets/headings/front matter/appendices checked | WIRED to server-study |
| Study docs archive scan | Input gate | No ZIP/XLSX/XLSM under apps/study-server/docs | No archive source |

## API Requirement Matrix

| API ID | Method | Endpoint | Actor/auth | Required input | Success / errors | Business rule / side effect | Status |
|---|---|---|---|---|---|---|---|
| 47 | POST | /api/v1/mentor/courses/{course_id}/lectures | Mentor / Bearer JWT | course_id:int64; title:string; content:int64; asset refs:string; order:int32 | 201 DESIGN_RESOURCE_CREATED; exactly 401/403/404/422/500 catalog codes | Create a Lecture under a course the Mentor may manage; AC-21 then reloads via #48; candidate INSERT lessons, asset resolution open | Draft — Needs Confirmation |

## Request Usage Matrix

| Request field | Source | Data Mapping step | Validate | SQL/mutation usage | Response usage | Gap |
|---|---|---|---|---|---|---|
| Authorization | Header | 0 | Valid JWT + Mentor role | Candidate principal → courses.mentor_id comparison | Not echoed | Mentor guard/principal mapping unresolved |
| course_id | Path | 1–2 | Parse int64 | Q1 courses.id; M1 lessons.course_id | data.course_id | Legacy BIGINT vs pilot UUID/live schema |
| title | Body | 1/3 | Required string; max 200 DERIVED | M1 lessons.name | data.title | No minimum/trim rule |
| content | Body | 1/3 | Required int64 | M1 lessons.content as decimal text candidate | data.content:string? | Meaning/type discrepancy |
| asset refs | Body catalog label | 1/pending | Required opaque string | No committed mutation/query | data.assets[] | Wire key, format, metadata lookup unresolved |
| order | Body | 1/3 | Required int32 | M1 lessons.sort_order | data.order | No range beyond type |

## Query Matrix

| Query ID | Type | Candidate source | Item | Predicate | Result / branch | Evidence |
|---|---|---|---|---|---|---|
| Q1 | SELECT | courses AS c | c.id | c.id = :course_id | Missing → candidate 404 | Legacy DDL |
| Q1 | SELECT | courses AS c | c.mentor_id | c.id = :course_id | Compare with current Mentor principal; mismatch → candidate 403 | Direct-owner rule DERIVED from #46 |
| Q2 | N/A | N/A | Asset lookup | N/A | Not issued; no resolver source | SOURCE_REQUIRED |

## Mutation Matrix

| ID | Operation | Table/condition | Column | Value | Mapping file | Transaction/failure |
|---|---|---|---|---|---|---|
| M1 | INSERT | lessons; Q1 exists and owner check passes | course_id | Path course_id | 07_lessons_insert.md | Candidate one-row transaction; rollback on failure |
| M1 | INSERT | lessons; same condition | name | title | 07_lessons_insert.md | Same transaction |
| M1 | INSERT | lessons; same condition | content | decimal text candidate from int64 | 07_lessons_insert.md | DERIVED; meaning unresolved |
| M1 | INSERT | lessons; same condition | sort_order | order | 07_lessons_insert.md | Same transaction |
| M1 | INSERT | lessons; same condition | created_at | CURRENT_TIMESTAMP | 07_lessons_insert.md | Same transaction; no DDL default |
| M1 | INSERT | lessons; same condition | updated_at | CURRENT_TIMESTAMP | 07_lessons_insert.md | Same transaction; no DDL default |
| M1 | INSERT | lessons; same condition | status | Omit column → legacy default DRAFT | 07_lessons_insert.md | Enum validity unresolved |
| M2 | N/A | No confirmed asset table or lookup | N/A | N/A | N/A | SOURCE_REQUIRED; no guessed write |

## Response Source Matrix

| Response field | Type | Candidate source | Step | Transform / null rule | Gap |
|---|---|---|---|---|---|
| success | boolean | API result | 5 | `true` on success | N/A |
| businessCode | string | API catalog | 5 | `DESIGN_RESOURCE_CREATED` | Direct |
| message | string | Application message | 5 | Safe localized message | Exact message text not specified |
| data.id | int64 | lessons.id | 4 | Direct | Legacy candidate |
| data.course_id | int64 | lessons.course_id | 4 | Direct | Legacy candidate |
| data.title | string | lessons.name | 4 | Alias name → title | Legacy candidate |
| data.content | string? | lessons.content | 4 | Decimal string candidate; omit NULL only if approved | Type/meaning discrepancy |
| data.assets[] | UploadAsset[] | N/A | Pending | No safe fabricated value | SOURCE_REQUIRED; required response field |
| data.order | int32 | lessons.sort_order | 4 | Alias sort_order → order | Legacy candidate |
| data.status | LessonStatus | lessons.status | 4 | Candidate default DRAFT | Enum values unknown |
| meta | object | Envelope default | 5 | `{}` | API guideline |
| traceId | uuid | Request trace | 5 | Propagate request trace | API guideline; no API #47 route today |

## Kết luận

Một candidate đơn giản cho bản legacy là: xác thực Mentor → đọc course và so quyền direct-owner → INSERT lessons → trả Lecture và client gọi #48 reload. Candidate chỉ có thể trở thành implementation contract khi xác nhận course assignment/ID mapping, content semantics, asset resolver/persistence, schema đang chạy và LessonStatus. Không thêm PUBLISHED filter, Content table, uploads table hoặc resources write theo suy đoán.

## Macro review AC-21 APIs #46–#48

| Check | Kết quả | Trạng thái |
|---|---|---|
| #46 selection → #47 create → #48 reload | Khớp thứ tự AC-21; #48 đọc cùng Lecture ID được tạo bởi #47. | PASS |
| Course access | #46/#47/#48 cùng dùng direct-owner candidate; assignment và Mentor identity mapping chưa có nguồn. | CONSISTENT / SOURCE_REQUIRED |
| Publish/status | #47 candidate có thể tạo DRAFT; #48 không lọc PUBLISHED; #46 không áp dụng public curriculum filter. | CONSISTENT / DERIVED |
| Schema | Cả ba DD giữ legacy BIGINT tách với V1-PILOT UUID/versioned; live schema chưa xác minh. | CONSISTENT / NOT_VERIFIED |
| Lecture fields | #47 và #48 giữ cùng shape; content null behavior và LessonStatus values còn mở. | CONSISTENT / NEEDS_CONFIRMATION |
| Asset refs → UploadAsset[] | #34 chưa có persistence/lookup; #47 không ghi resources/file_objects; #48 không đoán query hoặc trả assets giả. | BLOCKING SOURCE_REQUIRED |
| Error envelope | Guideline data:null và helper data:{} vẫn được tách biệt ở cả nhóm. | CONSISTENT / DISCREPANCY |
| AC-22 Content | Vẫn là workflow riêng, không nhập vào Lecture API #47/#48. | PASS |

Review hoàn tất sau khi DD #48 được author và kiểm tra. Các blocker chưa được giải quyết bằng suy luận; xem [API #48 open questions](../48_mentor_lecture_detail/OPEN_QUESTIONS.md).

