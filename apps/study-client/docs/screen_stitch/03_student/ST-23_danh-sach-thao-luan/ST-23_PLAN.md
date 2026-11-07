# ST-23 — Kế hoạch chi tiết

**Screen ID:** ST-23  
**Tên:** Danh sách thảo luận (Page)  
**Route trong inventory:** `/student/discussions`  
**Actor:** Student  
**Kế hoạch:** PLAN COMPLETE — lập trước HTML render, marker map, annotated image và DD.  
**DD dự kiến:** BLOCKED — API #39 DD Draft; Student endpoint absent; access/pagination/sort/visibility/title/comments boundaries unresolved.  
**Implementation/runtime:** Study Web UNWIRED; API #39 route/module/query/test NOT_FOUND.

## 1. Mục tiêu và phạm vi phiên

- Chỉ xử lý ST-23 trong phiên này; nối logic với ST-24 create-topic và ST-25 thread detail theo inventory/F07/AC-19.
- Giữ nguyên `screen.png` và `code.html`. PNG 1280×1142 nhìn thấy gần như toàn nền trống, không đủ dùng để đọc element; HTML là prototype static có empty-state shell hợp lệ.
- Đã render `code.html` thành `screen_rendered.png` bằng Google Chrome 155 headless/CDP ở viewport 1280×1142; full document 1280×1173. Đây là HTML/CSS tĩnh, không phải Study Web runtime/API. Chỉ đánh số trên bản rendered; không sửa ảnh/HTML gốc.
- Annotate các nhóm element thực sự có trong HTML: brand/navigation, breadcrumb, heading, empty-state panel/icon/copy/CTA và footer. Filter/sort/create CTA/topic cards/pagination là expected inventory surface nhưng không có trong asset; ghi discrepancy, không tạo marker giả.
- API #39 catalog: `GET /api/v1/discussions`, Student Bearer, optional `course_id:int64`, `page:int32`, `sort:string`, `ApiEnvelope<Page<Discussion>>`; 200/401/403/500 theo danh mục. Không thêm `size` query, 404/422, hoặc gộp với public reviews API #10.
- API #39 DD `Draft — Needs Confirmation`: access/enrollment scope, page/size/order, list comments, visibility/status, `title` source, query validation và DDL nullability đều mở. Page size 20, sort values, ACTIVE/enrollment rules, comments inclusion là DERIVED proposals, không phải quyết định được duyệt.

## 2. Expected behavior

- Inventory ST-23: `/student/discussions`, AC-19, API #39; topic theo khóa học, filter/sort, nút tạo thảo luận; state `loading/empty/ready/error`; link ST-24/ST-25.
- F07: ST-23 #39 list → ST-24 #40 create hoặc ST-25 #42 thread → #41 add comment → reload #42. Không tự gộp #39 với public course reviews #10; rich-text/content type chưa chốt.
- AC-19 actor Student, precondition đăng nhập và có quyền tham gia discussion của course; postcondition topic/comment được tạo và thread cập nhật. Diagram gọi #39 list trước nhánh create/reply.
- API catalog #39 yêu cầu Student Bearer và chỉ khai báo query `course_id?`, `page?`, `sort?`; response là `ApiEnvelope<Page<Discussion>>`; không có mutation side effect trên màn hình list.

## 3. Current behavior / source trace

- `screen.png` SHA256 `7c0c2fe1b79d0c44d88d915578f295d732738e41a0579f471405652f0e366b38`, 1280×1142. Ảnh hiển thị nền sáng/trống và không có element có thể đọc/đánh số; giữ làm asset nguồn.
- `code.html` SHA256 `2812398914f2a7b35942bffa912f747ef80536091b5316335279821ca89f2ebb`. Có Student-style header/nav, breadcrumbs, title “Danh sách thảo luận”, static empty card/icon/text/link back to `/student/courses`, footer groups. Không có list/thread cards, filter/sort/create/paging controls, API call, auth guard, event handler hay data binding; phần lớn anchor dùng `#`.
- Study Web editable source/package/router absent; route inventory không phải route runtime evidence.
- Current Study Server discussion route search chỉ tìm thấy Admin #97 `/admin/discussions/reported` và #98 `/admin/discussions/{discussion_id}`. Hai endpoint dùng actor/permission khác, không thay thế Student API #39. Không có Student #39 route/module/query/test.
- Checked-in legacy `discussions` DDL có `id`, nullable `course_id`, nullable `user_id`, nullable `parent_id`, required `content`, `status` default `ACTIVE`, timestamps; không có cột `title`. Đây là source artifact, không chứng minh live schema. DB guide ghi discussion/review/reply cùng logical tree, nhưng inventory cấm nhập nhằng #39 với public reviews #10.
- AC-19/API DD #39 là design-only/draft; no runnable #39 tests. Không chạy tests hoặc gọi API trong task docs này.

## 4. Discrepancies và blockers

1. **Blank PNG vs HTML:** giữ PNG; dùng HTML render thay thế với provenance, chỉ cho static empty state.
2. **Expected list controls absent:** course filter, sort, create CTA, root topic cards, comments/counts and pagination không xuất hiện trong HTML. Không thêm thành phần/marker dựa trên tưởng tượng.
3. **API #39 not runnable:** Student route/module/query/test NOT_FOUND; Study Web route/runtime UNWIRED.
4. **Draft response/query semantics:** API #39 DD có 7 open questions. `Discussion.title` required trong catalog nhưng không có cột physical; không map title từ `content`. Query `page/sort` validation/default/size unresolved; không thêm query `size` hay error code.
5. **Access/visibility:** AC-19 yêu cầu quyền tham gia course, còn API DD enrollment ACTIVE + omitted-course scope là DERIVED. Status enum/visibility gate cũng chưa duyệt; không coi DDL default là policy.
6. **Comments payload:** API DD đề xuất nested direct ACTIVE comments trong mỗi list item; AC-19 cũng gọi #42 riêng. Chưa quyết định có trả comments trên list; ghi rõ mismatch.
7. **Create handoff:** ST-24/API #40 có `content:int64` trong catalog dù UI intent là câu hỏi/rich text; do not submit from list or invent encoding. Create CTA stays blocked until route/design/API decision.
8. **Public reviews:** API #10 là separate public course-review design; no automatic merge into Student discussions despite shared `Discussion` schema and DDL candidate.

