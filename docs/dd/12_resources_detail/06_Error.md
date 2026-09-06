---
title: "Error"
order: 6
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "4.Error"
format: markdown
---

# Error

## Giải thích

Các trường hợp lỗi của API #12 theo contract API V1. Contract hiện chỉ khai báo `404 DESIGN_RESOURCE_NOT_FOUND` và `500 DESIGN_INTERNAL_ERROR`; không tự thêm `403` hoặc `503` dù diagram có access/storage branch chưa được khóa.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---:|---|
| 1 | Not found | `Yes` | `resource_id` | Path không parse được `int64`, hoặc Q1 không có `resources.id = resource_id` | `404` | `DESIGN_RESOURCE_NOT_FOUND` | `N/A — envelope message` | [`2.1`](./05_Data_Mapping.md#21-validate-resource_id) / [`3.2`](./05_Data_Mapping.md#32-check-resource-result) / [`6.2`](./05_Data_Mapping.md#62-not-found-response) | `No` | Không expose resource ID ngoài contract. |
| 2 | Not found | `Yes` | `parent course` | Q2 không có lesson/course liên kết hoặc parent course không ở trạng thái `PUBLISHED` theo derived public gate | `404` | `DESIGN_RESOURCE_NOT_FOUND` | `N/A — envelope message` | [`3.4`](./05_Data_Mapping.md#34-check-parent-result) / [`6.2`](./05_Data_Mapping.md#62-not-found-response) | `No` | Publication gate cần xác nhận trước implementation. |
| 3 | System error | `No` | `resources/lessons/courses` | Lỗi Q1/Q2, JOIN, duplicate primary-key result, hoặc lỗi map Resource/envelope | `500` | `DESIGN_INTERNAL_ERROR` | `N/A — envelope message` | [`3.2`](./05_Data_Mapping.md#32-check-resource-result) / [`6.3`](./05_Data_Mapping.md#63-system-error-response) | `No` | Không trả raw SQL hoặc stack trace. |
| 4 | System error | `No` | `Object Storage signer` | Storage signer lỗi hoặc không thể tạo URL trong private branch | `500` | `DESIGN_INTERNAL_ERROR` | `N/A — envelope message` | [`4.2`](./05_Data_Mapping.md#42-private-resource-object-storage-signer) / [`6.3`](./05_Data_Mapping.md#63-system-error-response) | `No` | API #12 chưa khai báo `503`; dependency failure tạm quy về `500`. |

> Diagram AC-06 mô tả nhánh `403` khi access denied, nhưng `list_api.md` khai báo API #12 là public và không có `403`. Đây là `DISCREPANCY`; cần cập nhật contract trước khi thêm error response 403.
>
> Mỗi error case và mỗi field validation nằm trên một row riêng.

---
## Phụ lục đối chiếu template Markdown

- Template: `../../../.agents/skills/create_dd/docs/dd/DD_API_Template_MD/06_Error.md`.
- Sheet logic: `4.Error`.
