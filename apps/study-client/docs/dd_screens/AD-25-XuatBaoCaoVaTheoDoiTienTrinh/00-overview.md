# AD-25 — Xuất báo cáo và theo dõi tiến trình · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `AD-25` |
| Module | Admin |
| Route | `/admin/reports/export` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **DD status:** BLOCKED — #103/#18, filter, operation, storage and download contracts leave implementation decisions unresolved.<br>; **Implementation status:** BLOCKED — Study Web, API #103, API #18 and export worker/storage flow are not wired in current source.<br>; **Runtime status:** NOT VERIFIED — this document is based on static design assets, catalog/AC/API Drafts and source inspection only. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [AD-25.md](../../screen_stitch/05_admin/AD-25_xuat-bao-cao-va-theo-doi-tien-trinh/AD-25.md), [AD-25_PLAN.md](../../screen_stitch/05_admin/AD-25_xuat-bao-cao-va-theo-doi-tien-trinh/AD-25_PLAN.md), [AD-25_markers.json](../../screen_stitch/05_admin/AD-25_xuat-bao-cao-va-theo-doi-tien-trinh/AD-25_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Chọn format/phạm vi/kỳ, theo dõi export và chỉ tải artifact sau khi có kết quả được xác nhận.
- In-scope: #103 optional `filters`/`format` → 202; `ApiEnvelope<Report>` vs `Operation` conflict. Chỉ gọi #18 với ID/type được BE xác nhận; tải xuống chỉ theo approved result URL.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-38 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Chọn format/phạm vi/kỳ, theo dõi export và chỉ tải artifact sau khi có kết quả được xác nhận. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #103, #18
- Liên kết màn hình dự kiến: [AD-24](../AD-24-BaoCaoTacDongCongDong/00-overview.md), [SH-07](../SH-07-TheoDoiTacVuBatDongBo/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | expected: queued/processing/ready/failed/expired; current: static/submit-blocked/download-disabled |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [AD-25 source screen.png](../../screen_stitch/05_admin/AD-25_xuat-bao-cao-va-theo-doi-tien-trinh/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/05_admin/AD-25_xuat-bao-cao-va-theo-doi-tien-trinh/screen_annotated.png))
- Luồng: #103 optional `filters`/`format` → 202; `ApiEnvelope<Report>` vs `Operation` conflict. Chỉ gọi #18 với ID/type được BE xác nhận; tải xuống chỉ theo approved result URL.
- Priority: P2; Gate/source status: **D**; **DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED:** #103/#18 catalog/Draft-only, no local route/query/model/test/worker/download source; response, GET retry, filter/format, permission, operation ID/access/status/result, AC-38 poll edge, storage/download and AD-24 filter handoff unresolved; Study Web UNWIRED

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# AD-25 — Xuất báo cáo và theo dõi tiến trình

