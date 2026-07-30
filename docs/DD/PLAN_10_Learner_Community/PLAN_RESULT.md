# Kết quả Plan 10 — Learner Community

- Phạm vi: API 070–074.
- Hoàn thành workbook: 5/5.
- Trạng thái: Draft; API suy dẫn cần xác nhận.
- Naming contract: camelCase cho JSON/query; path placeholder giữ nguyên catalog; DB dùng snake_case.
- Lưu ý nguồn: bundle hiện tại thiếu System Architecture, Study Architecture, schema seed SQL và API catalog CSV được plan viện dẫn.

| API | Method | Endpoint | Basis | Status | Workbook | DB ghi |
|---:|---|---|---|---|---|---|
| 070 | GET | `/api/v1/community-groups` | TRỰC TIẾP | Draft | `API_070_GET_community_groups.xlsx` | Không |
| 071 | GET | `/api/v1/community-groups/{group_id}` | SUY DẪN | Draft — Needs Confirmation | `API_071_GET_community_groups_by_group_id.xlsx` | Không |
| 072 | POST | `/api/v1/community-groups/{group_id}/open-link` | TRỰC TIẾP | Draft | `API_072_POST_community_groups_by_group_id_open_link.xlsx` | community_join_events, audit_logs |
| 073 | POST | `/api/v1/community-groups/{group_id}/reports` | TRỰC TIẾP | Draft | `API_073_POST_community_groups_by_group_id_reports.xlsx` | community_reports, audit_logs |
| 074 | GET | `/api/v1/me/community-reports` | SUY DẪN | Draft — Needs Confirmation | `API_074_GET_me_community_reports.xlsx` | Không |

## Reviewer notes

- Đối chiếu endpoint/contract suy dẫn với PO/BA trước khi đổi trạng thái Final.
- Đối chiếu logical table/column với schema seed SQL khi được cung cấp.
