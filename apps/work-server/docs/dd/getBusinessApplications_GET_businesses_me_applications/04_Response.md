---
title: "Response"
order: 4
dd_id: "getBusinessApplications"
api_name: "Get business applications"
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
| 7 | data[].id | id | `id` | number | Yes | UngVien | id | query/mutation result | BigInt → JSON number | N/A |  |
| 8 | data[].created_at | created_at | `created_at` | string | Yes | UngVien | created_at | query/mutation result | Date → ISO string | N/A |  |
| 9 | data[].sinhvien_id | sinhvien_id | `sinhvien_id` | number\|null | Yes | UngVien | sinhvien_id | query/mutation result | BigInt → JSON number | null nếu DB null | FK |
| 10 | data[].doanhnghiep_id | doanhnghiep_id | `doanhnghiep_id` | number\|null | Yes | UngVien | doanhnghiep_id | query/mutation result | BigInt → JSON number | null nếu DB null | FK |
| 11 | data[].trangthai | trangthai | `trangthai` | string\|null | Yes | UngVien | trangthai | query/mutation result | Direct | null nếu DB null | Default `chưa ứng tuyển` |
| 12 | data[].jd_id | jd_id | `jd_id` | number\|null | Yes | UngVien | jd_id | query/mutation result | BigInt → JSON number | null nếu DB null | FK |
| 13 | data[].SinhVien.id | id | `id` | number | Yes | SinhVien | id | query/mutation result | BigInt → JSON number | N/A | Public selected field |
| 14 | data[].SinhVien.hoten | hoten | `hoten` | string\|null | Yes | SinhVien | hoten | query/mutation result | Direct | null nếu DB null | Public selected field |
| 15 | data[].SinhVien.email | email | `email` | string\|null | Yes | SinhVien | email | query/mutation result | Direct | null nếu DB null | Public selected field |
| 16 | data[].SinhVien.chuyennganh | chuyennganh | `chuyennganh` | string\|null | Yes | SinhVien | chuyennganh | query/mutation result | Direct | null nếu DB null | Public selected field |
| 17 | data[].SinhVien.avt | avt | `avt` | string\|null | Yes | SinhVien | avt | query/mutation result | Direct | null nếu DB null | Public selected field |
| 18 | data[].JD.id | id | `id` | number | Yes | JD | id | query/mutation result | BigInt → JSON number | N/A |  |
| 19 | data[].JD.ten_vi_tri | ten_vi_tri | `ten_vi_tri` | string | Yes | JD | ten_vi_tri | query/mutation result | Direct | N/A | Required DB column |
| 20 | data[].JD.phong_ban | phong_ban | `phong_ban` | string\|null | Yes | JD | phong_ban | query/mutation result | Direct | null nếu DB null |  |
| 21 | data[].JD.cap_bac | cap_bac | `cap_bac` | string\|null | Yes | JD | cap_bac | query/mutation result | Direct | null nếu DB null |  |
| 22 | data[].JD.bao_cao_cho | bao_cao_cho | `bao_cao_cho` | string\|null | Yes | JD | bao_cao_cho | query/mutation result | Direct | null nếu DB null |  |
| 23 | data[].JD.nhiem_vu | nhiem_vu | `nhiem_vu` | string\|null | Yes | JD | nhiem_vu | query/mutation result | Direct | null nếu DB null |  |
| 24 | data[].JD.trinh_do | trinh_do | `trinh_do` | string\|null | Yes | JD | trinh_do | query/mutation result | Direct | null nếu DB null |  |
| 25 | data[].JD.kinh_nghiem | kinh_nghiem | `kinh_nghiem` | string\|null | Yes | JD | kinh_nghiem | query/mutation result | Direct | null nếu DB null |  |
| 26 | data[].JD.ky_nang | ky_nang | `ky_nang` | string\|null | Yes | JD | ky_nang | query/mutation result | Direct | null nếu DB null |  |
| 27 | data[].JD.ky_nang_mem | ky_nang_mem | `ky_nang_mem` | string\|null | Yes | JD | ky_nang_mem | query/mutation result | Direct | null nếu DB null |  |
| 28 | data[].JD.uu_tien | uu_tien | `uu_tien` | string\|null | Yes | JD | uu_tien | query/mutation result | Direct | null nếu DB null |  |
| 29 | data[].JD.muc_luong | muc_luong | `muc_luong` | string\|null | Yes | JD | muc_luong | query/mutation result | Direct | null nếu DB null |  |
| 30 | data[].JD.phuc_loi | phuc_loi | `phuc_loi` | string\|null | Yes | JD | phuc_loi | query/mutation result | Direct | null nếu DB null |  |
| 31 | data[].JD.moi_truong | moi_truong | `moi_truong` | string\|null | Yes | JD | moi_truong | query/mutation result | Direct | null nếu DB null |  |
| 32 | data[].JD.dia_diem | dia_diem | `dia_diem` | string\|null | Yes | JD | dia_diem | query/mutation result | Direct | null nếu DB null |  |
| 33 | data[].JD.thoi_gian | thoi_gian | `thoi_gian` | string\|null | Yes | JD | thoi_gian | query/mutation result | Direct | null nếu DB null |  |
| 34 | data[].JD.han_nop | han_nop | `han_nop` | string\|null | Yes | JD | han_nop | query/mutation result | Direct | null nếu DB null |  |
| 35 | data[].JD.cach_ung_tuyen | cach_ung_tuyen | `cach_ung_tuyen` | string\|null | Yes | JD | cach_ung_tuyen | query/mutation result | Direct | null nếu DB null |  |
| 36 | data[].JD.ngay_tao | ngay_tao | `ngay_tao` | string\|null | Yes | JD | ngay_tao | query/mutation result | Date → ISO string | null nếu DB null | Timestamptz |
| 37 | data[].JD.mo_ta | mo_ta | `mo_ta` | string\|null | Yes | JD | mo_ta | query/mutation result | Direct | null nếu DB null |  |
| 38 | data[].JD.doanhnghiep_id | doanhnghiep_id | `doanhnghiep_id` | number\|null | Yes | JD | doanhnghiep_id | query/mutation result | BigInt → JSON number | null nếu DB null | FK |
| 39 | data[].JD.ten_cong_ty | ten_cong_ty | `ten_cong_ty` | string\|null | Yes | JD | ten_cong_ty | query/mutation result | Direct | null nếu DB null |  |
| 40 | data[].JD.nganh | nganh | `nganh` | string\|null | Yes | JD | nganh | query/mutation result | Direct | null nếu DB null |  |
| 41 | data[].JD.avt | avt | `avt` | string\|null | Yes | JD | avt | query/mutation result | Direct | null nếu DB null | Stored `/uploads/` path for JD |

> HTTP status là transport status; không được thêm `HTTPStatus` vào JSON body vì current `reply` không trả field này.

## Ví dụ thành công

```json
{
  "success": true,
  "businessCode": "BUSINESS_APPLICATIONS_LOADED",
  "message": "Source success message",
  "data": [],
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
