# ST-15_PLAN — Xác nhận nộp bài kiểm tra

> Trạng thái: PLAN COMPLETE; DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED

## 1. Phạm vi và phân loại

- Phiên này chỉ xử lý **ST-15 — Xác nhận nộp bài kiểm tra**; không bắt đầu Screen ID khác.
- `primary_task_type: docs`; `secondary_task_types: []`; `project_scopes: [web-work, server-study]`.
- Cross-scope dependencies: ST-14 → ST-15 pending answer flush; API #30 → #31 submit; AC-16 grading branches; G-09; ST-16/#32 result handoff.
- Inventory: Student confirmation dialog; route `/student/attempts/:attemptId/submit`; APIs #30/#31; previous ST-14; next ST-16. Inventory requires flushing pending #30 updates before one #31 request, handling double-submit/409, and showing unanswered count; states `confirm/submitting/submitted/ambiguous-network`.
- F05 flow places `#30 save answer → ST-15 #31 submit after flush → ST-16 #32 result`. G-09 blocks answer versioning/autosave, submit idempotency and deadline/time policy.
- API #31 DD is Draft — Needs Confirmation; it is an API design artifact, not implementation/runtime evidence. UI-only DD has no registered canonical skill: the machine manifest excludes `web-ui-only-dd` from `createDD-markdown`.

## 2. Asset baseline and current visual state

- `screen.png` source is 1600×1280 RGB, SHA-256 `40d47787f58e9f962237ef41f4fbc58f8d2600d38f51f061cdffefb8a6d4aedc`.
- `code.html` is 12,313 bytes, SHA-256 `6debc6c68e6d046106e377876f34bb68ed3682480118903989ed32318f0d7976`.
- PNG shows a confirmation overlay over a blurred quiz: 18/20 answered, 2 unanswered (Q19/Q20), one flagged (Q15), 12:15 remaining, “synced 18/20”, rules/attempt text, Continue and Submit Now. Header stays visible with exit, brand, a separate 45:20 countdown and profile.
- HTML is a different unavailable/error state over a blurred sample question 18/20. It says valid work is not recorded and cannot be submitted, with only “Quay lại kiểm tra”. Its script looks for absent `btn-submit-exam`; the dormant branch would disable it and route after 600ms to hardcoded `#/student/attempts/att-react-02/result`. Present `btn-cancel-dialog` calls `window.history.back()`. No API or request is made.
- Preserve both originals; do not treat static DOM/JS as a current router or submit handler. Do not treat PNG examples as live count/time/attempt/policy data.

## 3. Contract expectation and limits

- API #30: `PUT /api/v1/attempts/{attempt_id}/answers`, Student Bearer, `question_id:int64!` plus ambiguous catalog notation `answer(s):string!`, success 200 `DESIGN_RESOURCE_UPDATED`, errors 401/403/404/422/500. The catalog has no 409. Payload, answer representation, pending queue ordering, version/idempotency, retry and outcome reconciliation remain open.
- API #31: `POST /api/v1/attempts/{attempt_id}/submit`, Student Bearer, `attempt_id:int64!`, no body/query, response `ApiEnvelope<QuizAttempt>`; success 200 `DESIGN_RESOURCE_UPDATED`; errors 401/403/404/422/409/500 with catalog business codes. No current Student route/module/test exists.
- AC-16: after submit, attempt becomes `SUBMITTED`; automatic grading follows. If any question requires manual grading, result state is `PENDING_GRADE`; otherwise `GRADED`. #32 reads permitted results. Grading formula/question-type detection, owner/state/expiry predicates, repeat-submit behavior, locking/transaction/rollback, timestamp and response disclosure are unresolved in API #31 Q-31-01..06.
- The displayed instant grading/skill chart, `2/3` attempt number, “1 attempt remaining”, answer counts, “synced 18/20” and countdowns have no authoritative #31 response/data mapping. Manual grading can remain pending. ST-14 image has a different progress snapshot; no contract guarantees summary transfer to this route.
- Current Study Web source has docs/assets plus ignored root-only `dist`; no editable app/router. Study Server route/module/test scan finds no Student #31 implementation. Candidate DB writes do not prove live schema or transaction.

## 4. Kế hoạch element/marker

Tạo marker tuần tự `#1–#18`, một-một với element IDs `ST15-EL-01`…`ST15-EL-18` trong bảng C của `ST-15.md`. Marker nằm trong margin/whitespace ngoài text/control; không che copy hoặc số liệu.

1. Header exit; 2. brand; 3. header countdown; 4. profile.
5. dialog backdrop; 6. dialog surface; 7. quiz icon tile; 8. eyebrow/confirmation label; 9. title; 10. explanatory paragraph.
11. answered/progress card; 12. unanswered card/question chips; 13. flagged card/question chip.
14. remaining-time strip; 15. synced-answer status chip; 16. exam rules/attempt-history card.
17. Continue test action; 18. Submit now action.

