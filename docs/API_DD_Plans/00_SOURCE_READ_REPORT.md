# Báo cáo đọc nguồn và kiểm kê API DD

## 1. Input Manifest

| Input | Loại | Kết quả |
|---|---:|---|
| `BD(5).zip` | ZIP | Đã giải nén an toàn: **48 file** (`47 .md`, `1 .sql`), **13,921 dòng**, **460,105 byte. Không có archive lồng nhau. |
| `Study2Work_API_Catalog_from_BD(1).csv` | CSV | Đã đọc đủ 157 dòng API và 11 cột; không có ô trống trong các cột catalog. |
| `Detail_Design_API_Template_Optimized.xlsx` | XLSX | Đã đọc 8 sheet: Overview, History, Request, Response, Data Mapping, Error, DB_TABLE_TEMPLATE, 00_Hướng dẫn điền. |
| `Document-Development-AI-Context(1).md` | Skill/Context | Đã đọc toàn bộ 1.132 dòng. |
| `AGENTS.md` | Governance | **Không tìm thấy** trong các input hoặc `/mnt/data`; không có nội dung để nạp. |

## 2. Kết quả xác định API

- Tổng API trong catalog: **157**.
- Basis: **32 trực tiếp**, **125 suy dẫn**.
- STT liên tục từ **1 đến 157**, không có gap.
- Không có cặp `HTTP method + endpoint` bị trùng.
- Phân bố method: **GET: 84**, **POST: 43**, **PUT: 11**, **PATCH: 13**, **DELETE: 6**.

### Phân bố theo module

| Module | API | Trực tiếp | Suy dẫn |
|---|---:|---:|---:|
| 01. Public Catalog | 6 | 3 | 3 |
| 02. Tài khoản, xác thực và hồ sơ | 14 | 3 | 11 |
| 03. Onboarding | 7 | 4 | 3 |
| 04. Lộ trình học | 11 | 2 | 9 |
| 05. Khóa học, chương, bài học và tài nguyên | 9 | 1 | 8 |
| 06. Bài tập và đánh giá | 13 | 3 | 10 |
| 07. Tiến độ và hoàn thành | 9 | 1 | 8 |
| 08. Cộng đồng Zalo | 13 | 4 | 9 |
| 09. Thông báo | 11 | 4 | 7 |
| 10. Admin quản trị nội dung | 34 | 2 | 32 |
| 11. Admin quản lý học viên và hỗ trợ ngoại lệ | 14 | 2 | 12 |
| 12. Báo cáo vận hành | 8 | 2 | 6 |
| 13. Vai trò, phân quyền và audit | 8 | 1 | 7 |

## 3. Cách hiểu template DD

- Template mô tả **một API trên một workbook**.
- `Overview`: định danh, source, transaction, DB interaction, affected tables, assumptions.
- `History`: bắt buộc tăng version/ghi lịch sử khi sửa.
- `Request`: mô tả từng field Path/Query/Header/Body theo JSON Path.
- `Response`: mô tả success response; error tách sang sheet `Error`.
- `Data Mapping`: thứ tự phải phản ánh flow chạy thực tế; query đặt tại bước phát sinh.
- `Error`: mọi lỗi phải liên kết về `Data Mapping Ref.`.
- `DB_TABLE_TEMPLATE`: chỉ duplicate cho bảng bị INSERT/UPDATE/DELETE/UPSERT hoặc đổi schema/constraint/index.
- Checklist template yêu cầu traceability Request → Variable → DB → Response, transaction/rollback, business code, concurrency/idempotency và history.

## 4. Xung đột/điểm cần khóa

1. **Response envelope:** `base/0. Study2Work_System_Architecture.md` chuẩn hóa `success`, `businessCode`, `message`, `data`, `meta`, `traceId`; template ví dụ dùng `code/message/data/traceId`, còn `Study Architecture` cũ dùng `trace_id`. Plan chọn kiến trúc tích hợp làm nguồn chuẩn và yêu cầu ghi rõ việc thay ví dụ template.
2. **SEQ-08 ngoài catalog:** `GET /api/v1/progress/summary` và `POST /api/v1/progress/recalculate` xuất hiện trực tiếp trong Sequence nhưng không nằm trong 157 API. Cần quyết định public/internal/replaced trước khi chốt Plan 09.
3. **Naming convention:** catalog có `page_size` và path param snake_case; kiến trúc tích hợp minh họa `pageSize`, `traceId`. Phải khóa quy ước contract trước bản Final.
4. **125 API suy dẫn:** đây là API proposal từ BD, không phải toàn bộ endpoint được nêu trực tiếp. Mỗi DD phải giữ trạng thái Draft/Needs Confirmation đến khi xác nhận.

