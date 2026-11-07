# ST-22 — Plan chi tiết

**Screen ID:** ST-22
**Tên:** Thành tích và chứng nhận (Page)
**Route trong inventory:** `/student/achievements`
**Actor:** Student
**Kế hoạch:** PLAN COMPLETE — lập trước marker map và DD.
**DD dự kiến:** BLOCKED bởi award rules, response projection, filter/pagination và proof/certificate actions chưa có contract.
**Implementation/runtime:** Study Web UNWIRED; Student API #38 route/module/query/test NOT_FOUND.

## 1. Mục tiêu và phạm vi

- Đặc tả ST-22 trong phiên này; liên kết ST-20 overview và ST-09 course context theo inventory.
- Giữ nguyên `screen.png` và `code.html`. PNG 803×1600 là loaded-state visual đủ dùng làm annotation source; HTML là static no-achievement fallback nên không dùng thay ảnh.
- Đánh số các nhóm UI nhìn thấy trong PNG theo thứ tự đọc. Dự kiến 46 nhóm: header/breadcrumb, trust hero, metrics, credential cards, competencies, next-certificate panel, integrity callout và footer. Marker group gộp các nội dung có chung component/card; mỗi ID sẽ map đúng một hàng DD.
- Đối chiếu API #38 theo catalog: GET `/api/v1/users/me/achievements`, Student Bearer, `course_id?:int64`, response `ApiEnvelope<Page<Achievement>>`, errors 401/403/500. Không thêm query pagination, response fields, endpoint hoặc certificate/proof API.
- Ghi rõ mọi giá trị/tuyên bố trong screenshot (GPA, reputation, percentile, crypto/On-Chain proof, QR/PDF/LinkedIn, next-certificate readiness) là sample/UI claims nếu không có contract/source mapping.
- Không tự xác nhận blockchain/credential validity, cấp chứng nhận, tính competency awards, hoặc cho rằng #38 trả các summary metrics.

## 2. Bằng chứng và ranh giới source

### Expected behavior

- Inventory ST-22: `/student/achievements`, AC-18, API #38; danh sách achievement theo course; chỉ hiển thị award được backend xác nhận; không tự cấp chứng chỉ; links ST-20/ST-09; states `loading/empty/earned/error`.
- API catalog #38: Student Bearer JWT; optional `course_id:int64`; `ApiEnvelope<Page<Achievement>>`; Achievement logical fields `id`, `code`, `title`, `awarded_at`, `course_id?`; success 200 `DESIGN_RESOURCE_RETRIEVED`; errors 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 500 `DESIGN_INTERNAL_ERROR`.
- AC-18 mô tả đọc achievement unlocked sau progress/course flow. Không định nghĩa achievement criteria, persistence, proof/certificate fields, course filter semantics hoặc Award/Revocation lifecycle.
- Cross-screen orchestration remains a `DISCREPANCY`: ST-20 inventory requires #21 and #38 independently, while AC-18 sequences #21 → #37 → #38. Keep ST-22's #38 responsibility and screen links without choosing page-entry timing or flow order.
- API #38 DD `Draft — Needs Confirmation`; Sáu câu hỏi mở trong Open Questions gồm: unlock criteria; definition/projection; `course_id` semantics/access; pagination/order; empty page; query parse/domain validation.

### Current behavior

- `screen.png` 803×1600 là loaded visual có header/profile, learning context, ledger status, hero cryptographic trust copy, bốn summary metrics, hai certificate cards với GPA/proof hash/QR/social/PDF actions, năm competency cards, next-certificate readiness, academic integrity note và footer. Giá trị hiển thị là ảnh thiết kế; không có payload source xác nhận chúng.
- `code.html` là static empty fallback: header/nav, breadcrumb, title/description, empty card “Chưa có thành tích để hiển thị.”, copy “Bạn chưa có chứng nhận hoặc huy hiệu nào được ghi nhận…” và link quay lại tiến độ. Có hai script tag cho Tailwind CDN và inline Tailwind config, cùng ba remote Google Font imports (Plus Jakarta Sans); không có API fetch/XHR, form/input, data binding, auth guard hoặc app event handler. PNG có loaded cards/search controls và nhiều hành vi nhìn thấy nhưng HTML không có chúng.
- Current Study Web không có editable source/package/router/Student route; ignored `dist` chỉ có root `/`, không có `/student/achievements`; serving/deployment chưa xác minh.
- API #38 Student route/module/query/test không có trong current Study Server source. Mentor/API #65–#67 không phải endpoint achievements và không thay thế #38.
- DB guide ghi `achievements` là logical concept được contract nhắc nhưng không có physical table trong ERD hiện tại; legacy/V1-PILOT SQL không định nghĩa achievement table/award registry. DB guide nói có thể tính từ dữ liệu hiện có nhưng không cung cấp rules. Đây là design evidence, không live-schema proof.

