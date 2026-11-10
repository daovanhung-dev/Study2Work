# AD-14 PLAN — Sửa, đổi trạng thái, xóa bài học

## 1. Phạm vi phiên

- Hoàn thiện **chỉ AD-14** theo `list_screen.md` row 72, kế hoạch tổng W4 và goal objective.
- Không xử lý AD-15 trong phiên này.
- Tạo DD Screen A–F, marker map JSON/SVG, `screen_annotated.png`, cập nhật row màn hình/API reverse index, checkpoint tổng và worklog.
- Giữ nguyên `screen.png` và `code.html`. Không sửa Study Server/API; chỉ mô tả current source.

## 2. Yêu cầu và điều hướng dự kiến

- Proposed route: `/admin/lessons/:lessonId/edit`, actor Admin với lesson-management permission theo AC-34.
- Handoff từ AD-13: numeric `Lesson.id` là path candidate do API #83 yêu cầu `lesson_id:int64`; không bổ sung query/state transport chưa được duyệt.
- AC-34 sequence: AD-12/#82 list → AD-13/#83 lesson + dependencies → chọn một nhánh riêng: #84 update, #85 status + audit, hoặc #86 delete theo policy → reload AD-12/#82.
- Inventory kỳ vọng editor, status action, delete confirmation/dependency handling và các trạng thái `dirty/saving/status-changing/deleting/error`. Đây là target design; đối chiếu với API contracts/current source trước khi chốt.

## 3. Current source và giới hạn cần giữ rõ

- Folder ban đầu có `screen.png` 1510×1600 (SHA-256 `6566d258887283bbba59361f613441cfdefe8f0a2a3416204016e1ec0e2baca9`) và `code.html` (SHA-256 `77e632dad66ca86d823e575c8339d7af0efd073976519602fdc06181d05118f9`). HTML là prototype tĩnh: form controls và mutation buttons disabled, anchors `#`, không route/data/API/event wiring.
- #84 route đang chạy cục bộ là PUT và trả một `Lesson`; catalog/AC chỉ khai báo path, không khai báo body. Local strict full-replacement body `{title, content, video_url, order}` là DERIVED; các field này không khớp đầy đủ form mockup (mockup có course/type, thiếu video_url). Không suy diễn mapping hoặc hidden-field preservation.
- #85 route đang chạy cục bộ là PATCH body `{status}`; local enum `DRAFT|PUBLISHED|SUSPENDED`, row lock, same-status no-op và audit insert atomic là DERIVED. Mockup gọi trạng thái cuối là “Lưu trữ/Archived”; không đồng nhất với `SUSPENDED`.
- #86 route đang chạy cục bộ là DELETE path-only. View khóa Lesson, kiểm tra mọi `lesson_progress`, `resources`, `lesson_uploads`; có reference thì 422, nếu không thì soft-delete `status='DELETED'` và trả `DeleteResult`. Dependency set/tombstone/timestamp/repeat-delete là local fallback, chưa được owner duyệt; #83 không trả dependency list/count.
- Cả #84–#86 dùng shared `ADMIN`, trong khi AC-34 yêu cầu lesson-management permission riêng. Legacy BIGINT DDL, V1-PILOT UUID schema, migration audit 012 và test fake DB không chứng minh live schema/deployment.
- Study Web vẫn `UNWIRED`; screenshot full-width Plus Jakarta Sans/cobalt cần được phân biệt với Study Web design target.

## 4. Sự kiện dự kiến trong DD

| Event | Trigger | Xử lý / nguồn | Kết quả và ranh giới |
|---|---|---|---|
| EV-01 Open/load editor | Route AD-14 được mở từ AD-13 | Lấy numeric Lesson ID candidate; GET #83 theo contract đã duyệt | Loading/ready/404/401/403/500; #83 hiện chỉ trả Lesson, không có dependencies; route chưa được wire. |
| EV-02 Edit metadata fields | Thay đổi form title/content/order hoặc field được owner chốt | Local dirty state; field mapping/validation từ #84 current implementation phải gắn DERIVED | Không gửi trường course/type/status ngoài body; `video_url` required nhưng mockup không có control, nên submit semantics bị chặn. |
| EV-03 Save metadata | Một trong hai nút “Lưu thay đổi thông tin” | Candidate PUT #84, body current-source DERIVED | Thành công trả Lesson và AC-34 quay về/reload AD-12; lỗi 401/403/404/422/500; không giả định retry/concurrency. |
| EV-04 Change status | Nút đổi trạng thái ở panel hành động | Candidate PATCH #85 `{status}`; enum/transition/audit policy còn mở | Thành công trả Lesson và audit được ghi cục bộ khi có đổi; lỗi catalog; không map Archived→SUSPENDED. |
| EV-05 Delete lesson | Nút xóa; confirmation UX chưa có trong ảnh | Candidate DELETE #86 path-only; server rechecks dependency trong transaction | 422 nếu local progress/resource/upload exists; 404 nếu thiếu/tombstone; 200 DeleteResult nếu soft-delete; sau thành công reload AD-12. |
| EV-06 Cancel/back | Cancel form, breadcrumb/back link | Prototype anchors `#`; target AD-13 vs AD-12/filter/history cần chốt | Không gửi API/mutation; không tuyên bố unsaved-changes dialog. |
| EV-07 Admin shell/footer | Nav, notification, RBAC, identity, footer links | Static copy/anchors, không có handlers trong HTML | Không gắn API/health/audit/security guarantees. |