## 5. Manifest 48 file đã đọc

| # | File | Dòng | Byte | SHA-256 |
|---:|---|---:|---:|---|
| 1 | `BD/0. Study2Work_Study_Business_Description.md` | 1270 | 57905 | `7340e89be1a18e10a9d96c04ec8ebf1e4e33e87f1ab597f3bb9a07b490baf574` |
| 2 | `BD/01. Study2Work_Study_BasicDesign_Public_Catalog.md` | 203 | 8044 | `92c442bba84589bc61d8a64e7945bc88a2a353b89b730a0345b5ee81ff2121b8` |
| 3 | `BD/02. Study2Work_Study_BasicDesign_Tai_Khoan_Xac_Thuc_Ho_So.md` | 198 | 6949 | `1d3fa307ed296f3c36718daac94eac40bcd573555debecb4961458e2f4cc7028` |
| 4 | `BD/03. Study2Work_Study_BasicDesign_Onboarding.md` | 205 | 6991 | `6adb009c4d5a37ffc156ebeb836094e73015e53c81fc866a95bdb0423abeeec1` |
| 5 | `BD/04. Study2Work_Study_BasicDesign_Lo_Trinh_Hoc.md` | 239 | 7343 | `29a81d3ba4afb551bf235519106f878a75aa816e11e15efc252ad7f8054bef91` |
| 6 | `BD/05. Study2Work_Study_BasicDesign_Khoa_Hoc_Noi_Dung_Hoc.md` | 232 | 6476 | `8c085d9c0e1dff3c20e27cb5f821c8678658f3f5d22af1a180a0ff41f3bce7e3` |
| 7 | `BD/06. Study2Work_Study_BasicDesign_Bai_Tap_Danh_Gia.md` | 229 | 6259 | `b5a5a85927678544d7986c57a810093fc3bce578f461218d9fe6a51354775a98` |
| 8 | `BD/07. Study2Work_Study_BasicDesign_Tien_Do_Hoan_Thanh.md` | 202 | 6117 | `87f3205d6087c4c00ea94c118c98d00ff1dcf1edad7371f8d8cabc7a3bcf89c1` |
| 9 | `BD/08. Study2Work_Study_BasicDesign_Cong_Dong_Zalo.md` | 183 | 5142 | `b842e94d691bfa6ddd7740b3708dc4ef7c62b5f0c98617abe2f872c840d66169` |
| 10 | `BD/09. Study2Work_Study_BasicDesign_Thong_Bao_Nghiep_Vu.md` | 178 | 5956 | `ec9be4d03c6d887eed9fd1f5141ae75f39b8db04c99f36dd5e8d45773f7c216b` |
| 11 | `BD/10. Study2Work_Study_BasicDesign_Admin_Quan_Tri_Noi_Dung.md` | 194 | 6189 | `e6fc1639a319e345e1f12f71c078f616dcde84be84de989e79f6cb809a8f717c` |
| 12 | `BD/11. Study2Work_Study_BasicDesign_Admin_Quan_Ly_Hoc_Vien_Ho_Tro_Ngoai_Le.md` | 192 | 5454 | `39fef5712dce6205bddc61754f42f9a772645e360246a74c3d0fc692c115138f` |
| 13 | `BD/12. Study2Work_Study_BasicDesign_Admin_Bao_Cao_Van_Hanh.md` | 206 | 5785 | `9cf881346aea660dac0b67487d19ab73491189efe6381fbc03902045b6f34962` |
| 14 | `BD/13. Study2Work_Study_BasicDesign_Vai_Tro_Phan_Quyen_Audit_Log.md` | 234 | 7656 | `3778ecc5dcd7650a20c2b8726fc30252d4b37c5f69723607a78fee86dd5aec32` |
| 15 | `BD/base/0. Study2Work_System_Architecture.md` | 1390 | 41013 | `f631c5245fe91966eadf6b8d267fae7ac630dfb5fc4aef6f3b80d4c33770493d` |
| 16 | `BD/base/1. Study2Work_Study_Architecture.md` | 2611 | 64076 | `a62e2390bcc6b4df3270334afeeff136a4e3d3a74450e9ea28f8a01caa1c3218` |
| 17 | `BD/base/2. Study2Work_Work_Architecture.md` | 1694 | 52945 | `2449bbb3297cde5e0a7c01cc8ebab36fbae2ea8d1602a463fcce6c635cc61750` |
| 18 | `BD/diagram/AC/01. Study2Work_Study_Diagram_AC_Luong_Nghiep_Vu_Cot_Loi.md` | 142 | 6024 | `bc706800032f5e64e577e81cf70af7c4ac6e91e2850f6a97957d53fed057e3a6` |
| 19 | `BD/diagram/AC/02. Study2Work_Study_AC_Public_Catalog.md` | 66 | 2526 | `d17f16bebd820d734c2729319d7e99cd142014641d475ec6dd9aa2a2cd8c3b40` |
| 20 | `BD/diagram/AC/03. Study2Work_Study_AC_Tai_Khoan_Xac_Thuc_Ho_So.md` | 60 | 2140 | `ab704350bae6cf3ff6863a6491f4c0704c2680634408a6f6180b5fb134e5c495` |
| 21 | `BD/diagram/AC/04. Study2Work_Study_AC_Onboarding.md` | 55 | 1758 | `ebef11dba375d4cd817e628f8f20ebde3dd947c6604abcca3796a158636421bd` |
| 22 | `BD/diagram/AC/05. Study2Work_Study_AC_Lo_Trinh_Hoc.md` | 54 | 2005 | `ce5335a9a783fea6043a3f4fb267a84ba06c22fc47ac31ffd911b468101cee9b` |
| 23 | `BD/diagram/AC/06. Study2Work_Study_AC_Khoa_Hoc_Noi_Dung_Hoc.md` | 51 | 1828 | `714ee32f7ef8b7f4a0bd94873dc5dc5c77d95cbaf3a2ecfb3afdb951545e5b41` |
| 24 | `BD/diagram/AC/07. Study2Work_Study_AC_Bai_Tap_Danh_Gia.md` | 62 | 1971 | `9c2fa7250da57732a842c60d7583c7fc6b81100fc9affbd7bd847d0ad8f47f95` |
| 25 | `BD/diagram/AC/08. Study2Work_Study_AC_Tien_Do_Hoan_Thanh.md` | 50 | 1804 | `718525819b872ab773041752aec5c4e49a4411e5ee92247ef6563fceaf83e65a` |
| 26 | `BD/diagram/AC/09. Study2Work_Study_AC_Cong_Dong_Zalo.md` | 48 | 1587 | `10e60a0411a74e9ea39370cd0a8d656aa517271be6f41541a465184802d6371a` |
| 27 | `BD/diagram/AC/10. Study2Work_Study_AC_Thong_Bao_Nghiep_Vu.md` | 48 | 1664 | `05bb3d584b650ccb6e2cdd2197a22c055974dcbec84c1a947cb7af3186f0ee82` |
| 28 | `BD/diagram/AC/11. Study2Work_Study_AC_Admin_Quan_Tri_Noi_Dung.md` | 61 | 1860 | `b42b8b9e9847de4be6860994143970a9b6bc97eda24d1335746d4a56a7478170` |
| 29 | `BD/diagram/AC/12. Study2Work_Study_AC_Admin_Hoc_Vien_Ho_Tro_Ngoai_Le.md` | 54 | 1697 | `fafdcb6a7c0907da146ec4726abccb9284afcec0e587529b7a3104f6463c8710` |
| 30 | `BD/diagram/AC/13. Study2Work_Study_AC_Admin_Bao_Cao_Van_Hanh.md` | 60 | 1775 | `ade8a856d0df76b266c927413d2c4ce1759b3b84c6082230f2e53b2e5660f702` |
| 31 | `BD/diagram/AC/14. Study2Work_Study_AC_RBAC_Audit_Log.md` | 50 | 1639 | `4be4a0255afc23f830538665f77b6d8236688b40fcfcef097c6547a0a3422c6f` |
| 32 | `BD/diagram/CLASS/01. Study2Work_Study_Diagram_CLASS_Mo_Hinh_Nghiep_Vu.md` | 372 | 9749 | `62903eae272e38c4baa8820e71a4355e9d2865520707c52877340e7a7bfdc440` |
| 33 | `BD/diagram/CLASS/study2work_study_full_schema_seed.sql` | 1193 | 75158 | `bce536f1a3888794140a5a18aaa1ebe3b5bf997dc62b1ffd3536608da932cfa5` |
| 34 | `BD/diagram/SEQUENCE/01. Study2Work_Study_Diagram_SEQUENCE_Hoc_Vien_Cot_Loi.md` | 149 | 6480 | `740d3f4909912fa9d7213d118ea6afaa7bddab6e1473a6d689d43905fc8534ad` |
| 35 | `BD/diagram/SEQUENCE/02. Study2Work_Study_SEQ_Public_Catalog.md` | 135 | 2933 | `ed509a9f06378304da8bfe67fd0cf7bedb9668aa4b120cdbfd54f2e8c7304903` |
| 36 | `BD/diagram/SEQUENCE/03. Study2Work_Study_SEQ_Tai_Khoan_Xac_Thuc_Dang_Nhap.md` | 143 | 2841 | `d0dd601011c9c8ac39a9d691c22771fef5daefa591bcfc73966fc57bad61208a` |
| 37 | `BD/diagram/SEQUENCE/04. Study2Work_Study_SEQ_Onboarding_Goi_Y_Lo_Trinh.md` | 119 | 2560 | `a9577d71fc0b254cd60f6cf92140651fb16a2dde7a1c1ce662aec42899d56598` |
| 38 | `BD/diagram/SEQUENCE/05. Study2Work_Study_SEQ_Kich_Hoat_Lo_Trinh.md` | 98 | 2200 | `a9d1cd9fcfcd9cea35d6b8aaaf2bdd054fe0526ed36ed33e1b2efddda633229c` |
| 39 | `BD/diagram/SEQUENCE/06. Study2Work_Study_SEQ_Hoc_Bai_Cap_Nhat_Tien_Do.md` | 124 | 2592 | `a68e924d35a9145aa9e5526b8e905099a1141a8fc16cd0242df330a4f17fd2b9` |
| 40 | `BD/diagram/SEQUENCE/07. Study2Work_Study_SEQ_Bai_Tap_Nop_Cham_Nop_Lai.md` | 131 | 2938 | `c5187e7c70149b55a12089be70b9040b8b45ab6f7976186abae93c2365d59bb5` |
| 41 | `BD/diagram/SEQUENCE/08. Study2Work_Study_SEQ_Hoan_Thanh_Khoa_Lo_Trinh.md` | 117 | 2452 | `6cdd677e80a212a33e430ecd65af8f850944ab6b5b081fda8c35686ca7958f7a` |
| 42 | `BD/diagram/SEQUENCE/09. Study2Work_Study_SEQ_Cong_Dong_Zalo.md` | 106 | 2283 | `16ac7aa8bf7a43ec52778b87ab7a66a5e06f5e073d3e6b871fb33db76af6690e` |
| 43 | `BD/diagram/SEQUENCE/10. Study2Work_Study_SEQ_Thong_Bao.md` | 122 | 2577 | `f7afbc356b145fe6747e405fe486c205fad4669ffe93b846be3b4ec389a6e8c9` |
| 44 | `BD/diagram/SEQUENCE/11. Study2Work_Study_SEQ_Admin_Quan_Tri_Noi_Dung.md` | 118 | 2615 | `b71d74172c67ef10045011b6e409f51d605329bdd35c8d839c21883637bdf226` |
| 45 | `BD/diagram/SEQUENCE/12. Study2Work_Study_SEQ_Admin_Ho_Tro_Ngoai_Le.md` | 112 | 2715 | `c5d0a2d0f013b03862821d246b34e4d7c3b480a14a59613fc96e7deb4ca0e917` |
| 46 | `BD/diagram/SEQUENCE/13. Study2Work_Study_SEQ_Bao_Cao_Van_Hanh.md` | 109 | 2144 | `32113c3f62ce95d2b6d5c4beb18532df7778852f72a2e50937e777225da22ae5` |
| 47 | `BD/diagram/SEQUENCE/14. Study2Work_Study_SEQ_RBAC_Audit.md` | 121 | 2672 | `3c72d1eb915db97f1735f9dafff0c9bec7b2c0efb4f1916a1225124cc35419b1` |
| 48 | `BD/diagram/UC/01. Study2Work_Study_Diagram_UC_Tong_Quan.md` | 131 | 4618 | `4cc3b127b7b0e84f3aa4930f2b9c3e26e2cd8cc8a1c2410bc387de1a36958afa` |