### Discrepancies

- PNG là loaded state nhiều dữ liệu/CTAs; HTML chỉ là empty state. Không biết PNG là approved target, sample mockup hay aspirational proposal.
- `Page<Achievement>` chỉ định nghĩa achievement identity/title/time/course; không xác nhận certificate file, proof hash, QR, GPA, points, ranking, competencies, streak, next-cert readiness hoặc blockchain proof.
- API `course_id` filter là optional nhưng không nêu scope, global award inclusion, ownership/enrollment policy; screenshot competency filters (All/Specialization/Community) không tương đương với `course_id`.
- Response là Page nhưng request không có page/size/sort; empty shape/order/default/count unresolved.
- Study Web/app route và API #38 runtime absent.
- PNG/HTML dùng royal-blue/gradient styling và HTML dùng remote CDN/font, `max-w-[1440px]`, cùng primary config `#004AC6` pha với `#0B5F8A`; Study Web guide yêu cầu không thêm remote font/CDN, ưu tiên Inter/system, semantic ocean tokens, content width khoảng 1120px và surfaces tiết chế. Cần alignment với intended target; không sửa source image/HTML trong DD task.

## 3. Source trace cần thể hiện trong DD

```text
Expected inventory: ST-20 / ST-09 → ST-22 GET #38 (optional course_id) →
  render only server-confirmed earned achievements.
AC-18: Student logged in → progress/course flow → read unlocked achievements.
Current: Student #38 route/module/query/test absent; Study Web route absent;
  PNG is populated sample; HTML is a static no-achievement fallback.
```

- #38 is GET/read-only, no mutation/award side effect.
- Preserve catalog response `ApiEnvelope<Page<Achievement>>`; no certificate/proof schema is implied by `Achievement`.
- Do not add `page`, `size`, `sort`, 404 or 422. Keep only catalog error codes 401/403/500.
- Do not treat Page `total` as a metric for the screenshot's “14 skills” without category/source definition; do not derive points, rank, GPA, course completion, ISO compliance, cryptographic validity or award date.
- Certificate view/download/share/QR verification, “copy certificate hash”, next course/credential CTA and competency filtering have no API or route contract in this screen's source.

## 4. Planned marker coverage

The expected visible groups (confirm against PNG before writing final map):

1–8. Header brand/nav/search/account controls; learner context/status; breadcrumb and ledger-node status.
9–12. Trust-layer hero, title/copy, verification sample card and copy control.
13–16. Certificate count, skill-badge count, reputation points and percentile metrics.
17–28. Credential section heading/description and two certificate cards, each split into identity/institution/content, proof/QR, and action groups.
29–35. Competency collection heading, filter chips and five visible competency cards.
36–40. Next-certificate progress, readiness/date, prerequisite group, CTA, academic-integrity/On-Chain link.
41–46. Footer brand, program/community/contact columns, certification seals and legal strip.

## 5. Event plan

1. Page entry/session/route and optional course context from an approved caller.
2. Load API #38 with Bearer Student; include `course_id` only if approved route/filter semantics provide one; no pagination fields.
3. Validate/map Page<Achievement> envelope and confirmed achievement fields.
4. Map summary metrics, which currently have no source/aggregation contract.
5. Map certificate cards; distinguish generic Achievement from certificate/proof payload not present in #38.
6. Competency filter chips; current API only supports `course_id`, not competency taxonomy.
7. Copy sample certificate/proof identifier; no clipboard value/proof API contract.
8. View original credential; destination/asset/access contract absent.
9. Download PDF; file URL, ownership, format and generation route absent.
10. LinkedIn share; consent/data/destination contract absent.
11. Open QR/verify proof; trust authority and verifier route absent.
12. Next-certificate panel/readiness and continue CTA; no eligibility/progress/course mapping source in #38.
13. Academic-integrity/On-Chain Proof link; destination and proof contract absent.
14. Header, breadcrumb, footer navigation; only visible labels/hrefs can be documented.
15. API/session/network error handling, preserving only catalog error codes.

For every event row in the DD, identify the marker ID(s) or page/response lifecycle source, event type, and precondition. If the trigger exists only in the loaded PNG or lacks a contract, keep it explicitly design-only and blocked.

