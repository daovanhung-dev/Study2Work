---
title: "Request"
order: 3
dd_id: "createBusinessJob"
api_name: "Create business job"
source_sheet: "1.Request"
status: "Draft — Needs Confirmation"
---
# Request

## API endpoint

| Thuộc tính | Giá trị |
|---|---|
| HTTP method | `POST` |
| URI | `/api/v1/businesses/me/jobs` |
| Character encoding | UTF-8 |
| Content-Type | multipart/form-data |

## Request header

| No | Logical name | Field name | Required | Value/Format | Description | Data Mapping reference |
|---|---|---|---|---|---|---|
| 1 | Contents type | `Content-Type` | Yes | multipart/form-data | Request media type | `05_Data_Mapping.md` |
| 2 | Bearer auth | `Authorization` | Yes | `Bearer redacted.jwt.token` | Verified by global middleware and route boundary | `05_Data_Mapping.md` |

## Path parameters

N/A — API không nhận Path parameter.

## Query parameters

N/A — API không nhận Query parameter.

## Request body

| No | Location | Logical name | Physical name | Type | Required | Min | Max | Character type | Format | Valid values | Description | Data Mapping reference |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | body | ten_vi_tri | `ten_vi_tri` | string | Conditional | N/A | N/A | UTF-8/text | N/A | N/A | Tên vị trí | `05_Data_Mapping.md` |
| 2 | body | phong_ban | `phong_ban` | string | No | N/A | N/A | UTF-8/text | N/A | N/A | Phòng ban | `05_Data_Mapping.md` |
| 3 | body | cap_bac | `cap_bac` | string | No | N/A | N/A | UTF-8/text | N/A | N/A | Cấp bậc | `05_Data_Mapping.md` |
| 4 | body | bao_cao_cho | `bao_cao_cho` | string | No | N/A | N/A | UTF-8/text | N/A | N/A | Báo cáo cho | `05_Data_Mapping.md` |
| 5 | body | nhiem_vu | `nhiem_vu` | string | No | N/A | N/A | UTF-8/text | N/A | N/A | Nhiệm vụ | `05_Data_Mapping.md` |
| 6 | body | trinh_do | `trinh_do` | string | No | N/A | N/A | UTF-8/text | N/A | N/A | Trình độ | `05_Data_Mapping.md` |
| 7 | body | kinh_nghiem | `kinh_nghiem` | string | No | N/A | N/A | UTF-8/text | N/A | N/A | Kinh nghiệm | `05_Data_Mapping.md` |
| 8 | body | ky_nang | `ky_nang` | string | No | N/A | N/A | UTF-8/text | N/A | N/A | Kỹ năng | `05_Data_Mapping.md` |
| 9 | body | ky_nang_mem | `ky_nang_mem` | string | No | N/A | N/A | UTF-8/text | N/A | N/A | Kỹ năng mềm | `05_Data_Mapping.md` |
| 10 | body | uu_tien | `uu_tien` | string | No | N/A | N/A | UTF-8/text | N/A | N/A | Ưu tiên | `05_Data_Mapping.md` |
| 11 | body | muc_luong | `muc_luong` | string | No | N/A | N/A | UTF-8/text | N/A | N/A | Mức lương | `05_Data_Mapping.md` |
| 12 | body | phuc_loi | `phuc_loi` | string | No | N/A | N/A | UTF-8/text | N/A | N/A | Phúc lợi | `05_Data_Mapping.md` |
| 13 | body | moi_truong | `moi_truong` | string | No | N/A | N/A | UTF-8/text | N/A | N/A | Môi trường | `05_Data_Mapping.md` |
| 14 | body | dia_diem | `dia_diem` | string | Conditional | N/A | N/A | UTF-8/text | N/A | N/A | Địa điểm | `05_Data_Mapping.md` |
| 15 | body | thoi_gian | `thoi_gian` | string | No | N/A | N/A | UTF-8/text | N/A | N/A | Thời gian | `05_Data_Mapping.md` |
| 16 | body | han_nop | `han_nop` | string | No | N/A | N/A | UTF-8/text | N/A | N/A | Hạn nộp | `05_Data_Mapping.md` |
| 17 | body | cach_ung_tuyen | `cach_ung_tuyen` | string | No | N/A | N/A | UTF-8/text | N/A | N/A | Cách ứng tuyển | `05_Data_Mapping.md` |
| 18 | body | mo_ta | `mo_ta` | string | No | N/A | N/A | UTF-8/text | N/A | N/A | Mô tả | `05_Data_Mapping.md` |
| 19 | body | ten_cong_ty | `ten_cong_ty` | string | No | N/A | N/A | UTF-8/text | N/A | N/A | Tên công ty; create lấy từ doanh nghiệp nếu bỏ trống | `05_Data_Mapping.md` |
| 20 | body | nganh | `nganh` | string | No | N/A | N/A | UTF-8/text | N/A | N/A | Ngành | `05_Data_Mapping.md` |
| 21 | file | avt | `avt` | binary file | No | N/A | N/A | UTF-8/text | jpeg\|jpg\|png\|gif; tối đa 10 MB | N/A | Ảnh JD; source lưu `/uploads/<filename>` | `05_Data_Mapping.md` |
> Mỗi field nằm trên một row riêng. `Conditional` nghĩa là source kiểm tra điều kiện kết hợp chứ không yêu cầu field đó độc lập.

