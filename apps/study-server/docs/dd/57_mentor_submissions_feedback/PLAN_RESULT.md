---
title: "Plan Result — Study API #57 Lưu feedback"
order: 9
dd_id: "57"
api_name: "Lưu feedback bài nộp Mentor"
status: "Draft — Needs Confirmation"
---

# Kế hoạch DD — Study API #57 Lưu feedback bài nộp Mentor

## Trạng thái kế hoạch

**Plan được ghi trước khi tạo sheets và runtime code.** DD giữ trạng thái `Draft — Needs Confirmation`; runtime chọn các fallback DERIVED bên dưới, nhưng contract owner chưa xác nhận wire key, attachments, history hoặc identity mapping.

## Hợp đồng giữ nguyên

| Thuộc tính | Giá trị | Nguồn/trạng thái |
|---|---|---|
| API ID | `57` | Catalog |
| Method/path | `POST /api/v1/mentor/submissions/{submission_id}/feedback` | Catalog + AC-23; DIRECT |
| Actor/auth | Bearer JWT; role `Mentor` | Catalog + AC-23; DIRECT |
| Path | `submission_id:int64!` | Catalog; DIRECT |
| Body field 1 | `feedback text:string!` | Catalog descriptor; runtime dùng `feedback_text` làm wire key DERIVED |
| Body field 2 | `attachments:string!` | Catalog; định dạng và persistence chưa rõ |
| Success | HTTP `200`, `DESIGN_RESOURCE_UPDATED`, `ApiEnvelope<Submission>` | Catalog + AC-23; DIRECT |
| Errors | `401 DESIGN_AUTHENTICATION_REQUIRED`; `403 DESIGN_ACCESS_DENIED`; `404 DESIGN_RESOURCE_NOT_FOUND`; `422 DESIGN_VALIDATION_ERROR`; `500 DESIGN_INTERNAL_ERROR` | Catalog + diagram; DIRECT |

Không thêm query, success field, status code hay business code.

## Flow AC-23

`#54` đọc danh sách → `#55` đọc submission, files và rubric → Mentor nhập điểm/nhận xét → `#56` cập nhật điểm và `status=GRADED` → `#57` lưu feedback → UI báo thành công.

Flow trên chỉ mô tả thứ tự UI. Không biến `status=GRADED` thành điều kiện bắt buộc cho gọi trực tiếp API #57 khi contract chưa nói vậy. API #57 không thay đổi score/status do #56 sở hữu.

## Cách thiết kế

1. Đọc feedback từ `assignment_submissions.feedback TEXT` như candidate hiện có; đề xuất cập nhật field đó cho submission được chọn, gắn nhãn `DERIVED`.
2. Runtime dùng UPDATE ghi đè một field feedback; đây là fallback DERIVED vì diagram cũng ghi `INSERT/UPDATE` nhưng không có history relation. Cần contract owner xác nhận semantics.
3. Runtime nhận `attachments` như strict opaque string nhưng không parse, lưu hoặc echo; không ánh xạ sang `assignment_submissions.file_url` hoặc student `Submission.files`. Format và persistence target vẫn chưa có nguồn.
4. Không nối bảng rubric assessment dùng UUID của V1-PILOT vào submission BIGINT legacy.
5. Reuse API #54's DERIVED constrained UploadAsset lookup for student `Submission.files`; API #35 URL persistence and separate feedback attachment handling remain unresolved.
6. Dùng candidate direct-owner `courses.mentor_id` thống nhất với #54–#56, chỉ ở mức `DERIVED`. Shared guard cung cấp numeric subject; assigned-Mentor và null/orphan relation chưa được xác nhận.
7. Giữ status sau #56 và candidate feedback trong response; `files[]` follows the API #54 fallback, with API #35 compatibility unresolved.
8. API Guidelines and the current helper both emit error `data=null`; the dynamic #57 route template is registered in middleware and maps validation/internal errors to `DESIGN_*`.

## Nguồn được đọc

