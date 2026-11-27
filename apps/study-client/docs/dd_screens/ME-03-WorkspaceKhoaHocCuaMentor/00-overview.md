# ME-03 — Workspace khóa học của mentor · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `ME-03` |
| Module | Mentor |
| Route | `/mentor/courses/:courseId` — source-wired in `mentor.route.ts`; runtime not verified |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | `DD BLOCKED` — API #65, permissions, course summary and prototype-only panels/actions still need product/API decisions.<br>`Implementation: SOURCE_PARTIAL` — route and #46/#49/#65 callers are present; route IDs and responses are validated, access errors fail closed, and unsupported prototype panels remain unavailable.<br>`Runtime: RUNTIME NOT VERIFIED` — no authenticated browser, deployed API/DB, or production runtime has been exercised. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.2 / 2026-11-27 |
| Nguồn đối chiếu | [ME-03.md](../../screen_stitch/04_mentor/ME-03_workspace-khoa-hoc-cua-mentor/ME-03.md), [ME-03_PLAN.md](../../screen_stitch/04_mentor/ME-03_workspace-khoa-hoc-cua-mentor/ME-03_PLAN.md), [ME-03_markers.json](../../screen_stitch/04_mentor/ME-03_workspace-khoa-hoc-cua-mentor/ME-03_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Tổng quan cây nội dung, tiến độ lớp, hành động tạo bài giảng.
- In-scope: GET #49 và #65 sau khi course thuộc #46; render module theo permissions.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-22,AC-26 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Tổng quan cây nội dung, tiến độ lớp, hành động tạo bài giảng. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #49, #65
- Liên kết màn hình dự kiến: [ME-04](../ME-04-TaiLenVaTaoBaiGiang/00-overview.md), [ME-06](../ME-06-CayNoiDungKhoaHoc/00-overview.md), [ME-16](../ME-16-TienDoToanKhoaHoc/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | loading/no-content/partial/error |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [ME-03 source screen.png](../../screen_stitch/04_mentor/ME-03_workspace-khoa-hoc-cua-mentor/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/04_mentor/ME-03_workspace-khoa-hoc-cua-mentor/screen_annotated.png))
- Luồng: GET #49 và #65 sau khi course thuộc #46; render module theo permissions.
- Priority: P1; Gate/source status: **D**

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# ME-03 — Workspace khóa học của mentor

> **DD status:** `DD BLOCKED` — source-backed phần cây Content và roster progress; contract API #65, permission, course summary và phần lớn dữ liệu mẫu/UI còn quyết định hoặc không có nguồn.
> **Implementation status:** `SOURCE_PARTIAL` — route `/mentor/courses/:courseId` và callers #46/#49/#65 có trong Study Web. ME-03 theo dõi `courseId`, hủy request cũ khi route đổi, kiểm tra response và tách trạng thái tải cây nội dung/tiến độ. Các panel prototype không có dữ liệu/API phù hợp vẫn chưa triển khai.
> **Runtime status:** `RUNTIME NOT VERIFIED` — không chạy frontend/API production hoặc live DB trong phiên này.

### Current source reconciliation — 2026-11-27

- The current Angular route calls #46 for course title, #49 for Content, and #65 for the local Student progress projection. All three requests use the Mentor session/API transport; #49/#65 are read-only server queries with direct-owner checks.
- The page validates route IDs, separates Content/progress loading and error states, and clears both panels if either endpoint returns an access-denial response. A successful envelope with a wrong business code or invalid projection uses a screen validation message; a `success:false` envelope preserves its server message.
- Five routed HTTP-backed tests cover the authenticated request paths, source-backed rendering, invalid route ID, fail-closed access handling, and response validation. Focused ME-03 tests pass 5/5; the Study Web suite passes 104 spec files/375 tests. These local mocks do not close ME03-B01–B09 or verify runtime.
- The source excerpt below is the original design-time snapshot; statements there that the Study Web route is absent do not describe the current checkout.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: 1. Tổng quan

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID / tên | ME-03 — Workspace khóa học của mentor |
| Mục tiêu theo inventory | Hiển thị cấu trúc nội dung khóa học và tiến độ lớp; là điểm điều hướng tới quản lý nội dung, tạo lecture và báo cáo tiến độ. |
| Actor | Mentor; AC-22 yêu cầu quyền quản lý course, AC-26 yêu cầu quyền xem analytics. |
| Route đề xuất | `/mentor/courses/:courseId`; route chưa có trong Study Web hiện tại. |
| Input chính | `courseId` path, candidate signed int64 theo #49/#65. Screen không có query/body contract. |
| API theo inventory | GET #49 cây nội dung và GET #65 tiến độ lớp, sau khi course được nhận diện từ ME-02/#46. |
| Liên kết được inventory xác nhận | ME-04, ME-06, ME-16; về trước ME-02. |
| UI states kỳ vọng | loading, no-content, partial, error. Cách khôi phục auth/permission và nghĩa chính xác của `partial` còn cần chốt. |
| Assets | [screen.png](../../screen_stitch/04_mentor/ME-03_workspace-khoa-hoc-cua-mentor/screen.png), [code.html](../../screen_stitch/04_mentor/ME-03_workspace-khoa-hoc-cua-mentor/code.html), [ảnh chú thích](../../screen_stitch/04_mentor/ME-03_workspace-khoa-hoc-cua-mentor/screen_annotated.png), [marker JSON](../../screen_stitch/04_mentor/ME-03_workspace-khoa-hoc-cua-mentor/ME-03_markers.json), [SVG overlay](../../screen_stitch/04_mentor/ME-03_workspace-khoa-hoc-cua-mentor/ME-03_markers_overlay.svg). |

### Trạng thái bằng chứng

- **Expected behavior:** [ME-03 trong inventory](../../list_screen.md#L163), AC-22/AC-26 và route/dependency list. Inventory xác định #49/#65, trạng thái và các màn hình liên kết.
- **Current API #49:** route/module hiện có, read-only, trả flat `Content[]`; catalog và AC-22 cùng nêu `Content[]`. API DD vẫn giữ Draft — Needs Confirmation cho payload/lifecycle/revision và direct-owner so với assigned-course policy.
- **Current API #65:** route/module hiện có, read-only, trả local `Page<MentorStudentProgress>`. API catalog vẫn ghi `ApiEnvelope<Page<Course>>`; local response, tính progress, roster eligibility và trang không giới hạn là lựa chọn DERIVED chưa được owner duyệt.
- **Current Study Web:** route `/mentor/courses/:courseId` gọi #46 để tra tiêu đề trang, #49 để lấy cây Content và #65 để lấy roster progress; #49/#65 kiểm tra direct ownership phía server. ME-03 xác thực ID/response, giữ tải/lỗi của cây và roster riêng, và hủy request của course trước đó khi route đổi. `screen.png`/`code.html` vẫn là prototype tĩnh; nhãn “API #49 & #65 Synchronized”/“Live Feed” không chứng minh runtime. API #65 response local vẫn khác catalog; analytics, per-module progress và các số liệu mẫu không được dựng giả.
- **Skill routing:** manifest/skill registry loại `web-ui-only-dd` khỏi `createDD-markdown`; UI-only DD chưa có skill canonical. Không dùng API DD template làm contract UI.
