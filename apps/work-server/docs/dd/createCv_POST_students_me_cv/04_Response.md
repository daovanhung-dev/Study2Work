---
title: "Response"
order: 4
dd_id: "createCv"
api_name: "cv.view.createCv"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "2.Response"
status: "Draft — Ready for Review"
---
# Response

## Format

Mọi success response dùng `successResponse`; mọi lỗi đi qua `errorResponse`/centralized exception handler.

| Field | Type | Example | Description | Source |
| ---: | --- | --- | --- | --- |
| success | boolean | true | Luôn true ở success response. | successResponse |
| businessCode | string | `CV_CREATED` | Business code do view/system route trả về. | successResponse |
| message | string | Tạo CV thành công. | Message source-confirmed. | successResponse |
| data | object | route-specific | jsonSafe chuyển BigInt/Date trước khi serialize. | view result |
| meta | object | {} | Pagination hoặc object rỗng. | successResponse |
| traceId | UUID string | 11111111-1111-4111-8111-111111111111 | Lấy từ AsyncLocalStorage/request trace context. | traceMiddleware |
| data.id | number sau jsonSafe | source value | Raw Cv Prisma field. | cv view/query |
| data.avt | string \| null | source value | Raw Cv Prisma field. | cv view/query |
| data.hoten | string \| null | source value | Raw Cv Prisma field. | cv view/query |
| data.ngaysinh | string ISO-8601 sau jsonSafe | source value | Raw Cv Prisma field. | cv view/query |
| data.gioitinh | string \| null | source value | Raw Cv Prisma field. | cv view/query |
| data.email | string \| null | source value | Raw Cv Prisma field. | cv view/query |
| data.sdt | string \| null | source value | Raw Cv Prisma field. | cv view/query |
| data.diachi | string \| null | source value | Raw Cv Prisma field. | cv view/query |
| data.vitri | string \| null | source value | Raw Cv Prisma field. | cv view/query |
| data.nganh | string \| null | source value | Raw Cv Prisma field. | cv view/query |
| data.muctieunghiep | string \| null | source value | Raw Cv Prisma field. | cv view/query |
| data.hocvan | string \| null | source value | Raw Cv Prisma field. | cv view/query |
| data.kinhnghiem | string \| null | source value | Raw Cv Prisma field. | cv view/query |
| data.kynang | string \| null | source value | Raw Cv Prisma field. | cv view/query |
| data.ngoaingu | string \| null | source value | Raw Cv Prisma field. | cv view/query |
| data.chungchi | string \| null | source value | Raw Cv Prisma field. | cv view/query |
| data.duan | string \| null | source value | Raw Cv Prisma field. | cv view/query |
| data.giaithuong | string \| null | source value | Raw Cv Prisma field. | cv view/query |
| data.hoatdong | string \| null | source value | Raw Cv Prisma field. | cv view/query |
| data.social | JSON \| null | source value | Raw Cv Prisma field. | cv view/query |
| data.portfolio | string \| null | source value | Raw Cv Prisma field. | cv view/query |
| data.luongmongmuon | string \| null | source value | Raw Cv Prisma field. | cv view/query |
| data.created_at | string ISO-8601 sau jsonSafe | source value | Raw Cv Prisma field. | cv view/query |
| data.sinhvien_id | number sau jsonSafe | source value | Raw Cv Prisma field. | cv view/query |

## Ví dụ thành công

```json
{
  "success": true,
  "businessCode": "CV_CREATED",
  "message": "Tạo CV thành công.",
  "data": {
    "id": 1,
    "avt": null,
    "hoten": "Test Student",
    "ngaysinh": null,
    "gioitinh": null,
    "email": "student@example.com",
    "sdt": null,
    "diachi": null,
    "vitri": null,
    "nganh": null,
    "muctieunghiep": null,
    "hocvan": null,
    "kinhnghiem": null,
    "kynang": null,
    "ngoaingu": null,
    "chungchi": null,
    "duan": null,
    "giaithuong": null,
    "hoatdong": null,
    "social": null,
    "portfolio": null,
    "luongmongmuon": null,
    "created_at": "2026-09-18T00:00:00.000Z",
    "sinhvien_id": 1
  },
  "meta": {},
  "traceId": "11111111-1111-4111-8111-111111111111"
}
```

## Ví dụ lỗi

```json
{
  "success": false,
  "businessCode": "INVALID_REQUEST",
  "message": "Họ tên CV bắt buộc.",
  "data": null,
  "meta": {},
  "traceId": "11111111-1111-4111-8111-111111111111"
}
```

## Serialization and trace

- `BigInt` được serialize thành number bởi `jsonSafe`.
- `Date` được serialize thành ISO-8601 string bởi `jsonSafe`.
- `X-Trace-Id` response header bằng `traceId` trong body.
- `meta.fieldErrors` chỉ có khi centralized mapper nhận `ZodError` có field issues.


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
