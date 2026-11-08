# AD-22 — Danh sách thảo luận bị báo cáo · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `AD-22` |
| Module | Admin |
| Route | `/admin/discussions/reported` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **DD status:** `DD BLOCKED` · **Implementation status:** `IMPLEMENTATION BLOCKED` · **Runtime status:** `RUNTIME NOT VERIFIED` |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [AD-22.md](../../screen_stitch/05_admin/AD-22_danh-sach-thao-luan-bi-bao-cao/AD-22.md), [AD-22_PLAN.md](../../screen_stitch/05_admin/AD-22_danh-sach-thao-luan-bi-bao-cao/AD-22_PLAN.md), [AD-22_markers.json](../../screen_stitch/05_admin/AD-22_danh-sach-thao-luan-bi-bao-cao/AD-22_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Queue theo severity/reason, pagination, ưu tiên pending.
- In-scope: GET #97 → detail AD-23; không tự giả lập endpoint report discussion.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-37 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Queue theo severity/reason, pagination, ưu tiên pending. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #97
- Liên kết màn hình dự kiến: [AD-23](../AD-23-DieuTraKiemDuyetThaoLuan/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | loading/empty/ready/error |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [AD-22 source screen.png](../../screen_stitch/05_admin/AD-22_danh-sach-thao-luan-bi-bao-cao/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/05_admin/AD-22_danh-sach-thao-luan-bi-bao-cao/screen_annotated.png))
- Luồng: GET #97 → detail AD-23; không tự giả lập endpoint report discussion.
- Priority: P1; Gate/source status: **R** local #97 route/module/query/validator/model source; API DD Draft. **BLOCK:** Chưa tìm thấy report writer hoặc xác minh live schema; #97 không trả count/reason/severity/reporter/time cho cột UI; search/status/pending priority/AC permission vs `ADMIN` chưa chốt; Study Web UNWIRED

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# AD-22 — Danh sách thảo luận bị báo cáo

> **DD status:** `DD BLOCKED` · **Implementation status:** `IMPLEMENTATION BLOCKED` · **Runtime status:** `RUNTIME NOT VERIFIED`
> Đây là đặc tả cho Screen ID 80 trong inventory. `screen.png` là ảnh nguyên trạng; các con số trong [`screen_annotated.png`](../../screen_stitch/05_admin/AD-22_danh-sach-thao-luan-bi-bao-cao/screen_annotated.png) ánh xạ theo thứ tự tới §C và [`AD-22_markers.json`](../../screen_stitch/05_admin/AD-22_danh-sach-thao-luan-bi-bao-cao/AD-22_markers.json).

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID / tên | `AD-22` — Danh sách thảo luận bị báo cáo; Page trong inventory. |
| Mục tiêu dự kiến | Admin xem hàng đợi các thảo luận bị báo cáo, lọc danh sách theo các query được #97 hỗ trợ và mở một Discussion để điều tra tại AD-23. |
| Actor / quyền | Expected actor là `Admin` theo AC-37 và catalog #97. Current #97 dùng shared guard `role="ADMIN"`. Chưa có bằng chứng hai chính sách này tương đương hoặc về tenant/fine-grained permission; không coi badge `RBAC` trong prototype là bằng chứng quyền đã kiểm tra. |
| Route | Candidate `/admin/discussions/reported` theo inventory. Study Web không có tracked `src/`, router hoặc API client trong checkout; route chưa được wire. |
| Điều kiện trước | Khi triển khai: phiên hợp lệ, backend xác thực quyền theo policy được phê duyệt; chỉ truyền query được contract cho phép. Report phải được ghi bởi một producer đã được duyệt và tồn tại trong schema đang chạy. Hai điều kiện cuối chưa được xác minh. |
| Kết quả sau | Expected: hiển thị trang kết quả #97 hoặc state lỗi/rỗng đã định nghĩa; chọn một Discussion bằng ID hợp lệ để đi tới AD-23/#98. Current #97 không trả report metadata mà các cột trong prototype yêu cầu. |
| Màn hình liên quan | AD-23 (`/admin/discussions/:discussionId/moderate`) là detail/handoff dự kiến; #98 nhận `discussion_id:int64`. #99/#100 và quyết định xử lý thuộc AD-23, không nằm trong AD-22. Header/footer destinations hiện không có route. |
| API liên quan | #97 `GET /api/v1/admin/discussions/reported`; #98 chỉ tại handoff. #97 local route/module tồn tại; API DD #97 vẫn `Draft — Needs Confirmation`. |
| UI state trong inventory | `loading / empty / ready / error`. Đây là expected checklist, không phải state machine được implement trong Study Web. |
| Ràng buộc chính | Không tạo Student report API; không suy diễn search/status/count/reason/time fields từ ảnh; không coi policy cards, số liệu, nhãn “SẠCH VI PHẠM” hay “System Normal” là backend state. |

### Traceability

| Nguồn | Phần sử dụng / trạng thái |
|---|---|
| [Inventory row 80](../../list_screen.md) | Route, AC/API, expected queue purpose/states, AD-23 handoff và blocker report creation. |
| [AC-37 flow](../../../../study-server/docs/diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) | Expected queue → #97 → read reports + Discussion summary → #98; quyết định moderation và optional delete là bước sau. |
| [API catalog](../../../../../docs/lists/list_api.md), rows #97–#100 | Direct request/response/error contracts; #97 không có search/status/report metadata. |
| [Study Server router](../../../../study-server/app/api/v1.py), [#97 module](../../../../study-server/app/modules/admin/api_97_admin_discussions_reported) | Current registered route, guard, validation, query, projection, errors, read-only effect. |
| [#97 open questions](../../../../study-server/docs/dd/97_admin_discussions_reported/OPEN_QUESTIONS.md) | Report writer/live schema, report response gap, nullable legacy projection fields; API DD remains Draft. |
| [#98 cover](../../../../study-server/docs/dd/98_admin_discussions_detail/00_Cover.md) and current #98 source | DD says `UNWIRED / NOT_FOUND`, while a local route/module exists; current projection does not read reports. Discrepancy retained. |
| [Web Study design guide](../../../../../.agents/web-study/design.md) | Shared UI/accessibility reference; source prototype is preserved as supplied and not treated as the design system implementation. |
| [`screen.png`](../../screen_stitch/05_admin/AD-22_danh-sach-thao-luan-bi-bao-cao/screen.png), [`code.html`](../../screen_stitch/05_admin/AD-22_danh-sach-thao-luan-bi-bao-cao/code.html) | Visual/DOM prototype only. Source hashes are listed in [plan](../../screen_stitch/05_admin/AD-22_danh-sach-thao-luan-bi-bao-cao/AD-22_PLAN.md). |
