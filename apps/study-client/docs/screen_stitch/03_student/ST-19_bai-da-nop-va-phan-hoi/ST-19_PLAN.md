# ST-19 — Plan chi tiết

**Screen ID:** ST-19
**Tên:** Bài đã nộp và phản hồi (Trang)
**Route trong inventory:** `/student/submissions/:submissionId`
**Actor:** Student
**Kế hoạch:** PLAN COMPLETE
**DD dự kiến:** BLOCKED bởi API #36 Student route/source chưa được wire và các policy mapping/access chưa được chốt
**Implementation/runtime:** Study Web hiện `UNWIRED`; route, app source và runtime chưa có để xác minh.

## 1. Mục tiêu và giới hạn

- Đặc tả duy nhất ST-19 trong phiên này, nối luồng AC-17 từ ST-18 sang thông tin submission và các màn hình ST-17/ST-20 liên quan.
- Tách expected behavior trong inventory/API/AC khỏi current source, prototype assets, API DD và trạng thái runtime.
- Bảo toàn `screen.png` và `code.html`. Dùng PNG loaded mockup làm ảnh nguồn cho marker; HTML unavailable fallback là trạng thái khác, không dùng để render thay thế.
- Lập bản đồ marker có thứ tự đọc cho toàn bộ cụm UI nhìn thấy; mỗi marker ánh xạ một-một với một dòng element trong DD. Cụm lặp cùng vai trò có thể chung một marker nếu bảng liệt kê rõ các phần con.
- Đặc tả events, API boundary, lỗi, states, điều hướng và câu hỏi chặn mà không tự quyết định disclosure điểm/feedback, quyền sở hữu, mapping asset, trạng thái chấm hay ID handoff.

## 2. Bằng chứng và source cần giữ riêng

### Expected behavior

- Inventory ST-19: GET API #36 theo submission ID; hiển thị thời điểm nộp, file, trạng thái chấm, score/feedback khi có; không tự hiển thị `GRADED` nếu nguồn chỉ là `SUBMITTED`.
- Luồng F06: ST-17 → ST-18 upload #34 nếu cần → POST #35 → nhận `submission_id` → ST-19 đọc #36.
- API catalog #36: `GET /api/v1/submissions/{submission_id}`, Student Bearer, path `submission_id:int64!`, `ApiEnvelope<Submission>`, success 200 `DESIGN_RESOURCE_RETRIEVED`, errors đúng 401/403/404/500.
- API #36 DD còn `Draft — Needs Confirmation`: access predicate/403-vs-404, score/feedback disclosure, `files[]` mapping, status lifecycle, timestamp semantics, path parse errors và schema baseline chưa được quyết định.

### Current behavior cần thể hiện trong DD

- PNG là một mockup loaded/graded với header, thông tin submission, điểm tổng, rubric, mentor feedback, file/link cards, skill-index strip và nút quay lại/đi tiếp. Các tên người dùng/mentor, điểm, nhận xét, timestamps, URL, trạng thái graded, ảnh preview và certification labels đều là nội dung mẫu, không phải runtime data.
- `code.html` là static Guest/unavailable fallback với dòng “Chưa có thông tin bài nộp để hiển thị.” và link `/student/courses`; có Tailwind CDN/config scripts và remote font imports nhưng không có form, app API call hoặc event handler và không biểu diễn loaded PNG.
- Visual source discrepancy: HTML dùng Plus Jakarta Sans, remote Google Fonts/Tailwind CDN và content width tối đa 1440px; Study Web design target yêu cầu Inter/system stack, không thêm remote font import và content width khoảng 1120px. Đây là design debt của mockup, không phải runtime behavior.
- Study Web hiện không có editable app source/package/router/Student routes; ignored dist chỉ có `/`. Không có runtime của ST-19 được xác minh.
- API #36 hiện chỉ có catalog/DD. Không tìm thấy Student route/module/query/test trong Study Server source. Mentor API #55 là endpoint riêng cho Mentor và không thay thế API #36.
- Checked-in `assignment_submissions` DDL là design evidence: có candidate score/feedback/status/submitted_at và một nullable `file_url`; logical `Submission` yêu cầu `files: UploadAsset[]`. Đây không phải live schema, và mapping/access/status semantics chưa đủ.

## 3. Source trace và quyết định đặc tả

```text
Expected: ST-18 success → submission ID handoff (inventory gọi submission_id;
  API #35 DD draft trả data.id) → ST-19 GET #36 → map Submission → receipt/grade UI.
Current: ST-19 web route absent; Student API #36 route/module/test absent.
  Mentor API #55 exists but has a different role/path and cannot serve this page.
  API #36 contract exists only in catalog/DD; no runtime query, response or access rule.
```

