# ST-02 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `ST-02-API-001` | #04 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #04
- Orchestration/data notes: GET #4 với Bearer; cache profile; profile có thể thiếu bio.
- BE/source status và gate: **R**
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: Dữ liệu #04 hiện có và giới hạn mapping

| Response path | Current source type/nullability | Candidate use on ST-02 | Limit |
|---|---|---|---|
| `data.id` | `int`, required | Identity for client state only if needed; do not display by default. | Not listed as a visible profile field. |
| `data.full_name` | `string`, required | Likely identity label in a ready state. | No ready-state layout in source assets. |
| `data.email` | `string`, required | Inventory expects email. | No ready-state layout or masking/copy policy. |
| `data.role` | `string`, required, from DB | Inventory expects role/status. | Authorization uses JWT role instead; DB role may differ from JWT. |
| `data.avatar_url` | `string \| null` | Inventory expects avatar. | No URL display/fallback/loading policy; current card icon is static, not avatar. |
| `data.phone` | `string \| null` | No display mapping in ST-02 inventory. | Do not add field to view without approved design. |
| `data.status` | `string`, required by model | Inventory expects status. | Source returns it but does not gate access by it; candidate DDL permits null. |
| `data.created_at`, `data.updated_at` | datetime serialized to JSON strings | Not in ST-02 inventory. | Do not expose or format without design requirement. |
| `data.bio` | Optional in catalog, no current source mapping | None. | Current query/model omit; current API #14 also ignores it. |
| permissions | Mentioned by AC-02, absent in catalog response model/query | None. | No permission source/schema/endpoint in #04. |

### Trích từ DD nguồn: API #04 contract/source matrix

| Hạng mục | Catalog/AC/API DD | Current source |
|---|---|---|
| Endpoint/auth | GET `/api/v1/users/me`; Bearer JWT; role Student; no path/body/query. | Registered GET route accepts one Authorization header; `validate_current_user_request(..., role="STUDENT")`; no path/query/body. |
| Input claims | Catalog does not fix JWT claims; AC-02 diagram says `user_id`/`role`. | #03 creates claims `sub`, `roles`, `type`, `jti`, `iat`, `exp`, `iss`, `aud`; #04 consumes `sub` and `roles`. |
| Success | HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; `ApiEnvelope<UserProfile>`. | HTTP 200, safe profile fields listed in §C, no permissions or bio; direct current source-backed. |
| Auth errors | Catalog/diagram: 401 and 403. | 401 for missing/bad token or absent user row; 403 for no Student token role. Role denial occurs before query. |
| System error | 500 `DESIGN_INTERNAL_ERROR`. | Decoder configuration, DB query, or model validation failures map to safe 500; SQLAlchemy exception rolls back. |
| DB effect | Read current user profile. | Single `users` SELECT by `users.id`; no joins/writes/external service. Candidate schema is not live verification. |
| Missing profile fields | `bio` optional at catalog; AC-02 says permissions. | Neither is selected, modeled or serialized by API #04. |

API #04 DD status is `Draft — Needs Confirmation`. Checked-in `infra/postgres/study-server/DB.sql` defines `status VARCHAR(20) DEFAULT 'ACTIVE'` without `NOT NULL`, while current `UserProfile.status` requires a string. A null status therefore causes source model validation to map an otherwise found row to 500; the deployed schema is not verified.

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/03_student/ST-02_ho-so-ca-nhan/ST-02.md)
