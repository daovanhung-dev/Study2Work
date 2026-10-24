# PLAN_RESULT — Study API #103

## Kết quả API

- API: #103 — Xuất báo cáo tác động cộng đồng.
- Method/endpoint: GET /api/v1/admin/reports/community-impact/export.
- Trạng thái tài liệu: Draft — Needs Confirmation.
- Mức hoàn thành: PARTIALLY COMPLETED.
- Trạng thái quyết định: NEEDS USER DECISION cho contract cuối.
- Trạng thái runtime: UNWIRED / NOT_FOUND — chưa tìm thấy route/module/query/export worker của Study.
- Thư mục đầu ra: apps/study-server/docs/dd/103_admin_reports_community_impact_export/.
- Deliverables: 8 sheet Markdown, PLAN_RESULT.md, OPEN_QUESTIONS.md và VERIFICATION_REPORT.md. Không tạo ZIP theo override của server-study.

## Căn cứ

- Contract API: row #103, schema Report/Operation/ExportAsset và mục Operation tracking trong docs/lists/list_api.md.
- Luồng AC: index AC-38 và page AC38 trong AC_04_ADMIN_MANAGEMENT.drawio.
- Ranh giới poll: DD API #18 và OPEN_QUESTIONS.md của API #18.
- API producer liên quan: discrepancy Notification/Operation của API #93.
- Tính liên tục báo cáo: DD #101 summary và #102 community report.
- Schema/storage: DB_UNICA_ERD.drawio, DB_UNICA_TABLES.md, legacy Study DB.sql và V1-PILOT 02_study_db.sql.
- Runtime: router, source search và test search của Study; không có handler export/poll API #103.
- Authoring: skill createDD-markdown đã đăng ký, 8 template Markdown, workflow Markdown-only của Study.

## Contract trực tiếp

- GET /api/v1/admin/reports/community-impact/export.
- Bearer JWT; role Admin; query tùy chọn filters:string và format:string.
- Không có path parameter hoặc request body.
- HTTP 202 DESIGN_OPERATION_ACCEPTED.
- Errors chính xác: 401 DESIGN_AUTHENTICATION_REQUIRED; 403 DESIGN_ACCESS_DENIED; 503 DESIGN_DEPENDENCY_UNAVAILABLE; 500 DESIGN_INTERNAL_ERROR.
- Endpoint row ghi ApiEnvelope<Report>; Operation tracking paragraph ghi data:Operation. Cả hai đều là bằng chứng DIRECT trong catalog nhưng mâu thuẫn.

## Luồng AC-38

Admin mở dashboard → #101 summary → #102 community metrics → chọn export hoặc view-only → tạo CSV/XLSX/PDF hoặc job → lưu File Storage tạm nếu file được tạo phía server → UI hiển thị report/tải file. AC-38 cũng tham chiếu poll GET /api/v1/operations/{operation_id}.

## Read/write và side effect

- Nguồn đọc ứng viên: community report theo semantics #102; hiện chưa có service/query.
- Tác động logic: nhận async Operation và tùy trường hợp lưu artifact export tạm.
- Chưa có physical mapping Study được duyệt cho Operation/queue/export. Pilot file_objects và report_snapshots là các candidate riêng, không được chọn làm mapping thực thi.

## Đề xuất DERIVED

Để có luồng async nhất quán, trả Operation tại 202 và để client poll API #18; job hoàn tất có thể cung cấp ExportAsset. Endpoint row, Operation.result?:Payment, các gap ID/quyền/lifecycle của API #18 và chính sách storage vẫn chưa được giải quyết. Đề xuất này không sửa nguồn canonical.

## Xung đột và câu hỏi mở

Xem OPEN_QUESTIONS.md: payload response; Operation ID/result; parser/default của filters/format; queue và retry GET; storage/quyền tải/expiry; quyền Admin; tính nhất quán với metrics/kỳ của #101/#102.
