---
task_id: "2026-10-12-review-study-api27-32-dds"
date: "2026-10-12"
primary_task_type: "docs"
secondary_task_types: ["review"]
project_scopes: ["server-study"]
cross_scope_dependencies: ["docs/lists/list_api.md", "apps/study-server/docs/diagrams/"]
status: "VERIFIED"
---

# Worklog: Rà soát Study API DD #27–#32

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-12/commit-push-study-dds.md`
    - carry_forward: Không suy luận runtime từ DD; giữ nguyên các artifact hiện có và tách behavior thiết kế khỏi source hiện hành.
  - path: `.agents/worklog/2026-10-12/create-study-api27-dd.md`
    - carry_forward: API #27 là design-only; giữ open questions về entitlement, curriculum order, no-next behavior và nullable `lessons.course_id`.
  - path: `.agents/worklog/2026-10-12/create-study-api28-dd.md`
    - carry_forward: API #28 giữ error set của catalog; ghi rõ discrepancy 403/409 với AC-16, schema gap QuizChoice/QuestionType và nullable foreign keys.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Rà soát sáu DD #27–#32 với API catalog, diagram AC-15/AC-16, ERD, DB table design và current Study source; báo findings bằng tiếng Việt có vị trí và bằng chứng. Không sửa DD, API contract hoặc schema.
- Canonical contract/approved DD: `docs/lists/list_api.md` là `APPROVED_DESIGN_CONTRACT`; phân biệt lỗi DD với `DISCREPANCY` giữa nguồn và `SOURCE_REQUIRED`.

## CURRENT_BEHAVIOR

- Source/config: `apps/study-server/app/api/v1.py` hiện đăng ký các route đang có; scan module/tests không tìm thấy API #27–#32. `app/utils/auth.py` hiện parse numeric positive `sub` và yêu cầu role `STUDENT`. Checked-in `infra/postgres/study-server/DB.sql` là design evidence: quiz foreign keys nullable, `quiz_answers.is_correct` NOT NULL; không kiểm tra live metadata.
- Runnable tests: Không chạy runtime tests; task chỉ rà tài liệu.
- Runtime wiring: API #27–#32 `UNWIRED / NOT_FOUND`; không dùng DD làm bằng chứng runtime.

## SOURCE_TRACE

```text
User request -> API catalog #27–#32 -> AC-15/AC-16 -> DB_UNICA ERD/table design + checked-in DDL
-> current Study router/module/test scan -> DD sheet/report/static validation -> findings
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #27 next lesson | AC-15 chỉ yêu cầu đọc curriculum order; cùng course, direction/tie-break, visibility và terminal result chưa được xác định. DD ghi các câu hỏi này. | `SOURCE_REQUIRED` | Cần owner chốt trước khi implementation; không phải lỗi DD đã xác nhận. |
| API #28 eligibility 403/409 | AC-16 diagram nêu 403/409 cho eligibility/attempt limit/expiry; catalog API #28 chỉ có 401/403/404/500. DD giữ catalog và đánh dấu xung đột. | `DISCREPANCY` | Cần xác định nhánh thuộc API #28 hay #29/cập nhật contract; DD không tự thêm 409. |
| API #29 eligibility and initial response | AC-16 không gán 403/409 theo điều kiện; `QuizAttempt.answers[]` required nhưng giá trị ban đầu chưa được quy định. DD ghi open questions. | `SOURCE_REQUIRED` | Cần policy cho eligibility và response create. |
| API #30 answer persistence | Catalog `answer(s):string!` chưa khớp `choice_ids`/`text_answer`; DDL chỉ lưu một `choice_id`, yêu cầu `is_correct NOT NULL` trước bước grading ở API #31, và không có unique key cho upsert. DD ghi rõ các điểm này. | `DISCREPANCY / SOURCE_REQUIRED` | Chặn chốt request/storage/upsert semantics; không phải kết luận lỗi DD. |
| API #31 grading | AC-16 nêu SUBMITTED rồi PENDING_GRADE/GRADED nhưng thiếu enum đầy đủ, công thức, manual-grade predicate, repeat-submit và transaction rules. DD giữ các điểm mở. | `SOURCE_REQUIRED` | Cần rule grading/state trước implementation. |
| API #32 result | AC-16 nhắc feedback nhưng logical schema và candidate tables không có field feedback; pending-grade score và answer/correctness disclosure chưa được policy chốt. DD ghi discrepancy/open questions. | `DISCREPANCY / SOURCE_REQUIRED` | Cần cập nhật contract/schema hoặc xác nhận flow trước approval. |
| Lesson/quiz/attempt foreign keys | `DB_UNICA_TABLES.md`/ERD mô tả một số FK là bắt buộc, còn checked-in DDL cho phép NULL. DDs đánh dấu candidate/design-only. | `DISCREPANCY / DESIGN_ONLY` | Xác nhận baseline schema trước triển khai; không suy luận live DB. |
| API #31 verification report | `VERIFICATION_REPORT.md:26` ghi template SHA-256 của `05_Data_Mapping.md` dài 60 ký tự và không khớp SHA-256 của template canonical. | `ERROR` | Lỗi traceability nhỏ trong report; cần sửa fingerprint trước khi dựa vào baseline verification. |

