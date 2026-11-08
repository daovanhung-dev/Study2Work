# GS-07 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `GS-07-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Preview metadata/media hỗ trợ; fallback download khi URL hợp lệ và được phép.
- Gate/status (giữ nguyên): **R (#12 source-backed locally; API DD Draft)**; **BLOCK:** current public/no-auth direct URL lacks AC-06 access check/signer; preview/MIME/URL policy, 403/404/expiry mapping, GS-06/ST-12 return context and Study Web route UNWIRED; live schema unknown; prototype differs from Study design guide and WCAG unmeasured
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

### Trích từ DD nguồn: F. Quyết định còn mở và điều kiện chặn

| Quyết định/phụ thuộc | Tác động | Trạng thái |
|---|---|---|
| Public vs private visibility, authorization source và actor policy; AC-06 403 so với catalog/current public #12. | Chặn quyền truy cập và ready/403 state. | `BLOCKER` |
| Direct URL vs Storage signed URL, expiry/refresh/error semantics. | Chặn safe open/download; source hiện chỉ trả direct URL. | `BLOCKER` |
| `Resource` visibility/MIME/type/capability schema and preview allowlist. | Chặn renderer/fallback behavior; current response lacks visibility and capability. | `BLOCKER` |
| URL null handling, external origin safety, download headers and private bucket exposure. | Chặn việc hiển thị/mở URL an toàn. | `BLOCKER` |
| 403/404/410/500 mapping, inline vs SH-06, copy/retry. | Chặn error-state composition and navigation. | `BLOCKER` |
| Entry/return contract for GS-06 and ST-12 including course/lesson context. | Chặn route/history behavior. | `UNWIRED` / `BLOCKER` |
| Study Web app/router/API client. | Chặn implementation and runtime verification. | `UNWIRED` |
| Prototype/design-system alignment and measured accessibility. | Prototype uses remote fonts/Tailwind, Plus Jakarta Sans/cobalt/1440px, 32×32 toolbar controls and hides nav below `md`; current guide has different tokens/layout and requires ≥44px controls/reflow/focus/reduced-motion. | `DESIGN DISCREPANCY` / `NOT VERIFIED` |
| API DD #12 and live schema approval. | Visibility/URL/database fields remain unconfirmed. | `Draft — Needs Confirmation`; live schema `NOT_VERIFIED` |

### Phân loại cuối

- `DD BLOCKED`: các yêu cầu access/signed URL/preview/error/navigation chưa thống nhất; ghi nhận discrepancy đầy đủ để làm cơ sở quyết định.
- `IMPLEMENTATION BLOCKED`: access/signer/URL/type policy, state mapping và Study Web wiring còn thiếu.
- `RUNTIME NOT VERIFIED`: chỉ có static prototype và current backend source/test artifacts; không có end-to-end/browser/deployed evidence. Test source đã đọc nhưng không chạy.

## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
