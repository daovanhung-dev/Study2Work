# SH-07 — Theo dõi tác vụ bất đồng bộ · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `SH-07` |
| Module | Shared / Auth / System |
| Route | `/operations/:operationId` — Shared route calls API #18 for notification Operation UUID; initial load and manual refresh |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | SH-07 hoàn thiện 100% theo rubric tĩnh UI/UX/logic/API trong notification-only scope, wired to current API #18 and producer #63/#93 behavior. Generic payment/export tracking remains out of scope; browser/live runtime is not verified. |
| Current implementation | Validates UUID, loads owner-bound notification status for Student/Mentor/Admin sessions, exposes manual refresh, and avoids delivery claims; focused tests pass. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.3 / 2026-11-21 |
| Nguồn đối chiếu | [SH-07.md](../../screen_stitch/01_shared_auth_system/SH-07_theo-doi-tac-vu-bat-dong-bo/SH-07.md), [SH-07_PLAN.md](../../screen_stitch/01_shared_auth_system/SH-07_theo-doi-tac-vu-bat-dong-bo/SH-07_PLAN.md), [SH-07_markers.json](../../screen_stitch/01_shared_auth_system/SH-07_theo-doi-tac-vu-bat-dong-bo/SH-07_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Hiển thị trạng thái backend của notification dispatch đã được chấp nhận.
- In-scope: Notification tracking only through current API #18 UUID, owner-bound contract, current statuses and approved producers.
- Out-of-scope: Payment/export results, generic operation lifecycle, polling, automatic retry and delivery-provider behavior.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-12,AC-25,AC-36,AC-38 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Dùng lại trạng thái job thanh toán/gửi thông báo/export theo ownership. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #18; producer handoffs #63 and #93; Admin explicit recipient list #68
- Liên kết màn hình dự kiến: [ST-07](../ST-07-KetQuaDangKyKhoaHoc/00-overview.md), [ME-15](../ME-15-TheoDoiGuiThongBao/00-overview.md), [AD-21](../AD-21-SuaKiemSoatDoTrangThaiThongBao/00-overview.md), [AD-25](../AD-25-XuatBaoCaoVaTheoDoiTienTrinh/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | queued/running/succeeded/failed/expired |
| Current source | SH07 page/service/model and current API #18 | UUID validation, role session selection, initial GET, manual refresh, queue/failure/sent mapping and private not-found/error states are source-wired; runtime not verified. |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [SH-07 source screen.png](../../screen_stitch/01_shared_auth_system/SH-07_theo-doi-tac-vu-bat-dong-bo/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/01_shared_auth_system/SH-07_theo-doi-tac-vu-bat-dong-bo/screen_annotated.png))
- Luồng: ME-14/#63 và AD-20/#93 trả UUID đã được kiểm tra; SH-07 gọi #18, nhận `NOTIFICATION_DISPATCH` cùng `QUEUED`/`FAILED`/`SENT`, và chỉ tải lại khi người dùng bấm. Queue có nghĩa là đã tiếp nhận, không xác nhận đã gửi.
- Priority: P2; generic operation types and provider delivery are outside this screen's approved scope.

## 6. Open questions / Change log
- Generic API #18 lifecycle/result/retention questions remain open outside the approved notification-only screen scope.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.
- 2026-11-21 — Reconciled SH-07 to the approved notification-only API #18 slice, wired API and producer handoffs, and verified focused tests; browser/live runtime remains unverified.

## Trạng thái và ranh giới bằng chứng

# SH-07 — Theo dõi tác vụ bất đồng bộ

> **DD status:** notification-only scope approved and source-wired · **Implementation:** complete for #63/#93 handoffs and #18 status reads · **Runtime:** `RUNTIME NOT VERIFIED`.

> Các block/source analysis bên dưới là bản DD trước khi scope được giới hạn ngày 2026-11-21. Chúng tiếp tục là lịch sử cho generic payment/export lifecycle; không mô tả trạng thái hiện tại của SH-07 notification flow.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: 1. Tổng quan màn hình

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID / tên | SH-07 — Theo dõi tác vụ bất đồng bộ |
| Loại surface | Panel dùng chung, theo inventory. HTML hiện dựng thành một trang dài; đây là design artifact. |
| Mục tiêu | Hiển thị trạng thái do backend xác nhận cho một operation đã được chấp nhận. SH-07 không tạo operation, không suy ra kết quả từ thời gian chờ và không khẳng định giao dịch/gửi/xuất đã xong khi chưa có response tương ứng. |
| Actor dự kiến | Student, Mentor hoặc Admin; API #18 requires the caller to own the notification operation. |
| Route | `/operations/:operationId` is registered to `SH07Page`; producer #63/#93 handoffs supply the validated UUID. |
| Input | UUID from the successful producer response; invalid UUID is rejected before the API request. |
| API | Client descriptor `API_018` is WIRED. Current API #18 source returns notification operations only and owner-binds lookup; SH-07 does not implement generic payment/export results. |
| Màn hình liên kết | ME-14 and AD-20 send accepted notification operations to SH-07; a safe in-app return route is carried in router state. |
| Side effect | Owner-bound read only; no write, polling, result download, or delivery-provider side effect. |
| Trạng thái tài liệu | Notification-only screen flow is source-backed; the broad generic Operation contract remains Draft outside this screen scope. |
