# Review API DD — S2W-STUDY-API-045

- DD nguồn: `docs/DD/Study2Work_DD_API/05_Khoa_hoc_chuong_bai_hoc_va_tai_nguyen/S2W-STUDY-API-045_GET_resources_resource_id_access.xlsx`
- Endpoint: `GET /api/v1/resources/{resource_id}/access`
- Verdict: **CẦN SỬA**

## Findings

| Mức | Sheet/cell | Finding | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P0 | `3.Data mapping!A12:H12`, `A20` | Predicate `course_materials.resource_id` sai; PK thật là `id`. Không join lesson/chapter/course enrollment để kiểm quyền. | SQL `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:416-484` | Lookup `course_materials.id`, authorize scope/unlock/owner trước khi cấp URL. |
| P0 | `2.Response!A16:H21` | `resource_id,access_type,url,expires_at,tracking_required` bị coi là stored columns; schema chỉ có `id,type,resource_url,required,source,usage_right_status`. | SQL `:472-481` | Phân biệt stored metadata và generated signed-access result; định nghĩa enum/expiry/provider. |
| P0 | `2.Response!A18:H19`, `3.Data mapping!A15:H15` | DD có thể trả permanent raw URL; không mô tả signed URL TTL, one-time/redirect, revocation hay không log URL. | `docs/BD/05. Study2Work_Study_BasicDesign_Khoa_Hoc_Noi_Dung_Hoc.md:159-169`; `docs/BD/base/0. Study2Work_System_Architecture.md:975-1042` | Generate short-lived signed access after auth; redact logs; test expiry/revocation. |
| P1 | `4.Error!A13:H15` | Gộp not-found/not-owned/not-published nhưng không kiểm usage rights `UNKNOWN/REJECTED`; có thể cấp tài liệu chưa đủ quyền sử dụng. | `docs/BD/05. Study2Work_Study_BasicDesign_Khoa_Hoc_Noi_Dung_Hoc.md:163-169`; SQL `:472-481` | Thêm eligibility matrix cho publication/usage rights/enrollment/lesson unlock. |
| P0 | `2.Response!A9:E11`, `A22:H22` | Envelope/pagination mẫu thừa không canonical. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Canonical singleton response. |

## Điều kiện duyệt lại

- [ ] PK/ownership/unlock/usage-right checks đúng.
- [ ] Signed URL lifecycle và logging policy được mô tả/test.
- [ ] Stored/derived fields phân biệt rõ; envelope canonical.
- [ ] Endpoint suy dẫn được duyệt.
