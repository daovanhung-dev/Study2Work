# Verification Report — API #81 Từ chối nội dung

## Scope

- DD output: apps/study-server/docs/dd/81_admin_content_reject/.
- Task: Markdown DD and connected AC-33 review; no runtime/schema/catalog/diagram changes.
- DD status: Draft — Needs Confirmation.
- Application tests: NOT_RUN; API #81 has no route.

## Static checks

| Check | Result | Status |
|---|---|---|
| Expected package | Exact 11 Markdown files: eight template sheets and three standard reports | PASS |
| Template appendix parity | 8/8 compared byte-for-byte with registered template suffixes | PASS |
| Catalog contract | Request, Content response, success and error codes match row #81 | PASS |
| Response coverage | Eight reusable Content fields represented; no reason field added | PASS |
| JSON examples | 4/4 JSON blocks parsed | PASS |
| Relative links/anchors | 41 local links resolve | PASS |
| Markdown tables/fences | 37 tables have consistent column counts; 5 fenced blocks are balanced | PASS |
| Whitespace | Final newline on all files; no trailing whitespace | PASS |
| Inventory | 81 DD folders / 22 missing; 69 full packages; 12 route/view pairs / 91 without pair | PASS — STATIC |
| AC-33 macro-review | #78–#81 document review completed; unresolved questions remain explicitly listed below | REVIEWED_WITH_OPEN_QUESTIONS |

## Fingerprints

| Fingerprint | Scope | SHA-256 |
|---|---|---|
| Registered template pack | Eight sorted template sheet names + NUL + raw bytes + NUL | `3dc7fd2242dd1ed1bd9faba50aadad913a31b97ebf1392d6144bb905c5208137` |
| DD output payload | Eight sheets, `OPEN_QUESTIONS.md`, and `PLAN_RESULT.md`; verification report excluded | `40f1b96aa33c6d298a64861e77452cd8e7ae533f1176a5279180c17eb5c8e5de` |

## Findings and limits

- AC-33 directly gives the logical rejection effect REJECTED plus review reason.
- Physical Content/reason persistence and parity of audit writes with #80 remain open.
- Cross-DD anchor links in #78–#80 were corrected during the group review and checked against their Data Mapping headings.
- Current source has no API #81 route/module/test. Static DD checks do not prove Admin authorization, live schema, database writes or runtime behavior.

## AC-33 macro-review #78–#81

Kết luận: review liên kết tài liệu đã hoàn tất; không có contract, schema hay source nào được sửa để tự giải quyết điểm chưa có bằng chứng. Một số liên kết tới các bước Data Mapping trong #78–#80 được sửa để trỏ đúng heading; toàn bộ local link/anchor trong nhóm #78–#81 hiện resolve.

| Area | Cross-DD finding | Status |
|---|---|---|
| Queue and reload (#78) | Queue dùng predicate `status=PENDING_REVIEW`, còn catalog trả `Content` đơn dù tên/`page` gợi ý danh sách. Nếu đúng cùng row được chuyển sang `REJECTED`, row đó không còn khớp predicate khi tải lại; revision identity chưa chứng minh hai thao tác nhắm cùng row. | DISCREPANCY / SOURCE_REQUIRED |
| Detail projection (#79) | AC-33 yêu cầu đọc `content/version/author`, nhưng reusable `Content` chỉ có tám field và không chứa version/author. Không tự thêm field response. | DISCREPANCY |
| Approval/rejection states (#80/#81) | #80 ghi `APPROVED/PUBLISHED` và audit; API #52 quản lý publish riêng. #81 ghi `REJECTED` cùng review reason nhưng không nêu audit append. Casing/ý nghĩa trạng thái và audit parity chưa được chốt. | SOURCE_REQUIRED |
| Revision identity (#78–#81) | Các catalog request chỉ truyền `content_id`; không có revision ID/expected row version. Stale decision, locking và conflict error chưa được định nghĩa. | SOURCE_REQUIRED |
| Authorization and storage | Catalog yêu cầu Admin, nhưng current Study source chưa có Admin route/guard. Legacy DDL không có generic Content/review relation; pilot decision log dùng UUID revision identity, không map trực tiếp sang Content int64. | UNWIRED / SOURCE_REQUIRED |
| Delete/lifecycle (#52/#53) | Publish/delete là API riêng. Quy tắc cho rejected content, soft delete và queue filtering chưa được nối với AC-33. | SOURCE_REQUIRED |

Application tests remain `NOT_RUN`; this review checks document consistency only.
