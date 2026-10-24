# PLAN_RESULT — Study API #97

## Kết quả

- Đã author DD Markdown tiếng Việt cho `GET /api/v1/admin/discussions/reported`.
- Giữ nguyên contract trực tiếp: Bearer JWT/Admin, query `reason?:string`, `severity?:string`, `page?:int32`, `ApiEnvelope<Page<Discussion>>`, HTTP 200 và errors 401/403/500.
- Ghi AC-37 flow đọc reports + discussion summary; không phát minh physical report table, field hoặc query.
- Ghi rõ response `Discussion` thiếu report data; `title` không có trong legacy DDL; pagination/Admin policy còn cần nguồn/confirmation.
- Tạo 8 template-backed sheets và 3 reports. DD status vẫn `Draft — Needs Confirmation`.

## Plan result

| Hạng mục | Kết quả |
|---|---|
| Contract matrix | Direct catalog contract retained; no additional API fields/codes |
| Request/query mapping | Every declared query listed; semantics/defaults open |
| Read mapping | Logical Q1 plus legacy candidate projections separated; no guessed SQL |
| Mutation mapping | N/A — read-only |
| Response mapping | PageMeta, Discussion, DiscussionComment and UserSummary fields inventoried |
| AC-37 review | #97 flow and post-#100 macro-review recorded; contract/schema gaps remain open |
| Output format | Markdown only, 11 expected files |

## Chưa quyết định

See [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md): report relation/grain, response report fields, Discussion title, filters, pagination, comments scope, Admin authorization and future error integration.
