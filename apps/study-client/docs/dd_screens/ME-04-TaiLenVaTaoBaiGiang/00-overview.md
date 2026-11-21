# ME-04 — Tải lên và tạo bài giảng · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `ME-04` |
| Module | Mentor |
| Route | `/mentor/courses/:courseId/lectures/new` — registered in `mentor.route.ts`; browser runtime not verified |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | `DD BLOCKED` for unsupported design fields/lifecycle; current source implements a partial screen. Browser/runtime status: `RUNTIME NOT VERIFIED`. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.2 / 2026-11-20 |
| Nguồn đối chiếu | [ME-04.md](../../screen_stitch/04_mentor/ME-04_tai-len-va-tao-bai-giang/ME-04.md), [ME-04_PLAN.md](../../screen_stitch/04_mentor/ME-04_tai-len-va-tao-bai-giang/ME-04_PLAN.md), [ME-04_markers.json](../../screen_stitch/04_mentor/ME-04_tai-len-va-tao-bai-giang/ME-04_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Form lecture metadata, sắp xếp thứ tự, đính kèm media.
- In-scope: GET #46 course list → POST #34 upload → POST #47 create Markdown lecture → open ME-05, which reloads via #48.
- Out-of-scope: Module hierarchy, draft/review, preview, duration, media type metadata and other fields without source contracts.

## Current implementation (2026-11-21)
- The route and page are present. ME-04 calls #46 with `page=1,size=100`, uploads selected files through #34 as `purpose=LECTURE`, submits the returned IDs and Markdown `content:string` to #47, then opens ME-05 using the returned lecture ID. #46 performs separate COUNT and LIST queries; the client validates each page field and derived `total_pages` without requiring the separately read count to be at least the returned item count. The content textarea has accessible Markdown insertion actions for emphasis, headings, lists, quotes and code; they modify the same string submitted to #47. The supported form uses a two-column desktop layout and stacks at tablet/mobile widths.
- API #34/#47 enforce direct course ownership. #47 returns `PUBLISHED` immediately and stores content unchanged. Assigned-course access, upload cleanup, modules, preview/autosave and other mockup fields remain unsupported.
- Client response/error checks are source-backed. No test/build/browser verification was run in the active task; live API/storage is unverified.
- Route deactivation is blocked during #34/#47 writes so a pending mutation cannot silently lose its result when leaving ME-04.
- A second #47 submit event is ignored while a create request is already in flight; the button state remains the primary UI guard and no idempotency behavior is inferred.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-21 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Form lecture metadata, sắp xếp thứ tự, đính kèm media. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #46, #34, #47
- Liên kết màn hình dự kiến: [ME-05](../ME-05-XemBaiGiangMentor/00-overview.md), [ME-03](../ME-03-WorkspaceKhoaHocCuaMentor/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | draft/uploading/creating/422/error |
| Current runtime | Study Web route/page/source | `WIRED IN SOURCE` / browser and live runtime not verified |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [ME-04 source screen.png](../../screen_stitch/04_mentor/ME-04_tai-len-va-tao-bai-giang/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/04_mentor/ME-04_tai-len-va-tao-bai-giang/screen_annotated.png))
- Luồng: #46 → #34 → #47 (`content:string`, Markdown) → ME-05/#48. UI design remains partial because the mockup editor and lifecycle fields are not all supported by current APIs.
- Priority: P1; Gate/source status: **D**; content and asset ID mapping are resolved by T041; lifecycle, assigned-course access and unsupported fields remain open.

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# ME-04 — Tải lên và tạo bài giảng

> **DD status:** `DD BLOCKED` for fields/lifecycle beyond the current contract.
> **Implementation status:** `PARTIAL SOURCE IMPLEMENTATION` — route/page and #46/#34/#47 callers are wired.
> **Runtime status:** `RUNTIME NOT VERIFIED` — no test/build/browser/live API run in the active task.
> **Scope phiên:** chỉ Screen ID ME-04.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: 1. Tổng quan

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID | ME-04 |
| Tên | Tải lên và tạo bài giảng |
| Mục tiêu | Tạo lecture trong course, tải media/tài liệu qua API #34 rồi gửi metadata và asset references qua API #47. |
| Actor dự kiến | Mentor đã đăng nhập. AC-21 cho phép sở hữu hoặc được phân công course; current APIs chỉ chấp nhận trực tiếp owner. |
| Route đề xuất | `/mentor/courses/:courseId/lectures/new`; route chưa được wire. `courseId` phải tương thích signed int64 của #34/#47. |
| Trước màn hình | ME-03 workspace/course context hoặc deep link; authenticated MENTOR session; quyền truy cập course cần được xác minh. |
| Sau thành công | ME-05 `/mentor/lectures/:lectureId`; ME-05 dùng GET #48 để đọc lại lecture và asset links. Quay lại ME-03 dùng course context hiện tại. |
| API | GET #46 context; POST #34 upload; POST #47 create; GET #48 downstream read. |
| Thiết kế được cung cấp | `screen.png` và `code.html`; đây là sample/mockup, không phải runtime. |

### 1.1 Trạng thái bằng chứng

| Nhóm | Kết luận | Bằng chứng |
|---|---|---|
| Expected behavior | Form metadata, thứ tự, media, tạo lecture; inventory nêu #46 → #34 → #47 và trạng thái draft/uploading/creating/422/error. | [`list_screen.md` ME-04](../../list_screen.md#L164), AC-21. |
| Current UI | Historical preimplementation snapshot: source mockup HTML had no form/API and its CTA faked success after 900 ms. Current Study Web page contains a form, source-backed API callers and basic Markdown insertion actions; WYSIWYG/preview remain unavailable. | Original checkout/mockup; current source is under `src/app/features/mentor/ME04/`. |
| Current backend source | #34, #46, #47, #48 có route/module source; #34/#47 side effects và response được ghi ở dưới. | [`app/api/v1.py`](../../../../study-server/app/api/v1.py#L697), module source liên kết ở §10. |
| API tests | Test source có cho các nhánh chính; đã đọc nhưng **không chạy trong phiên này**. Test DB/provider giả không xác minh live deployment. | Test files ở §10; `.agents/server-study/tests.md`. |
| Persistence/runtime | SQL legacy BIGINT và migrations 004/005 có trong repo; live DB, migration deployment, object storage credentials/network chưa xác minh. | `infra/postgres/study-server/DB.sql`, migrations 004/005. |
