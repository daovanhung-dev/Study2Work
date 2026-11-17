# Kế hoạch màn hình — SH-07 Theo dõi tác vụ bất đồng bộ

> **Trạng thái kế hoạch:** `STATIC_REVIEW_COMPLETE`; DD vẫn `BLOCKED`, implementation `BLOCKED`, runtime `NOT VERIFIED`. Plan được tạo trước DD, marker map và ảnh chú thích. **Phiên:** chỉ xử lý SH-07.

## 1. Mục tiêu, phạm vi và nguồn

- Hoàn thiện đặc tả cho shared operation-tracking surface theo inventory, giữ nguyên ảnh/HTML mẫu, tạo DD, marker map và ảnh chú thích trong thư mục SH-07, cập nhật tracker/worklog.
- Không triển khai API/runtime, không thay đổi Study contract, không tự quyết định operation ID, status enum, owner policy, polling cadence, TTL, result schema hoặc route quay về.
- Inventory đề xuất `/operations/:operationId`, tham chiếu AC-12/25/36/38 và API #18; liên kết tới ST-07, ME-15, AD-21, AD-25. Ưu tiên W4/P2; catalog hiện ghi `D` và block vì operation status/ID mapping chưa thống nhất.
- Nguồn giao diện: `screen.png` (1503×1600) và `code.html`. SHA-256 trước chỉnh sửa: PNG `eb5329637c5942f0ac43b439b2dece09cac071565d1b300efa3405f9628ce110`; HTML `2fb2fdab9c88b9b31c5cde9e61b771e233075ac3339d2d6ed1259f0bd99fa3a3`.
- Historical snapshot (2026-11-08): Study Web editable source/package were recorded as absent. Current re-audit (2026-11-16): Angular app source and router exist; `/operations/:operationId` and a SH-07 feature caller are still absent. `API_018` remains `UNWIRED` in the client descriptor, so the generic transport blocks it. `.agents/web-work/study/AGENTS.md` and `INDEX.md` are context pages, not route/runtime evidence. `.agents/web-study/design.md` is the intended UI target. Do not use `dist/` as source/router evidence.
- API contract: `docs/lists/list_api.md` rows #17/#18/#63/#64/#93/#96/#103, reusable `Operation` schema và operation-tracking section; API #18 DD dưới `apps/study-server/docs/dd/18_operations/` Draft/Needs Confirmation.
- Historical source scan (2026-11-07): API #18 route/module/query/test and #17/#103 producers were not found. Current source re-audit (2026-11-16): route #18, Shared module and query are present; a dedicated HTTP test module passes 8 cases. The handler currently looks up only notification operations and binds the authenticated owner ID. The Study schema still has no generic `operations` table; migration 009 adds notification `operation_id UUID` and delivery outbox storage only. #17 remains fail-closed and #103 remains absent. `contracts/openapi/study/README.md` is still a placeholder. None of this verifies live schema or deployment.
- Cross-boundary wiring: workflow/contract registry đã tra trong `.agents/context-manifest.json`; `study-openapi` là `NOT_FOUND`, `cross-scope-contract` được wire; `createDD-markdown` explicitly excludes `web-ui-only-dd`, nên SH-07 screen DD không áp API-sheet template.

## 2. Expected behavior và current evidence

