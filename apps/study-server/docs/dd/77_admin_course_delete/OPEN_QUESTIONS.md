# Câu hỏi còn mở — API #77

Trạng thái tài liệu: `Draft — Needs Confirmation`. API đã được wire theo fallback `DERIVED`; policy owner, live schema và linked lifecycle behavior vẫn chưa được xác nhận.

1. **Dependency policy:** Runtime blocks any enrollment row, active generic Content row, lesson, quiz or assignment. Is this complete, and should completed/inactive records also block? Current set is DERIVED.
2. **Content coverage:** Legacy DDL/API sources also include other course-linked relations; owner should confirm whether the selected learning-content set is sufficient. No child rows are mutated.
3. **Soft-delete representation:** Runtime uses `courses.status='DELETED'` and maps DB-returned `updated_at` to `DeleteResult.deleted_at`, following API #72. Confirm this marker/timestamp mapping for the target environment.
4. **Schema/live DB:** Runtime targets the checked-in legacy BIGINT candidate. Live schema, migration state, grants and FK metadata are not verified; V1-PILOT UUID/`archived_at` remains separate.
5. **Admin authorization:** Shared JWT role `ADMIN` is enforced; does deployment require a separate course-management permission or scope check?
6. **Visibility/restore:** #73/#74 can expose the `DELETED` status; #75 can still update metadata and #76 can replace the status. Confirm whether deleted courses should remain visible or become immutable, and whether #76 is an allowed restore path.
7. **Other course writers:** Mentor APIs #47/#50 and other course-linked operations were not changed in this one-API task. Confirm their behavior when course status is `DELETED`.
8. **Repeated DELETE:** Runtime returns 404 for a missing/already-`DELETED` course. Confirm whether retries should instead be idempotent.
9. **Audit boundary:** #77 does not write the #76 audit relation because AC-32 assigns audit to status updates only. Confirm if delete auditing is separately required.

## Ranh giới proposal

- Runtime uses the selected 422 blocker fallback and `status='DELETED'`; both remain `DERIVED` and require owner confirmation.
- `DeleteResult.status="deleted"` and its three fields are direct contract; `deleted_at <- updated_at` is DERIVED.
- No hard delete, cascade, child mutation, audit, Idempotency-Key, new business code or response field is added.

## Rà nhóm AC-32 #73–#77

Đã rà runtime/DD boundary: #73 list, #74 detail, #75 metadata-only update, #76 status + audit, #77 soft-delete. #73/#74 hiện có thể hiển thị `DELETED`; #76 có thể thay trạng thái marker. Category/counter/response wrapper và permission riêng là gaps khác trong AC-32; không đổi chúng trong API #77 task. Chi tiết ở `VERIFICATION_REPORT.md`.
