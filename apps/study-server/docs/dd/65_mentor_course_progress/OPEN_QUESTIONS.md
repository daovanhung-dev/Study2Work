# Open Questions — Study API #65

Status: Draft — Needs Confirmation. API #65 có local implementation theo các fallback bên dưới. Các quyết định này chưa thay catalog contract hoặc phê duyệt business policy.

1. **Owner approval for response:** Runtime returns `Page<MentorStudentProgress>` because `Page<Course>` has no progress fields; catalog still declares `Page<Course>`. Confirm/update the catalog and API owner contract before treating runtime shape as canonical.
2. **Pagination bound:** Request has no page/size. Local fallback returns the complete roster in one page; define a bounded pagination contract before using this route for large courses.
3. **Course access:** Local code maps JWT numeric `sub` to `courses.mentor_id`, allows direct owners only, checks 404 for absent and 403 for other-owner. Confirm whether assigned Mentors or privacy-hiding 404 are required.
4. **Enrollment eligibility:** Local code includes `ACTIVE` enrollments and `STUDENT` users, collapsing duplicate enrollment rows by user ID. Confirm withdrawn/deleted-user policy if represented by the deployed schema.
5. **Lesson/progress rules:** Local code uses PUBLISHED lessons, latest duplicate progress row by timestamp then ID, COMPLETED count, floor average, missing/NULL percent as zero, zero when denominator is empty; invalid status/range yields 500. Confirm these business rules and status enum.
6. **Live schema/freshness:** Checked-in legacy BIGINT DDL is the implementation candidate; live schema metadata and data freshness/snapshot guarantees were not inspected. Confirm deployed schema and acceptable freshness.
7. **AC-26 group consistency:** #66 event analytics and #67 selected-Student details remain separate and unwired. Their contracts and source rules still need owner review; do not infer event analytics from progress data.

Các local choices trên được áp dụng theo chỉ thị người dùng “tự xử lý hợp lý”; chúng vẫn là DERIVED và không thay thế phê duyệt. Contract catalog direct vẫn là Page<Course> cho tới khi owner phê duyệt thay đổi.

## Macro-review AC-26 after DD #67

- Status: `VERIFIED_WITH_OPEN_QUESTIONS`; see [API #67 verification report](../67_mentor_student_progress/VERIFICATION_REPORT.md).
- #65 stays class-level roster summary; #66 stays course-wide event analytics; #67 is selected-Student lesson progress detail. The diagram sequence is UI orchestration, not server-to-server coupling.
- #65 and #67 proposals share PUBLISHED lesson denominator and floor-average formula. #66 event-active Student count is distinct from #65 enrollment count; progress state/time fields are not event source.
- Open: #65 `Page<Course>` mismatch and missing page/size inputs; owner approval for its DERIVED response, access/eligibility and progress rules, plus live schema/freshness. #66 event-source semantics and #67 selected-Student source/eligibility remain unverified. The #65 local helper error data is null and its middleware path is wired/tested.

