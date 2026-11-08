# AD-01 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `AD-01-EV-001` | `Source heading` / EV-01 — Khởi tạo dashboard / tải KPI | See source event detail below |
| `AD-01-EV-002` | `Source heading` / EV-02 — Chọn khoảng ngày | See source event detail below |
| `AD-01-EV-003` | `Source heading` / EV-03 — Làm mới số liệu | See source event detail below |
| `AD-01-EV-004` | `Source heading` / EV-04 — Header navigation | See source event detail below |
| `AD-01-EV-005` | `Source heading` / EV-05 — Notifications | See source event detail below |
| `AD-01-EV-006` | `Source heading` / EV-06 — Quick-link cards | See source event detail below |
| `AD-01-EV-007` | `Source heading` / EV-07 — Xem nhật ký kiểm toán | See source event detail below |
| `AD-01-EV-008` | `Source heading` / EV-08 — Footer links | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả sự kiện

### EV-01 — Khởi tạo dashboard / tải KPI

| Thuộc tính | Đặc tả |
|---|---|
| Trigger / điều kiện | Route `/admin` được đăng ký và Admin đã xác thực; report permission và date policy được phê duyệt. Current prototype không có event/caller. |
| Input | Bearer JWT từ session theo client contract chưa có; optional `from?:date`, `to?:date`; không body/path. Không suy ra giá trị ngày từ lựa chọn đang disabled. |
| API | Expected #101 `GET /api/v1/admin/reports/summary`; HTTP 200 `ApiEnvelope<Report>`. Không có current API call. |
| Xử lý theo thứ tự | 1) Kiểm tra route/session; 2) xác nhận quyền Admin/report; 3) chuẩn hóa bounds theo policy đã duyệt; 4) gửi GET với Bearer và query đã xác nhận; 5) đọc HTTP/business code; 6) validate envelope/`Report`; 7) yêu cầu mapping metrics theo key/formula đã duyệt; 8) render kỳ từ response và chỉ các card có mapping. |
| Thành công | `Report.period`, `metrics[]`, `generated_at` được parse theo schema; metric `value` là decimal-string. UI rendering, format/rounding và card mapping chưa thể chốt khi open questions còn tồn tại. |
| Lỗi/biên | Contract khai báo 401/403/500 với business codes ở §A. Invalid date, range đảo, timeout/network, partial metric, retry/cache chưa có mapping; không tự thêm response code hoặc công thức. |
| Side effect | #101 được mô tả read-only; query/DB side effect hiện không tồn tại trong source. |

### EV-02 — Chọn khoảng ngày

- **Trigger/current:** click trên “Hôm nay”, “7 ngày qua” hoặc “30 ngày qua”; cả ba button `disabled`, nên browser không phát sinh handler/change event trong prototype.
- **Expected input:** date bounds `from`/`to` kiểu `date`. Không có timezone, inclusive/exclusive, default window hay quy tắc chỉ truyền một đầu mút được phê duyệt.
- **Expected processing:** sau khi policy được chốt, giữ lựa chọn hiện tại, ánh xạ chính xác thành query #101 và gọi lại summary; không tự xử lý trong client bằng timezone local.
- **Current output:** không đổi UI, không request, không URL/state update. Default 30 ngày trong API DD là `DERIVED`, không phải hành vi được duyệt.

### EV-03 — Làm mới số liệu

- **Trigger:** click button `refresh-btn` khi `isRotating=false`.
- **Input:** không có filter/API input từ handler hiện tại; `refreshIcon` là DOM element được tìm theo ID.
- **Xử lý current source:** đặt `isRotating=true` → thêm class `rotate-180` → chờ 700 ms → bỏ class → đặt lại `isRotating=false`. Click liên tiếp trong thời gian xoay bị bỏ qua.
- **Kết quả:** chỉ icon đổi hình; số liệu không thay đổi vì không có request hoặc dashboard state. Nếu tương lai cần refetch #101, cần owner xác nhận refresh semantics, loading/error và duplicate policy.

### EV-04 — Header navigation

- **Trigger:** click một trong năm nav anchor.
- **Current input/processing:** `data-path` lần lượt là `tong-quan`, `nguoi-dung`, `khoa-hoc-noi-dung`, `kiem-duyet`, `bao-cao`; `href="#"`; không có router handler.
- **Current result:** browser điều hướng tới fragment rỗng/top của document; không có screen/API transition. Target screen cho từng label chưa được nối trong source.

### EV-05 — Notifications

- **Trigger:** click button `aria-label="Notifications"`.
- **Current processing/result:** button không có listener, badge đỏ là tĩnh; không có request, menu hay destination. Target/API chưa được xác định.

### EV-06 — Quick-link cards

- **Trigger:** click một card anchor.
- **Input/current output:** `href` lần lượt `/admin/users`, `/admin/courses`, `/admin/content/pending`; browser điều hướng theo URL path. Các đích phù hợp lần lượt với AD-02, AD-06, AD-10 trong inventory nhưng router/client runtime hiện không có, nên không xác nhận trang đích mở được.
- **API/data:** card click không trực tiếp gửi request. API tương ứng thuộc màn đích, không tự gọi từ AD-01.

### EV-07 — Xem nhật ký kiểm toán

- **Trigger/current:** nút có `disabled`; click không được kích hoạt.
- **Input/API/result:** không có request hoặc chuyển trạng thái. Cần audit-list endpoint, permission, filter, empty/error rules và route đích trước khi enable.

### EV-08 — Footer links

- **Trigger/current:** click privacy, RBAC standards hoặc technical support.
- **Current processing/result:** mỗi anchor có `href="#"`, không handler; chỉ fragment navigation. Đích nội dung chưa có trong contract.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
