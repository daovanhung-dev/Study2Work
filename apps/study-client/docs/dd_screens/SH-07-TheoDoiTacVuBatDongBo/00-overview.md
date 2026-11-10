# SH-07 — Theo dõi tác vụ bất đồng bộ · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `SH-07` |
| Module | Shared / Auth / System |
| Route | `/operations/:operationId` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **DD status:** `BLOCKED` — bộ mô tả và ảnh chú thích đã lập, nhưng contract API #18 và các producer chưa đủ nhất quán để lập trình luồng theo dõi.; **Implementation status:** `IMPLEMENTATION BLOCKED` · **Runtime status:** `RUNTIME NOT VERIFIED`. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [SH-07.md](../../screen_stitch/01_shared_auth_system/SH-07_theo-doi-tac-vu-bat-dong-bo/SH-07.md), [SH-07_PLAN.md](../../screen_stitch/01_shared_auth_system/SH-07_theo-doi-tac-vu-bat-dong-bo/SH-07_PLAN.md), [SH-07_markers.json](../../screen_stitch/01_shared_auth_system/SH-07_theo-doi-tac-vu-bat-dong-bo/SH-07_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Dùng lại trạng thái job thanh toán/gửi thông báo/export theo ownership.
- In-scope: Chỉ GET #18 nếu đã có operation_id do BE xác nhận; không tự sinh ID, stop theo terminal state.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-12,AC-25,AC-36,AC-38 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Dùng lại trạng thái job thanh toán/gửi thông báo/export theo ownership. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #18
- Liên kết màn hình dự kiến: [ST-07](../ST-07-KetQuaDangKyKhoaHoc/00-overview.md), [ME-15](../ME-15-TheoDoiGuiThongBao/00-overview.md), [AD-21](../AD-21-SuaKiemSoatDoTrangThaiThongBao/00-overview.md), [AD-25](../AD-25-XuatBaoCaoVaTheoDoiTienTrinh/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | queued/running/succeeded/failed/expired |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [SH-07 source screen.png](../../screen_stitch/01_shared_auth_system/SH-07_theo-doi-tac-vu-bat-dong-bo/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/01_shared_auth_system/SH-07_theo-doi-tac-vu-bat-dong-bo/screen_annotated.png))
- Luồng: Chỉ GET #18 nếu đã có operation_id do BE xác nhận; không tự sinh ID, stop theo terminal state.
- Priority: P2; Gate/source status: **D**; **BLOCK:** Operation status enum/ID mapping còn mâu thuẫn

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# SH-07 — Theo dõi tác vụ bất đồng bộ

> **DD status:** `BLOCKED` — bộ mô tả và ảnh chú thích đã lập, nhưng contract API #18 và các producer chưa đủ nhất quán để lập trình luồng theo dõi.
> **Implementation status:** `IMPLEMENTATION BLOCKED` · **Runtime status:** `RUNTIME NOT VERIFIED`.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: 1. Tổng quan màn hình

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID / tên | SH-07 — Theo dõi tác vụ bất đồng bộ |
| Loại surface | Panel dùng chung, theo inventory. HTML hiện dựng thành một trang dài; đây là design artifact. |
| Mục tiêu | Hiển thị trạng thái do backend xác nhận cho một operation đã được chấp nhận. SH-07 không tạo operation, không suy ra kết quả từ thời gian chờ và không khẳng định giao dịch/gửi/xuất đã xong khi chưa có response tương ứng. |
| Actor dự kiến | Student, Mentor hoặc Admin chỉ trong phạm vi operation được phép xem. AC diagrams nói owner-only; operation-tracking summary nói owner hoặc Admin. Role và owner policy chưa thống nhất. |
| Route đề xuất | `/operations/:operationId`; hiện không có Study Web router/source để xác nhận route. API design dùng `/api/v1/operations/{operation_id}`. |
| Input | Operation ID phải do producer/backend trả về. Không tự sinh ID, không dùng UUID minh họa/fallback. Kiểu path chưa thể validate vì API #18 row khai báo int64, còn convention/schema/AC và producer source có UUID. |
| API | API #18 là thiết kế `D`; `GET /api/v1/operations/{operation_id}` chưa có route/module/query/test trong Study Server hiện tại. Notification-specific #64/#96 không thay thế endpoint generic. |
| Màn hình liên kết | ST-07, ME-15, AD-21, AD-25 là các caller/consumer trong inventory. HTML prototype lại đưa CTA về GS-01 và SH-01; safe-return context chưa có contract. |
| Side effect | Đọc trạng thái operation theo contract; không sửa operation hoặc tạo side effect nghiệp vụ. Hiện prototype không gọi API. |
| Trạng thái tài liệu | Các element, event, state gate và blocker được ghi dưới đây; không tuyên bố DD READY do identifier, owner policy, enum/lifecycle và producer mapping còn chặn luồng cốt lõi. |
