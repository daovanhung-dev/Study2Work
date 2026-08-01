# Review API DD — S2W-STUDY-API-127

- DD source: `docs/DD/Study2Work_DD_API/10_Admin_quan_tri_noi_dung/S2W-STUDY-API-127_POST_admin_content_content_type_content_id_publish.xlsx`
- Method + endpoint: `POST /api/v1/admin/content/{content_type}/{content_id}/publish`
- Kết luận: **CẦN SỬA**

## Diff bắt buộc với SEQ-11

SEQ-11 mô tả đây là mutation publish/archive/update: request có `targetStatus`, `changeType`, `reason`, `notifyAffectedLearners`; hệ thống cập nhật publish status, ghi audit before/after và có thể gửi notification; response trả `contentType`, `id`, `publishStatus`, `auditLogId`, `notificationBatchId`. DD lại thiết kế một API “xem tác động trước”, nhận `proposed_action/change_summary`, trả recommendation và không cập nhật content. Đây không còn là API trong SEQ-11.

## Findings

| Severity | Sheet + cell | Mô tả cụ thể | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P1 | `00.Hướng dẫn!A4:B4`, `Cover!B19` | DD dùng inventory 44 file/không schema dù hiện có 48 file và SQL. | `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:1-31`; canonical `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Cập nhật inventory/schema/precedence; bỏ VERIFIED tới khi contract được sửa. |
| P0 | `2.Response!D9:D11`, `2.Response!A37` | Envelope/error dùng format cũ, không có canonical business code/message/traceId. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Dùng canonical envelope/camelCase. |
| P1 | `2.Response!A25` | Non-list mutation chứa `meta.page/page_size`; pagination mẫu thừa. SEQ `meta:{}` cũng phải nhường canonical mới hơn. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700`; SEQ-11 `docs/BD/diagram/SEQUENCE/11. Study2Work_Study_SEQ_Admin_Quan_Tri_Noi_Dung.md:95-111` | Bỏ `meta`; `traceId` top-level. |
| P1 | `3.Data mapping!A20`, `00.Hướng dẫn!A13:B18` | UPDATE_ACTION còn `<current_columns>/<mapping>` và checklist tự tick hoàn tất. | `docs/BD/base/0. Study2Work_System_Architecture.md:601-628,738-752` | Viết dispatch, transition UPDATE, audit và outbox cụ thể; checklist để chưa đạt. |
| P1 | `Cover!B10`, `1.Request!D21:D22` | DD dùng `{content_type}/{content_id}`, khác chính xác SEQ-11 `{type}/{id}`. | SEQ-11 `:28-31,76-93`; versioning `docs/BD/base/0. Study2Work_System_Architecture.md:738-751` | Giữ param của contract hoặc làm migration/version review đồng bộ. |
| P0 | `Cover!B4:B10`, `Overview!A8`, `Overview!A12` | Mục đích DD là “xem tác động trước khi xuất bản”, trái endpoint `/publish` và SEQ-11 là mutation thực. | SEQ-11 `:28-36`; BD-10 `:159-167` | Chuyển phần xem tác động sang pre-publish/impact API; `/publish` phải thực hiện transition atomically. |
| P0 | `1.Request!D23:I24`, `1.Request!A27` | Request trực tiếp từ SEQ là `{targetStatus,changeType,reason,notifyAffectedLearners}`; DD thay bằng opaque `proposed_action: Object` và optional `change_summary`, làm mất target/status/reason/notify decision. | SEQ-11 `:76-93` | Khôi phục đúng bốn field, enum/rules/nullability; reason bắt buộc cho important/archive, notify boolean explicit. |
| P0 | `2.Response!C16:H21`, `2.Response!A25` | SEQ trả content/status/audit/notification IDs; DD chỉ trả validation/impact/recommendation, nên client không biết publish có xảy ra. Counts còn sai kiểu String. | SEQ-11 `:95-111` | Trả `contentType,id,publishStatus,auditLogId,notificationBatchId` đúng kiểu; impact thuộc pre-check, không thay result mutation. |
| P0 | `3.Data mapping!D12:H16`, `5.DB_Update_Main!A6:I11` | DD SELECT/UPDATE `study.users.proposed_action/change_summary`; `users` không có content discriminator/cột đó. Không hề update `publish_status` của target. | SQL users `:239-249`; content status SQL `:323-374,458-500`; SEQ-11 `:30-32` | Dispatch content type tới bảng thật; lock row, validate current transition, update `publish_status/published_at` và check affected rows. |
| P0 | `1.Request!D10`, `Overview!D5`, `4.Error!A11:H11` | Permission dùng `study.content.manage` cho cả Content Admin; BD phân vai Content Admin soạn/gửi review, còn Admin xuất bản/lưu trữ. | BD-10 `:24-31`; lifecycle rules `:35-51` | Dùng permission publish riêng, ví dụ `study.content.publish`, và map role/permission rõ; không chỉ kiểm tên role hiển thị. |
| P0 | `3.Data mapping!D15:H15`, `6.DB_Update_Related!A8:I8` | Side effect chỉ có audit generic; không có notification batch/outbox. Chưa bảo đảm status + audit + outbox cùng transaction và gửi sau commit. | SEQ-11 `:28-36,114-117`; architecture `docs/BD/base/0. Study2Work_System_Architecture.md:601-628` | Persist content transition, audit before/after và outbox/notification batch atomically; worker gửi sau commit, có dedupe/idempotency. |
| P0 | `3.Data mapping!C13:G14`, `4.Error!A15:H16` | DD không chứng minh pre-publish checklist vừa chạy trên cùng version; concurrent edit giữa check và publish có thể bypass nguồn/quyền/completion. | BD-10 `:146-182`; SEQ-11 `:22-35` | Publish re-run blocking checks dưới lock hoặc nhận validated content version/check token; conflict nếu version đổi. |

## Checklist duyệt lại

- [ ] Source inventory là 48 file; bỏ VERIFIED tới khi re-review.
- [ ] URI/path param khớp SEQ-11 hoặc có version migration.
- [ ] `/publish` là mutation, không phải impact preview.
- [ ] Request đúng `targetStatus/changeType/reason/notifyAffectedLearners`.
- [ ] Response đúng `contentType/id/publishStatus/auditLogId/notificationBatchId`.
- [ ] Permission publish riêng được enforce.
- [ ] Target table/status mapping, lock/version và checklist atomic.
- [ ] Audit + outbox notification cùng transaction; retry/idempotency/test đầy đủ.
