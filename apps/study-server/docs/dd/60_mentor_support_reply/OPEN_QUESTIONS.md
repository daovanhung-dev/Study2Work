# OPEN_QUESTIONS — Study API #60

Status: `Draft — Needs Confirmation`. Runtime uses the documented local fallback; each choice remains DERIVED until the API/data owners approve it.

| ID | Câu hỏi còn mở | Quyết định hiện tại cho local implementation | Còn cần xác nhận |
|---|---|---|---|
| Q-60-01 | `attachment refs` có wire key `attachment_refs` và JSON array string của UploadAsset int64 IDs không? | Dùng `attachment_refs` dạng chuỗi JSON array, thứ tự được giữ, `[]` nghĩa không đính kèm; cùng pattern đang có trong API #47 source. | Thống nhất catalog/API #35/#47/#60 khi macro-review; wire key/encoding vẫn DERIVED. |
| Q-60-02 | Upload registry và điều kiện file có thể gắn vào reply? | Dùng bảng `uploads` local; yêu cầu cùng Mentor, request course, purpose `LECTURE`, status `UPLOADED`; asset thiếu/ngoài scope trả 404 chung. | DDL/source local không chứng minh live registry hoặc storage URL còn hoạt động. |
| Q-60-03 | Support model/IDs được phê duyệt chính thức? | Dùng BIGINT `support_requests`, `support_messages`, `support_message_uploads` trong migration 008 như local fallback của #58/#59. | Cần data owner phê duyệt schema; live schema/deployment chưa xác minh. |
| Q-60-04 | Mentor principal và request assignment scope? | Dùng numeric JWT `sub` làm `users.id`, shared MENTOR guard và trực tiếp `courses.mentor_id`. | Chưa có quan hệ assigned Mentor được nguồn xác nhận; owner policy là DERIVED. |
| Q-60-05 | Message có nonblank/length/visibility rule nào? | Từ chối whitespace-only, lưu nguyên text; không đặt length cap. Dùng message thread chung vì local schema không có internal flag. | Business owner cần xác nhận blank/length và visibility policy. |
| Q-60-06 | Có cho reply sau RESOLVED/CANCELLED không? | Không chặn theo status và không reopen; giữ status hiện tại vì #61 sở hữu resolve và #60 không khai báo 409. | Post-resolve/cancel behavior cần xác nhận. |
| Q-60-07 | Response cần giới hạn/thread pagination không? | Rehydrate toàn bộ thread theo API #59: message `created_at ASC, id ASC`, assets theo `asset_position ASC`. | Giới hạn thread/performance và response size chưa được contract định nghĩa. |
| Q-60-08 | Transaction có rollback nếu insert/link/read-back/commit lỗi không? | Khóa request, ghi message và links, hydrate response, validate rồi commit một lần; failure rollback và trả 500 an toàn. | Local convention/test xác minh code path với fake DB; chưa xác minh concurrency/live DB. |
| Q-60-09 | Content-Type của request? | Dùng `application/json` cho strict body model. | DERIVED transport choice do catalog không ghi media type. |

## Giới hạn giữ nguyên

- Không đổi catalog, API #35/#47, API #61, diagram hoặc DB schema trong task #60.
- Không thêm status mutation, notification, 409 hay 503.
- Migration 008 và các TestClient fake-DB checks là source evidence; không xác nhận live schema, deployment hoặc storage behavior.
- AC-24 macro-review #58–#61 vẫn cần rà soát sau khi API #61 được implement.
