# ST-18 — Plan chi tiết

**Screen ID:** ST-18

**Tên:** Soạn và nộp bài tập

**Route trong inventory:** `/student/assignments/:assignmentId/submit`

**Actor:** Student

**Kế hoạch:** PLAN COMPLETE

**DD dự kiến:** BLOCKED bởi hợp đồng #33/#35 và các quyết định draft/upload còn mở

**Implementation/runtime:** Study Web hiện `UNWIRED`; không có route Student để xác minh.

## 1. Mục tiêu và giới hạn

- Mô tả duy nhất màn hình ST-18 trong phiên này, nối flow `ST-17 → ST-18 → ST-19` của AC-17.
- Giữ riêng trạng thái thiết kế, source/API hiện hành, test source và runtime/deployment.
- Bảo toàn `screen.png` và `code.html`; dùng PNG hiện có làm nền cho ảnh đánh dấu. HTML là unavailable fallback khác trạng thái, không dùng để dựng ảnh thay thế.
- Đánh số 60 cụm element nhìn thấy theo thứ tự đọc, dự kiến IDs `ST18-EL-01`…`ST18-EL-60`. Một marker có thể đại diện một cụm lặp có cùng vai trò (ví dụ thanh định dạng, dòng lịch sử kèm nút phục hồi hoặc một cột footer); bảng DD phải nêu rõ các thành phần nằm trong cụm.
- Author DD trung tâm phần A–F, định nghĩa từng event với input, xử lý, output, lỗi và ranh giới API. Không tự chốt field wire, giới hạn upload, chính sách retry, draft persistence hoặc trạng thái submit.

## 2. Bằng chứng và phạm vi source

### Expected behavior

- Inventory ST-18: GET #33 → gọi POST #34 cho từng file cần upload → nhận asset references → POST #35 → nhận ID submission; trạng thái `editing/uploading/submitting/failed/submitted`.
- AC-17: Student có quyền và assignment còn hạn; nhập text/chọn files; upload object; tạo submission `SUBMITTED`; sau thành công luồng tiếp tục tới đọc #36 và ST-19. AC-17 mô tả overdue/no permission bằng 403/409.
- F06 yêu cầu tách `upload succeeded` khỏi `submission succeeded`; việc giữ nội dung/draft khi lỗi vẫn là quyết định cần xác nhận cùng orphan cleanup, size, MIME và retry. Không mô tả việc giữ form như quy tắc đã duyệt.
- API #34 catalog dùng multipart `file`, `purpose`, optional `course_id`. API #35 catalog dùng path `assignment_id`, body `text:string!` và `file refs:string!`, response `ApiEnvelope<Submission>`, status 201 và lỗi 401/403/404/409/422/500.

### Current behavior cần thể hiện trong DD

- Study Web checkout hiện chỉ có docs/assets và ignored `dist` với route `/`; editable app source/package/router/Student routes vắng mặt.
- PNG 826×1600 là màn hình loaded Student form với URL GitHub/deployment, checklist, giới hạn hiển thị 50 MB, hai file mẫu, mentor/review details, draft history/autosave, Markdown editor, integrity checkbox và CTA. Các giá trị/copy là nội dung thiết kế, không phải dữ liệu runtime.
- `code.html` là Guest unavailable fallback với link về chi tiết bài tập; không có form, API, script hoặc route binding. Không coi nội dung/giá trị sample trong PNG là dữ liệu runtime.
- API #33 có catalog/DD nhưng không có route/module/test Student trong source hiện tại; DD còn câu hỏi về access, deadline, submission rule, schema/serialization và path errors.
- API #34 có route/module/provider và test source hiện tại. Handler xác thực Student/Mentor, gắn `SUBMISSION`/`LECTURE` theo role, nhận từng multipart file, chấp nhận mọi bytes/MIME, không có application size cap, Student `course_id` tùy chọn (nếu gửi thì kiểm tra enrollment ACTIVE), upload S3-compatible object trước, insert metadata `uploads` sau rồi commit; lỗi storage trả 503, lỗi DB rollback + best-effort delete + 500. DDL/migration và test source không chứng minh live DB/provider.
- API #35 chỉ có catalog/DD; không tìm thấy route/module/test. File-ref wire name/encoding, text constraints, access/deadline/409, insert-vs-update, idempotency, association schema và response fields còn mở. Response design dùng `data.id`; inventory nói nhận `submission_id`.
- Candidate `assignment_submissions` chỉ có một `file_url`, trong khi logical response là `files: UploadAsset[]`; không thấy bảng liên kết submission-upload. `uploads` là DDL/migration source, không phải live-schema proof.

