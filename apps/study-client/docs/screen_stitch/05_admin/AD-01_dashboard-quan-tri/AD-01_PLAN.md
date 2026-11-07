# AD-01 — Kế hoạch Detailed Design

**Trạng thái:** `COMPLETED WITH BLOCKERS` — kế hoạch được viết trước marker, ảnh chú thích và DD; kết quả DD còn blocker được liệt kê tại §5.
**Phạm vi phiên:** chỉ Screen ID `AD-01`.

## 1. Mục tiêu và ranh giới

- Hoàn thiện kế hoạch, marker map, ảnh `screen_annotated.png` và DD A–F cho `/admin` dựa trên inventory, AC-38, API catalog/DD #101, PNG/HTML gốc, Study Web design guide và Study Server source hiện hành.
- Giữ riêng expected behavior và current behavior. Không biến các trường KPI, identity, audit log, status hạ tầng hoặc trạng thái ready trong mockup thành dữ liệu runtime.
- Truy vết điều hướng tới AD-02, AD-06, AD-10 và nhánh báo cáo AD-24/AD-25 đủ để nêu đúng handoff; không author DD cho các màn khác.
- Bảo toàn `screen.png` và `code.html`; mọi overlay chỉ tạo từ ảnh gốc.

## 2. Bằng chứng đã kiểm tra

### Expected behavior

- Inventory row 59: Admin dashboard `/admin`, AC-38, API #101, tổng quan học viên/khóa/tác động/KPI theo kỳ; GET #101 với `from`/`to`; states loading/partial/no-data/error; links AD-02/AD-06/AD-24; blocker hiện có là thiếu Admin role-profile endpoint.
- AC-38: Admin có quyền xem report/analytics; mở dashboard → #101 summary → #102 community impact → optional #103 export. API #101 trực tiếp khai báo Bearer JWT/Admin, `from?:date`, `to?:date`, không body, `ApiEnvelope<Report>`, 200 và lỗi 401/403/500.
- API #101 DD đang `Draft — Needs Confirmation`: `Report.period`, `metrics[]`, `generated_at` là response shape; bốn row-count metrics, default 30 ngày, population, query source, empty behavior và report permission là proposal/open questions.

### Current behavior

- `screen.png` 1600×1594, SHA-256 `93304b0a9846047a5e21a90bdb44fb197d4449e9dc725ec13b4239f416a0c25f`; `code.html` 26,680 bytes, SHA-256 `e9c678cee115f8ac83b9d73779420005d411ad7918846696ff4c6fe8484df979`.
- Prototype có bốn KPI placeholder (users, courses, moderation, infrastructure), status/audit/identity/compliance copy, disabled date choices và audit button, timer xoay icon làm mới 700 ms, placeholder navigation/footer và ba quick-link href. Không có API request.
- Study Web không có editable source/package/router; `dist/` chỉ có `index.html`, không thấy `/admin`/report-summary route string. Status `UNWIRED`; không suy ra serving/runtime.
- Study Server source hiện tới API #98; không có route/module/query/model/test cho #101. Existing Admin APIs #68–#98 dùng shared `ADMIN` role guard, nhưng điều đó không chứng minh #101 route/report authorization. `/users/me` hiện yêu cầu `STUDENT`; không có `/admin/me` profile route. Ghi rõ câu “shared helper chỉ Student” trong API #101 DD đã cũ so với source hiện tại.
- Canonical Study Web guide dùng palette ocean-blue/font Inter hoặc system; mockup dùng palette cobalt và remote Plus Jakarta Sans. Ghi đây là design discrepancy để owner/FE xử lý.

## 3. Kế hoạch sự kiện

| Event dự kiến | Element | Expected flow | Current prototype |
|---|---|---|---|
| EV-01 — Khởi tạo dashboard | Route/page | Sau auth Admin và route context, gọi #101 với date bounds đã được chốt; parse `Report`; ánh xạ KPI khi metric contract được duyệt. | Không có route/client/API; các số là `--`. |
| EV-02 — Chọn khoảng ngày | Segmented control | `Hôm nay`/`7 ngày qua`/`30 ngày qua` cần ánh xạ ra `from`/`to`; default, timezone, inclusive boundaries và response period còn mở. | Cả ba button disabled; không có change handler. |
| EV-03 — Làm mới số liệu | Refresh button | Khi được wire, chỉ refetch #101 với khoảng ngày hiện hành theo policy được duyệt. | Chỉ xoay icon 700 ms; không gửi request/state. |
| EV-04 — Header navigation | Primary nav | Route đích phải đối chiếu inventory trước khi mở. | Năm anchor dùng `href="#"`. |
| EV-05 — Notification | Bell button | Destination/API chưa xác định. | Không có listener. |
| EV-06 — Quick links | Users/courses/moderation cards | Candidate handoff tới AD-02, AD-06, AD-10. | Native href `/admin/users`, `/admin/courses`, `/admin/content/pending`; app router chưa có. |
| EV-07 — Audit log | View audit button | Cần audit-list contract và permission. | Disabled; không có handler/API. |
| EV-08 — Footer links | Privacy/RBAC/support | Destination chưa xác định. | Anchor `href="#"`. |