- Giữ mismatch `submission_id` so với draft #35 `data.id`; không tự chọn route param source.
- Chỉ hiển thị field từ response API đã được chốt; không suy score/feedback từ mockup hoặc từ Mentor API.
- Không tạo link tài liệu, URL public/signed hay preview từ `file_url`; API #36 `files[]`/API #34 asset association chưa được chốt.
- Không tạo API/event booking cho “Xem 3 Line Comments”, “Đặt lịch 1-on-1” hoặc “Xem đồ án tiếp theo”; các nút là mockup actions chưa có contract/destination.

## 4. Danh sách element dự kiến

Marker IDs theo thứ tự đọc từ trên xuống; cụm lặp được nêu cụ thể trong DD.

| Marker range | Cụm element |
|---|---|
| 01–09 | Brand, search, global navigation, notification/profile, breadcrumb và submission ID chip |
| 10–16 | Submission status/course/title, timestamps, grader identity, overall score card |
| 17–31 | Rubric heading/coefficient, summary grade ring/text, metric labels, four rubric rows với điểm, progress và helper copy |
| 32–39 | Mentor review header/date, avatar/identity/credentials, feedback quotation, comments và meeting buttons |
| 40–47 | Stored submission files heading/version, ba file/resource rows, actions và preview image |
| 48–50 | Skill index icon, label/value and trend chart |
| 51–54 | Completion callout, return-to-progress button and next-assignment button |
| 55–58 | Footer brand/description, certification badges, link groups, copyright/platform attribution |

## 5. Event và luồng dữ liệu cần đặc tả

1. **ST19-EV-01 Load submission:** đọc `submissionId` từ route theo thiết kế; validate là path int64 theo catalog, nhưng positivity/invalid parse contract chưa có; gọi GET #36 bằng Student Bearer. Route/API hiện chưa được wire.
2. **ST19-EV-02 Map receipt/status:** chỉ sau 200 `DESIGN_RESOURCE_RETRIEVED` mới ánh xạ logical `Submission`; status enum và timestamp format vẫn cần quyết định. Không nâng `SUBMITTED` thành `GRADED` do score UI mẫu.
3. **ST19-EV-03 Render score/feedback:** schema cho phép score/feedback optional; thời điểm công bố và omit/null behavior cho Student chưa được chốt. Hiển thị theo field/policy đã duyệt; nếu thiếu policy thì DD ghi blocker.
4. **ST19-EV-04 Render file list/open file:** logical `files[]` có UploadAsset shape; mapping vật lý từ `file_url`, association với #34 và URL access policy unresolved. Không suy ra ba file card mẫu từ response hiện có.
5. **ST19-EV-05 Breadcrumb/back to ST-17 or ST-20:** inventory links screen ST-17/ST-20; screenshot back CTA trỏ ST-20. Submission/assignment/course identifiers và return policy chưa được xác nhận.
6. **ST19-EV-06 Comments action:** screenshot button gợi ý line comments/PR. Không có API hoặc contract field trong #36; destination/action phải chờ product contract.
7. **ST19-EV-07 One-on-one meeting action:** screenshot button không có booking API/route trong ST-19 contract; không tạo event side effect.
8. **ST19-EV-08 Next assignment action:** CTA gợi ý assignment tiếp theo, nhưng ID/order/access/destination không có trong #36. Không tự dựng route/path.
9. **ST19-EV-09 Global/footer navigation:** prototype anchors/placeholders không phải Study Web route runtime; destinations/auth policy hiện chưa wire.
10. **ST19-EV-10 Handle load errors:** theo catalog giữ đúng 401/403/404/500 codes; 403-vs-404 masking unresolved; không thêm 400/422 cho malformed ID khi catalog chưa cập nhật; network/timeout client UI policy chưa có contract.

## 6. Blockers

- Student API #36 route/module/query/test hiện `NOT_FOUND`; API DD không phải current behavior.
- Student resource access predicate, owner/enrollment rule, 403-vs-404 và row masking chưa chốt.
- Score/feedback disclosure timing và null/omit policy chưa chốt; mockup ghi `GRADED` và feedback cụ thể.
- `files[]`/UploadAsset không map được trực tiếp từ candidate scalar `file_url`; API #34 association, metadata and URL security chưa chốt.
- SubmissionStatus enum/transitions, timezone/serialization và `assignment_id`/`user_id` nullability chưa thống nhất; DDL không phải live-schema proof.
- Invalid `submission_id` parse response chưa có trong error catalog.
- API #35 DD response `data.id` và inventory handoff `submission_id` chưa khớp; direct-entry, refresh and return routing chưa wire.
- Mockup actions for comments, meeting, next assignment and skill index have no source-backed API/destination/data contract.
- PNG/HTML state mismatch; Study Web remains `UNWIRED`.

