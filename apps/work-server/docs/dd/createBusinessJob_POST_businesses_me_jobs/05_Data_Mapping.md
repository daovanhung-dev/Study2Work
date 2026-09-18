---
title: "Data Mapping"
order: 5
dd_id: "createBusinessJob"
api_name: "Create business job"
source_sheet: "3. Data mapping"
status: "Draft — Needs Confirmation"
---
# Data Mapping

## Flow xử lý data

## 1. Get thông tin

### 1.1. Get request header và token

- `authorization`: middleware đọc từ `header["Authorization"]`.
- `user_id`: lấy từ verified `req.user.id`.
- `email`: lấy từ verified `req.user.email`.
- `role`: lấy từ verified `req.user.role`.

### 1.2. Get path/query/body data

- `ten_vi_tri`: lấy từ `req.body.ten_vi_tri`.
- `phong_ban`: lấy từ `req.body.phong_ban`.
- `cap_bac`: lấy từ `req.body.cap_bac`.
- `bao_cao_cho`: lấy từ `req.body.bao_cao_cho`.
- `nhiem_vu`: lấy từ `req.body.nhiem_vu`.
- `trinh_do`: lấy từ `req.body.trinh_do`.
- `kinh_nghiem`: lấy từ `req.body.kinh_nghiem`.
- `ky_nang`: lấy từ `req.body.ky_nang`.
- `ky_nang_mem`: lấy từ `req.body.ky_nang_mem`.
- `uu_tien`: lấy từ `req.body.uu_tien`.
- `muc_luong`: lấy từ `req.body.muc_luong`.
- `phuc_loi`: lấy từ `req.body.phuc_loi`.
- `moi_truong`: lấy từ `req.body.moi_truong`.
- `dia_diem`: lấy từ `req.body.dia_diem`.
- `thoi_gian`: lấy từ `req.body.thoi_gian`.
- `han_nop`: lấy từ `req.body.han_nop`.
- `cach_ung_tuyen`: lấy từ `req.body.cach_ung_tuyen`.
- `mo_ta`: lấy từ `req.body.mo_ta`.
- `ten_cong_ty`: lấy từ `req.body.ten_cong_ty`.
- `nganh`: lấy từ `req.body.nganh`.
- `avt`: lấy từ `req.file` và dùng `req.file.filename` nếu upload thành công.

## 2. Check quyền

### 2.1. Permission

- `ensureAuthenticated`: yêu cầu `req.user` tồn tại và `req.authenticated` không phải `false`.
- `checkRole("business")`: chỉ cho phép JWT có role `business`.

## 3. Validate data input

- `ten_vi_tri` và `dia_diem` phải có giá trị.
- `doanhnghiep_id` được lấy từ JWT, không lấy từ request.
- Ảnh phải qua Multer extension/file-size filter.

## 4. Query và business processing

### 4.1. Chuẩn bị owner/company

- Tạo data bằng `jdData(req.body, req.file.filename)`.
- Gán `data.doanhnghiep_id = user.id`.
- Gọi `BusinessService.getDoanhNghiepById(user.id)` để lấy `hoten`.
- Nếu request không có `ten_cong_ty` và business tồn tại, dùng `business.data.hoten`.

## 5. Insert/Update/Delete thông tin

### 5.1. INSERT `JD`

- Nếu thiếu `ten_vi_tri` hoặc `dia_diem`, trả `400 INVALID_REQUEST`.
- Gọi `JDService.insertJD(data)`.
- Prisma tạo record `JD`.
- Không có transaction explicit trong source.

## 6. Map response và error

- `data` là record `JD` vừa tạo.
- Ảnh được lưu ở dạng `/uploads/<filename>` trong `JD.avt`.
- Thành công: `reply` trả HTTP `201`, `businessCode = JOB_CREATED`, `data` theo [04_Response.md](./04_Response.md).
- Mọi lỗi route dùng `reply` hoặc app exception handler; `data = null`, `success = false`, `traceId` được trả trong body và `X-Trace-Id` header.
- Chi tiết lỗi: [06_Error.md](./06_Error.md).
- DB mapping: [07_JD_insert.md](./07_JD_insert.md).

