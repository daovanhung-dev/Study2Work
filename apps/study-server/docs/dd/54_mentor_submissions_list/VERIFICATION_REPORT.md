# Verification Report — Study API #54 Lấy submissions Mentor

**Result:** VERIFIED_WITH_OPEN_QUESTIONS
**DD status:** Draft — Needs Confirmation
**Output:** 8 Markdown sheets plus PLAN_RESULT.md, OPEN_QUESTIONS.md and this report.

## Source coverage

| Source | Result |
|---|---|
| API catalog and reusable schemas | Read API #54, ApiEnvelope, Submission and UploadAsset. |
| AC-23 index and diagram | Read actor, precondition, postcondition and all diagram nodes/edges. Flow is GET list → read by Mentor permission → select one → API #55 detail → grade → feedback. |
| DB table guide and ERD | Read assignment_submissions, assignments and courses fields/relations. |
| Checked-in V1-PILOT DDL | Candidate columns read; DDL allows NULL on assignment_submissions.assignment_id/user_id and assignments.course_id. Live DB was not queried. |
| Related API #35 DD | Read Overview, Response, Data Mapping and Open Questions for Submission fields and file persistence gaps. |
| Current runtime source | Router/auth/middleware/response source inspected; no API #54 route, module or test found. Shared auth helper is Student-only. |
| Templates | All eight registered Markdown templates opened; appendix suffixes match output sheets exactly. |
| Archives | No archive source was provided or found in the scoped API/diagram/schema source set. |

## Checks

| Check | Result |
|---|---|
| Catalog method/path/query/response | PASS — GET /api/v1/mentor/submissions; course_id?:int64, status?:string, page?:int32; ApiEnvelope<Submission>. |
| Catalog status/code set | PASS — success 200 DESIGN_RESOURCE_RETRIEVED; errors 401/403/409/500 with exact catalog codes. |
| Response fields | PASS — every Submission and nested UploadAsset field is listed; unavailable file mappings remain SOURCE_REQUIRED. |
| Mutation mapping | PASS — read-only; 07_table.md marks N/A — READ-ONLY API. |
| JSON examples | PASS — two examples parse. |
| Markdown structure | PASS — exact 11-file manifest; eight front matters use dd_id 54 and Draft — Needs Confirmation; all template appendix suffixes match. |
| Relative links | PASS — all local relative links resolve. |
| Tables and fences | PASS — consistent table widths and closed code fences. |
| Whitespace | PASS — no trailing whitespace; git diff --check is clean. |
| Source implementation | PASS — static scan found no API #54 route/module/test. This does not prove runtime behavior. |
| Context validator | FAIL — Node v24 `--skip-drift` still returns `AGENT_CONTEXT_INVALID` for pre-existing missing db-admin context/source paths and broken db-admin links. This run skips source drift checks; the earlier Deno run also reported pre-existing server-study source drift. No API #54 worklog error was reported. |
| Application tests | NOT_RUN — documentation-only task; API #54 has no test module. |
| Live schema/runtime DB | NOT_VERIFIED — pilot DDL and design guide are not deployment evidence. |

## Open design decisions

- List cardinality conflicts with singular Submission response.
- Page has no size/default/range/order/count or pagination metadata.
- Submission status enum and 409 trigger are unresolved.
- Mentor identity/assigned-course authorization is not source-backed.
- UploadAsset[] cannot be mapped from the single candidate file_url.
- ERD/table guide nullability conflicts with checked-in DDL.
- API Guidelines expect data:null on errors; current helper emits {} when data is omitted/None.

## Template fingerprints

