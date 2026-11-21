# ST-21 — Plan chi tiết

**Screen ID:** ST-21  
**Tên:** Tiến độ theo khóa học (Page)  
**Route trong inventory:** `/student/progress/:courseId`  
**Actor:** Student  
**Kế hoạch:** PLAN COMPLETE — plan này được ghi trước marker map và DD.  
**DD dự kiến:** BLOCKED bởi API #37 response, aggregate/access/empty policies chưa được chốt.  
**Implementation/runtime:** Study Web UNWIRED; Student API #37 route/module/query/test NOT_FOUND.

## 1. Mục tiêu và phạm vi

- Đặc tả ST-21 trong phiên này; nối ST-20 overview với lesson navigation ST-10/ST-11 theo inventory.
- Giữ nguyên `screen.png` và `code.html`. PNG 1280×1024 gần như chỉ có nền trống và dải tối ở đáy; HTML có header, breadcrumb, title/description, static empty card, nút quay lại ST-20 và footer. Nếu Chrome render được, tạo `screen_rendered.png` riêng từ HTML tĩnh, ghi provenance/hash/dimensions, và dùng ảnh đó làm nền annotation.
- Đánh số mọi nhóm giao diện nhìn thấy trong HTML render; mỗi marker sẽ map một-một với một element row của DD. Loaded progress/course/lesson chart chưa có trong assets nên không tạo element giả.
- Đặc tả API #37 đúng catalog (GET/path/Auth/response/statuses), giữ mismatch `UserProfile` với expected progress; không thêm schema, phép tính, code lỗi, query hoặc route runtime.
- Mô tả mối quan hệ ST-20 → ST-21, ST-21 → ST-10/ST-11 sau access gate, và quay lại ST-20; route/handoff là expected inventory, chưa phải client behavior.

## 2. Bằng chứng và ranh giới source

### Expected behavior

- Inventory ST-21: route `/student/progress/:courseId`, AC-18, API #37; hiển thị bài đã/đang/chưa học, tỷ lệ hoàn thành và mốc thời gian có chứng cứ; route tới ST-10/ST-11 theo `lesson_id` sau gate; states `loading/empty/in-progress/completed`.
- AC-18 diagram/API index: sau Student login, xem progress tổng hợp, chọn course, gọi `GET /api/v1/users/me/progress/{course_id}`, tổng hợp lesson + quiz + assignment progress. AC-18 không định nghĩa output fields, công thức hoặc quyết định quiz attempt/assignment submission.
- API catalog #37: Student Bearer; required `course_id:int64`; response `ApiEnvelope<UserProfile>`; success 200 `DESIGN_RESOURCE_RETRIEVED`; errors 401/403/404/500 với business codes catalog. DD #37 Draft; `UserProfile` không có progress fields.

### Current behavior

- Current folder ban đầu chỉ có `screen.png` 1280×1024 và static `code.html`; PNG có main content trống và dải đen dưới đáy; HTML có empty card “Chưa có dữ liệu tiến độ cho khóa học này.” và anchor `/student/progress`. HTML không có script, API call, auth, route parameter binding hoặc lesson list.
- Study Web hiện không có editable source/package/router cho Student route; ignored `dist` chỉ có `/` và không có #37 integration.
- Current Study Server không có API #37 route/module/query/test. Các API #65/#67 là Mentor progress, dùng actor/path/access khác nên không thay được API Student #37.
- API #37 DD là `Draft — Needs Confirmation`, giữ response `ApiEnvelope<UserProfile>` theo catalog nhưng ghi rõ response gap và chín câu hỏi mở: response DTO, aggregate dataset/formula, attempt/submission selection, enrollment/access, 403/404 masking, no-progress shape, path parsing, JWT identity/live schema, UserProfile projection.
- DB guide và legacy `infra/postgres/study-server/DB.sql` mô tả `lesson_progress` candidate với `status`, `progress_percent`, `last_accessed_at`, `completed_at`; API DD còn nêu candidates `quiz_attempts`, `quizzes`, `assignment_submissions`, `assignments`. Đây chỉ là design candidates. V1-PILOT `infra/postgres/02_study_db.sql` có `lesson_progress_facts` và `progress_snapshots` với UUID/enrollment snapshot model; hai schema generation không được tự reconcile và không chứng minh live schema.

### Discrepancies

- `screen.png` không có thiết kế loaded state; HTML chỉ mô tả empty state. Không dùng empty HTML để kết luận mọi course không có progress.
- API #37 catalog/DD trả `UserProfile`, trong khi AC-18/inventory cần course progress và lesson/course/assessment detail.
- API #37 DD candidate reads chưa có accepted rules; quiz nhiều attempts/submissions làm thay đổi aggregate; enrollment/role/course access chưa chốt.
- Inventory nói ST-21 nối `lesson_id` tới ST-10/ST-11 sau gate; chưa xác định lesson-specific access API, URL/content exposure, hay permission behavior trong ST-21.

## 3. Source trace cần thể hiện trong DD

```text
Expected inventory: ST-20 selects course → ST-21 GET #37(course_id) →
  show confirmed course progress → ST-10/ST-11 by lesson_id after access gate.
AC-18: Student login → course selected → #37 → aggregate lesson + quiz + assignment.
Current: ST-21 web route absent; Student API #37 route/module/query/test absent;
  PNG body blank; HTML is static no-progress fallback.
```

