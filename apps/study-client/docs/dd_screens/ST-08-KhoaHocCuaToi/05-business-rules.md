# ST-08 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `ST-08-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Danh sách khóa đã ghi danh, filter trạng thái và thanh tiến độ.
- Gate/status (giữ nguyên): **D**; **BLOCK:** #20/#21 Draft/NOT_FOUND, response UserProfile không biểu diễn list/progress; query/merge chưa chốt; AC-13 nhánh EMPTY/HAS DATA cùng tới node render; DDL BIGINT/UUID khác model; loaded/filter UI và design guide alignment còn thiếu; Study Web UNWIRED
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu và blockers

### Blockers / quyết định cần đóng

1. **BLOCKER — API #20 response:** catalog `ApiEnvelope<UserProfile>` không biểu diễn course list; API owner cần chốt payload, fields, identifier, enrollment/course projection, empty response và cập nhật nguồn canonical. Xem Q-20-01/Q-20-04.
2. **BLOCKER — #20 filter/paging:** chốt `status` semantics, values/default/case, page indexing/size/max/order/metadata; xem Q-20-02/Q-20-03.
3. **BLOCKER — API #21 query/response:** grammar `course_id list hoặc aggregate?:string`, progress DTO, merge key, scope/formula, empty behavior và identity binding cần quyết định; xem Q-21-01…Q-21-05.
4. **BLOCKER — AC/inventory orchestration:** xác nhận #21 luôn được gọi hay chỉ khi #20 thiếu progress, thứ tự/parallelism và partial-failure behavior.
5. **BLOCKER — loaded UI:** cần thiết kế/duyệt filter, course list/card, progress display, pagination, loading/partial/error/access-denied states; current asset chỉ có empty state.
6. **BLOCKER — navigation contract:** card → ST-09 cần course identifier và behavior khi enrollment không còn hợp lệ; ST-20/session handoff/back behavior chưa có runtime route.
7. **BLOCKER — Study Web:** checkout không có app source/router/entrypoint nên không thể xác minh hoặc implement route, auth guard, API calls, responsive/accessibility behavior.
8. **BLOCKER — AC-13 empty branch:** decision node labels `NO → empty state`, but both `EMPTY` and `HAS DATA` edges target the same course/progress render node. Clarify the target/transition before finalizing the empty-state flow.
9. **BLOCKER — database model:** checked-in legacy BIGINT and V1-PILOT UUID DDL use different course, enrollment and progress relations; API #20/#21 have no query source selecting either. Live schema remains unverified.
10. **BLOCKER — Study Web design alignment:** source HTML's remote font/CDN, Plus Jakarta Sans and 1440px width diverge from the intended guide; no approved exception or implementation is present.
11. **BLOCKER — runtime:** API #20/#21 have no route/module/query/test source, Study Web has no editable source/router, and the database/runtime were not verified.

### Checklist nghiệm thu

- [x] Kế hoạch riêng được ghi trước DD/annotation; scope chỉ ST-08.
- [x] Giữ nguyên `screen.png` và `code.html`; hashes gốc được ghi trong `ST-08_PLAN.md`/`ST-08_markers.json`.
- [x] Vì `screen.png` không thể hiện header và có band đen, tạo `screen_rendered.png` từ HTML tĩnh, ghi rõ provenance; không gọi là runtime capture.
- [x] `screen_annotated.png` có 9 marker; mỗi marker ánh xạ tới đúng một element row bên dưới và trong marker JSON.
- [x] Ghi rõ mỗi element/event có bằng chứng static, expected design hay missing source; API status không bị mô tả thành runtime.
- [x] Ghi luồng ST-07 → ST-08, ST-08 → ST-09/ST-20 và liên kết ST-01/SH-02 có điều kiện.
- [x] Ghi các HTTP/business codes hiện có trong catalog cùng response type và các khác biệt AC/inventory.
- [x] Ghi loading, empty, loaded, partial-progress, filtered và error state expectations; phân biệt với UI hiện hữu.
- [x] Rà soát lại AC-13 decision edges, hai thế hệ checked-in Study DDL và Study Web design guide; các nhánh/projection/design khác biệt được giữ là blocker.
- [ ] DD READY: chờ chốt API #20/#21 payload/query/mapping, loaded-state design, navigation/auth/error behavior và hoàn tất traceability không còn quyết định nghiệp vụ mở.
- [ ] IMPLEMENTATION READY: chờ Study Web source/router/session và API #20/#21 được nối theo contract đã duyệt.
- [ ] RUNTIME VERIFIED: chưa chạy app/API, chưa xác minh database live.

## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
