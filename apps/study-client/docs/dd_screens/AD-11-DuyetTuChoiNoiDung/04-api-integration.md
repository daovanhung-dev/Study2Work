# AD-11 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `AD-11-API-001` | #79 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `AD-11-API-002` | #80 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `AD-11-API-003` | #81 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #79, #80, #81
- Orchestration/data notes: Candidate `Content.id` từ AD-10 → GET #79 → PATCH #80 hoặc PATCH #81 với `{reason}` → reload #78. #80 local đặt `APPROVED`, không publish; #79 không trả author/version.
- BE/source status và gate: **R** local route/module/test source #79–#81; API DD Draft. **DD BLOCKED; IMPLEMENTATION BLOCKED:** AC `APPROVED/PUBLISHED` vs #80 `APPROVED`; reason required vs optional/disabled; author/version/media/rubric source thiếu; revision/stale policy, moderation permission, live schema/migration và Study Web `UNWIRED` còn mở; **RUNTIME NOT VERIFIED**
- Contract sources and discrepancies are preserved in the source excerpts below.

> CẦN_XÁC_NHẬN: API detail chưa có section riêng trong DD nguồn; xem API catalog/source references và giữ CẦN_XÁC_NHẬN.


## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/05_admin/AD-11_duyet-tu-choi-noi-dung/AD-11.md)
