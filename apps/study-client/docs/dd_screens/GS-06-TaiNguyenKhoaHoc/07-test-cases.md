# GS-06 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `GS-06-TC-001` | Planning ref / not run | `AC-06` | See source acceptance section | P2 |

## 2. Test planning references

### GS-06-TC-001 — Acceptance planning reference (AC-06)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [GS-06](../../screen_stitch/02_guest_discovery/GS-06_tai-nguyen-khoa-hoc/GS-06.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-06`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/02_guest_discovery/GS-06_tai-nguyen-khoa-hoc/GS-06.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu

- [x] Có original PNG hợp lệ, static HTML được đối chiếu; không tạo dữ liệu resource giả.
- [x] Có 23 marker ID duy nhất và ordered; mỗi marker có một element row tương ứng trong §C.
- [x] Có event trace cho expected resource load/select/open và từng visible interactive group, bao gồm disabled/placeholder behavior.
- [x] API #11 status `DECLARED_NOT_RUNNABLE`, response singleton/list discrepancy, missing visibility source, 404/500 scope và AC-06 conflict được giữ rõ.
- [x] API #12 current route/view/query/model/test source được đối chiếu; direct URL, no-auth route, conditional parent gate, 404/500 và test-not-run status được mô tả.
- [x] States, data handoff, unknown routes, 403/410/signer blockers và empty-vs-contract-block distinction được liệt kê.
- [ ] API #11 implementation/cardinality/visibility/list schema được duyệt và runnable; cần trước `DD READY`.
- [ ] AC-06 access policy thống nhất với API catalog và current #12; private-resource authorization, signed URL TTL/expiry, 403/404 mapping được chốt trước implementation.
- [ ] Resource list/loaded/error UI, route/cache/back behavior và controls được phê duyệt.
- [ ] Study Web implementation và deployed end-to-end behavior được verify; cần trước `RUNTIME VERIFIED`.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 0. Kế hoạch rà soát lại (2026-11-07; hoàn tất static audit 2026-11-08)

Thứ tự công việc trong phiên này:

1. Đọc lại mục tiêu 83 màn hình, inventory GS-06, AC-06, API catalog/DD #11/#12 và nguồn Study Web/Study Server hiện tại; phân biệt expected với current behavior.
2. Đối chiếu route/module/query/validator/model/test của #12 và tìm riêng route/module/test của #11; chỉ đọc test source, không chạy application tests.
3. So sánh schema candidate legacy với V1-PILOT; không suy luận rằng artifact DDL hay test fake-session chứng minh production/live schema.
4. Kiểm tra lại `screen.png`, `code.html`, `screen_annotated.png`, marker JSON/SVG, mapping marker↔element và tất cả event của DD; giữ nguyên PNG/HTML nguồn.
5. Cập nhật DD và marker/ảnh chỉ khi audit phát hiện thiếu hoặc sai; nếu mapping/ảnh hiện hữu hợp lệ thì giữ nguyên.
6. Cập nhật trạng thái GS-06 ở `list_screen.md` và bảng/checkpoint trong `dd_screens/PLAN.md`; hoàn thiện worklog, chạy kiểm tra tĩnh và context validator nếu có thay đổi registered context.

### Bằng chứng hiện tại được xác nhận trước khi sửa DD/marker/tracker

