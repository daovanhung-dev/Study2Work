# ĐẶC TẢ ÁNH XẠ UTC JSON → EXCEL

## 1. Cấu trúc chính thức

| Trang tính | Vai trò | Bảng ca kiểm thử |
|---|---|---|
| `01. Bìa` | Quản lý hồ sơ, nguồn chuẩn, dashboard thống kê | Không |
| `02. Tổng quan` | Mô tả màn hình, API, yêu cầu, blocker, ca toàn màn hình | Dòng 117–266 |
| `03. Thành phần` | Danh mục 50 thành phần và testcase chi tiết theo element | Dòng 71–270 |
| `04. Sự kiện` | Danh mục 50 event và testcase xử lý từng sự kiện | Dòng 71–270 |

## 2. Cột chung cho các ca

| Cột | Tên | Khóa trong JSON | Quy tắc |
|---|---|---|---|
| A | Mã ca kiểm thử | `id` | duy nhất, không bỏ trống |
| B | Mã yêu cầu | `requirement_ids` | các ID có trong bảng yêu cầu, phân cách `;` |
| C | Mã đối tượng | `target_id` | mã screen / element / event |
| D | Nhóm kiểm thử | `group` | trạng thái, API, giao diện, bảo mật... |
| E | Mục tiêu kiểm thử | `title` | một mục tiêu rõ |
| F | Điều kiện tiên quyết | `precondition` | có thể dựng lại |
| G | Dữ liệu kiểm thử | `data` | cụ thể hoặc đánh dấu đang chờ fixture |
| H | Các bước thực hiện | `steps` | danh sách, chuyển thành 1–n dòng |
| I | Kết quả mong đợi | `expected` | quan sát/đo được; nếu DD thiếu phải ghi chờ xác nhận |
| J | API liên quan | `api_ids` | tham chiếu API catalog đã trích |
| K | Nguồn DD | `source_refs` | file+mục+ID, không để trống |
| L | Mức ưu tiên | `priority` | Cao/Trung bình/Thấp |
| M | Tình trạng DD | `design_status` | Đã xác nhận/Chờ xác nhận/Không áp dụng |
| N | Trạng thái thực thi | script khởi tạo | luôn Chưa chạy |
| O–S | Kết quả thực tế, bằng chứng, mã lỗi, người, ngày | KHÔNG có trong JSON thiết kế | người kiểm thử điền sau khi chạy |
| T | Kiểm tra hồ sơ | công thức | Hợp lệ/Thiếu thông tin/Chờ xác nhận DD/Thiếu bằng chứng |

## 3. Nguồn thống kê và liên kết

- `01. Bìa` dùng công thức thống kê từ các vùng testcase; tổng ca = ca MH + TP + SK.
- Các yêu cầu `02. Tổng quan!A44:A103` có cột H đánh dấu “Có ca kiểm thử” nếu tồn tại link được sinh từ JSON.
- Bảng link có trong **`02. Tổng quan!V:W`** (vùng phụ trợ, không được chỉnh tay); các công thức coverage dùng `COUNTIF` mã chính xác.
- Không dựa vào tỷ lệ có ca để kết luận thiết kế hoặc runtime đạt nghiệm thu.
- Khi thêm/xóa/sửa ca hoặc yêu cầu, sửa JSON rồi **sinh lại Excel** để bảng V:W cập nhật theo đúng dữ liệu mới.

## 4. Cấu trúc JSON tối thiểu

```json
{
  "metadata": {
    "screen_id": "DEMO-01",
    "screen_name": "Màn hình minh họa",
    "dd_status": "Đã xác nhận",
    "runtime_status": "Chưa chạy",
    "source_name": "DD_DEMO-01.md"
  },
  "overall": {
    "objective": "Chức năng theo DD",
    "states": ["Đang tải", "Sẵn sàng"]
  },
  "apis": [],
  "requirements": [{
    "id":"DEMO-01-YC-001", "description":"Yêu cầu có trong DD",
    "source_ref":"DD_DEMO-01.md §1", "design_status":"Đã xác nhận"
  }],
  "elements": [{
    "id":"DEMO-01-EL-001", "name":"Nút A", "type":"Nút",
    "source_ref":"DD_DEMO-01.md §2"
  }],
  "events": [{
    "id":"DEMO-01-EV-001", "name":"Nhấn A", "trigger":"Nhấn nút",
    "element_ids":["DEMO-01-EL-001"], "api_ids":[], "source_ref":"DD_DEMO-01.md §3"
  }],
  "blockers": [],
  "test_cases": {
    "screen": [], "elements": [], "events": []
  }
}
```

Đây là ví dụ **cấu trúc**, không phải JSON hợp lệ hoàn chỉnh để thông qua validator vì chưa có ca kiểm thử. Ví dụ chạy thực tế có 73 ca tại `vi-du/GS-01/utc-gs01.json`. Schema mô tả cấu trúc tại `schema/utc-spec.schema.json`.

## 5. Giới hạn vùng

Giới hạn hiện hành: 17 API, 60 yêu cầu, 8 blocker, 200 thành phần, 200 sự kiện, 150 ca MH, 200 ca TP và 200 ca SK. Trang `03. Thành phần` và `04. Sự kiện` tự dời bảng ca xuống dưới danh mục khi có hơn 50 dòng; nếu vượt các giới hạn còn lại, mở rộng đồng bộ bộ sinh, validator và công thức trước khi phát hành. Không chép thêm ngoài vùng rồi cho rằng dashboard đã nhận.