## 3. Danh sách element dự kiến

| Marker range | Cụm element |
|---|---|
| 01–06 | Brand, search, nav header, notification, profile, breadcrumb |
| 07–12 | Assignment ID/draft chips, title, summary, deadline timer, policy banner, rubric badge |
| 13–20 | Section 01 heading/required badge, GitHub input/status/helper, deployment input/status/helper |
| 21–25 | Checklist heading/description và bốn dòng tự đánh giá |
| 26–37 | Attachment heading/50 MB label, dropzone, picker, format note, file count, hai file rows và preview/remove actions |
| 38–44 | Mentor card, identity, availability, review process, draft history/current entry, previous entry with restore action |
| 45–49 | Editor heading, toolbar group (bold/italic/code/lists/quote/link), text area, Markdown note, character count |
| 50–51 | Academic-integrity checkbox và statement |
| 52–55 | Save-state strip, save draft, cancel/back, submit |
| 56–60 | Footer brand/certifications, three navigation groups, copyright |

## 4. Event và luồng dữ liệu cần đặc tả

1. **ST18-EV-01 Load form:** parse `assignmentId`, require Student context per design, call candidate GET #33; map only schema-supported Assignment fields; show its catalog error envelope. Current route/API missing.
2. **ST18-EV-02 Show eligibility/deadline:** separate server decision from countdown; #33 access/deadline semantics are open, AC-17 403/409 differs from #33 catalog which has no 409.
3. **ST18-EV-03 Edit delivery URLs:** keep GitHub/deployment inputs as visible design fields; no #35 field mapping or validation/persistence contract exists.
4. **ST18-EV-04 Add/upload a file:** select/drop one file, submit multipart #34 with `purpose=SUBMISSION`; `course_id` is optional in source contract and its requirement/source is unresolved. Map #34's `data.id/name/url/content_type/size_bytes/status`; don't claim the 50 MB cap or accepted-MIME allowlist is enforced by #34.
5. **ST18-EV-05 Preview a file:** use only a returned upload URL if present; current URL is public-base-derived and has no verified per-file access policy. Preview/open behavior needs approval.
6. **ST18-EV-06 Remove a file:** distinguish a local not-yet-uploaded selection from a persisted object; no delete API/orphan lifecycle contract exists.
7. **ST18-EV-07 Edit reflection:** map editor text to API #35 `text` only as a candidate; Markdown/HTML encoding and validation are unconfirmed.
8. **ST18-EV-08 Academic-integrity consent:** checkbox is shown but no request field, storage or gating rule is in #35; document without asserting submission precondition.
9. **ST18-EV-09 Save draft:** screenshot claims server autosave and has a manual save CTA; no draft API or durable client storage contract exists.
10. **ST18-EV-10 Restore draft:** prior draft row has restore action; source, version identity and overwrite/merge behavior are undefined.
11. **ST18-EV-11 Cancel/back:** return to proposed ST-17 route only if assignmentId and navigation policy are valid; whether to preserve a draft, warn before abandoning changes or reconcile already-uploaded assets is open.
12. **ST18-EV-12 Submit:** require eligibility from approved server result; complete needed #34 uploads before #35; collect references without inventing the required wire property/format; POST #35 once, map only confirmed response, then hand the returned ID to ST-19. Form retention after validation/network failure is unresolved. Catalog 409 exists but trigger is unknown; retry/idempotency and ambiguous timeout recovery are unresolved. ST-19 #36 is a later-screen read, not silently folded into ST-18.
13. **ST18-EV-13 Global navigation:** screenshot anchors are prototype links; destinations/auth behavior are not current Study Web routes.