> **DD status:** BLOCKED — #103/#18, filter, operation, storage and download contracts leave implementation decisions unresolved.<br>
> **Implementation status:** BLOCKED — Study Web, API #103, API #18 and export worker/storage flow are not wired in current source.<br>
> **Runtime status:** NOT VERIFIED — this document is based on static design assets, catalog/AC/API Drafts and source inspection only.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID / tên | AD-25 — Xuất báo cáo và theo dõi tiến trình xuất báo cáo |
| Mục tiêu | Cho Admin cấu hình format/phạm vi/kỳ xuất, yêu cầu export, theo dõi tác vụ và tải artifact nếu server xác nhận hoàn tất. Các bước sau khi submit đang là thiết kế, không có runtime source. |
| Actor | AC-38 yêu cầu Admin có quyền xem report/analytics. Catalog #103 khai báo Bearer JWT và role Admin. Mapping giữa report permission, JWT claim và backend guard chưa có trong report route vì #103 chưa được triển khai. |
| Route | `/admin/reports/export` là route candidate từ inventory. Study Web không có tracked editable source, package, router hay client hiện tại. |
| Liên kết | AD-24 → AD-25 là export branch; quay lại AD-24 là candidate. SH-07 là handoff candidate nếu có Operation ID đã được xác nhận. Các anchor/SH-07 callout trong prototype không điều hướng. |
| Điều kiện trước | Expected: Admin report permission và, nếu giữ bộ lọc AD-24, một cách được duyệt để chuyển `from/to/segment`. Current: trang HTML render tĩnh, không xác minh principal, query string, permissions hay previous screen. |
| Điều kiện sau | Expected: #103 có thể chấp nhận một export request; chỉ sau contract approval mới có Operation polling hoặc kết quả tải xuống. Current: submit bị `preventDefault()`, không tạo job, không thay panel và không gọi API. |
| API liên quan | #103 `GET /api/v1/admin/reports/community-impact/export` (catalog/API DD Draft; no current route). Conditional #18 `GET /api/v1/operations/{operation_id}` (catalog/API DD Draft; no current route). Không có download API được khai báo riêng trong row AD-25/#103. |
| Dữ liệu và state | UI prototype chọn `csv`, hai scope, `month`; API #103 chỉ khai báo `filters?:string` và `format?:string`. Không có mapping được duyệt từ controls sang query. Operation result/ExportAsset và lifecycle chưa thống nhất. |
| Bảo mật | Expected catalog: #103 Bearer JWT/Admin; AC-38 report/analytics permission; #18 owner-only versus owner/Admin conflict. Current RBAC labels, checksum, signed URL, audit/IP/session and retention statements are static copy, not a security control. |
| Trạng thái hiện tại | Design HTML/PNG only. Current controls change only native local state; submit is cancelled; download is disabled; the SH-07 card and back link are informational/inert. Study Web `UNWIRED`; #103/#18 `D` and `UNWIRED / NOT_FOUND`. |
| Phụ thuộc | #103 payload conflict, GET acceptance/retry semantics, filter serialization, format values, report authorization, durable queue/worker, #18 ID/access/status/result/store, file download/expiry/cleanup and AD-24 filter continuity. |

### Nguồn và ranh giới bằng chứng

- **Expected behavior:** inventory row 83, AC-38, API catalog #103/#18 and the Draft DDs. The API catalog is design evidence; endpoint rows and DDs are not current Study runtime.
- **Current prototype:** `code.html` has three format radios, three scope checkboxes, three period radios, a submit form with inline `event.preventDefault()`, disabled download control, placeholder operation/status panels, inert anchors and static worker/policy copy. It contains no API client, fetch/XHR, progress handler, polling loop or storage/download code.
- **Current Study source:** `app/api/v1.py` composes Admin APIs through #98. Scoped source/test search found no #103 or #18 route/module/query/model/test, Celery/export worker, report export endpoint or download-serving path. The shared auth helper can accept explicit roles and current Admin APIs use `ADMIN`; this does not implement or prove a report permission policy.
- **Database candidates:** pilot `file_objects`, `report_snapshots` and `evidence_export_requests` are distinct artifacts. The evidence table is for signed learner-evidence requests; report snapshots store calculated report data; generic file objects do not establish an export job or result. No approved Study Operation/export mapping or live schema/deployment was found.
- **No runtime claim:** `Worker Node 04`, Celery, “RBAC L3”, SHA-256, 120-minute signed links, audit/IP/session logging, browser cache prevention and 24-hour deletion are statements in the mockup only. The pilot file-object note about a generic 5-minute URL does not map to this export feature and does not validate the mockup's 120-minute claim.

### Source register