## 7. Kiểm tra dự kiến

- Lưu SHA-256 và kích thước nguồn; xác minh PNG gốc và HTML không đổi.
- Tạo JSON marker map, SVG gutter overlay và `screen_annotated.png`; đảm bảo marker theo thứ tự, unique, tọa độ nằm trong ảnh, map khớp từng dòng DD; mở ảnh annotated để kiểm tra trực quan.
- Đối chiếu catalog/API #36 DD, AC-17, AC-23, candidate DDL, Mentor #55 current source, Study Web route/source status và ST-18 handoff.
- Kiểm tra sections A–F, IDs event liên tục, liên kết cục bộ, tracker/counters/next pointer và `git diff --check`.
- Không chạy tests hoặc runtime checks trong task docs này.

## 8. Nguồn

- [Screen inventory and F06](../../../list_screen.md)
- [Original screenshot](./screen.png), [HTML companion](./code.html)
- [API catalog](../../../../../../docs/lists/list_api.md)
- [API #36 DD overview](../../../../../../apps/study-server/docs/dd/36_submissions_detail/02_Overview.md), [open questions](../../../../../../apps/study-server/docs/dd/36_submissions_detail/OPEN_QUESTIONS.md)
- [AC-17 diagram](../../../../../../apps/study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio), [AC-23 diagram](../../../../../../apps/study-server/docs/diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio)
- [Mentor API #55 current view](../../../../../../apps/study-server/app/modules/mentor/api_55_mentor_submissions_detail/view.py)
- [Candidate DDL](../../../../../../infra/postgres/study-server/DB.sql), [Study Server route inventory](../../../../../../.agents/server-study/apis/declared-routes.md)
- [Study Web design target](../../../../../../.agents/web-study/design.md)

## 9. Re-audit nguồn trước khi hoàn tất DD (2026-11-07)

- Giữ scope một màn hình ST-19. Đã đọc lại inventory/F06, AC-17, API catalog #36, API #36 Draft DD/open questions, API #35 response draft, Study Server route inventory/current source, Study Web design target và asset ST-19.
- Expected/current separation được giữ nguyên: catalog/AC quy định ý định Student receipt; current Student API #36 route/module/query/test và Study Web editable source/router không có trong checkout. API #55 hiện tại chỉ là Mentor route `/api/v1/mentor/submissions/{submission_id}` với auth/owner check riêng, không thay thế #36.
- `code.html` có script tải Tailwind và script cấu hình Tailwind; không tìm thấy form hoặc handler/API nghiệp vụ. Sửa mô tả “không có script” thành “không có script tương tác/API”. HTML có remote Google Fonts, Plus Jakarta Sans và max-width 1440px, khác với Study Web guide.
- API #36 contract giữ đúng `GET /api/v1/submissions/{submission_id}`, Student Bearer, `ApiEnvelope<Submission>`, 200 và error set 401/403/404/500. Access/403-vs-404, grade disclosure, files mapping, status/timestamp/schema, invalid path và #35 `data.id` → inventory `submission_id` vẫn mở; không tự chọn policy.
- Legacy DDL `assignment_submissions` cho phép NULL ở `assignment_id`/`user_id`, có một `file_url`, score/feedback nullable và `submitted_at TIMESTAMP`; V1-PILOT `02_study_db.sql` không khai báo business assignment/submission/upload tables. Đây là checked-in artifacts, không phải bằng chứng live schema.

## 10. Kết quả kiểm tra tĩnh (2026-11-07)

- `screen.png` 1241×1600, SHA-256 `359e259cf97a8880009e8f9324466a3437f932f0a00dc80532d2d3aeffacca57`; `code.html` 8,812 bytes, SHA-256 `142253c74400da2f37fb9832d6cefcf93d3f74c6dbb4802dfc575b2d2106cab2`; cả hai asset nguồn được giữ nguyên trong phiên này.
- `screen_annotated.png` 1401×1600; đã xem ảnh trực tiếp. Marker map/SVG/DD có 58 marker tuần tự, target tọa độ duy nhất và nằm trong ảnh, 58 element ID khớp một-một, 58 SVG groups khớp nhãn/marker và tọa độ badge. Badge có khoảng cách tâm tối thiểu 25px.
- DD có đủ A–F, 13 event liên tục với element/type/precondition, 58 hàng element và ref hợp lệ; local Markdown links: DD 18/18, plan 12/12 đều resolve.
- Đối chiếu tĩnh hiện tại: 83 Screen ID duy nhất khớp 83 screen folder; 82/83 folder có đủ sáu artifact cốt lõi; ST-19 đủ bộ. Không chạy application tests, browser/runtime hay live DB/storage checks.
- Kết quả screen: `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED` do các policy/contract/source blockers ở §6.
