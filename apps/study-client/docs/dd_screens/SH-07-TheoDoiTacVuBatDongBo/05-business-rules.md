# SH-07 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `SH-07-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Dùng lại trạng thái job thanh toán/gửi thông báo/export theo ownership.
- Gate/status (giữ nguyên): **D**; **BLOCK:** Operation status enum/ID mapping còn mâu thuẫn
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

### Trích từ DD nguồn: 9. Bảo mật, accessibility và design system

- Hiển thị operation chỉ sau khi server áp dụng authorization. Không tin `owner_id` từ client state và không đoán quyền Admin. 403/404 semantics phải được chốt để hạn chế IDOR/resource-existence leakage.
- Operation ID phải từ producer đã được contract phê duyệt; không dùng fallback mẫu hoặc ID lấy từ notification path. Không log response/result URL/raw error vào console.
- Không hiển thị raw database/internal details. `Developer Hand-off & Schema Diagnostic`, `STAGING-MOCK-07`, “migration v2.4” và `HANDOFF_STRICT` là mock/dev content; cần loại khỏi user production surface hoặc duyệt audience/feature gate riêng.
- Chỉ render result/download affordance nếu per-kind API schema cho biết trường và ownership/expiry policy; hiện `result_url` chưa thuộc generic Operation schema.
- Header account icon hiện là `div` không tương tác; không tạo profile button nếu chưa có requirement. Anchor `href="#"` không phải route hoạt động. Cần semantics/focus-visible cho controls.
- Modal phải dùng semantic dialog, quản lý focus vào/ra, keyboard close theo quyết định; hidden modal không có marker trong ảnh mặc định nhưng cần được kiểm tra khi implement.
- State labels có text kèm màu/chấm; giữ tên state bằng text và announce updates với screen reader chỉ khi có status source thật. Không chỉ dùng màu hoặc animation pulse.
- Design guide target: Inter nếu đã có hoặc system font, không tải remote font; content width khoảng 1120px; reflow ở mobile/tablet/desktop và không ẩn primary navigation/actions; controls ≥44px. Prototype dùng Plus Jakarta Sans/Material Symbols remote, Tailwind CDN, 1440px max width, nav ẩn dưới `md`, icon account 32px. Đây là design drift cần xử lý ở implementation.
- SVG architecture diagram hiện không có accessible label/hidden semantics. Status screenshot có `animate-pulse`; theo guide phải tôn trọng `prefers-reduced-motion` khi dùng animation trong runtime.

### Trích từ DD nguồn: 10. Blockers và quyết định còn thiếu

| ID | Hạng mục | Evidence | Cần chốt / tác động |
|---|---|---|---|
| `SH07-B01` | API #18 runtime/store absent | Không route/module/query/test; Study DDL không có operations table. | BE cung cấp API #18 runtime, approved Study persistence/query, migration/deployment evidence hoặc đóng design. Không map Work table. |
| `SH07-D01` | ID type | API #18 row int64 vs UUID convention/schema/AC/producer #63/#93. | Contract owner chọn một type và đồng bộ producer response/path/storage/client. |
| `SH07-D02` | Kind/status enum + lifecycle | No enum values/transition/terminal list; #64 statuses notification-specific. | BE/Product cung cấp canonical registry, transitions, terminal states, expiry semantics. |
| `SH07-D03` | Authorization and 403/404 | owner-only vs owner/Admin; owner claims/predicate absent. | Security/Product/BE chốt roles, owner mapping, Admin access, wrong-owner behavior. |
| `SH07-D04` | Producer response/result | #93 source/row/summary conflict; #17/#103 absent; `result?:Payment` doesn't cover notification/export. | Chuẩn hóa 202 producer data, operation ID placement, result schema per kind, export artifact ownership/URL. |
| `SH07-B02` | Polling/TTL/retry | Không cadence, SSE route, backoff, polling stop/retention policy. | Product/BE chốt transport/frequency/reconnect/retry/retention trước khi bật status refresh. |
| `SH07-B03` | Return navigation | Inventory links to four caller screens; prototype CTA uses GS-01/SH-01. | Product/FE chốt safe origin preservation/return target; không tự tạo query/state contract. |
| `SH07-B04` | Prototype vs user surface | Visible developer diagnostics, mock environment/ID and architecture claims. | UX/Product quyết định developer panel có bị loại khỏi production screen hay có audience guard. |
| `SH07-B05` | Study Web router/runtime absent | `apps/study-client/src/` và package manifest vắng; `.agents/web-work/study/` context tồn tại, registry status `UNWIRED`, xác nhận thiếu app source. | FE cung cấp current UI/router source và entrypoint để xác minh route/auth/404 integration; không gọi context page là runtime implementation. |

## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
