# AD-23 — Điều tra/kiểm duyệt thảo luận · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `AD-23` |
| Module | Admin |
| Route | `/admin/discussions/:discussionId/moderate` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **DD status:** BLOCKED — prototype, AC-37 and catalog identify an intended flow, but report detail, moderation actions, audit behavior and deletion are not implementable from approved/current evidence.<br>; **Implementation status:** BLOCKED — Study Web has no editable route/client; #99 and #100 have no local server implementation.<br>; **Runtime status:** NOT VERIFIED — this DD records static assets, contracts and local source only. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [AD-23.md](../../screen_stitch/05_admin/AD-23_dieu-tra-kiem-duyet-thao-luan/AD-23.md), [AD-23_PLAN.md](../../screen_stitch/05_admin/AD-23_dieu-tra-kiem-duyet-thao-luan/AD-23_PLAN.md), [AD-23_markers.json](../../screen_stitch/05_admin/AD-23_dieu-tra-kiem-duyet-thao-luan/AD-23_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Đọc full thread/report, action hide/lock/warn/delete có lý do.
- In-scope: GET #98 → PATCH #99 với action/reason hoặc DELETE #100 → refresh #97.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-37 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Đọc full thread/report, action hide/lock/warn/delete có lý do. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #98, #99, #100
- Liên kết màn hình dự kiến: [AD-22](../AD-22-DanhSachThaoLuanBiBaoCao/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | loading/reviewing/processing/resolved/conflict |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [AD-23 source screen.png](../../screen_stitch/05_admin/AD-23_dieu-tra-kiem-duyet-thao-luan/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/05_admin/AD-23_dieu-tra-kiem-duyet-thao-luan/screen_annotated.png))
- Luồng: GET #98 → PATCH #99 với action/reason hoặc DELETE #100 → refresh #97.
- Priority: P1; Gate/source status: **R #98** local route/module/query/model/validator/view/test source; API DD #98 stale `UNWIRED`; #99/#100 **D** catalog/Draft only, no local route. **DD BLOCKED; IMPLEMENTATION BLOCKED:** #98 report projection, #99 action/audit, #100 soft-delete policy, dismissal branch, target grain, Admin permission mapping and Study Web remain unresolved/unwired

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# AD-23 — Điều tra/kiểm duyệt thảo luận

> **DD status:** BLOCKED — prototype, AC-37 and catalog identify an intended flow, but report detail, moderation actions, audit behavior and deletion are not implementable from approved/current evidence.<br>
> **Implementation status:** BLOCKED — Study Web has no editable route/client; #99 and #100 have no local server implementation.<br>
> **Runtime status:** NOT VERIFIED — this DD records static assets, contracts and local source only.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID / tên | AD-23 — Điều tra/kiểm duyệt thảo luận |
| Mục tiêu | Từ AD-22 xem ngữ cảnh một thảo luận bị báo cáo, cân nhắc quyết định moderation và quay lại hàng đợi. Hành động xử lý chưa được mở khóa trong prototype. |
| Actor | Thiết kế AC/catalog ghi Admin. API #98 local hiện kiểm tra role `ADMIN`; điều này chưa chứng minh mapping permission/tenant của AC-37. Chính sách #99/#100 chưa có source. |
| Điều kiện trước | Expected: Admin mở AD-23 từ một hàng AD-22 có Discussion ID hợp lệ. Contract #98 yêu cầu `discussion_id:int64!`; ID và target grain (discussion gốc hay reply) chưa được chứng minh bởi handoff hiện có. |
| Điều kiện sau | Current prototype không tải dữ liệu và không thay đổi trạng thái. Expected: đọc ngữ cảnh qua #98; nếu đủ điều kiện và có quyết định được duyệt thì #99; optional delete qua #100 theo AC-37; quay lại/làm mới AD-22 qua #97. Điều kiện chuyển trạng thái và refresh chưa được xác định đầy đủ. |
| Route | `/admin/discussions/:discussionId/moderate` là candidate trong inventory, chưa có Study Web route. API #98 path là `/api/v1/admin/discussions/{discussion_id}`. |
| Màn hình liên kết | AD-22 là màn hình trước và đường quay lại; #97 là API queue liên quan. Không có màn hình sau được xác nhận. |
| Assets | [Ảnh gốc](../../screen_stitch/05_admin/AD-23_dieu-tra-kiem-duyet-thao-luan/screen.png), [HTML prototype](../../screen_stitch/05_admin/AD-23_dieu-tra-kiem-duyet-thao-luan/code.html), [ảnh đánh số](../../screen_stitch/05_admin/AD-23_dieu-tra-kiem-duyet-thao-luan/screen_annotated.png), [marker map](../../screen_stitch/05_admin/AD-23_dieu-tra-kiem-duyet-thao-luan/AD-23_markers.json), [kế hoạch](../../screen_stitch/05_admin/AD-23_dieu-tra-kiem-duyet-thao-luan/AD-23_PLAN.md). |
| API liên quan | #98 GET detail (local route/source exists, API DD still says UNWIRED); #99 PATCH moderate (catalog/Draft only); #100 DELETE conditional (catalog/Draft only); #97 GET reported queue for AD-22 (local source exists). |
| Bảo mật | Catalog yêu cầu Bearer JWT, role Admin. Current local #98 guard checks `ADMIN` before path parsing/query. AC permission and identity mapping for audit, #99/#100 guard, tenant scope and session handling remain open. |
| Quy tắc nghiệp vụ | AC-37 expects read discussion/comments/reports; on violation, action #99 updates moderation state and audit; optional #100 soft-deletes and preserves audit. AC no-violation branch says dismiss report, but no dismissal endpoint is listed. |
| Phụ thuộc / trạng thái hiện tại | Study Web `UNWIRED`; #98 local projection has Discussion and direct comments but no report fields; #99/#100 are `D`/unwired locally; report writer/live schema and audit persistence unverified. DD and implementation blocked. |