| Template file | SHA-256 |
|---|---|
| 00_Cover.md | fd5f568c5329d3069fbaff617a6f4ed3b5ffaf050e042c95b7c9100a05f79e63 |
| 01_Lich_su.md | d1cec6573433a9551812bf47552f8a44d7c533d790341941047c410e1d57771e |
| 02_Overview.md | c2879c2f0e007395558dfee4167484786c5aadb3fdd63ab135ca111e7c5f8aa6 |
| 03_Request.md | 37aaa1e9d7f3e83329e81ab38d922c9dff959284d5b7b3ae353878798dd4b7aa |
| 04_Response.md | 5bcb43ba5eb487302dd5d5efde4383b9f452f9fed2149f55315d64ff78a19ab8 |
| 05_Data_Mapping.md | 11bc77bc0522d3af27b9499114991c8819046ac32bde5c1efdc841be088dcc5b |
| 06_Error.md | e0160ea07fdbc74f2cafebd6ed3b21e60029662d28d67f5f6a0b4d95ba72be9b |
| 07_table.md | 4c9a0e037872333210aaf44ba9fbf00a0e63343a69d55250e537d2c3c5e2d356 |

## Output fingerprints

SHA-256 values are recorded for the other 10 DD files; this report is excluded to avoid a self-referential hash.

| Output file | SHA-256 |
|---|---|
| 00_Cover.md | 13ffc9d32ab2cb431eebe7fe1c9ac35b1a9302efd4420b05a99a31d6593f3566 |
| 01_Lich_su.md | b04cfb11e052c89928f382db3d09a876014a5f57a1c79266b27d5c8fe93a2247 |
| 02_Overview.md | 3312791accf3680b9e1b70743a54ddac57fad5f4f65d5c87ac401e798b35a220 |
| 03_Request.md | c39c6399cac310394f10f3ace770de7db84aec0b55b90005d767675d577c6dc8 |
| 04_Response.md | 16c061b96f932b3380bb016d42ca54931fe32a9157d6425ed71d820a91714940 |
| 05_Data_Mapping.md | afaa7149af27c323a2fc473ff30f528327b58be875287fe302088f6a93369793 |
| 06_Error.md | aa9d9030897f5cb5502856197b2dc991159651f55b92a9c378fe4ec3e75a2701 |
| 07_table.md | 57d1fc938be99f55602610da467fb4df20ba3936bd871c5748b6a305fc4a1bd9 |
| OPEN_QUESTIONS.md | ccd233bbf2fed8d12c3f9cd330d4fc50983d4c7dd334c3c45b971e4b1e142f46 |
| PLAN_RESULT.md | 31e882da636d0edfd0c75878bcaef1dfe38528f7beba69b48837ad0726eada60 |

## Boundary

No runtime code, tests, schema, API catalog, AC diagram or .agents/server-study context page was changed. AC-23 macro-review #54–#57 is complete at document level with unresolved contract questions retained below.

## Rà soát vĩ mô AC-23 #54–#57

**Kết quả:** VERIFIED_WITH_OPEN_QUESTIONS.

- Thứ tự diagram nhất quán: #54 list → #55 detail/files/rubric → #56 grade/status → #57 feedback → success.
- API #54 vẫn có mục đích lấy danh sách nhưng response catalog là một ApiEnvelope<Submission>; giữ discrepancy thay vì tự tạo response Page.
- API #55 cần đọc rubric theo diagram nhưng Submission không có field rubric; API #56 nhận rubric items nhưng chưa có schema hoặc target persistence legacy được xác nhận.
- API #56 sở hữu mutation score/status; API #57 sở hữu mutation feedback ở bước sau. Không gộp hai mutation.
- Submission.files vẫn thiếu resolver UploadAsset cho file học viên nộp. attachments của #57 là descriptor request riêng, chưa có association hoặc field response.
- courses.mentor_id chỉ là candidate direct-owner DERIVED; Mentor identity, assigned-course và quan hệ null/orphan vẫn mở.
- Helper hiện trả data {}; API Guidelines yêu cầu data null. Dynamic Mentor paths chưa nằm trong DESIGN_CONTRACT_PATHS.
- Không chạy runtime test hoặc AC-23 end-to-end.
