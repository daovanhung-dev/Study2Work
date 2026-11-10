# AD-08 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `AD-08-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Sửa metadata khóa, ảnh/giá nếu contract xác nhận.
- Gate/status (giữ nguyên): **R**; #75 route/module/test source exists, API DD remains Draft. **DD BLOCKED; IMPLEMENTATION BLOCKED:** catalog/AC omit PUT body; local four-field full-replacement body and rules are DERIVED; thumbnail upload contract absent; mentor edit mockup conflicts with #75; AC-32 permission vs `ADMIN`, legacy/live schema, response/revalidation and Study Web UNWIRED remain open; Back/Cancel currently point to AD-06; **RUNTIME NOT VERIFIED**
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu và blocker

### Checklist

- [x] Có source screenshot nguyên trạng; hash được kiểm tra, không sửa ảnh nguồn.
- [x] Có 61 marker liên tục, unique; DD có một hàng cho mỗi marker.
- [x] Current prototype controls, links, static values và API/server behavior được phân biệt.
- [x] #74/#75 đối chiếu catalog, AC, route/model/validator/view/query, API DD và test evidence.
- [x] Auth, candidate body, validation, transaction, response/errors và API limitations được truy vết.
- [x] States/navigation và expected/current discrepancy được ghi rõ.
- [ ] API #75 body, validation, schema và permission mapping được owner xác nhận.
- [ ] Thumbnail upload/storage contract và return/revalidation behavior được quyết định.
- [ ] Study Web route/client/error handling được implement và runtime verified.

### Blockers

1. API catalog/AC thiếu body #75; local body, replacement/null semantics, title/price bounds và legacy schema mapping đang là `DERIVED`.
2. AC-32 course-management permission chưa được chứng minh bằng local shared role `ADMIN`.
3. Mockup mô tả mentor edit nhưng #75 không sửa mentor; thumbnail upload/S3/multipart không có endpoint/contract trong module #75.
4. Legacy BIGINT schema và V1-PILOT UUID/versioned schema khác nhau; live DB/deployment chưa được xác minh.
5. Response singleton Page và yêu cầu revalidation thứ hai chưa được owner/client contract xác nhận.
6. Study Web app source/router/client không có; Back/Cancel route sai so với copy/AD-07 intent; static preview/metrics/audit/RBAC claims thiếu nguồn.

**Completion decision:** Tài liệu mô tả đầy đủ evidence và điểm quyết định nhưng chưa đạt `DD READY` vì các blocker ảnh hưởng trực tiếp đến body, authorization, persistence, upload và route. Trạng thái cuối màn hình: **DD BLOCKED** · **IMPLEMENTATION BLOCKED** · **RUNTIME NOT VERIFIED**. API #75 reverse inventory có thể là `R` cho local route/module/test source; API DD vẫn Draft.

## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
