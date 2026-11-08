# ME-03 — Workspace khóa học của mentor · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `ME-03` |
| Module | Mentor |
| Route | `/mentor/courses/:courseId` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **DD status:** `DD BLOCKED` — source-backed phần cây Content và roster progress; contract API #65, permission, course summary và phần lớn dữ liệu mẫu/UI còn quyết định hoặc không có nguồn.; **Implementation status:** `IMPLEMENTATION BLOCKED` — Study Web route/session chưa có; quyền course và các panel chính chưa có contract/API phù hợp.; **Runtime status:** `RUNTIME NOT VERIFIED` — không chạy frontend/API production hoặc live DB trong phiên này. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
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
> **Implementation status:** `IMPLEMENTATION BLOCKED` — Study Web route/session chưa có; quyền course và các panel chính chưa có contract/API phù hợp.
> **Runtime status:** `RUNTIME NOT VERIFIED` — không chạy frontend/API production hoặc live DB trong phiên này.

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
- **Current Study Web:** checkout không có `src/`, `package.json` hoặc router có thể sửa. `screen.png`/`code.html` là prototype tĩnh; nhãn “API #49 & #65 Synchronized”/“Live Feed” không chứng minh có API call.
- **Skill routing:** manifest/skill registry loại `web-ui-only-dd` khỏi `createDD-markdown`; UI-only DD chưa có skill canonical. Không dùng API DD template làm contract UI.