- [Catalog API](../../../../../docs/lists/list_api.md), rows #54–#57 và reusable Submission/UploadAsset.
- [AC/API index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md), AC-23.
- [AC-23 draw.io](../../diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio), page AC23, tất cả node và edge.
- [DB table guide](../../diagrams/DB_UNICA_TABLES.md), assignment_submissions, assignments và courses.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql), các cột candidate và quan hệ nullable.
- [V1-PILOT DDL](../../../../../infra/postgres/02_study_db.sql), mô hình assessment/rubric UUID tách biệt.
- DD [#54](../54_mentor_submissions_list/02_Overview.md), [#55](../55_mentor_submissions_detail/OPEN_QUESTIONS.md), [#56](../56_mentor_submissions_grade/OPEN_QUESTIONS.md).
- [API Guidelines](../../../../../contracts/api-guidelines/README.md), [Study middleware](../../../app/core/middleware.py) và [response helper](../../../app/core/responses.py).
- [Study route source](../../../app/api/v1.py), inventory module và test; API #57 chưa có.
- Đã mở đủ tám Markdown template có registry; không có archive source trong phạm vi. Workflow Study chỉ giao Markdown.

## Ma trận dự kiến

| Thành phần | Phạm vi |
|---|---|
| Request usage | Authorization, path ID, descriptor feedback text và attachments; không có query/body field bổ sung |
| Query | Đọc submission và course scope theo candidate; giữ nhánh null/orphan/access unresolved |
| Mutation | Runtime UPDATE assignment_submissions.feedback as DERIVED overwrite; attachment persistence SOURCE_REQUIRED |
| Response source | Mọi field envelope, Submission và nested UploadAsset; giữ score/status; note DERIVED API #54 file lookup and unresolved producer compatibility |
| Error | Chính xác 401/403/404/422/500 theo catalog |
| Deliverables | 8 template sheets + 1 mapping table candidate + 3 report; chỉ Markdown |

## Cổng kiểm tra sau soạn

- Đúng manifest 11 file; phụ lục của cả 8 sheet khớp template byte-for-byte.
- Từng request/response field được liệt kê riêng.
- Contract và error set khớp catalog; không thêm business code.
- Mutation candidate chỉ chạm feedback column hiện có; không tạo persistence cho attachment/rubric.
- JSON, relative links/anchors, độ rộng bảng, code fence, metadata và whitespace đã được kiểm tra.
- Macro-review #54–#57 được ghi trong report và worklog liên quan.
- DD lúc tạo ghi runtime tests NOT_RUN; implementation kết quả được ghi ở phần dưới.

## Kết quả sau soạn

- Đã tạo đủ 8 sheet theo template, một mapping candidate assignment_submissions.feedback và ba report; tổng cộng 11 file.
- Contract, error set, độ phủ field, template appendix, JSON, liên kết/anchor, bảng, code fence và whitespace đã được kiểm tra.
- Macro-review #54–#57 hoàn tất ở mức tài liệu; #54 cardinality/file lookup are DERIVED, while rubric, producer compatibility, assigned-Mentor access and feedback attachments remain open.
- At DD authoring time API #57 was UNWIRED; the current route/module/tests are recorded below.

## Kết quả implementation

- Added the route, request/response models, signed-int64 validator, SQL constants, view orchestration and middleware template registration.
- Runtime updates only the legacy `assignment_submissions.feedback` candidate with direct-owner predicate; score/status remain unchanged. Required `attachments` is accepted opaquely and not persisted or returned.
- The response reuses API #54 `SubmissionResponse` and constrained student-file lookup. Fallback choices remain DERIVED/SOURCE_REQUIRED; DD remains Draft — Needs Confirmation.
- Focused API #57 suite: 28 passed; full Study Server suite: 538 passed; Ruff and OpenAPI route checks pass. Tests use fake DB results. Live schema, migrations, deployment and AC-23 end-to-end remain NOT_VERIFIED.