## 4. Kế hoạch marker và DD

- Tạo 35 component rows theo thứ tự đọc giao diện: brand/navigation/status/profile; hai dải breadcrumb; hero/date/refresh; bốn KPI cards; activity/audit; server status/permission notice; ba quick links; footer.
- Mỗi marker đại diện một component hoặc control; các label/icon nằm trong component được ghi chung tại element row. Ba date options và ba footer anchors được tách/diễn giải đầy đủ trong hàng component, không bỏ qua trạng thái từng control.
- Tạo `AD-01_markers.json`, `AD-01_markers.svg` và render `screen_annotated.png`; marker tuần tự `1..35`, nằm trong 1600×1594, không che nhãn/action.
- DD A–F: overview/roles/routes; expected vs current flow; element table 1:1; event contract theo nguồn; state/authorization/navigation; acceptance checklist và blockers.
- Với API #101, DD screen chỉ mô tả direct contract và error codes đã khai báo; gắn mọi field/KPI/range proposal là `DERIVED`; không nối #102/#103 vào dashboard nếu inventory/AC chỉ yêu cầu handoff.

## 5. Blocker cần giữ rõ

1. API #101 chưa có current route/module/query/model/test; API DD vẫn Draft.
2. KPI keys/formulas, population, units, order, empty/partial semantics và mapping với bốn card chưa duyệt.
3. Date options/default window/timezone/boundaries và invalid range behavior chưa chốt.
4. Report-specific authorization chưa source-backed; Admin profile endpoint/identity mapping chưa có.
5. Audit data, server/service health and queue status không được API #101 trả; prototype claims không được xem là live.
6. Study Web route/runtime chưa có; links và event hiện chỉ là mockup.
7. Visual tokens/font trong screenshot khác Study Web design guide.

## 6. Thứ tự thực hiện và kiểm chứng

1. [x] Hoàn thành kế hoạch này trước khi tạo marker/annotation/DD.
2. [x] Lập marker JSON/SVG và đối chiếu từng điểm với PNG gốc.
3. [x] Render ảnh chú thích 2×, kiểm tra kích thước/tỷ lệ và xem trực tiếp; đã chuyển marker #12 ra lề phải khỏi date-range text.
4. [x] Viết `AD-01.md` A–F với 35 hàng marker/event/API trace/state/navigation và blocker.
5. [x] Cập nhật row AD-01 trong `list_screen.md`, tracker trong `dd_screens/PLAN.md` và worklog trước verification.
6. [x] Hoàn tất static audit JSON/XML, IDs/in-bounds/links/PNG dimensions/hash, 83-screen inventory (`54/83` complete core bundles) và `git diff --check`. Không chạy application tests/runtime.
7. [x] Giữ phạm vi chỉ AD-01; không bắt đầu AD-02 trong phiên này.

## 7. Tiêu chí kết thúc phiên

- Giữ nguyên hash `screen.png` và `code.html`; có ảnh nguyên trạng + ảnh annotated hợp lệ.
- 35 marker tuần tự, duy nhất, trong bounds và khớp chính xác 35 element rows.
- DD có A–F, mô tả sự kiện thực có source, trace API/error mapping, state/navigation và mọi blocker chưa xác nhận.
- Tracker/worklog khớp **DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED** nếu các contract blockers vẫn mở.
- Không bắt đầu AD-02 trong phiên này; chỉ nêu AD-02 là ứng viên cho phiên riêng.

## Kết quả phiên

- Artifacts và tracker hoàn tất; static audit đạt, ảnh đã được xem trực tiếp.
- `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`.
- AD-02 chỉ là ứng viên cho phiên kế tiếp; không được bắt đầu trong phiên AD-01.