### Nguồn và ranh giới bằng chứng

- **Expected behavior:** inventory row 81, AC-37 and direct API catalog #98–#100. The screen route and interactions are design candidates, not an existing frontend contract.
- **Current prototype:** `code.html` is static: summary values are placeholders, thread content is empty, four radio options/textarea/apply button are disabled, return anchors use `#ad-22`, and there is no script, form handler, fetch/XHR or API client.
- **Current local #98 source:** registered GET route and module exist. Shared auth validation for role `ADMIN` runs before path validation and DB access. Path must be positive signed int64 digits; invalid, non-positive, overflow and missing row map to local 404. Query reads the Discussion plus author, then direct child comments without a status filter, ordered `created_at ASC, id ASC`. Mapping derives a title from normalized content (maximum 120 characters, otherwise `Thảo luận #id`), maps comments/author/timestamps and returns a one-item `Page<Discussion>`. It does not query reports, does not mutate/commit, and query/projection failure is returned as a safe 500 with rollback. Characterization test source was inspected but not run.
- **Source/DD discrepancy:** API DD #98 still states `UNWIRED / NOT_FOUND`; this DD records the currently registered local source and does not treat that stale DD label as runtime proof.
- **#99/#100 current source:** no local route/module/query/model/test source was found. Catalog fields/codes and API DDs are design evidence only; neither API is runtime verified.
- Candidate report migration/DDL is not proof of a deployed/live schema or a functioning report writer.

### Source register

| Source | Use in this DD |
|---|---|
| [Screen inventory](../../list_screen.md) | Row 81, candidate route, links, states and tracker status. |
| [AC-37 diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) | Expected queue/detail/moderation/delete/dismissal branches. |
| [API catalog](../../../../../docs/lists/list_api.md) | Direct #98–#100 request, response, auth and error contract. |
| [Study Server router](../../../../study-server/app/api/v1.py), [#98 query](../../../../study-server/app/modules/admin/api_98_admin_discussions_detail/query.py), [#98 view](../../../../study-server/app/modules/admin/api_98_admin_discussions_detail/view.py), [#98 validation](../../../../study-server/app/modules/admin/api_98_admin_discussions_detail/validate.py) | Current local route, query/projection, auth/validation and failure behavior. |
| [#98 characterization test source](../../../../study-server/tests/modules/admin/api_98_admin_discussions_detail/test_admin_discussion_detail.py) | Test assertions inspected; not run in this task. |
| [#98 API DD](../../../../study-server/docs/dd/98_admin_discussions_detail/00_Cover.md), [#99 API DD](../../../../study-server/docs/dd/99_admin_discussions_moderate/00_Cover.md), [#100 API DD](../../../../study-server/docs/dd/100_admin_discussions_delete/00_Cover.md) | Draft boundary, declared response details and unresolved questions. |
| [Candidate report migration](../../../../../infra/postgres/study-server/migrations/014_discussion_reports.sql), [candidate Study DDL](../../../../../infra/postgres/study-server/DB.sql) | Candidate schema only; not proof of live deployment or writer behavior. |
| [Study Web design guidance](../../../../../.agents/web-study/design.md) | Shared UI/accessibility guidance; does not establish app runtime. |

### Expected versus current discrepancies

| Topic | Expected / prototype claim | Current evidence | DD treatment |
|---|---|---|---|
| Report detail | AC-37 and #98 name full thread + report detail. | Current #98 projection has no report query/fields; #97 also lacks report details required by the queue UI. | Block report reason, severity, reporter, count and report timestamp mapping. |
| No-violation branch | AC-37 says dismiss report. | No dismissal API is catalogued or implemented. | Do not map this branch to #99 without approval. |
| Action choices | Prototype shows hide, lock comments, warn author and permanent delete. | AC gives hide/lock/warn at a logical level; exact action tokens/transitions are unresolved. Delete is a separate optional #100 in AC/catalog. | Keep all controls disabled until contracts and UI flow are approved. |
| Delete semantics | Prototype copy says permanent/full removal. | AC/#100 describe conditional soft delete while preserving audit; state/timestamp/persistence mapping unresolved. | Prototype conflicts with contract; do not implement hard delete or route delete through #99. |
| Warning/audit | Prototype says a warning letter is sent and audit is stored automatically. | No source-backed delivery or audit persistence for #99. | Treat the statements as unverified prototype copy. |
| Authorization | AC/catalog actor is Admin. | #98 local guard is `ADMIN`; #99/#100 source and permission mapping absent. | Preserve the distinction; do not claim AC authorization is satisfied. |
| Runtime | Prototype depicts an Admin page. | Study Web has no tracked editable `src` route/client; no runtime test was run. | `RUNTIME NOT VERIFIED`. |
