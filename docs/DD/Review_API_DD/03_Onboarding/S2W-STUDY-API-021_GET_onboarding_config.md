# Review API DD — S2W-STUDY-API-021

- DD nguồn: `docs/DD/Study2Work_DD_API/03_Onboarding/S2W-STUDY-API-021_GET_onboarding_config.xlsx`
- Endpoint: `GET /api/v1/onboarding/config`
- Verdict: **CẦN SỬA**

## Findings

| Mức | Sheet/cell | Finding | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P0 | `2.Response!A9:E11`, `A24:H24` | Envelope `{data, meta}` / `{error}` và `meta.request_id` không phải canonical contract. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Dùng `success`, `businessCode`, `message`, `data`, `errors`, `traceId`; camelCase. |
| P0 | `2.Response!A15:H23`, `3.Data mapping!A12:H12`, `A20` | Config bị đọc như các cột `version`, `steps`, `technologies`, `goals` của `onboarding_records`; bảng thật không có các cột này. | `docs/BD/03. Study2Work_Study_BasicDesign_Onboarding.md:24-30,59-70`; `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:340-359` | Chốt nguồn cấu hình Admin/config service hoặc bổ sung schema cấu hình; định nghĩa object option thay vì mảng không schema. |
| P1 | `1.Request!A21:J21`, `3.Data mapping!A12:H12` | `version` cho phép tới `2^31-1` nhưng không có semantics/version registry; SQL còn lọc `onboarding_records.version`, cột không tồn tại. | `docs/BD/03. Study2Work_Study_BasicDesign_Onboarding.md:59-70,123-137` | Bỏ query hoặc định nghĩa version config, cache/ETag và hành vi khi version cũ/không tồn tại. |
| P1 | `4.Error!A14:H16` | `ONBOARDING_REQUIRED`, `ACTIVE_PATH_EXISTS`, `PATH_NOT_PUBLISHED` bị chép vào API tải config dù không phải điều kiện của thao tác. | `docs/BD/03. Study2Work_Study_BasicDesign_Onboarding.md:38-43,76-96` | Giữ auth/suspended/config-version errors; bỏ lỗi activation không liên quan. |
| P1 | `Cover!B19`, `Lịch sử!A4:F4`, `00.Hướng dẫn!A4:B18` | Tuyên bố không có schema, hết placeholder và `VERIFIED` đã stale; repo có 48 nguồn và SQL trong khi reviewer/approver chưa được chỉ định. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:1-31` | Cập nhật nguồn, bỏ placeholder, chuyển trạng thái về review cho tới khi PO/API owner duyệt endpoint suy dẫn. |

## Điều kiện duyệt lại

- [ ] Có nguồn cấu hình/version thực, schema option và contract cache rõ.
- [ ] Error catalog chỉ chứa lỗi của config.
- [ ] Envelope canonical và không còn cột/SQL giả.
- [ ] Endpoint suy dẫn được PO/API owner phê duyệt.
