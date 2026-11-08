# SH-02 — API Integration

> **DEMO CONTRACT — CHƯA XÁC MINH**: Endpoint và schema chỉ dùng mô phỏng.

## 1. API matrix
| ID | Method/path | Auth | Event |
|---|---|---|---|
| `SH-02-API-001` | `GET /api/v1/courses/{courseId}` | Public; optional bearer to read enrollment status | EV-001, EV-006 |
| `SH-02-API-002` | `POST /api/v1/enrollments` | Required bearer | EV-004 |

## 2. SH-02-API-001 — GetCourseDetail
- Path: `courseId: string` nonempty max 64 chars; percent-encode when building URL.
- Header `Accept: application/json`; `Authorization: Bearer ...` chỉ khi user logged-in, không bắt buộc cho public read.

### Response 200
```json
{
  "id": "crs-101",
  "title": "Lập trình Python căn bản",
  "topic": "programming",
  "level": "basic",
  "description": "Học cú pháp Python, biến, vòng lặp và hàm qua bài tập.",
  "duration_minutes": 540,
  "lessons_count": 18,
  "chapters": [
    {"id":"ch-01","title":"Làm quen với Python","lesson_count":6},
    {"id":"ch-02","title":"Biến và cấu trúc điều khiển","lesson_count":12}
  ],
  "viewer": {"is_enrolled": false}
}
```

- Nếu anonymous, `viewer` có thể `null`; client diễn giải như chưa đăng ký và auth=false (auth state lấy từ session).
- `id,title,description,topic,level` → title/tags/description; `chapters[]` → accordion; `duration_minutes,lessons_count` → panel; `viewer.is_enrolled` → CTA.
- 404: screen not found; 422: invalid route id → not found UI; 500/network timeout: error banner + retry.

## 3. SH-02-API-002 — EnrollInCourse
- `POST /api/v1/enrollments`, header `Authorization: Bearer <access_token>`, `Content-Type: application/json`.
- Body:
```json
{"course_id":"crs-101"}
```
- Không có `user_id` trong payload; BE lấy actor từ token.

### Response 201
```json
{"enrollment_id":"enr-9001","course_id":"crs-101","status":"active"}
```

### Lỗi
| Case | Handling |
|---|---|
| 201 | Set `isEnrolled=true`; CTA `Đã đăng ký`, toast success |
| 401 | Clear pending, điều hướng login kèm returnUrl (không gửi lại POST tự động) |
| 403 | Toast `Bạn không có quyền đăng ký khóa học này` |
| 404 | Course không khả dụng; đổi sang not-found UI |
| 409 `ALREADY_ENROLLED` | Đồng bộ `isEnrolled=true`; không tạo enrollment mới |
| 422 | Hiển thị `Yêu cầu không hợp lệ`; không retry tự động |
| 500/503/network | Giữ CTA enabled sau khi kết thúc; thông báo thử lại thủ công |

- Timeout giả định 10s, không auto retry POST vì có thể gây duplicate khi chưa biết kết quả server.
- Nếu hết hạn token, flow xử lý token refresh là trách nhiệm shared auth layer, tránh tự retry POST vô điều kiện.
