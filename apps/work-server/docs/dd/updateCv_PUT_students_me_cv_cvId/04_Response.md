---
title: "Response"
order: 4
dd_id: "updateCv"
api_name: "Update CV"
source_sheet: "2.Response"
status: "Draft — Needs Confirmation"
---
# Response

## Format

| Format | Character encoding | Content-Type |
|---|---|---|
| JSON | UTF-8 | application/json |

## Response fields

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | success | Success flag | `success` | boolean | No | N/A | N/A | reply | `status < 400` | Always present | Envelope field |
| 2 | businessCode | Business code | `businessCode` | string | No | N/A | N/A | reply | Fixed by branch | Always present | Source-confirmed code |
| 3 | message | Message | `message` | string | No | N/A | N/A | reply | Fixed by branch | Always present | Vietnamese source message |
| 4 | data | Payload | `data` | object\|array\|null | Yes | Route/service result | N/A | reply | `jsonSafe` on success; null on errors | null on errors | See data-specific rows |
| 5 | meta | Metadata | `meta` | object | No | N/A | N/A | reply | Pagination metadata where applicable | {} if none |  |
| 6 | traceId | Trace ID | `traceId` | string | No | N/A | N/A | reply/traceId | Header value or generated UUID | Always present | Also returned as X-Trace-Id header |
| 7 | data.id | id | `id` | number | Yes | Cv | id | query/mutation result | BigInt → JSON number | N/A | Full Prisma result |
| 8 | data.avt | avt | `avt` | string\|null | Yes | Cv | avt | query/mutation result | Direct | null nếu DB null | Stored filename |
| 9 | data.hoten | hoten | `hoten` | string | Yes | Cv | hoten | query/mutation result | Direct | N/A | Required DB column |
| 10 | data.ngaysinh | ngaysinh | `ngaysinh` | string\|null | Yes | Cv | ngaysinh | query/mutation result | Date → ISO string | null nếu DB null | Timestamptz |
| 11 | data.gioitinh | gioitinh | `gioitinh` | string\|null | Yes | Cv | gioitinh | query/mutation result | Direct | null nếu DB null |  |
| 12 | data.email | email | `email` | string | Yes | Cv | email | query/mutation result | Direct | N/A | Required DB column |
| 13 | data.sdt | sdt | `sdt` | string\|null | Yes | Cv | sdt | query/mutation result | Direct | null nếu DB null |  |
| 14 | data.diachi | diachi | `diachi` | string\|null | Yes | Cv | diachi | query/mutation result | Direct | null nếu DB null |  |
| 15 | data.vitri | vitri | `vitri` | string\|null | Yes | Cv | vitri | query/mutation result | Direct | null nếu DB null |  |
| 16 | data.nganh | nganh | `nganh` | string\|null | Yes | Cv | nganh | query/mutation result | Direct | null nếu DB null |  |
| 17 | data.muctieunghiep | muctieunghiep | `muctieunghiep` | string\|null | Yes | Cv | muctieunghiep | query/mutation result | Direct | null nếu DB null |  |
| 18 | data.hocvan | hocvan | `hocvan` | string\|null | Yes | Cv | hocvan | query/mutation result | Direct | null nếu DB null |  |
| 19 | data.kinhnghiem | kinhnghiem | `kinhnghiem` | string\|null | Yes | Cv | kinhnghiem | query/mutation result | Direct | null nếu DB null |  |
| 20 | data.kynang | kynang | `kynang` | string\|null | Yes | Cv | kynang | query/mutation result | Direct | null nếu DB null |  |
| 21 | data.ngoaingu | ngoaingu | `ngoaingu` | string\|null | Yes | Cv | ngoaingu | query/mutation result | Direct | null nếu DB null |  |
| 22 | data.chungchi | chungchi | `chungchi` | string\|null | Yes | Cv | chungchi | query/mutation result | Direct | null nếu DB null |  |
| 23 | data.duan | duan | `duan` | string\|null | Yes | Cv | duan | query/mutation result | Direct | null nếu DB null |  |
| 24 | data.giaithuong | giaithuong | `giaithuong` | string\|null | Yes | Cv | giaithuong | query/mutation result | Direct | null nếu DB null |  |
| 25 | data.hoatdong | hoatdong | `hoatdong` | string\|null | Yes | Cv | hoatdong | query/mutation result | Direct | null nếu DB null |  |
| 26 | data.social | social | `social` | object\|string\|null | Yes | Cv | social | query/mutation result | Direct/JSONB | null nếu DB null | String input is parsed when valid |
| 27 | data.portfolio | portfolio | `portfolio` | string\|null | Yes | Cv | portfolio | query/mutation result | Direct | null nếu DB null |  |
| 28 | data.luongmongmuon | luongmongmuon | `luongmongmuon` | string\|null | Yes | Cv | luongmongmuon | query/mutation result | Direct | null nếu DB null |  |
| 29 | data.created_at | created_at | `created_at` | string\|null | Yes | Cv | created_at | query/mutation result | Date → ISO string | null nếu DB null | Timestamptz |
| 30 | data.sinhvien_id | sinhvien_id | `sinhvien_id` | number\|null | Yes | Cv | sinhvien_id | query/mutation result | BigInt → JSON number | null nếu DB null | Unique FK |

