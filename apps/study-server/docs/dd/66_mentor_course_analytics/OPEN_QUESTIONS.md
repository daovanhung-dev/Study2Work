# Open Questions — Study API #66

Status: Draft — Needs Confirmation. Local runtime dùng activity proxy vì schema hiện có không lưu event history.

## Quyết định DERIVED đang dùng cục bộ

1. Activity proxy lấy từ lesson_progress.last_accessed_at, trên lesson PUBLISHED và user.role=STUDENT.
2. tracked_lesson_accesses đếm cặp user_id/lesson_id phân biệt có timestamp; không đếm số lần truy cập hoặc learning events.
3. students_with_activity đếm Student phân biệt trong các cặp proxy.
4. last_activity_at là MAX timestamp đang lưu; empty aggregate trả 0, 0, null.
5. Course permission dùng direct courses.mentor_id so với JWT sub; course thiếu trả 404, course owner khác trả 403.
6. Local response là summary object để phục vụ mục tiêu AC-26; catalog/diagram vẫn ghi ApiEnvelope<Page<Course>>.
7. Request không khai báo page/size hoặc from/to; endpoint không thêm query params.
8. DD và fallback vẫn Draft — Needs Confirmation; fake-DB test không chứng minh schema live/deployment.

## Cần product/domain owner xác nhận

1. Có chấp nhận activity proxy từ current progress state khi AC-26 yêu cầu learning events?
2. Có event ledger khác hoặc event-producing source chưa nằm trong checked-in DDL không? Nếu có, cung cấp relation, taxonomy, actor mapping, event key/timestamp, retention và retry/dedup rule.
3. Contract success có được đổi từ Page<Course> sang activity summary không? Nếu giữ Page<Course>, metrics sẽ được trả ở field/schema nào?
4. Activity có cần giới hạn enrollment ACTIVE, lesson status, loại event hoặc khoảng thời gian không?
5. Mentor access chỉ gồm direct owner hay còn course assignment? Xác nhận live identity/schema và 403/404 privacy order.
6. Null/timezone/freshness/retention expectations cho last_activity_at là gì?

## Macro-review AC-26 #65–#67

- #65 trả roster progress; #66 hiện trả các dấu activity proxy; #67 trả progress của Student được chọn.
- Không có server-to-server calls giữa ba API.
- students_with_activity không phải enrollment count; tracked_lesson_accesses không phải learning-event count.
- API #65/#67 và #66 có nguồn/schema khác nhau nhưng dùng cùng legacy course owner boundary cục bộ.
- DD #67 vẫn mô tả Mentor guard chưa có và error helper mặc định data {}; hiện các mô tả này đã stale vì shared guard nhận MENTOR và error helper trả data null. API #67 vẫn UNWIRED; reconcile trong phiên triển khai #67.
- Catalog/diagram đều vẫn khai báo Page<Course>, thiếu pagination inputs; #66 summary response là discrepancy DERIVED.
- Runtime checks cho #66/#65 là fake-DB HTTP tests; live schema, migration và deployment chưa được xác nhận.
