# Review API DD — S2W-STUDY-API-042

- DD nguồn: `docs/DD/Study2Work_DD_API/05_Khoa_hoc_chuong_bai_hoc_va_tai_nguyen/S2W-STUDY-API-042_GET_lessons_lesson_id_study.xlsx`
- Endpoint: `GET /api/v1/lessons/{lesson_id}/study`
- Verdict: **CẦN SỬA**

## Findings

| Mức | Sheet/cell | Finding | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P0 | `1.Request!A10:D10`, `Overview!A12` | Permission đặt `study.admin.manage` dù endpoint direct phục vụ Learner; cover còn nói Learner/preview Admin. Learner hợp lệ sẽ bị từ chối. | `docs/BD/diagram/SEQUENCE/06. Study2Work_Study_SEQ_Hoc_Bai_Cap_Nhat_Tien_Do.md:15-25`; `docs/BD/13. Study2Work_Study_BasicDesign_Vai_Tro_Phan_Quyen_Audit_Log.md:57-76` | Cho learner owner permission; Admin preview là capability/route/context riêng và không tạo progress. |
| P0 | `2.Response!A16:H28`, `A30` | Direct response không khớp SEQ06: thiếu `lessonId`, `accessStatus`, typed `content`, `materials`, `progress.status/videoWatchPercent`; thay bằng nhiều String/generic fields. | `docs/BD/diagram/SEQUENCE/06. Study2Work_Study_SEQ_Hoc_Bai_Cap_Nhat_Tien_Do.md:37-80` | Giữ exact sequence payload/business code hoặc trace quyết định thay contract. |
| P0 | `3.Data mapping!A12:H12`, `A20` | `lessons.lesson_id` sai PK; objectives/content/video/resources/progress bị SELECT như lesson columns. Không join course enrollment để access-check. | SQL `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:416-481,539-555` | Query `lessons.id`; join chapter/course/enrollment/material/progress/exercise; check unlock/owner trước content. |
| P0 | `2.Response!A18:H20`, `A27:H27` | Private URLs/community data không có signed URL/expiry/field gating; sequence URLs chỉ là ví dụ và không thắng security policy. | `docs/BD/05. Study2Work_Study_BasicDesign_Khoa_Hoc_Noi_Dung_Hoc.md:159-169`; `docs/BD/base/0. Study2Work_System_Architecture.md:975-1042` | Chỉ trả signed/authorized access action, không permanent private URL; community qua module scope. |
| P0 | `2.Response!A9:E11` | Envelope không canonical. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Canonical envelope/camelCase/stable SEQ06 code. |

## Điều kiện duyệt lại

- [ ] Learner owner và Admin preview permission tách đúng.
- [ ] Request/response/access/error khớp SEQ06.
- [ ] Query dùng sources thật và không trả content trước authorization.
- [ ] Private resources dùng signed access + negative tests.