> HTTP status là transport status; không được thêm `HTTPStatus` vào JSON body vì current `reply` không trả field này.

## Ví dụ thành công

```json
{
  "success": true,
  "businessCode": "CV_UPDATED",
  "message": "Source success message",
  "data": {},
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000000"
}
```

## Ví dụ lỗi

```json
{
  "success": false,
  "businessCode": "UNAUTHORIZED",
  "message": "Source error message",
  "data": null,
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000000"
}
```

---
## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `2.Response`
- Dimension: `A2:BR45`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `52`
- Số vùng merge: `15`

<details>
<summary>Danh sách vùng merge</summary>

- `B14:C15`
- `B16:C16`
- `B21:C21`
- `B22:BA22`
- `B23:C23`
- `B24:C24`
- `D14:S14`
- `T14:AK14`
- `AL14:BA15`
- `B20:C20`
- `B17:C17`
- `B18:C18`
- `T18:AB18`
- `AC18:AK18`
- `B19:BA19`

</details>

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 2 | `B2` | Giải thích |  |
| 4 | `C4` | Giá trị trả về khi call API |  |
| 9 | `B9` | Format |  |
| 9 | `L9` | JSON |  |
| 10 | `B10` | Code ký tự |  |
| 10 | `L10` | UTF-8 |  |
| 11 | `B11` | Content-Type |  |
| 11 | `L11` | application/json |  |
| 14 | `B14` | No |  |
| 14 | `D14` | Response item name |  |
| 14 | `T14` | Refer DB |  |
| 14 | `AL14` | Remarks |  |
| 15 | `D15` | Tên logic |  |
| 15 | `L15` | Tên vật lý |  |
| 15 | `T15` | Table nguồn get |  |
| 15 | `AC15` | Field nguồn get |  |
| 16 | `B16` | 1 |  |
| 16 | `D16` | HTTP Status |  |
| 16 | `L16` | HTTPStatus |  |
| 16 | `AL16` | Thành công: 200/ Phát sinh lỗi: 500/ Validate lỗi: 400 |  |
| 17 | `B17` | 2 |  |
| 17 | `D17` | Status |  |
| 17 | `L17` | status |  |
| 17 | `AL17` | Thành công: 1/phát sinh error: 2 |  |
| 18 | `B18` | 3 |  |
| 18 | `D18` | Nội dung response |  |
| 18 | `L18` | response |  |
| 19 | `B19` | Trường hợp thành công |  |
| 20 | `B20` | 3.1 |  |
| 21 | `B21` | 3.2 |  |
| 22 | `B22` | Các trường hợp lỗi của API |  |
| 23 | `B23` | 3.1 |  |
| 23 | `D23` | Error code |  |
| 23 | `M23` | error_code |  |
| 24 | `B24` | 3.2 |  |
| 24 | `D24` | Error Message id |  |
| 24 | `M24` | error_message_id |  |
| 26 | `B26` | Ví dụ |  |
| 27 | `M27` | Trường hợp thành công |  |
| 28 | `N28` | { |  |
| 29 | `O29` |   "status": 1, |  |
| 30 | `O30` |   "response":{ |  |
| 33 | `O33` | } |  |
| 34 | `N34` | } |  |
| 36 | `M36` | Trường hợp lỗi |  |
| 37 | `N37` | { |  |
| 38 | `O38` | "status" : 2 , |  |
| 39 | `O39` | "response" : {  |  |
| 40 | `P40` | "error_code" : "9999", |  |
| 41 | `P41` | "error_message_id" : "DLG000000" |  |
| 42 | `O42` |  } |  |
| 43 | `N43` |  } |  |

</details>
