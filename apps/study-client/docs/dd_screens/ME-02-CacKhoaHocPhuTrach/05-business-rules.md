# ME-02 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `ME-02-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Course list theo ownership/assignment, status/page/size, action manage.
- Gate/status (giữ nguyên): **D**
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

### Trích từ DD nguồn: 8. Security, accessibility and design notes

- Never infer ownership in the browser; backend auth/scope remains authoritative. #46 gets principal from JWT; the UI cannot select `mentor_id`.
- `courses.mentor_id` direct-owner logic does not satisfy AC-21 “owns/assigned” if assignment is a separate concept; keep assigned courses unavailable until source/API supports them.
- Preserve 401/403 distinctions in API calls; no client retry policy, refresh flow, redirect or token storage is source-backed here.
- Intended Study Web design guide uses Ocean primary `#0B5F8A`, Inter/system font, controls at least 44px, content width about 1120px and keyboard/focus/reflow expectations. Prototype uses primary `#004ac6`, remote Plus Jakarta Sans and Tailwind CDN, 32–40px controls and max-width 1440px. Resolve before implementation; do not treat prototype style as approved exception.
- The header/profile and support/footer content includes sample personal/contact/brand/certification claims. Keep accessible labels, links and externally displayed contact/credentials out of live UI until ownership and content are approved.
- Require semantic buttons/links, visible focus, accessible names for icon-only controls, form labels/errors, responsive reflow and reduced-motion handling according to the design guide. Current HTML controls lack many of these semantics/labels.

### Trích từ DD nguồn: 9. Blockers and acceptance

| ID | Required decision/source | Impact |
|---|---|---|
| ME02-B01 | Confirm course scope: direct ownership vs assignment, identity/schema and matching access policy across #46/#47/#48/#49/#65/#66. | Main list may omit legitimately assigned courses or downstream routes may disagree. |
| ME02-B02 | Implement/identify Study Web Mentor shell, role/session lifecycle and `/mentor/courses` route. | No frontend runtime or implementation route. |
| ME02-B03 | Provide/approve KPI definitions and data sources for course/learner totals, average completion, Capstone, rating and submission counts. | Screenshot shows sample values without current screen response fields. |
| ME02-B04 | Decide search, course-code, level, semester and sort contracts. | #46 cannot support these controls. |
| ME02-B05 | Define mapping between UI status labels and `DRAFT|PUBLISHED`; decide whether all statuses display by default. | Current labels cannot be safely serialized as #46 status. |
| ME02-B06 | Reconcile API #46 DD snapshot/catalog status with current route/module/test source; confirm source is intended API contract. | Existing DD says API is absent; current source says present. Deployment remains unverified. |
| ME02-B07 | Confirm direct CTA targets for ME-06/ME-09/ME-16/ME-18 and global report; decide card-level context and access handoff. | Image links disagree with ME-02 inventory; report route lacks source. |
| ME02-B08 | Decide page-size initial value, reset behavior on filter/sort, out-of-range handling, timeout/retry/stale-response/cache policy. | Screenshot selects 10; API default is 20. |
| ME02-B09 | Approve Study design-token/accessibility reconciliation or provide revised screen assets. | Current mockup conflicts with intended Study Web guide. |
| ME02-B10 | Confirm all data fields/content claims such as code, level, ratings, lesson/lab counts, module labels, partner/academic/footer claims. | Do not expose sample/mock data as live product content. |

### Acceptance checklist

- [x] 47 marker JSON entries are sequential/unique and each has a corresponding `ME02-EL-xx` row.
- [x] Source image and HTML preserved; annotated image and marker overlay visually inspected.
- [x] #46 route → guard → validation → query/count → mapping → response/error and relevant test source traced; tests were not run.
- [x] Expected behavior and current source differences are kept separate; `DISCREPANCY`, `UNWIRED` and `NOT_FOUND` claims are explicit.
- [x] Element/event/state/navigation matrix links every source marker to the DD.
- [ ] Resolve ME02-B01–B10 and review the resulting approved behavior before marking `DD READY`.
- [ ] Frontend implementation/runtime verification; not performed in this documentation session.

## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