| Hạng mục | Expected theo inventory/contract/AC | Current evidence và xử lý trong DD |
|---|---|---|
| Route/entry | Shared route `/operations/:operationId`; chỉ vào từ response operation ID do server xác nhận; không tự sinh ID. | Angular app/router hiện có nhưng chưa đăng ký SH-07 route hoặc caller. `API_018` client descriptor vẫn `UNWIRED`. Script prototype đọc path rồi dùng UUID mẫu nếu thiếu param; đây không phải route/runtime source. |
| API #18 | `GET /api/v1/operations/{operation_id}`, Bearer JWT, `ApiEnvelope<Operation>`, 200 `DESIGN_OPERATION_RETRIEVED`; 401/403/404/500. | Backend route, Shared module/query và HTTP tests hiện có. OpenAPI/path validator dùng UUID; API catalog row vẫn dùng `int64`. Current query chỉ đọc notification operation, giới hạn theo owner, với state `QUEUED`/`FAILED`/`SENT`. API DD vẫn Draft; client descriptor/caller chưa wired. |
| Response/status | Reusable Operation gồm `id`, `kind`, `status`, `owner_id`, `submitted_at`, `updated_at`, `completed_at?`, `result?:Payment`. | OperationKind/OperationStatus values, lifecycle, source, result theo loại job và terminal states chưa định nghĩa. UI liệt kê 5 status chỉ là static reference; notification API source dùng QUEUED/FAILED/SENT. |
| Producers | API #17/#63/#93/#103 có thể phát operation theo tracking section. | #63 trả 202 + `data:Operation` UUID/QUEUED; #93 current source trả 202 + `data:Notification`, `meta.operation_id` UUID và `notification_ids`; #17/#103 routes absent. Tracking summary conflicts with #93 row/source. |
| Notification status | ME-15/AD-21 có thể liên kết SH-07 qua operation ID. | #64/#96 tra cứu theo `notification_id:int64`, không phải UUID `operation_id`; #64 dựng Operation riêng từ notification/outbox, #96 trả Notification. Không thay API #18 bằng các endpoint chuyên biệt này. |
| Authorization | API #18 yêu cầu Bearer; role/ownership giới hạn operation owner (AC) hoặc owner/Admin (tracking summary). | Current #18 source allows `STUDENT`, `MENTOR`, `ADMIN` and binds lookup to authenticated owner ID; missing/non-owned row maps to 404. This matches AC diagram owner-only lookup but does not resolve the catalog owner/Admin discrepancy or 403/404 policy. |
| Polling/result/expiry | List row yêu cầu dừng theo terminal state; lifecycle và origin flows cần trạng thái thật. | Không có interval, retry/backoff, SSE route, TTL, terminal enum, result URL/error schema được chuẩn hóa. HTML modal hints 3000ms/backoff hoặc SSE; không biến thành yêu cầu runtime. |
| Navigation | Return tới caller flow ST-07/ME-15/AD-21/AD-25, hoặc action được phê duyệt. | HTML CTA về GS-01/SH-01 với `href="#"`; safe-return data/route chưa định nghĩa. Ghi discrepancy/blocker, không tự đổi flow. |

Source checkpoints revalidated: API #18 route uses a UUID path in OpenAPI, passes the diagram-listed role tuple to the shared auth guard, queries notification rows by operation UUID plus owner ID, and has 8 dedicated HTTP tests. It is source/test verified, not live-deployment verified or a generic operation store. API #63 `OperationResponse.id` is UUID and its 202 response carries `data:Operation` plus notification IDs in metadata; API #64 accepts `notification_id` and derives a notification-specific Operation-like response (`QUEUED`/`FAILED`/`SENT`) after Mentor ownership checks. API #93 returns the first `Notification` in `data` and UUID `operation_id` plus notification IDs in `meta`; API #96 accepts `notification_id` and returns `Notification`. These source shapes do not resolve the generic API #18 contract. Relevant code is in `apps/study-server/app/modules/{shared/api_18_operations,mentor/api_63_mentor_notifications_create,mentor/api_64_mentor_notification_status,admin/api_93_admin_notifications_create,admin/api_96_admin_notifications_status}/`; route registration is in `apps/study-server/app/api/v1.py`. The API #18 open questions and catalog/AC discrepancies remain unchanged.

## 3. Kế hoạch element và marker

Ảnh mặc định có **35 marker**, theo pixel gốc 1503×1600. Mỗi marker map duy nhất tới Element ID cùng số. Marker target chỉ đánh dấu component nhìn thấy trong ảnh mặc định; Contract Spec modal hiện `hidden` trong HTML nên được mô tả riêng trong DD nhưng không có marker trong ảnh mặc định.