| Source | Evidence used |
|---|---|
| [Screen inventory](../../list_screen.md) | AD-25 candidate route, #103/#18 references, expected progress states, AD-24/SH-07 neighbors and conditional operation handoff. |
| [AC-38 diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio), [AC/API index](../../../../study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md) | Actor/precondition, optional export branch, #103 request, generation/storage/display nodes and the unconnected #18 operation node. |
| [API catalog](../../../../../docs/lists/list_api.md) | Direct #103/#18 rows, shared Operation/ExportAsset/Report schemas, ID convention and conflicting Operation tracking paragraph. |
| [API #103 DD](../../../../study-server/docs/dd/103_admin_reports_community_impact_export/00_Cover.md), [request](../../../../study-server/docs/dd/103_admin_reports_community_impact_export/03_Request.md), [response](../../../../study-server/docs/dd/103_admin_reports_community_impact_export/04_Response.md), [mapping](../../../../study-server/docs/dd/103_admin_reports_community_impact_export/05_Data_Mapping.md), [open questions](../../../../study-server/docs/dd/103_admin_reports_community_impact_export/OPEN_QUESTIONS.md) | Draft input/response alternatives and unresolved format, retry, storage, authorization and result questions. |
| [API #18 DD](../../../../study-server/docs/dd/18_operations/00_Cover.md), [overview](../../../../study-server/docs/dd/18_operations/02_Overview.md), [open questions](../../../../study-server/docs/dd/18_operations/OPEN_QUESTIONS.md) | Draft operation ID, owner policy, store, status/lifecycle and per-kind result gaps. |
| [Study Server router](../../../../study-server/app/api/v1.py), [auth helper](../../../../study-server/app/utils/auth.py), [declared routes](../../../../../.agents/server-study/apis/declared-routes.md) | Current route ceiling and shared guard capability; no report/export or operations route. |
| [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql), [V1-PILOT DDL](../../../../../infra/postgres/02_study_db.sql) | Candidate schema context only; no approved Operation/export job mapping. |
| [AD-24 DD](../../screen_stitch/05_admin/AD-24_bao-cao-tac-dong-cong-dong/AD-24.md), [Study Web design guide](../../../../../.agents/web-study/design.md) | Upstream filter handoff gap and canonical visual/accessibility target. |

Original asset hashes recorded before authoring:

- `screen.png`: `5d90eabc1fcf154433771d58b91e814e6fc6a40e89933ffac9c5b0f35522b722`
- `code.html`: `0cd68b7aba2052a35cf89289241cf125c64ca1c1cce9e23d5d0187c276a861be`

### Expected versus current discrepancies

| Topic | Expected/design | Current evidence | DD treatment |
|---|---|---|---|
| Export acceptance payload | #103 endpoint row: HTTP 202 `ApiEnvelope<Report>`; same catalog's Operation tracking: HTTP 202 `Operation`. AC-38 describes a job and poll reference. | No #103 route or worker. | Keep both direct declarations; no success payload mapping is approved. |
| Operation ID/poll | Inventory conditionally hands off to SH-07/#18; reusable schema/AC use UUID. | #18 catalog row uses int64; row/diagram owner rule differs from tracking paragraph; no handler/store/status enum. AC-38's #18 node has no connected edge. | No ID conversion, polling cadence, terminal state or SH-07 navigation. |
| Format and filter | Catalog has optional `filters:string`, `format:string`; AC-38 names CSV/XLSX/PDF. | Prototype has lower-case `csv/xlsx/pdf`; scopes `COURSE_SUMMARY/LEARNER_PROGRESS/CAREER_IMPACT`; periods `week/month/custom`; these are not a query mapping. | Treat UI values as prototype state only; no serialization/default/validation invented. |
| Retry/GET semantics | #103 method is GET, success is 202 and design says accept async job. | No idempotency key, queue, durable acceptance or request handler. | Duplicate submit/retry behavior remains open; do not change method or add retry logic by inference. |
| Result/download policy | AC-38 says temporary server storage if generated server-side and UI can display/download. | No export storage/result route. Mockup claims 120-minute signed URL, SHA-256, no browser cache and 24-hour cleanup. | Keep unsupported security/lifecycle copy out of runtime behavior; Download remains blocked. |
| Report permission | AC-38 requires report/analytics permission; catalog says Admin. | No #103 route policy. API #103 DD's “Student-only helper” note conflicts with current shared helper accepting explicit roles and Admin routes using `ADMIN`. | Shared capability is not a report guard; permission source/policy stays unresolved. |
| Filter handoff/navigation | Inventory expects AD-24 filters retained; AD-24 links to candidate `/admin/reports/export`. | AD-24 link drops query; AD-25 does not read URL state; its back anchor is `#`. | No filter transfer or return navigation claimed. |
| Visual system | Study Web guide specifies ocean tokens and Inter/system fonts, with no remote font import. | Mockup uses cobalt palette, Plus Jakarta Sans and Tailwind CDN. | Preserve source image; record implementation design discrepancy. |