## 5. Planned marker map

Plan for 15 marker groups in rendered static HTML, in top-to-bottom/read order:

1–2. Header brand/logo; primary Student navigation.  
3–4. Upper breadcrumb bar; page breadcrumb.  
5. Page title.  
6–10. Empty-state card; icon; heading; explanation; return-to-courses link.  
11–15. Footer brand/description; program links; community/support links; contact text; legal/copyright strip.

Each marker receives one `ST23-EL-XX` row. Element rows must state source/static status, behavior/data binding absent and event relation. Expected but absent controls stay in a “not represented in assets” blocker list, outside the numbered image-to-DD map.

## 6. Event plan

1. Route entry/session and Student/course context.
2. GET API #39 with exact optional query fields only.
3. Envelope/list/PageMeta parsing and state mapping; respect `title`/comments contract gaps.
4. Select course filter (`course_id`) — expected affordance missing; access/scope unresolved.
5. Select sort — expected affordance missing; API sort values/default unresolved.
6. Select page — expected affordance missing; page default and fixed response size unresolved.
7. Open a topic to ST-25 — no topic row/card in HTML; route param/authorization handoff unresolved.
8. Navigate to ST-24 create — create button absent; form/API #40 contract has `content:int64` conflict.
9. Return/navigation via back link, header/footer; only prototype hrefs are known.
10. Auth/access/API/network/parse failure handling, preserving catalog statuses and not mapping failure to empty.

Each event in DD will include trigger, input, ordered handling, output and exceptions, marking unsupported behavior as blocked.

## 7. Verification plan

- Verify original PNG/HTML hashes and dimensions unchanged; record `screen_rendered.png` provenance/size separately.
- Visually inspect the full rendered HTML and annotated image; adjust marker positions if any marker covers copy/controls.
- Static audit: marker order/uniqueness/bounds; one-to-one map to DD rows; SVG XML; DD sections A–F; event numbering/input-process-output-exception coverage; API #39 contract/query/status exactness; local Markdown links; tracker counts/next pointers; `git diff --check`.
- No API calls, runtime verification or tests (not requested).
- No `.agents/` context changes are planned; run context validator only if a context page/manifest actually changes.

## 8. Sources

- [Screen inventory/F07](../../../list_screen.md); [original screen.png](./screen.png); [HTML companion](./code.html).
- [API catalog](../../../../../../docs/lists/list_api.md); [API #39 overview](../../../../../../apps/study-server/docs/dd/39_discussions/02_Overview.md), [request](../../../../../../apps/study-server/docs/dd/39_discussions/03_Request.md), [response](../../../../../../apps/study-server/docs/dd/39_discussions/04_Response.md), [data mapping](../../../../../../apps/study-server/docs/dd/39_discussions/05_Data_Mapping.md), [open questions](../../../../../../apps/study-server/docs/dd/39_discussions/OPEN_QUESTIONS.md).
- [AC/API index](../../../../../../apps/study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md); [AC-19 diagram](../../../../../../apps/study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio); [DB table guide](../../../../../../apps/study-server/docs/diagrams/DB_UNICA_TABLES.md); [legacy Study DDL](../../../../../../infra/postgres/study-server/DB.sql).
- [Current declared routes](../../../../../../.agents/server-study/apis/declared-routes.md); [Study Web design target](../../../../../../.agents/web-study/design.md).

## 9. Kết quả thực hiện và kiểm tra

- Giữ nguyên `screen.png` (1280×1142, SHA256 `7c0c2fe1b79d0c44d88d915578f295d732738e41a0579f471405652f0e366b38`) và `code.html` (SHA256 `2812398914f2a7b35942bffa912f747ef80536091b5316335279821ca89f2ebb`).
- Tạo `screen_rendered.png` từ `code.html` bằng Chrome 155 headless/CDP, kích thước 1280×1173, SHA256 `7f18526b721176028e58b2417df7dd43a5a6cfa83ac8df29eefd2724f7197e6a`; `screen_annotated.png` 1392×1213.
- Hoàn tất marker JSON và SVG overlay với 15 marker tuần tự, duy nhất, trong bounds; 15 marker khớp 1:1 với 15 dòng element trong DD. Kiểm tra hình ảnh trực quan: nhãn rõ và không che nội dung quan trọng.
- DD có đủ phần A–F và 10 event tuần tự; mỗi event ghi trigger, input, xử lý, output và ngoại lệ. Các query/status/error code khớp catalog #39; link nội bộ resolve; JSON/SVG parse hợp lệ.
- Static audit: PASS. Hash/dimensions, marker map/bounds, event/section coverage, API contract references, local links và SVG XML đều đạt. `git diff --check`: PASS. Không chạy tests, API calls hoặc runtime verification.
- Trạng thái kết quả: `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`. Blockers ghi tại DD §A.5/§F và worklog; không ảnh hưởng ST-24/25 ngoài contract handoff đã nêu.
