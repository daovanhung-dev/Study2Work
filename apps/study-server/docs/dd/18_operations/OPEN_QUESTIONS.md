# OPEN_QUESTIONS

Các câu hỏi còn lại chỉ chặn việc chốt API #18 như một generic Operation API. SH-07 notification tracking đã được triển khai và reconcile trong scope hẹp bên dưới; không dùng các câu generic còn mở để phủ nhận flow notification hiện tại.

**Current source and decision note (2026-11-21):** API #18 has a routed Shared handler and notification-only owner-bound query. For SH-07, the user selected UUID path and owner-only lookup for Student/Mentor/Admin; wrong role is 403 and missing/non-owner is 404. API #63 and #93 producers hand their accepted operation UUID to SH-07. Generic operation lifecycle/result and non-notification producer differences remain unresolved, so this API DD stays Draft overall.

## Q-18-01 — Kiểu operation_id (resolved for SH-07)

**Bằng chứng**

- Quy ước trong list_api.md khai báo operation_id và traceId là UUID.
- Reusable Operation schema khai báo id:uuid.
- The earlier catalog snapshot declared `operation_id:int64`; the current row uses UUID.
- AC-12, AC-25, AC-36 và AC-38 diagrams khai báo operation_id:uuid.

**Vấn đề**

- Historical discrepancy: the API row has since been reconciled to UUID.

**Ảnh hưởng**

- The current producer UUID can be passed directly to API #18.

**Quyết định 2026-11-21:** `RESOLVED_FOR_SH-07` — current Study source uses UUID; the catalog row, API request DD and SH-07 validate UUID before lookup.

## Q-18-02 — Authorization: owner-only hay owner/Admin (resolved for SH-07)

**Bằng chứng**

- API #18 row mô tả Bearer JWT; operation owner.
- Diagrams ghi RBAC Student|Mentor|Admin; owner only.
- The earlier Operation tracking summary implied an Admin bypass; the current row and SH-07 decision keep access owner-only.
- Current source uses the authenticated subject as the owner ID.

**Vấn đề**

- Historical ambiguity: Admin does not bypass ownership under the approved SH-07 scope.

**Ảnh hưởng**

- Current role matrix and owner query are selected for the notification-only route; generic operations still need separate review if introduced.

**Quyết định 2026-11-21:** `RESOLVED_FOR_SH-07` — allow Student/Mentor/Admin roles, with every caller restricted to their own Operation. Admin receives no bypass; owner ID is the authenticated subject.

## Q-18-03 — Study Operation storage, enums và lifecycle

**Bằng chứng**

- Study reusable Operation schema khai báo id, kind, status, owner_id, submitted_at, updated_at, optional completed_at và optional result.
- Study DB.sql, DB_UNICA_TABLES.md và DB_UNICA_ERD.drawio không định nghĩa Study Operation table.
- Current Study source has a routed API #18 handler/query/tests, but only for notification outbox operations; no generic Study `operations` table exists.
- Có một bảng operations trong Work Server schema, nhưng FK tham chiếu work_users; không có contract xác nhận dùng chung với Study.
- API #17 DD cũng ghi persistence, enum values, initial state, lifecycle và owner source là SOURCE_REQUIRED.

**Vấn đề**

- Current source supplies notification-only storage/query, statuses and owner source. Generic Study physical storage, other OperationKind/OperationStatus values, transitions, producer/worker lifecycle and retention remain unspecified.

**Ảnh hưởng**

- Only notification dispatch can be queried through current API #18. Query, result fields, terminal states and polling guarantees cannot be generalized to other operation kinds.

**Cần quyết định**

- Before adding another operation kind, provide approved Study persistence/query source, enum registry, lifecycle/state machine, owner source and retention policy; confirm explicitly if a Work Server table has a cross-service relationship.

## Q-18-04 — Operation result theo từng loại job và producer response contract (generic scope open)

**Bằng chứng**

- Reusable Operation schema khai báo optional result:Payment.
- Operation tracking section nói payments, mentor notifications, admin notifications và report export trả Operation.
- Catalog rows cho API #93 admin notification và API #103 report export lần lượt khai báo ApiEnvelope<Notification> và ApiEnvelope<Report>; điều này không khớp với Operation tracking summary.
- Catalog reusable schemas cũng có NotificationDelivery, Report, ExportAsset và OperationError, nhưng không chỉ rõ trường hợp nào nằm trong Operation.result.
- For the approved notification flow, API #93 returns the accepted operation UUID in `meta.operation_id`; AD-20 routes that UUID to API #18, whose current notification projection omits a per-kind Payment result.

**Vấn đề**

- The remaining mismatch is generic: producer response bodies and `Operation.result` do not share one schema across operation kinds. The SH-07 notification flow does not decode a generic `result`.

**Ảnh hưởng**

- Clients for future generic operation kinds cannot decode result by `kind`; this does not block the current UUID-to-notification-status handoff.

**Cần quyết định**

- Before adding generic operation kinds, define a result schema per kind and align each producer's success response with the tracking contract.

## Q-18-05 — Semantics của 403 và 404 (resolved for SH-07)

**Bằng chứng**

- API #18 declares 403 and 404; current source uses 403 for a disallowed role and 404 for missing or non-owner operations.

**Vấn đề**

- For SH-07, current behavior is resolved: disallowed role is 403; missing and non-owner notification operations both return 404.

**Ảnh hưởng**

- Generic operation kinds have no current handler branch to define; for the notification slice, role, missing and non-owner branches are resolved and tested.

**Quyết định 2026-11-21:** `RESOLVED_FOR_SH-07` — disallowed roles return 403; missing and non-owner notification operations share 404. This avoids exposing another owner's operation.
