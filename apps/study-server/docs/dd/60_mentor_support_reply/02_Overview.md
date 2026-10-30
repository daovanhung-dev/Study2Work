---
title: "Overview"
order: 2
dd_id: "60"
api_name: "Gửi phản hồi"
source_sheet: "Overview"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | 60 |
| Module | MENTOR / TEACHING & SUPPORT |
| Method | POST |
| Endpoint | /api/v1/mentor/support/{request_id}/reply |
| Purpose | Lưu phản hồi của Mentor vào conversation của support request. |
| Consumer/Actor | Mentor |
| Authentication | Bearer JWT; shared MENTOR guard |
| Authorization | Direct course owner: courses.mentor_id bằng JWT sub; DERIVED từ API #58/#59 local fallback. |
| Request | request_id:int64; message:string; attachment refs:string. Wire key attachment_refs là DERIVED. |
| Success | HTTP 200 DESIGN_RESOURCE_UPDATED; ApiEnvelope<SupportRequest> |
| Errors | Chỉ 401, 403, 404, 422, 500 theo catalog. |
| Transaction | Lock request; insert message/link rows; reload full response; commit sau khi projection hợp lệ. DERIVED theo DB helper convention. |
| Side effects | INSERT support_messages và, nếu có file, support_message_uploads. Không upload bytes hoặc đổi request status. |
| Status | Draft — Needs Confirmation; physical schema và local wire choices chưa được business owner phê duyệt. |

## Sources

- [API catalog và reusable schemas](../../../../../docs/lists/list_api.md).
- [AC-24 flow diagram](../../diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio).
- [API #34 UploadAsset response/source](../34_uploads/04_Response.md).
- [API #47 ordered JSON asset refs/source](../47_mentor_lectures_create/03_Request.md).
- [API #58 local support schema](../58_mentor_support_requests/02_Overview.md).
- [API #59 thread projection](../59_mentor_support_request_detail/02_Overview.md).
- [API #61 resolve boundary](../61_mentor_support_resolve/02_Overview.md).
- [Checked-in support migration 008](../../../../../infra/postgres/study-server/migrations/008_support_requests.sql).
- [Current API #34 upload query](../../../../../apps/study-server/app/modules/student/api_34_uploads/query.py).
- [Current API #47 ref validator/query](../../../../../apps/study-server/app/modules/mentor/api_47_mentor_lectures_create/validate.py).
- [Current API #58 response models](../../../../../apps/study-server/app/modules/mentor/api_58_mentor_support_requests/models.py).
- [Current API #59 response/thread query](../../../../../apps/study-server/app/modules/mentor/api_59_mentor_support_request_detail/query.py).

## Source-backed local fallback

- Diagram defines logical INSERT SupportMessage and delegates status resolution to API #61; it does not define a physical table or attachment encoding.
- API #58 source/migration 008 provides BIGINT request/message/link rows; API #59 returns all messages in chronological order.
- API #34 stores numeric UploadAsset metadata. Mentor LECTURE uploads are scoped to the same course and UPLOADED status.
- API #47 currently accepts JSON arrays of ordered unique int64 asset IDs encoded as strings. API #60 uses the same representation under the DERIVED snake_case key attachment_refs; [] means no attachments.
- API #60 keeps request status unchanged, stores the original nonblank message, and returns the full rehydrated thread. No new migration is introduced.

## Remaining limits

The fallback is a checked-in local implementation basis, not live schema evidence or business-owner approval. Post-resolve reply policy, message length limits, asset URL reachability, migration deployment and production behavior remain unverified.

---
## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `Overview`
- Dimension: `A1:BA10`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `4`
- Số vùng merge: `0`

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 1 | `A1` | 【Khái quát】 |  |
| 3 | `B3` | Get thông tin…. |  |
| 5 | `A5` | 【Mục chú ý】 |  |
| 7 | `B7` | Không có |  |

</details>
