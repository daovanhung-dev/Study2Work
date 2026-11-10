# ST-09 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `ST-09-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Đề cương, tiến độ từng bài và CTA tiếp tục học.
- Gate/status (giữ nguyên): **D**; #09 local source-backed/public (API DD Draft, int64 range check absent); #20/#37 and #22–#24 not source-backed; **BLOCK:** Chưa có contract course-learning tree đầy đủ
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

### Trích từ DD nguồn: Ràng buộc UI, accessibility và design system

- Asset HTML dùng Plus Jakarta Sans, primary #004AC6 và max width 1440px. Study UI guidance target dùng Inter/system, ocean primary #0B5F8A và content width khoảng 1120px. Giữ đây là design discrepancy, không tự sửa screenshot.
- Header nav có hidden md:flex nhưng không có mobile menu trong HTML. Responsive behavior ở viewport nhỏ chưa được thể hiện.
- Thẻ WCAG nói warning dùng role=alert và aria-live=polite, nhưng markup chỉ in các tên thuộc tính như explanatory text; warning element không có attributes tương ứng. Không coi accessibility requirement đã được implement.
- Khi có source frontend, cần kiểm chứng keyboard focus, current-page semantics, contrast, touch target, screen-reader announcement, heading order và responsive navigation. Đây là verification cần thiết trước khi DD READY/implementation acceptance.
- Static developer handoff cards/tokens/WCAG claims hiện là visible UI content trong mockup; cần quyết định chúng có thuộc sản phẩm hay chỉ phục vụ design handoff.

### Trích từ DD nguồn: F. Blockers và tiêu chí nghiệm thu

### Blockers

| ID | Blocker | Owner/decision needed |
|---|---|---|
| ST09-B01 | API #20 route/module/test absent; response ApiEnvelope<UserProfile> không biểu diễn course membership; status/paging semantics chưa chốt. | API/backend/Product |
| ST09-B02 | API #37 route/module/test absent; response type, aggregate formula, zero/partial/completion semantics chưa định nghĩa. | API/backend/Product |
| ST09-B03 | API #09 public current projection includes lesson content/video_url and has no enrollment/access check. | Backend/security/product: approve public projection or define protected access contract |
| ST09-B04 | APIs #22–#24 absent; lesson access/start/content sequence and error semantics unresolved. | Backend/product |
| ST09-B05 | Expected loaded course/lesson/progress states and controls absent from PNG/HTML; ST-21 control absent. | Product/design |
| ST09-B06 | Study Web editable source/router absent; ignored dist root-only, provenance/serving unknown. | Frontend/build/deployment owner |
| ST09-B07 | ST-08 course card handoff and route guards/session behavior unverified. | Frontend/product |
| ST09-B08 | HTML’s static API badge, token/accessibility claims disagree with source/guidance; CTA lacks lessonId; footer/legal destinations unresolved. | Product/design/frontend |
| ST09-B09 | API #09 declares `course_id:int64`, but the source validator does not explicitly enforce signed-int64 bounds. | API/backend: align path-range behavior with the declared contract |

### Acceptance checklist

- [x] 20 visual marker IDs have one-to-one element descriptions in the same order.
- [x] Original screen.png remains unchanged; HTML source remains unchanged.
- [x] Main route, actors, relationships and evidence states are recorded.
- [x] All identified static and expected events have input, processing, output and gaps described.
- [x] #09 is traced against current route/module/query/model/test source; test source read, not run.
- [x] #20/#37 and #22–#24 are distinctly marked NOT_FOUND in current source.
- [x] Authorization risk and public #09 payload are documented.
- [x] API #09's current registered source is distinguished from its Draft DD and stale mockup badge; path-range discrepancy is recorded.
- [ ] Loaded course tree, per-lesson progress, loading/empty/error states are designed and approved.
- [ ] API #20/#37 payload, rules and error contracts are finalized and source-backed.
- [ ] Lesson access/start/content APIs and ST-10 handoff are finalized.
- [ ] ST-21 navigation control and progress formula are finalized.
- [ ] Study Web route/session/API integration is implemented and runtime-verified.
- [ ] Design-system and accessibility discrepancies are resolved or explicitly approved.

**Decision:** DD BLOCKED; not implementable without product/API decisions in B01–B05 and B09. Implementation BLOCKED by missing frontend and backend wiring. Runtime NOT VERIFIED.

## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