## 6. Blockers and no-invention rules

- API #38 has no source route/module/query/test, no award criteria, definition registry, persistence/projection source or revocation behavior.
- `Achievement` fields do not establish certificate metadata, asset/PDF, proof hash, QR, signature, GPA, skill taxonomy, ranking or next-certificate projection.
- `course_id` filter/access semantics are unresolved; screen taxonomy filters are not request parameters.
- Page request pagination/order/default and empty-page behavior are unresolved; no query additions.
- Static HTML empty state is not evidence of an API empty response. PNG sample is not evidence of actual earned records.
- Study Web route/runtime and visual status approval are absent. No implementation/runtime claim.

## 7. Verification plan

- Record PNG/HTML source hashes/dimensions and preserve both byte-for-byte.
- Use original PNG for annotation because it is a valid, complete image; document HTML mismatch. Check marker order/uniqueness/bounds, exact DD row mapping, SVG parse and visual readability/non-obscuration.
- Verify DD A–F, event sequence and element/type/precondition mapping, API method/path/auth/fields/statuses, no unauthorized query fields, link resolution, tracker counts/pointers and `git diff --check`.
- No tests or runtime API calls unless requested; run context validator only if a context page/manifest is changed.

## 8. Sources

- [Screen inventory / F07](../../../list_screen.md)
- [Original screenshot](./screen.png), [HTML companion](./code.html)
- [API catalog](../../../../../../docs/lists/list_api.md)
- [API #38 overview](../../../../../../apps/study-server/docs/dd/38_users_me_achievements/02_Overview.md), [request](../../../../../../apps/study-server/docs/dd/38_users_me_achievements/03_Request.md), [response](../../../../../../apps/study-server/docs/dd/38_users_me_achievements/04_Response.md), [open questions](../../../../../../apps/study-server/docs/dd/38_users_me_achievements/OPEN_QUESTIONS.md)
- [AC/API index](../../../../../../apps/study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md), [AC-18 diagram](../../../../../../apps/study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio)
- [DB table guide](../../../../../../apps/study-server/docs/diagrams/DB_UNICA_TABLES.md), [legacy Study DDL](../../../../../../infra/postgres/study-server/DB.sql), [V1-PILOT DDL](../../../../../../infra/postgres/02_study_db.sql)
- [Current Study route inventory](../../../../../../.agents/server-study/apis/declared-routes.md), [Study Web design target](../../../../../../.agents/web-study/design.md)

## 9. Kết quả xác minh

- Giữ nguyên hash `screen.png` (`cf11ec7d3e064b689c90853e275fcd65dcb828e644c495e1d9b004d58b974b4f`) và `code.html` (`abde69d2bc108b1b5bc9004896fff0ec016a61a7ec14a3a9e2b9f63ae10a5439`); kích thước gốc 803×1600, ảnh đánh số 907×1640.
- Rà soát ảnh theo các vùng trên/giữa/dưới; 46 marker rõ, theo thứ tự và không che nội dung quan trọng. Marker #42 được chuyển vào khoảng trống giữa hai cột footer sau lần rà soát đầu.
- Static consistency audit đạt 34/34: ID marker duy nhất 1–46 và nằm trong bounds; JSON khớp 46 hàng element; SVG parse hợp lệ; DD có A–F và đủ 15 event có input/process/output/exception; API #38/query/statuses, local links, tracker/pointers và whitespace kiểm tra đạt.
- `git diff --check` đạt. Không chạy tests hoặc API/UI runtime; runtime vẫn `NOT VERIFIED`.
- Kết luận: tài sản/tài liệu đã được rà soát tĩnh, nhưng `DD BLOCKED` và `IMPLEMENTATION BLOCKED` do các blocker tại mục 6; không đánh dấu `DD READY`.

## 10. Re-audit plan — 2026-11-07

- Current asset recheck confirms the original PNG/HTML and existing 46-marker annotation remain usable; preserve and verify their hashes rather than regenerate them.
- Correct the current-behavior note to distinguish Tailwind/config scripts from application behavior and identify remote font/CDN, absent form/listeners, and PNG-only controls.
- Add explicit marker/lifecycle element IDs, event type and precondition to each of the 15 DD events; retain design-only/blocker labels for sample actions.
- Expand the ST-22 inventory/global blocker text with the confirmed source-vs-design gaps, rerun static checks, and record this re-audit in the dated worklog. No context page changes or app tests are planned.
