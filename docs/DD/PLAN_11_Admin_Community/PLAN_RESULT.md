# Kết quả Plan 11 — Admin Community

- Phạm vi: API 075–082.
- Hoàn thành workbook: 8/8.
- Trạng thái: Draft; API suy dẫn cần xác nhận.
- Naming contract: camelCase cho JSON/query; path placeholder giữ nguyên catalog; DB dùng snake_case.
- Lưu ý nguồn: bundle hiện tại thiếu System Architecture, Study Architecture, schema seed SQL và API catalog CSV được plan viện dẫn.

| API | Method | Endpoint | Basis | Status | Workbook | DB ghi |
|---:|---|---|---|---|---|---|
| 075 | GET | `/api/v1/admin/community-groups` | SUY DẪN | Draft — Needs Confirmation | `API_075_GET_admin_community_groups.xlsx` | Không |
| 076 | POST | `/api/v1/admin/community-groups` | SUY DẪN | Draft — Needs Confirmation | `API_076_POST_admin_community_groups.xlsx` | community_groups, audit_logs |
| 077 | GET | `/api/v1/admin/community-groups/{group_id}` | SUY DẪN | Draft — Needs Confirmation | `API_077_GET_admin_community_groups_by_group_id.xlsx` | Không |
| 078 | PATCH | `/api/v1/admin/community-groups/{group_id}` | TRỰC TIẾP | Draft | `API_078_PATCH_admin_community_groups_by_group_id.xlsx` | community_groups, audit_logs |
| 079 | PUT | `/api/v1/admin/community-groups/{group_id}/status` | SUY DẪN | Draft — Needs Confirmation | `API_079_PUT_admin_community_groups_by_group_id_status.xlsx` | community_groups, audit_logs, outbox_events |
| 080 | PUT | `/api/v1/admin/community-groups/{group_id}/moderators` | SUY DẪN | Draft — Needs Confirmation | `API_080_PUT_admin_community_groups_by_group_id_moderators.xlsx` | community_groups, audit_logs |
| 081 | GET | `/api/v1/admin/community-reports` | SUY DẪN | Draft — Needs Confirmation | `API_081_GET_admin_community_reports.xlsx` | Không |
| 082 | PATCH | `/api/v1/admin/community-reports/{report_id}` | SUY DẪN | Draft — Needs Confirmation | `API_082_PATCH_admin_community_reports_by_report_id.xlsx` | community_reports, audit_logs |

## Reviewer notes

- Đối chiếu endpoint/contract suy dẫn với PO/BA trước khi đổi trạng thái Final.
- Đối chiếu logical table/column với schema seed SQL khi được cung cấp.