## 5. Blockers and discrepancy checklist

- Screenshot loaded form vs HTML unavailable fallback; actor/state differ.
- Screenshot's GitHub/deployment/checklist/draft/autosave/consent details have no source mapping in #33/#35.
- Screenshot says 50 MB and advertises PDF/DOCX/ZIP/PNG/WEBP; current #34 source has no application size/MIME restriction.
- #34 `course_id` is optional; omitting it skips Student enrollment query. The assignment/course context and client behavior are not approved.
- #34 returns an asset ID and a public URL, but #35's required `file refs:string!` has no key/encoding/cardinality contract; physical `file_url` cannot represent logical `files[]` without a schema decision.
- API #35 and Student #33/#36 are not wired; #35 response ID naming (`data.id` vs inventory `submission_id`) and state transition/idempotency are open.
- Inventory assigns GET #33 to ST-17 and ST-18 while AC-17 depicts one read before entering the submission form; cache/refetch ownership is unresolved.
- Study Web route/runtime and real database/object-storage deployment are not verified.

## 6. Verification plan

- Preserve original PNG/HTML hashes/dimensions.
- Produce ordered marker JSON and side-gutter SVG/PNG; ensure 60 IDs map exactly once to the DD table, coordinates are in bounds, labels don't overlap or cover screenshot content, then visually inspect the rendered result.
- Check DD sections A–F, sequential event IDs and complete API/error/state/navigation trace; verify local links and tracker row/counters/next pointers.
- Run `git diff --check` and a focused static artifact/whitespace audit. No tests or runtime are run under current task instructions.

## 7. Sources

