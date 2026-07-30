# Study2Work API Response Template

## 1. Mục đích

Template này chuẩn hóa response JSON cho **Study API** và **Work API đích**.

- Dễ xử lý ở frontend.
- Dễ theo dõi lỗi bằng `traceId`.
- Không trả stack trace, SQL, token hoặc dữ liệu nhạy cảm.

> Không áp dụng cho các route HTML/EJS của Work prototype.

---

## 2. Response thành công

```json
{
  "success": true,
  "businessCode": "COURSE_DETAIL_RETRIEVED",
  "message": "Lấy thông tin khóa học thành công.",
  "data": {
    "id": "course-uuid",
    "name": "FastAPI Foundation"
  },
  "meta": {},
  "traceId": "7d61fc96-5cac-4e4d-9154-7b6a5f844878"
}
```

---

## 3. Response danh sách có phân trang

```json
{
  "success": true,
  "businessCode": "COURSE_LIST_RETRIEVED",
  "message": "Lấy danh sách khóa học thành công.",
  "data": [],
  "meta": {
    "pagination": {
      "page": 1,
      "pageSize": 20,
      "totalItems": 100,
      "totalPages": 5,
      "hasNext": true,
      "hasPrevious": false
    }
  },
  "traceId": "7d61fc96-5cac-4e4d-9154-7b6a5f844878"
}
```

---

## 4. Response lỗi

```json
{
  "success": false,
  "businessCode": "VALIDATION_ERROR",
  "message": "Dữ liệu đầu vào không hợp lệ.",
  "errors": [
    {
      "code": "FIELD_REQUIRED",
      "field": "displayName",
      "message": "displayName là bắt buộc."
    }
  ],
  "traceId": "7d61fc96-5cac-4e4d-9154-7b6a5f844878"
}
```

---

## 5. Giải thích các thành phần

| Thành phần | Kiểu dữ liệu | Ý nghĩa |
|---|---|---|
| `success` | `boolean` | Request thành công hay thất bại. |
| `businessCode` | `string` | Mã nghiệp vụ ổn định để frontend xử lý logic. |
| `message` | `string` | Thông báo an toàn, có thể hiển thị cho người dùng. |
| `data` | `object`, `array`, `null` | Dữ liệu trả về khi thành công. |
| `meta` | `object` | Metadata bổ sung, thường chứa phân trang. |
| `errors` | `array` | Danh sách lỗi chi tiết khi thất bại. |
| `traceId` | `string` | UUID dùng để truy vết request trong log. |

---

## 6. Quy tắc sử dụng

### `businessCode`

Dùng chữ in hoa và dấu gạch dưới:

```text
COURSE_CREATED
COURSE_NOT_FOUND
AUTH_INVALID_CREDENTIALS
VALIDATION_ERROR
INTERNAL_SERVER_ERROR
```

Frontend phải xử lý theo `businessCode`, không phụ thuộc vào nội dung `message`.

### `traceId`

- Header chuẩn: `X-Trace-Id`.
- Backend nhận từ upstream hoặc tự tạo UUID mới nếu thiếu/không hợp lệ.
- Một chuỗi xử lý dùng cùng một `traceId`.
- Trả lại trong response header và response body.

### `errors`

Mỗi phần tử lỗi nên có cấu trúc:

```json
{
  "code": "FIELD_REQUIRED",
  "field": "email",
  "message": "email là bắt buộc."
}
```

`field` có thể bỏ qua nếu lỗi không gắn với một trường cụ thể.

---

## 7. HTTP status đề xuất

| Status | Trường hợp |
|---:|---|
| `200` | Thành công thông thường. |
| `201` | Tạo resource thành công. |
| `204` | Thành công nhưng không có response body. |
| `400` | Request hoặc điều kiện nghiệp vụ không hợp lệ. |
| `401` | Chưa xác thực hoặc token không hợp lệ. |
| `403` | Không có quyền truy cập. |
| `404` | Không tìm thấy resource. |
| `409` | Xung đột dữ liệu hoặc trạng thái. |
| `422` | Validation request thất bại. |
| `429` | Vượt giới hạn request. |
| `500` | Lỗi nội bộ hệ thống. |

---

## 8. Cấu trúc tổng quát

### Thành công

```json
{
  "success": true,
  "businessCode": "STABLE_CODE",
  "message": "Safe message",
  "data": {},
  "meta": {},
  "traceId": "uuid"
}
```

### Thất bại

```json
{
  "success": false,
  "businessCode": "STABLE_CODE",
  "message": "Safe message",
  "errors": [],
  "traceId": "uuid"
}
```
