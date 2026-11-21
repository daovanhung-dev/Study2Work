# ME-01 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `ME-01-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Card khóa đang phụ trách, submission chưa chấm, yêu cầu hỗ trợ.
- Gate/status (giữ nguyên): **D**; **BLOCK:** Role introspection Mentor chưa có
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

### Trích từ DD nguồn: 8. Điều hướng, quyền và dữ liệu truyền

| Từ | Đích dự kiến | Dữ liệu truyền | Điều kiện / trạng thái |
|---|---|---|---|
| Header/course “Tất cả lớp học” | ME-02 `/mentor/courses` | Không cần ID | Inventory link; route runtime `UNWIRED`. |
| Course “Workspace” | ME-03 `/mentor/courses/:courseId` | `Course.id` từ API #46 | Screenshot CTA; direct route cần được xác nhận; server vẫn phải kiểm ownership. |
| Course content-tree icon | ME-06 `/mentor/courses/:courseId/content` | `Course.id` từ #46 | Label “Xem cây nội dung”; target/flow chưa được link ở dòng ME-01 inventory. |
| Header/grading “Xem tất cả” | ME-09 `/mentor/submissions` | Không cần ID | Inventory link; route runtime `UNWIRED`. |
| Submission preview action | ME-10 `/mentor/submissions/:submissionId` hoặc ME-09 trước | `Submission.id` nếu direct | Asset cho ME-10; AC-23/list flow qua ME-09; `DISCREPANCY`, Product quyết định. |
| Header/support “Mở Workspace” | ME-11 `/mentor/support` | Không cần ID | Inventory link; route runtime `UNWIRED`. |
| Support preview action | ME-12 `/mentor/support/:requestId` hoặc ME-11 trước | `SupportRequest.id` nếu direct | Asset cho ME-12; AC-24/list flow qua ME-11; `DISCREPANCY`, Product quyết định. |
| Notifications, schedule, announcement, footer | Chưa xác định | Không truyền data từ sample | Không tạo route hoặc external link. |

Các API list kiểm soát owner/role ở server. Không xem ẩn menu hoặc parse role ở client là authorization. Không có xác nhận refresh/logout/return-to-route policy cho dashboard.

### Trích từ DD nguồn: 9. Bảo mật, quyền riêng tư và accessibility

- Chỉ gọi API với Bearer token theo cơ chế Study Web được duyệt; không đưa token vào URL/query, HTML hoặc log. Current browser token storage không xác minh.
- Mọi request Mentor phải để server guard kiểm role/owner. Không dùng client course card để suy ra quyền ME-03/ME-06.
- Submission body/files và support messages là dữ liệu learner. #54 trả tới 20 submissions/page, #58 trả toàn bộ support threads không pagination; dashboard cần data minimization/summary decision trước khi tải và render nội dung nhạy cảm ở overview.
- Không sử dụng tên, avatar, score, deadline, rating, email/hotline hay meeting URL trong ảnh làm dữ liệu production.
- Khi implement, áp dụng Study Web guide: semantic button/link, accessible name cho icon-only, visible focus, keyboard tab order, text/error association, WCAG AA, target tối thiểu 44×44px, reflow 320px, `prefers-reduced-motion`. Prototype input chỉ có placeholder, icon button là 40px và không có handler; cần kiểm tra lại khi có app source.

### Trích từ DD nguồn: 10. Blockers và quyết định cần bổ sung

| ID | Cần xác nhận | Evidence / impact |
|---|---|---|
| ME01-B01 | Mentor shell bootstrap: role/session source và 401/403 handoff. | Current app/router absent; #04 profile endpoint Student-only. |
| ME01-B02 | Course scope: direct owner hay assigned Mentor; các course status nào hiển thị. | #46/#54 current query chỉ `courses.mentor_id`; #46 status allowlist DRAFT/PUBLISHED. |
| ME01-B03 | Dashboard course preview/card fields and count. | #46 lacks track, progress, enrollment/lesson counts; resolve page size 3 vs API default20. |
| ME01-B04 | Define “pending grading”, overdue policy and course/assignment/student display contract. | #54 raw status string, fixed20/page and response lacks display fields/deadline/rubric. `Rubrics V2` badge unsupported. |
| ME01-B05 | Support overview projection, pending/unread metric, ordering/preview, pagination. | #58 returns every full thread; no subject, unread, SLA, course title or last activity field; table/schema choices derived and live schema unverified. |
| ME01-B06 | Rating source and aggregation/period/denominator. | No referenced rating API or source field. |
| ME01-B07 | Mentor calendar/availability/on-call provider, schedule mutations and meeting-link policy. | No endpoint/provider/ID/URL contract. |
| ME01-B08 | Academic announcement API, term/source, read state and link targets. | No list API among screen references; #63/#64 have different send/status purposes. |
| ME01-B09 | Notification badge and Mentor profile data/navigation. | No inbox/unread endpoint; #04 is Student-only; #46 embeds mentor info only on course items. |
| ME01-B10 | CTA routes for submission/support cards and content-tree icon. | Image CTA direct ME-10/12; AC/inventory route through ME-09/11. Code links are `#`. |
| ME01-B11 | Loading/error retry/cache/timeout UX and independent widget composition. | Inventory requires independent errors; no frontend implementation or accepted design for these states. |
| ME01-B12 | Reconcile prototype visual/accessibility tokens with Study Web design guide. | `#004ac6`, remote Plus Jakarta Sans/CDN, broad gradient and 40px button vs guide tokens. |

Do not close these blockers by inventing APIs, fields, tables, metrics, policy, routes or status mapping. Once decisions are supplied, update this DD and relevant screen dependencies.

## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
