# GS-07 — Business Rules

> **T041/current-source update (2026-11-20):** Enforce the approved PUBLIC/PRIVATE rule through #12: PUBLIC gets a validated direct HTTP(S) URL; PRIVATE requires a Student token, published parent course, ACTIVE enrollment and a 300-second signed URL. The client separately validates response identity/projection and URL safety, and does not embed or auto-open the URL. No MIME allowlist or expiry-specific UI is implemented. The rule table and source excerpt retain older catalog/mockup language where marked; local source does not prove live storage/schema.

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `GS-07-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Preview metadata/media hỗ trợ; fallback download khi URL hợp lệ và được phép.
- Gate/status: **PARTIAL SOURCE; #12 caller and T041 PUBLIC/PRIVATE access semantics are wired/approved; runtime not verified.** Remaining gates: MIME-specific viewer and expiry UX, no `resources` producer found (#47 writes `lesson_uploads`), schema/storage availability, prototype/design-guide mismatch and unmeasured accessibility.
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

### Trích từ DD nguồn: F. Quyết định còn mở và điều kiện chặn

| Quyết định/phụ thuộc | Tác động | Trạng thái |
|---|---|---|
| Public/private visibility and authorization. | T041 resolves: PUBLIC direct URL; PRIVATE requires Student ACTIVE enrollment. | `APPROVED / SOURCE-WIRED` |
| Direct URL vs Storage signed URL. | T041 resolves PRIVATE URL signing with 300-second TTL; PUBLIC uses valid direct HTTP(S). | `APPROVED / SOURCE-WIRED` |
| `Resource` visibility/MIME/type/capability schema and preview allowlist. | Response includes visibility; MIME-specific renderer/allowlist remains unspecified. | `PARTIAL / PREVIEW OPEN` |
| URL null handling, external origin safety, download headers and private bucket exposure. | Chặn việc hiển thị/mở URL an toàn. | `BLOCKER` |
| Error mapping and retry. | Source distinguishes 401/403/404; other errors show retry. No 410 expiry response contract. | `PARTIAL SOURCE` |
| Entry/return contract for GS-06 and ST-12 including course/lesson context. | Source carries `courseId`/`lessonId` query and returns to the matching panel. Browser/runtime unverified. | `SOURCE-WIRED / RUNTIME NOT VERIFIED` |
| Resource detail behavior, API #12 client, and verified runtime. | #12 caller and current data flow exist; deployment/runtime remains unverified. | `PARTIAL SOURCE / RUNTIME NOT VERIFIED` |
| Prototype/design-system alignment and measured accessibility. | Prototype uses remote fonts/Tailwind, Plus Jakarta Sans/cobalt/1440px, 32×32 toolbar controls and hides nav below `md`; current guide has different tokens/layout and requires ≥44px controls/reflow/focus/reduced-motion. | `DESIGN DISCREPANCY` / `NOT VERIFIED` |
| API DD #12 and live schema approval. | Visibility/URL/database fields remain unconfirmed. | `Draft — Needs Confirmation`; live schema `NOT_VERIFIED` |

### Phân loại cuối

- `DD BLOCKED`: MIME-specific preview/expiry presentation and some catalog/API DD fields still require synchronization.
- `IMPLEMENTATION PARTIAL`: access, URL and primary state/navigation behavior are implemented; media-specific preview remains absent.
- `RUNTIME NOT VERIFIED`: source review does not prove live schema/storage/API or deployed browser behavior. Tests were not run in this task.

## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
