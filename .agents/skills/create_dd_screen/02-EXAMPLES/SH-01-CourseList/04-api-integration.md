# SH-01 — API Integration

> **DEMO CONTRACT — CHƯA XÁC MINH**: Endpoint và schema dưới đây chỉ dùng trong bộ ví dụ.

## 1. Usage matrix
| ID | Method/Path | Auth | Invoked by |
|---|---|---|---|
| `SH-01-API-001` | `GET /api/v1/courses` | Public | EV-001, EV-002, EV-003, EV-005, EV-006, EV-007 |

## 2. SH-01-API-001 — ListPublishedCourses
- Headers: `Accept: application/json`.
- Query: `keyword?: string` (trimmed, 0–80 chars), `topic?: string` (`all` hoặc enum), `page: int >=1`, `page_size: 6`.
- Backend filter: chỉ trả khóa học published theo `SH-01-BR-004`.
- Ví dụ request: `GET /api/v1/courses?keyword=python&topic=all&page=1&page_size=6`.

### Response 200 (example)
```json
{
  "items": [
    {
      "id": "crs-101",
      "title": "Lập trình Python căn bản",
      "topic": "programming",
      "level": "basic",
      "short_description": "Học cú pháp và tư duy lập trình Python.",
      "thumbnail_url": null
    }
  ],
  "pagination": {
    "page": 1,
    "page_size": 6,
    "total_items": 1,
    "total_pages": 1
  }
}
```

### Data mapping
- `items[].id → CourseListItem.id`; `items[].title → title`; `topic, level` → tag; `short_description → description`; `thumbnail_url ?? fallback` → thumbnail.
- `pagination.total_items → totalItems`; `pagination.total_pages → totalPages`; `pagination.page → page`.
- `items=[]` là thành công/empty, **không** là lỗi.

### Error handling
| Status / case | Diễn giải | UI/state | Retry |
|---|---|---|---|
| 200 | Thành công, kể cả `items=[]` | Cập nhật data/empty | — |
| 422 | Query không hợp lệ | Banner `Bộ lọc không hợp lệ`, giữ input | Không tự động |
| 429 | Bị giới hạn request | Banner `Thao tác quá nhanh`; cho retry thủ công | Sau cooldown nếu header có |
| 500/503 | Server lỗi | Error banner + Retry | Thủ công |
| Network/timeout | Không kết nối được | Error banner + Retry | Thủ công |

- Timeout đề xuất demo: 10s; abort request cũ khi query mới xuất hiện (hoặc sequence guard); **không tự động retry** để tránh thêm tải.
- Cache: không cache phía client trong demo; khi quay lại screen request lại. Nguồn sự thật là backend.
- Source status: mock trong kit, không có OpenAPI thật.