## 5. Marker plan

Dự kiến 72 marker theo thứ tự thị giác, mỗi marker ánh xạ một dòng §C của DD. Marker groups:

| Range | Nhóm | Số lượng |
|---|---|---:|
| #1–#11 | Brand, Admin navigation, system/notification/identity, global breadcrumb, RBAC badge | 11 |
| #12–#15 | Ba breadcrumb cục bộ và nút về AD-12 | 4 |
| #16–#19 | Screen badge, route label, heading, subtitle | 4 |
| #20–#22 | Policy banner: icon, heading, explanatory copy | 3 |
| #23–#24 | Editor panel heading, selection/loading badge | 2 |
| #25–#28 | Title label/input/lock/helper | 4 |
| #29–#31 | Course label/select/helper | 3 |
| #32–#34 | Content type label/select/helper | 3 |
| #35–#37 | Order label/input/helper | 3 |
| #38–#41 | Current status label/display/hourglass/helper | 4 |
| #42–#43 | Description label/textarea | 2 |
| #44–#45 | Cancel and primary save actions | 2 |
| #46–#48 | Admin operation-standard card: icon/heading/copy | 3 |
| #49–#52 | Dangerous-actions panel: icon/title/subtitle/copy | 4 |
| #53–#56 | Update action card: title/lock tag/copy/button | 4 |
| #57–#60 | Status action card: title/lock tag/copy/button | 4 |
| #61–#64 | Delete action card: title/lock tag/copy/button | 4 |
| #65–#67 | Support/data-dependency card: icon/title/copy | 3 |
| #68–#72 | Footer copyright/descriptor/three links | 5 |

Decorative separators/background surfaces may be described with their containing component and are not independent controls. Place numbered circles in margins/unused surface whitespace, keep all strokes in bounds, then render and review the 2× image.

## 6. Blocker register

- **#84 body/form mismatch:** source body is DERIVED, course/content type are absent from current Lesson/update contract, and video_url is required but has no visible editor field.
- **#85 status mismatch:** local enum and AC do not define `ARCHIVED`, transition guards or publication readiness; status audit relation is migration 012 candidate only.
- **#86 dependency output/policy:** no #83 dependency payload or dedicated dependency API; local three-relation guard may not be complete; no UI count/preflight source.
- **Authorization:** no evidence that shared `ADMIN` is equivalent to lesson-management permission.
- **Database:** BIGINT legacy and UUID V1-PILOT Lesson models conflict; required response fields are nullable in legacy DDL; live migration/schema/locks unverified.
- **UI:** no editable Study Web app/router/client; source HTML controls/actions are static/disabled and visual direction differs from intended Study target.

## 7. Work order and acceptance checklist

1. [x] Re-read objective/router/context/worklog contract; classify `docs`; selector READY 3/219 and read all selected AD-01/02/03 worklogs plus AD-13 handoff.
2. [x] Load cross-scope project, Web Study, Server Study, registry/workflow context; inspect AC-34, inventory, APIs #84–#86 route/module/query/model/test source and DDL evidence.
3. [x] Save this plan before marker JSON/SVG, annotated image, or AD-14 DD.
4. [x] Create 72 ordered marker entries in JSON and SVG; render annotated image 2× and inspect it directly.
5. [x] Author A–F DD with exactly 72 §C rows; fully specify observed events, inputs, local processing, API boundaries, responses/errors, states, navigation and explicit blockers.
6. [x] Update AD-14 inventory and API reverse index #084–#086 based on local route/module/test source; append global checkpoint and finalize worklog. Keep API DDs Draft and do not alter AD-15.
7. [x] Static audit source hashes/dimensions, JSON/XML, marker sequence/coords/stroke bounds, 1:1 rows, local links, 83 IDs/folders/core artifact count, image review, whitespace and `git diff --check`. Do not run app tests/runtime.
8. [x] End after AD-14; preserve `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, `RUNTIME NOT VERIFIED` wherever current evidence requires them.