| # | Element ID | Element/vùng cần đánh dấu | Target (x,y) ảnh gốc |
|---:|---|---|---:|
| 1 | `SH07-EL-01` | Brand/logo header | 150,38 |
| 2 | `SH07-EL-02` | Primary navigation group: Trang chủ/Khóa học/Tìm kiếm | 455,38 |
| 3 | `SH07-EL-03` | Link Đăng nhập | 1235,38 |
| 4 | `SH07-EL-04` | CTA Đăng ký | 1357,38 |
| 5 | `SH07-EL-05` | Icon người dùng trang trí | 1448,38 |
| 6 | `SH07-EL-06` | Specification Gate banner: title/status/API blocked/explanation | 500,120 |
| 7 | `SH07-EL-07` | Button “Xem Contract Spec” | 1333,144 |
| 8 | `SH07-EL-08` | Breadcrumb + proposed route | 256,251 |
| 9 | `SH07-EL-09` | Page title + supporting description | 274,307 |
| 10 | `SH07-EL-10` | System status badge | 1053,302 |
| 11 | `SH07-EL-11` | Environment badge `STAGING-MOCK-07` | 1318,302 |
| 12 | `SH07-EL-12` | Target Reference Route + displayed Operation ID | 334,486 |
| 13 | `SH07-EL-13` | Copy Operation ID button | 591,490 |
| 14 | `SH07-EL-14` | “Chờ tích hợp backend / Gated (Design Only)” badge | 727,457 |
| 15 | `SH07-EL-15` | Metric “Loại tác vụ” | 203,574 |
| 16 | `SH07-EL-16` | Metric “Nguồn gốc khởi tạo” | 439,574 |
| 17 | `SH07-EL-17` | Metric “Tiến độ thực thi” / no fake % | 680,574 |
| 18 | `SH07-EL-18` | Anti-faking policy panel + three guardrail rows | 433,748 |
| 19 | `SH07-EL-19` | CTA “Quay lại danh sách khóa học (GS-01)” | 251,909 |
| 20 | `SH07-EL-20` | CTA “Về trang chủ (SH-01)” | 576,909 |
| 21 | `SH07-EL-21` | Developer hand-off panel heading + `HANDOFF_STRICT` badge | 419,1012 |
| 22 | `SH07-EL-22` | Developer hand-off explanatory paragraph | 430,1101 |
| 23 | `SH07-EL-23` | Schema mismatch code fragment | 431,1264 |
| 24 | `SH07-EL-24` | Lifecycle contract heading/subtitle/icon | 1084,420 |
| 25 | `SH07-EL-25` | QUEUED reference card | 1112,532 |
| 26 | `SH07-EL-26` | RUNNING reference card | 1112,647 |
| 27 | `SH07-EL-27` | SUCCEEDED reference card | 1112,761 |
| 28 | `SH07-EL-28` | FAILED reference card | 1112,877 |
| 29 | `SH07-EL-29` | EXPIRED reference card | 1112,1000 |
| 30 | `SH07-EL-30` | Orchestration card heading | 1096,1145 |
| 31 | `SH07-EL-31` | Client → API Gateway → Queue/Worker architecture diagram | 1100,1310 |
| 32 | `SH07-EL-32` | Diagram caption | 1120,1448 |
| 33 | `SH07-EL-33` | Footer brand + platform descriptor | 201,1560 |
| 34 | `SH07-EL-34` | Footer navigation group | 840,1560 |
| 35 | `SH07-EL-35` | Copyright text | 1360,1560 |

Marker visual target: adjacent blue circle `#0B5F8A`, white bold `#n`, white stroke, about 32px diameter. Place badges in margins/card corners without leader lines so they do not cross or cover labels/status text. Visual audit found marker #23 touching the diagnostic code line; move its circle into the left page gutter aligned with the schema-conflict card while keeping the target coordinate and element mapping. Keep original image bytes unchanged.

## 4. Event plan

