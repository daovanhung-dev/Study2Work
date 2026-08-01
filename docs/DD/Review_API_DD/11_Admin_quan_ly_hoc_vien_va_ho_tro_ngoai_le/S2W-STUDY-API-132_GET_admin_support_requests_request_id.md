# Review S2W-STUDY-API-132 — GET support request detail

- DD nguồn: `docs/DD/Study2Work_DD_API/11_Admin_quan_ly_hoc_vien_va_ho_tro_ngoai_le/S2W-STUDY-API-132_GET_admin_support_requests_request_id.xlsx`
- Endpoint: `GET /api/v1/admin/support-requests/{request_id}`
- Kết luận: **CẦN SỬA — chưa đủ điều kiện VERIFIED**

## Các điểm cần sửa

| ID | Mức độ | Vị trí DD | Nhận xét và căn cứ BD | Cách sửa |
|---|---|---|---|---|
| 132-01 | P0 | `3.Data mapping!A12:H20` | Điều kiện `support_requests.request_id` sai vì PK là `id`; các field `learner_snapshot`, `progress_snapshot`, `allowed_actions`, `impact_preview` không phải cột (`schema_seed.sql:662-682`). SQL placeholder không mô tả cách tổng hợp. | Query bằng `id`; định nghĩa projection/JOIN và thuật toán allowed actions/impact preview. |
| 132-02 | P1 | `2.Response!A16:H21` | `request` và `impact_preview` để String, còn object snapshot không có field con. Điều này không đủ để Admin đánh giá tình trạng trước/sau theo luồng `BD-11:91-111`. | Khai báo object schema, nullable, enum và các con số tác động (progress/submission/enrollment bị ảnh hưởng). |
| 132-03 | P1 | `3.Data mapping!A13:H17` | `allowed_actions` chưa gắn role, trạng thái request, loại yêu cầu hay mức rủi ro; câu rule PUBLISHED/ownership là template. | Lập decision table type × status × role × allowed action; nêu yêu cầu reason/approval. |
| 132-04 | P0 | `2.Response!A9:E11`, sample success | Envelope cũ và pagination giả cho singleton trái `System_Architecture.md:632-700`. | Dùng envelope chuẩn camelCase, bỏ pagination và đưa traceId đúng cấp. |
| 132-05 | P1 | `00.Hướng dẫn!A10:B18`, `Lịch sử!A4:F4` | Checklist đánh dấu SQL/JOIN/placeholder đã hoàn tất dù chính SQL chưa thực thi được. | Chuyển NEEDS_REVIEW và cập nhật checklist theo bằng chứng test. |

## Điều kiện duyệt lại

- Projection detail và impact preview có định nghĩa kiểm thử được.
- Có test permission/status cho từng allowed action.
