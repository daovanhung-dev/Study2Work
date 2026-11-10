# ST-12 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [ST-12_markers.json](../../screen_stitch/03_student/ST-12_tai-lieu-kem-bai-hoc/ST-12_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `ST-12-EL-001` | `ST12-EL-01` | Study2Work LMS brand and the primary navigation in the top header |
| #2 | `ST-12-EL-002` | `ST12-EL-02` | Hard-coded learner name, role label and avatar at the top-right |
| #3 | `ST-12-EL-003` | `ST12-EL-03` | Breadcrumb from home through learner courses and ST-11 to the current screen |
| #4 | `ST-12-EL-004` | `ST12-EL-04` | Proposed route label at the right side of the breadcrumb row |
| #5 | `ST-12-EL-005` | `ST12-EL-05` | ST-12 Resource Panel and DESIGN_ONLY badges in the hero |
| #6 | `ST-12-EL-006` | `ST12-EL-06` | Tài liệu kèm bài học heading and the explanatory subtitle |
| #7 | `ST-12-EL-007` | `ST12-EL-07` | Zero Information Disclosure Enforced status card in the hero |
| #8 | `ST-12-EL-008` | `ST12-EL-08` | Folder icon above the unavailable-resource message |
| #9 | `ST-12-EL-009` | `ST12-EL-09` | Centralized access-control badge above the empty-state heading |
| #10 | `ST-12-EL-010` | `ST12-EL-10` | Empty/unavailable heading and privacy explanation in the main panel |
| #11 | `ST-12-EL-011` | `ST12-EL-11` | Button-style link labelled Quay lại trình học bài (ST-11) |
| #12 | `ST-12-EL-012` | `ST12-EL-12` | Static E2E, no-public-metadata and one-time-token claims below the CTA |
| #13 | `ST-12-EL-013` | `ST12-EL-13` | Heading for the connection capability status panel |
| #14 | `ST-12-EL-014` | `ST12-EL-14` | Static label claiming automatic refresh every 30 seconds |
| #15 | `ST-12-EL-015` | `ST12-EL-15` | Schema mismatch and Type: Lesson status tile in the left column |
| #16 | `ST-12-EL-016` | `ST12-EL-16` | Design Only and Pending Auth status tile in the right column |
| #17 | `ST-12-EL-017` | `ST12-EL-17` | Hand-off Technical Notes heading and frontend-engine subtitle |
| #18 | `ST-12-EL-018` | `ST12-EL-18` | Warning not to open URLs outside an approved security policy |
| #19 | `ST-12-EL-019` | `ST12-EL-19` | Warning not to invent file names, extensions, sizes or URLs |
| #20 | `ST-12-EL-020` | `ST12-EL-20` | Note about WCAG 2.1 AA and visible keyboard focus |
| #21 | `ST-12-EL-021` | `ST12-EL-21` | Note naming the Ocean brand color #0B5F8A |
| #22 | `ST-12-EL-022` | `ST12-EL-22` | ST-12 v2.4 and static Valid Spec label at the bottom of hand-off panel |
| #23 | `ST-12-EL-023` | `ST12-EL-23` | Help title and copy about contacting the instructor or teaching assistant |
| #24 | `ST-12-EL-024` | `ST12-EL-24` | Link inviting the learner to visit the discussion forum |
| #25 | `ST-12-EL-025` | `ST12-EL-25` | Static Study2Work LMS copyright text at lower-left |
| #26 | `ST-12-EL-026` | `ST12-EL-26` | Static WCAG 2.1 AA Compliant badge in the footer |
| #27 | `ST-12-EL-027` | `ST12-EL-27` | Terms, privacy and help anchors at lower-right |

## 3. Đặc tả từng element

### Trích từ DD nguồn: C. Đặc tả element

`Visible in prototype` mô tả ảnh/HTML tĩnh, không khẳng định runtime. Nhãn chính sách, trạng thái và nội dung kỹ thuật dưới đây là copy trong mockup trừ khi có nguồn backend cụ thể.