## CHANGES

- Files changed: Worklog này. Sáu DD và nguồn đối chiếu không bị sửa.
- CONTEXT_UPDATES: None; không có thay đổi source/contract/context.
- Context pages changed: None.
- Assumptions: Report chỉ nêu lỗi xác nhận nếu có bằng chứng mâu thuẫn trong DD; các khoảng trống được phân loại riêng. Không chạy runtime tests.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type docs --limit 3` | Chọn và đọc ba worklog liệt kê ở `PRIOR_WORKLOG_REVIEW`; không thiếu log. | VERIFIED |
| Static audit sáu DD folders | Đủ 11 file cho mỗi API #27–#30 và #32, 12 file cho #31; 8 sheet chuẩn mỗi API, #31 có thêm mapping thứ hai; front matter/order đúng. | VERIFIED |
| Markdown/JSON/link/whitespace audit | JSON: #27 2, #28 2, #29 2, #30 2 response fences + request body JSON hợp lệ, #31 2, #32 3; bảng Markdown, 158 relative links/anchors và whitespace không có lỗi. | VERIFIED |
| Catalog contract check | Method/path, success code và error status của #27–#32 khớp catalog; API #28 không thêm 409 và API #30 không thêm 409. | VERIFIED |
| Report fingerprints | Output fingerprints của #28–#32 khớp file hiện tại. Riêng template fingerprint API #31 tại `VERIFICATION_REPORT.md:26` sai: report ghi `11bc77bc0522d3af27b9499114991c881a5dd3210c6f2cb949be088dcc5b` (60 ký tự), canonical là `11bc77bc0522d3af27b9499114991c8819046ac32bde5c1efdc841be088dcc5b`. | FINDING |
| Current route/module/test scan | `api/v1.py` không có route #27–#32; scan modules/tests không tìm thấy quiz/attempt API tương ứng. | UNWIRED / NOT_FOUND |
| Runtime tests / live DB | Không chạy/không kiểm tra; ngoài phạm vi rà soát tài liệu. | NOT_RUN |

## HANDOFF

- Remaining blockers: Owner decisions liệt kê tại từng `OPEN_QUESTIONS.md`; đặc biệt answer storage/grading, eligibility ownership, result disclosure và feedback.
- Next owner/action: Sửa fingerprint API #31 tại `VERIFICATION_REPORT.md:26`; chốt/cập nhật canonical contract và schema cho các open questions trước khi chuyển DD sang approved/implementation-ready. Review này giữ nguyên DD theo phạm vi được yêu cầu.