Background quiz is intentionally blurred in the image; annotate it as one backdrop group, not as independent hidden screen controls. The sample question/status grid and HTML fallback are documented in the discrepancy section, not marked as visible foreground controls.

## 5. Sự kiện và luồng cần đặc tả

1. **ST15-EV-01 — Open confirmation route:** read `attemptId` from URL and require Student access; inventory has no attempt-read endpoint. Counts/dirty queue must come from the ST-14 in-memory handoff, but the handoff contract is missing. Do not invent a GET or reconstruct data from the modal sample.
2. **ST15-EV-02 — Continue the attempt:** “Tiếp tục kiểm tra” dismisses confirmation and returns to ST-14 for the same `attemptId`, matching modal purpose and inventory link. No API. Exact route/history/dirty-state restoration and dialog close mechanics remain unverified.
3. **ST15-EV-03 — Confirm submit:** on explicit “Nộp bài ngay”, read `attemptId` and pending #30 status; block duplicate in-flight local clicks. Await all pending answer writes per inventory; do not call #31 until every required #30 operation has confirmed success. Exact queue/replay/body semantics are blocked by API #30/G-09. Then send exactly one #31 POST with Bearer and path only; no body/query or client counts/answers. Do not automatically retry #31 after a lost response.
4. **ST15-EV-04 — Interpret #31 response:** 200 `DESIGN_RESOURCE_UPDATED` means the API accepted the update under the design contract; use `ApiEnvelope<QuizAttempt>` only after response schema/runtime exists. AC-16 branches `PENDING_GRADE` vs `GRADED`; do not promise immediate score/skill chart. Navigate to ST-16 only after an accepted response. Response projection, status values and 200-vs-409 reconciliation are unresolved.
5. **ST15-EV-05 — Submit/API failures:** retain 401/403/404/422/409/500 business codes; no catalog-specific messages/field errors or recovery UI are defined. A failed pending #30 flush must not fall through to #31. For timeout after #31, enter `ambiguous-network`; do not treat as success or replay until owner defines reconciliation/idempotency.
6. **ST15-EV-06 — Time/summary state while dialog is open:** no client timer may submit or expire the attempt. Header 45:20 and modal 12:15 disagree; `saved 18/20` and attempt counts have no source. Do not recompute/lock based on these sample values.
7. **ST15-EV-07 — Exit/profile/backdrop interaction:** header exit and profile are visible but destinations are not in this screen contract. Modal backdrop click/escape/focus behavior is not specified by assets; preserve as UI/accessibility decisions. Study Web target requires semantic controls, visible focus and keyboard operation; do not infer current behavior.

## 6. Trạng thái, blocker và đầu ra

- Model `opening → confirm → flushing_answers → submitting → submitted → ST-16`; alternate `continue → ST-14`, `flush_error`, API error states, `ambiguous_network` and `conflict`. `submitted` only follows #31 success; do not infer it from button click or the HTML sample.
- No #31 retry/dedup or automatic redirect from 409/timeout until API owner defines whether to reconcile via #32 or another approved flow. No score/correct answer is shown in ST-15.
- Create `ST-15_markers.json`, `ST-15_markers_overlay.svg`, `screen_annotated.png` using the shared renderer at scale 2, and `ST-15.md` with A–F, 18 element specs, event inputs/ordered steps/API/error/output, state/navigation, security and acceptance checklist.
- Record blockers: #30 flush ordering/idempotency/schema; #31 ownership/state/repeat/expiry/grading/transaction/response; route state/data handoff; sample timers/counts/attempt policy; screenshot/HTML mismatch; Study Web and Student API #31 unavailability.
- Static audit only: source hashes/dimensions, marker order/bounds/map, annotated image ratio, SVG/JSON validity, local links, tracker count/pointer, whitespace and `git diff --check`. No tests or runtime.

## 7. Nguồn truy vết