| Event ID | Trigger/element | Input | Processing and output |
|---|---|---|---|
| `SH07-EV-01` | Route entry `/operations/:operationId` | Path segment and navigation origin from caller | Normalize only after contract selects UUID or int64; no client-generated/default ID. Current prototype fallback is explicitly rejected for production. Current route shows design gate only and does not request API. Missing/invalid route behavior remains a contract/router blocker. |
| `SH07-EV-02` | Click “Xem Contract Spec” #7 | No payload | Current inline handler toggles `.hidden` on modal; no network. Target modal must be semantic dialog with focus management, but exact accessibility behavior is an implementation requirement, not API behavior. |
| `SH07-EV-03` | Click close icon or “Đóng cửa sổ” in modal | No payload | Current handler adds `.hidden`; modal closes without API/cache effects. Escape/backdrop behavior is absent and remains an accessibility decision. |
| `SH07-EV-04` | Click copy button #13 | Displayed ID string | Current code copies text content. Production can copy only a server-issued ID in the canonical accepted type; never copy fallback/sample values. Clipboard failure/success feedback is absent in prototype and needs UI acceptance. |
| `SH07-EV-05` | Future initial status read after API #18 and ID/owner contract are approved | Bearer token; `operation_id` path; no body/query | `GET /api/v1/operations/{operation_id}`. Backend route/module/query and source-level HTTP tests exist; the client descriptor is `UNWIRED` and no SH-07 caller exists. Do not call until the producer and response contracts are approved. |
| `SH07-EV-06` | Future status refresh / poll | Last accepted response and approved refresh policy | No timer or SSE implementation is authorized by source. Prototype's 3000ms/backoff and `/operations/{id}/stream` are design-only. Owner must choose poll/SSE, cadence, backoff, visibility/reconnect and stop rule; only then map statuses/cache/terminal state. |
| `SH07-EV-07` | Click recovery CTA #19 | No payload; proposed GS-01 route | HTML target is a `#` placeholder; route `/courses` is a proposal. Caller/job context must not be silently discarded; keep disabled/gated until Product approves safe-return behavior. |
| `SH07-EV-08` | Click home CTA #20 or logo/header home | No payload; proposed SH-01 route `/` | Placeholder `#`; no API. Resolve route with Study Web router before enabling. |
| `SH07-EV-09` | Click header nav/login/register #2–#4 | Selected link key | Prototype anchors are `#`; route proposals `/`, `/courses`, `/courses/search`, `/login`, `/register` require actual router targets. No auth state or route guard is source-backed in Study Web. |
| `SH07-EV-10` | Click footer links #34 | Link label | Four prototype links use `href="#"` and have no confirmed destinations. Do not present as functional navigation until Product supplies approved routes. |

Không có download button trong default screen. `result_url`, `error`, fake progress, countdown và result actions trong modal/sample không được biến thành events mới nếu chưa có approved per-kind Operation result contract.

## 5. State, API and cross-screen checks

- Static source state: `DESIGN_GATE` / `GATED_UNAVAILABLE`; displays status `D`, mock environment and anti-faking copy; no API call. Five cards are design-reference cards, not current job data.
- Future API state machine is blocked: `INITIAL → LOADING → RESPONSE_VALIDATION → <approved status>` only after #18 is implemented. Do not normalize lowercase/uppercase or treat listed states as exhaustive until enum is approved.
- Catalog errors: 401 authentication, 403 access denied, 404 operation not found, 500 internal. Expected SH-05/SH-06/service-error destination must follow the shared Study route policy; 500/network/timeout must not become 404. Wrong-owner 403 versus 404 is still unresolved.
- ID producer trace: ST-06 uses #17 by contract but #17 is absent from current source; ME-14 #63 returns UUID Operation data and notification IDs, while ME-15 #64 takes notification ID; AD-20 #93 returns Notification data and UUID operation ID in meta, while AD-21 #96 takes notification ID; AD-25 #103 has no current source and returns Report in its API row. No generic current path joins these producer cases to API #18.
- Study OpenAPI is a placeholder; no live DB metadata/deployment evidence. The checked-in Work `operations` table is not a Study dependency and must not be used as a backing store.
- Visual guide: `.agents/web-study/design.md` targets local/system Inter, content width ~1120px, responsive nav/actions at all widths and >=44px controls. Prototype uses Plus Jakarta Sans/Material Symbols/Tailwind CDN, 1440px max width, 32px account `div`, hidden mobile nav, and diagnostics exposed in the user surface; record as design drift, don't mutate source assets.

## 6. Blockers and acceptance gate

