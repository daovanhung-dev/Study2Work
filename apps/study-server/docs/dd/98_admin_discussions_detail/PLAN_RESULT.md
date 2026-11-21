# PLAN_RESULT — Study API #98

## Kết quả

- Tạo DD tiếng Việt cho `GET /api/v1/admin/discussions/{discussion_id}`.
- Giữ nguyên Bearer JWT/Admin, path `discussion_id:int64!`, `ApiEnvelope<Page<Discussion>>`, HTTP 200 và đúng errors 401/403/404/500.
- Đọc AC-37 flow từ #97 queue đến #98 detail, rồi decision sang #99/#100.
- Đề xuất one-item Page và direct child comments theo #42, gắn `DERIVED`; không áp dụng Student enrollment/ACTIVE filter cho Admin.
- Ghi rõ report relation/response fields và Discussion.title chưa có source; không tạo report table/query/field.
- Tạo 8 template-backed sheets + 3 reports; DD vẫn `Draft — Needs Confirmation`.

## Plan result

| Hạng mục | Kết quả |
|---|---|
| Request/response/error | Direct catalog contract retained |
| Thread/Page behavior | One-item Page/root/direct-child proposal is `DERIVED` and pending confirmation |
| Report detail | AC-37 logical read recorded; physical relation and response projection `SOURCE_REQUIRED` |
| DB mapping | Legacy discussion/users columns listed only as candidates; no guessed SQL |
| Mutation | N/A — read-only |
| AC-37 macro-review | Completed after #100; report/thread/projection gaps remain open |
| Output | Markdown only; 11 expected files |

## Chưa quyết định

See [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md): report schema/response, thread target grain, title, pagination, comments visibility, Admin guard and parse/error integration.
