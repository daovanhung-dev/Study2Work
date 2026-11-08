# SH-01 — Data Flow & State

## 1. State model
```ts
type Topic = 'all' | 'programming' | 'backend';
type LoadStatus = 'idle' | 'loading' | 'success' | 'error';
interface CourseListItem {
  id: string; title: string; topic: string; level: string;
  description: string; thumbnailUrl: string | null;
}
interface CourseListState {
  searchKeyword: string; topic: Topic; page: number; pageSize: 6;
  items: CourseListItem[]; totalItems: number; totalPages: number;
  status: LoadStatus; errorMessage: string | null; requestSeq: number;
}
```

## 2. Data source → target
| Data | Source | Transform | Destination |
|---|---|---|---|
| keyword | `SH-01-EL-003` input | trim, max 80 | request `keyword`, state |
| topic | `SH-01-EL-004` select | validate enum | request `topic`, state |
| page | pagination click or reset | clamp/validate | request `page`, state |
| courses | `SH-01-API-001.items` | DTO→CourseListItem | `SH-01-EL-006` |
| total/count | `SH-01-API-001.pagination` | integers >=0 | `SH-01-EL-005/007` |

## 3. Read flow
1. `SH-01-EV-001` khởi tạo state `{keyword:'', topic:'all', page:1, pageSize:6}`.
2. Tăng `requestSeq`; set `status='loading'`, `errorMessage=null`, clear `items` của lượt truy vấn cũ để tránh hiển thị stale.
3. Gọi `SH-01-API-001` với params mới; chỉ áp dụng response có sequence mới nhất.
4. Kiểm tra field/type; map DTO vào `CourseListItem`, state `totalItems/totalPages/page`, set `status='success'`.
5. Nếu `items=[]`, hiển thị empty; lỗi/timeout mới nhất → `status='error'`, `items=[]`, thông báo retry.

## 4. Write flow (đổi bộ lọc / page)
1. User cập nhật `searchKeyword` hoặc `topic`; reset `page=1` theo `SH-01-BR-002`.
2. Debounce `keyword` 300ms; với `topic/page` request ngay. Hủy debounce cũ.
3. Chạy lại read flow; chọn card chỉ đọc `courseId` và điều hướng, không mutate backend.

## 5. Derived/cache/concurrency
- `showPagination = status === 'success' && totalPages > 1`.
- `showEmpty = status === 'success' && items.length === 0`.
- Không cache trong demo; unmount: cancel pending debounce/request hoặc ignore response khi component bị tháo.
- `requestSeq` tăng trước request, **không** cho lỗi của request cũ ghi đè kết quả mới (`SH-01-BR-005`).
- Các dữ liệu API được giả định là public; không lưu dữ liệu người dùng nhạy cảm ở query/local storage.

## 6. Mapping liên quan
[UI](01-ui-elements.md) · [Events](02-events.md) · [API](04-api-integration.md) · [Rules](05-business-rules.md)
