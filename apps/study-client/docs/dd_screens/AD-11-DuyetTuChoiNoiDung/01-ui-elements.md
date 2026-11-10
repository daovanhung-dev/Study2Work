# AD-11 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [AD-11_markers.json](../../screen_stitch/05_admin/AD-11_duyet-tu-choi-noi-dung/AD-11_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `AD-11-EL-001` | `not supplied in marker JSON` | Study2Work Admin brand |
| #2 | `AD-11-EL-002` | `not supplied in marker JSON` | Admin navigation: Tổng quan |
| #3 | `AD-11-EL-003` | `not supplied in marker JSON` | Admin navigation: Người dùng |
| #4 | `AD-11-EL-004` | `not supplied in marker JSON` | Admin navigation: Khóa học và Nội dung |
| #5 | `AD-11-EL-005` | `not supplied in marker JSON` | Active navigation: Kiểm duyệt |
| #6 | `AD-11-EL-006` | `not supplied in marker JSON` | Admin navigation: Báo cáo |
| #7 | `AD-11-EL-007` | `not supplied in marker JSON` | Static SYSTEM NORMAL badge |
| #8 | `AD-11-EL-008` | `not supplied in marker JSON` | Notification button without handler |
| #9 | `AD-11-EL-009` | `not supplied in marker JSON` | Static Admin identity and avatar |
| #10 | `AD-11-EL-010` | `not supplied in marker JSON` | Global breadcrumb trail |
| #11 | `AD-11-EL-011` | `not supplied in marker JSON` | Static RBAC assurance badge |
| #12 | `AD-11-EL-012` | `not supplied in marker JSON` | Moderation breadcrumb |
| #13 | `AD-11-EL-013` | `not supplied in marker JSON` | Pending queue breadcrumb |
| #14 | `AD-11-EL-014` | `not supplied in marker JSON` | Current detail breadcrumb |
| #15 | `AD-11-EL-015` | `not supplied in marker JSON` | Back to AD-10 link with href hash |
| #16 | `AD-11-EL-016` | `not supplied in marker JSON` | Static quality-review portal kicker |
| #17 | `AD-11-EL-017` | `not supplied in marker JSON` | Review and approval page title |
| #18 | `AD-11-EL-018` | `not supplied in marker JSON` | Static review-page subtitle |
| #19 | `AD-11-EL-019` | `not supplied in marker JSON` | Static control-lock icon |
| #20 | `AD-11-EL-020` | `not supplied in marker JSON` | Static approval-gate status citing APIs 79 and 80 |
| #21 | `AD-11-EL-021` | `not supplied in marker JSON` | Content preview card header |
| #22 | `AD-11-EL-022` | `not supplied in marker JSON` | Preview status: no Content ID linked |
| #23 | `AD-11-EL-023` | `not supplied in marker JSON` | Static empty preview video/document icon |
| #24 | `AD-11-EL-024` | `not supplied in marker JSON` | Empty preview heading |
| #25 | `AD-11-EL-025` | `not supplied in marker JSON` | Instruction to choose an item from AD-10 |
| #26 | `AD-11-EL-026` | `not supplied in marker JSON` | Static secure player and SCORM/PDF decoder claim |
| #27 | `AD-11-EL-027` | `not supplied in marker JSON` | Publishing and copyright metadata card heading |
| #28 | `AD-11-EL-028` | `not supplied in marker JSON` | Content title placeholder |
| #29 | `AD-11-EL-029` | `not supplied in marker JSON` | Author or lecturer placeholder |
| #30 | `AD-11-EL-030` | `not supplied in marker JSON` | Course placeholder |
| #31 | `AD-11-EL-031` | `not supplied in marker JSON` | Submission date placeholder |
| #32 | `AD-11-EL-032` | `not supplied in marker JSON` | Content ID NULL placeholder |
| #33 | `AD-11-EL-033` | `not supplied in marker JSON` | Review version N/A placeholder |
| #34 | `AD-11-EL-034` | `not supplied in marker JSON` | Review decision card heading |
| #35 | `AD-11-EL-035` | `not supplied in marker JSON` | Locked decision badge |
| #36 | `AD-11-EL-036` | `not supplied in marker JSON` | Rejection reason or comment label marked optional |
| #37 | `AD-11-EL-037` | `not supplied in marker JSON` | Disabled rejection reason textarea |
| #38 | `AD-11-EL-038` | `not supplied in marker JSON` | Static warning about ownership policy |
| #39 | `AD-11-EL-039` | `not supplied in marker JSON` | Disabled approve-publish button |
| #40 | `AD-11-EL-040` | `not supplied in marker JSON` | Disabled reject-or-request-changes button |
| #41 | `AD-11-EL-041` | `not supplied in marker JSON` | Static three-step process claim citing API 81 |
| #42 | `AD-11-EL-042` | `not supplied in marker JSON` | Standard evaluation criteria card heading |
| #43 | `AD-11-EL-043` | `not supplied in marker JSON` | Static Rubric v2 badge |
| #44 | `AD-11-EL-044` | `not supplied in marker JSON` | Checked copyright criterion |
| #45 | `AD-11-EL-045` | `not supplied in marker JSON` | Checked video resolution criterion |
| #46 | `AD-11-EL-046` | `not supplied in marker JSON` | Checked practice-material criterion |
| #47 | `AD-11-EL-047` | `not supplied in marker JSON` | Contradictory 0-of-3 criteria loaded progress |
| #48 | `AD-11-EL-048` | `not supplied in marker JSON` | Footer copyright, privacy, RBAC, and support links |