- [Screen inventory and F06](../../../list_screen.md)
- [Original screenshot](./screen.png), [HTML companion](./code.html)
- [API catalog](../../../../../../docs/lists/list_api.md)
- [AC-17 diagram](../../../../../../apps/study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio)
- [API #33 open questions](../../../../../../apps/study-server/docs/dd/33_assignments_detail/OPEN_QUESTIONS.md)
- [API #34 route](../../../../../../apps/study-server/app/api/v1.py), [current view](../../../../../../apps/study-server/app/modules/student/api_34_uploads/view.py), [storage provider](../../../../../../apps/study-server/app/service/object_storage/upload.py), [test source](../../../../../../apps/study-server/tests/modules/student/api_34_uploads/test_uploads.py), [API #34 DD](../../../../../../apps/study-server/docs/dd/34_uploads/02_Overview.md)
- [API #35 open questions](../../../../../../apps/study-server/docs/dd/35_assignments_submissions/OPEN_QUESTIONS.md)
- [Candidate DDL](../../../../../../infra/postgres/study-server/DB.sql), [Study Server route inventory](../../../../../../.agents/server-study/apis/declared-routes.md)
- [Study Web design target](../../../../../../.agents/web-study/design.md)

## 8. Re-audit source/plan trước khi sửa DD và tracker (2026-11-07)

- Inventory row 32 and F06 still define `ST-17 #33 → ST-18 #34 per file → collect asset refs → #35 → ST-19 #36`; F06 explicitly separates upload success from submission success. It leaves draft-preservation, retry, orphan cleanup, and size/MIME policies to confirmation. Previous plan wording that said F06 required form retention was unsupported and is corrected above.
- AC-17's diagram reads the assignment/rule, checks eligibility, uploads with #34, creates the submission with #35, then reads #36 before showing the submitted state. The screen inventory assigns #36 to ST-19. Preserve this event-owner/order discrepancy; do not call #36 from ST-18 without an approved decision.
- API #34 catalog and `Draft — Ready for Review` DD define `POST /api/v1/uploads`, multipart `file` + `purpose` + optional `course_id`, response `ApiEnvelope<UploadAsset>` and 201/401/403/422/503/500. Current route/view/provider source and test source exist: Student+`SUBMISSION`, optional course enrollment check only when `course_id` is supplied, byte measurement, UUID object upload, metadata INSERT/commit, `UPLOADED` response; app code has no size/MIME allowlist. Tests are source evidence only and were not run. The API index's `D` marker is stale relative to the local route/module/test source; update only #034 to `R` and continue to mark runtime/deployment unverified.
- API #35 catalog/DD are design-only. Catalog requires `text:string` and `file refs:string`; its DD remains Draft with Q-35-01…08. Wire key/encoding/cardinality, text empty/length rules, deadline/access/409, insert-vs-update, idempotency, files persistence, and response-ID naming remain open. Logical `Submission.files[]` conflicts with candidate `assignment_submissions.file_url`; no association table is present in the reviewed candidate. API #33/#35/#36 Student route/module/test searches return no matches; only Mentor submission routes are present.
- Upload DDL/migration 004 and legacy `assignments`/`assignment_submissions` candidates use BIGINT artifacts. V1-PILOT `infra/postgres/02_study_db.sql` has no business `uploads`, `assignments`, or `assignment_submissions` table; `service_role_assignments` is unrelated. No live database, migration deployment, or real object-storage access was checked.
- Study Web remains `UNWIRED`: `src/`, package manifest and Student route are absent; the only file in ignored `dist/` is `index.html`. The raw PNG is a loaded Student submission form; the HTML is a Guest/unavailable fallback with a hash link `#/student/assignments/detail`, no form, API request or screen-specific interaction code, plus remote Google fonts, Tailwind CDN/config script and a 1440px max width. This differs in actor/state and route from inventory and does not meet the Study Web guide's no-remote-font target; do not treat either artifact as runtime.
- Raw source baseline rechecked: `screen.png` 826×1600, SHA-256 `be8b06a7f90dc5febab40aab9e50b3e3a81740fc599f26958c5d0fd433d5e940`; `code.html` 8,726 bytes, SHA-256 `8c0a81d5fbd1b2907bd9fe8d8b358ab3c8026f1200519ae44f12cd5a8299491c`. Existing marker map/overlay was verified against 60 DD rows, SVG labels/transforms, coordinates and screenshot layout; source assets remain unchanged.
- Edits after this re-audit: corrected F06/draft-retention wording across ST-18 DD and plan; clarified API #34 source behavior and HTML/route/design mismatch; updated ST-18 inventory/global-tracker blocker details and the directly related F06/API #034 index status; created this session's worklog. No other Screen ID, API DD, code or schema was edited.

## 9. Post-edit static audit (2026-11-07)

- Artifact audit: `screen.png` remains 826×1600 and `code.html` remains 8,726 bytes with the hashes above; annotated PNG is 2036×3200. The raw and annotated images were reviewed; marker badges sit in side gutters.
- Mapping audit: 60 sequential unique JSON markers = 60 ordered DD element rows = 60 SVG groups; IDs, SVG badge transforms and JSON coordinates match; targets are unique/in bounds; badge centers are unique, in the side gutters and at least 25px apart. DD includes A–F and 13 sequential events with valid element event references.
- Link/coverage audit: all 19 DD and 15 plan local Markdown links resolve. The acceptance checklist has 9 checked documentation/static items and one unchecked cross-screen agreement item pending the open API/cache/ID decisions.
- Inventory audit: 83 unique screen IDs match 83 folders; 82/83 six-artifact bundles are complete (only ST-01 is incomplete); ST-18 has all six artifacts.
- Scoped `git diff --check` and authored-file whitespace checks pass. `node scripts/validate-agent-context.mjs` exits 1 with `AGENT_CONTEXT_INVALID` due missing db-admin context/source roots and stale scope manifests for server-study/server-work/web-work/web-work/work-web/mobile-work/db-admin; validator output has no ST-18 reference.
- No application tests, Study Web runtime, live DB, migration deployment or real object-storage check was run. Status remains `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`. ST-19 is next in a separate session.
