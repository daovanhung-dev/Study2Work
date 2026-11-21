# Plan Result — API #82 Lấy danh sách lesson

## Kết quả

Đã triển khai cục bộ `GET /api/v1/admin/lessons` và đồng bộ DD Markdown cùng server-study context. Runtime dùng shared `ADMIN` JWT guard, đọc legacy BIGINT `lessons` candidate, hỗ trợ exact filters `course`/`status`, trả `Lesson[]`, và từ chối rõ `type` bằng 422 do schema source không có mapping tương thích.

## Quyết định implementation

- Giữ discrepancy giữa catalog `ApiEnvelope<Lesson>` và list intent; local `ApiEnvelope<Lesson[]>` là fallback DERIVED, DD vẫn `Draft — Needs Confirmation`.
- `course` parse signed int64; `course`/`status` là exact match. Không thêm default `PUBLISHED`, page, size, count hay join.
- `type` vẫn có trong OpenAPI theo catalog; khi được gửi, trả `DESIGN_VALIDATION_ERROR`/`UNSUPPORTED_FILTER` thay vì bỏ qua.
- Legacy `lessons` là query candidate, không phải live schema proof. Required projection null gây 500 an toàn và rollback; optional `content`/`video_url` null được giữ.
- Shared guard kiểm tra role `ADMIN`; dedicated AC-34 permission, live schema, enum đầy đủ, pagination policy và deleted visibility còn mở.

## Verification boundary

- Kết quả chạy: focused 15 tests, linked #09/#78/#82 regression 47 tests, full Study suite 1012 tests, scoped Ruff pass và OpenAPI 48 paths / 53 operations; DD static checks pass. Context validator có baseline DB Admin failures được nêu trong [Verification Report](./VERIFICATION_REPORT.md).
- Fake DB tests xác minh HTTP/source behavior cục bộ, không chứng minh live database, migration deployment hoặc owner approval.

## Phạm vi

Chỉ API #82 runtime, tests, DD #82, AC-34 report note có liên quan và server-study context/worklog. Không sửa catalog, diagram, schema hoặc behavior của APIs #83–#86; không stage/commit.