| # / Element ID | Tên, loại, vị trí, mục đích | Thuộc tính/nguồn/trạng thái | Sự kiện |
|---|---|---|---|
| #1 `ST12-EL-01` | Thương hiệu Study2Work LMS và navigation ở header. | Static HTML anchors; các mục Trang chủ/Khóa học của tôi/Tiến độ/Thảo luận/Thông báo dùng `href="#"`. Không phải current nav. | `ST12-EV-05`; route target chưa có. |
| #2 `ST12-EL-02` | Tóm tắt người học và avatar ở góc phải header. | Tên “Nguyễn Văn A”, role “Học viên” và icon được hard-code; không có API/session mapping. | Không có event/control được xác nhận. |
| #3 `ST12-EL-03` | Breadcrumb Trang chủ → Khóa học của tôi → ST-11 → Tài liệu kèm bài học. | Static anchors và current text; không chứa runtime IDs. | `ST12-EV-05`; `lessonId` handoff chưa có. |
| #4 `ST12-EL-04` | Route badge ở đầu nội dung. | Hiển thị chuỗi `/student/lessons/:lessonId/resources`; route label là design metadata. | Không có event. |
| #5 `ST12-EL-05` | Badge `ST-12 RESOURCE PANEL` và `DESIGN_ONLY (D)`. | Static label, không phải status API/deployment. | Không có event. |
| #6 `ST12-EL-06` | H1 “Tài liệu kèm bài học” và mô tả purpose. | Static Vietnamese copy; không lấy từ API. | Không có event. |
| #7 `ST12-EL-07` | Thẻ “Zero Information Disclosure Enforced”. | Static security claim. Current #12 source trả `name/type/url` public; không chứng minh zero disclosure hoặc policy enforcement. | Không có event; cần duyệt/cập nhật copy. |
| #8 `ST12-EL-08` | Icon folder ở empty/fallback panel. | Trang trí; không có accessibility alternative/status semantics được xác minh. | Không có event. |
| #9 `ST12-EL-09` | Badge “Chính sách kiểm soát truy cập tập trung”. | Static copy; chưa có policy/service source hỗ trợ. | Không có event. |
| #10 `ST12-EL-10` | Empty/unavailable heading và giải thích về tài liệu hoặc phân quyền đang cấu hình. | Copy cố định; không phân biệt `200 empty`, 401/403, 404, 500, network error hay setup issue. Không có `Resource` fields. | Trạng thái dự kiến do `ST12-EV-01`; hiện không có mapper. |
| #11 `ST12-EL-11` | CTA “Quay lại trình học bài (ST-11)”. | Anchor button-style, cao 48px trong HTML; `data-path="student-lessons-lessonId"`, `href="#"`. Không có ID/state binding. | `ST12-EV-03`; hiện chỉ là placeholder anchor. |
| #12 `ST12-EL-12` | Dải claims “Chuẩn mã hóa E2E”, “Không công khai metadata”, “Token xác thực một lần”. | Ba static claims, không có backend/identity/storage evidence; không được ghi như tính năng đã triển khai. | Không có event. |
| #13 `ST12-EL-13` | Heading “Trạng thái kiểm định khả năng kết nối”. | Static section title/icon; không có diagnostic API/source. | Không có event. |
| #14 `ST12-EL-14` | Badge “Tự động làm mới mỗi 30s”. | Static text. Không có `setInterval`, timer, request hoặc focus/visibility behavior trong HTML. | Không tạo polling event nếu chưa có yêu cầu/cost/error policy. |
| #15 `ST12-EL-15` | Thẻ API #26: “Schema Mismatch (Blocked)”, “Type: Lesson”. | Phản ánh mismatch catalog/DD, không phải runtime health check. Catalog: Student Bearer; GET; `lesson_id:int64!`; response `ApiEnvelope<Lesson>`; declared 200/401/403/404/500. Runtime route/module/test không tìm thấy. | `ST12-EV-01`; không thể đọc dữ liệu hiện tại. |
| #16 `ST12-EL-16` | Thẻ API #12: “Design Only (Locked)”, “Pending Auth”. | Nhãn `Pending Auth` sai với current #12 route/catalog public/no Bearer. API DD còn Draft; source trả direct stored URL và thiếu auth/visibility/signer. | `ST12-EV-02`; không khẳng định auth pending là server behavior. |
| #17 `ST12-EL-17` | Header Hand-off Technical Notes và subtitle. | Static annotation hướng frontend, không cấu hình/capability contract. | Không có event. |
| #18 `ST12-EL-18` | Note cấm mở URL ngoài chính sách bảo mật. | Design recommendation; allowlist domain, URL parser, scheme, redirects và behavior chưa định nghĩa. | Liên quan `ST12-EV-02`; chưa đủ để triển khai an toàn. |
| #19 `ST12-EL-19` | Note không giả lập tên/extension/size/URL. | Quy tắc prototype phù hợp yêu cầu không bịa dữ liệu; metadata thật chưa có do #26 contract/source thiếu. | Áp dụng khi thiết kế resource item; hiện không có item. |
| #20 `ST12-EL-20` | Note WCAG 2.1 AA/focus visible. | Claim trên mockup chưa được kiểm thử. `.agents/web-study/design.md` yêu cầu contrast, focus-visible, keyboard order và hit target tối thiểu 44px. | Không có event; tiêu chí UX cho implementation. |
| #21 `ST12-EL-21` | Note Ocean brand và màu `#0B5F8A`. | Khớp token `ocean-primary` của Study Web guide ở icon/note; các màu Tailwind của HTML còn có `#004AC6`/`#2563EB`, cần thống nhất khi triển khai. | Không có event. |
| #22 `ST12-EL-22` | Footer panel tag `ST-12 v2.4` và `Valid Spec`. | Static version/validity claim, không phải approval record. Tài liệu DD hiện BLOCKED. | Không có event; không dùng làm trạng thái DD. |
| #23 `ST12-EL-23` | Help card title/copy mời liên hệ giảng viên/trợ giảng. | Static content; không có recipient, course context hoặc service/link logic. | Liên quan `ST12-EV-04`; không có request/action riêng. |
| #24 `ST12-EL-24` | Link “Truy cập Diễn đàn Thảo luận”. | `data-path="thao-luan"`, `href="#"`; không có `courseId`/destination. | `ST12-EV-04`; destination cần xác nhận. |
| #25 `ST12-EL-25` | Footer copyright “© 2025 Study2Work LMS”. | Static copy; không có nguồn cấu hình năm. | Không có event. |
| #26 `ST12-EL-26` | Badge “WCAG 2.1 AA Compliant”. | Static claim; chưa có runtime accessibility audit. | Không có event. |
| #27 `ST12-EL-27` | Nhóm Điều khoản dịch vụ/Chính sách bảo mật/Trợ giúp. | Ba anchors `href="#"`, `data-path` tĩnh; destination chưa được wire. | `ST12-EV-05`; không suy ra route. |

## 4. Conditional UI & state variations
- States theo inventory: empty/loading/available/forbidden
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/03_student/ST-12_tai-lieu-kem-bai-hoc/ST-12.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
