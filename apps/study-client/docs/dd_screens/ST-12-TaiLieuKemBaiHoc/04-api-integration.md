# ST-12 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `ST-12-API-001` | #26 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `ST-12-API-002` | #12 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #26, #12
- Orchestration/data notes: GET #26; nếu có resource_id hợp lệ GET #12; không tự mở URL ngoài chính sách.
- BE/source status và gate: **D; DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED:** #26 chưa có Student route/module/query/test; `ApiEnvelope<Lesson>` chưa định nghĩa Resource collection, cardinality/order/empty/access/visibility/URL còn mở; #12 source-backed locally nhưng public, không auth/visibility/signer và trả stored URL; AC-06 signed-URL branch khác source; ST-12 prototype không có resource item hay valid `resource_id`; return context/Study Web route UNWIRED; legacy BIGINT và V1-PILOT UUID schema khác nhau; live DB chưa xác minh
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: I. Nguồn truy vết

- Inventory/flow/API index: [`list_screen.md`](../../list_screen.md) — ST-12, F04, API index, G-07.
- API catalog: [`list_api.md`](../../../../../docs/lists/list_api.md) — #12, #26 và `Resource` schema.
- AC-15: [`AC API index`](../../../../study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md), [`Student Learning diagram`](../../../../study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio).
- API #26: [cover](../../../../study-server/docs/dd/26_lessons_resources/00_Cover.md), [open questions](../../../../study-server/docs/dd/26_lessons_resources/OPEN_QUESTIONS.md).
- API #12: [current route](../../../../study-server/app/api/v1.py), [view](../../../../study-server/app/modules/guest/api_12_resources_detail/view.py), [query](../../../../study-server/app/modules/guest/api_12_resources_detail/query.py), [tests — read, not run](../../../../study-server/tests/modules/guest/api_12_resources_detail/test_resources_detail.py), [API DD](../../../../study-server/docs/dd/12_resources_detail/00_Cover.md).
- Candidate DB: [`DB.sql`](../../../../../infra/postgres/study-server/DB.sql) — không phải live-schema evidence.
- Linked screens: [`ST-11`](../../screen_stitch/03_student/ST-11_trinh-hoc-bai-lesson-player/ST-11.md), [`GS-07`](../../screen_stitch/02_guest_discovery/GS-07_xem-tai-tai-nguyen/GS-07.md).
- Study Web target/status: [design guide](../../../../../.agents/web-study/design.md), [Study Web index](../../../../../.agents/web-work/study/INDEX.md).

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/03_student/ST-12_tai-lieu-kem-bai-hoc/ST-12.md)
