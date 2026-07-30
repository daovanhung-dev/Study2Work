# Kết quả Plan 12 — Notifications

- Phạm vi: API 083–093.
- Hoàn thành workbook: 11/11.
- Trạng thái: Draft; API suy dẫn cần xác nhận.
- Naming contract: camelCase cho JSON/query; path placeholder giữ nguyên catalog; DB dùng snake_case.
- Lưu ý nguồn: bundle hiện tại thiếu System Architecture, Study Architecture, schema seed SQL và API catalog CSV được plan viện dẫn.

| API | Method | Endpoint | Basis | Status | Workbook | DB ghi |
|---:|---|---|---|---|---|---|
| 083 | GET | `/api/v1/notifications` | TRỰC TIẾP | Draft | `API_083_GET_notifications.xlsx` | Không |
| 084 | GET | `/api/v1/notifications/unread-count` | SUY DẪN | Draft — Needs Confirmation | `API_084_GET_notifications_unread_count.xlsx` | Không |
| 085 | PATCH | `/api/v1/notifications/{notification_id}/read` | TRỰC TIẾP | Draft | `API_085_PATCH_notifications_by_notification_id_read.xlsx` | notifications |
| 086 | POST | `/api/v1/notifications/read-all` | SUY DẪN | Draft — Needs Confirmation | `API_086_POST_notifications_read_all.xlsx` | notifications |
| 087 | DELETE | `/api/v1/notifications/{notification_id}` | SUY DẪN | Draft — Needs Confirmation | `API_087_DELETE_notifications_by_notification_id.xlsx` | notifications |
| 088 | GET | `/api/v1/notification-settings/me` | SUY DẪN | Draft — Needs Confirmation | `API_088_GET_notification_settings_me.xlsx` | Không |
| 089 | PUT | `/api/v1/notification-settings/me` | TRỰC TIẾP | Draft | `API_089_PUT_notification_settings_me.xlsx` | notification_settings |
| 090 | POST | `/api/v1/admin/notifications/recipient-preview` | SUY DẪN | Draft — Needs Confirmation | `API_090_POST_admin_notifications_recipient_preview.xlsx` | Không |
| 091 | POST | `/api/v1/admin/notifications` | TRỰC TIẾP | Draft | `API_091_POST_admin_notifications.xlsx` | notification_batches, audit_logs, notification_recipients, outbox_events |
| 092 | GET | `/api/v1/admin/notifications` | SUY DẪN | Draft — Needs Confirmation | `API_092_GET_admin_notifications.xlsx` | Không |
| 093 | POST | `/api/v1/admin/notifications/{batch_id}/cancel` | SUY DẪN | Draft — Needs Confirmation | `API_093_POST_admin_notifications_by_batch_id_cancel.xlsx` | notification_batches, audit_logs, outbox_events |

## Reviewer notes

- Đối chiếu endpoint/contract suy dẫn với PO/BA trước khi đổi trạng thái Final.
- Đối chiếu logical table/column với schema seed SQL khi được cung cấp.
