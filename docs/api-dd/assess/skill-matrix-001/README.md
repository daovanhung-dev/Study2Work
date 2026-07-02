# API DD - SKILL-MATRIX-001

| Field | Value |
|---|---|
| Status | `DRAFT` |
| Updated | `2026-07-02` |
| Module | `ASSESSMENT` |
| Endpoint | `GET /api/v1/me/skill-matrix` |
| Source checklist | `docs/checklists/API.md` |
| Worklog | `.agent/worklog/2026-07/0004_api_dd_canonical_drafts.md` |

## Purpose

Folder này là bản API Detail Design draft cho `SKILL-MATRIX-001`. Nội dung được tạo từ BD, API checklist và diagrams; các điểm chưa có source rõ ràng được ghi trong Open Questions.

## Files

| File | Purpose |
|---|---|
| `01_Overview/Overview.md` | Mục tiêu, scope, trace source, authorization, ownership, async side effects. |
| `02_History/History.md` | Lịch sử thay đổi DD. |
| `03_Request/Request.md` | Header, path/query/body field dictionary, validation sequence, request example. |
| `04_Response/Response.md` | Response matrix, success/error envelope, data fields, pagination. |
| `05_DataMapping/DataMapping.md` | Runtime flow, table access, transaction, idempotency, audit/event/job, tests. |
| `06_Error/Error.md` | Error catalog, error envelope và logging rules. |
| `API_DD_CHECKLIST.md` | Readiness checklist và approval placeholders. |
| `HUONG_DAN_NHAP_LIEU_DD.md` | Hướng dẫn cập nhật DD này trong các lần review sau. |
