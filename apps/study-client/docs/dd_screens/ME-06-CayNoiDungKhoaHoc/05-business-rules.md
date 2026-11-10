# ME-06 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `ME-06-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Tree sections/contents và thứ tự; mở editor/publish/delete khi được phép.
- Gate/status (giữ nguyên): **D**; **BLOCK:** Content không nằm trong 18 bảng DB.sql
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

### Trích từ DD nguồn: 6. Ma trận trạng thái, lỗi và bảo mật

| State | Trigger/evidence | UI rule |
|---|---|---|
| `loading` | Request #49 đang chờ | Skeleton/progress và cancel/retry behavior cần design; không có current client implementation. |
| `empty` | 200 `data:[]` | Hiển thị empty course state. Không phải lỗi; CTA create chỉ bật sau khi #50/type/parent rules được duyệt. |
| `ready` | 200 có cây đã validate | Dựng từ flat Content[] và giữ `id/status/order`; không gán mock values hoặc version không có. |
| `denied` | 401 hoặc 403 | Phân biệt sign-in/role/owner theo auth UX đã duyệt; không lộ course/node data. Current owner check direct. |
| `not-found` | 404 malformed/out-of-range path hoặc missing course | Không render mock course. Path error hiện cùng business code resource not found. |
| `error` | 500 DB/projection/tree integrity; network error ở client tương lai | Safe message, retry theo policy; không render partial tree. Network mapping chưa có source. |
| `saving/blocked` | Mutation handoff | Chỉ bật theo allowed server transition. #51/#52/#53 có 422 path; không optimistic-commit status/order. |
| `filter-empty` | Local search/filter không có row | Copy/ancestor behavior chưa có design; combine search and filter state thay vì để JS handlers ghi đè. |

- Server source yêu cầu role MENTOR và so khớp numeric principal với `courses.mentor_id`; assigned Mentor chưa được hỗ trợ ở các API này. UI không tự quyết định quyền bằng status badge.
- Mọi ID/status từ API phải được giữ an toàn; không đặt token/secret trong route. `payload` là object bất kỳ theo API model nên cần schema-specific sanitization/rendering trước khi render HTML hoặc URL.
- Không coi asset, GitHub, handbook, audit row hoặc external link trong fixture là trusted URL. Link policy/allowlist hiện chưa có contract cho ME-06.
- Keyboard/ARIA/focus, responsive behavior, loading/retry copy và destructive confirmation cần được chốt cho implementation; HTML hiện không chứng minh khả năng tiếp cận hay runtime layout ngoài snapshot desktop.

### Trích từ DD nguồn: 7. Discrepancies và quyết định còn mở

| Chủ đề | Expected/design | Current evidence | Ảnh hưởng |
|---|---|---|---|
| Content tree shape | Inventory gọi là tree | #49 trả flat `Content[]` + `parent_id`; API DD ghi owner confirmation còn mở | Client có thể dựng tree nhưng response shape approval chưa xong; giữ `DD BLOCKED`. |
| Chapter/lesson/lab/quiz model | Mockup phân loại rõ và có counts/duration | `content_type/status` open strings, `payload` object không subtype schema | Không có row-to-type mapping/validation. |
| ID/version | Inventory nói preserve IDs/version | `id` có; `version` không có trong #49; #51 archive version nhưng không chọn/return version | Không thể bảo đảm version-aware conflict/load. |
| Order | Mockup cho drag/save | #49 đọc `order`; #50 cấp order root; #51 giữ order; #52 là publish PATCH | Không có reorder persistence API; toast mock nhầm route/method. |
| Child create | Button thêm bài trong chapter | #50 luôn root `parent_id=NULL` | Không tạo được cây lồng từ endpoint hiện tại. |
| Draft publish | CTA publish trực tiếp ở row Draft | #52 chỉ APPROVED→PUBLISHED; PENDING_REVIEW không hợp lệ | CTA hiện không thể chạy đúng source state machine. |
| Delete parent | Mockup menu không mô tả dependency | #53 chặn PUBLISHED và active children, soft-delete | ME-08 cần confirmation/error flow; không cascade. |
| Course/KPI/quality/audit data | 4 KPIs, chart, QA rules, audit timeline | Không được trả bởi #49; không có read contract gắn cho các panel trong ME-06 | Không thể hydrate panels từ API #49. |
| Authorization | “Course phụ trách” | Source chỉ direct owner | AC assignment semantics và implementation lệch nhau. |
| Persistence | Content model đã có trong checkout | DDL/migrations 006/007 có; live deployment chưa xác minh | Không tuyên bố schema runtime. |
| Frontend/runtime | Route đề xuất | Study Web `UNWIRED`, HTML chỉ là mockup | Không thể xác nhận end-to-end, error UI hoặc route target. |

Các câu hỏi cần owner quyết định: ContentType/Status enums và payload schemas; flat-vs-nested API approval; chapter/lesson entity mapping; version selection/concurrency token; child-create/reorder endpoints; assignment authorization; publish readiness; delete/undo/refresh behavior; KPI, quality handbook, audit-log read source; migration deployment.

## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