- #37 is GET/read-only, no mutation or side effect.
- Use only catalog error set 401/403/404/500; malformed path status is open, catalog has no 400/422 for #37.
- Do not derive overall course percent from lesson `progress_percent`, quiz score, or assignment score. Denominator, weights, eligibility, attempt/submission selection, rounding and cross-type combine formula are open.
- Do not treat Mentor #65/#67 local source as authorization or payload precedent for Student #37.

## 4. Planned marker and event coverage

Expected visible groups after HTML render (confirm count/coordinates before final map):

1. Brand/home link.
2. Header navigation group with active Tiến độ.
3. Breadcrumb including back to ST-20 and static course-progress label.
4. Page title.
5. Supporting description.
6. Empty-state progress icon.
7. Empty-state heading.
8. Empty-state explanation.
9. Return-to-overview CTA.
10. Footer brand.
11. Footer policy/support links group.

Expected event plan (refine against final visible DOM):

1. Route entry/auth and `courseId` input.
2. Parse/validate course path value without inventing malformed-path response.
3. Load API #37 with Bearer Student and no body/query.
4. Map response only if a progress DTO is approved; currently `UserProfile` cannot supply it.
5. Render loading/empty/in-progress/completed/error according to clarified contract; retain current inventory state names and document unresolved conditions.
6. Select a lesson to ST-10/ST-11 only after access gate; there is no lesson element in the current HTML.
7. Return to ST-20 and static header/footer navigation.
8. Handle 401/403/404/500 and transport failures without adding API status codes.

## 5. Blockers and no-invention rules

- Response schema, course aggregate formula, source dataset, selected quiz attempt/submission and empty-course shape are open in API #37 OPEN_QUESTIONS.
- Student course enrollment/published/visibility access, JWT claim-to-user mapping and 403/404 masking are unresolved.
- `course_id` int64 parse/range behavior has no catalog 400/422. Do not invent code or framework result.
- Lesson link access semantics are only stated as “after gate”; do not bypass ST-10 or expose lesson content from progress UI.
- Legacy DB candidate and V1-PILOT progress snapshot/fact model differ; no live schema or migration reconciliation.
- Study Web route/runtime and loaded state remain absent.

## 6. Verification plan

- Keep original screenshot/HTML hashes unchanged; record render provenance, dimensions and hash if Chromium render works.
- Validate marker JSON, ordered unique markers, in-bounds coordinates and exact DD element mapping; inspect annotated image visually for correct targets and unobscured content.
- Validate DD A–F, events, API statuses/fields, relative links, tracker row/count/pointers, source hashes and `git diff --check`.
- No tests or runtime API check unless requested. Run context validator only if a context page/manifest changes.

## 7. Sources

- [Screen inventory / F07](../../../list_screen.md)
- [Original screenshot](./screen.png), [HTML companion](./code.html)
- [API catalog #37](../../../../../../docs/lists/list_api.md)
- [API #37 overview](../../../../../../apps/study-server/docs/dd/37_users_me_progress_course/02_Overview.md), [request](../../../../../../apps/study-server/docs/dd/37_users_me_progress_course/03_Request.md), [response](../../../../../../apps/study-server/docs/dd/37_users_me_progress_course/04_Response.md), [open questions](../../../../../../apps/study-server/docs/dd/37_users_me_progress_course/OPEN_QUESTIONS.md)
- [AC/API index](../../../../../../apps/study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md), [AC-18 diagram](../../../../../../apps/study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio)
- [Candidate table guide](../../../../../../apps/study-server/docs/diagrams/DB_UNICA_TABLES.md), [legacy Study DDL](../../../../../../infra/postgres/study-server/DB.sql), [V1-PILOT DDL](../../../../../../infra/postgres/02_study_db.sql)
- [Current Study route inventory](../../../../../../.agents/server-study/apis/declared-routes.md), [Study Web design target](../../../../../../.agents/web-study/design.md)

## 8. Kết quả thực hiện plan

- Chrome Stable headless/CDP render `code.html` thành công: `screen_rendered.png`, 1280×916, SHA256 `ac30e06639a2002b0c2343303d6c91955be2885d925ec0a71dd16b69688f9ded`. Ảnh chỉ thể hiện HTML/CSS tĩnh; không có app/API runtime. Original `screen.png`/`code.html` hashes được kiểm tra trước khi thay đổi.
- Tạo 11 marker theo các nhóm UI thực tế và `screen_annotated.png` 1376×916; ảnh annotation đã được xem trực quan và marker đặt cạnh element, không che nội dung chính.
- Viết DD A–F với 9 event, contract #37, navigation, state matrix, security và các câu hỏi/blockers; không tự đặt progress DTO hoặc công thức AC-18.
- Static audit thành công: 11 marker unique/ordered/in-bounds ánh xạ một-một; JSON/SVG hợp lệ; 9 event; sections A–F; 21 relative link resolve; source/render hashes giữ nguyên; tracker 33/83, 50 còn thiếu, next Student ST-22 và Mentor ME-04; `git diff --check` sạch.