## 3. Đặc tả từng element

### Trích từ DD nguồn: C. Thuộc tính từng phần tử

| # | Thành phần / vị trí trên ảnh nguồn (px) | Current asset/source | Trạng thái / dữ liệu | Sự kiện |
|---:|---|---|---|---|
| 1 | Brand Study2Work Admin, `(55,35)` | Logo/wordmark viết trong HTML. | Tĩnh; không chứng minh tenant/role. | EV-08 |
| 2 | Nav “Tổng quan”, `(350,35)` | Anchor `href="#"`. | Không có route handler. | EV-08 |
| 3 | Nav “Người dùng”, `(480,35)` | Anchor `href="#"`. | Không điều hướng. | EV-08 |
| 4 | Nav “Khóa học & Nội dung”, `(648,35)` | Anchor `href="#"`. | Tĩnh. | EV-08 |
| 5 | Nav “Kiểm duyệt” active, `(828,35)` | Active styling; anchor hash. | Không chứng minh route hiện hành. | EV-08 |
| 6 | Nav “Báo cáo”, `(945,35)` | Anchor `href="#"`. | Không có destination. | EV-08 |
| 7 | `SYSTEM NORMAL`, `(1135,35)` | Static status badge. | Không health API/monitoring evidence. | EV-08 |
| 8 | Notification bell, `(1255,35)` | Button không handler. | Không unread count/read API. | EV-08 |
| 9 | Admin identity/avatar, `(1520,35)` | Text/avatar tĩnh. | Không lấy từ JWT/profile. | EV-08 |
| 10 | Breadcrumb hệ thống, `(510,92)` | Breadcrumb shell tĩnh. | Không route state. | EV-08 |
| 11 | “Chuẩn xác thực RBAC”, `(1338,92)` | Static copy. | Không chứng minh auth/RBAC enforcement. | EV-08 |
| 12 | Breadcrumb “Kiểm duyệt đào tạo”, `(80,195)` | Breadcrumb text. | Không handler. | EV-08 |
| 13 | Breadcrumb “Hàng đợi chờ duyệt”, `(690,172)` | Breadcrumb text. | Hướng về AD-10 nhưng chưa có URL. | EV-08 |
| 14 | Crumb “Thẩm định nội dung”, `(550,195)` | Current-page chip tĩnh. | Không route source. | EV-08 |
| 15 | Back “Quay lại hàng đợi… (AD-10)”, `(1548,172)` | Anchor `href="#"`. | Không truyền filter/page/history. | EV-08 |
| 16 | Kicker “Cổng kiểm định chất lượng đào tạo”, `(365,238)` | Static text. | Không có moderation service/status source. | EV-08 |
| 17 | H1 “Thẩm định và phê duyệt nội dung bài giảng”, `(790,276)` | Static title. | Presentation only. | EV-08 |
| 18 | Subtitle mô tả preview/quyết định xuất bản, `(970,319)` | Static text. | “Xuất bản” vượt hành vi #80 local. | EV-08 |
| 19 | Lock-control icon, `(1165,301)` | Decorative icon. | Không phải state/API result. | EV-08 |
| 20 | “Cổng phê duyệt đang khóa (API #79/#80)”, `(1510,321)` | Static badge/copy. | Không có server gate response; ownership policy claim chưa có source. | EV-08 |
| 21 | Preview card title, `(520,403)` | Static header. | Chưa có preview caller/renderer. | EV-02 |
| 22 | Badge “Chưa liên kết ID”, `(1000,403)` | Static empty-state label. | Không bind route param. | EV-01 |
| 23 | Empty preview media/document icon, `(610,580)` | Decorative Material icon. | Không có `<video>`, iframe hoặc document renderer. | EV-02 |
| 24 | Empty heading, `(770,677)` | “Chưa có nội dung thẩm định được chọn”. | Static; AD-10 selection chưa được nối. | EV-01 |
| 25 | Instruction chọn item từ AD-10, `(850,722)` | Static paragraph. | Không handoff/click action. | EV-01 |
| 26 | Claim secure video + SCORM/PDF decoder, `(930,800)` | Static info strip. | Không source cho secure media, decoder hay `contentId` initialization. | EV-02 |
| 27 | Metadata card heading, `(750,967)` | “Thông tin xuất bản & Bản quyền”. | Static section. | EV-03 |
| 28 | Content title field, `(475,1080)` | Label + `--`. | #79 `data.title` available when populated; no current binding. | EV-03 |
| 29 | Author/lecturer field, `(985,1080)` | Label + `--`. | Không có author field/lookup trong #79. | EV-03 |
| 30 | Course field, `(475,1164)` | Label + `--`. | #79 có `course_id`; không có course name. | EV-03 |
| 31 | Submitted date field, `(985,1164)` | Label + `--`. | Không có submitted timestamp trong #79. | EV-03 |
| 32 | Content ID `NULL`, `(550,1238)` | Static string. | #79 trả `data.id:int64`; NULL không phải server value evidence. | EV-03 |
| 33 | Review version `N/A`, `(1000,1250)` | Static string. | #79 không trả version/revision ID. | EV-03 |
| 34 | Decision card heading, `(1395,403)` | Static “Quyết định kiểm duyệt”. | Chưa có form state. | EV-04–EV-06 |
| 35 | Badge “Khóa”, `(1508,420)` | Static badge. | Disabled controls được ghi trong HTML; không có policy API. | EV-04–EV-06 |
| 36 | Reason label + “Tùy chọn”, `(1068,481)` | Static `<label>`. | Conflicts with #81 required body field. | EV-04 |
| 37 | `#review-comments` textarea, disabled, `(1508,560)` | `rows=4`, placeholder copy, no `name`/validation. | Không nhận input; length/trim policy chưa có. | EV-04 |
| 38 | Ownership-policy warning, `(1508,702)` | Static alert copy. | Không có policy endpoint/authorization detail. | EV-04–EV-06 |
| 39 | Approve button, `(1508,811)` | Disabled button; label “Phê duyệt xuất bản”. | #80 path-only; source target `APPROVED`, không publish. | EV-05 |
| 40 | Reject/request-changes button, `(1508,876)` | Disabled button; label gộp “Từ chối / Yêu cầu chỉnh sửa”. | #81 chỉ định `REJECTED`; không phân biệt request-revision. | EV-06 |
| 41 | “Quy trình 3 bước … (API #81)”, `(1508,936)` | Static copy. | API #81 là endpoint decision; không có workflow orchestration evidence. | EV-06 |
| 42 | Rubric heading, `(1390,1054)` | “Tiêu chí đánh giá chuẩn”. | Tĩnh, không rubric source. | EV-07 |
| 43 | “Rubric v2” badge, `(1508,1054)` | Static version label. | Không rubric version API/config. | EV-07 |
| 44 | Criterion copyright, `(1067,1150)` | Static checked criterion + explanatory text. | Không evidence review result/policy. | EV-07 |
| 45 | Criterion video resolution, `(1067,1275)` | Static checked Full HD/stereo statement. | Không có media metadata/validation source. | EV-07 |
| 46 | Criterion practice materials, `(1067,1380)` | Static checked materials statement. | Không có rubric data source. | EV-07 |
| 47 | “0/3 tiêu chí được nạp” progress, `(1508,1457)` | Static counter/progress bar. | Contradicts three checked criteria; no dynamic loading. | EV-07 |
| 48 | Footer copyright/privacy/RBAC/support, `(1548,1550)` | Footer text and `href="#"` links. | Static; destinations unimplemented. | EV-08 |

## 4. Conditional UI & state variations
- States theo inventory: loading/ready/approving/rejecting/stale/error
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/05_admin/AD-11_duyet-tu-choi-noi-dung/AD-11.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
