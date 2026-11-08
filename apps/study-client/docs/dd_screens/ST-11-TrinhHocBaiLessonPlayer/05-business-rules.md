# ST-11 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `ST-11-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Video/nội dung, mục lục, nút complete, vị trí học, bài tiếp theo.
- Gate/status (giữ nguyên): **D; DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED:** asset hiện là fallback, không có player/progress/resource/next controls; #24–#27 chưa có Student route/module/query/test và API DD còn Draft; ST-10/ST-11 cùng gọi #24, ST-09 thiếu lessonId; #25 position/percent/state/storage/aggregate open; #26 `ApiEnvelope<Lesson>` vs Resource payload/visibility/URL open; #27 order/tie-break/no-next open; legacy BIGINT và V1-PILOT UUID DDL khác nhau; Study Web UNWIRED
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu và blockers

### Blockers

| ID | Blocker | Owner/decision |
|---|---|---|
| ST11-B01 | Inventory says player but supplied screenshot/HTML is only unavailable fallback; no loaded/player design or progress/resource/Next controls. | Product/design |
| ST11-B02 | ST-10/ST-11 both list #24; request owner/response handoff/cache and duplicate-fetch policy unresolved. | Product/frontend/API |
| ST11-B03 | ST-09/ST-10 do not currently provide lessonId; Study Web route/auth/router absent. | Product/frontend |
| ST11-B04 | API #24 absent from runtime; entitlement/JWT binding, publish scope, 403/404, payload/null/path and media URL access unresolved. | API/backend/security |
| ST11-B05 | API #25 absent; neither lesson-progress candidate maps `position`/`percent` as requested (a separate block-level `last_position_seconds` is not lesson mapping); percent/range, completion state, identity/upsert key, aggregate, transaction, autosave/throttle/retry/idempotency unresolved. | API/backend/database/product |
| ST11-B06 | API #26 absent; `ApiEnvelope<Lesson>` conflicts with Resource use-case; response cardinality/order/empty, entitlement, visibility, signed URL policy and URL owner unresolved. | API/backend/security/storage |
| ST11-B07 | API #27 absent; curriculum scope/order/tie-break, direct auth, 403/404, payload and last-lesson semantics unresolved. | API/backend/product |
| ST11-B08 | No Student route/module/query/focused test for #24–#27; Admin #82–#86 are not substitutes; Study Web remains UNWIRED. | Frontend/backend/build owner |
| ST11-B09 | Playback engine/control/accessibility/media security and error/loading/recovery UI are not designed or source-backed. | Product/design/frontend/security |

### Acceptance checklist

- [x] Original PNG and HTML hashes recorded; source files preserved.
- [x] All 14 visible marker groups have exactly one matching DD element row.
- [x] Expected inventory/AC behavior is separated from current static fallback behavior.
- [x] All declared APIs #24–#27 include method/path/auth/input/response/status and current source status.
- [x] Progress body fields and #25/#26/#27 contract mismatches/open questions are traced.
- [x] ST-10 duplicate #24 request and missing lessonId handoff are explicit.
- [x] Current links and absence of media/player/progress/resources/Next controls are documented.
- [ ] Loaded player, loading/error/denied/finished states and recovery UI approved/designed.
- [ ] #24–#27 canonical API rules, error mapping, auth, schema, update/URL/order semantics approved and source-backed.
- [ ] ST-10/ST-11 #24 ownership and lessonId handoff resolved.
- [ ] Progress throttle/autosave/position/completion/aggregate/retry/idempotency policy approved.
- [ ] Study Web route/player/API wiring and ST-12/13/17 navigation implemented and runtime-verified.
- [ ] Accessibility, media URL/security and responsive behavior verified in runtime.

**Decision:** DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED. Current artifacts do not define an implementable loaded lesson player, and API declarations do not close the progress/security contract.

### Trích từ DD nguồn: G. Ghi chú UI, accessibility và design system

- Source uses Plus Jakarta Sans via Google Fonts, max width 1440px, fixed 64px header, responsive gutters and a 48px minimum-height CTA. Study UI guide targets Inter/system without remote font import, content width around 1120px and semantic ocean tokens. Record as design discrepancy; preserve the supplied screenshot/HTML.
- CTA and navigation links have visible text labels. Material Symbol spans include text tokens such as `arrow_back`, `chevron_right`, and `play_lesson` without explicit `aria-hidden`/accessible-name attributes; verify announcement behavior when the app is implemented.
- Links include hover styles but no explicit `focus-visible` utility. Do not assume keyboard focus is absent; verify visible focus and tab order in the real runtime.
- The static fallback has a correctly visible H1 and text message, but there is no dynamic status announcement, loading/live region or player keyboard contract.
- Verify reflow at 320px, browser zoom, focus visibility, contrast, target size, screen-reader names, captions/transcript and reduced-motion behavior when actual player/UI is designed. Do not claim WCAG conformance from the asset.

## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