1. `SH07-B01 GENERIC_OPERATION_CONTRACT`: route/module/query and source-level tests exist, but the implementation only reads notification outbox records; no generic Study Operation table, full lifecycle or per-kind result contract exists.
2. `SH07-D01 OPERATION_ID_TYPE`: API #18 row int64 vs UUID convention/schema/AC and producer #63/#93 UUID.
3. `SH07-D02 STATUS_AND_KIND`: enum/lifecycle/terminal states unresolved; notification-specific QUEUED/FAILED/SENT do not define generic status.
4. `SH07-D03 AUTHORIZATION`: owner-only vs owner/Admin and wrong-owner 403/404 semantics unresolved.
5. `SH07-D04 PRODUCER_AND_RESULT`: #93 row/source/summary disagree; #103 Report vs Operation result and `result?:Payment` mismatch; #17/#103 not source-backed.
6. `SH07-B02 POLLING_AND_RETENTION`: no cadence/retry/SSE/TTL contract; prototype-specific 3s, 24h, 15min are unsupported.
7. `SH07-B03 NAVIGATION_ORIGIN`: generic safe-return origin not specified; CTAs in source conflict with inventory linkage.
8. `SH07-B04 PROTOTYPE_ONLY_UI`: UUID fallback, mock environment, diagnostic claims and backend architecture copy cannot be presented as live user/job data.

- [x] `SH-07_PLAN.md` was created before DD/markers/annotation; source trace was revalidated before any DD or image edit in this session.
- [x] Original image and HTML hashes remain unchanged; source and annotated images are 1503×1600.
- [x] Annotated source has 35 ordered unique markers mapping exactly to 35 visible DD elements; hidden modal is excluded from default-image numbering. Visual review moved #23 into the left gutter so it does not cover the diagnostic code.
- [x] DD covers every visible element plus hidden modal controls, 10 event paths, state/error/navigation, security, accessibility, design-system drift and source links; re-audit corrected its stale Study Web subcontext status statement before final verification.
- [x] API #18 and producer sources are distinguished from design catalog; no API/field/enum/route behavior is invented.
- [x] Major unresolved contract decisions are blockers; set `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, `RUNTIME NOT VERIFIED` until approved evidence closes them.
- [x] Static ID/element/event/link/image/hash/whitespace audit and tracker/worklog update are complete; the 83 inventory IDs match the 83 tracker rows and the next handoff is GS-01.

## 7. Session result (fill after review)

- Historical result (2026-11-07): Study source/contract and marker trace was revalidated; the original static audit passed. Application tests/runtime were not run at that checkpoint.
- DD status: `DD BLOCKED` because API #18 and end-to-end operation ID/status/owner/producer contracts remain inconsistent or absent; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`.
- Next Screen ID: GS-01, the first unstarted W0 screen in the tracker, for a separate session. No other Screen ID is part of this session.

### Re-audit note (2026-11-07)

- Rechecked the Study Web context claim: `.agents/web-work/study/AGENTS.md` and `INDEX.md` exist and the manifest registers them as `study-web: UNWIRED`; editable app source and `package.json` remain absent. Corrected the DD, this plan and tracker to distinguish context docs from runtime evidence.
- Static verification passed: 83 inventory IDs match 83 tracker rows; all 35 ordered markers map to 35 DD element rows, marker coordinates are in bounds, the SVG parses with labels 1–35, 10 unique event IDs are present, and all 23 local DD/plan links resolve. Original `screen.png` and `code.html` hashes are unchanged; both source and annotated images are 1503×1600. The annotation was viewed and marker #23 is clear of the diagnostic text.
- Tests, browser/runtime, live database and deployment were not run or verified. Status remains `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`.

### Current source re-audit (2026-11-16)

- Study Web app/router exist, but SH-07 has no route/caller and the `API_018` client descriptor remains `UNWIRED`.
- Study Server API #18 route/module/query are present and the auth role argument defect is fixed. The focused suite passes 8 tests and full Study suite passes 1492; both use local source/fake DB tests and do not verify deployment/live schema.
- Generic operation storage/lifecycle/result, producer handoff, UUID/int64, owner/Admin, polling/retention and safe-return questions remain open. Keep `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, and SH-07 `RUNTIME NOT VERIFIED`.