- [Screen inventory, F05, G-09](../../../list_screen.md)
- [PNG source](./screen.png), [HTML companion](./code.html)
- [ST-14 attempt-screen handoff](../ST-14_lam-bai-kiem-tra/ST-14.md)
- [API catalog #30–#32](../../../../../../docs/lists/list_api.md)
- API #31 DD: [overview](../../../../../../apps/study-server/docs/dd/31_attempts_submit/02_Overview.md), [request](../../../../../../apps/study-server/docs/dd/31_attempts_submit/03_Request.md), [response](../../../../../../apps/study-server/docs/dd/31_attempts_submit/04_Response.md), [mapping](../../../../../../apps/study-server/docs/dd/31_attempts_submit/05_Data_Mapping.md), [errors](../../../../../../apps/study-server/docs/dd/31_attempts_submit/06_Error.md), [open questions](../../../../../../apps/study-server/docs/dd/31_attempts_submit/OPEN_QUESTIONS.md)
- [API #30 open questions](../../../../../../apps/study-server/docs/dd/30_attempts_answers/OPEN_QUESTIONS.md)
- [AC-16 index](../../../../../../apps/study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md), [AC-16 diagram](../../../../../../apps/study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio)
- [Attempt/answer table design](../../../../../../apps/study-server/docs/diagrams/DB_UNICA_TABLES.md), [candidate DDL](../../../../../../infra/postgres/study-server/DB.sql)
- [Study route inventory](../../../../../../.agents/server-study/apis/declared-routes.md), [current API router](../../../../../../apps/study-server/app/api/v1.py), [Study Web status](../../../../../../.agents/web-work/study/INDEX.md), [UI design target](../../../../../../.agents/web-study/design.md)

## 8. Re-audit trước khi sửa DD/tracker (2026-11-07)

### Kết quả đối chiếu nguồn hiện hành

- `apps/study-client/docs/list_screen.md` giữ route ST-15 và yêu cầu flush #30 đang pending trước một lần POST #31, double-submit/409 handling và số câu chưa làm. F05 đặt #28 → eligibility → #29 → #30 → #31 → #32; xung đột owner/handoff #29 giữa ST-13/ST-14 vẫn là dependency upstream, không giải quyết trong màn hình này. G-09 vẫn mở answer versioning/autosave, submit idempotency và deadline/time policy.
- Catalog #30–#32 xác nhận #30 là PUT, success 200 và không có 409; #31 là POST không body/query với success 200 và errors gồm 409; #32 là GET result thuộc ST-16. AC-16 XML page `AC16` xác nhận submit cập nhật Attempt thành `SUBMITTED`, tự chấm và rẽ sang `PENDING_GRADE` nếu còn câu cần chấm tay, nếu không `GRADED`, rồi gọi #32. API #31 DD còn Draft — Needs Confirmation, Q-31-01…06 tiếp tục mở ownership, state/repeat/expiry/concurrency, grading, transaction, response/disclosure và mapping.
- API #30/#31/#32 không được tìm thấy trong `apps/study-server/app/api/v1.py`, `.agents/server-study/apis/declared-routes.md`, hoặc Student modules/tests; thư mục Student hiện chỉ có API #34 uploads. `apps/study-client/` không có editable Student app/router hoặc package manifest; Study Web vẫn `UNWIRED`. Đây là source/route absence, không phải kết luận về deployment/live service.
- Schema candidates khác lifecycle: `infra/postgres/study-server/DB.sql` dùng BIGSERIAL/BIGINT `quiz_attempts`/`quiz_answers`, trạng thái mặc định `IN_PROGRESS`, answer có một `choice_id` và `is_correct NOT NULL`; `infra/postgres/02_study_db.sql` là V1-PILOT UUID `assessment_attempts` với `submitted_payload_snapshot` bắt buộc khi chèn và `assessment_answers` immutable, trạng thái/passing branches theo `SUBMITTED→PASSED|FAILED` hoặc review flow. Không có mapping được duyệt từ #30 autosave/#31 AC-16 sang V1-PILOT và không xác minh live schema.
- Asset baseline được xác nhận lại: `screen.png` 1600×1280 SHA-256 `40d47787f58e9f962237ef41f4fbc58f8d2600d38f51f061cdffefb8a6d4aedc`; `code.html` SHA-256 `6debc6c68e6d046106e377876f34bb68ed3682480118903989ed32318f0d7976`; annotated PNG 3200×2560. PNG là confirmation mockup, còn HTML là unavailable fallback; DOM thiếu `btn-submit-exam`, script có hardcoded hash route, không có API request. Không thay đổi asset nguồn.
- Static audit hiện tại: JSON/SVG hợp lệ; 18 marker tuần tự, trong bounds; 18 DD element rows và 18 SVG groups/labels khớp một-một, tọa độ JSON/SVG trùng; annotated PNG đúng 2×; 22 link trong DD và 20 link trong plan đều resolve. Raw và annotated PNG đã được xem lại.
- DD element table đang gán nhầm event cho hai action: #17 Continue trỏ EV-03 thay vì EV-02; #18 Submit trỏ EV-04/EV-05 thay vì event submit EV-03. Đây là lỗi traceability cục bộ; không đổi marker/ảnh.

### Thay đổi đã lên kế hoạch trước khi sửa DD/tracker

- Sửa mapping event ở element #17/#18; giữ EV-04 là response success và EV-05 là failure/recovery. Nêu rõ discrepancy legacy BIGINT với V1-PILOT UUID/lifecycle trong DD và blocker.
- Đánh dấu các mục static/traceability checklist đã audit; không đổi nội dung mẫu/asset và không biến các design candidates thành source-backed behavior.
- Cập nhật ST-15 inventory gate/status và F05 dependency note nếu cần, cập nhật ST-15 row/checkpoint trong `dd_screens/PLAN.md`, rồi hoàn tất worklog.
- Chỉ chạy static checks và `git diff --check`; không chạy application tests, browser/runtime hoặc live DB checks. Kết quả dự kiến vẫn `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED` do các contract/handoff blockers nêu trên.
