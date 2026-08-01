# Review API DD — S2W-STUDY-API-029

- DD nguồn: `docs/DD/Study2Work_DD_API/04_Lo_trinh_hoc/S2W-STUDY-API-029_GET_learning_paths_path_id.xlsx`
- Endpoint: `GET /api/v1/learning-paths/{path_id}`
- Verdict: **CẦN SỬA**

## Findings

| Mức | Sheet/cell | Finding | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P0 | `3.Data mapping!A12:H12`, `A20` | Predicate `learning_paths.learning_path_id=:path_id` sai; PK thật là `id`. SQL pseudocode SELECT các aggregate như cột thật. | SQL `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:323-385` | Query `learning_paths.id`; JOIN course ordering/enrollment/completion sources, không SELECT placeholder aggregate. |
| P0 | `2.Response!A16:H21` | `path`, `courses`, completion/missing conditions, community groups và activation state đều gán nguồn `learning_paths`; shape/type/cardinality không đủ để triển khai. | `docs/BD/04. Study2Work_Study_BasicDesign_Lo_Trinh_Hoc.md:34-67,97-110`; SQL `:323-414,560-580,623-640` | Định nghĩa nested schema, nguồn từng field và scope community; progress/ownership từ enrollment. |
| P1 | `3.Data mapping!A12:H13` | Không khóa policy xem path archived/unpublished đối với learner đang học/đã hoàn thành; chỉ chép “PUBLISHED”. | `docs/BD/04. Study2Work_Study_BasicDesign_Lo_Trinh_Hoc.md:143-151,218-227` | Chốt visibility matrix cho new/active/completed learner và safe 404. |
| P1 | `4.Error!A16:H16` | `ACTIVE_PATH_EXISTS` không phải lỗi khi xem detail; BD yêu cầu hiển thị cảnh báo/action state nếu đang có path khác. | `docs/BD/04. Study2Work_Study_BasicDesign_Lo_Trinh_Hoc.md:58-67` | Trả blocking state trong success; chỉ activation API trả conflict. |
| P0 | `2.Response!A9:E11`, `A22:H22` | Envelope/snake_case/pagination mẫu không canonical. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Canonical envelope/camelCase/`traceId`, không pagination singleton. |

## Điều kiện duyệt lại

- [ ] Query/JOIN và nested response dùng cột thật.
- [ ] Có ownership + historical visibility matrix.
- [ ] Action state không bị biến thành lỗi đọc detail.
- [ ] Endpoint suy dẫn được PO/API owner duyệt.
