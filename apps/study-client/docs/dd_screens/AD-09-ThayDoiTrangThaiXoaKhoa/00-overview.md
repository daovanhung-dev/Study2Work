# AD-09 — Thay đổi trạng thái/xóa khóa · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `AD-09` |
| Module | Admin |
| Route | `/admin/courses/:courseId/actions` — Angular route/page source is present; browser/deployment runtime remains unverified |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: # AD-09 — Thay đổi trạng thái/xóa khóa; **Detailed Design:** `DD BLOCKED` · **Implementation:** `PARTIAL SOURCE; WRITE FLOW BLOCKED` · **Study Web runtime:** `NOT VERIFIED` (Angular route/page/#74 caller present)<br> |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.3 / 2026-11-21 (#74 Page<Course> validation) |
| Nguồn đối chiếu | [AD-09.md](../../screen_stitch/05_admin/AD-09_thay-doi-trang-thai-xoa-khoa/AD-09.md), [AD-09_PLAN.md](../../screen_stitch/05_admin/AD-09_thay-doi-trang-thai-xoa-khoa/AD-09_PLAN.md), [AD-09_markers.json](../../screen_stitch/05_admin/AD-09_thay-doi-trang-thai-xoa-khoa/AD-09_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Confirmation đổi trạng thái và cảnh báo enrollment/content phụ thuộc.
- In-scope: PATCH #76 hoặc DELETE #77 sau khi policy được duyệt → reload #73/#74 theo điều hướng được chốt.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-32 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Confirmation đổi trạng thái và cảnh báo enrollment/content phụ thuộc. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #74, #76, #77
- Liên kết màn hình dự kiến: [AD-06](../AD-06-DanhSachKhoaHocQuanTri/00-overview.md), [AD-07](../AD-07-ChiTietKhoaHocQuanTri/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | confirm/working/conflict/done |
| Current source | Angular AD-09 page | Route/page + GET #74 caller present; states `loading/loaded/error`; status/delete/reason disabled; no #76/#77 caller. Runtime `NOT VERIFIED`. |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [AD-09 source screen.png](../../screen_stitch/05_admin/AD-09_thay-doi-trang-thai-xoa-khoa/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/05_admin/AD-09_thay-doi-trang-thai-xoa-khoa/screen_annotated.png))
- Luồng: PATCH #76 hoặc DELETE #77 sau khi policy được duyệt → reload #73/#74 theo điều hướng được chốt.
- Priority: P2; Gate/source status: **R** local source #74/#76/#77 route/module/test; Angular route/page/#74 caller present; API DDs Draft. **DD BLOCKED; IMPLEMENTATION PARTIAL SOURCE; WRITE FLOW BLOCKED:** #76 body/enum/transition còn DERIVED; `archive` không có mapping; #77 local soft-delete trái copy permanent-delete, dependency/repeat/restore/audit policy chưa duyệt; AC-32 permission vs `ADMIN`, live schema và post-write reload còn mở. Status/delete/reason disabled. **RUNTIME NOT VERIFIED**

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# AD-09 — Thay đổi trạng thái/xóa khóa

> **Detailed Design:** `DD BLOCKED` · **Implementation:** `PARTIAL SOURCE; WRITE FLOW BLOCKED` · **Study Web runtime:** `NOT VERIFIED` (Angular route/page/#74 caller present)<br>
> **Screen:** AD-09 · **Actor:** Admin có course-management permission theo AC-32 · **Route:** `/admin/courses/:courseId/actions` (Angular route source-present; permission mapping open) · **AC:** AC-32 · **API:** #74, #76, #77<br>
> **Assets:** [screen nguyên trạng](../../screen_stitch/05_admin/AD-09_thay-doi-trang-thai-xoa-khoa/screen.png) · [screen đánh số](../../screen_stitch/05_admin/AD-09_thay-doi-trang-thai-xoa-khoa/screen_annotated.png) · [marker map](../../screen_stitch/05_admin/AD-09_thay-doi-trang-thai-xoa-khoa/AD-09_markers.json) · [kế hoạch](../../screen_stitch/05_admin/AD-09_thay-doi-trang-thai-xoa-khoa/AD-09_PLAN.md)

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

### Expected behavior

AD-09 là màn hình điều phối action cho một Course do Admin chọn. Inventory đề xuất `/admin/courses/:courseId/actions`, liên kết từ danh sách AD-06 và chi tiết AD-07. Handoff là numeric `Course.id`; không dùng mã hiển thị trong mockup làm khóa. AC-32 mô tả: GET #73 danh sách → GET #74 detail (course/owner/counters) → chọn Update, Status hoặc Delete; nhánh #76 đổi trạng thái + audit, nhánh #77 soft-delete theo policy; sau đó reload course management.

API catalog #76 khai báo `PATCH /api/v1/admin/courses/{course_id}/status`, Bearer JWT/Admin, `course_id:int64`, `ApiEnvelope<Page<Course>>`, 200 `DESIGN_RESOURCE_UPDATED`, lỗi 401/403/404/422/500. Catalog và AC **không khai báo body hoặc enum members**. API catalog #77 khai báo `DELETE /api/v1/admin/courses/{course_id}`, Bearer JWT/Admin, `course_id:int64`, không body/query, `ApiEnvelope<DeleteResult>`, 200 `DESIGN_RESOURCE_DELETED`, lỗi 401/403/404/422/500. Hai API DD đều `Draft — Needs Confirmation`.

### Current behavior và trạng thái bằng chứng

| Chủ đề | Expected / contract | Current source hoặc prototype | Trạng thái |
|---|---|---|---|
| Route/actor/ID | AC-32 Admin có course-management permission; action route nhận numeric `Course.id`. | Angular route/page validates the complete raw `courseId` against signed-int64 bounds before GET #74; valid IDs are passed unchanged. Permission mapping vẫn mở. | Route/read flow source-present; malformed/missing/out-of-range IDs skip GET; write-flow blocked; runtime `NOT VERIFIED`. |
| Target context | AC-32 yêu cầu đọc detail #74 trước khi chọn nhánh. | Stitch prototype hiển thị “Chưa chọn khóa học” và “Chưa xác định”; Angular tải #74 và hiển thị title/status/mentor/price cùng raw route ID. #74 không có counters. | `DISCREPANCY`: prototype tĩnh khác Angular; counter contract/source thiếu. |
| Chọn thao tác | Một lựa chọn duy nhất theo prototype; status và delete là nhánh AC-32 riêng. | Native radio `draft` mặc định checked, `archive`, `delete`; listener `change` rỗng. | Chỉ thay selection trong DOM; không có API action. |
| Status (#76) | API status branch và audit intent trong AC-32. | Catalog/AC bỏ body; local strict candidate là `{status:DRAFT|PUBLISHED|SUSPENDED}`; không transition/readiness rule; same-status no-op; changed status ghi audit atomically. | Enum/body/transition/audit schema local là `DERIVED`; API DD Draft. `archive` không có mapping. |
| Delete (#77) | DELETE/soft-delete theo policy AC-32; catalog trả DeleteResult. | Local source soft-marks `status='DELETED'`; chặn any enrollment và active Content/lesson/quiz/assignment; không hard-delete, cascade, child mutation hay audit. | Dependency set, marker, repeat semantics là `DERIVED`; API DD Draft. |
| Audit reason | AC-32 yêu cầu status + audit log ở #76; direct body chưa được nêu. | Prototype đòi lý do ISO-27001 nhưng textarea disabled; #76 candidate body chỉ có status/audit old/new/actor, #77 không ghi audit. | `UNSUPPORTED`; không gửi reason. |
| Permanent delete copy | AC-32 nói delete/soft-delete theo policy. | Prototype gọi xóa vĩnh viễn, “không thể hoàn tác”; local #77 chỉ đổi status thành DELETED. | `DISCREPANCY`; không hứa hard-delete/irreversibility. |
| Authorization | AC-32 yêu cầu course-management permission; catalog nói Admin. | Local #76/#77 shared guard kiểm tra role `ADMIN`, không check permission riêng. | `OPEN`; ADMIN role không chứng minh fine-grained permission. |
| Reload/visibility | AC-32 yêu cầu reload course management sau action. | Local #73/#74 không lọc DELETED; #76 cũng không chặn DELETED target. | Deleted item có thể còn trong Admin list/detail; restore/visibility policy chưa chốt. |
| Navigation | Inventory liên kết AD-06/AD-07; Angular hiện dùng AD-07 cho Back/footer. | Stitch prototype Back/Cancel đều link `/admin/courses` (AD-06). Angular Back/footer về AD-07 for valid route IDs and return to AD-06 for missing/malformed/out-of-range IDs; load error state về AD-06. | `DISCREPANCY` giữa prototype và Angular; post-mutation navigation/reload vẫn mở. |
| Static safeguards | Claims chỉ dùng khi được source-backed. | RBAC, system normal, protection gate, enrollment, ISO, lifetime retention đều là text tĩnh. | `STATIC_ONLY`; không phải permission, monitor, audit hoặc retention evidence. |

### Current Study Web source re-audit — 2026-11-20

- AD09Page validates the complete raw `courseId` against API #74's optional-sign signed-int64 path parser before requesting, without converting through JavaScript `Number`. Missing, malformed, or out-of-range IDs render a local error and skip GET #74; valid IDs are passed unchanged.
- Toolbar/footer links return invalid IDs to AD-06 and preserve the AD-07 destination for valid IDs. #76/#77 and reason controls remain unavailable; mutation policy and permission mapping remain open. Runtime and tests were not checked in this continuation.

### Current #74 response audit (2026-11-21)

- Before showing the selected Course, AD-09 requires `DESIGN_RESOURCE_RETRIEVED` and the exact locally implemented #74 singleton `Page<Course>` shape: one valid Course/mentor item and pagination `1/1/1/1`. Empty, multi-item or malformed success responses use the safe error state.
- The raw signed-int64 route string remains authoritative for GET #74 and navigation; the response Course ID is not compared through lossy JavaScript conversion. #76/#77 and reason controls remain disabled because write semantics and course-management permission are unresolved. Runtime is unverified.

### Actor, điều kiện và dữ liệu

- **Actor dự kiến:** Admin có course-management permission theo AC-32. Catalog yêu cầu Bearer JWT/Admin; current local #76/#77 kiểm tra shared role `ADMIN`. Mapping giữa role claim và permission AC-32 còn mở.
- **Điều kiện vào:** Angular route `courses/:courseId/actions` nhận raw `courseId` string; AD09Page gọi GET #74 qua AD09ApiService. Local path parser nhận signed int64; screen không tự thêm positive-only rule. API #74 projection không có counters mà AC diagram nhắc.
- **Status output:** Catalog chỉ nêu semantic labels draft/published/suspended. Local #76 candidate body dùng uppercase `DRAFT`, `PUBLISHED`, `SUSPENDED`; không có `ARCHIVED`, không nhận lý do và không định nghĩa transition matrix.
- **Delete output:** #77 catalog response là DeleteResult. Local source dùng tombstone `courses.status='DELETED'`, không xóa vật lý hoặc cascade. Cách xử lý khi còn enrollment/content là local fallback 422, chưa phải policy được owner duyệt.
- **Sau thành công:** AC-32 yêu cầu reload course management. GET #73/#74 response/client destination, liệu ở lại dialog hay quay về detail/list và cách invalidate cache cần quyết định. Local #73/#74 không lọc DELETED; kết quả xóa không đảm bảo course biến mất khỏi Admin list.
- **Screen type:** Inventory gọi AD-09 là Dialog, trong khi Stitch screenshot là trang form đầy đủ. Angular hiện render một routed page. Dialog-vs-page design classification còn khác nhau; runtime deployment chưa được xác minh.

### Nguồn truy vết

- [Screen inventory](../../list_screen.md) · [Global screen plan](../../screen_stitch/dd_screens/PLAN.md) · [AC-32 admin flow](../../../../study-server/docs/diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio)
- [API catalog](../../../../../docs/lists/list_api.md) · [API #76 router](../../../../study-server/app/api/v1.py) · [#76 model](../../../../study-server/app/modules/admin/api_76_admin_course_status/models.py) · [#76 validator](../../../../study-server/app/modules/admin/api_76_admin_course_status/validate.py) · [#76 view](../../../../study-server/app/modules/admin/api_76_admin_course_status/view.py) · [#76 SQL](../../../../study-server/app/modules/admin/api_76_admin_course_status/query.py)
- [API #77 model](../../../../study-server/app/modules/admin/api_77_admin_course_delete/models.py) · [#77 validator](../../../../study-server/app/modules/admin/api_77_admin_course_delete/validate.py) · [#77 view](../../../../study-server/app/modules/admin/api_77_admin_course_delete/view.py) · [#77 SQL](../../../../study-server/app/modules/admin/api_77_admin_course_delete/query.py)
- [#76 open questions](../../../../study-server/docs/dd/76_admin_course_status/OPEN_QUESTIONS.md) · [#77 open questions](../../../../study-server/docs/dd/77_admin_course_delete/OPEN_QUESTIONS.md) · [#76 tests](../../../../study-server/tests/modules/admin/api_76_admin_course_status/test_admin_course_status.py) · [#77 tests](../../../../study-server/tests/modules/admin/api_77_admin_course_delete/test_admin_course_delete.py)
- [API #73 list SQL](../../../../study-server/app/modules/admin/api_73_admin_courses_list/query.py) · [API #74 detail SQL](../../../../study-server/app/modules/admin/api_74_admin_course_detail/query.py) · [legacy candidate DDL](../../../../../infra/postgres/study-server/DB.sql) · [migration 010 candidate](../../../../../infra/postgres/study-server/migrations/010_course_status_audit_logs.sql) · [V1-PILOT Course DDL](../../../../../infra/postgres/02_study_db.sql)
- [Study Web design target](../../../../../.agents/web-study/design.md) · [Study Web scope index](../../../../../.agents/web-work/study/INDEX.md)