- API #11 vẫn là declaration/Draft: catalog khai báo public GET với `ApiEnvelope<Resource>` đơn, không query/body; tìm kiếm current Study Server `app/` và `tests/` không thấy route/module/test #11. Cardinality, list-empty, thứ tự/pagination và `visibility` chưa có nguồn runtime.
- API #12 có route/module/query/validator/model trong current Study Server và route được compose ở `/api/v1/resources/{resource_id}`. Route không nhận/kiểm tra Authorization; validator chỉ chấp nhận positive signed-int64 và map path sai thành 404; view đọc `resources.url` trực tiếp, conditional gate parent lesson/course chỉ chạy khi `lesson_id` khác null, và không gọi storage signer hoặc kiểm tra enrollment/visibility. Test source xác nhận các nhánh này nhưng không được chạy trong phiên.
- AC-06 yêu cầu resource public hoặc có quyền truy cập, có nhánh 403, và signed URL cho object private; API catalog #11/#12 chỉ public và 404/500. Đây là `DISCREPANCY`, chưa được phép hợp nhất bằng suy đoán.
- Schema candidate legacy `infra/postgres/study-server/DB.sql` khai báo `resources(id, lesson_id, name, resource_type, url, created_at)` và không có `visibility`; V1-PILOT `infra/postgres/02_study_db.sql` hiện không khai báo bảng `resources`. Live production schema/deployment không được xác minh.
- `apps/study-client/` hiện không có editable app source, package manifest hoặc screen router; chỉ có docs/assets, ignored `dist/` và build metadata. Study Web vẫn `UNWIRED`; asset tĩnh không chứng minh route/runtime.
- PNG gốc hiện là 1486×1600, SHA-256 `b90795438d5369466bb101e8f6730265667f8ecc45c0d047d66495410da87dcd`; HTML gốc SHA-256 `6843e2cc0f01a24e1db8100b8fec49d88e1f3fe39859b102bb9828d4905a8c31`. Giữ nguyên cả hai.
- Trước khi chỉnh DD/marker/tracker, thư mục đã có 23 markers, annotation và DD từ phiên 2026-11-06. Phiên này sẽ xác minh lại một-một, bounds, SVG/image consistency, event completeness và các liên kết thay vì mặc định chúng hợp lệ.

### Definition of completion riêng cho lần rà soát này

- Ghi đầy đủ 23 element và các tương tác hiện có; mỗi event có loại/trigger, precondition, input, processing, output và error/exception, tách rõ hành vi HTML tĩnh với luồng expected chưa runnable.
- Ghi API #11 `DECLARED_NOT_RUNNABLE`, #12 `SOURCE-BACKED LOCALLY`, Draft status, #12 direct-URL behavior, schema discrepancy, AC-06 conflict, `UNWIRED` Study Web và live-schema limitation.
- Chỉ giữ `DD BLOCKED`/`IMPLEMENTATION BLOCKED`/`RUNTIME NOT VERIFIED` khi các blockers còn đúng; không nâng `DD READY` hay `RUNTIME VERIFIED` bằng việc chỉ có file/test source.
- Xác minh `screen.png`/`code.html` hashes, ảnh chú thích, marker IDs/tọa độ/mapping, local links, tracker IDs/folders và whitespace.

### Trích từ DD nguồn: 4. Planned output and acceptance

- Keep `screen.png` and `code.html` byte-identical.
- Create `GS-06_markers.json`, a vector overlay and `screen_annotated.png`; keep markers ordered and unique, align them to visible grouped elements and avoid covering primary copy or controls.
- Create `GS-06.md` with overview, expected/current flow, element table, sequential event procedures, #11/#12 request/response/status trace, state matrix, navigation/data handoff, acceptance checklist, source links and explicit blockers.
- Update `list_screen.md` and `dd_screens/PLAN.md` with API #12 source status, GS-06 blockers and a dated checkpoint. Current file inventory has all six core artifacts for 83/83 IDs; this is file-presence evidence only, not proof that all 83 DDs passed quality review. Keep GS-07 as the next separate-session screen and keep `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, `RUNTIME NOT VERIFIED` separate.
- Create this session worklog with prior-worklog review, source trace, discrepancy register and static audit. Read but do not run backend tests or claim runtime verification.

### Acceptance checklist

- [x] Plan existed before annotation/DD authoring and was updated before this re-audit's DD/tracker edits.
- [x] Original PNG/HTML hashes unchanged; original image is valid and the annotated image was visually inspected.
- [x] Every marker is unique, ordered, within canvas bounds and maps 1:1 to one DD element row.
- [x] All visible static controls/cards/states are documented; each actionable element and conditional tooltip state has a sequential event or explicit disabled/unknown behavior, with type/trigger/precondition/input/process/output/error.
- [x] #11 absence, singleton/list discrepancy and missing visibility source are explicit.
- [x] #12 current direct URL/public behavior, conditional parent check, response fields and errors are source-backed; API DD's stale `DECLARED_NOT_RUNNABLE` note and temporary-branch report are separated from production verification; tests are not described as run.
- [x] AC-06 vs API catalog/backend mismatch and unsupported 403/410/signer claims remain explicit blockers.
- [x] Overall tracker counts/status and next screen are updated; static diff and artifact checks pass.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