## Ví dụ Request data

```text
Content-Type: multipart/form-data; boundary=client-generated-boundary

field_name = field_value
avt = example.jpg (optional)
```

---
## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `1.Request`
- Dimension: `A1:BR34`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `62`
- Số vùng merge: `25`

<details>
<summary>Danh sách vùng merge</summary>

- `S16:T16`
- `U16:V16`
- `W18:X18`
- `W19:X19`
- `U19:V19`
- `S19:T19`
- `U18:V18`
- `S17:T17`
- `S18:T18`
- `AK18:BA18`
- `S15:T15`
- `U15:V15`
- `W15:X15`
- `U14:V14`
- `W14:X14`
- `W17:X17`
- `S13:T14`
- `U13:X13`
- `U17:V17`
- `W16:X16`
- `Y13:AA14`
- `AB14:AD14`
- `AE14:AG14`
- `AB13:AG13`
- `AH13:AJ14`

</details>

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 2 | `B2` | HTTP method |  |
| 2 | `L2` | GET/POST |  |
| 3 | `B3` | URI |  |
| 4 | `B4` | Code ký tự |  |
| 4 | `L4` | UTF-8 |  |
| 6 | `B6` | Request header |  |
| 7 | `B7` | Name |  |
| 7 | `J7` | Field name |  |
| 7 | `V7` | Giá trị |  |
| 7 | `AK7` | Giải thích |  |
| 8 | `B8` | Contents type |  |
| 8 | `J8` | Content-Type |  |
| 8 | `V8` | application/json |  |
| 8 | `AK8` | Thực hiện request bằng json data |  |
| 9 | `B9` | Basic authen |  |
| 9 | `J9` | Authorization |  |
| 9 | `V9` | Token |  |
| 11 | `B11` | Request data |  |
| 12 | `B12` | No |  |
| 12 | `C12` | Key name |  |
| 12 | `S12` | Nội dung check |  |
| 12 | `AK12` | Giải thích |  |
| 13 | `S13` | Bắt buộc |  |
| 13 | `U13` | Số ký tự |  |
| 13 | `Y13` | Loại ký tự |  |
| 13 | `AB13` | Format |  |
| 13 | `AH13` | Giá trị hợp lệ |  |
| 14 | `C14` | Logic |  |
| 14 | `K14` | Vật lý |  |
| 14 | `U14` | Tối thiểu |  |
| 14 | `W14` | Tối đa |  |
| 15 | `B15` | 1 |  |
| 15 | `S15` | ○ |  |
| 15 | `U15` | 1 |  |
| 15 | `W15` | 20 |  |
| 15 | `Y15` | halfsize |  |
| 16 | `B16` | 2 |  |
| 16 | `S16` | ○ |  |
| 16 | `U16` | 1 |  |
| 16 | `W16` | 8 |  |
| 16 | `Y16` | halfsize |  |
| 16 | `AB16` | datetime |  |
| 16 | `AE16` | yyyyMMdd |  |
| 17 | `S17` | ○ |  |
| 17 | `U17` | 1 |  |
| 17 | `W17` | 1 |  |
| 17 | `Y17` | halfsize |  |
| 17 | `AB17` | numberic |  |
| 17 | `AH17` | 2,3,4 |  |
| 18 | `S18` | ○ |  |
| 18 | `U18` | 1 |  |
| 18 | `Y18` | fullsize |  |
| 19 | `S19` | ○ |  |
| 19 | `U19` | 1 |  |
| 25 | `B25` | Ví dụ về Request data |  |
| 26 | `L26` | { |  |
| 27 | `M27` | "tnorsh_pln_id" : "0000000001", |  |
| 28 | `M28` | "yt_ymd":" 20201001", |  |
| 29 | `M29` | "yt_hmi":" 0830", |  |
| 30 | `M30` | "excpt_id":" 001", |  |
| 31 | `M31` | "bik_desc":" 計画削除" |  |
| 32 | `L32` | } |  |

</details>