---
## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `3. Data mapping`
- Dimension: `B1:BB61`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `63`
- Số vùng merge: `0`

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 2 | `B2` | Flow xử lý data |  |
| 4 | `D4` | 0. |  |
| 4 | `E4` | Check quyền |  |
| 5 | `E5` | ・ |  |
| 5 | `F5` | Thực hiện check quyền |  |
| 6 | `E6` | ・ |  |
| 6 | `F6` | Get count khi get data từ … |  |
| 7 | `G7` | Table get |  |
| 7 | `K7` | : |  |
| 8 | `G8` | Conditions |  |
| 8 | `K8` | : |  |
| 10 | `E10` | ・ |  |
| 10 | `F10` | Trường hợp giá trị get được lớn hơn 0, thực hiện các xử lý tiếp theo |  |
| 11 | `E11` | ・ |  |
| 11 | `F11` | Trường hợp giá trị get được bằng 0, trả về status 2 |  |
| 13 | `D13` | 1. |  |
| 13 | `E13` | validate data input |  |
| 14 | `F14` | refer sheet [４．Error] |  |
| 16 | `D16` | 2. |  |
| 16 | `E16` | Get thông tin… |  |
| 18 | `F18` | Table get |  |
| 18 | `K18` | Column get |  |
| 18 | `P18` | Chú thích |  |
| 18 | `U18` | Remarks |  |
| 29 | `F29` | Target table / join condition |  |
| 30 | `F30` | Target table |  |
| 30 | `N30` | Join condition |  |
| 30 | `AL30` | 結合種類 |  |
| 31 | `F31` | txn_ams_t0320 AS a |  |
| 32 | `F32` | txn_amm_v0002 AS b |  |
| 32 | `N32` | ON a . chy_typ = b . kbn_typ AND b . dmin_cd = A AND b . kbnknr_cd = 001 |  |
| 32 | `AL32` | LEFT JOIN |  |
| 33 | `F33` | txn_amm_v0002 AS c |  |
| 33 | `N33` | ON a . chy_typ = c . kbn_typ AND c . dmin_cd = A AND c . kbnknr_cd = Z02 |  |
| 33 | `AL33` | LEFT JOIN |  |
| 35 | `F35` | ・ |  |
| 35 | `G35` | Điều kiện get data |  |
| 37 | `F37` | ・ |  |
| 37 | `G37` | Điều kiện sort |  |
| 41 | `D41` | 3. |  |
| 41 | `E41` | Insert/Update thông tin … |  |
| 42 | `E42` | Update table…. |  |
| 43 | `E43` | ・ |  |
| 43 | `F43` | Items update |  |
| 44 | `F44` | ・ |  |
| 44 | `G44` | Refer sheet [xxxx] |  |
| 45 | `E45` | ・ |  |
| 45 | `F45` | Điều kiện get data |  |
| 46 | `F46` | ・ |  |
| 46 | `G46` | auth_user. id = user hiện tại theo token |  |
| 48 | `D48` | 4. |  |
| 48 | `E48` | check kết quả execute query  |  |
| 49 | `E49` | 1. Thành công |  |
| 50 | `F50` | HTTPStatus = 200 |  |
| 51 | `F51` | Trả về kết quả status = 1 |  |
| 52 | `E52` | 2. Lỗi hệ thống phát sinh |  |
| 53 | `F53` | HTTPStatus = 500 |  |
| 54 | `F54` | Trả về kết quả status = 2 |  |
| 55 | `E55` | 3. Validate lỗi |  |
| 56 | `F56` | HTTPStatus = 400 |  |
| 57 | `F57` | Trả về kết quả status = 2 |  |
| 58 | `E58` | 4. Ngoài trường hợp trên |  |
| 59 | `F59` | Trả về kết quả status = 2 |  |

</details>
