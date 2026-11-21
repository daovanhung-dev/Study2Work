# GS-06 — Business Rules

> **T041/current-source update (2026-11-20):** GS-03 waits for #08 published-course success; GS-06 then calls #11 and renders validated PUBLIC resources. T041 approves PUBLIC/PRIVATE visibility, defaults existing resources to PRIVATE, returns #11 results ordered by ID ASC and defines valid empty as `200 []`. A selected ID goes to GS-07/#12. PRIVATE access requires Student auth, published parent course, ACTIVE enrollment and signed URL TTL 300 seconds. Source/runtime and resource producer gaps remain; historical T022 rules below are superseded.

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `GS-06-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Tài nguyên public theo khóa học; thể hiện quyền mở/tải theo metadata từ BE.
- Gate/status: **PARTIAL SOURCE; #11/#12 callers and T041 resource access semantics are source-wired/approved; runtime not verified.** Remaining gates are resource data population/schema (no `resources` writer found; #47 writes `lesson_uploads`), MIME-specific viewer behavior and live DB/storage. GS-06 itself calls #11 and enables resource selection to GS-07.
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

> T041 policy supersedes the pre-T041 gate claims; retain current-source evidence and runtime limitations.


## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
