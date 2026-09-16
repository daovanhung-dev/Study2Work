# Work seed accounts

> Dữ liệu synthetic dành cho development/QA. Mật khẩu bên dưới là plaintext vì cơ chế đăng nhập hiện tại của Work đang so sánh trực tiếp trường `matkhau`.
> Không dùng các tài khoản này cho production. Tài liệu không chứa Neon connection string hoặc credential của database.

## Thông tin seed

| Trường | Giá trị |
| --- | --- |
| Seed version | work-accounts-v1 |
| Generated at | 2026-09-16T14:45:51.659Z |
| Database | neondb / public |
| Student namespace | seed.student.001..100@study2work.dev |
| Business namespace | seed.business.01..10@study2work.dev |
| Sinh viên | 100 |
| CV | 100 |
| Doanh nghiệp | 10 |
| JD | 40 |
| Ngành nghề | 10 |
| Rerun policy | Additive idempotent; chỉ upsert namespace seed, không xóa dữ liệu khác |

## Mật khẩu dùng cho QA

- Sinh viên: `WorkStudent@123`
- Doanh nghiệp: `WorkBusiness@123`

## Tài khoản sinh viên

| STT | ID | Họ tên | Email | Mật khẩu | Chuyên ngành | CV ID |
| ---: | ---: | --- | --- | --- | --- | ---: |
| 1 | 9 | Nguyễn Minh An | seed.student.001@study2work.dev | `WorkStudent@123` | Công nghệ thông tin | 4 |
| 2 | 10 | Nguyễn Ngọc Bình | seed.student.002@study2work.dev | `WorkStudent@123` | Công nghệ thông tin | 5 |
| 3 | 11 | Nguyễn Gia Chi | seed.student.003@study2work.dev | `WorkStudent@123` | Công nghệ thông tin | 6 |
| 4 | 12 | Nguyễn Thanh Dũng | seed.student.004@study2work.dev | `WorkStudent@123` | Công nghệ thông tin | 7 |
| 5 | 13 | Nguyễn Khánh Hà | seed.student.005@study2work.dev | `WorkStudent@123` | Công nghệ thông tin | 8 |
| 6 | 14 | Nguyễn Thu Khang | seed.student.006@study2work.dev | `WorkStudent@123` | Công nghệ thông tin | 9 |
| 7 | 15 | Nguyễn Đức Linh | seed.student.007@study2work.dev | `WorkStudent@123` | Công nghệ thông tin | 10 |
| 8 | 16 | Nguyễn Quỳnh Nam | seed.student.008@study2work.dev | `WorkStudent@123` | Công nghệ thông tin | 11 |
| 9 | 17 | Nguyễn Hải Phương | seed.student.009@study2work.dev | `WorkStudent@123` | Công nghệ thông tin | 12 |
| 10 | 18 | Nguyễn Bảo Quân | seed.student.010@study2work.dev | `WorkStudent@123` | Công nghệ thông tin | 13 |
| 11 | 19 | Trần Minh An | seed.student.011@study2work.dev | `WorkStudent@123` | Tài chính - Ngân hàng | 14 |
| 12 | 20 | Trần Ngọc Bình | seed.student.012@study2work.dev | `WorkStudent@123` | Tài chính - Ngân hàng | 15 |
| 13 | 21 | Trần Gia Chi | seed.student.013@study2work.dev | `WorkStudent@123` | Tài chính - Ngân hàng | 16 |
| 14 | 22 | Trần Thanh Dũng | seed.student.014@study2work.dev | `WorkStudent@123` | Tài chính - Ngân hàng | 17 |
| 15 | 23 | Trần Khánh Hà | seed.student.015@study2work.dev | `WorkStudent@123` | Tài chính - Ngân hàng | 18 |
| 16 | 24 | Trần Thu Khang | seed.student.016@study2work.dev | `WorkStudent@123` | Tài chính - Ngân hàng | 19 |
| 17 | 25 | Trần Đức Linh | seed.student.017@study2work.dev | `WorkStudent@123` | Tài chính - Ngân hàng | 20 |
| 18 | 26 | Trần Quỳnh Nam | seed.student.018@study2work.dev | `WorkStudent@123` | Tài chính - Ngân hàng | 21 |
| 19 | 27 | Trần Hải Phương | seed.student.019@study2work.dev | `WorkStudent@123` | Tài chính - Ngân hàng | 22 |
| 20 | 28 | Trần Bảo Quân | seed.student.020@study2work.dev | `WorkStudent@123` | Tài chính - Ngân hàng | 23 |
| 21 | 29 | Lê Minh An | seed.student.021@study2work.dev | `WorkStudent@123` | Marketing - Truyền thông | 24 |
| 22 | 30 | Lê Ngọc Bình | seed.student.022@study2work.dev | `WorkStudent@123` | Marketing - Truyền thông | 25 |
| 23 | 31 | Lê Gia Chi | seed.student.023@study2work.dev | `WorkStudent@123` | Marketing - Truyền thông | 26 |
| 24 | 32 | Lê Thanh Dũng | seed.student.024@study2work.dev | `WorkStudent@123` | Marketing - Truyền thông | 27 |
| 25 | 33 | Lê Khánh Hà | seed.student.025@study2work.dev | `WorkStudent@123` | Marketing - Truyền thông | 28 |
| 26 | 34 | Lê Thu Khang | seed.student.026@study2work.dev | `WorkStudent@123` | Marketing - Truyền thông | 29 |
| 27 | 35 | Lê Đức Linh | seed.student.027@study2work.dev | `WorkStudent@123` | Marketing - Truyền thông | 30 |
| 28 | 36 | Lê Quỳnh Nam | seed.student.028@study2work.dev | `WorkStudent@123` | Marketing - Truyền thông | 31 |
| 29 | 37 | Lê Hải Phương | seed.student.029@study2work.dev | `WorkStudent@123` | Marketing - Truyền thông | 32 |
| 30 | 38 | Lê Bảo Quân | seed.student.030@study2work.dev | `WorkStudent@123` | Marketing - Truyền thông | 33 |
| 31 | 39 | Phạm Minh An | seed.student.031@study2work.dev | `WorkStudent@123` | Thương mại điện tử | 34 |
| 32 | 40 | Phạm Ngọc Bình | seed.student.032@study2work.dev | `WorkStudent@123` | Thương mại điện tử | 35 |
| 33 | 41 | Phạm Gia Chi | seed.student.033@study2work.dev | `WorkStudent@123` | Thương mại điện tử | 36 |
| 34 | 42 | Phạm Thanh Dũng | seed.student.034@study2work.dev | `WorkStudent@123` | Thương mại điện tử | 37 |
| 35 | 43 | Phạm Khánh Hà | seed.student.035@study2work.dev | `WorkStudent@123` | Thương mại điện tử | 38 |
| 36 | 44 | Phạm Thu Khang | seed.student.036@study2work.dev | `WorkStudent@123` | Thương mại điện tử | 39 |
| 37 | 45 | Phạm Đức Linh | seed.student.037@study2work.dev | `WorkStudent@123` | Thương mại điện tử | 40 |
| 38 | 46 | Phạm Quỳnh Nam | seed.student.038@study2work.dev | `WorkStudent@123` | Thương mại điện tử | 41 |
| 39 | 47 | Phạm Hải Phương | seed.student.039@study2work.dev | `WorkStudent@123` | Thương mại điện tử | 42 |
| 40 | 48 | Phạm Bảo Quân | seed.student.040@study2work.dev | `WorkStudent@123` | Thương mại điện tử | 43 |
| 41 | 49 | Hoàng Minh An | seed.student.041@study2work.dev | `WorkStudent@123` | Giáo dục | 44 |
| 42 | 50 | Hoàng Ngọc Bình | seed.student.042@study2work.dev | `WorkStudent@123` | Giáo dục | 45 |
| 43 | 51 | Hoàng Gia Chi | seed.student.043@study2work.dev | `WorkStudent@123` | Giáo dục | 46 |
| 44 | 52 | Hoàng Thanh Dũng | seed.student.044@study2work.dev | `WorkStudent@123` | Giáo dục | 47 |
| 45 | 53 | Hoàng Khánh Hà | seed.student.045@study2work.dev | `WorkStudent@123` | Giáo dục | 48 |
| 46 | 54 | Hoàng Thu Khang | seed.student.046@study2work.dev | `WorkStudent@123` | Giáo dục | 49 |
| 47 | 55 | Hoàng Đức Linh | seed.student.047@study2work.dev | `WorkStudent@123` | Giáo dục | 50 |
| 48 | 56 | Hoàng Quỳnh Nam | seed.student.048@study2work.dev | `WorkStudent@123` | Giáo dục | 51 |
| 49 | 57 | Hoàng Hải Phương | seed.student.049@study2work.dev | `WorkStudent@123` | Giáo dục | 52 |
| 50 | 58 | Hoàng Bảo Quân | seed.student.050@study2work.dev | `WorkStudent@123` | Giáo dục | 53 |
| 51 | 59 | Huỳnh Minh An | seed.student.051@study2work.dev | `WorkStudent@123` | Logistics | 54 |
| 52 | 60 | Huỳnh Ngọc Bình | seed.student.052@study2work.dev | `WorkStudent@123` | Logistics | 55 |
| 53 | 61 | Huỳnh Gia Chi | seed.student.053@study2work.dev | `WorkStudent@123` | Logistics | 56 |
| 54 | 62 | Huỳnh Thanh Dũng | seed.student.054@study2work.dev | `WorkStudent@123` | Logistics | 57 |
| 55 | 63 | Huỳnh Khánh Hà | seed.student.055@study2work.dev | `WorkStudent@123` | Logistics | 58 |
| 56 | 64 | Huỳnh Thu Khang | seed.student.056@study2work.dev | `WorkStudent@123` | Logistics | 59 |
| 57 | 65 | Huỳnh Đức Linh | seed.student.057@study2work.dev | `WorkStudent@123` | Logistics | 60 |
| 58 | 66 | Huỳnh Quỳnh Nam | seed.student.058@study2work.dev | `WorkStudent@123` | Logistics | 61 |
| 59 | 67 | Huỳnh Hải Phương | seed.student.059@study2work.dev | `WorkStudent@123` | Logistics | 62 |
| 60 | 68 | Huỳnh Bảo Quân | seed.student.060@study2work.dev | `WorkStudent@123` | Logistics | 63 |
| 61 | 69 | Phan Minh An | seed.student.061@study2work.dev | `WorkStudent@123` | Sản xuất | 64 |
| 62 | 70 | Phan Ngọc Bình | seed.student.062@study2work.dev | `WorkStudent@123` | Sản xuất | 65 |
| 63 | 71 | Phan Gia Chi | seed.student.063@study2work.dev | `WorkStudent@123` | Sản xuất | 66 |
| 64 | 72 | Phan Thanh Dũng | seed.student.064@study2work.dev | `WorkStudent@123` | Sản xuất | 67 |
| 65 | 73 | Phan Khánh Hà | seed.student.065@study2work.dev | `WorkStudent@123` | Sản xuất | 68 |
| 66 | 74 | Phan Thu Khang | seed.student.066@study2work.dev | `WorkStudent@123` | Sản xuất | 69 |
| 67 | 75 | Phan Đức Linh | seed.student.067@study2work.dev | `WorkStudent@123` | Sản xuất | 70 |
| 68 | 76 | Phan Quỳnh Nam | seed.student.068@study2work.dev | `WorkStudent@123` | Sản xuất | 71 |
| 69 | 77 | Phan Hải Phương | seed.student.069@study2work.dev | `WorkStudent@123` | Sản xuất | 72 |
| 70 | 78 | Phan Bảo Quân | seed.student.070@study2work.dev | `WorkStudent@123` | Sản xuất | 73 |
| 71 | 79 | Vũ Minh An | seed.student.071@study2work.dev | `WorkStudent@123` | Y tế - Chăm sóc sức khỏe | 74 |
| 72 | 80 | Vũ Ngọc Bình | seed.student.072@study2work.dev | `WorkStudent@123` | Y tế - Chăm sóc sức khỏe | 75 |
| 73 | 81 | Vũ Gia Chi | seed.student.073@study2work.dev | `WorkStudent@123` | Y tế - Chăm sóc sức khỏe | 76 |
| 74 | 82 | Vũ Thanh Dũng | seed.student.074@study2work.dev | `WorkStudent@123` | Y tế - Chăm sóc sức khỏe | 77 |
| 75 | 83 | Vũ Khánh Hà | seed.student.075@study2work.dev | `WorkStudent@123` | Y tế - Chăm sóc sức khỏe | 78 |
| 76 | 84 | Vũ Thu Khang | seed.student.076@study2work.dev | `WorkStudent@123` | Y tế - Chăm sóc sức khỏe | 79 |
| 77 | 85 | Vũ Đức Linh | seed.student.077@study2work.dev | `WorkStudent@123` | Y tế - Chăm sóc sức khỏe | 80 |
| 78 | 86 | Vũ Quỳnh Nam | seed.student.078@study2work.dev | `WorkStudent@123` | Y tế - Chăm sóc sức khỏe | 81 |
| 79 | 87 | Vũ Hải Phương | seed.student.079@study2work.dev | `WorkStudent@123` | Y tế - Chăm sóc sức khỏe | 82 |
| 80 | 88 | Vũ Bảo Quân | seed.student.080@study2work.dev | `WorkStudent@123` | Y tế - Chăm sóc sức khỏe | 83 |
| 81 | 89 | Võ Minh An | seed.student.081@study2work.dev | `WorkStudent@123` | Du lịch - Khách sạn | 84 |
| 82 | 90 | Võ Ngọc Bình | seed.student.082@study2work.dev | `WorkStudent@123` | Du lịch - Khách sạn | 85 |
| 83 | 91 | Võ Gia Chi | seed.student.083@study2work.dev | `WorkStudent@123` | Du lịch - Khách sạn | 86 |
| 84 | 92 | Võ Thanh Dũng | seed.student.084@study2work.dev | `WorkStudent@123` | Du lịch - Khách sạn | 87 |
| 85 | 93 | Võ Khánh Hà | seed.student.085@study2work.dev | `WorkStudent@123` | Du lịch - Khách sạn | 88 |
| 86 | 94 | Võ Thu Khang | seed.student.086@study2work.dev | `WorkStudent@123` | Du lịch - Khách sạn | 89 |
| 87 | 95 | Võ Đức Linh | seed.student.087@study2work.dev | `WorkStudent@123` | Du lịch - Khách sạn | 90 |
| 88 | 96 | Võ Quỳnh Nam | seed.student.088@study2work.dev | `WorkStudent@123` | Du lịch - Khách sạn | 91 |
| 89 | 97 | Võ Hải Phương | seed.student.089@study2work.dev | `WorkStudent@123` | Du lịch - Khách sạn | 92 |
| 90 | 98 | Võ Bảo Quân | seed.student.090@study2work.dev | `WorkStudent@123` | Du lịch - Khách sạn | 93 |
| 91 | 99 | Đặng Minh An | seed.student.091@study2work.dev | `WorkStudent@123` | Năng lượng xanh | 94 |
| 92 | 100 | Đặng Ngọc Bình | seed.student.092@study2work.dev | `WorkStudent@123` | Năng lượng xanh | 95 |
| 93 | 101 | Đặng Gia Chi | seed.student.093@study2work.dev | `WorkStudent@123` | Năng lượng xanh | 96 |
| 94 | 102 | Đặng Thanh Dũng | seed.student.094@study2work.dev | `WorkStudent@123` | Năng lượng xanh | 97 |
| 95 | 103 | Đặng Khánh Hà | seed.student.095@study2work.dev | `WorkStudent@123` | Năng lượng xanh | 98 |
| 96 | 104 | Đặng Thu Khang | seed.student.096@study2work.dev | `WorkStudent@123` | Năng lượng xanh | 99 |
| 97 | 105 | Đặng Đức Linh | seed.student.097@study2work.dev | `WorkStudent@123` | Năng lượng xanh | 100 |
| 98 | 106 | Đặng Quỳnh Nam | seed.student.098@study2work.dev | `WorkStudent@123` | Năng lượng xanh | 101 |
| 99 | 107 | Đặng Hải Phương | seed.student.099@study2work.dev | `WorkStudent@123` | Năng lượng xanh | 102 |
| 100 | 108 | Đặng Bảo Quân | seed.student.100@study2work.dev | `WorkStudent@123` | Năng lượng xanh | 103 |

### Sinh viên 001 — Nguyễn Minh An

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 9 |
| Họ tên | Nguyễn Minh An |
| Email | seed.student.001@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Công nghệ thông tin |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 4 |
| Họ tên | Nguyễn Minh An |
| Ngày sinh | 1998-01-05T00:00:00.000Z |
| Giới tính | Nam |
| Email CV | seed.student.001@study2work.dev |
| Số điện thoại | 0903000001 |
| Địa chỉ | Đà Nẵng, Việt Nam |
| Vị trí | Frontend React Developer |
| Ngành | Công nghệ thông tin |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Công nghệ thông tin với vai trò Frontend React Developer. |
| Học vấn | Đại học chuyên ngành CNTT hoặc tương đương |
| Kinh nghiệm | Fresher; hoàn thành dự án học thuật và 6 tháng thực tập. |
| Kỹ năng | React, TypeScript, Node.js, SQL |
| Ngoại ngữ | Tiếng Anh B1 |
| Chứng chỉ | AWS Cloud Practitioner hoặc chứng chỉ tương đương |
| Dự án | Dự án portfolio 001: xây dựng giải pháp thử nghiệm cho nền tảng số. |
| Giải thưởng | Giải thưởng đồ án cấp khoa |
| Hoạt động | CLB Lập trình và Công nghệ; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-001","linkedin":"https://www.linkedin.com/in/seed-student-001"} |
| Portfolio | https://portfolio.study2work.dev/student-001 |
| Mức lương mong muốn | 15-30 triệu VNĐ/tháng |
| sinhvien_id | 9 |
| created_at | 2026-09-16T14:42:59.160Z |

### Sinh viên 002 — Nguyễn Ngọc Bình

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 10 |
| Họ tên | Nguyễn Ngọc Bình |
| Email | seed.student.002@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Công nghệ thông tin |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 5 |
| Họ tên | Nguyễn Ngọc Bình |
| Ngày sinh | 1999-01-06T00:00:00.000Z |
| Giới tính | Nữ |
| Email CV | seed.student.002@study2work.dev |
| Số điện thoại | 0903000002 |
| Địa chỉ | Đà Nẵng, Việt Nam |
| Vị trí | Backend Node.js Developer |
| Ngành | Công nghệ thông tin |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Công nghệ thông tin với vai trò Backend Node.js Developer. |
| Học vấn | Đại học chuyên ngành CNTT hoặc tương đương |
| Kinh nghiệm | 1 năm kinh nghiệm liên quan đến nền tảng số. |
| Kỹ năng | React, TypeScript, Node.js, SQL |
| Ngoại ngữ | Tiếng Anh B2 |
| Chứng chỉ | AWS Cloud Practitioner hoặc chứng chỉ tương đương |
| Dự án | Dự án portfolio 002: xây dựng giải pháp thử nghiệm cho nền tảng số. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Lập trình và Công nghệ; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-002","linkedin":"https://www.linkedin.com/in/seed-student-002"} |
| Portfolio | https://portfolio.study2work.dev/student-002 |
| Mức lương mong muốn | 15-30 triệu VNĐ/tháng |
| sinhvien_id | 10 |
| created_at | 2026-09-16T14:42:59.662Z |

### Sinh viên 003 — Nguyễn Gia Chi

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 11 |
| Họ tên | Nguyễn Gia Chi |
| Email | seed.student.003@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Công nghệ thông tin |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 6 |
| Họ tên | Nguyễn Gia Chi |
| Ngày sinh | 2000-01-07T00:00:00.000Z |
| Giới tính | Nam |
| Email CV | seed.student.003@study2work.dev |
| Số điện thoại | 0903000003 |
| Địa chỉ | Đà Nẵng, Việt Nam |
| Vị trí | QA Automation Engineer |
| Ngành | Công nghệ thông tin |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Công nghệ thông tin với vai trò QA Automation Engineer. |
| Học vấn | Đại học chuyên ngành CNTT hoặc tương đương |
| Kinh nghiệm | 2 năm kinh nghiệm thực tế trong lĩnh vực nền tảng số. |
| Kỹ năng | React, TypeScript, Node.js, SQL |
| Ngoại ngữ | Tiếng Anh giao tiếp |
| Chứng chỉ | AWS Cloud Practitioner hoặc chứng chỉ tương đương |
| Dự án | Dự án portfolio 003: xây dựng giải pháp thử nghiệm cho nền tảng số. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Lập trình và Công nghệ; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-003","linkedin":"https://www.linkedin.com/in/seed-student-003"} |
| Portfolio | https://portfolio.study2work.dev/student-003 |
| Mức lương mong muốn | 15-30 triệu VNĐ/tháng |
| sinhvien_id | 11 |
| created_at | 2026-09-16T14:43:00.173Z |

### Sinh viên 004 — Nguyễn Thanh Dũng

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 12 |
| Họ tên | Nguyễn Thanh Dũng |
| Email | seed.student.004@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Công nghệ thông tin |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 7 |
| Họ tên | Nguyễn Thanh Dũng |
| Ngày sinh | 2001-01-08T00:00:00.000Z |
| Giới tính | Nữ |
| Email CV | seed.student.004@study2work.dev |
| Số điện thoại | 0903000004 |
| Địa chỉ | Đà Nẵng, Việt Nam |
| Vị trí | Product Designer |
| Ngành | Công nghệ thông tin |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Công nghệ thông tin với vai trò Product Designer. |
| Học vấn | Đại học chuyên ngành CNTT hoặc tương đương |
| Kinh nghiệm | Fresher; hoàn thành dự án học thuật và 6 tháng thực tập. |
| Kỹ năng | React, TypeScript, Node.js, SQL |
| Ngoại ngữ | Tiếng Anh B1 |
| Chứng chỉ | AWS Cloud Practitioner hoặc chứng chỉ tương đương |
| Dự án | Dự án portfolio 004: xây dựng giải pháp thử nghiệm cho nền tảng số. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Lập trình và Công nghệ; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-004","linkedin":"https://www.linkedin.com/in/seed-student-004"} |
| Portfolio | https://portfolio.study2work.dev/student-004 |
| Mức lương mong muốn | 15-30 triệu VNĐ/tháng |
| sinhvien_id | 12 |
| created_at | 2026-09-16T14:43:00.692Z |

### Sinh viên 005 — Nguyễn Khánh Hà

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 13 |
| Họ tên | Nguyễn Khánh Hà |
| Email | seed.student.005@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Công nghệ thông tin |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 8 |
| Họ tên | Nguyễn Khánh Hà |
| Ngày sinh | 2002-01-09T00:00:00.000Z |
| Giới tính | Nam |
| Email CV | seed.student.005@study2work.dev |
| Số điện thoại | 0903000005 |
| Địa chỉ | Đà Nẵng, Việt Nam |
| Vị trí | Frontend React Developer |
| Ngành | Công nghệ thông tin |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Công nghệ thông tin với vai trò Frontend React Developer. |
| Học vấn | Đại học chuyên ngành CNTT hoặc tương đương |
| Kinh nghiệm | 1 năm kinh nghiệm liên quan đến nền tảng số. |
| Kỹ năng | React, TypeScript, Node.js, SQL |
| Ngoại ngữ | Tiếng Anh B2 |
| Chứng chỉ | AWS Cloud Practitioner hoặc chứng chỉ tương đương |
| Dự án | Dự án portfolio 005: xây dựng giải pháp thử nghiệm cho nền tảng số. |
| Giải thưởng | Giải thưởng đồ án cấp khoa |
| Hoạt động | CLB Lập trình và Công nghệ; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-005","linkedin":"https://www.linkedin.com/in/seed-student-005"} |
| Portfolio | https://portfolio.study2work.dev/student-005 |
| Mức lương mong muốn | 15-30 triệu VNĐ/tháng |
| sinhvien_id | 13 |
| created_at | 2026-09-16T14:43:01.206Z |

### Sinh viên 006 — Nguyễn Thu Khang

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 14 |
| Họ tên | Nguyễn Thu Khang |
| Email | seed.student.006@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Công nghệ thông tin |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 9 |
| Họ tên | Nguyễn Thu Khang |
| Ngày sinh | 1998-01-10T00:00:00.000Z |
| Giới tính | Nữ |
| Email CV | seed.student.006@study2work.dev |
| Số điện thoại | 0903000006 |
| Địa chỉ | Đà Nẵng, Việt Nam |
| Vị trí | Backend Node.js Developer |
| Ngành | Công nghệ thông tin |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Công nghệ thông tin với vai trò Backend Node.js Developer. |
| Học vấn | Đại học chuyên ngành CNTT hoặc tương đương |
| Kinh nghiệm | 2 năm kinh nghiệm thực tế trong lĩnh vực nền tảng số. |
| Kỹ năng | React, TypeScript, Node.js, SQL |
| Ngoại ngữ | Tiếng Anh giao tiếp |
| Chứng chỉ | AWS Cloud Practitioner hoặc chứng chỉ tương đương |
| Dự án | Dự án portfolio 006: xây dựng giải pháp thử nghiệm cho nền tảng số. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Lập trình và Công nghệ; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-006","linkedin":"https://www.linkedin.com/in/seed-student-006"} |
| Portfolio | https://portfolio.study2work.dev/student-006 |
| Mức lương mong muốn | 15-30 triệu VNĐ/tháng |
| sinhvien_id | 14 |
| created_at | 2026-09-16T14:43:01.709Z |

### Sinh viên 007 — Nguyễn Đức Linh

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 15 |
| Họ tên | Nguyễn Đức Linh |
| Email | seed.student.007@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Công nghệ thông tin |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 10 |
| Họ tên | Nguyễn Đức Linh |
| Ngày sinh | 1999-01-11T00:00:00.000Z |
| Giới tính | Nam |
| Email CV | seed.student.007@study2work.dev |
| Số điện thoại | 0903000007 |
| Địa chỉ | Đà Nẵng, Việt Nam |
| Vị trí | QA Automation Engineer |
| Ngành | Công nghệ thông tin |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Công nghệ thông tin với vai trò QA Automation Engineer. |
| Học vấn | Đại học chuyên ngành CNTT hoặc tương đương |
| Kinh nghiệm | Fresher; hoàn thành dự án học thuật và 6 tháng thực tập. |
| Kỹ năng | React, TypeScript, Node.js, SQL |
| Ngoại ngữ | Tiếng Anh B1 |
| Chứng chỉ | AWS Cloud Practitioner hoặc chứng chỉ tương đương |
| Dự án | Dự án portfolio 007: xây dựng giải pháp thử nghiệm cho nền tảng số. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Lập trình và Công nghệ; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-007","linkedin":"https://www.linkedin.com/in/seed-student-007"} |
| Portfolio | https://portfolio.study2work.dev/student-007 |
| Mức lương mong muốn | 15-30 triệu VNĐ/tháng |
| sinhvien_id | 15 |
| created_at | 2026-09-16T14:43:02.222Z |

### Sinh viên 008 — Nguyễn Quỳnh Nam

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 16 |
| Họ tên | Nguyễn Quỳnh Nam |
| Email | seed.student.008@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Công nghệ thông tin |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 11 |
| Họ tên | Nguyễn Quỳnh Nam |
| Ngày sinh | 2000-01-12T00:00:00.000Z |
| Giới tính | Nữ |
| Email CV | seed.student.008@study2work.dev |
| Số điện thoại | 0903000008 |
| Địa chỉ | Đà Nẵng, Việt Nam |
| Vị trí | Product Designer |
| Ngành | Công nghệ thông tin |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Công nghệ thông tin với vai trò Product Designer. |
| Học vấn | Đại học chuyên ngành CNTT hoặc tương đương |
| Kinh nghiệm | 1 năm kinh nghiệm liên quan đến nền tảng số. |
| Kỹ năng | React, TypeScript, Node.js, SQL |
| Ngoại ngữ | Tiếng Anh B2 |
| Chứng chỉ | AWS Cloud Practitioner hoặc chứng chỉ tương đương |
| Dự án | Dự án portfolio 008: xây dựng giải pháp thử nghiệm cho nền tảng số. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Lập trình và Công nghệ; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-008","linkedin":"https://www.linkedin.com/in/seed-student-008"} |
| Portfolio | https://portfolio.study2work.dev/student-008 |
| Mức lương mong muốn | 15-30 triệu VNĐ/tháng |
| sinhvien_id | 16 |
| created_at | 2026-09-16T14:43:02.735Z |

### Sinh viên 009 — Nguyễn Hải Phương

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 17 |
| Họ tên | Nguyễn Hải Phương |
| Email | seed.student.009@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Công nghệ thông tin |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 12 |
| Họ tên | Nguyễn Hải Phương |
| Ngày sinh | 2001-01-13T00:00:00.000Z |
| Giới tính | Nam |
| Email CV | seed.student.009@study2work.dev |
| Số điện thoại | 0903000009 |
| Địa chỉ | Đà Nẵng, Việt Nam |
| Vị trí | Frontend React Developer |
| Ngành | Công nghệ thông tin |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Công nghệ thông tin với vai trò Frontend React Developer. |
| Học vấn | Đại học chuyên ngành CNTT hoặc tương đương |
| Kinh nghiệm | 2 năm kinh nghiệm thực tế trong lĩnh vực nền tảng số. |
| Kỹ năng | React, TypeScript, Node.js, SQL |
| Ngoại ngữ | Tiếng Anh giao tiếp |
| Chứng chỉ | AWS Cloud Practitioner hoặc chứng chỉ tương đương |
| Dự án | Dự án portfolio 009: xây dựng giải pháp thử nghiệm cho nền tảng số. |
| Giải thưởng | Giải thưởng đồ án cấp khoa |
| Hoạt động | CLB Lập trình và Công nghệ; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-009","linkedin":"https://www.linkedin.com/in/seed-student-009"} |
| Portfolio | https://portfolio.study2work.dev/student-009 |
| Mức lương mong muốn | 15-30 triệu VNĐ/tháng |
| sinhvien_id | 17 |
| created_at | 2026-09-16T14:43:03.246Z |

### Sinh viên 010 — Nguyễn Bảo Quân

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 18 |
| Họ tên | Nguyễn Bảo Quân |
| Email | seed.student.010@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Công nghệ thông tin |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 13 |
| Họ tên | Nguyễn Bảo Quân |
| Ngày sinh | 2002-01-14T00:00:00.000Z |
| Giới tính | Nữ |
| Email CV | seed.student.010@study2work.dev |
| Số điện thoại | 0903000010 |
| Địa chỉ | Đà Nẵng, Việt Nam |
| Vị trí | Backend Node.js Developer |
| Ngành | Công nghệ thông tin |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Công nghệ thông tin với vai trò Backend Node.js Developer. |
| Học vấn | Đại học chuyên ngành CNTT hoặc tương đương |
| Kinh nghiệm | Fresher; hoàn thành dự án học thuật và 6 tháng thực tập. |
| Kỹ năng | React, TypeScript, Node.js, SQL |
| Ngoại ngữ | Tiếng Anh B1 |
| Chứng chỉ | AWS Cloud Practitioner hoặc chứng chỉ tương đương |
| Dự án | Dự án portfolio 010: xây dựng giải pháp thử nghiệm cho nền tảng số. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Lập trình và Công nghệ; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-010","linkedin":"https://www.linkedin.com/in/seed-student-010"} |
| Portfolio | https://portfolio.study2work.dev/student-010 |
| Mức lương mong muốn | 15-30 triệu VNĐ/tháng |
| sinhvien_id | 18 |
| created_at | 2026-09-16T14:43:03.761Z |

### Sinh viên 011 — Trần Minh An

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 19 |
| Họ tên | Trần Minh An |
| Email | seed.student.011@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Tài chính - Ngân hàng |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 14 |
| Họ tên | Trần Minh An |
| Ngày sinh | 1998-02-05T00:00:00.000Z |
| Giới tính | Nam |
| Email CV | seed.student.011@study2work.dev |
| Số điện thoại | 0903000011 |
| Địa chỉ | Hà Nội, Việt Nam |
| Vị trí | Chuyên viên Phân tích Tài chính |
| Ngành | Tài chính - Ngân hàng |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Tài chính - Ngân hàng với vai trò Chuyên viên Phân tích Tài chính. |
| Học vấn | Đại học chuyên ngành Tài chính, Kinh tế hoặc CNTT |
| Kinh nghiệm | Fresher; hoàn thành dự án học thuật và 6 tháng thực tập. |
| Kỹ năng | Excel, SQL, Python, phân tích dữ liệu |
| Ngoại ngữ | Tiếng Anh B1 |
| Chứng chỉ | CFA level 1, FRM hoặc chứng chỉ phân tích dữ liệu |
| Dự án | Dự án portfolio 011: xây dựng giải pháp thử nghiệm cho dịch vụ tài chính số. |
| Giải thưởng | Giải thưởng đồ án cấp khoa |
| Hoạt động | CLB Tài chính và Phân tích; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-011","linkedin":"https://www.linkedin.com/in/seed-student-011"} |
| Portfolio | https://portfolio.study2work.dev/student-011 |
| Mức lương mong muốn | 12-25 triệu VNĐ/tháng |
| sinhvien_id | 19 |
| created_at | 2026-09-16T14:43:04.272Z |

### Sinh viên 012 — Trần Ngọc Bình

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 20 |
| Họ tên | Trần Ngọc Bình |
| Email | seed.student.012@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Tài chính - Ngân hàng |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 15 |
| Họ tên | Trần Ngọc Bình |
| Ngày sinh | 1999-02-06T00:00:00.000Z |
| Giới tính | Nữ |
| Email CV | seed.student.012@study2work.dev |
| Số điện thoại | 0903000012 |
| Địa chỉ | Hà Nội, Việt Nam |
| Vị trí | Banking Integration Developer |
| Ngành | Tài chính - Ngân hàng |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Tài chính - Ngân hàng với vai trò Banking Integration Developer. |
| Học vấn | Đại học chuyên ngành Tài chính, Kinh tế hoặc CNTT |
| Kinh nghiệm | 1 năm kinh nghiệm liên quan đến dịch vụ tài chính số. |
| Kỹ năng | Excel, SQL, Python, phân tích dữ liệu |
| Ngoại ngữ | Tiếng Anh B2 |
| Chứng chỉ | CFA level 1, FRM hoặc chứng chỉ phân tích dữ liệu |
| Dự án | Dự án portfolio 012: xây dựng giải pháp thử nghiệm cho dịch vụ tài chính số. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Tài chính và Phân tích; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-012","linkedin":"https://www.linkedin.com/in/seed-student-012"} |
| Portfolio | https://portfolio.study2work.dev/student-012 |
| Mức lương mong muốn | 12-25 triệu VNĐ/tháng |
| sinhvien_id | 20 |
| created_at | 2026-09-16T14:43:04.781Z |

### Sinh viên 013 — Trần Gia Chi

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 21 |
| Họ tên | Trần Gia Chi |
| Email | seed.student.013@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Tài chính - Ngân hàng |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 16 |
| Họ tên | Trần Gia Chi |
| Ngày sinh | 2000-02-07T00:00:00.000Z |
| Giới tính | Nam |
| Email CV | seed.student.013@study2work.dev |
| Số điện thoại | 0903000013 |
| Địa chỉ | Hà Nội, Việt Nam |
| Vị trí | Data Analyst |
| Ngành | Tài chính - Ngân hàng |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Tài chính - Ngân hàng với vai trò Data Analyst. |
| Học vấn | Đại học chuyên ngành Tài chính, Kinh tế hoặc CNTT |
| Kinh nghiệm | 2 năm kinh nghiệm thực tế trong lĩnh vực dịch vụ tài chính số. |
| Kỹ năng | Excel, SQL, Python, phân tích dữ liệu |
| Ngoại ngữ | Tiếng Anh giao tiếp |
| Chứng chỉ | CFA level 1, FRM hoặc chứng chỉ phân tích dữ liệu |
| Dự án | Dự án portfolio 013: xây dựng giải pháp thử nghiệm cho dịch vụ tài chính số. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Tài chính và Phân tích; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-013","linkedin":"https://www.linkedin.com/in/seed-student-013"} |
| Portfolio | https://portfolio.study2work.dev/student-013 |
| Mức lương mong muốn | 12-25 triệu VNĐ/tháng |
| sinhvien_id | 21 |
| created_at | 2026-09-16T14:43:05.293Z |

### Sinh viên 014 — Trần Thanh Dũng

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 22 |
| Họ tên | Trần Thanh Dũng |
| Email | seed.student.014@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Tài chính - Ngân hàng |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 17 |
| Họ tên | Trần Thanh Dũng |
| Ngày sinh | 2001-02-08T00:00:00.000Z |
| Giới tính | Nữ |
| Email CV | seed.student.014@study2work.dev |
| Số điện thoại | 0903000014 |
| Địa chỉ | Hà Nội, Việt Nam |
| Vị trí | Risk & Compliance Specialist |
| Ngành | Tài chính - Ngân hàng |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Tài chính - Ngân hàng với vai trò Risk & Compliance Specialist. |
| Học vấn | Đại học chuyên ngành Tài chính, Kinh tế hoặc CNTT |
| Kinh nghiệm | Fresher; hoàn thành dự án học thuật và 6 tháng thực tập. |
| Kỹ năng | Excel, SQL, Python, phân tích dữ liệu |
| Ngoại ngữ | Tiếng Anh B1 |
| Chứng chỉ | CFA level 1, FRM hoặc chứng chỉ phân tích dữ liệu |
| Dự án | Dự án portfolio 014: xây dựng giải pháp thử nghiệm cho dịch vụ tài chính số. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Tài chính và Phân tích; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-014","linkedin":"https://www.linkedin.com/in/seed-student-014"} |
| Portfolio | https://portfolio.study2work.dev/student-014 |
| Mức lương mong muốn | 12-25 triệu VNĐ/tháng |
| sinhvien_id | 22 |
| created_at | 2026-09-16T14:43:05.804Z |

### Sinh viên 015 — Trần Khánh Hà

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 23 |
| Họ tên | Trần Khánh Hà |
| Email | seed.student.015@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Tài chính - Ngân hàng |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 18 |
| Họ tên | Trần Khánh Hà |
| Ngày sinh | 2002-02-09T00:00:00.000Z |
| Giới tính | Nam |
| Email CV | seed.student.015@study2work.dev |
| Số điện thoại | 0903000015 |
| Địa chỉ | Hà Nội, Việt Nam |
| Vị trí | Chuyên viên Phân tích Tài chính |
| Ngành | Tài chính - Ngân hàng |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Tài chính - Ngân hàng với vai trò Chuyên viên Phân tích Tài chính. |
| Học vấn | Đại học chuyên ngành Tài chính, Kinh tế hoặc CNTT |
| Kinh nghiệm | 1 năm kinh nghiệm liên quan đến dịch vụ tài chính số. |
| Kỹ năng | Excel, SQL, Python, phân tích dữ liệu |
| Ngoại ngữ | Tiếng Anh B2 |
| Chứng chỉ | CFA level 1, FRM hoặc chứng chỉ phân tích dữ liệu |
| Dự án | Dự án portfolio 015: xây dựng giải pháp thử nghiệm cho dịch vụ tài chính số. |
| Giải thưởng | Giải thưởng đồ án cấp khoa |
| Hoạt động | CLB Tài chính và Phân tích; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-015","linkedin":"https://www.linkedin.com/in/seed-student-015"} |
| Portfolio | https://portfolio.study2work.dev/student-015 |
| Mức lương mong muốn | 12-25 triệu VNĐ/tháng |
| sinhvien_id | 23 |
| created_at | 2026-09-16T14:43:06.319Z |

### Sinh viên 016 — Trần Thu Khang

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 24 |
| Họ tên | Trần Thu Khang |
| Email | seed.student.016@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Tài chính - Ngân hàng |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 19 |
| Họ tên | Trần Thu Khang |
| Ngày sinh | 1998-02-10T00:00:00.000Z |
| Giới tính | Nữ |
| Email CV | seed.student.016@study2work.dev |
| Số điện thoại | 0903000016 |
| Địa chỉ | Hà Nội, Việt Nam |
| Vị trí | Banking Integration Developer |
| Ngành | Tài chính - Ngân hàng |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Tài chính - Ngân hàng với vai trò Banking Integration Developer. |
| Học vấn | Đại học chuyên ngành Tài chính, Kinh tế hoặc CNTT |
| Kinh nghiệm | 2 năm kinh nghiệm thực tế trong lĩnh vực dịch vụ tài chính số. |
| Kỹ năng | Excel, SQL, Python, phân tích dữ liệu |
| Ngoại ngữ | Tiếng Anh giao tiếp |
| Chứng chỉ | CFA level 1, FRM hoặc chứng chỉ phân tích dữ liệu |
| Dự án | Dự án portfolio 016: xây dựng giải pháp thử nghiệm cho dịch vụ tài chính số. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Tài chính và Phân tích; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-016","linkedin":"https://www.linkedin.com/in/seed-student-016"} |
| Portfolio | https://portfolio.study2work.dev/student-016 |
| Mức lương mong muốn | 12-25 triệu VNĐ/tháng |
| sinhvien_id | 24 |
| created_at | 2026-09-16T14:43:06.829Z |

### Sinh viên 017 — Trần Đức Linh

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 25 |
| Họ tên | Trần Đức Linh |
| Email | seed.student.017@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Tài chính - Ngân hàng |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 20 |
| Họ tên | Trần Đức Linh |
| Ngày sinh | 1999-02-11T00:00:00.000Z |
| Giới tính | Nam |
| Email CV | seed.student.017@study2work.dev |
| Số điện thoại | 0903000017 |
| Địa chỉ | Hà Nội, Việt Nam |
| Vị trí | Data Analyst |
| Ngành | Tài chính - Ngân hàng |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Tài chính - Ngân hàng với vai trò Data Analyst. |
| Học vấn | Đại học chuyên ngành Tài chính, Kinh tế hoặc CNTT |
| Kinh nghiệm | Fresher; hoàn thành dự án học thuật và 6 tháng thực tập. |
| Kỹ năng | Excel, SQL, Python, phân tích dữ liệu |
| Ngoại ngữ | Tiếng Anh B1 |
| Chứng chỉ | CFA level 1, FRM hoặc chứng chỉ phân tích dữ liệu |
| Dự án | Dự án portfolio 017: xây dựng giải pháp thử nghiệm cho dịch vụ tài chính số. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Tài chính và Phân tích; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-017","linkedin":"https://www.linkedin.com/in/seed-student-017"} |
| Portfolio | https://portfolio.study2work.dev/student-017 |
| Mức lương mong muốn | 12-25 triệu VNĐ/tháng |
| sinhvien_id | 25 |
| created_at | 2026-09-16T14:43:07.341Z |

### Sinh viên 018 — Trần Quỳnh Nam

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 26 |
| Họ tên | Trần Quỳnh Nam |
| Email | seed.student.018@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Tài chính - Ngân hàng |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 21 |
| Họ tên | Trần Quỳnh Nam |
| Ngày sinh | 2000-02-12T00:00:00.000Z |
| Giới tính | Nữ |
| Email CV | seed.student.018@study2work.dev |
| Số điện thoại | 0903000018 |
| Địa chỉ | Hà Nội, Việt Nam |
| Vị trí | Risk & Compliance Specialist |
| Ngành | Tài chính - Ngân hàng |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Tài chính - Ngân hàng với vai trò Risk & Compliance Specialist. |
| Học vấn | Đại học chuyên ngành Tài chính, Kinh tế hoặc CNTT |
| Kinh nghiệm | 1 năm kinh nghiệm liên quan đến dịch vụ tài chính số. |
| Kỹ năng | Excel, SQL, Python, phân tích dữ liệu |
| Ngoại ngữ | Tiếng Anh B2 |
| Chứng chỉ | CFA level 1, FRM hoặc chứng chỉ phân tích dữ liệu |
| Dự án | Dự án portfolio 018: xây dựng giải pháp thử nghiệm cho dịch vụ tài chính số. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Tài chính và Phân tích; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-018","linkedin":"https://www.linkedin.com/in/seed-student-018"} |
| Portfolio | https://portfolio.study2work.dev/student-018 |
| Mức lương mong muốn | 12-25 triệu VNĐ/tháng |
| sinhvien_id | 26 |
| created_at | 2026-09-16T14:43:07.870Z |

### Sinh viên 019 — Trần Hải Phương

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 27 |
| Họ tên | Trần Hải Phương |
| Email | seed.student.019@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Tài chính - Ngân hàng |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 22 |
| Họ tên | Trần Hải Phương |
| Ngày sinh | 2001-02-13T00:00:00.000Z |
| Giới tính | Nam |
| Email CV | seed.student.019@study2work.dev |
| Số điện thoại | 0903000019 |
| Địa chỉ | Hà Nội, Việt Nam |
| Vị trí | Chuyên viên Phân tích Tài chính |
| Ngành | Tài chính - Ngân hàng |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Tài chính - Ngân hàng với vai trò Chuyên viên Phân tích Tài chính. |
| Học vấn | Đại học chuyên ngành Tài chính, Kinh tế hoặc CNTT |
| Kinh nghiệm | 2 năm kinh nghiệm thực tế trong lĩnh vực dịch vụ tài chính số. |
| Kỹ năng | Excel, SQL, Python, phân tích dữ liệu |
| Ngoại ngữ | Tiếng Anh giao tiếp |
| Chứng chỉ | CFA level 1, FRM hoặc chứng chỉ phân tích dữ liệu |
| Dự án | Dự án portfolio 019: xây dựng giải pháp thử nghiệm cho dịch vụ tài chính số. |
| Giải thưởng | Giải thưởng đồ án cấp khoa |
| Hoạt động | CLB Tài chính và Phân tích; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-019","linkedin":"https://www.linkedin.com/in/seed-student-019"} |
| Portfolio | https://portfolio.study2work.dev/student-019 |
| Mức lương mong muốn | 12-25 triệu VNĐ/tháng |
| sinhvien_id | 27 |
| created_at | 2026-09-16T14:43:08.402Z |

### Sinh viên 020 — Trần Bảo Quân

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 28 |
| Họ tên | Trần Bảo Quân |
| Email | seed.student.020@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Tài chính - Ngân hàng |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 23 |
| Họ tên | Trần Bảo Quân |
| Ngày sinh | 2002-02-14T00:00:00.000Z |
| Giới tính | Nữ |
| Email CV | seed.student.020@study2work.dev |
| Số điện thoại | 0903000020 |
| Địa chỉ | Hà Nội, Việt Nam |
| Vị trí | Banking Integration Developer |
| Ngành | Tài chính - Ngân hàng |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Tài chính - Ngân hàng với vai trò Banking Integration Developer. |
| Học vấn | Đại học chuyên ngành Tài chính, Kinh tế hoặc CNTT |
| Kinh nghiệm | Fresher; hoàn thành dự án học thuật và 6 tháng thực tập. |
| Kỹ năng | Excel, SQL, Python, phân tích dữ liệu |
| Ngoại ngữ | Tiếng Anh B1 |
| Chứng chỉ | CFA level 1, FRM hoặc chứng chỉ phân tích dữ liệu |
| Dự án | Dự án portfolio 020: xây dựng giải pháp thử nghiệm cho dịch vụ tài chính số. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Tài chính và Phân tích; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-020","linkedin":"https://www.linkedin.com/in/seed-student-020"} |
| Portfolio | https://portfolio.study2work.dev/student-020 |
| Mức lương mong muốn | 12-25 triệu VNĐ/tháng |
| sinhvien_id | 28 |
| created_at | 2026-09-16T14:43:08.924Z |

### Sinh viên 021 — Lê Minh An

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 29 |
| Họ tên | Lê Minh An |
| Email | seed.student.021@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Marketing - Truyền thông |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 24 |
| Họ tên | Lê Minh An |
| Ngày sinh | 1998-03-05T00:00:00.000Z |
| Giới tính | Nam |
| Email CV | seed.student.021@study2work.dev |
| Số điện thoại | 0903000021 |
| Địa chỉ | TP. Hồ Chí Minh, Việt Nam |
| Vị trí | Content Marketing Executive |
| Ngành | Marketing - Truyền thông |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Marketing - Truyền thông với vai trò Content Marketing Executive. |
| Học vấn | Đại học chuyên ngành Marketing, Truyền thông hoặc Ngôn ngữ |
| Kinh nghiệm | Fresher; hoàn thành dự án học thuật và 6 tháng thực tập. |
| Kỹ năng | Content, SEO, Meta Ads, Google Analytics |
| Ngoại ngữ | Tiếng Anh B1 |
| Chứng chỉ | Google Analytics hoặc Meta Blueprint |
| Dự án | Dự án portfolio 021: xây dựng giải pháp thử nghiệm cho chiến dịch thương hiệu. |
| Giải thưởng | Giải thưởng đồ án cấp khoa |
| Hoạt động | CLB Truyền thông và Sự kiện; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-021","linkedin":"https://www.linkedin.com/in/seed-student-021"} |
| Portfolio | https://portfolio.study2work.dev/student-021 |
| Mức lương mong muốn | 10-22 triệu VNĐ/tháng |
| sinhvien_id | 29 |
| created_at | 2026-09-16T14:43:09.439Z |

### Sinh viên 022 — Lê Ngọc Bình

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 30 |
| Họ tên | Lê Ngọc Bình |
| Email | seed.student.022@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Marketing - Truyền thông |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 25 |
| Họ tên | Lê Ngọc Bình |
| Ngày sinh | 1999-03-06T00:00:00.000Z |
| Giới tính | Nữ |
| Email CV | seed.student.022@study2work.dev |
| Số điện thoại | 0903000022 |
| Địa chỉ | TP. Hồ Chí Minh, Việt Nam |
| Vị trí | Performance Marketing Specialist |
| Ngành | Marketing - Truyền thông |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Marketing - Truyền thông với vai trò Performance Marketing Specialist. |
| Học vấn | Đại học chuyên ngành Marketing, Truyền thông hoặc Ngôn ngữ |
| Kinh nghiệm | 1 năm kinh nghiệm liên quan đến chiến dịch thương hiệu. |
| Kỹ năng | Content, SEO, Meta Ads, Google Analytics |
| Ngoại ngữ | Tiếng Anh B2 |
| Chứng chỉ | Google Analytics hoặc Meta Blueprint |
| Dự án | Dự án portfolio 022: xây dựng giải pháp thử nghiệm cho chiến dịch thương hiệu. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Truyền thông và Sự kiện; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-022","linkedin":"https://www.linkedin.com/in/seed-student-022"} |
| Portfolio | https://portfolio.study2work.dev/student-022 |
| Mức lương mong muốn | 10-22 triệu VNĐ/tháng |
| sinhvien_id | 30 |
| created_at | 2026-09-16T14:43:09.954Z |

### Sinh viên 023 — Lê Gia Chi

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 31 |
| Họ tên | Lê Gia Chi |
| Email | seed.student.023@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Marketing - Truyền thông |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 26 |
| Họ tên | Lê Gia Chi |
| Ngày sinh | 2000-03-07T00:00:00.000Z |
| Giới tính | Nam |
| Email CV | seed.student.023@study2work.dev |
| Số điện thoại | 0903000023 |
| Địa chỉ | TP. Hồ Chí Minh, Việt Nam |
| Vị trí | Social Media Planner |
| Ngành | Marketing - Truyền thông |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Marketing - Truyền thông với vai trò Social Media Planner. |
| Học vấn | Đại học chuyên ngành Marketing, Truyền thông hoặc Ngôn ngữ |
| Kinh nghiệm | 2 năm kinh nghiệm thực tế trong lĩnh vực chiến dịch thương hiệu. |
| Kỹ năng | Content, SEO, Meta Ads, Google Analytics |
| Ngoại ngữ | Tiếng Anh giao tiếp |
| Chứng chỉ | Google Analytics hoặc Meta Blueprint |
| Dự án | Dự án portfolio 023: xây dựng giải pháp thử nghiệm cho chiến dịch thương hiệu. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Truyền thông và Sự kiện; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-023","linkedin":"https://www.linkedin.com/in/seed-student-023"} |
| Portfolio | https://portfolio.study2work.dev/student-023 |
| Mức lương mong muốn | 10-22 triệu VNĐ/tháng |
| sinhvien_id | 31 |
| created_at | 2026-09-16T14:43:10.462Z |

### Sinh viên 024 — Lê Thanh Dũng

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 32 |
| Họ tên | Lê Thanh Dũng |
| Email | seed.student.024@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Marketing - Truyền thông |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 27 |
| Họ tên | Lê Thanh Dũng |
| Ngày sinh | 2001-03-08T00:00:00.000Z |
| Giới tính | Nữ |
| Email CV | seed.student.024@study2work.dev |
| Số điện thoại | 0903000024 |
| Địa chỉ | TP. Hồ Chí Minh, Việt Nam |
| Vị trí | Account Executive |
| Ngành | Marketing - Truyền thông |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Marketing - Truyền thông với vai trò Account Executive. |
| Học vấn | Đại học chuyên ngành Marketing, Truyền thông hoặc Ngôn ngữ |
| Kinh nghiệm | Fresher; hoàn thành dự án học thuật và 6 tháng thực tập. |
| Kỹ năng | Content, SEO, Meta Ads, Google Analytics |
| Ngoại ngữ | Tiếng Anh B1 |
| Chứng chỉ | Google Analytics hoặc Meta Blueprint |
| Dự án | Dự án portfolio 024: xây dựng giải pháp thử nghiệm cho chiến dịch thương hiệu. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Truyền thông và Sự kiện; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-024","linkedin":"https://www.linkedin.com/in/seed-student-024"} |
| Portfolio | https://portfolio.study2work.dev/student-024 |
| Mức lương mong muốn | 10-22 triệu VNĐ/tháng |
| sinhvien_id | 32 |
| created_at | 2026-09-16T14:43:10.989Z |

### Sinh viên 025 — Lê Khánh Hà

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 33 |
| Họ tên | Lê Khánh Hà |
| Email | seed.student.025@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Marketing - Truyền thông |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 28 |
| Họ tên | Lê Khánh Hà |
| Ngày sinh | 2002-03-09T00:00:00.000Z |
| Giới tính | Nam |
| Email CV | seed.student.025@study2work.dev |
| Số điện thoại | 0903000025 |
| Địa chỉ | TP. Hồ Chí Minh, Việt Nam |
| Vị trí | Content Marketing Executive |
| Ngành | Marketing - Truyền thông |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Marketing - Truyền thông với vai trò Content Marketing Executive. |
| Học vấn | Đại học chuyên ngành Marketing, Truyền thông hoặc Ngôn ngữ |
| Kinh nghiệm | 1 năm kinh nghiệm liên quan đến chiến dịch thương hiệu. |
| Kỹ năng | Content, SEO, Meta Ads, Google Analytics |
| Ngoại ngữ | Tiếng Anh B2 |
| Chứng chỉ | Google Analytics hoặc Meta Blueprint |
| Dự án | Dự án portfolio 025: xây dựng giải pháp thử nghiệm cho chiến dịch thương hiệu. |
| Giải thưởng | Giải thưởng đồ án cấp khoa |
| Hoạt động | CLB Truyền thông và Sự kiện; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-025","linkedin":"https://www.linkedin.com/in/seed-student-025"} |
| Portfolio | https://portfolio.study2work.dev/student-025 |
| Mức lương mong muốn | 10-22 triệu VNĐ/tháng |
| sinhvien_id | 33 |
| created_at | 2026-09-16T14:43:11.491Z |

### Sinh viên 026 — Lê Thu Khang

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 34 |
| Họ tên | Lê Thu Khang |
| Email | seed.student.026@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Marketing - Truyền thông |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 29 |
| Họ tên | Lê Thu Khang |
| Ngày sinh | 1998-03-10T00:00:00.000Z |
| Giới tính | Nữ |
| Email CV | seed.student.026@study2work.dev |
| Số điện thoại | 0903000026 |
| Địa chỉ | TP. Hồ Chí Minh, Việt Nam |
| Vị trí | Performance Marketing Specialist |
| Ngành | Marketing - Truyền thông |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Marketing - Truyền thông với vai trò Performance Marketing Specialist. |
| Học vấn | Đại học chuyên ngành Marketing, Truyền thông hoặc Ngôn ngữ |
| Kinh nghiệm | 2 năm kinh nghiệm thực tế trong lĩnh vực chiến dịch thương hiệu. |
| Kỹ năng | Content, SEO, Meta Ads, Google Analytics |
| Ngoại ngữ | Tiếng Anh giao tiếp |
| Chứng chỉ | Google Analytics hoặc Meta Blueprint |
| Dự án | Dự án portfolio 026: xây dựng giải pháp thử nghiệm cho chiến dịch thương hiệu. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Truyền thông và Sự kiện; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-026","linkedin":"https://www.linkedin.com/in/seed-student-026"} |
| Portfolio | https://portfolio.study2work.dev/student-026 |
| Mức lương mong muốn | 10-22 triệu VNĐ/tháng |
| sinhvien_id | 34 |
| created_at | 2026-09-16T14:43:12.001Z |

### Sinh viên 027 — Lê Đức Linh

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 35 |
| Họ tên | Lê Đức Linh |
| Email | seed.student.027@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Marketing - Truyền thông |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 30 |
| Họ tên | Lê Đức Linh |
| Ngày sinh | 1999-03-11T00:00:00.000Z |
| Giới tính | Nam |
| Email CV | seed.student.027@study2work.dev |
| Số điện thoại | 0903000027 |
| Địa chỉ | TP. Hồ Chí Minh, Việt Nam |
| Vị trí | Social Media Planner |
| Ngành | Marketing - Truyền thông |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Marketing - Truyền thông với vai trò Social Media Planner. |
| Học vấn | Đại học chuyên ngành Marketing, Truyền thông hoặc Ngôn ngữ |
| Kinh nghiệm | Fresher; hoàn thành dự án học thuật và 6 tháng thực tập. |
| Kỹ năng | Content, SEO, Meta Ads, Google Analytics |
| Ngoại ngữ | Tiếng Anh B1 |
| Chứng chỉ | Google Analytics hoặc Meta Blueprint |
| Dự án | Dự án portfolio 027: xây dựng giải pháp thử nghiệm cho chiến dịch thương hiệu. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Truyền thông và Sự kiện; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-027","linkedin":"https://www.linkedin.com/in/seed-student-027"} |
| Portfolio | https://portfolio.study2work.dev/student-027 |
| Mức lương mong muốn | 10-22 triệu VNĐ/tháng |
| sinhvien_id | 35 |
| created_at | 2026-09-16T14:43:12.509Z |

### Sinh viên 028 — Lê Quỳnh Nam

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 36 |
| Họ tên | Lê Quỳnh Nam |
| Email | seed.student.028@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Marketing - Truyền thông |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 31 |
| Họ tên | Lê Quỳnh Nam |
| Ngày sinh | 2000-03-12T00:00:00.000Z |
| Giới tính | Nữ |
| Email CV | seed.student.028@study2work.dev |
| Số điện thoại | 0903000028 |
| Địa chỉ | TP. Hồ Chí Minh, Việt Nam |
| Vị trí | Account Executive |
| Ngành | Marketing - Truyền thông |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Marketing - Truyền thông với vai trò Account Executive. |
| Học vấn | Đại học chuyên ngành Marketing, Truyền thông hoặc Ngôn ngữ |
| Kinh nghiệm | 1 năm kinh nghiệm liên quan đến chiến dịch thương hiệu. |
| Kỹ năng | Content, SEO, Meta Ads, Google Analytics |
| Ngoại ngữ | Tiếng Anh B2 |
| Chứng chỉ | Google Analytics hoặc Meta Blueprint |
| Dự án | Dự án portfolio 028: xây dựng giải pháp thử nghiệm cho chiến dịch thương hiệu. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Truyền thông và Sự kiện; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-028","linkedin":"https://www.linkedin.com/in/seed-student-028"} |
| Portfolio | https://portfolio.study2work.dev/student-028 |
| Mức lương mong muốn | 10-22 triệu VNĐ/tháng |
| sinhvien_id | 36 |
| created_at | 2026-09-16T14:43:13.029Z |

### Sinh viên 029 — Lê Hải Phương

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 37 |
| Họ tên | Lê Hải Phương |
| Email | seed.student.029@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Marketing - Truyền thông |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 32 |
| Họ tên | Lê Hải Phương |
| Ngày sinh | 2001-03-13T00:00:00.000Z |
| Giới tính | Nam |
| Email CV | seed.student.029@study2work.dev |
| Số điện thoại | 0903000029 |
| Địa chỉ | TP. Hồ Chí Minh, Việt Nam |
| Vị trí | Content Marketing Executive |
| Ngành | Marketing - Truyền thông |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Marketing - Truyền thông với vai trò Content Marketing Executive. |
| Học vấn | Đại học chuyên ngành Marketing, Truyền thông hoặc Ngôn ngữ |
| Kinh nghiệm | 2 năm kinh nghiệm thực tế trong lĩnh vực chiến dịch thương hiệu. |
| Kỹ năng | Content, SEO, Meta Ads, Google Analytics |
| Ngoại ngữ | Tiếng Anh giao tiếp |
| Chứng chỉ | Google Analytics hoặc Meta Blueprint |
| Dự án | Dự án portfolio 029: xây dựng giải pháp thử nghiệm cho chiến dịch thương hiệu. |
| Giải thưởng | Giải thưởng đồ án cấp khoa |
| Hoạt động | CLB Truyền thông và Sự kiện; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-029","linkedin":"https://www.linkedin.com/in/seed-student-029"} |
| Portfolio | https://portfolio.study2work.dev/student-029 |
| Mức lương mong muốn | 10-22 triệu VNĐ/tháng |
| sinhvien_id | 37 |
| created_at | 2026-09-16T14:43:13.588Z |

### Sinh viên 030 — Lê Bảo Quân

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 38 |
| Họ tên | Lê Bảo Quân |
| Email | seed.student.030@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Marketing - Truyền thông |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 33 |
| Họ tên | Lê Bảo Quân |
| Ngày sinh | 2002-03-14T00:00:00.000Z |
| Giới tính | Nữ |
| Email CV | seed.student.030@study2work.dev |
| Số điện thoại | 0903000030 |
| Địa chỉ | TP. Hồ Chí Minh, Việt Nam |
| Vị trí | Performance Marketing Specialist |
| Ngành | Marketing - Truyền thông |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Marketing - Truyền thông với vai trò Performance Marketing Specialist. |
| Học vấn | Đại học chuyên ngành Marketing, Truyền thông hoặc Ngôn ngữ |
| Kinh nghiệm | Fresher; hoàn thành dự án học thuật và 6 tháng thực tập. |
| Kỹ năng | Content, SEO, Meta Ads, Google Analytics |
| Ngoại ngữ | Tiếng Anh B1 |
| Chứng chỉ | Google Analytics hoặc Meta Blueprint |
| Dự án | Dự án portfolio 030: xây dựng giải pháp thử nghiệm cho chiến dịch thương hiệu. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Truyền thông và Sự kiện; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-030","linkedin":"https://www.linkedin.com/in/seed-student-030"} |
| Portfolio | https://portfolio.study2work.dev/student-030 |
| Mức lương mong muốn | 10-22 triệu VNĐ/tháng |
| sinhvien_id | 38 |
| created_at | 2026-09-16T14:43:14.108Z |

### Sinh viên 031 — Phạm Minh An

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 39 |
| Họ tên | Phạm Minh An |
| Email | seed.student.031@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Thương mại điện tử |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 34 |
| Họ tên | Phạm Minh An |
| Ngày sinh | 1998-04-05T00:00:00.000Z |
| Giới tính | Nam |
| Email CV | seed.student.031@study2work.dev |
| Số điện thoại | 0903000031 |
| Địa chỉ | Hải Phòng, Việt Nam |
| Vị trí | E-commerce Operations Specialist |
| Ngành | Thương mại điện tử |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Thương mại điện tử với vai trò E-commerce Operations Specialist. |
| Học vấn | Đại học chuyên ngành Kinh doanh, CNTT hoặc Thiết kế |
| Kinh nghiệm | Fresher; hoàn thành dự án học thuật và 6 tháng thực tập. |
| Kỹ năng | E-commerce, SQL, Figma, phân tích funnel |
| Ngoại ngữ | Tiếng Anh B1 |
| Chứng chỉ | Google Analytics hoặc chứng chỉ Product Analytics |
| Dự án | Dự án portfolio 031: xây dựng giải pháp thử nghiệm cho sàn thương mại điện tử. |
| Giải thưởng | Giải thưởng đồ án cấp khoa |
| Hoạt động | CLB Kinh doanh và Khởi nghiệp; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-031","linkedin":"https://www.linkedin.com/in/seed-student-031"} |
| Portfolio | https://portfolio.study2work.dev/student-031 |
| Mức lương mong muốn | 11-24 triệu VNĐ/tháng |
| sinhvien_id | 39 |
| created_at | 2026-09-16T14:43:14.611Z |

### Sinh viên 032 — Phạm Ngọc Bình

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 40 |
| Họ tên | Phạm Ngọc Bình |
| Email | seed.student.032@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Thương mại điện tử |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 35 |
| Họ tên | Phạm Ngọc Bình |
| Ngày sinh | 1999-04-06T00:00:00.000Z |
| Giới tính | Nữ |
| Email CV | seed.student.032@study2work.dev |
| Số điện thoại | 0903000032 |
| Địa chỉ | Hải Phòng, Việt Nam |
| Vị trí | Product Owner E-commerce |
| Ngành | Thương mại điện tử |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Thương mại điện tử với vai trò Product Owner E-commerce. |
| Học vấn | Đại học chuyên ngành Kinh doanh, CNTT hoặc Thiết kế |
| Kinh nghiệm | 1 năm kinh nghiệm liên quan đến sàn thương mại điện tử. |
| Kỹ năng | E-commerce, SQL, Figma, phân tích funnel |
| Ngoại ngữ | Tiếng Anh B2 |
| Chứng chỉ | Google Analytics hoặc chứng chỉ Product Analytics |
| Dự án | Dự án portfolio 032: xây dựng giải pháp thử nghiệm cho sàn thương mại điện tử. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Kinh doanh và Khởi nghiệp; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-032","linkedin":"https://www.linkedin.com/in/seed-student-032"} |
| Portfolio | https://portfolio.study2work.dev/student-032 |
| Mức lương mong muốn | 11-24 triệu VNĐ/tháng |
| sinhvien_id | 40 |
| created_at | 2026-09-16T14:43:15.132Z |

### Sinh viên 033 — Phạm Gia Chi

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 41 |
| Họ tên | Phạm Gia Chi |
| Email | seed.student.033@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Thương mại điện tử |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 36 |
| Họ tên | Phạm Gia Chi |
| Ngày sinh | 2000-04-07T00:00:00.000Z |
| Giới tính | Nam |
| Email CV | seed.student.033@study2work.dev |
| Số điện thoại | 0903000033 |
| Địa chỉ | Hải Phòng, Việt Nam |
| Vị trí | UI/UX Designer |
| Ngành | Thương mại điện tử |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Thương mại điện tử với vai trò UI/UX Designer. |
| Học vấn | Đại học chuyên ngành Kinh doanh, CNTT hoặc Thiết kế |
| Kinh nghiệm | 2 năm kinh nghiệm thực tế trong lĩnh vực sàn thương mại điện tử. |
| Kỹ năng | E-commerce, SQL, Figma, phân tích funnel |
| Ngoại ngữ | Tiếng Anh giao tiếp |
| Chứng chỉ | Google Analytics hoặc chứng chỉ Product Analytics |
| Dự án | Dự án portfolio 033: xây dựng giải pháp thử nghiệm cho sàn thương mại điện tử. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Kinh doanh và Khởi nghiệp; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-033","linkedin":"https://www.linkedin.com/in/seed-student-033"} |
| Portfolio | https://portfolio.study2work.dev/student-033 |
| Mức lương mong muốn | 11-24 triệu VNĐ/tháng |
| sinhvien_id | 41 |
| created_at | 2026-09-16T14:43:15.646Z |

### Sinh viên 034 — Phạm Thanh Dũng

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 42 |
| Họ tên | Phạm Thanh Dũng |
| Email | seed.student.034@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Thương mại điện tử |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 37 |
| Họ tên | Phạm Thanh Dũng |
| Ngày sinh | 2001-04-08T00:00:00.000Z |
| Giới tính | Nữ |
| Email CV | seed.student.034@study2work.dev |
| Số điện thoại | 0903000034 |
| Địa chỉ | Hải Phòng, Việt Nam |
| Vị trí | Customer Growth Analyst |
| Ngành | Thương mại điện tử |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Thương mại điện tử với vai trò Customer Growth Analyst. |
| Học vấn | Đại học chuyên ngành Kinh doanh, CNTT hoặc Thiết kế |
| Kinh nghiệm | Fresher; hoàn thành dự án học thuật và 6 tháng thực tập. |
| Kỹ năng | E-commerce, SQL, Figma, phân tích funnel |
| Ngoại ngữ | Tiếng Anh B1 |
| Chứng chỉ | Google Analytics hoặc chứng chỉ Product Analytics |
| Dự án | Dự án portfolio 034: xây dựng giải pháp thử nghiệm cho sàn thương mại điện tử. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Kinh doanh và Khởi nghiệp; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-034","linkedin":"https://www.linkedin.com/in/seed-student-034"} |
| Portfolio | https://portfolio.study2work.dev/student-034 |
| Mức lương mong muốn | 11-24 triệu VNĐ/tháng |
| sinhvien_id | 42 |
| created_at | 2026-09-16T14:43:16.157Z |

### Sinh viên 035 — Phạm Khánh Hà

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 43 |
| Họ tên | Phạm Khánh Hà |
| Email | seed.student.035@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Thương mại điện tử |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 38 |
| Họ tên | Phạm Khánh Hà |
| Ngày sinh | 2002-04-09T00:00:00.000Z |
| Giới tính | Nam |
| Email CV | seed.student.035@study2work.dev |
| Số điện thoại | 0903000035 |
| Địa chỉ | Hải Phòng, Việt Nam |
| Vị trí | E-commerce Operations Specialist |
| Ngành | Thương mại điện tử |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Thương mại điện tử với vai trò E-commerce Operations Specialist. |
| Học vấn | Đại học chuyên ngành Kinh doanh, CNTT hoặc Thiết kế |
| Kinh nghiệm | 1 năm kinh nghiệm liên quan đến sàn thương mại điện tử. |
| Kỹ năng | E-commerce, SQL, Figma, phân tích funnel |
| Ngoại ngữ | Tiếng Anh B2 |
| Chứng chỉ | Google Analytics hoặc chứng chỉ Product Analytics |
| Dự án | Dự án portfolio 035: xây dựng giải pháp thử nghiệm cho sàn thương mại điện tử. |
| Giải thưởng | Giải thưởng đồ án cấp khoa |
| Hoạt động | CLB Kinh doanh và Khởi nghiệp; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-035","linkedin":"https://www.linkedin.com/in/seed-student-035"} |
| Portfolio | https://portfolio.study2work.dev/student-035 |
| Mức lương mong muốn | 11-24 triệu VNĐ/tháng |
| sinhvien_id | 43 |
| created_at | 2026-09-16T14:43:16.671Z |

### Sinh viên 036 — Phạm Thu Khang

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 44 |
| Họ tên | Phạm Thu Khang |
| Email | seed.student.036@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Thương mại điện tử |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 39 |
| Họ tên | Phạm Thu Khang |
| Ngày sinh | 1998-04-10T00:00:00.000Z |
| Giới tính | Nữ |
| Email CV | seed.student.036@study2work.dev |
| Số điện thoại | 0903000036 |
| Địa chỉ | Hải Phòng, Việt Nam |
| Vị trí | Product Owner E-commerce |
| Ngành | Thương mại điện tử |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Thương mại điện tử với vai trò Product Owner E-commerce. |
| Học vấn | Đại học chuyên ngành Kinh doanh, CNTT hoặc Thiết kế |
| Kinh nghiệm | 2 năm kinh nghiệm thực tế trong lĩnh vực sàn thương mại điện tử. |
| Kỹ năng | E-commerce, SQL, Figma, phân tích funnel |
| Ngoại ngữ | Tiếng Anh giao tiếp |
| Chứng chỉ | Google Analytics hoặc chứng chỉ Product Analytics |
| Dự án | Dự án portfolio 036: xây dựng giải pháp thử nghiệm cho sàn thương mại điện tử. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Kinh doanh và Khởi nghiệp; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-036","linkedin":"https://www.linkedin.com/in/seed-student-036"} |
| Portfolio | https://portfolio.study2work.dev/student-036 |
| Mức lương mong muốn | 11-24 triệu VNĐ/tháng |
| sinhvien_id | 44 |
| created_at | 2026-09-16T14:43:17.175Z |

### Sinh viên 037 — Phạm Đức Linh

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 45 |
| Họ tên | Phạm Đức Linh |
| Email | seed.student.037@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Thương mại điện tử |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 40 |
| Họ tên | Phạm Đức Linh |
| Ngày sinh | 1999-04-11T00:00:00.000Z |
| Giới tính | Nam |
| Email CV | seed.student.037@study2work.dev |
| Số điện thoại | 0903000037 |
| Địa chỉ | Hải Phòng, Việt Nam |
| Vị trí | UI/UX Designer |
| Ngành | Thương mại điện tử |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Thương mại điện tử với vai trò UI/UX Designer. |
| Học vấn | Đại học chuyên ngành Kinh doanh, CNTT hoặc Thiết kế |
| Kinh nghiệm | Fresher; hoàn thành dự án học thuật và 6 tháng thực tập. |
| Kỹ năng | E-commerce, SQL, Figma, phân tích funnel |
| Ngoại ngữ | Tiếng Anh B1 |
| Chứng chỉ | Google Analytics hoặc chứng chỉ Product Analytics |
| Dự án | Dự án portfolio 037: xây dựng giải pháp thử nghiệm cho sàn thương mại điện tử. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Kinh doanh và Khởi nghiệp; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-037","linkedin":"https://www.linkedin.com/in/seed-student-037"} |
| Portfolio | https://portfolio.study2work.dev/student-037 |
| Mức lương mong muốn | 11-24 triệu VNĐ/tháng |
| sinhvien_id | 45 |
| created_at | 2026-09-16T14:43:17.688Z |

### Sinh viên 038 — Phạm Quỳnh Nam

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 46 |
| Họ tên | Phạm Quỳnh Nam |
| Email | seed.student.038@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Thương mại điện tử |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 41 |
| Họ tên | Phạm Quỳnh Nam |
| Ngày sinh | 2000-04-12T00:00:00.000Z |
| Giới tính | Nữ |
| Email CV | seed.student.038@study2work.dev |
| Số điện thoại | 0903000038 |
| Địa chỉ | Hải Phòng, Việt Nam |
| Vị trí | Customer Growth Analyst |
| Ngành | Thương mại điện tử |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Thương mại điện tử với vai trò Customer Growth Analyst. |
| Học vấn | Đại học chuyên ngành Kinh doanh, CNTT hoặc Thiết kế |
| Kinh nghiệm | 1 năm kinh nghiệm liên quan đến sàn thương mại điện tử. |
| Kỹ năng | E-commerce, SQL, Figma, phân tích funnel |
| Ngoại ngữ | Tiếng Anh B2 |
| Chứng chỉ | Google Analytics hoặc chứng chỉ Product Analytics |
| Dự án | Dự án portfolio 038: xây dựng giải pháp thử nghiệm cho sàn thương mại điện tử. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Kinh doanh và Khởi nghiệp; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-038","linkedin":"https://www.linkedin.com/in/seed-student-038"} |
| Portfolio | https://portfolio.study2work.dev/student-038 |
| Mức lương mong muốn | 11-24 triệu VNĐ/tháng |
| sinhvien_id | 46 |
| created_at | 2026-09-16T14:43:18.195Z |

### Sinh viên 039 — Phạm Hải Phương

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 47 |
| Họ tên | Phạm Hải Phương |
| Email | seed.student.039@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Thương mại điện tử |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 42 |
| Họ tên | Phạm Hải Phương |
| Ngày sinh | 2001-04-13T00:00:00.000Z |
| Giới tính | Nam |
| Email CV | seed.student.039@study2work.dev |
| Số điện thoại | 0903000039 |
| Địa chỉ | Hải Phòng, Việt Nam |
| Vị trí | E-commerce Operations Specialist |
| Ngành | Thương mại điện tử |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Thương mại điện tử với vai trò E-commerce Operations Specialist. |
| Học vấn | Đại học chuyên ngành Kinh doanh, CNTT hoặc Thiết kế |
| Kinh nghiệm | 2 năm kinh nghiệm thực tế trong lĩnh vực sàn thương mại điện tử. |
| Kỹ năng | E-commerce, SQL, Figma, phân tích funnel |
| Ngoại ngữ | Tiếng Anh giao tiếp |
| Chứng chỉ | Google Analytics hoặc chứng chỉ Product Analytics |
| Dự án | Dự án portfolio 039: xây dựng giải pháp thử nghiệm cho sàn thương mại điện tử. |
| Giải thưởng | Giải thưởng đồ án cấp khoa |
| Hoạt động | CLB Kinh doanh và Khởi nghiệp; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-039","linkedin":"https://www.linkedin.com/in/seed-student-039"} |
| Portfolio | https://portfolio.study2work.dev/student-039 |
| Mức lương mong muốn | 11-24 triệu VNĐ/tháng |
| sinhvien_id | 47 |
| created_at | 2026-09-16T14:43:18.710Z |

### Sinh viên 040 — Phạm Bảo Quân

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 48 |
| Họ tên | Phạm Bảo Quân |
| Email | seed.student.040@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Thương mại điện tử |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 43 |
| Họ tên | Phạm Bảo Quân |
| Ngày sinh | 2002-04-14T00:00:00.000Z |
| Giới tính | Nữ |
| Email CV | seed.student.040@study2work.dev |
| Số điện thoại | 0903000040 |
| Địa chỉ | Hải Phòng, Việt Nam |
| Vị trí | Product Owner E-commerce |
| Ngành | Thương mại điện tử |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Thương mại điện tử với vai trò Product Owner E-commerce. |
| Học vấn | Đại học chuyên ngành Kinh doanh, CNTT hoặc Thiết kế |
| Kinh nghiệm | Fresher; hoàn thành dự án học thuật và 6 tháng thực tập. |
| Kỹ năng | E-commerce, SQL, Figma, phân tích funnel |
| Ngoại ngữ | Tiếng Anh B1 |
| Chứng chỉ | Google Analytics hoặc chứng chỉ Product Analytics |
| Dự án | Dự án portfolio 040: xây dựng giải pháp thử nghiệm cho sàn thương mại điện tử. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Kinh doanh và Khởi nghiệp; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-040","linkedin":"https://www.linkedin.com/in/seed-student-040"} |
| Portfolio | https://portfolio.study2work.dev/student-040 |
| Mức lương mong muốn | 11-24 triệu VNĐ/tháng |
| sinhvien_id | 48 |
| created_at | 2026-09-16T14:43:19.223Z |

### Sinh viên 041 — Hoàng Minh An

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 49 |
| Họ tên | Hoàng Minh An |
| Email | seed.student.041@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Giáo dục |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 44 |
| Họ tên | Hoàng Minh An |
| Ngày sinh | 1998-05-05T00:00:00.000Z |
| Giới tính | Nam |
| Email CV | seed.student.041@study2work.dev |
| Số điện thoại | 0903000041 |
| Địa chỉ | Cần Thơ, Việt Nam |
| Vị trí | Academic Advisor |
| Ngành | Giáo dục |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Giáo dục với vai trò Academic Advisor. |
| Học vấn | Đại học chuyên ngành Giáo dục, Xã hội học hoặc CNTT |
| Kinh nghiệm | Fresher; hoàn thành dự án học thuật và 6 tháng thực tập. |
| Kỹ năng | Instructional Design, LMS, giao tiếp, Excel |
| Ngoại ngữ | Tiếng Anh B1 |
| Chứng chỉ | Google Educator hoặc chứng chỉ đào tạo trực tuyến |
| Dự án | Dự án portfolio 041: xây dựng giải pháp thử nghiệm cho giáo dục số. |
| Giải thưởng | Giải thưởng đồ án cấp khoa |
| Hoạt động | CLB Giáo dục và Cộng đồng; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-041","linkedin":"https://www.linkedin.com/in/seed-student-041"} |
| Portfolio | https://portfolio.study2work.dev/student-041 |
| Mức lương mong muốn | 9-20 triệu VNĐ/tháng |
| sinhvien_id | 49 |
| created_at | 2026-09-16T14:43:19.737Z |

### Sinh viên 042 — Hoàng Ngọc Bình

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 50 |
| Họ tên | Hoàng Ngọc Bình |
| Email | seed.student.042@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Giáo dục |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 45 |
| Họ tên | Hoàng Ngọc Bình |
| Ngày sinh | 1999-05-06T00:00:00.000Z |
| Giới tính | Nữ |
| Email CV | seed.student.042@study2work.dev |
| Số điện thoại | 0903000042 |
| Địa chỉ | Cần Thơ, Việt Nam |
| Vị trí | Instructional Designer |
| Ngành | Giáo dục |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Giáo dục với vai trò Instructional Designer. |
| Học vấn | Đại học chuyên ngành Giáo dục, Xã hội học hoặc CNTT |
| Kinh nghiệm | 1 năm kinh nghiệm liên quan đến giáo dục số. |
| Kỹ năng | Instructional Design, LMS, giao tiếp, Excel |
| Ngoại ngữ | Tiếng Anh B2 |
| Chứng chỉ | Google Educator hoặc chứng chỉ đào tạo trực tuyến |
| Dự án | Dự án portfolio 042: xây dựng giải pháp thử nghiệm cho giáo dục số. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Giáo dục và Cộng đồng; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-042","linkedin":"https://www.linkedin.com/in/seed-student-042"} |
| Portfolio | https://portfolio.study2work.dev/student-042 |
| Mức lương mong muốn | 9-20 triệu VNĐ/tháng |
| sinhvien_id | 50 |
| created_at | 2026-09-16T14:43:20.250Z |

### Sinh viên 043 — Hoàng Gia Chi

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 51 |
| Họ tên | Hoàng Gia Chi |
| Email | seed.student.043@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Giáo dục |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 46 |
| Họ tên | Hoàng Gia Chi |
| Ngày sinh | 2000-05-07T00:00:00.000Z |
| Giới tính | Nam |
| Email CV | seed.student.043@study2work.dev |
| Số điện thoại | 0903000043 |
| Địa chỉ | Cần Thơ, Việt Nam |
| Vị trí | Full-stack Developer EdTech |
| Ngành | Giáo dục |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Giáo dục với vai trò Full-stack Developer EdTech. |
| Học vấn | Đại học chuyên ngành Giáo dục, Xã hội học hoặc CNTT |
| Kinh nghiệm | 2 năm kinh nghiệm thực tế trong lĩnh vực giáo dục số. |
| Kỹ năng | Instructional Design, LMS, giao tiếp, Excel |
| Ngoại ngữ | Tiếng Anh giao tiếp |
| Chứng chỉ | Google Educator hoặc chứng chỉ đào tạo trực tuyến |
| Dự án | Dự án portfolio 043: xây dựng giải pháp thử nghiệm cho giáo dục số. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Giáo dục và Cộng đồng; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-043","linkedin":"https://www.linkedin.com/in/seed-student-043"} |
| Portfolio | https://portfolio.study2work.dev/student-043 |
| Mức lương mong muốn | 9-20 triệu VNĐ/tháng |
| sinhvien_id | 51 |
| created_at | 2026-09-16T14:43:20.755Z |

### Sinh viên 044 — Hoàng Thanh Dũng

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 52 |
| Họ tên | Hoàng Thanh Dũng |
| Email | seed.student.044@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Giáo dục |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 47 |
| Họ tên | Hoàng Thanh Dũng |
| Ngày sinh | 2001-05-08T00:00:00.000Z |
| Giới tính | Nữ |
| Email CV | seed.student.044@study2work.dev |
| Số điện thoại | 0903000044 |
| Địa chỉ | Cần Thơ, Việt Nam |
| Vị trí | Student Success Specialist |
| Ngành | Giáo dục |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Giáo dục với vai trò Student Success Specialist. |
| Học vấn | Đại học chuyên ngành Giáo dục, Xã hội học hoặc CNTT |
| Kinh nghiệm | Fresher; hoàn thành dự án học thuật và 6 tháng thực tập. |
| Kỹ năng | Instructional Design, LMS, giao tiếp, Excel |
| Ngoại ngữ | Tiếng Anh B1 |
| Chứng chỉ | Google Educator hoặc chứng chỉ đào tạo trực tuyến |
| Dự án | Dự án portfolio 044: xây dựng giải pháp thử nghiệm cho giáo dục số. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Giáo dục và Cộng đồng; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-044","linkedin":"https://www.linkedin.com/in/seed-student-044"} |
| Portfolio | https://portfolio.study2work.dev/student-044 |
| Mức lương mong muốn | 9-20 triệu VNĐ/tháng |
| sinhvien_id | 52 |
| created_at | 2026-09-16T14:43:21.273Z |

### Sinh viên 045 — Hoàng Khánh Hà

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 53 |
| Họ tên | Hoàng Khánh Hà |
| Email | seed.student.045@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Giáo dục |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 48 |
| Họ tên | Hoàng Khánh Hà |
| Ngày sinh | 2002-05-09T00:00:00.000Z |
| Giới tính | Nam |
| Email CV | seed.student.045@study2work.dev |
| Số điện thoại | 0903000045 |
| Địa chỉ | Cần Thơ, Việt Nam |
| Vị trí | Academic Advisor |
| Ngành | Giáo dục |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Giáo dục với vai trò Academic Advisor. |
| Học vấn | Đại học chuyên ngành Giáo dục, Xã hội học hoặc CNTT |
| Kinh nghiệm | 1 năm kinh nghiệm liên quan đến giáo dục số. |
| Kỹ năng | Instructional Design, LMS, giao tiếp, Excel |
| Ngoại ngữ | Tiếng Anh B2 |
| Chứng chỉ | Google Educator hoặc chứng chỉ đào tạo trực tuyến |
| Dự án | Dự án portfolio 045: xây dựng giải pháp thử nghiệm cho giáo dục số. |
| Giải thưởng | Giải thưởng đồ án cấp khoa |
| Hoạt động | CLB Giáo dục và Cộng đồng; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-045","linkedin":"https://www.linkedin.com/in/seed-student-045"} |
| Portfolio | https://portfolio.study2work.dev/student-045 |
| Mức lương mong muốn | 9-20 triệu VNĐ/tháng |
| sinhvien_id | 53 |
| created_at | 2026-09-16T14:43:21.783Z |

### Sinh viên 046 — Hoàng Thu Khang

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 54 |
| Họ tên | Hoàng Thu Khang |
| Email | seed.student.046@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Giáo dục |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 49 |
| Họ tên | Hoàng Thu Khang |
| Ngày sinh | 1998-05-10T00:00:00.000Z |
| Giới tính | Nữ |
| Email CV | seed.student.046@study2work.dev |
| Số điện thoại | 0903000046 |
| Địa chỉ | Cần Thơ, Việt Nam |
| Vị trí | Instructional Designer |
| Ngành | Giáo dục |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Giáo dục với vai trò Instructional Designer. |
| Học vấn | Đại học chuyên ngành Giáo dục, Xã hội học hoặc CNTT |
| Kinh nghiệm | 2 năm kinh nghiệm thực tế trong lĩnh vực giáo dục số. |
| Kỹ năng | Instructional Design, LMS, giao tiếp, Excel |
| Ngoại ngữ | Tiếng Anh giao tiếp |
| Chứng chỉ | Google Educator hoặc chứng chỉ đào tạo trực tuyến |
| Dự án | Dự án portfolio 046: xây dựng giải pháp thử nghiệm cho giáo dục số. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Giáo dục và Cộng đồng; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-046","linkedin":"https://www.linkedin.com/in/seed-student-046"} |
| Portfolio | https://portfolio.study2work.dev/student-046 |
| Mức lương mong muốn | 9-20 triệu VNĐ/tháng |
| sinhvien_id | 54 |
| created_at | 2026-09-16T14:43:22.291Z |

### Sinh viên 047 — Hoàng Đức Linh

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 55 |
| Họ tên | Hoàng Đức Linh |
| Email | seed.student.047@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Giáo dục |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 50 |
| Họ tên | Hoàng Đức Linh |
| Ngày sinh | 1999-05-11T00:00:00.000Z |
| Giới tính | Nam |
| Email CV | seed.student.047@study2work.dev |
| Số điện thoại | 0903000047 |
| Địa chỉ | Cần Thơ, Việt Nam |
| Vị trí | Full-stack Developer EdTech |
| Ngành | Giáo dục |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Giáo dục với vai trò Full-stack Developer EdTech. |
| Học vấn | Đại học chuyên ngành Giáo dục, Xã hội học hoặc CNTT |
| Kinh nghiệm | Fresher; hoàn thành dự án học thuật và 6 tháng thực tập. |
| Kỹ năng | Instructional Design, LMS, giao tiếp, Excel |
| Ngoại ngữ | Tiếng Anh B1 |
| Chứng chỉ | Google Educator hoặc chứng chỉ đào tạo trực tuyến |
| Dự án | Dự án portfolio 047: xây dựng giải pháp thử nghiệm cho giáo dục số. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Giáo dục và Cộng đồng; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-047","linkedin":"https://www.linkedin.com/in/seed-student-047"} |
| Portfolio | https://portfolio.study2work.dev/student-047 |
| Mức lương mong muốn | 9-20 triệu VNĐ/tháng |
| sinhvien_id | 55 |
| created_at | 2026-09-16T14:43:22.807Z |

### Sinh viên 048 — Hoàng Quỳnh Nam

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 56 |
| Họ tên | Hoàng Quỳnh Nam |
| Email | seed.student.048@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Giáo dục |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 51 |
| Họ tên | Hoàng Quỳnh Nam |
| Ngày sinh | 2000-05-12T00:00:00.000Z |
| Giới tính | Nữ |
| Email CV | seed.student.048@study2work.dev |
| Số điện thoại | 0903000048 |
| Địa chỉ | Cần Thơ, Việt Nam |
| Vị trí | Student Success Specialist |
| Ngành | Giáo dục |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Giáo dục với vai trò Student Success Specialist. |
| Học vấn | Đại học chuyên ngành Giáo dục, Xã hội học hoặc CNTT |
| Kinh nghiệm | 1 năm kinh nghiệm liên quan đến giáo dục số. |
| Kỹ năng | Instructional Design, LMS, giao tiếp, Excel |
| Ngoại ngữ | Tiếng Anh B2 |
| Chứng chỉ | Google Educator hoặc chứng chỉ đào tạo trực tuyến |
| Dự án | Dự án portfolio 048: xây dựng giải pháp thử nghiệm cho giáo dục số. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Giáo dục và Cộng đồng; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-048","linkedin":"https://www.linkedin.com/in/seed-student-048"} |
| Portfolio | https://portfolio.study2work.dev/student-048 |
| Mức lương mong muốn | 9-20 triệu VNĐ/tháng |
| sinhvien_id | 56 |
| created_at | 2026-09-16T14:43:23.317Z |

### Sinh viên 049 — Hoàng Hải Phương

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 57 |
| Họ tên | Hoàng Hải Phương |
| Email | seed.student.049@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Giáo dục |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 52 |
| Họ tên | Hoàng Hải Phương |
| Ngày sinh | 2001-05-13T00:00:00.000Z |
| Giới tính | Nam |
| Email CV | seed.student.049@study2work.dev |
| Số điện thoại | 0903000049 |
| Địa chỉ | Cần Thơ, Việt Nam |
| Vị trí | Academic Advisor |
| Ngành | Giáo dục |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Giáo dục với vai trò Academic Advisor. |
| Học vấn | Đại học chuyên ngành Giáo dục, Xã hội học hoặc CNTT |
| Kinh nghiệm | 2 năm kinh nghiệm thực tế trong lĩnh vực giáo dục số. |
| Kỹ năng | Instructional Design, LMS, giao tiếp, Excel |
| Ngoại ngữ | Tiếng Anh giao tiếp |
| Chứng chỉ | Google Educator hoặc chứng chỉ đào tạo trực tuyến |
| Dự án | Dự án portfolio 049: xây dựng giải pháp thử nghiệm cho giáo dục số. |
| Giải thưởng | Giải thưởng đồ án cấp khoa |
| Hoạt động | CLB Giáo dục và Cộng đồng; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-049","linkedin":"https://www.linkedin.com/in/seed-student-049"} |
| Portfolio | https://portfolio.study2work.dev/student-049 |
| Mức lương mong muốn | 9-20 triệu VNĐ/tháng |
| sinhvien_id | 57 |
| created_at | 2026-09-16T14:43:23.827Z |

### Sinh viên 050 — Hoàng Bảo Quân

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 58 |
| Họ tên | Hoàng Bảo Quân |
| Email | seed.student.050@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Giáo dục |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 53 |
| Họ tên | Hoàng Bảo Quân |
| Ngày sinh | 2002-05-14T00:00:00.000Z |
| Giới tính | Nữ |
| Email CV | seed.student.050@study2work.dev |
| Số điện thoại | 0903000050 |
| Địa chỉ | Cần Thơ, Việt Nam |
| Vị trí | Instructional Designer |
| Ngành | Giáo dục |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Giáo dục với vai trò Instructional Designer. |
| Học vấn | Đại học chuyên ngành Giáo dục, Xã hội học hoặc CNTT |
| Kinh nghiệm | Fresher; hoàn thành dự án học thuật và 6 tháng thực tập. |
| Kỹ năng | Instructional Design, LMS, giao tiếp, Excel |
| Ngoại ngữ | Tiếng Anh B1 |
| Chứng chỉ | Google Educator hoặc chứng chỉ đào tạo trực tuyến |
| Dự án | Dự án portfolio 050: xây dựng giải pháp thử nghiệm cho giáo dục số. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Giáo dục và Cộng đồng; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-050","linkedin":"https://www.linkedin.com/in/seed-student-050"} |
| Portfolio | https://portfolio.study2work.dev/student-050 |
| Mức lương mong muốn | 9-20 triệu VNĐ/tháng |
| sinhvien_id | 58 |
| created_at | 2026-09-16T14:43:24.341Z |

### Sinh viên 051 — Huỳnh Minh An

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 59 |
| Họ tên | Huỳnh Minh An |
| Email | seed.student.051@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Logistics |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 54 |
| Họ tên | Huỳnh Minh An |
| Ngày sinh | 1998-06-05T00:00:00.000Z |
| Giới tính | Nam |
| Email CV | seed.student.051@study2work.dev |
| Số điện thoại | 0903000051 |
| Địa chỉ | Bình Dương, Việt Nam |
| Vị trí | Supply Chain Analyst |
| Ngành | Logistics |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Logistics với vai trò Supply Chain Analyst. |
| Học vấn | Đại học chuyên ngành Logistics, Kinh tế hoặc Kỹ thuật |
| Kinh nghiệm | Fresher; hoàn thành dự án học thuật và 6 tháng thực tập. |
| Kỹ năng | Supply Chain, Excel, SQL, quản lý vận hành |
| Ngoại ngữ | Tiếng Anh B1 |
| Chứng chỉ | CSCP, Excel nâng cao hoặc chứng chỉ logistics |
| Dự án | Dự án portfolio 051: xây dựng giải pháp thử nghiệm cho chuỗi cung ứng. |
| Giải thưởng | Giải thưởng đồ án cấp khoa |
| Hoạt động | CLB Logistics và Quản trị; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-051","linkedin":"https://www.linkedin.com/in/seed-student-051"} |
| Portfolio | https://portfolio.study2work.dev/student-051 |
| Mức lương mong muốn | 10-23 triệu VNĐ/tháng |
| sinhvien_id | 59 |
| created_at | 2026-09-16T14:43:24.873Z |

### Sinh viên 052 — Huỳnh Ngọc Bình

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 60 |
| Họ tên | Huỳnh Ngọc Bình |
| Email | seed.student.052@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Logistics |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 55 |
| Họ tên | Huỳnh Ngọc Bình |
| Ngày sinh | 1999-06-06T00:00:00.000Z |
| Giới tính | Nữ |
| Email CV | seed.student.052@study2work.dev |
| Số điện thoại | 0903000052 |
| Địa chỉ | Bình Dương, Việt Nam |
| Vị trí | Logistics Operations Coordinator |
| Ngành | Logistics |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Logistics với vai trò Logistics Operations Coordinator. |
| Học vấn | Đại học chuyên ngành Logistics, Kinh tế hoặc Kỹ thuật |
| Kinh nghiệm | 1 năm kinh nghiệm liên quan đến chuỗi cung ứng. |
| Kỹ năng | Supply Chain, Excel, SQL, quản lý vận hành |
| Ngoại ngữ | Tiếng Anh B2 |
| Chứng chỉ | CSCP, Excel nâng cao hoặc chứng chỉ logistics |
| Dự án | Dự án portfolio 052: xây dựng giải pháp thử nghiệm cho chuỗi cung ứng. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Logistics và Quản trị; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-052","linkedin":"https://www.linkedin.com/in/seed-student-052"} |
| Portfolio | https://portfolio.study2work.dev/student-052 |
| Mức lương mong muốn | 10-23 triệu VNĐ/tháng |
| sinhvien_id | 60 |
| created_at | 2026-09-16T14:43:25.373Z |

### Sinh viên 053 — Huỳnh Gia Chi

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 61 |
| Họ tên | Huỳnh Gia Chi |
| Email | seed.student.053@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Logistics |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 56 |
| Họ tên | Huỳnh Gia Chi |
| Ngày sinh | 2000-06-07T00:00:00.000Z |
| Giới tính | Nam |
| Email CV | seed.student.053@study2work.dev |
| Số điện thoại | 0903000053 |
| Địa chỉ | Bình Dương, Việt Nam |
| Vị trí | Fleet Technology Product Specialist |
| Ngành | Logistics |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Logistics với vai trò Fleet Technology Product Specialist. |
| Học vấn | Đại học chuyên ngành Logistics, Kinh tế hoặc Kỹ thuật |
| Kinh nghiệm | 2 năm kinh nghiệm thực tế trong lĩnh vực chuỗi cung ứng. |
| Kỹ năng | Supply Chain, Excel, SQL, quản lý vận hành |
| Ngoại ngữ | Tiếng Anh giao tiếp |
| Chứng chỉ | CSCP, Excel nâng cao hoặc chứng chỉ logistics |
| Dự án | Dự án portfolio 053: xây dựng giải pháp thử nghiệm cho chuỗi cung ứng. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Logistics và Quản trị; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-053","linkedin":"https://www.linkedin.com/in/seed-student-053"} |
| Portfolio | https://portfolio.study2work.dev/student-053 |
| Mức lương mong muốn | 10-23 triệu VNĐ/tháng |
| sinhvien_id | 61 |
| created_at | 2026-09-16T14:43:25.887Z |

### Sinh viên 054 — Huỳnh Thanh Dũng

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 62 |
| Họ tên | Huỳnh Thanh Dũng |
| Email | seed.student.054@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Logistics |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 57 |
| Họ tên | Huỳnh Thanh Dũng |
| Ngày sinh | 2001-06-08T00:00:00.000Z |
| Giới tính | Nữ |
| Email CV | seed.student.054@study2work.dev |
| Số điện thoại | 0903000054 |
| Địa chỉ | Bình Dương, Việt Nam |
| Vị trí | Warehouse Process Engineer |
| Ngành | Logistics |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Logistics với vai trò Warehouse Process Engineer. |
| Học vấn | Đại học chuyên ngành Logistics, Kinh tế hoặc Kỹ thuật |
| Kinh nghiệm | Fresher; hoàn thành dự án học thuật và 6 tháng thực tập. |
| Kỹ năng | Supply Chain, Excel, SQL, quản lý vận hành |
| Ngoại ngữ | Tiếng Anh B1 |
| Chứng chỉ | CSCP, Excel nâng cao hoặc chứng chỉ logistics |
| Dự án | Dự án portfolio 054: xây dựng giải pháp thử nghiệm cho chuỗi cung ứng. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Logistics và Quản trị; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-054","linkedin":"https://www.linkedin.com/in/seed-student-054"} |
| Portfolio | https://portfolio.study2work.dev/student-054 |
| Mức lương mong muốn | 10-23 triệu VNĐ/tháng |
| sinhvien_id | 62 |
| created_at | 2026-09-16T14:43:26.387Z |

### Sinh viên 055 — Huỳnh Khánh Hà

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 63 |
| Họ tên | Huỳnh Khánh Hà |
| Email | seed.student.055@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Logistics |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 58 |
| Họ tên | Huỳnh Khánh Hà |
| Ngày sinh | 2002-06-09T00:00:00.000Z |
| Giới tính | Nam |
| Email CV | seed.student.055@study2work.dev |
| Số điện thoại | 0903000055 |
| Địa chỉ | Bình Dương, Việt Nam |
| Vị trí | Supply Chain Analyst |
| Ngành | Logistics |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Logistics với vai trò Supply Chain Analyst. |
| Học vấn | Đại học chuyên ngành Logistics, Kinh tế hoặc Kỹ thuật |
| Kinh nghiệm | 1 năm kinh nghiệm liên quan đến chuỗi cung ứng. |
| Kỹ năng | Supply Chain, Excel, SQL, quản lý vận hành |
| Ngoại ngữ | Tiếng Anh B2 |
| Chứng chỉ | CSCP, Excel nâng cao hoặc chứng chỉ logistics |
| Dự án | Dự án portfolio 055: xây dựng giải pháp thử nghiệm cho chuỗi cung ứng. |
| Giải thưởng | Giải thưởng đồ án cấp khoa |
| Hoạt động | CLB Logistics và Quản trị; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-055","linkedin":"https://www.linkedin.com/in/seed-student-055"} |
| Portfolio | https://portfolio.study2work.dev/student-055 |
| Mức lương mong muốn | 10-23 triệu VNĐ/tháng |
| sinhvien_id | 63 |
| created_at | 2026-09-16T14:43:26.904Z |

### Sinh viên 056 — Huỳnh Thu Khang

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 64 |
| Họ tên | Huỳnh Thu Khang |
| Email | seed.student.056@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Logistics |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 59 |
| Họ tên | Huỳnh Thu Khang |
| Ngày sinh | 1998-06-10T00:00:00.000Z |
| Giới tính | Nữ |
| Email CV | seed.student.056@study2work.dev |
| Số điện thoại | 0903000056 |
| Địa chỉ | Bình Dương, Việt Nam |
| Vị trí | Logistics Operations Coordinator |
| Ngành | Logistics |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Logistics với vai trò Logistics Operations Coordinator. |
| Học vấn | Đại học chuyên ngành Logistics, Kinh tế hoặc Kỹ thuật |
| Kinh nghiệm | 2 năm kinh nghiệm thực tế trong lĩnh vực chuỗi cung ứng. |
| Kỹ năng | Supply Chain, Excel, SQL, quản lý vận hành |
| Ngoại ngữ | Tiếng Anh giao tiếp |
| Chứng chỉ | CSCP, Excel nâng cao hoặc chứng chỉ logistics |
| Dự án | Dự án portfolio 056: xây dựng giải pháp thử nghiệm cho chuỗi cung ứng. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Logistics và Quản trị; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-056","linkedin":"https://www.linkedin.com/in/seed-student-056"} |
| Portfolio | https://portfolio.study2work.dev/student-056 |
| Mức lương mong muốn | 10-23 triệu VNĐ/tháng |
| sinhvien_id | 64 |
| created_at | 2026-09-16T14:43:27.411Z |

### Sinh viên 057 — Huỳnh Đức Linh

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 65 |
| Họ tên | Huỳnh Đức Linh |
| Email | seed.student.057@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Logistics |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 60 |
| Họ tên | Huỳnh Đức Linh |
| Ngày sinh | 1999-06-11T00:00:00.000Z |
| Giới tính | Nam |
| Email CV | seed.student.057@study2work.dev |
| Số điện thoại | 0903000057 |
| Địa chỉ | Bình Dương, Việt Nam |
| Vị trí | Fleet Technology Product Specialist |
| Ngành | Logistics |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Logistics với vai trò Fleet Technology Product Specialist. |
| Học vấn | Đại học chuyên ngành Logistics, Kinh tế hoặc Kỹ thuật |
| Kinh nghiệm | Fresher; hoàn thành dự án học thuật và 6 tháng thực tập. |
| Kỹ năng | Supply Chain, Excel, SQL, quản lý vận hành |
| Ngoại ngữ | Tiếng Anh B1 |
| Chứng chỉ | CSCP, Excel nâng cao hoặc chứng chỉ logistics |
| Dự án | Dự án portfolio 057: xây dựng giải pháp thử nghiệm cho chuỗi cung ứng. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Logistics và Quản trị; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-057","linkedin":"https://www.linkedin.com/in/seed-student-057"} |
| Portfolio | https://portfolio.study2work.dev/student-057 |
| Mức lương mong muốn | 10-23 triệu VNĐ/tháng |
| sinhvien_id | 65 |
| created_at | 2026-09-16T14:43:27.925Z |

### Sinh viên 058 — Huỳnh Quỳnh Nam

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 66 |
| Họ tên | Huỳnh Quỳnh Nam |
| Email | seed.student.058@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Logistics |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 61 |
| Họ tên | Huỳnh Quỳnh Nam |
| Ngày sinh | 2000-06-12T00:00:00.000Z |
| Giới tính | Nữ |
| Email CV | seed.student.058@study2work.dev |
| Số điện thoại | 0903000058 |
| Địa chỉ | Bình Dương, Việt Nam |
| Vị trí | Warehouse Process Engineer |
| Ngành | Logistics |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Logistics với vai trò Warehouse Process Engineer. |
| Học vấn | Đại học chuyên ngành Logistics, Kinh tế hoặc Kỹ thuật |
| Kinh nghiệm | 1 năm kinh nghiệm liên quan đến chuỗi cung ứng. |
| Kỹ năng | Supply Chain, Excel, SQL, quản lý vận hành |
| Ngoại ngữ | Tiếng Anh B2 |
| Chứng chỉ | CSCP, Excel nâng cao hoặc chứng chỉ logistics |
| Dự án | Dự án portfolio 058: xây dựng giải pháp thử nghiệm cho chuỗi cung ứng. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Logistics và Quản trị; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-058","linkedin":"https://www.linkedin.com/in/seed-student-058"} |
| Portfolio | https://portfolio.study2work.dev/student-058 |
| Mức lương mong muốn | 10-23 triệu VNĐ/tháng |
| sinhvien_id | 66 |
| created_at | 2026-09-16T14:43:28.484Z |

### Sinh viên 059 — Huỳnh Hải Phương

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 67 |
| Họ tên | Huỳnh Hải Phương |
| Email | seed.student.059@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Logistics |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 62 |
| Họ tên | Huỳnh Hải Phương |
| Ngày sinh | 2001-06-13T00:00:00.000Z |
| Giới tính | Nam |
| Email CV | seed.student.059@study2work.dev |
| Số điện thoại | 0903000059 |
| Địa chỉ | Bình Dương, Việt Nam |
| Vị trí | Supply Chain Analyst |
| Ngành | Logistics |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Logistics với vai trò Supply Chain Analyst. |
| Học vấn | Đại học chuyên ngành Logistics, Kinh tế hoặc Kỹ thuật |
| Kinh nghiệm | 2 năm kinh nghiệm thực tế trong lĩnh vực chuỗi cung ứng. |
| Kỹ năng | Supply Chain, Excel, SQL, quản lý vận hành |
| Ngoại ngữ | Tiếng Anh giao tiếp |
| Chứng chỉ | CSCP, Excel nâng cao hoặc chứng chỉ logistics |
| Dự án | Dự án portfolio 059: xây dựng giải pháp thử nghiệm cho chuỗi cung ứng. |
| Giải thưởng | Giải thưởng đồ án cấp khoa |
| Hoạt động | CLB Logistics và Quản trị; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-059","linkedin":"https://www.linkedin.com/in/seed-student-059"} |
| Portfolio | https://portfolio.study2work.dev/student-059 |
| Mức lương mong muốn | 10-23 triệu VNĐ/tháng |
| sinhvien_id | 67 |
| created_at | 2026-09-16T14:43:28.998Z |

### Sinh viên 060 — Huỳnh Bảo Quân

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 68 |
| Họ tên | Huỳnh Bảo Quân |
| Email | seed.student.060@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Logistics |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 63 |
| Họ tên | Huỳnh Bảo Quân |
| Ngày sinh | 2002-06-14T00:00:00.000Z |
| Giới tính | Nữ |
| Email CV | seed.student.060@study2work.dev |
| Số điện thoại | 0903000060 |
| Địa chỉ | Bình Dương, Việt Nam |
| Vị trí | Logistics Operations Coordinator |
| Ngành | Logistics |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Logistics với vai trò Logistics Operations Coordinator. |
| Học vấn | Đại học chuyên ngành Logistics, Kinh tế hoặc Kỹ thuật |
| Kinh nghiệm | Fresher; hoàn thành dự án học thuật và 6 tháng thực tập. |
| Kỹ năng | Supply Chain, Excel, SQL, quản lý vận hành |
| Ngoại ngữ | Tiếng Anh B1 |
| Chứng chỉ | CSCP, Excel nâng cao hoặc chứng chỉ logistics |
| Dự án | Dự án portfolio 060: xây dựng giải pháp thử nghiệm cho chuỗi cung ứng. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Logistics và Quản trị; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-060","linkedin":"https://www.linkedin.com/in/seed-student-060"} |
| Portfolio | https://portfolio.study2work.dev/student-060 |
| Mức lương mong muốn | 10-23 triệu VNĐ/tháng |
| sinhvien_id | 68 |
| created_at | 2026-09-16T14:43:29.509Z |

### Sinh viên 061 — Phan Minh An

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 69 |
| Họ tên | Phan Minh An |
| Email | seed.student.061@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Sản xuất |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 64 |
| Họ tên | Phan Minh An |
| Ngày sinh | 1998-07-05T00:00:00.000Z |
| Giới tính | Nam |
| Email CV | seed.student.061@study2work.dev |
| Số điện thoại | 0903000061 |
| Địa chỉ | Đồng Nai, Việt Nam |
| Vị trí | Production Planning Engineer |
| Ngành | Sản xuất |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Sản xuất với vai trò Production Planning Engineer. |
| Học vấn | Đại học chuyên ngành Kỹ thuật, Cơ khí hoặc Quản lý công nghiệp |
| Kinh nghiệm | Fresher; hoàn thành dự án học thuật và 6 tháng thực tập. |
| Kỹ năng | Lean, AutoCAD, Excel, kiểm soát chất lượng |
| Ngoại ngữ | Tiếng Anh B1 |
| Chứng chỉ | Lean Six Sigma hoặc chứng chỉ quản lý chất lượng |
| Dự án | Dự án portfolio 061: xây dựng giải pháp thử nghiệm cho sản xuất công nghiệp. |
| Giải thưởng | Giải thưởng đồ án cấp khoa |
| Hoạt động | CLB Kỹ thuật và Sáng tạo; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-061","linkedin":"https://www.linkedin.com/in/seed-student-061"} |
| Portfolio | https://portfolio.study2work.dev/student-061 |
| Mức lương mong muốn | 12-26 triệu VNĐ/tháng |
| sinhvien_id | 69 |
| created_at | 2026-09-16T14:43:30.023Z |

### Sinh viên 062 — Phan Ngọc Bình

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 70 |
| Họ tên | Phan Ngọc Bình |
| Email | seed.student.062@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Sản xuất |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 65 |
| Họ tên | Phan Ngọc Bình |
| Ngày sinh | 1999-07-06T00:00:00.000Z |
| Giới tính | Nữ |
| Email CV | seed.student.062@study2work.dev |
| Số điện thoại | 0903000062 |
| Địa chỉ | Đồng Nai, Việt Nam |
| Vị trí | Quality Assurance Engineer |
| Ngành | Sản xuất |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Sản xuất với vai trò Quality Assurance Engineer. |
| Học vấn | Đại học chuyên ngành Kỹ thuật, Cơ khí hoặc Quản lý công nghiệp |
| Kinh nghiệm | 1 năm kinh nghiệm liên quan đến sản xuất công nghiệp. |
| Kỹ năng | Lean, AutoCAD, Excel, kiểm soát chất lượng |
| Ngoại ngữ | Tiếng Anh B2 |
| Chứng chỉ | Lean Six Sigma hoặc chứng chỉ quản lý chất lượng |
| Dự án | Dự án portfolio 062: xây dựng giải pháp thử nghiệm cho sản xuất công nghiệp. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Kỹ thuật và Sáng tạo; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-062","linkedin":"https://www.linkedin.com/in/seed-student-062"} |
| Portfolio | https://portfolio.study2work.dev/student-062 |
| Mức lương mong muốn | 12-26 triệu VNĐ/tháng |
| sinhvien_id | 70 |
| created_at | 2026-09-16T14:43:30.619Z |

### Sinh viên 063 — Phan Gia Chi

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 71 |
| Họ tên | Phan Gia Chi |
| Email | seed.student.063@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Sản xuất |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 66 |
| Họ tên | Phan Gia Chi |
| Ngày sinh | 2000-07-07T00:00:00.000Z |
| Giới tính | Nam |
| Email CV | seed.student.063@study2work.dev |
| Số điện thoại | 0903000063 |
| Địa chỉ | Đồng Nai, Việt Nam |
| Vị trí | Industrial Automation Engineer |
| Ngành | Sản xuất |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Sản xuất với vai trò Industrial Automation Engineer. |
| Học vấn | Đại học chuyên ngành Kỹ thuật, Cơ khí hoặc Quản lý công nghiệp |
| Kinh nghiệm | 2 năm kinh nghiệm thực tế trong lĩnh vực sản xuất công nghiệp. |
| Kỹ năng | Lean, AutoCAD, Excel, kiểm soát chất lượng |
| Ngoại ngữ | Tiếng Anh giao tiếp |
| Chứng chỉ | Lean Six Sigma hoặc chứng chỉ quản lý chất lượng |
| Dự án | Dự án portfolio 063: xây dựng giải pháp thử nghiệm cho sản xuất công nghiệp. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Kỹ thuật và Sáng tạo; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-063","linkedin":"https://www.linkedin.com/in/seed-student-063"} |
| Portfolio | https://portfolio.study2work.dev/student-063 |
| Mức lương mong muốn | 12-26 triệu VNĐ/tháng |
| sinhvien_id | 71 |
| created_at | 2026-09-16T14:43:31.116Z |

### Sinh viên 064 — Phan Thanh Dũng

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 72 |
| Họ tên | Phan Thanh Dũng |
| Email | seed.student.064@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Sản xuất |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 67 |
| Họ tên | Phan Thanh Dũng |
| Ngày sinh | 2001-07-08T00:00:00.000Z |
| Giới tính | Nữ |
| Email CV | seed.student.064@study2work.dev |
| Số điện thoại | 0903000064 |
| Địa chỉ | Đồng Nai, Việt Nam |
| Vị trí | Procurement Specialist |
| Ngành | Sản xuất |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Sản xuất với vai trò Procurement Specialist. |
| Học vấn | Đại học chuyên ngành Kỹ thuật, Cơ khí hoặc Quản lý công nghiệp |
| Kinh nghiệm | Fresher; hoàn thành dự án học thuật và 6 tháng thực tập. |
| Kỹ năng | Lean, AutoCAD, Excel, kiểm soát chất lượng |
| Ngoại ngữ | Tiếng Anh B1 |
| Chứng chỉ | Lean Six Sigma hoặc chứng chỉ quản lý chất lượng |
| Dự án | Dự án portfolio 064: xây dựng giải pháp thử nghiệm cho sản xuất công nghiệp. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Kỹ thuật và Sáng tạo; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-064","linkedin":"https://www.linkedin.com/in/seed-student-064"} |
| Portfolio | https://portfolio.study2work.dev/student-064 |
| Mức lương mong muốn | 12-26 triệu VNĐ/tháng |
| sinhvien_id | 72 |
| created_at | 2026-09-16T14:43:31.632Z |

### Sinh viên 065 — Phan Khánh Hà

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 73 |
| Họ tên | Phan Khánh Hà |
| Email | seed.student.065@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Sản xuất |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 68 |
| Họ tên | Phan Khánh Hà |
| Ngày sinh | 2002-07-09T00:00:00.000Z |
| Giới tính | Nam |
| Email CV | seed.student.065@study2work.dev |
| Số điện thoại | 0903000065 |
| Địa chỉ | Đồng Nai, Việt Nam |
| Vị trí | Production Planning Engineer |
| Ngành | Sản xuất |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Sản xuất với vai trò Production Planning Engineer. |
| Học vấn | Đại học chuyên ngành Kỹ thuật, Cơ khí hoặc Quản lý công nghiệp |
| Kinh nghiệm | 1 năm kinh nghiệm liên quan đến sản xuất công nghiệp. |
| Kỹ năng | Lean, AutoCAD, Excel, kiểm soát chất lượng |
| Ngoại ngữ | Tiếng Anh B2 |
| Chứng chỉ | Lean Six Sigma hoặc chứng chỉ quản lý chất lượng |
| Dự án | Dự án portfolio 065: xây dựng giải pháp thử nghiệm cho sản xuất công nghiệp. |
| Giải thưởng | Giải thưởng đồ án cấp khoa |
| Hoạt động | CLB Kỹ thuật và Sáng tạo; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-065","linkedin":"https://www.linkedin.com/in/seed-student-065"} |
| Portfolio | https://portfolio.study2work.dev/student-065 |
| Mức lương mong muốn | 12-26 triệu VNĐ/tháng |
| sinhvien_id | 73 |
| created_at | 2026-09-16T14:43:32.170Z |

### Sinh viên 066 — Phan Thu Khang

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 74 |
| Họ tên | Phan Thu Khang |
| Email | seed.student.066@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Sản xuất |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 69 |
| Họ tên | Phan Thu Khang |
| Ngày sinh | 1998-07-10T00:00:00.000Z |
| Giới tính | Nữ |
| Email CV | seed.student.066@study2work.dev |
| Số điện thoại | 0903000066 |
| Địa chỉ | Đồng Nai, Việt Nam |
| Vị trí | Quality Assurance Engineer |
| Ngành | Sản xuất |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Sản xuất với vai trò Quality Assurance Engineer. |
| Học vấn | Đại học chuyên ngành Kỹ thuật, Cơ khí hoặc Quản lý công nghiệp |
| Kinh nghiệm | 2 năm kinh nghiệm thực tế trong lĩnh vực sản xuất công nghiệp. |
| Kỹ năng | Lean, AutoCAD, Excel, kiểm soát chất lượng |
| Ngoại ngữ | Tiếng Anh giao tiếp |
| Chứng chỉ | Lean Six Sigma hoặc chứng chỉ quản lý chất lượng |
| Dự án | Dự án portfolio 066: xây dựng giải pháp thử nghiệm cho sản xuất công nghiệp. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Kỹ thuật và Sáng tạo; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-066","linkedin":"https://www.linkedin.com/in/seed-student-066"} |
| Portfolio | https://portfolio.study2work.dev/student-066 |
| Mức lương mong muốn | 12-26 triệu VNĐ/tháng |
| sinhvien_id | 74 |
| created_at | 2026-09-16T14:43:32.685Z |

### Sinh viên 067 — Phan Đức Linh

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 75 |
| Họ tên | Phan Đức Linh |
| Email | seed.student.067@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Sản xuất |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 70 |
| Họ tên | Phan Đức Linh |
| Ngày sinh | 1999-07-11T00:00:00.000Z |
| Giới tính | Nam |
| Email CV | seed.student.067@study2work.dev |
| Số điện thoại | 0903000067 |
| Địa chỉ | Đồng Nai, Việt Nam |
| Vị trí | Industrial Automation Engineer |
| Ngành | Sản xuất |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Sản xuất với vai trò Industrial Automation Engineer. |
| Học vấn | Đại học chuyên ngành Kỹ thuật, Cơ khí hoặc Quản lý công nghiệp |
| Kinh nghiệm | Fresher; hoàn thành dự án học thuật và 6 tháng thực tập. |
| Kỹ năng | Lean, AutoCAD, Excel, kiểm soát chất lượng |
| Ngoại ngữ | Tiếng Anh B1 |
| Chứng chỉ | Lean Six Sigma hoặc chứng chỉ quản lý chất lượng |
| Dự án | Dự án portfolio 067: xây dựng giải pháp thử nghiệm cho sản xuất công nghiệp. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Kỹ thuật và Sáng tạo; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-067","linkedin":"https://www.linkedin.com/in/seed-student-067"} |
| Portfolio | https://portfolio.study2work.dev/student-067 |
| Mức lương mong muốn | 12-26 triệu VNĐ/tháng |
| sinhvien_id | 75 |
| created_at | 2026-09-16T14:43:33.198Z |

### Sinh viên 068 — Phan Quỳnh Nam

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 76 |
| Họ tên | Phan Quỳnh Nam |
| Email | seed.student.068@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Sản xuất |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 71 |
| Họ tên | Phan Quỳnh Nam |
| Ngày sinh | 2000-07-12T00:00:00.000Z |
| Giới tính | Nữ |
| Email CV | seed.student.068@study2work.dev |
| Số điện thoại | 0903000068 |
| Địa chỉ | Đồng Nai, Việt Nam |
| Vị trí | Procurement Specialist |
| Ngành | Sản xuất |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Sản xuất với vai trò Procurement Specialist. |
| Học vấn | Đại học chuyên ngành Kỹ thuật, Cơ khí hoặc Quản lý công nghiệp |
| Kinh nghiệm | 1 năm kinh nghiệm liên quan đến sản xuất công nghiệp. |
| Kỹ năng | Lean, AutoCAD, Excel, kiểm soát chất lượng |
| Ngoại ngữ | Tiếng Anh B2 |
| Chứng chỉ | Lean Six Sigma hoặc chứng chỉ quản lý chất lượng |
| Dự án | Dự án portfolio 068: xây dựng giải pháp thử nghiệm cho sản xuất công nghiệp. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Kỹ thuật và Sáng tạo; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-068","linkedin":"https://www.linkedin.com/in/seed-student-068"} |
| Portfolio | https://portfolio.study2work.dev/student-068 |
| Mức lương mong muốn | 12-26 triệu VNĐ/tháng |
| sinhvien_id | 76 |
| created_at | 2026-09-16T14:43:33.759Z |

### Sinh viên 069 — Phan Hải Phương

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 77 |
| Họ tên | Phan Hải Phương |
| Email | seed.student.069@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Sản xuất |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 72 |
| Họ tên | Phan Hải Phương |
| Ngày sinh | 2001-07-13T00:00:00.000Z |
| Giới tính | Nam |
| Email CV | seed.student.069@study2work.dev |
| Số điện thoại | 0903000069 |
| Địa chỉ | Đồng Nai, Việt Nam |
| Vị trí | Production Planning Engineer |
| Ngành | Sản xuất |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Sản xuất với vai trò Production Planning Engineer. |
| Học vấn | Đại học chuyên ngành Kỹ thuật, Cơ khí hoặc Quản lý công nghiệp |
| Kinh nghiệm | 2 năm kinh nghiệm thực tế trong lĩnh vực sản xuất công nghiệp. |
| Kỹ năng | Lean, AutoCAD, Excel, kiểm soát chất lượng |
| Ngoại ngữ | Tiếng Anh giao tiếp |
| Chứng chỉ | Lean Six Sigma hoặc chứng chỉ quản lý chất lượng |
| Dự án | Dự án portfolio 069: xây dựng giải pháp thử nghiệm cho sản xuất công nghiệp. |
| Giải thưởng | Giải thưởng đồ án cấp khoa |
| Hoạt động | CLB Kỹ thuật và Sáng tạo; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-069","linkedin":"https://www.linkedin.com/in/seed-student-069"} |
| Portfolio | https://portfolio.study2work.dev/student-069 |
| Mức lương mong muốn | 12-26 triệu VNĐ/tháng |
| sinhvien_id | 77 |
| created_at | 2026-09-16T14:43:34.348Z |

### Sinh viên 070 — Phan Bảo Quân

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 78 |
| Họ tên | Phan Bảo Quân |
| Email | seed.student.070@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Sản xuất |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 73 |
| Họ tên | Phan Bảo Quân |
| Ngày sinh | 2002-07-14T00:00:00.000Z |
| Giới tính | Nữ |
| Email CV | seed.student.070@study2work.dev |
| Số điện thoại | 0903000070 |
| Địa chỉ | Đồng Nai, Việt Nam |
| Vị trí | Quality Assurance Engineer |
| Ngành | Sản xuất |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Sản xuất với vai trò Quality Assurance Engineer. |
| Học vấn | Đại học chuyên ngành Kỹ thuật, Cơ khí hoặc Quản lý công nghiệp |
| Kinh nghiệm | Fresher; hoàn thành dự án học thuật và 6 tháng thực tập. |
| Kỹ năng | Lean, AutoCAD, Excel, kiểm soát chất lượng |
| Ngoại ngữ | Tiếng Anh B1 |
| Chứng chỉ | Lean Six Sigma hoặc chứng chỉ quản lý chất lượng |
| Dự án | Dự án portfolio 070: xây dựng giải pháp thử nghiệm cho sản xuất công nghiệp. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Kỹ thuật và Sáng tạo; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-070","linkedin":"https://www.linkedin.com/in/seed-student-070"} |
| Portfolio | https://portfolio.study2work.dev/student-070 |
| Mức lương mong muốn | 12-26 triệu VNĐ/tháng |
| sinhvien_id | 78 |
| created_at | 2026-09-16T14:43:34.851Z |

### Sinh viên 071 — Vũ Minh An

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 79 |
| Họ tên | Vũ Minh An |
| Email | seed.student.071@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Y tế - Chăm sóc sức khỏe |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 74 |
| Họ tên | Vũ Minh An |
| Ngày sinh | 1998-08-05T00:00:00.000Z |
| Giới tính | Nam |
| Email CV | seed.student.071@study2work.dev |
| Số điện thoại | 0903000071 |
| Địa chỉ | Huế, Việt Nam |
| Vị trí | Healthcare Product Specialist |
| Ngành | Y tế - Chăm sóc sức khỏe |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Y tế - Chăm sóc sức khỏe với vai trò Healthcare Product Specialist. |
| Học vấn | Đại học chuyên ngành Y tế, Dữ liệu, CNTT hoặc Kinh doanh |
| Kinh nghiệm | Fresher; hoàn thành dự án học thuật và 6 tháng thực tập. |
| Kỹ năng | SQL, phân tích dữ liệu, quy trình y tế, giao tiếp |
| Ngoại ngữ | Tiếng Anh B1 |
| Chứng chỉ | Health Informatics hoặc chứng chỉ phân tích dữ liệu |
| Dự án | Dự án portfolio 071: xây dựng giải pháp thử nghiệm cho chăm sóc sức khỏe số. |
| Giải thưởng | Giải thưởng đồ án cấp khoa |
| Hoạt động | CLB Sức khỏe và Công nghệ; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-071","linkedin":"https://www.linkedin.com/in/seed-student-071"} |
| Portfolio | https://portfolio.study2work.dev/student-071 |
| Mức lương mong muốn | 11-25 triệu VNĐ/tháng |
| sinhvien_id | 79 |
| created_at | 2026-09-16T14:43:35.351Z |

### Sinh viên 072 — Vũ Ngọc Bình

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 80 |
| Họ tên | Vũ Ngọc Bình |
| Email | seed.student.072@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Y tế - Chăm sóc sức khỏe |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 75 |
| Họ tên | Vũ Ngọc Bình |
| Ngày sinh | 1999-08-06T00:00:00.000Z |
| Giới tính | Nữ |
| Email CV | seed.student.072@study2work.dev |
| Số điện thoại | 0903000072 |
| Địa chỉ | Huế, Việt Nam |
| Vị trí | Clinical Data Analyst |
| Ngành | Y tế - Chăm sóc sức khỏe |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Y tế - Chăm sóc sức khỏe với vai trò Clinical Data Analyst. |
| Học vấn | Đại học chuyên ngành Y tế, Dữ liệu, CNTT hoặc Kinh doanh |
| Kinh nghiệm | 1 năm kinh nghiệm liên quan đến chăm sóc sức khỏe số. |
| Kỹ năng | SQL, phân tích dữ liệu, quy trình y tế, giao tiếp |
| Ngoại ngữ | Tiếng Anh B2 |
| Chứng chỉ | Health Informatics hoặc chứng chỉ phân tích dữ liệu |
| Dự án | Dự án portfolio 072: xây dựng giải pháp thử nghiệm cho chăm sóc sức khỏe số. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Sức khỏe và Công nghệ; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-072","linkedin":"https://www.linkedin.com/in/seed-student-072"} |
| Portfolio | https://portfolio.study2work.dev/student-072 |
| Mức lương mong muốn | 11-25 triệu VNĐ/tháng |
| sinhvien_id | 80 |
| created_at | 2026-09-16T14:43:35.882Z |

### Sinh viên 073 — Vũ Gia Chi

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 81 |
| Họ tên | Vũ Gia Chi |
| Email | seed.student.073@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Y tế - Chăm sóc sức khỏe |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 76 |
| Họ tên | Vũ Gia Chi |
| Ngày sinh | 2000-08-07T00:00:00.000Z |
| Giới tính | Nam |
| Email CV | seed.student.073@study2work.dev |
| Số điện thoại | 0903000073 |
| Địa chỉ | Huế, Việt Nam |
| Vị trí | Backend Engineer |
| Ngành | Y tế - Chăm sóc sức khỏe |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Y tế - Chăm sóc sức khỏe với vai trò Backend Engineer. |
| Học vấn | Đại học chuyên ngành Y tế, Dữ liệu, CNTT hoặc Kinh doanh |
| Kinh nghiệm | 2 năm kinh nghiệm thực tế trong lĩnh vực chăm sóc sức khỏe số. |
| Kỹ năng | SQL, phân tích dữ liệu, quy trình y tế, giao tiếp |
| Ngoại ngữ | Tiếng Anh giao tiếp |
| Chứng chỉ | Health Informatics hoặc chứng chỉ phân tích dữ liệu |
| Dự án | Dự án portfolio 073: xây dựng giải pháp thử nghiệm cho chăm sóc sức khỏe số. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Sức khỏe và Công nghệ; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-073","linkedin":"https://www.linkedin.com/in/seed-student-073"} |
| Portfolio | https://portfolio.study2work.dev/student-073 |
| Mức lương mong muốn | 11-25 triệu VNĐ/tháng |
| sinhvien_id | 81 |
| created_at | 2026-09-16T14:43:36.383Z |

### Sinh viên 074 — Vũ Thanh Dũng

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 82 |
| Họ tên | Vũ Thanh Dũng |
| Email | seed.student.074@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Y tế - Chăm sóc sức khỏe |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 77 |
| Họ tên | Vũ Thanh Dũng |
| Ngày sinh | 2001-08-08T00:00:00.000Z |
| Giới tính | Nữ |
| Email CV | seed.student.074@study2work.dev |
| Số điện thoại | 0903000074 |
| Địa chỉ | Huế, Việt Nam |
| Vị trí | Customer Care Supervisor |
| Ngành | Y tế - Chăm sóc sức khỏe |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Y tế - Chăm sóc sức khỏe với vai trò Customer Care Supervisor. |
| Học vấn | Đại học chuyên ngành Y tế, Dữ liệu, CNTT hoặc Kinh doanh |
| Kinh nghiệm | Fresher; hoàn thành dự án học thuật và 6 tháng thực tập. |
| Kỹ năng | SQL, phân tích dữ liệu, quy trình y tế, giao tiếp |
| Ngoại ngữ | Tiếng Anh B1 |
| Chứng chỉ | Health Informatics hoặc chứng chỉ phân tích dữ liệu |
| Dự án | Dự án portfolio 074: xây dựng giải pháp thử nghiệm cho chăm sóc sức khỏe số. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Sức khỏe và Công nghệ; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-074","linkedin":"https://www.linkedin.com/in/seed-student-074"} |
| Portfolio | https://portfolio.study2work.dev/student-074 |
| Mức lương mong muốn | 11-25 triệu VNĐ/tháng |
| sinhvien_id | 82 |
| created_at | 2026-09-16T14:43:36.885Z |

### Sinh viên 075 — Vũ Khánh Hà

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 83 |
| Họ tên | Vũ Khánh Hà |
| Email | seed.student.075@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Y tế - Chăm sóc sức khỏe |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 78 |
| Họ tên | Vũ Khánh Hà |
| Ngày sinh | 2002-08-09T00:00:00.000Z |
| Giới tính | Nam |
| Email CV | seed.student.075@study2work.dev |
| Số điện thoại | 0903000075 |
| Địa chỉ | Huế, Việt Nam |
| Vị trí | Healthcare Product Specialist |
| Ngành | Y tế - Chăm sóc sức khỏe |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Y tế - Chăm sóc sức khỏe với vai trò Healthcare Product Specialist. |
| Học vấn | Đại học chuyên ngành Y tế, Dữ liệu, CNTT hoặc Kinh doanh |
| Kinh nghiệm | 1 năm kinh nghiệm liên quan đến chăm sóc sức khỏe số. |
| Kỹ năng | SQL, phân tích dữ liệu, quy trình y tế, giao tiếp |
| Ngoại ngữ | Tiếng Anh B2 |
| Chứng chỉ | Health Informatics hoặc chứng chỉ phân tích dữ liệu |
| Dự án | Dự án portfolio 075: xây dựng giải pháp thử nghiệm cho chăm sóc sức khỏe số. |
| Giải thưởng | Giải thưởng đồ án cấp khoa |
| Hoạt động | CLB Sức khỏe và Công nghệ; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-075","linkedin":"https://www.linkedin.com/in/seed-student-075"} |
| Portfolio | https://portfolio.study2work.dev/student-075 |
| Mức lương mong muốn | 11-25 triệu VNĐ/tháng |
| sinhvien_id | 83 |
| created_at | 2026-09-16T14:43:37.408Z |

### Sinh viên 076 — Vũ Thu Khang

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 84 |
| Họ tên | Vũ Thu Khang |
| Email | seed.student.076@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Y tế - Chăm sóc sức khỏe |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 79 |
| Họ tên | Vũ Thu Khang |
| Ngày sinh | 1998-08-10T00:00:00.000Z |
| Giới tính | Nữ |
| Email CV | seed.student.076@study2work.dev |
| Số điện thoại | 0903000076 |
| Địa chỉ | Huế, Việt Nam |
| Vị trí | Clinical Data Analyst |
| Ngành | Y tế - Chăm sóc sức khỏe |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Y tế - Chăm sóc sức khỏe với vai trò Clinical Data Analyst. |
| Học vấn | Đại học chuyên ngành Y tế, Dữ liệu, CNTT hoặc Kinh doanh |
| Kinh nghiệm | 2 năm kinh nghiệm thực tế trong lĩnh vực chăm sóc sức khỏe số. |
| Kỹ năng | SQL, phân tích dữ liệu, quy trình y tế, giao tiếp |
| Ngoại ngữ | Tiếng Anh giao tiếp |
| Chứng chỉ | Health Informatics hoặc chứng chỉ phân tích dữ liệu |
| Dự án | Dự án portfolio 076: xây dựng giải pháp thử nghiệm cho chăm sóc sức khỏe số. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Sức khỏe và Công nghệ; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-076","linkedin":"https://www.linkedin.com/in/seed-student-076"} |
| Portfolio | https://portfolio.study2work.dev/student-076 |
| Mức lương mong muốn | 11-25 triệu VNĐ/tháng |
| sinhvien_id | 84 |
| created_at | 2026-09-16T14:43:37.922Z |

### Sinh viên 077 — Vũ Đức Linh

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 85 |
| Họ tên | Vũ Đức Linh |
| Email | seed.student.077@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Y tế - Chăm sóc sức khỏe |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 80 |
| Họ tên | Vũ Đức Linh |
| Ngày sinh | 1999-08-11T00:00:00.000Z |
| Giới tính | Nam |
| Email CV | seed.student.077@study2work.dev |
| Số điện thoại | 0903000077 |
| Địa chỉ | Huế, Việt Nam |
| Vị trí | Backend Engineer |
| Ngành | Y tế - Chăm sóc sức khỏe |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Y tế - Chăm sóc sức khỏe với vai trò Backend Engineer. |
| Học vấn | Đại học chuyên ngành Y tế, Dữ liệu, CNTT hoặc Kinh doanh |
| Kinh nghiệm | Fresher; hoàn thành dự án học thuật và 6 tháng thực tập. |
| Kỹ năng | SQL, phân tích dữ liệu, quy trình y tế, giao tiếp |
| Ngoại ngữ | Tiếng Anh B1 |
| Chứng chỉ | Health Informatics hoặc chứng chỉ phân tích dữ liệu |
| Dự án | Dự án portfolio 077: xây dựng giải pháp thử nghiệm cho chăm sóc sức khỏe số. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Sức khỏe và Công nghệ; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-077","linkedin":"https://www.linkedin.com/in/seed-student-077"} |
| Portfolio | https://portfolio.study2work.dev/student-077 |
| Mức lương mong muốn | 11-25 triệu VNĐ/tháng |
| sinhvien_id | 85 |
| created_at | 2026-09-16T14:43:38.419Z |

### Sinh viên 078 — Vũ Quỳnh Nam

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 86 |
| Họ tên | Vũ Quỳnh Nam |
| Email | seed.student.078@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Y tế - Chăm sóc sức khỏe |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 81 |
| Họ tên | Vũ Quỳnh Nam |
| Ngày sinh | 2000-08-12T00:00:00.000Z |
| Giới tính | Nữ |
| Email CV | seed.student.078@study2work.dev |
| Số điện thoại | 0903000078 |
| Địa chỉ | Huế, Việt Nam |
| Vị trí | Customer Care Supervisor |
| Ngành | Y tế - Chăm sóc sức khỏe |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Y tế - Chăm sóc sức khỏe với vai trò Customer Care Supervisor. |
| Học vấn | Đại học chuyên ngành Y tế, Dữ liệu, CNTT hoặc Kinh doanh |
| Kinh nghiệm | 1 năm kinh nghiệm liên quan đến chăm sóc sức khỏe số. |
| Kỹ năng | SQL, phân tích dữ liệu, quy trình y tế, giao tiếp |
| Ngoại ngữ | Tiếng Anh B2 |
| Chứng chỉ | Health Informatics hoặc chứng chỉ phân tích dữ liệu |
| Dự án | Dự án portfolio 078: xây dựng giải pháp thử nghiệm cho chăm sóc sức khỏe số. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Sức khỏe và Công nghệ; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-078","linkedin":"https://www.linkedin.com/in/seed-student-078"} |
| Portfolio | https://portfolio.study2work.dev/student-078 |
| Mức lương mong muốn | 11-25 triệu VNĐ/tháng |
| sinhvien_id | 86 |
| created_at | 2026-09-16T14:43:38.941Z |

### Sinh viên 079 — Vũ Hải Phương

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 87 |
| Họ tên | Vũ Hải Phương |
| Email | seed.student.079@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Y tế - Chăm sóc sức khỏe |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 82 |
| Họ tên | Vũ Hải Phương |
| Ngày sinh | 2001-08-13T00:00:00.000Z |
| Giới tính | Nam |
| Email CV | seed.student.079@study2work.dev |
| Số điện thoại | 0903000079 |
| Địa chỉ | Huế, Việt Nam |
| Vị trí | Healthcare Product Specialist |
| Ngành | Y tế - Chăm sóc sức khỏe |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Y tế - Chăm sóc sức khỏe với vai trò Healthcare Product Specialist. |
| Học vấn | Đại học chuyên ngành Y tế, Dữ liệu, CNTT hoặc Kinh doanh |
| Kinh nghiệm | 2 năm kinh nghiệm thực tế trong lĩnh vực chăm sóc sức khỏe số. |
| Kỹ năng | SQL, phân tích dữ liệu, quy trình y tế, giao tiếp |
| Ngoại ngữ | Tiếng Anh giao tiếp |
| Chứng chỉ | Health Informatics hoặc chứng chỉ phân tích dữ liệu |
| Dự án | Dự án portfolio 079: xây dựng giải pháp thử nghiệm cho chăm sóc sức khỏe số. |
| Giải thưởng | Giải thưởng đồ án cấp khoa |
| Hoạt động | CLB Sức khỏe và Công nghệ; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-079","linkedin":"https://www.linkedin.com/in/seed-student-079"} |
| Portfolio | https://portfolio.study2work.dev/student-079 |
| Mức lương mong muốn | 11-25 triệu VNĐ/tháng |
| sinhvien_id | 87 |
| created_at | 2026-09-16T14:43:39.455Z |

### Sinh viên 080 — Vũ Bảo Quân

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 88 |
| Họ tên | Vũ Bảo Quân |
| Email | seed.student.080@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Y tế - Chăm sóc sức khỏe |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 83 |
| Họ tên | Vũ Bảo Quân |
| Ngày sinh | 2002-08-14T00:00:00.000Z |
| Giới tính | Nữ |
| Email CV | seed.student.080@study2work.dev |
| Số điện thoại | 0903000080 |
| Địa chỉ | Huế, Việt Nam |
| Vị trí | Clinical Data Analyst |
| Ngành | Y tế - Chăm sóc sức khỏe |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Y tế - Chăm sóc sức khỏe với vai trò Clinical Data Analyst. |
| Học vấn | Đại học chuyên ngành Y tế, Dữ liệu, CNTT hoặc Kinh doanh |
| Kinh nghiệm | Fresher; hoàn thành dự án học thuật và 6 tháng thực tập. |
| Kỹ năng | SQL, phân tích dữ liệu, quy trình y tế, giao tiếp |
| Ngoại ngữ | Tiếng Anh B1 |
| Chứng chỉ | Health Informatics hoặc chứng chỉ phân tích dữ liệu |
| Dự án | Dự án portfolio 080: xây dựng giải pháp thử nghiệm cho chăm sóc sức khỏe số. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Sức khỏe và Công nghệ; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-080","linkedin":"https://www.linkedin.com/in/seed-student-080"} |
| Portfolio | https://portfolio.study2work.dev/student-080 |
| Mức lương mong muốn | 11-25 triệu VNĐ/tháng |
| sinhvien_id | 88 |
| created_at | 2026-09-16T14:43:39.964Z |

### Sinh viên 081 — Võ Minh An

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 89 |
| Họ tên | Võ Minh An |
| Email | seed.student.081@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Du lịch - Khách sạn |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 84 |
| Họ tên | Võ Minh An |
| Ngày sinh | 1998-09-05T00:00:00.000Z |
| Giới tính | Nam |
| Email CV | seed.student.081@study2work.dev |
| Số điện thoại | 0903000081 |
| Địa chỉ | Nha Trang, Việt Nam |
| Vị trí | Travel Consultant |
| Ngành | Du lịch - Khách sạn |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Du lịch - Khách sạn với vai trò Travel Consultant. |
| Học vấn | Cao đẳng/Đại học chuyên ngành Du lịch, Khách sạn hoặc Ngoại ngữ |
| Kinh nghiệm | Fresher; hoàn thành dự án học thuật và 6 tháng thực tập. |
| Kỹ năng | Tiếng Anh, bán hàng, chăm sóc khách hàng, Excel |
| Ngoại ngữ | Tiếng Anh B1 |
| Chứng chỉ | IELTS, TOEIC hoặc chứng chỉ nghiệp vụ du lịch |
| Dự án | Dự án portfolio 081: xây dựng giải pháp thử nghiệm cho du lịch và lưu trú. |
| Giải thưởng | Giải thưởng đồ án cấp khoa |
| Hoạt động | CLB Du lịch và Ngoại ngữ; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-081","linkedin":"https://www.linkedin.com/in/seed-student-081"} |
| Portfolio | https://portfolio.study2work.dev/student-081 |
| Mức lương mong muốn | 8-18 triệu VNĐ/tháng |
| sinhvien_id | 89 |
| created_at | 2026-09-16T14:43:40.471Z |

### Sinh viên 082 — Võ Ngọc Bình

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 90 |
| Họ tên | Võ Ngọc Bình |
| Email | seed.student.082@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Du lịch - Khách sạn |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 85 |
| Họ tên | Võ Ngọc Bình |
| Ngày sinh | 1999-09-06T00:00:00.000Z |
| Giới tính | Nữ |
| Email CV | seed.student.082@study2work.dev |
| Số điện thoại | 0903000082 |
| Địa chỉ | Nha Trang, Việt Nam |
| Vị trí | Hotel Operations Executive |
| Ngành | Du lịch - Khách sạn |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Du lịch - Khách sạn với vai trò Hotel Operations Executive. |
| Học vấn | Cao đẳng/Đại học chuyên ngành Du lịch, Khách sạn hoặc Ngoại ngữ |
| Kinh nghiệm | 1 năm kinh nghiệm liên quan đến du lịch và lưu trú. |
| Kỹ năng | Tiếng Anh, bán hàng, chăm sóc khách hàng, Excel |
| Ngoại ngữ | Tiếng Anh B2 |
| Chứng chỉ | IELTS, TOEIC hoặc chứng chỉ nghiệp vụ du lịch |
| Dự án | Dự án portfolio 082: xây dựng giải pháp thử nghiệm cho du lịch và lưu trú. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Du lịch và Ngoại ngữ; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-082","linkedin":"https://www.linkedin.com/in/seed-student-082"} |
| Portfolio | https://portfolio.study2work.dev/student-082 |
| Mức lương mong muốn | 8-18 triệu VNĐ/tháng |
| sinhvien_id | 90 |
| created_at | 2026-09-16T14:43:40.986Z |

### Sinh viên 083 — Võ Gia Chi

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 91 |
| Họ tên | Võ Gia Chi |
| Email | seed.student.083@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Du lịch - Khách sạn |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 86 |
| Họ tên | Võ Gia Chi |
| Ngày sinh | 2000-09-07T00:00:00.000Z |
| Giới tính | Nam |
| Email CV | seed.student.083@study2work.dev |
| Số điện thoại | 0903000083 |
| Địa chỉ | Nha Trang, Việt Nam |
| Vị trí | Digital Marketing Executive |
| Ngành | Du lịch - Khách sạn |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Du lịch - Khách sạn với vai trò Digital Marketing Executive. |
| Học vấn | Cao đẳng/Đại học chuyên ngành Du lịch, Khách sạn hoặc Ngoại ngữ |
| Kinh nghiệm | 2 năm kinh nghiệm thực tế trong lĩnh vực du lịch và lưu trú. |
| Kỹ năng | Tiếng Anh, bán hàng, chăm sóc khách hàng, Excel |
| Ngoại ngữ | Tiếng Anh giao tiếp |
| Chứng chỉ | IELTS, TOEIC hoặc chứng chỉ nghiệp vụ du lịch |
| Dự án | Dự án portfolio 083: xây dựng giải pháp thử nghiệm cho du lịch và lưu trú. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Du lịch và Ngoại ngữ; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-083","linkedin":"https://www.linkedin.com/in/seed-student-083"} |
| Portfolio | https://portfolio.study2work.dev/student-083 |
| Mức lương mong muốn | 8-18 triệu VNĐ/tháng |
| sinhvien_id | 91 |
| created_at | 2026-09-16T14:43:41.497Z |

### Sinh viên 084 — Võ Thanh Dũng

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 92 |
| Họ tên | Võ Thanh Dũng |
| Email | seed.student.084@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Du lịch - Khách sạn |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 87 |
| Họ tên | Võ Thanh Dũng |
| Ngày sinh | 2001-09-08T00:00:00.000Z |
| Giới tính | Nữ |
| Email CV | seed.student.084@study2work.dev |
| Số điện thoại | 0903000084 |
| Địa chỉ | Nha Trang, Việt Nam |
| Vị trí | Front Office Supervisor |
| Ngành | Du lịch - Khách sạn |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Du lịch - Khách sạn với vai trò Front Office Supervisor. |
| Học vấn | Cao đẳng/Đại học chuyên ngành Du lịch, Khách sạn hoặc Ngoại ngữ |
| Kinh nghiệm | Fresher; hoàn thành dự án học thuật và 6 tháng thực tập. |
| Kỹ năng | Tiếng Anh, bán hàng, chăm sóc khách hàng, Excel |
| Ngoại ngữ | Tiếng Anh B1 |
| Chứng chỉ | IELTS, TOEIC hoặc chứng chỉ nghiệp vụ du lịch |
| Dự án | Dự án portfolio 084: xây dựng giải pháp thử nghiệm cho du lịch và lưu trú. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Du lịch và Ngoại ngữ; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-084","linkedin":"https://www.linkedin.com/in/seed-student-084"} |
| Portfolio | https://portfolio.study2work.dev/student-084 |
| Mức lương mong muốn | 8-18 triệu VNĐ/tháng |
| sinhvien_id | 92 |
| created_at | 2026-09-16T14:43:42.001Z |

### Sinh viên 085 — Võ Khánh Hà

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 93 |
| Họ tên | Võ Khánh Hà |
| Email | seed.student.085@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Du lịch - Khách sạn |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 88 |
| Họ tên | Võ Khánh Hà |
| Ngày sinh | 2002-09-09T00:00:00.000Z |
| Giới tính | Nam |
| Email CV | seed.student.085@study2work.dev |
| Số điện thoại | 0903000085 |
| Địa chỉ | Nha Trang, Việt Nam |
| Vị trí | Travel Consultant |
| Ngành | Du lịch - Khách sạn |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Du lịch - Khách sạn với vai trò Travel Consultant. |
| Học vấn | Cao đẳng/Đại học chuyên ngành Du lịch, Khách sạn hoặc Ngoại ngữ |
| Kinh nghiệm | 1 năm kinh nghiệm liên quan đến du lịch và lưu trú. |
| Kỹ năng | Tiếng Anh, bán hàng, chăm sóc khách hàng, Excel |
| Ngoại ngữ | Tiếng Anh B2 |
| Chứng chỉ | IELTS, TOEIC hoặc chứng chỉ nghiệp vụ du lịch |
| Dự án | Dự án portfolio 085: xây dựng giải pháp thử nghiệm cho du lịch và lưu trú. |
| Giải thưởng | Giải thưởng đồ án cấp khoa |
| Hoạt động | CLB Du lịch và Ngoại ngữ; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-085","linkedin":"https://www.linkedin.com/in/seed-student-085"} |
| Portfolio | https://portfolio.study2work.dev/student-085 |
| Mức lương mong muốn | 8-18 triệu VNĐ/tháng |
| sinhvien_id | 93 |
| created_at | 2026-09-16T14:43:42.517Z |

### Sinh viên 086 — Võ Thu Khang

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 94 |
| Họ tên | Võ Thu Khang |
| Email | seed.student.086@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Du lịch - Khách sạn |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 89 |
| Họ tên | Võ Thu Khang |
| Ngày sinh | 1998-09-10T00:00:00.000Z |
| Giới tính | Nữ |
| Email CV | seed.student.086@study2work.dev |
| Số điện thoại | 0903000086 |
| Địa chỉ | Nha Trang, Việt Nam |
| Vị trí | Hotel Operations Executive |
| Ngành | Du lịch - Khách sạn |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Du lịch - Khách sạn với vai trò Hotel Operations Executive. |
| Học vấn | Cao đẳng/Đại học chuyên ngành Du lịch, Khách sạn hoặc Ngoại ngữ |
| Kinh nghiệm | 2 năm kinh nghiệm thực tế trong lĩnh vực du lịch và lưu trú. |
| Kỹ năng | Tiếng Anh, bán hàng, chăm sóc khách hàng, Excel |
| Ngoại ngữ | Tiếng Anh giao tiếp |
| Chứng chỉ | IELTS, TOEIC hoặc chứng chỉ nghiệp vụ du lịch |
| Dự án | Dự án portfolio 086: xây dựng giải pháp thử nghiệm cho du lịch và lưu trú. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Du lịch và Ngoại ngữ; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-086","linkedin":"https://www.linkedin.com/in/seed-student-086"} |
| Portfolio | https://portfolio.study2work.dev/student-086 |
| Mức lương mong muốn | 8-18 triệu VNĐ/tháng |
| sinhvien_id | 94 |
| created_at | 2026-09-16T14:43:43.036Z |

### Sinh viên 087 — Võ Đức Linh

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 95 |
| Họ tên | Võ Đức Linh |
| Email | seed.student.087@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Du lịch - Khách sạn |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 90 |
| Họ tên | Võ Đức Linh |
| Ngày sinh | 1999-09-11T00:00:00.000Z |
| Giới tính | Nam |
| Email CV | seed.student.087@study2work.dev |
| Số điện thoại | 0903000087 |
| Địa chỉ | Nha Trang, Việt Nam |
| Vị trí | Digital Marketing Executive |
| Ngành | Du lịch - Khách sạn |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Du lịch - Khách sạn với vai trò Digital Marketing Executive. |
| Học vấn | Cao đẳng/Đại học chuyên ngành Du lịch, Khách sạn hoặc Ngoại ngữ |
| Kinh nghiệm | Fresher; hoàn thành dự án học thuật và 6 tháng thực tập. |
| Kỹ năng | Tiếng Anh, bán hàng, chăm sóc khách hàng, Excel |
| Ngoại ngữ | Tiếng Anh B1 |
| Chứng chỉ | IELTS, TOEIC hoặc chứng chỉ nghiệp vụ du lịch |
| Dự án | Dự án portfolio 087: xây dựng giải pháp thử nghiệm cho du lịch và lưu trú. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Du lịch và Ngoại ngữ; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-087","linkedin":"https://www.linkedin.com/in/seed-student-087"} |
| Portfolio | https://portfolio.study2work.dev/student-087 |
| Mức lương mong muốn | 8-18 triệu VNĐ/tháng |
| sinhvien_id | 95 |
| created_at | 2026-09-16T14:43:43.536Z |

### Sinh viên 088 — Võ Quỳnh Nam

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 96 |
| Họ tên | Võ Quỳnh Nam |
| Email | seed.student.088@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Du lịch - Khách sạn |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 91 |
| Họ tên | Võ Quỳnh Nam |
| Ngày sinh | 2000-09-12T00:00:00.000Z |
| Giới tính | Nữ |
| Email CV | seed.student.088@study2work.dev |
| Số điện thoại | 0903000088 |
| Địa chỉ | Nha Trang, Việt Nam |
| Vị trí | Front Office Supervisor |
| Ngành | Du lịch - Khách sạn |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Du lịch - Khách sạn với vai trò Front Office Supervisor. |
| Học vấn | Cao đẳng/Đại học chuyên ngành Du lịch, Khách sạn hoặc Ngoại ngữ |
| Kinh nghiệm | 1 năm kinh nghiệm liên quan đến du lịch và lưu trú. |
| Kỹ năng | Tiếng Anh, bán hàng, chăm sóc khách hàng, Excel |
| Ngoại ngữ | Tiếng Anh B2 |
| Chứng chỉ | IELTS, TOEIC hoặc chứng chỉ nghiệp vụ du lịch |
| Dự án | Dự án portfolio 088: xây dựng giải pháp thử nghiệm cho du lịch và lưu trú. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Du lịch và Ngoại ngữ; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-088","linkedin":"https://www.linkedin.com/in/seed-student-088"} |
| Portfolio | https://portfolio.study2work.dev/student-088 |
| Mức lương mong muốn | 8-18 triệu VNĐ/tháng |
| sinhvien_id | 96 |
| created_at | 2026-09-16T14:43:44.058Z |

### Sinh viên 089 — Võ Hải Phương

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 97 |
| Họ tên | Võ Hải Phương |
| Email | seed.student.089@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Du lịch - Khách sạn |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 92 |
| Họ tên | Võ Hải Phương |
| Ngày sinh | 2001-09-13T00:00:00.000Z |
| Giới tính | Nam |
| Email CV | seed.student.089@study2work.dev |
| Số điện thoại | 0903000089 |
| Địa chỉ | Nha Trang, Việt Nam |
| Vị trí | Travel Consultant |
| Ngành | Du lịch - Khách sạn |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Du lịch - Khách sạn với vai trò Travel Consultant. |
| Học vấn | Cao đẳng/Đại học chuyên ngành Du lịch, Khách sạn hoặc Ngoại ngữ |
| Kinh nghiệm | 2 năm kinh nghiệm thực tế trong lĩnh vực du lịch và lưu trú. |
| Kỹ năng | Tiếng Anh, bán hàng, chăm sóc khách hàng, Excel |
| Ngoại ngữ | Tiếng Anh giao tiếp |
| Chứng chỉ | IELTS, TOEIC hoặc chứng chỉ nghiệp vụ du lịch |
| Dự án | Dự án portfolio 089: xây dựng giải pháp thử nghiệm cho du lịch và lưu trú. |
| Giải thưởng | Giải thưởng đồ án cấp khoa |
| Hoạt động | CLB Du lịch và Ngoại ngữ; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-089","linkedin":"https://www.linkedin.com/in/seed-student-089"} |
| Portfolio | https://portfolio.study2work.dev/student-089 |
| Mức lương mong muốn | 8-18 triệu VNĐ/tháng |
| sinhvien_id | 97 |
| created_at | 2026-09-16T14:43:44.568Z |

### Sinh viên 090 — Võ Bảo Quân

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 98 |
| Họ tên | Võ Bảo Quân |
| Email | seed.student.090@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Du lịch - Khách sạn |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 93 |
| Họ tên | Võ Bảo Quân |
| Ngày sinh | 2002-09-14T00:00:00.000Z |
| Giới tính | Nữ |
| Email CV | seed.student.090@study2work.dev |
| Số điện thoại | 0903000090 |
| Địa chỉ | Nha Trang, Việt Nam |
| Vị trí | Hotel Operations Executive |
| Ngành | Du lịch - Khách sạn |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Du lịch - Khách sạn với vai trò Hotel Operations Executive. |
| Học vấn | Cao đẳng/Đại học chuyên ngành Du lịch, Khách sạn hoặc Ngoại ngữ |
| Kinh nghiệm | Fresher; hoàn thành dự án học thuật và 6 tháng thực tập. |
| Kỹ năng | Tiếng Anh, bán hàng, chăm sóc khách hàng, Excel |
| Ngoại ngữ | Tiếng Anh B1 |
| Chứng chỉ | IELTS, TOEIC hoặc chứng chỉ nghiệp vụ du lịch |
| Dự án | Dự án portfolio 090: xây dựng giải pháp thử nghiệm cho du lịch và lưu trú. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Du lịch và Ngoại ngữ; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-090","linkedin":"https://www.linkedin.com/in/seed-student-090"} |
| Portfolio | https://portfolio.study2work.dev/student-090 |
| Mức lương mong muốn | 8-18 triệu VNĐ/tháng |
| sinhvien_id | 98 |
| created_at | 2026-09-16T14:43:45.071Z |

### Sinh viên 091 — Đặng Minh An

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 99 |
| Họ tên | Đặng Minh An |
| Email | seed.student.091@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Năng lượng xanh |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 94 |
| Họ tên | Đặng Minh An |
| Ngày sinh | 1998-10-05T00:00:00.000Z |
| Giới tính | Nam |
| Email CV | seed.student.091@study2work.dev |
| Số điện thoại | 0903000091 |
| Địa chỉ | Quảng Ninh, Việt Nam |
| Vị trí | Solar Project Engineer |
| Ngành | Năng lượng xanh |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Năng lượng xanh với vai trò Solar Project Engineer. |
| Học vấn | Đại học chuyên ngành Kỹ thuật, Môi trường hoặc Kinh tế |
| Kinh nghiệm | Fresher; hoàn thành dự án học thuật và 6 tháng thực tập. |
| Kỹ năng | AutoCAD, Excel, IoT, phân tích phát thải |
| Ngoại ngữ | Tiếng Anh B1 |
| Chứng chỉ | ISO 14001 hoặc chứng chỉ quản lý dự án |
| Dự án | Dự án portfolio 091: xây dựng giải pháp thử nghiệm cho năng lượng tái tạo. |
| Giải thưởng | Giải thưởng đồ án cấp khoa |
| Hoạt động | CLB Môi trường và Đổi mới; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-091","linkedin":"https://www.linkedin.com/in/seed-student-091"} |
| Portfolio | https://portfolio.study2work.dev/student-091 |
| Mức lương mong muốn | 12-28 triệu VNĐ/tháng |
| sinhvien_id | 99 |
| created_at | 2026-09-16T14:43:45.588Z |

### Sinh viên 092 — Đặng Ngọc Bình

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 100 |
| Họ tên | Đặng Ngọc Bình |
| Email | seed.student.092@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Năng lượng xanh |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 95 |
| Họ tên | Đặng Ngọc Bình |
| Ngày sinh | 1999-10-06T00:00:00.000Z |
| Giới tính | Nữ |
| Email CV | seed.student.092@study2work.dev |
| Số điện thoại | 0903000092 |
| Địa chỉ | Quảng Ninh, Việt Nam |
| Vị trí | Sustainability Analyst |
| Ngành | Năng lượng xanh |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Năng lượng xanh với vai trò Sustainability Analyst. |
| Học vấn | Đại học chuyên ngành Kỹ thuật, Môi trường hoặc Kinh tế |
| Kinh nghiệm | 1 năm kinh nghiệm liên quan đến năng lượng tái tạo. |
| Kỹ năng | AutoCAD, Excel, IoT, phân tích phát thải |
| Ngoại ngữ | Tiếng Anh B2 |
| Chứng chỉ | ISO 14001 hoặc chứng chỉ quản lý dự án |
| Dự án | Dự án portfolio 092: xây dựng giải pháp thử nghiệm cho năng lượng tái tạo. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Môi trường và Đổi mới; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-092","linkedin":"https://www.linkedin.com/in/seed-student-092"} |
| Portfolio | https://portfolio.study2work.dev/student-092 |
| Mức lương mong muốn | 12-28 triệu VNĐ/tháng |
| sinhvien_id | 100 |
| created_at | 2026-09-16T14:43:46.100Z |

### Sinh viên 093 — Đặng Gia Chi

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 101 |
| Họ tên | Đặng Gia Chi |
| Email | seed.student.093@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Năng lượng xanh |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 96 |
| Họ tên | Đặng Gia Chi |
| Ngày sinh | 2000-10-07T00:00:00.000Z |
| Giới tính | Nam |
| Email CV | seed.student.093@study2work.dev |
| Số điện thoại | 0903000093 |
| Địa chỉ | Quảng Ninh, Việt Nam |
| Vị trí | IoT Field Engineer |
| Ngành | Năng lượng xanh |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Năng lượng xanh với vai trò IoT Field Engineer. |
| Học vấn | Đại học chuyên ngành Kỹ thuật, Môi trường hoặc Kinh tế |
| Kinh nghiệm | 2 năm kinh nghiệm thực tế trong lĩnh vực năng lượng tái tạo. |
| Kỹ năng | AutoCAD, Excel, IoT, phân tích phát thải |
| Ngoại ngữ | Tiếng Anh giao tiếp |
| Chứng chỉ | ISO 14001 hoặc chứng chỉ quản lý dự án |
| Dự án | Dự án portfolio 093: xây dựng giải pháp thử nghiệm cho năng lượng tái tạo. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Môi trường và Đổi mới; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-093","linkedin":"https://www.linkedin.com/in/seed-student-093"} |
| Portfolio | https://portfolio.study2work.dev/student-093 |
| Mức lương mong muốn | 12-28 triệu VNĐ/tháng |
| sinhvien_id | 101 |
| created_at | 2026-09-16T14:43:46.613Z |

### Sinh viên 094 — Đặng Thanh Dũng

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 102 |
| Họ tên | Đặng Thanh Dũng |
| Email | seed.student.094@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Năng lượng xanh |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 97 |
| Họ tên | Đặng Thanh Dũng |
| Ngày sinh | 2001-10-08T00:00:00.000Z |
| Giới tính | Nữ |
| Email CV | seed.student.094@study2work.dev |
| Số điện thoại | 0903000094 |
| Địa chỉ | Quảng Ninh, Việt Nam |
| Vị trí | Business Development Executive |
| Ngành | Năng lượng xanh |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Năng lượng xanh với vai trò Business Development Executive. |
| Học vấn | Đại học chuyên ngành Kỹ thuật, Môi trường hoặc Kinh tế |
| Kinh nghiệm | Fresher; hoàn thành dự án học thuật và 6 tháng thực tập. |
| Kỹ năng | AutoCAD, Excel, IoT, phân tích phát thải |
| Ngoại ngữ | Tiếng Anh B1 |
| Chứng chỉ | ISO 14001 hoặc chứng chỉ quản lý dự án |
| Dự án | Dự án portfolio 094: xây dựng giải pháp thử nghiệm cho năng lượng tái tạo. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Môi trường và Đổi mới; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-094","linkedin":"https://www.linkedin.com/in/seed-student-094"} |
| Portfolio | https://portfolio.study2work.dev/student-094 |
| Mức lương mong muốn | 12-28 triệu VNĐ/tháng |
| sinhvien_id | 102 |
| created_at | 2026-09-16T14:43:47.124Z |

### Sinh viên 095 — Đặng Khánh Hà

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 103 |
| Họ tên | Đặng Khánh Hà |
| Email | seed.student.095@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Năng lượng xanh |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 98 |
| Họ tên | Đặng Khánh Hà |
| Ngày sinh | 2002-10-09T00:00:00.000Z |
| Giới tính | Nam |
| Email CV | seed.student.095@study2work.dev |
| Số điện thoại | 0903000095 |
| Địa chỉ | Quảng Ninh, Việt Nam |
| Vị trí | Solar Project Engineer |
| Ngành | Năng lượng xanh |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Năng lượng xanh với vai trò Solar Project Engineer. |
| Học vấn | Đại học chuyên ngành Kỹ thuật, Môi trường hoặc Kinh tế |
| Kinh nghiệm | 1 năm kinh nghiệm liên quan đến năng lượng tái tạo. |
| Kỹ năng | AutoCAD, Excel, IoT, phân tích phát thải |
| Ngoại ngữ | Tiếng Anh B2 |
| Chứng chỉ | ISO 14001 hoặc chứng chỉ quản lý dự án |
| Dự án | Dự án portfolio 095: xây dựng giải pháp thử nghiệm cho năng lượng tái tạo. |
| Giải thưởng | Giải thưởng đồ án cấp khoa |
| Hoạt động | CLB Môi trường và Đổi mới; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-095","linkedin":"https://www.linkedin.com/in/seed-student-095"} |
| Portfolio | https://portfolio.study2work.dev/student-095 |
| Mức lương mong muốn | 12-28 triệu VNĐ/tháng |
| sinhvien_id | 103 |
| created_at | 2026-09-16T14:43:47.689Z |

### Sinh viên 096 — Đặng Thu Khang

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 104 |
| Họ tên | Đặng Thu Khang |
| Email | seed.student.096@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Năng lượng xanh |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 99 |
| Họ tên | Đặng Thu Khang |
| Ngày sinh | 1998-10-10T00:00:00.000Z |
| Giới tính | Nữ |
| Email CV | seed.student.096@study2work.dev |
| Số điện thoại | 0903000096 |
| Địa chỉ | Quảng Ninh, Việt Nam |
| Vị trí | Sustainability Analyst |
| Ngành | Năng lượng xanh |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Năng lượng xanh với vai trò Sustainability Analyst. |
| Học vấn | Đại học chuyên ngành Kỹ thuật, Môi trường hoặc Kinh tế |
| Kinh nghiệm | 2 năm kinh nghiệm thực tế trong lĩnh vực năng lượng tái tạo. |
| Kỹ năng | AutoCAD, Excel, IoT, phân tích phát thải |
| Ngoại ngữ | Tiếng Anh giao tiếp |
| Chứng chỉ | ISO 14001 hoặc chứng chỉ quản lý dự án |
| Dự án | Dự án portfolio 096: xây dựng giải pháp thử nghiệm cho năng lượng tái tạo. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Môi trường và Đổi mới; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-096","linkedin":"https://www.linkedin.com/in/seed-student-096"} |
| Portfolio | https://portfolio.study2work.dev/student-096 |
| Mức lương mong muốn | 12-28 triệu VNĐ/tháng |
| sinhvien_id | 104 |
| created_at | 2026-09-16T14:43:48.204Z |

### Sinh viên 097 — Đặng Đức Linh

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 105 |
| Họ tên | Đặng Đức Linh |
| Email | seed.student.097@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Năng lượng xanh |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 100 |
| Họ tên | Đặng Đức Linh |
| Ngày sinh | 1999-10-11T00:00:00.000Z |
| Giới tính | Nam |
| Email CV | seed.student.097@study2work.dev |
| Số điện thoại | 0903000097 |
| Địa chỉ | Quảng Ninh, Việt Nam |
| Vị trí | IoT Field Engineer |
| Ngành | Năng lượng xanh |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Năng lượng xanh với vai trò IoT Field Engineer. |
| Học vấn | Đại học chuyên ngành Kỹ thuật, Môi trường hoặc Kinh tế |
| Kinh nghiệm | Fresher; hoàn thành dự án học thuật và 6 tháng thực tập. |
| Kỹ năng | AutoCAD, Excel, IoT, phân tích phát thải |
| Ngoại ngữ | Tiếng Anh B1 |
| Chứng chỉ | ISO 14001 hoặc chứng chỉ quản lý dự án |
| Dự án | Dự án portfolio 097: xây dựng giải pháp thử nghiệm cho năng lượng tái tạo. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Môi trường và Đổi mới; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-097","linkedin":"https://www.linkedin.com/in/seed-student-097"} |
| Portfolio | https://portfolio.study2work.dev/student-097 |
| Mức lương mong muốn | 12-28 triệu VNĐ/tháng |
| sinhvien_id | 105 |
| created_at | 2026-09-16T14:43:48.718Z |

### Sinh viên 098 — Đặng Quỳnh Nam

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 106 |
| Họ tên | Đặng Quỳnh Nam |
| Email | seed.student.098@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Năng lượng xanh |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 101 |
| Họ tên | Đặng Quỳnh Nam |
| Ngày sinh | 2000-10-12T00:00:00.000Z |
| Giới tính | Nữ |
| Email CV | seed.student.098@study2work.dev |
| Số điện thoại | 0903000098 |
| Địa chỉ | Quảng Ninh, Việt Nam |
| Vị trí | Business Development Executive |
| Ngành | Năng lượng xanh |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Năng lượng xanh với vai trò Business Development Executive. |
| Học vấn | Đại học chuyên ngành Kỹ thuật, Môi trường hoặc Kinh tế |
| Kinh nghiệm | 1 năm kinh nghiệm liên quan đến năng lượng tái tạo. |
| Kỹ năng | AutoCAD, Excel, IoT, phân tích phát thải |
| Ngoại ngữ | Tiếng Anh B2 |
| Chứng chỉ | ISO 14001 hoặc chứng chỉ quản lý dự án |
| Dự án | Dự án portfolio 098: xây dựng giải pháp thử nghiệm cho năng lượng tái tạo. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Môi trường và Đổi mới; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-098","linkedin":"https://www.linkedin.com/in/seed-student-098"} |
| Portfolio | https://portfolio.study2work.dev/student-098 |
| Mức lương mong muốn | 12-28 triệu VNĐ/tháng |
| sinhvien_id | 106 |
| created_at | 2026-09-16T14:43:49.223Z |

### Sinh viên 099 — Đặng Hải Phương

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 107 |
| Họ tên | Đặng Hải Phương |
| Email | seed.student.099@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Năng lượng xanh |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 102 |
| Họ tên | Đặng Hải Phương |
| Ngày sinh | 2001-10-13T00:00:00.000Z |
| Giới tính | Nam |
| Email CV | seed.student.099@study2work.dev |
| Số điện thoại | 0903000099 |
| Địa chỉ | Quảng Ninh, Việt Nam |
| Vị trí | Solar Project Engineer |
| Ngành | Năng lượng xanh |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Năng lượng xanh với vai trò Solar Project Engineer. |
| Học vấn | Đại học chuyên ngành Kỹ thuật, Môi trường hoặc Kinh tế |
| Kinh nghiệm | 2 năm kinh nghiệm thực tế trong lĩnh vực năng lượng tái tạo. |
| Kỹ năng | AutoCAD, Excel, IoT, phân tích phát thải |
| Ngoại ngữ | Tiếng Anh giao tiếp |
| Chứng chỉ | ISO 14001 hoặc chứng chỉ quản lý dự án |
| Dự án | Dự án portfolio 099: xây dựng giải pháp thử nghiệm cho năng lượng tái tạo. |
| Giải thưởng | Giải thưởng đồ án cấp khoa |
| Hoạt động | CLB Môi trường và Đổi mới; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-099","linkedin":"https://www.linkedin.com/in/seed-student-099"} |
| Portfolio | https://portfolio.study2work.dev/student-099 |
| Mức lương mong muốn | 12-28 triệu VNĐ/tháng |
| sinhvien_id | 107 |
| created_at | 2026-09-16T14:43:49.737Z |

### Sinh viên 100 — Đặng Bảo Quân

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 108 |
| Họ tên | Đặng Bảo Quân |
| Email | seed.student.100@study2work.dev |
| Mật khẩu | WorkStudent@123 |
| Chuyên ngành | Năng lượng xanh |
| Avatar | — |

#### CV

| Trường | Giá trị |
| --- | --- |
| ID CV | 103 |
| Họ tên | Đặng Bảo Quân |
| Ngày sinh | 2002-10-14T00:00:00.000Z |
| Giới tính | Nữ |
| Email CV | seed.student.100@study2work.dev |
| Số điện thoại | 0903000100 |
| Địa chỉ | Quảng Ninh, Việt Nam |
| Vị trí | Sustainability Analyst |
| Ngành | Năng lượng xanh |
| Mục tiêu nghề nghiệp | Phát triển sự nghiệp bền vững trong lĩnh vực Năng lượng xanh với vai trò Sustainability Analyst. |
| Học vấn | Đại học chuyên ngành Kỹ thuật, Môi trường hoặc Kinh tế |
| Kinh nghiệm | Fresher; hoàn thành dự án học thuật và 6 tháng thực tập. |
| Kỹ năng | AutoCAD, Excel, IoT, phân tích phát thải |
| Ngoại ngữ | Tiếng Anh B1 |
| Chứng chỉ | ISO 14001 hoặc chứng chỉ quản lý dự án |
| Dự án | Dự án portfolio 100: xây dựng giải pháp thử nghiệm cho năng lượng tái tạo. |
| Giải thưởng | Thành tích học tập và hoạt động câu lạc bộ |
| Hoạt động | CLB Môi trường và Đổi mới; tình nguyện cộng đồng. |
| Mạng xã hội | {"github":"https://github.com/seed-student-100","linkedin":"https://www.linkedin.com/in/seed-student-100"} |
| Portfolio | https://portfolio.study2work.dev/student-100 |
| Mức lương mong muốn | 12-28 triệu VNĐ/tháng |
| sinhvien_id | 108 |
| created_at | 2026-09-16T14:43:50.250Z |

## Tài khoản doanh nghiệp

### Doanh nghiệp 01 — Công ty TNHH Sao Khuê Digital

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 6 |
| Tên doanh nghiệp | Công ty TNHH Sao Khuê Digital |
| Email | seed.business.01@study2work.dev |
| Mật khẩu | WorkBusiness@123 |
| Địa chỉ | Đà Nẵng, Việt Nam |
| Số điện thoại | 02363880001 |
| Ngành | Công nghệ thông tin |
| Mô tả doanh nghiệp | Doanh nghiệp phát triển nền tảng số và sản phẩm phần mềm cho thị trường Việt Nam. |
| Nhu cầu tuyển dụng | Xây dựng sản phẩm web, dữ liệu và trải nghiệm số. |
| Avatar | — |

#### JD

##### JD 1.1 — Frontend React Developer

| Trường | Giá trị |
| --- | --- |
| ID | 4 |
| Tên vị trí | Frontend React Developer |
| Phòng ban | Sản phẩm & Kỹ thuật |
| Cấp bậc | Junior |
| Báo cáo cho | Trưởng bộ phận Sản phẩm & Kỹ thuật |
| Nhiệm vụ | Phụ trách công việc Frontend React Developer; phối hợp với đội ngũ sản phẩm & kỹ thuật để hoàn thành mục tiêu. |
| Trình độ | Đại học chuyên ngành CNTT hoặc tương đương |
| Kinh nghiệm | Từ 1 đến 3 năm kinh nghiệm liên quan |
| Kỹ năng | React, TypeScript, Node.js, SQL |
| Kỹ năng mềm | Giao tiếp, làm việc nhóm, quản lý thời gian và tư duy giải quyết vấn đề |
| Ưu tiên | Có GitHub hoặc portfolio sản phẩm |
| Mức lương | 15-30 triệu VNĐ/tháng |
| Phúc lợi | BHXH, thưởng hiệu suất, đào tạo chuyên môn và ngày nghỉ theo quy định |
| Môi trường | Agile, mentoring và làm việc hybrid |
| Địa điểm | Đà Nẵng, Việt Nam |
| Thời gian | Toàn thời gian |
| Hạn nộp | 30/11/2026 |
| Cách ứng tuyển | Nộp CV qua hệ thống Study2Work |
| Ngày tạo | 2026-09-16T14:42:31.460Z |
| Mô tả | Tham gia phát triển nền tảng số cùng Công ty TNHH Sao Khuê Digital, tạo ra kết quả có thể đo lường. |
| doanhnghiep_id | 6 |
| Tên công ty | Công ty TNHH Sao Khuê Digital |
| Ngành | Công nghệ thông tin |
| Avatar | — |

##### JD 1.2 — Backend Node.js Developer

| Trường | Giá trị |
| --- | --- |
| ID | 5 |
| Tên vị trí | Backend Node.js Developer |
| Phòng ban | Sản phẩm & Kỹ thuật |
| Cấp bậc | Middle |
| Báo cáo cho | Trưởng bộ phận Sản phẩm & Kỹ thuật |
| Nhiệm vụ | Phụ trách công việc Backend Node.js Developer; phối hợp với đội ngũ sản phẩm & kỹ thuật để hoàn thành mục tiêu. |
| Trình độ | Đại học chuyên ngành CNTT hoặc tương đương |
| Kinh nghiệm | Từ 1 đến 3 năm kinh nghiệm liên quan |
| Kỹ năng | React, TypeScript, Node.js, SQL |
| Kỹ năng mềm | Giao tiếp, làm việc nhóm, quản lý thời gian và tư duy giải quyết vấn đề |
| Ưu tiên | Có GitHub hoặc portfolio sản phẩm |
| Mức lương | 15-30 triệu VNĐ/tháng |
| Phúc lợi | BHXH, thưởng hiệu suất, đào tạo chuyên môn và ngày nghỉ theo quy định |
| Môi trường | Agile, mentoring và làm việc hybrid |
| Địa điểm | Đà Nẵng, Việt Nam |
| Thời gian | Toàn thời gian |
| Hạn nộp | 15/12/2026 |
| Cách ứng tuyển | Nộp CV qua hệ thống Study2Work |
| Ngày tạo | 2026-09-16T14:42:31.973Z |
| Mô tả | Tham gia phát triển nền tảng số cùng Công ty TNHH Sao Khuê Digital, tạo ra kết quả có thể đo lường. |
| doanhnghiep_id | 6 |
| Tên công ty | Công ty TNHH Sao Khuê Digital |
| Ngành | Công nghệ thông tin |
| Avatar | — |

##### JD 1.3 — QA Automation Engineer

| Trường | Giá trị |
| --- | --- |
| ID | 6 |
| Tên vị trí | QA Automation Engineer |
| Phòng ban | Sản phẩm & Kỹ thuật |
| Cấp bậc | Junior |
| Báo cáo cho | Trưởng bộ phận Sản phẩm & Kỹ thuật |
| Nhiệm vụ | Phụ trách công việc QA Automation Engineer; phối hợp với đội ngũ sản phẩm & kỹ thuật để hoàn thành mục tiêu. |
| Trình độ | Đại học chuyên ngành CNTT hoặc tương đương |
| Kinh nghiệm | Từ 1 đến 3 năm kinh nghiệm liên quan |
| Kỹ năng | React, TypeScript, Node.js, SQL |
| Kỹ năng mềm | Giao tiếp, làm việc nhóm, quản lý thời gian và tư duy giải quyết vấn đề |
| Ưu tiên | Có GitHub hoặc portfolio sản phẩm |
| Mức lương | 15-30 triệu VNĐ/tháng |
| Phúc lợi | BHXH, thưởng hiệu suất, đào tạo chuyên môn và ngày nghỉ theo quy định |
| Môi trường | Agile, mentoring và làm việc hybrid |
| Địa điểm | Đà Nẵng, Việt Nam |
| Thời gian | Toàn thời gian |
| Hạn nộp | 31/12/2026 |
| Cách ứng tuyển | Nộp CV qua hệ thống Study2Work |
| Ngày tạo | 2026-09-16T14:42:32.483Z |
| Mô tả | Tham gia phát triển nền tảng số cùng Công ty TNHH Sao Khuê Digital, tạo ra kết quả có thể đo lường. |
| doanhnghiep_id | 6 |
| Tên công ty | Công ty TNHH Sao Khuê Digital |
| Ngành | Công nghệ thông tin |
| Avatar | — |

##### JD 1.4 — Product Designer

| Trường | Giá trị |
| --- | --- |
| ID | 7 |
| Tên vị trí | Product Designer |
| Phòng ban | Sản phẩm & Kỹ thuật |
| Cấp bậc | Fresher |
| Báo cáo cho | Trưởng bộ phận Sản phẩm & Kỹ thuật |
| Nhiệm vụ | Phụ trách công việc Product Designer; phối hợp với đội ngũ sản phẩm & kỹ thuật để hoàn thành mục tiêu. |
| Trình độ | Đại học chuyên ngành CNTT hoặc tương đương |
| Kinh nghiệm | Từ 0 đến 1 năm kinh nghiệm hoặc có dự án tương đương |
| Kỹ năng | React, TypeScript, Node.js, SQL |
| Kỹ năng mềm | Giao tiếp, làm việc nhóm, quản lý thời gian và tư duy giải quyết vấn đề |
| Ưu tiên | Có GitHub hoặc portfolio sản phẩm |
| Mức lương | 15-30 triệu VNĐ/tháng |
| Phúc lợi | BHXH, thưởng hiệu suất, đào tạo chuyên môn và ngày nghỉ theo quy định |
| Môi trường | Agile, mentoring và làm việc hybrid |
| Địa điểm | Đà Nẵng, Việt Nam |
| Thời gian | Toàn thời gian |
| Hạn nộp | 15/01/2027 |
| Cách ứng tuyển | Nộp CV qua hệ thống Study2Work |
| Ngày tạo | 2026-09-16T14:42:32.990Z |
| Mô tả | Tham gia phát triển nền tảng số cùng Công ty TNHH Sao Khuê Digital, tạo ra kết quả có thể đo lường. |
| doanhnghiep_id | 6 |
| Tên công ty | Công ty TNHH Sao Khuê Digital |
| Ngành | Công nghệ thông tin |
| Avatar | — |

### Doanh nghiệp 02 — Việt Tín Finance

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 7 |
| Tên doanh nghiệp | Việt Tín Finance |
| Email | seed.business.02@study2work.dev |
| Mật khẩu | WorkBusiness@123 |
| Địa chỉ | Hà Nội, Việt Nam |
| Số điện thoại | 02438800002 |
| Ngành | Tài chính - Ngân hàng |
| Mô tả doanh nghiệp | Công ty công nghệ tài chính tập trung vào thanh toán số và phân tích dữ liệu tín dụng. |
| Nhu cầu tuyển dụng | Phát triển dịch vụ tài chính an toàn, minh bạch và dễ tiếp cận. |
| Avatar | — |

#### JD

##### JD 2.1 — Chuyên viên Phân tích Tài chính

| Trường | Giá trị |
| --- | --- |
| ID | 8 |
| Tên vị trí | Chuyên viên Phân tích Tài chính |
| Phòng ban | Phân tích & Vận hành |
| Cấp bậc | Junior |
| Báo cáo cho | Trưởng bộ phận Phân tích & Vận hành |
| Nhiệm vụ | Phụ trách công việc Chuyên viên Phân tích Tài chính; phối hợp với đội ngũ phân tích & vận hành để hoàn thành mục tiêu. |
| Trình độ | Đại học chuyên ngành Tài chính, Kinh tế hoặc CNTT |
| Kinh nghiệm | Từ 1 đến 3 năm kinh nghiệm liên quan |
| Kỹ năng | Excel, SQL, Python, phân tích dữ liệu |
| Kỹ năng mềm | Giao tiếp, làm việc nhóm, quản lý thời gian và tư duy giải quyết vấn đề |
| Ưu tiên | Tư duy định lượng và cẩn trọng với dữ liệu |
| Mức lương | 12-25 triệu VNĐ/tháng |
| Phúc lợi | BHXH, thưởng hiệu suất, đào tạo chuyên môn và ngày nghỉ theo quy định |
| Môi trường | Quy trình rõ ràng, phối hợp liên phòng ban |
| Địa điểm | Hà Nội, Việt Nam |
| Thời gian | Toàn thời gian |
| Hạn nộp | 30/11/2026 |
| Cách ứng tuyển | Nộp CV qua hệ thống Study2Work |
| Ngày tạo | 2026-09-16T14:42:33.757Z |
| Mô tả | Tham gia phát triển dịch vụ tài chính số cùng Việt Tín Finance, tạo ra kết quả có thể đo lường. |
| doanhnghiep_id | 7 |
| Tên công ty | Việt Tín Finance |
| Ngành | Tài chính - Ngân hàng |
| Avatar | — |

##### JD 2.2 — Banking Integration Developer

| Trường | Giá trị |
| --- | --- |
| ID | 9 |
| Tên vị trí | Banking Integration Developer |
| Phòng ban | Phân tích & Vận hành |
| Cấp bậc | Middle |
| Báo cáo cho | Trưởng bộ phận Phân tích & Vận hành |
| Nhiệm vụ | Phụ trách công việc Banking Integration Developer; phối hợp với đội ngũ phân tích & vận hành để hoàn thành mục tiêu. |
| Trình độ | Đại học chuyên ngành Tài chính, Kinh tế hoặc CNTT |
| Kinh nghiệm | Từ 1 đến 3 năm kinh nghiệm liên quan |
| Kỹ năng | Excel, SQL, Python, phân tích dữ liệu |
| Kỹ năng mềm | Giao tiếp, làm việc nhóm, quản lý thời gian và tư duy giải quyết vấn đề |
| Ưu tiên | Tư duy định lượng và cẩn trọng với dữ liệu |
| Mức lương | 12-25 triệu VNĐ/tháng |
| Phúc lợi | BHXH, thưởng hiệu suất, đào tạo chuyên môn và ngày nghỉ theo quy định |
| Môi trường | Quy trình rõ ràng, phối hợp liên phòng ban |
| Địa điểm | Hà Nội, Việt Nam |
| Thời gian | Toàn thời gian |
| Hạn nộp | 15/12/2026 |
| Cách ứng tuyển | Nộp CV qua hệ thống Study2Work |
| Ngày tạo | 2026-09-16T14:42:34.257Z |
| Mô tả | Tham gia phát triển dịch vụ tài chính số cùng Việt Tín Finance, tạo ra kết quả có thể đo lường. |
| doanhnghiep_id | 7 |
| Tên công ty | Việt Tín Finance |
| Ngành | Tài chính - Ngân hàng |
| Avatar | — |

##### JD 2.3 — Data Analyst

| Trường | Giá trị |
| --- | --- |
| ID | 10 |
| Tên vị trí | Data Analyst |
| Phòng ban | Phân tích & Vận hành |
| Cấp bậc | Junior |
| Báo cáo cho | Trưởng bộ phận Phân tích & Vận hành |
| Nhiệm vụ | Phụ trách công việc Data Analyst; phối hợp với đội ngũ phân tích & vận hành để hoàn thành mục tiêu. |
| Trình độ | Đại học chuyên ngành Tài chính, Kinh tế hoặc CNTT |
| Kinh nghiệm | Từ 1 đến 3 năm kinh nghiệm liên quan |
| Kỹ năng | Excel, SQL, Python, phân tích dữ liệu |
| Kỹ năng mềm | Giao tiếp, làm việc nhóm, quản lý thời gian và tư duy giải quyết vấn đề |
| Ưu tiên | Tư duy định lượng và cẩn trọng với dữ liệu |
| Mức lương | 12-25 triệu VNĐ/tháng |
| Phúc lợi | BHXH, thưởng hiệu suất, đào tạo chuyên môn và ngày nghỉ theo quy định |
| Môi trường | Quy trình rõ ràng, phối hợp liên phòng ban |
| Địa điểm | Hà Nội, Việt Nam |
| Thời gian | Toàn thời gian |
| Hạn nộp | 31/12/2026 |
| Cách ứng tuyển | Nộp CV qua hệ thống Study2Work |
| Ngày tạo | 2026-09-16T14:42:34.778Z |
| Mô tả | Tham gia phát triển dịch vụ tài chính số cùng Việt Tín Finance, tạo ra kết quả có thể đo lường. |
| doanhnghiep_id | 7 |
| Tên công ty | Việt Tín Finance |
| Ngành | Tài chính - Ngân hàng |
| Avatar | — |

##### JD 2.4 — Risk & Compliance Specialist

| Trường | Giá trị |
| --- | --- |
| ID | 11 |
| Tên vị trí | Risk & Compliance Specialist |
| Phòng ban | Phân tích & Vận hành |
| Cấp bậc | Fresher |
| Báo cáo cho | Trưởng bộ phận Phân tích & Vận hành |
| Nhiệm vụ | Phụ trách công việc Risk & Compliance Specialist; phối hợp với đội ngũ phân tích & vận hành để hoàn thành mục tiêu. |
| Trình độ | Đại học chuyên ngành Tài chính, Kinh tế hoặc CNTT |
| Kinh nghiệm | Từ 0 đến 1 năm kinh nghiệm hoặc có dự án tương đương |
| Kỹ năng | Excel, SQL, Python, phân tích dữ liệu |
| Kỹ năng mềm | Giao tiếp, làm việc nhóm, quản lý thời gian và tư duy giải quyết vấn đề |
| Ưu tiên | Tư duy định lượng và cẩn trọng với dữ liệu |
| Mức lương | 12-25 triệu VNĐ/tháng |
| Phúc lợi | BHXH, thưởng hiệu suất, đào tạo chuyên môn và ngày nghỉ theo quy định |
| Môi trường | Quy trình rõ ràng, phối hợp liên phòng ban |
| Địa điểm | Hà Nội, Việt Nam |
| Thời gian | Toàn thời gian |
| Hạn nộp | 15/01/2027 |
| Cách ứng tuyển | Nộp CV qua hệ thống Study2Work |
| Ngày tạo | 2026-09-16T14:42:35.290Z |
| Mô tả | Tham gia phát triển dịch vụ tài chính số cùng Việt Tín Finance, tạo ra kết quả có thể đo lường. |
| doanhnghiep_id | 7 |
| Tên công ty | Việt Tín Finance |
| Ngành | Tài chính - Ngân hàng |
| Avatar | — |

### Doanh nghiệp 03 — Mộc Miên Media

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 8 |
| Tên doanh nghiệp | Mộc Miên Media |
| Email | seed.business.03@study2work.dev |
| Mật khẩu | WorkBusiness@123 |
| Địa chỉ | TP. Hồ Chí Minh, Việt Nam |
| Số điện thoại | 02838800003 |
| Ngành | Marketing - Truyền thông |
| Mô tả doanh nghiệp | Agency truyền thông tích hợp cung cấp chiến lược thương hiệu, nội dung và quảng cáo số. |
| Nhu cầu tuyển dụng | Tạo chiến dịch có câu chuyện rõ ràng và đo lường được hiệu quả. |
| Avatar | — |

#### JD

##### JD 3.1 — Content Marketing Executive

| Trường | Giá trị |
| --- | --- |
| ID | 12 |
| Tên vị trí | Content Marketing Executive |
| Phòng ban | Marketing & Sáng tạo |
| Cấp bậc | Junior |
| Báo cáo cho | Trưởng bộ phận Marketing & Sáng tạo |
| Nhiệm vụ | Phụ trách công việc Content Marketing Executive; phối hợp với đội ngũ marketing & sáng tạo để hoàn thành mục tiêu. |
| Trình độ | Đại học chuyên ngành Marketing, Truyền thông hoặc Ngôn ngữ |
| Kinh nghiệm | Từ 1 đến 3 năm kinh nghiệm liên quan |
| Kỹ năng | Content, SEO, Meta Ads, Google Analytics |
| Kỹ năng mềm | Giao tiếp, làm việc nhóm, quản lý thời gian và tư duy giải quyết vấn đề |
| Ưu tiên | Có portfolio nội dung hoặc chiến dịch thực tế |
| Mức lương | 10-22 triệu VNĐ/tháng |
| Phúc lợi | BHXH, thưởng hiệu suất, đào tạo chuyên môn và ngày nghỉ theo quy định |
| Môi trường | Sáng tạo, phản hồi nhanh và tôn trọng ý tưởng |
| Địa điểm | TP. Hồ Chí Minh, Việt Nam |
| Thời gian | Toàn thời gian |
| Hạn nộp | 30/11/2026 |
| Cách ứng tuyển | Nộp CV qua hệ thống Study2Work |
| Ngày tạo | 2026-09-16T14:42:36.057Z |
| Mô tả | Tham gia phát triển chiến dịch thương hiệu cùng Mộc Miên Media, tạo ra kết quả có thể đo lường. |
| doanhnghiep_id | 8 |
| Tên công ty | Mộc Miên Media |
| Ngành | Marketing - Truyền thông |
| Avatar | — |

##### JD 3.2 — Performance Marketing Specialist

| Trường | Giá trị |
| --- | --- |
| ID | 13 |
| Tên vị trí | Performance Marketing Specialist |
| Phòng ban | Marketing & Sáng tạo |
| Cấp bậc | Middle |
| Báo cáo cho | Trưởng bộ phận Marketing & Sáng tạo |
| Nhiệm vụ | Phụ trách công việc Performance Marketing Specialist; phối hợp với đội ngũ marketing & sáng tạo để hoàn thành mục tiêu. |
| Trình độ | Đại học chuyên ngành Marketing, Truyền thông hoặc Ngôn ngữ |
| Kinh nghiệm | Từ 1 đến 3 năm kinh nghiệm liên quan |
| Kỹ năng | Content, SEO, Meta Ads, Google Analytics |
| Kỹ năng mềm | Giao tiếp, làm việc nhóm, quản lý thời gian và tư duy giải quyết vấn đề |
| Ưu tiên | Có portfolio nội dung hoặc chiến dịch thực tế |
| Mức lương | 10-22 triệu VNĐ/tháng |
| Phúc lợi | BHXH, thưởng hiệu suất, đào tạo chuyên môn và ngày nghỉ theo quy định |
| Môi trường | Sáng tạo, phản hồi nhanh và tôn trọng ý tưởng |
| Địa điểm | TP. Hồ Chí Minh, Việt Nam |
| Thời gian | Toàn thời gian |
| Hạn nộp | 15/12/2026 |
| Cách ứng tuyển | Nộp CV qua hệ thống Study2Work |
| Ngày tạo | 2026-09-16T14:42:36.573Z |
| Mô tả | Tham gia phát triển chiến dịch thương hiệu cùng Mộc Miên Media, tạo ra kết quả có thể đo lường. |
| doanhnghiep_id | 8 |
| Tên công ty | Mộc Miên Media |
| Ngành | Marketing - Truyền thông |
| Avatar | — |

##### JD 3.3 — Social Media Planner

| Trường | Giá trị |
| --- | --- |
| ID | 14 |
| Tên vị trí | Social Media Planner |
| Phòng ban | Marketing & Sáng tạo |
| Cấp bậc | Junior |
| Báo cáo cho | Trưởng bộ phận Marketing & Sáng tạo |
| Nhiệm vụ | Phụ trách công việc Social Media Planner; phối hợp với đội ngũ marketing & sáng tạo để hoàn thành mục tiêu. |
| Trình độ | Đại học chuyên ngành Marketing, Truyền thông hoặc Ngôn ngữ |
| Kinh nghiệm | Từ 1 đến 3 năm kinh nghiệm liên quan |
| Kỹ năng | Content, SEO, Meta Ads, Google Analytics |
| Kỹ năng mềm | Giao tiếp, làm việc nhóm, quản lý thời gian và tư duy giải quyết vấn đề |
| Ưu tiên | Có portfolio nội dung hoặc chiến dịch thực tế |
| Mức lương | 10-22 triệu VNĐ/tháng |
| Phúc lợi | BHXH, thưởng hiệu suất, đào tạo chuyên môn và ngày nghỉ theo quy định |
| Môi trường | Sáng tạo, phản hồi nhanh và tôn trọng ý tưởng |
| Địa điểm | TP. Hồ Chí Minh, Việt Nam |
| Thời gian | Toàn thời gian |
| Hạn nộp | 31/12/2026 |
| Cách ứng tuyển | Nộp CV qua hệ thống Study2Work |
| Ngày tạo | 2026-09-16T14:42:37.085Z |
| Mô tả | Tham gia phát triển chiến dịch thương hiệu cùng Mộc Miên Media, tạo ra kết quả có thể đo lường. |
| doanhnghiep_id | 8 |
| Tên công ty | Mộc Miên Media |
| Ngành | Marketing - Truyền thông |
| Avatar | — |

##### JD 3.4 — Account Executive

| Trường | Giá trị |
| --- | --- |
| ID | 15 |
| Tên vị trí | Account Executive |
| Phòng ban | Marketing & Sáng tạo |
| Cấp bậc | Fresher |
| Báo cáo cho | Trưởng bộ phận Marketing & Sáng tạo |
| Nhiệm vụ | Phụ trách công việc Account Executive; phối hợp với đội ngũ marketing & sáng tạo để hoàn thành mục tiêu. |
| Trình độ | Đại học chuyên ngành Marketing, Truyền thông hoặc Ngôn ngữ |
| Kinh nghiệm | Từ 0 đến 1 năm kinh nghiệm hoặc có dự án tương đương |
| Kỹ năng | Content, SEO, Meta Ads, Google Analytics |
| Kỹ năng mềm | Giao tiếp, làm việc nhóm, quản lý thời gian và tư duy giải quyết vấn đề |
| Ưu tiên | Có portfolio nội dung hoặc chiến dịch thực tế |
| Mức lương | 10-22 triệu VNĐ/tháng |
| Phúc lợi | BHXH, thưởng hiệu suất, đào tạo chuyên môn và ngày nghỉ theo quy định |
| Môi trường | Sáng tạo, phản hồi nhanh và tôn trọng ý tưởng |
| Địa điểm | TP. Hồ Chí Minh, Việt Nam |
| Thời gian | Toàn thời gian |
| Hạn nộp | 15/01/2027 |
| Cách ứng tuyển | Nộp CV qua hệ thống Study2Work |
| Ngày tạo | 2026-09-16T14:42:37.603Z |
| Mô tả | Tham gia phát triển chiến dịch thương hiệu cùng Mộc Miên Media, tạo ra kết quả có thể đo lường. |
| doanhnghiep_id | 8 |
| Tên công ty | Mộc Miên Media |
| Ngành | Marketing - Truyền thông |
| Avatar | — |

### Doanh nghiệp 04 — Chợ Việt Commerce

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 9 |
| Tên doanh nghiệp | Chợ Việt Commerce |
| Email | seed.business.04@study2work.dev |
| Mật khẩu | WorkBusiness@123 |
| Địa chỉ | Hải Phòng, Việt Nam |
| Số điện thoại | 02253880004 |
| Ngành | Thương mại điện tử |
| Mô tả doanh nghiệp | Nền tảng thương mại điện tử kết nối thương hiệu địa phương với người tiêu dùng trên toàn quốc. |
| Nhu cầu tuyển dụng | Tối ưu vận hành sàn, trải nghiệm mua sắm và tăng trưởng khách hàng. |
| Avatar | — |

#### JD

##### JD 4.1 — E-commerce Operations Specialist

| Trường | Giá trị |
| --- | --- |
| ID | 16 |
| Tên vị trí | E-commerce Operations Specialist |
| Phòng ban | Vận hành & Tăng trưởng |
| Cấp bậc | Junior |
| Báo cáo cho | Trưởng bộ phận Vận hành & Tăng trưởng |
| Nhiệm vụ | Phụ trách công việc E-commerce Operations Specialist; phối hợp với đội ngũ vận hành & tăng trưởng để hoàn thành mục tiêu. |
| Trình độ | Đại học chuyên ngành Kinh doanh, CNTT hoặc Thiết kế |
| Kinh nghiệm | Từ 1 đến 3 năm kinh nghiệm liên quan |
| Kỹ năng | E-commerce, SQL, Figma, phân tích funnel |
| Kỹ năng mềm | Giao tiếp, làm việc nhóm, quản lý thời gian và tư duy giải quyết vấn đề |
| Ưu tiên | Hiểu hành vi người dùng và quy trình bán hàng online |
| Mức lương | 11-24 triệu VNĐ/tháng |
| Phúc lợi | BHXH, thưởng hiệu suất, đào tạo chuyên môn và ngày nghỉ theo quy định |
| Môi trường | Nhanh, thực tế và định hướng theo dữ liệu |
| Địa điểm | Hải Phòng, Việt Nam |
| Thời gian | Toàn thời gian |
| Hạn nộp | 30/11/2026 |
| Cách ứng tuyển | Nộp CV qua hệ thống Study2Work |
| Ngày tạo | 2026-09-16T14:42:38.360Z |
| Mô tả | Tham gia phát triển sàn thương mại điện tử cùng Chợ Việt Commerce, tạo ra kết quả có thể đo lường. |
| doanhnghiep_id | 9 |
| Tên công ty | Chợ Việt Commerce |
| Ngành | Thương mại điện tử |
| Avatar | — |

##### JD 4.2 — Product Owner E-commerce

| Trường | Giá trị |
| --- | --- |
| ID | 17 |
| Tên vị trí | Product Owner E-commerce |
| Phòng ban | Vận hành & Tăng trưởng |
| Cấp bậc | Middle |
| Báo cáo cho | Trưởng bộ phận Vận hành & Tăng trưởng |
| Nhiệm vụ | Phụ trách công việc Product Owner E-commerce; phối hợp với đội ngũ vận hành & tăng trưởng để hoàn thành mục tiêu. |
| Trình độ | Đại học chuyên ngành Kinh doanh, CNTT hoặc Thiết kế |
| Kinh nghiệm | Từ 1 đến 3 năm kinh nghiệm liên quan |
| Kỹ năng | E-commerce, SQL, Figma, phân tích funnel |
| Kỹ năng mềm | Giao tiếp, làm việc nhóm, quản lý thời gian và tư duy giải quyết vấn đề |
| Ưu tiên | Hiểu hành vi người dùng và quy trình bán hàng online |
| Mức lương | 11-24 triệu VNĐ/tháng |
| Phúc lợi | BHXH, thưởng hiệu suất, đào tạo chuyên môn và ngày nghỉ theo quy định |
| Môi trường | Nhanh, thực tế và định hướng theo dữ liệu |
| Địa điểm | Hải Phòng, Việt Nam |
| Thời gian | Toàn thời gian |
| Hạn nộp | 15/12/2026 |
| Cách ứng tuyển | Nộp CV qua hệ thống Study2Work |
| Ngày tạo | 2026-09-16T14:42:38.876Z |
| Mô tả | Tham gia phát triển sàn thương mại điện tử cùng Chợ Việt Commerce, tạo ra kết quả có thể đo lường. |
| doanhnghiep_id | 9 |
| Tên công ty | Chợ Việt Commerce |
| Ngành | Thương mại điện tử |
| Avatar | — |

##### JD 4.3 — UI/UX Designer

| Trường | Giá trị |
| --- | --- |
| ID | 18 |
| Tên vị trí | UI/UX Designer |
| Phòng ban | Vận hành & Tăng trưởng |
| Cấp bậc | Junior |
| Báo cáo cho | Trưởng bộ phận Vận hành & Tăng trưởng |
| Nhiệm vụ | Phụ trách công việc UI/UX Designer; phối hợp với đội ngũ vận hành & tăng trưởng để hoàn thành mục tiêu. |
| Trình độ | Đại học chuyên ngành Kinh doanh, CNTT hoặc Thiết kế |
| Kinh nghiệm | Từ 1 đến 3 năm kinh nghiệm liên quan |
| Kỹ năng | E-commerce, SQL, Figma, phân tích funnel |
| Kỹ năng mềm | Giao tiếp, làm việc nhóm, quản lý thời gian và tư duy giải quyết vấn đề |
| Ưu tiên | Hiểu hành vi người dùng và quy trình bán hàng online |
| Mức lương | 11-24 triệu VNĐ/tháng |
| Phúc lợi | BHXH, thưởng hiệu suất, đào tạo chuyên môn và ngày nghỉ theo quy định |
| Môi trường | Nhanh, thực tế và định hướng theo dữ liệu |
| Địa điểm | Hải Phòng, Việt Nam |
| Thời gian | Toàn thời gian |
| Hạn nộp | 31/12/2026 |
| Cách ứng tuyển | Nộp CV qua hệ thống Study2Work |
| Ngày tạo | 2026-09-16T14:42:39.390Z |
| Mô tả | Tham gia phát triển sàn thương mại điện tử cùng Chợ Việt Commerce, tạo ra kết quả có thể đo lường. |
| doanhnghiep_id | 9 |
| Tên công ty | Chợ Việt Commerce |
| Ngành | Thương mại điện tử |
| Avatar | — |

##### JD 4.4 — Customer Growth Analyst

| Trường | Giá trị |
| --- | --- |
| ID | 19 |
| Tên vị trí | Customer Growth Analyst |
| Phòng ban | Vận hành & Tăng trưởng |
| Cấp bậc | Fresher |
| Báo cáo cho | Trưởng bộ phận Vận hành & Tăng trưởng |
| Nhiệm vụ | Phụ trách công việc Customer Growth Analyst; phối hợp với đội ngũ vận hành & tăng trưởng để hoàn thành mục tiêu. |
| Trình độ | Đại học chuyên ngành Kinh doanh, CNTT hoặc Thiết kế |
| Kinh nghiệm | Từ 0 đến 1 năm kinh nghiệm hoặc có dự án tương đương |
| Kỹ năng | E-commerce, SQL, Figma, phân tích funnel |
| Kỹ năng mềm | Giao tiếp, làm việc nhóm, quản lý thời gian và tư duy giải quyết vấn đề |
| Ưu tiên | Hiểu hành vi người dùng và quy trình bán hàng online |
| Mức lương | 11-24 triệu VNĐ/tháng |
| Phúc lợi | BHXH, thưởng hiệu suất, đào tạo chuyên môn và ngày nghỉ theo quy định |
| Môi trường | Nhanh, thực tế và định hướng theo dữ liệu |
| Địa điểm | Hải Phòng, Việt Nam |
| Thời gian | Toàn thời gian |
| Hạn nộp | 15/01/2027 |
| Cách ứng tuyển | Nộp CV qua hệ thống Study2Work |
| Ngày tạo | 2026-09-16T14:42:39.892Z |
| Mô tả | Tham gia phát triển sàn thương mại điện tử cùng Chợ Việt Commerce, tạo ra kết quả có thể đo lường. |
| doanhnghiep_id | 9 |
| Tên công ty | Chợ Việt Commerce |
| Ngành | Thương mại điện tử |
| Avatar | — |

### Doanh nghiệp 05 — Học Mở Education

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 10 |
| Tên doanh nghiệp | Học Mở Education |
| Email | seed.business.05@study2work.dev |
| Mật khẩu | WorkBusiness@123 |
| Địa chỉ | Cần Thơ, Việt Nam |
| Số điện thoại | 02923880005 |
| Ngành | Giáo dục |
| Mô tả doanh nghiệp | Đơn vị giáo dục số phát triển nội dung học tập và dịch vụ hỗ trợ người học suốt đời. |
| Nhu cầu tuyển dụng | Cải thiện chất lượng học tập và trải nghiệm của học viên. |
| Avatar | — |

#### JD

##### JD 5.1 — Academic Advisor

| Trường | Giá trị |
| --- | --- |
| ID | 20 |
| Tên vị trí | Academic Advisor |
| Phòng ban | Học thuật & Sản phẩm |
| Cấp bậc | Junior |
| Báo cáo cho | Trưởng bộ phận Học thuật & Sản phẩm |
| Nhiệm vụ | Phụ trách công việc Academic Advisor; phối hợp với đội ngũ học thuật & sản phẩm để hoàn thành mục tiêu. |
| Trình độ | Đại học chuyên ngành Giáo dục, Xã hội học hoặc CNTT |
| Kinh nghiệm | Từ 1 đến 3 năm kinh nghiệm liên quan |
| Kỹ năng | Instructional Design, LMS, giao tiếp, Excel |
| Kỹ năng mềm | Giao tiếp, làm việc nhóm, quản lý thời gian và tư duy giải quyết vấn đề |
| Ưu tiên | Yêu thích giáo dục và có tư duy lấy người học làm trung tâm |
| Mức lương | 9-20 triệu VNĐ/tháng |
| Phúc lợi | BHXH, thưởng hiệu suất, đào tạo chuyên môn và ngày nghỉ theo quy định |
| Môi trường | Nhân văn, học hỏi liên tục và hợp tác đa chuyên môn |
| Địa điểm | Cần Thơ, Việt Nam |
| Thời gian | Toàn thời gian |
| Hạn nộp | 30/11/2026 |
| Cách ứng tuyển | Nộp CV qua hệ thống Study2Work |
| Ngày tạo | 2026-09-16T14:42:40.662Z |
| Mô tả | Tham gia phát triển giáo dục số cùng Học Mở Education, tạo ra kết quả có thể đo lường. |
| doanhnghiep_id | 10 |
| Tên công ty | Học Mở Education |
| Ngành | Giáo dục |
| Avatar | — |

##### JD 5.2 — Instructional Designer

| Trường | Giá trị |
| --- | --- |
| ID | 21 |
| Tên vị trí | Instructional Designer |
| Phòng ban | Học thuật & Sản phẩm |
| Cấp bậc | Middle |
| Báo cáo cho | Trưởng bộ phận Học thuật & Sản phẩm |
| Nhiệm vụ | Phụ trách công việc Instructional Designer; phối hợp với đội ngũ học thuật & sản phẩm để hoàn thành mục tiêu. |
| Trình độ | Đại học chuyên ngành Giáo dục, Xã hội học hoặc CNTT |
| Kinh nghiệm | Từ 1 đến 3 năm kinh nghiệm liên quan |
| Kỹ năng | Instructional Design, LMS, giao tiếp, Excel |
| Kỹ năng mềm | Giao tiếp, làm việc nhóm, quản lý thời gian và tư duy giải quyết vấn đề |
| Ưu tiên | Yêu thích giáo dục và có tư duy lấy người học làm trung tâm |
| Mức lương | 9-20 triệu VNĐ/tháng |
| Phúc lợi | BHXH, thưởng hiệu suất, đào tạo chuyên môn và ngày nghỉ theo quy định |
| Môi trường | Nhân văn, học hỏi liên tục và hợp tác đa chuyên môn |
| Địa điểm | Cần Thơ, Việt Nam |
| Thời gian | Toàn thời gian |
| Hạn nộp | 15/12/2026 |
| Cách ứng tuyển | Nộp CV qua hệ thống Study2Work |
| Ngày tạo | 2026-09-16T14:42:41.177Z |
| Mô tả | Tham gia phát triển giáo dục số cùng Học Mở Education, tạo ra kết quả có thể đo lường. |
| doanhnghiep_id | 10 |
| Tên công ty | Học Mở Education |
| Ngành | Giáo dục |
| Avatar | — |

##### JD 5.3 — Full-stack Developer EdTech

| Trường | Giá trị |
| --- | --- |
| ID | 22 |
| Tên vị trí | Full-stack Developer EdTech |
| Phòng ban | Học thuật & Sản phẩm |
| Cấp bậc | Junior |
| Báo cáo cho | Trưởng bộ phận Học thuật & Sản phẩm |
| Nhiệm vụ | Phụ trách công việc Full-stack Developer EdTech; phối hợp với đội ngũ học thuật & sản phẩm để hoàn thành mục tiêu. |
| Trình độ | Đại học chuyên ngành Giáo dục, Xã hội học hoặc CNTT |
| Kinh nghiệm | Từ 1 đến 3 năm kinh nghiệm liên quan |
| Kỹ năng | Instructional Design, LMS, giao tiếp, Excel |
| Kỹ năng mềm | Giao tiếp, làm việc nhóm, quản lý thời gian và tư duy giải quyết vấn đề |
| Ưu tiên | Yêu thích giáo dục và có tư duy lấy người học làm trung tâm |
| Mức lương | 9-20 triệu VNĐ/tháng |
| Phúc lợi | BHXH, thưởng hiệu suất, đào tạo chuyên môn và ngày nghỉ theo quy định |
| Môi trường | Nhân văn, học hỏi liên tục và hợp tác đa chuyên môn |
| Địa điểm | Cần Thơ, Việt Nam |
| Thời gian | Toàn thời gian |
| Hạn nộp | 31/12/2026 |
| Cách ứng tuyển | Nộp CV qua hệ thống Study2Work |
| Ngày tạo | 2026-09-16T14:42:41.691Z |
| Mô tả | Tham gia phát triển giáo dục số cùng Học Mở Education, tạo ra kết quả có thể đo lường. |
| doanhnghiep_id | 10 |
| Tên công ty | Học Mở Education |
| Ngành | Giáo dục |
| Avatar | — |

##### JD 5.4 — Student Success Specialist

| Trường | Giá trị |
| --- | --- |
| ID | 23 |
| Tên vị trí | Student Success Specialist |
| Phòng ban | Học thuật & Sản phẩm |
| Cấp bậc | Fresher |
| Báo cáo cho | Trưởng bộ phận Học thuật & Sản phẩm |
| Nhiệm vụ | Phụ trách công việc Student Success Specialist; phối hợp với đội ngũ học thuật & sản phẩm để hoàn thành mục tiêu. |
| Trình độ | Đại học chuyên ngành Giáo dục, Xã hội học hoặc CNTT |
| Kinh nghiệm | Từ 0 đến 1 năm kinh nghiệm hoặc có dự án tương đương |
| Kỹ năng | Instructional Design, LMS, giao tiếp, Excel |
| Kỹ năng mềm | Giao tiếp, làm việc nhóm, quản lý thời gian và tư duy giải quyết vấn đề |
| Ưu tiên | Yêu thích giáo dục và có tư duy lấy người học làm trung tâm |
| Mức lương | 9-20 triệu VNĐ/tháng |
| Phúc lợi | BHXH, thưởng hiệu suất, đào tạo chuyên môn và ngày nghỉ theo quy định |
| Môi trường | Nhân văn, học hỏi liên tục và hợp tác đa chuyên môn |
| Địa điểm | Cần Thơ, Việt Nam |
| Thời gian | Toàn thời gian |
| Hạn nộp | 15/01/2027 |
| Cách ứng tuyển | Nộp CV qua hệ thống Study2Work |
| Ngày tạo | 2026-09-16T14:42:42.525Z |
| Mô tả | Tham gia phát triển giáo dục số cùng Học Mở Education, tạo ra kết quả có thể đo lường. |
| doanhnghiep_id | 10 |
| Tên công ty | Học Mở Education |
| Ngành | Giáo dục |
| Avatar | — |

### Doanh nghiệp 06 — Đông Hải Logistics

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 11 |
| Tên doanh nghiệp | Đông Hải Logistics |
| Email | seed.business.06@study2work.dev |
| Mật khẩu | WorkBusiness@123 |
| Địa chỉ | Bình Dương, Việt Nam |
| Số điện thoại | 02743880006 |
| Ngành | Logistics |
| Mô tả doanh nghiệp | Doanh nghiệp logistics cung cấp giải pháp vận chuyển, kho bãi và theo dõi chuỗi cung ứng. |
| Nhu cầu tuyển dụng | Tăng khả năng quan sát, tối ưu chi phí và nâng độ tin cậy giao hàng. |
| Avatar | — |

#### JD

##### JD 6.1 — Supply Chain Analyst

| Trường | Giá trị |
| --- | --- |
| ID | 24 |
| Tên vị trí | Supply Chain Analyst |
| Phòng ban | Chuỗi cung ứng & Vận hành |
| Cấp bậc | Junior |
| Báo cáo cho | Trưởng bộ phận Chuỗi cung ứng & Vận hành |
| Nhiệm vụ | Phụ trách công việc Supply Chain Analyst; phối hợp với đội ngũ chuỗi cung ứng & vận hành để hoàn thành mục tiêu. |
| Trình độ | Đại học chuyên ngành Logistics, Kinh tế hoặc Kỹ thuật |
| Kinh nghiệm | Từ 1 đến 3 năm kinh nghiệm liên quan |
| Kỹ năng | Supply Chain, Excel, SQL, quản lý vận hành |
| Kỹ năng mềm | Giao tiếp, làm việc nhóm, quản lý thời gian và tư duy giải quyết vấn đề |
| Ưu tiên | Có tư duy quy trình và sẵn sàng làm việc với dữ liệu vận hành |
| Mức lương | 10-23 triệu VNĐ/tháng |
| Phúc lợi | BHXH, thưởng hiệu suất, đào tạo chuyên môn và ngày nghỉ theo quy định |
| Môi trường | Kỷ luật, phối hợp thực địa và cải tiến liên tục |
| Địa điểm | Bình Dương, Việt Nam |
| Thời gian | Toàn thời gian |
| Hạn nộp | 30/11/2026 |
| Cách ứng tuyển | Nộp CV qua hệ thống Study2Work |
| Ngày tạo | 2026-09-16T14:42:43.278Z |
| Mô tả | Tham gia phát triển chuỗi cung ứng cùng Đông Hải Logistics, tạo ra kết quả có thể đo lường. |
| doanhnghiep_id | 11 |
| Tên công ty | Đông Hải Logistics |
| Ngành | Logistics |
| Avatar | — |

##### JD 6.2 — Logistics Operations Coordinator

| Trường | Giá trị |
| --- | --- |
| ID | 25 |
| Tên vị trí | Logistics Operations Coordinator |
| Phòng ban | Chuỗi cung ứng & Vận hành |
| Cấp bậc | Middle |
| Báo cáo cho | Trưởng bộ phận Chuỗi cung ứng & Vận hành |
| Nhiệm vụ | Phụ trách công việc Logistics Operations Coordinator; phối hợp với đội ngũ chuỗi cung ứng & vận hành để hoàn thành mục tiêu. |
| Trình độ | Đại học chuyên ngành Logistics, Kinh tế hoặc Kỹ thuật |
| Kinh nghiệm | Từ 1 đến 3 năm kinh nghiệm liên quan |
| Kỹ năng | Supply Chain, Excel, SQL, quản lý vận hành |
| Kỹ năng mềm | Giao tiếp, làm việc nhóm, quản lý thời gian và tư duy giải quyết vấn đề |
| Ưu tiên | Có tư duy quy trình và sẵn sàng làm việc với dữ liệu vận hành |
| Mức lương | 10-23 triệu VNĐ/tháng |
| Phúc lợi | BHXH, thưởng hiệu suất, đào tạo chuyên môn và ngày nghỉ theo quy định |
| Môi trường | Kỷ luật, phối hợp thực địa và cải tiến liên tục |
| Địa điểm | Bình Dương, Việt Nam |
| Thời gian | Toàn thời gian |
| Hạn nộp | 15/12/2026 |
| Cách ứng tuyển | Nộp CV qua hệ thống Study2Work |
| Ngày tạo | 2026-09-16T14:42:43.789Z |
| Mô tả | Tham gia phát triển chuỗi cung ứng cùng Đông Hải Logistics, tạo ra kết quả có thể đo lường. |
| doanhnghiep_id | 11 |
| Tên công ty | Đông Hải Logistics |
| Ngành | Logistics |
| Avatar | — |

##### JD 6.3 — Fleet Technology Product Specialist

| Trường | Giá trị |
| --- | --- |
| ID | 26 |
| Tên vị trí | Fleet Technology Product Specialist |
| Phòng ban | Chuỗi cung ứng & Vận hành |
| Cấp bậc | Junior |
| Báo cáo cho | Trưởng bộ phận Chuỗi cung ứng & Vận hành |
| Nhiệm vụ | Phụ trách công việc Fleet Technology Product Specialist; phối hợp với đội ngũ chuỗi cung ứng & vận hành để hoàn thành mục tiêu. |
| Trình độ | Đại học chuyên ngành Logistics, Kinh tế hoặc Kỹ thuật |
| Kinh nghiệm | Từ 1 đến 3 năm kinh nghiệm liên quan |
| Kỹ năng | Supply Chain, Excel, SQL, quản lý vận hành |
| Kỹ năng mềm | Giao tiếp, làm việc nhóm, quản lý thời gian và tư duy giải quyết vấn đề |
| Ưu tiên | Có tư duy quy trình và sẵn sàng làm việc với dữ liệu vận hành |
| Mức lương | 10-23 triệu VNĐ/tháng |
| Phúc lợi | BHXH, thưởng hiệu suất, đào tạo chuyên môn và ngày nghỉ theo quy định |
| Môi trường | Kỷ luật, phối hợp thực địa và cải tiến liên tục |
| Địa điểm | Bình Dương, Việt Nam |
| Thời gian | Toàn thời gian |
| Hạn nộp | 31/12/2026 |
| Cách ứng tuyển | Nộp CV qua hệ thống Study2Work |
| Ngày tạo | 2026-09-16T14:42:44.322Z |
| Mô tả | Tham gia phát triển chuỗi cung ứng cùng Đông Hải Logistics, tạo ra kết quả có thể đo lường. |
| doanhnghiep_id | 11 |
| Tên công ty | Đông Hải Logistics |
| Ngành | Logistics |
| Avatar | — |

##### JD 6.4 — Warehouse Process Engineer

| Trường | Giá trị |
| --- | --- |
| ID | 27 |
| Tên vị trí | Warehouse Process Engineer |
| Phòng ban | Chuỗi cung ứng & Vận hành |
| Cấp bậc | Fresher |
| Báo cáo cho | Trưởng bộ phận Chuỗi cung ứng & Vận hành |
| Nhiệm vụ | Phụ trách công việc Warehouse Process Engineer; phối hợp với đội ngũ chuỗi cung ứng & vận hành để hoàn thành mục tiêu. |
| Trình độ | Đại học chuyên ngành Logistics, Kinh tế hoặc Kỹ thuật |
| Kinh nghiệm | Từ 0 đến 1 năm kinh nghiệm hoặc có dự án tương đương |
| Kỹ năng | Supply Chain, Excel, SQL, quản lý vận hành |
| Kỹ năng mềm | Giao tiếp, làm việc nhóm, quản lý thời gian và tư duy giải quyết vấn đề |
| Ưu tiên | Có tư duy quy trình và sẵn sàng làm việc với dữ liệu vận hành |
| Mức lương | 10-23 triệu VNĐ/tháng |
| Phúc lợi | BHXH, thưởng hiệu suất, đào tạo chuyên môn và ngày nghỉ theo quy định |
| Môi trường | Kỷ luật, phối hợp thực địa và cải tiến liên tục |
| Địa điểm | Bình Dương, Việt Nam |
| Thời gian | Toàn thời gian |
| Hạn nộp | 15/01/2027 |
| Cách ứng tuyển | Nộp CV qua hệ thống Study2Work |
| Ngày tạo | 2026-09-16T14:42:44.857Z |
| Mô tả | Tham gia phát triển chuỗi cung ứng cùng Đông Hải Logistics, tạo ra kết quả có thể đo lường. |
| doanhnghiep_id | 11 |
| Tên công ty | Đông Hải Logistics |
| Ngành | Logistics |
| Avatar | — |

### Doanh nghiệp 07 — Việt Thành Manufacturing

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 12 |
| Tên doanh nghiệp | Việt Thành Manufacturing |
| Email | seed.business.07@study2work.dev |
| Mật khẩu | WorkBusiness@123 |
| Địa chỉ | Đồng Nai, Việt Nam |
| Số điện thoại | 02513880007 |
| Ngành | Sản xuất |
| Mô tả doanh nghiệp | Nhà sản xuất công nghiệp chú trọng chất lượng, an toàn và tự động hóa dây chuyền. |
| Nhu cầu tuyển dụng | Chuẩn hóa quy trình và nâng hiệu suất nhà máy bằng công nghệ. |
| Avatar | — |

#### JD

##### JD 7.1 — Production Planning Engineer

| Trường | Giá trị |
| --- | --- |
| ID | 28 |
| Tên vị trí | Production Planning Engineer |
| Phòng ban | Kỹ thuật & Chất lượng |
| Cấp bậc | Junior |
| Báo cáo cho | Trưởng bộ phận Kỹ thuật & Chất lượng |
| Nhiệm vụ | Phụ trách công việc Production Planning Engineer; phối hợp với đội ngũ kỹ thuật & chất lượng để hoàn thành mục tiêu. |
| Trình độ | Đại học chuyên ngành Kỹ thuật, Cơ khí hoặc Quản lý công nghiệp |
| Kinh nghiệm | Từ 1 đến 3 năm kinh nghiệm liên quan |
| Kỹ năng | Lean, AutoCAD, Excel, kiểm soát chất lượng |
| Kỹ năng mềm | Giao tiếp, làm việc nhóm, quản lý thời gian và tư duy giải quyết vấn đề |
| Ưu tiên | Có tư duy cải tiến và tuân thủ an toàn lao động |
| Mức lương | 12-26 triệu VNĐ/tháng |
| Phúc lợi | BHXH, thưởng hiệu suất, đào tạo chuyên môn và ngày nghỉ theo quy định |
| Môi trường | Thực tế, an toàn và hướng tới cải tiến đo lường được |
| Địa điểm | Đồng Nai, Việt Nam |
| Thời gian | Toàn thời gian |
| Hạn nộp | 30/11/2026 |
| Cách ứng tuyển | Nộp CV qua hệ thống Study2Work |
| Ngày tạo | 2026-09-16T14:42:45.604Z |
| Mô tả | Tham gia phát triển sản xuất công nghiệp cùng Việt Thành Manufacturing, tạo ra kết quả có thể đo lường. |
| doanhnghiep_id | 12 |
| Tên công ty | Việt Thành Manufacturing |
| Ngành | Sản xuất |
| Avatar | — |

##### JD 7.2 — Quality Assurance Engineer

| Trường | Giá trị |
| --- | --- |
| ID | 29 |
| Tên vị trí | Quality Assurance Engineer |
| Phòng ban | Kỹ thuật & Chất lượng |
| Cấp bậc | Middle |
| Báo cáo cho | Trưởng bộ phận Kỹ thuật & Chất lượng |
| Nhiệm vụ | Phụ trách công việc Quality Assurance Engineer; phối hợp với đội ngũ kỹ thuật & chất lượng để hoàn thành mục tiêu. |
| Trình độ | Đại học chuyên ngành Kỹ thuật, Cơ khí hoặc Quản lý công nghiệp |
| Kinh nghiệm | Từ 1 đến 3 năm kinh nghiệm liên quan |
| Kỹ năng | Lean, AutoCAD, Excel, kiểm soát chất lượng |
| Kỹ năng mềm | Giao tiếp, làm việc nhóm, quản lý thời gian và tư duy giải quyết vấn đề |
| Ưu tiên | Có tư duy cải tiến và tuân thủ an toàn lao động |
| Mức lương | 12-26 triệu VNĐ/tháng |
| Phúc lợi | BHXH, thưởng hiệu suất, đào tạo chuyên môn và ngày nghỉ theo quy định |
| Môi trường | Thực tế, an toàn và hướng tới cải tiến đo lường được |
| Địa điểm | Đồng Nai, Việt Nam |
| Thời gian | Toàn thời gian |
| Hạn nộp | 15/12/2026 |
| Cách ứng tuyển | Nộp CV qua hệ thống Study2Work |
| Ngày tạo | 2026-09-16T14:42:46.171Z |
| Mô tả | Tham gia phát triển sản xuất công nghiệp cùng Việt Thành Manufacturing, tạo ra kết quả có thể đo lường. |
| doanhnghiep_id | 12 |
| Tên công ty | Việt Thành Manufacturing |
| Ngành | Sản xuất |
| Avatar | — |

##### JD 7.3 — Industrial Automation Engineer

| Trường | Giá trị |
| --- | --- |
| ID | 30 |
| Tên vị trí | Industrial Automation Engineer |
| Phòng ban | Kỹ thuật & Chất lượng |
| Cấp bậc | Junior |
| Báo cáo cho | Trưởng bộ phận Kỹ thuật & Chất lượng |
| Nhiệm vụ | Phụ trách công việc Industrial Automation Engineer; phối hợp với đội ngũ kỹ thuật & chất lượng để hoàn thành mục tiêu. |
| Trình độ | Đại học chuyên ngành Kỹ thuật, Cơ khí hoặc Quản lý công nghiệp |
| Kinh nghiệm | Từ 1 đến 3 năm kinh nghiệm liên quan |
| Kỹ năng | Lean, AutoCAD, Excel, kiểm soát chất lượng |
| Kỹ năng mềm | Giao tiếp, làm việc nhóm, quản lý thời gian và tư duy giải quyết vấn đề |
| Ưu tiên | Có tư duy cải tiến và tuân thủ an toàn lao động |
| Mức lương | 12-26 triệu VNĐ/tháng |
| Phúc lợi | BHXH, thưởng hiệu suất, đào tạo chuyên môn và ngày nghỉ theo quy định |
| Môi trường | Thực tế, an toàn và hướng tới cải tiến đo lường được |
| Địa điểm | Đồng Nai, Việt Nam |
| Thời gian | Toàn thời gian |
| Hạn nộp | 31/12/2026 |
| Cách ứng tuyển | Nộp CV qua hệ thống Study2Work |
| Ngày tạo | 2026-09-16T14:42:46.671Z |
| Mô tả | Tham gia phát triển sản xuất công nghiệp cùng Việt Thành Manufacturing, tạo ra kết quả có thể đo lường. |
| doanhnghiep_id | 12 |
| Tên công ty | Việt Thành Manufacturing |
| Ngành | Sản xuất |
| Avatar | — |

##### JD 7.4 — Procurement Specialist

| Trường | Giá trị |
| --- | --- |
| ID | 31 |
| Tên vị trí | Procurement Specialist |
| Phòng ban | Kỹ thuật & Chất lượng |
| Cấp bậc | Fresher |
| Báo cáo cho | Trưởng bộ phận Kỹ thuật & Chất lượng |
| Nhiệm vụ | Phụ trách công việc Procurement Specialist; phối hợp với đội ngũ kỹ thuật & chất lượng để hoàn thành mục tiêu. |
| Trình độ | Đại học chuyên ngành Kỹ thuật, Cơ khí hoặc Quản lý công nghiệp |
| Kinh nghiệm | Từ 0 đến 1 năm kinh nghiệm hoặc có dự án tương đương |
| Kỹ năng | Lean, AutoCAD, Excel, kiểm soát chất lượng |
| Kỹ năng mềm | Giao tiếp, làm việc nhóm, quản lý thời gian và tư duy giải quyết vấn đề |
| Ưu tiên | Có tư duy cải tiến và tuân thủ an toàn lao động |
| Mức lương | 12-26 triệu VNĐ/tháng |
| Phúc lợi | BHXH, thưởng hiệu suất, đào tạo chuyên môn và ngày nghỉ theo quy định |
| Môi trường | Thực tế, an toàn và hướng tới cải tiến đo lường được |
| Địa điểm | Đồng Nai, Việt Nam |
| Thời gian | Toàn thời gian |
| Hạn nộp | 15/01/2027 |
| Cách ứng tuyển | Nộp CV qua hệ thống Study2Work |
| Ngày tạo | 2026-09-16T14:42:47.189Z |
| Mô tả | Tham gia phát triển sản xuất công nghiệp cùng Việt Thành Manufacturing, tạo ra kết quả có thể đo lường. |
| doanhnghiep_id | 12 |
| Tên công ty | Việt Thành Manufacturing |
| Ngành | Sản xuất |
| Avatar | — |

### Doanh nghiệp 08 — An Tâm HealthTech

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 13 |
| Tên doanh nghiệp | An Tâm HealthTech |
| Email | seed.business.08@study2work.dev |
| Mật khẩu | WorkBusiness@123 |
| Địa chỉ | Huế, Việt Nam |
| Số điện thoại | 02343880008 |
| Ngành | Y tế - Chăm sóc sức khỏe |
| Mô tả doanh nghiệp | Công ty healthtech xây dựng giải pháp quản lý dịch vụ và dữ liệu chăm sóc sức khỏe. |
| Nhu cầu tuyển dụng | Ứng dụng công nghệ có trách nhiệm để hỗ trợ nhân viên y tế và bệnh nhân. |
| Avatar | — |

#### JD

##### JD 8.1 — Healthcare Product Specialist

| Trường | Giá trị |
| --- | --- |
| ID | 32 |
| Tên vị trí | Healthcare Product Specialist |
| Phòng ban | Sản phẩm & Dữ liệu Y tế |
| Cấp bậc | Junior |
| Báo cáo cho | Trưởng bộ phận Sản phẩm & Dữ liệu Y tế |
| Nhiệm vụ | Phụ trách công việc Healthcare Product Specialist; phối hợp với đội ngũ sản phẩm & dữ liệu y tế để hoàn thành mục tiêu. |
| Trình độ | Đại học chuyên ngành Y tế, Dữ liệu, CNTT hoặc Kinh doanh |
| Kinh nghiệm | Từ 1 đến 3 năm kinh nghiệm liên quan |
| Kỹ năng | SQL, phân tích dữ liệu, quy trình y tế, giao tiếp |
| Kỹ năng mềm | Giao tiếp, làm việc nhóm, quản lý thời gian và tư duy giải quyết vấn đề |
| Ưu tiên | Tôn trọng bảo mật dữ liệu và trải nghiệm bệnh nhân |
| Mức lương | 11-25 triệu VNĐ/tháng |
| Phúc lợi | BHXH, thưởng hiệu suất, đào tạo chuyên môn và ngày nghỉ theo quy định |
| Môi trường | Cẩn trọng, nhân văn và phối hợp với chuyên gia y tế |
| Địa điểm | Huế, Việt Nam |
| Thời gian | Toàn thời gian |
| Hạn nộp | 30/11/2026 |
| Cách ứng tuyển | Nộp CV qua hệ thống Study2Work |
| Ngày tạo | 2026-09-16T14:42:47.937Z |
| Mô tả | Tham gia phát triển chăm sóc sức khỏe số cùng An Tâm HealthTech, tạo ra kết quả có thể đo lường. |
| doanhnghiep_id | 13 |
| Tên công ty | An Tâm HealthTech |
| Ngành | Y tế - Chăm sóc sức khỏe |
| Avatar | — |

##### JD 8.2 — Clinical Data Analyst

| Trường | Giá trị |
| --- | --- |
| ID | 33 |
| Tên vị trí | Clinical Data Analyst |
| Phòng ban | Sản phẩm & Dữ liệu Y tế |
| Cấp bậc | Middle |
| Báo cáo cho | Trưởng bộ phận Sản phẩm & Dữ liệu Y tế |
| Nhiệm vụ | Phụ trách công việc Clinical Data Analyst; phối hợp với đội ngũ sản phẩm & dữ liệu y tế để hoàn thành mục tiêu. |
| Trình độ | Đại học chuyên ngành Y tế, Dữ liệu, CNTT hoặc Kinh doanh |
| Kinh nghiệm | Từ 1 đến 3 năm kinh nghiệm liên quan |
| Kỹ năng | SQL, phân tích dữ liệu, quy trình y tế, giao tiếp |
| Kỹ năng mềm | Giao tiếp, làm việc nhóm, quản lý thời gian và tư duy giải quyết vấn đề |
| Ưu tiên | Tôn trọng bảo mật dữ liệu và trải nghiệm bệnh nhân |
| Mức lương | 11-25 triệu VNĐ/tháng |
| Phúc lợi | BHXH, thưởng hiệu suất, đào tạo chuyên môn và ngày nghỉ theo quy định |
| Môi trường | Cẩn trọng, nhân văn và phối hợp với chuyên gia y tế |
| Địa điểm | Huế, Việt Nam |
| Thời gian | Toàn thời gian |
| Hạn nộp | 15/12/2026 |
| Cách ứng tuyển | Nộp CV qua hệ thống Study2Work |
| Ngày tạo | 2026-09-16T14:42:48.442Z |
| Mô tả | Tham gia phát triển chăm sóc sức khỏe số cùng An Tâm HealthTech, tạo ra kết quả có thể đo lường. |
| doanhnghiep_id | 13 |
| Tên công ty | An Tâm HealthTech |
| Ngành | Y tế - Chăm sóc sức khỏe |
| Avatar | — |

##### JD 8.3 — Backend Engineer

| Trường | Giá trị |
| --- | --- |
| ID | 34 |
| Tên vị trí | Backend Engineer |
| Phòng ban | Sản phẩm & Dữ liệu Y tế |
| Cấp bậc | Junior |
| Báo cáo cho | Trưởng bộ phận Sản phẩm & Dữ liệu Y tế |
| Nhiệm vụ | Phụ trách công việc Backend Engineer; phối hợp với đội ngũ sản phẩm & dữ liệu y tế để hoàn thành mục tiêu. |
| Trình độ | Đại học chuyên ngành Y tế, Dữ liệu, CNTT hoặc Kinh doanh |
| Kinh nghiệm | Từ 1 đến 3 năm kinh nghiệm liên quan |
| Kỹ năng | SQL, phân tích dữ liệu, quy trình y tế, giao tiếp |
| Kỹ năng mềm | Giao tiếp, làm việc nhóm, quản lý thời gian và tư duy giải quyết vấn đề |
| Ưu tiên | Tôn trọng bảo mật dữ liệu và trải nghiệm bệnh nhân |
| Mức lương | 11-25 triệu VNĐ/tháng |
| Phúc lợi | BHXH, thưởng hiệu suất, đào tạo chuyên môn và ngày nghỉ theo quy định |
| Môi trường | Cẩn trọng, nhân văn và phối hợp với chuyên gia y tế |
| Địa điểm | Huế, Việt Nam |
| Thời gian | Toàn thời gian |
| Hạn nộp | 31/12/2026 |
| Cách ứng tuyển | Nộp CV qua hệ thống Study2Work |
| Ngày tạo | 2026-09-16T14:42:48.971Z |
| Mô tả | Tham gia phát triển chăm sóc sức khỏe số cùng An Tâm HealthTech, tạo ra kết quả có thể đo lường. |
| doanhnghiep_id | 13 |
| Tên công ty | An Tâm HealthTech |
| Ngành | Y tế - Chăm sóc sức khỏe |
| Avatar | — |

##### JD 8.4 — Customer Care Supervisor

| Trường | Giá trị |
| --- | --- |
| ID | 35 |
| Tên vị trí | Customer Care Supervisor |
| Phòng ban | Sản phẩm & Dữ liệu Y tế |
| Cấp bậc | Fresher |
| Báo cáo cho | Trưởng bộ phận Sản phẩm & Dữ liệu Y tế |
| Nhiệm vụ | Phụ trách công việc Customer Care Supervisor; phối hợp với đội ngũ sản phẩm & dữ liệu y tế để hoàn thành mục tiêu. |
| Trình độ | Đại học chuyên ngành Y tế, Dữ liệu, CNTT hoặc Kinh doanh |
| Kinh nghiệm | Từ 0 đến 1 năm kinh nghiệm hoặc có dự án tương đương |
| Kỹ năng | SQL, phân tích dữ liệu, quy trình y tế, giao tiếp |
| Kỹ năng mềm | Giao tiếp, làm việc nhóm, quản lý thời gian và tư duy giải quyết vấn đề |
| Ưu tiên | Tôn trọng bảo mật dữ liệu và trải nghiệm bệnh nhân |
| Mức lương | 11-25 triệu VNĐ/tháng |
| Phúc lợi | BHXH, thưởng hiệu suất, đào tạo chuyên môn và ngày nghỉ theo quy định |
| Môi trường | Cẩn trọng, nhân văn và phối hợp với chuyên gia y tế |
| Địa điểm | Huế, Việt Nam |
| Thời gian | Toàn thời gian |
| Hạn nộp | 15/01/2027 |
| Cách ứng tuyển | Nộp CV qua hệ thống Study2Work |
| Ngày tạo | 2026-09-16T14:42:49.472Z |
| Mô tả | Tham gia phát triển chăm sóc sức khỏe số cùng An Tâm HealthTech, tạo ra kết quả có thể đo lường. |
| doanhnghiep_id | 13 |
| Tên công ty | An Tâm HealthTech |
| Ngành | Y tế - Chăm sóc sức khỏe |
| Avatar | — |

### Doanh nghiệp 09 — Lữ Hành Việt Hospitality

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 14 |
| Tên doanh nghiệp | Lữ Hành Việt Hospitality |
| Email | seed.business.09@study2work.dev |
| Mật khẩu | WorkBusiness@123 |
| Địa chỉ | Nha Trang, Việt Nam |
| Số điện thoại | 02583880009 |
| Ngành | Du lịch - Khách sạn |
| Mô tả doanh nghiệp | Thương hiệu du lịch và lưu trú phát triển trải nghiệm địa phương cho khách trong nước và quốc tế. |
| Nhu cầu tuyển dụng | Mang đến dịch vụ thân thiện, nhất quán và giàu bản sắc địa phương. |
| Avatar | — |

#### JD

##### JD 9.1 — Travel Consultant

| Trường | Giá trị |
| --- | --- |
| ID | 36 |
| Tên vị trí | Travel Consultant |
| Phòng ban | Kinh doanh & Dịch vụ |
| Cấp bậc | Junior |
| Báo cáo cho | Trưởng bộ phận Kinh doanh & Dịch vụ |
| Nhiệm vụ | Phụ trách công việc Travel Consultant; phối hợp với đội ngũ kinh doanh & dịch vụ để hoàn thành mục tiêu. |
| Trình độ | Cao đẳng/Đại học chuyên ngành Du lịch, Khách sạn hoặc Ngoại ngữ |
| Kinh nghiệm | Từ 1 đến 3 năm kinh nghiệm liên quan |
| Kỹ năng | Tiếng Anh, bán hàng, chăm sóc khách hàng, Excel |
| Kỹ năng mềm | Giao tiếp, làm việc nhóm, quản lý thời gian và tư duy giải quyết vấn đề |
| Ưu tiên | Giao tiếp tốt, chủ động và yêu thích dịch vụ khách hàng |
| Mức lương | 8-18 triệu VNĐ/tháng |
| Phúc lợi | BHXH, thưởng hiệu suất, đào tạo chuyên môn và ngày nghỉ theo quy định |
| Môi trường | Thân thiện, đa văn hóa và chú trọng trải nghiệm khách hàng |
| Địa điểm | Nha Trang, Việt Nam |
| Thời gian | Toàn thời gian |
| Hạn nộp | 30/11/2026 |
| Cách ứng tuyển | Nộp CV qua hệ thống Study2Work |
| Ngày tạo | 2026-09-16T14:42:50.243Z |
| Mô tả | Tham gia phát triển du lịch và lưu trú cùng Lữ Hành Việt Hospitality, tạo ra kết quả có thể đo lường. |
| doanhnghiep_id | 14 |
| Tên công ty | Lữ Hành Việt Hospitality |
| Ngành | Du lịch - Khách sạn |
| Avatar | — |

##### JD 9.2 — Hotel Operations Executive

| Trường | Giá trị |
| --- | --- |
| ID | 37 |
| Tên vị trí | Hotel Operations Executive |
| Phòng ban | Kinh doanh & Dịch vụ |
| Cấp bậc | Middle |
| Báo cáo cho | Trưởng bộ phận Kinh doanh & Dịch vụ |
| Nhiệm vụ | Phụ trách công việc Hotel Operations Executive; phối hợp với đội ngũ kinh doanh & dịch vụ để hoàn thành mục tiêu. |
| Trình độ | Cao đẳng/Đại học chuyên ngành Du lịch, Khách sạn hoặc Ngoại ngữ |
| Kinh nghiệm | Từ 1 đến 3 năm kinh nghiệm liên quan |
| Kỹ năng | Tiếng Anh, bán hàng, chăm sóc khách hàng, Excel |
| Kỹ năng mềm | Giao tiếp, làm việc nhóm, quản lý thời gian và tư duy giải quyết vấn đề |
| Ưu tiên | Giao tiếp tốt, chủ động và yêu thích dịch vụ khách hàng |
| Mức lương | 8-18 triệu VNĐ/tháng |
| Phúc lợi | BHXH, thưởng hiệu suất, đào tạo chuyên môn và ngày nghỉ theo quy định |
| Môi trường | Thân thiện, đa văn hóa và chú trọng trải nghiệm khách hàng |
| Địa điểm | Nha Trang, Việt Nam |
| Thời gian | Toàn thời gian |
| Hạn nộp | 15/12/2026 |
| Cách ứng tuyển | Nộp CV qua hệ thống Study2Work |
| Ngày tạo | 2026-09-16T14:42:50.746Z |
| Mô tả | Tham gia phát triển du lịch và lưu trú cùng Lữ Hành Việt Hospitality, tạo ra kết quả có thể đo lường. |
| doanhnghiep_id | 14 |
| Tên công ty | Lữ Hành Việt Hospitality |
| Ngành | Du lịch - Khách sạn |
| Avatar | — |

##### JD 9.3 — Digital Marketing Executive

| Trường | Giá trị |
| --- | --- |
| ID | 38 |
| Tên vị trí | Digital Marketing Executive |
| Phòng ban | Kinh doanh & Dịch vụ |
| Cấp bậc | Junior |
| Báo cáo cho | Trưởng bộ phận Kinh doanh & Dịch vụ |
| Nhiệm vụ | Phụ trách công việc Digital Marketing Executive; phối hợp với đội ngũ kinh doanh & dịch vụ để hoàn thành mục tiêu. |
| Trình độ | Cao đẳng/Đại học chuyên ngành Du lịch, Khách sạn hoặc Ngoại ngữ |
| Kinh nghiệm | Từ 1 đến 3 năm kinh nghiệm liên quan |
| Kỹ năng | Tiếng Anh, bán hàng, chăm sóc khách hàng, Excel |
| Kỹ năng mềm | Giao tiếp, làm việc nhóm, quản lý thời gian và tư duy giải quyết vấn đề |
| Ưu tiên | Giao tiếp tốt, chủ động và yêu thích dịch vụ khách hàng |
| Mức lương | 8-18 triệu VNĐ/tháng |
| Phúc lợi | BHXH, thưởng hiệu suất, đào tạo chuyên môn và ngày nghỉ theo quy định |
| Môi trường | Thân thiện, đa văn hóa và chú trọng trải nghiệm khách hàng |
| Địa điểm | Nha Trang, Việt Nam |
| Thời gian | Toàn thời gian |
| Hạn nộp | 31/12/2026 |
| Cách ứng tuyển | Nộp CV qua hệ thống Study2Work |
| Ngày tạo | 2026-09-16T14:42:51.246Z |
| Mô tả | Tham gia phát triển du lịch và lưu trú cùng Lữ Hành Việt Hospitality, tạo ra kết quả có thể đo lường. |
| doanhnghiep_id | 14 |
| Tên công ty | Lữ Hành Việt Hospitality |
| Ngành | Du lịch - Khách sạn |
| Avatar | — |

##### JD 9.4 — Front Office Supervisor

| Trường | Giá trị |
| --- | --- |
| ID | 39 |
| Tên vị trí | Front Office Supervisor |
| Phòng ban | Kinh doanh & Dịch vụ |
| Cấp bậc | Fresher |
| Báo cáo cho | Trưởng bộ phận Kinh doanh & Dịch vụ |
| Nhiệm vụ | Phụ trách công việc Front Office Supervisor; phối hợp với đội ngũ kinh doanh & dịch vụ để hoàn thành mục tiêu. |
| Trình độ | Cao đẳng/Đại học chuyên ngành Du lịch, Khách sạn hoặc Ngoại ngữ |
| Kinh nghiệm | Từ 0 đến 1 năm kinh nghiệm hoặc có dự án tương đương |
| Kỹ năng | Tiếng Anh, bán hàng, chăm sóc khách hàng, Excel |
| Kỹ năng mềm | Giao tiếp, làm việc nhóm, quản lý thời gian và tư duy giải quyết vấn đề |
| Ưu tiên | Giao tiếp tốt, chủ động và yêu thích dịch vụ khách hàng |
| Mức lương | 8-18 triệu VNĐ/tháng |
| Phúc lợi | BHXH, thưởng hiệu suất, đào tạo chuyên môn và ngày nghỉ theo quy định |
| Môi trường | Thân thiện, đa văn hóa và chú trọng trải nghiệm khách hàng |
| Địa điểm | Nha Trang, Việt Nam |
| Thời gian | Toàn thời gian |
| Hạn nộp | 15/01/2027 |
| Cách ứng tuyển | Nộp CV qua hệ thống Study2Work |
| Ngày tạo | 2026-09-16T14:42:51.739Z |
| Mô tả | Tham gia phát triển du lịch và lưu trú cùng Lữ Hành Việt Hospitality, tạo ra kết quả có thể đo lường. |
| doanhnghiep_id | 14 |
| Tên công ty | Lữ Hành Việt Hospitality |
| Ngành | Du lịch - Khách sạn |
| Avatar | — |

### Doanh nghiệp 10 — Green Horizon Energy

| Trường | Giá trị |
| --- | --- |
| ID tài khoản | 15 |
| Tên doanh nghiệp | Green Horizon Energy |
| Email | seed.business.10@study2work.dev |
| Mật khẩu | WorkBusiness@123 |
| Địa chỉ | Quảng Ninh, Việt Nam |
| Số điện thoại | 02033880010 |
| Ngành | Năng lượng xanh |
| Mô tả doanh nghiệp | Doanh nghiệp năng lượng tái tạo triển khai giải pháp điện mặt trời và quản lý phát thải. |
| Nhu cầu tuyển dụng | Thúc đẩy chuyển dịch năng lượng bằng dự án hiệu quả và bền vững. |
| Avatar | — |

#### JD

##### JD 10.1 — Solar Project Engineer

| Trường | Giá trị |
| --- | --- |
| ID | 40 |
| Tên vị trí | Solar Project Engineer |
| Phòng ban | Dự án & Phát triển bền vững |
| Cấp bậc | Junior |
| Báo cáo cho | Trưởng bộ phận Dự án & Phát triển bền vững |
| Nhiệm vụ | Phụ trách công việc Solar Project Engineer; phối hợp với đội ngũ dự án & phát triển bền vững để hoàn thành mục tiêu. |
| Trình độ | Đại học chuyên ngành Kỹ thuật, Môi trường hoặc Kinh tế |
| Kinh nghiệm | Từ 1 đến 3 năm kinh nghiệm liên quan |
| Kỹ năng | AutoCAD, Excel, IoT, phân tích phát thải |
| Kỹ năng mềm | Giao tiếp, làm việc nhóm, quản lý thời gian và tư duy giải quyết vấn đề |
| Ưu tiên | Quan tâm đến phát triển bền vững và an toàn dự án |
| Mức lương | 12-28 triệu VNĐ/tháng |
| Phúc lợi | BHXH, thưởng hiệu suất, đào tạo chuyên môn và ngày nghỉ theo quy định |
| Môi trường | Định hướng tác động, an toàn và làm việc liên ngành |
| Địa điểm | Quảng Ninh, Việt Nam |
| Thời gian | Toàn thời gian |
| Hạn nộp | 30/11/2026 |
| Cách ứng tuyển | Nộp CV qua hệ thống Study2Work |
| Ngày tạo | 2026-09-16T14:42:52.496Z |
| Mô tả | Tham gia phát triển năng lượng tái tạo cùng Green Horizon Energy, tạo ra kết quả có thể đo lường. |
| doanhnghiep_id | 15 |
| Tên công ty | Green Horizon Energy |
| Ngành | Năng lượng xanh |
| Avatar | — |

##### JD 10.2 — Sustainability Analyst

| Trường | Giá trị |
| --- | --- |
| ID | 41 |
| Tên vị trí | Sustainability Analyst |
| Phòng ban | Dự án & Phát triển bền vững |
| Cấp bậc | Middle |
| Báo cáo cho | Trưởng bộ phận Dự án & Phát triển bền vững |
| Nhiệm vụ | Phụ trách công việc Sustainability Analyst; phối hợp với đội ngũ dự án & phát triển bền vững để hoàn thành mục tiêu. |
| Trình độ | Đại học chuyên ngành Kỹ thuật, Môi trường hoặc Kinh tế |
| Kinh nghiệm | Từ 1 đến 3 năm kinh nghiệm liên quan |
| Kỹ năng | AutoCAD, Excel, IoT, phân tích phát thải |
| Kỹ năng mềm | Giao tiếp, làm việc nhóm, quản lý thời gian và tư duy giải quyết vấn đề |
| Ưu tiên | Quan tâm đến phát triển bền vững và an toàn dự án |
| Mức lương | 12-28 triệu VNĐ/tháng |
| Phúc lợi | BHXH, thưởng hiệu suất, đào tạo chuyên môn và ngày nghỉ theo quy định |
| Môi trường | Định hướng tác động, an toàn và làm việc liên ngành |
| Địa điểm | Quảng Ninh, Việt Nam |
| Thời gian | Toàn thời gian |
| Hạn nộp | 15/12/2026 |
| Cách ứng tuyển | Nộp CV qua hệ thống Study2Work |
| Ngày tạo | 2026-09-16T14:42:53.004Z |
| Mô tả | Tham gia phát triển năng lượng tái tạo cùng Green Horizon Energy, tạo ra kết quả có thể đo lường. |
| doanhnghiep_id | 15 |
| Tên công ty | Green Horizon Energy |
| Ngành | Năng lượng xanh |
| Avatar | — |

##### JD 10.3 — IoT Field Engineer

| Trường | Giá trị |
| --- | --- |
| ID | 42 |
| Tên vị trí | IoT Field Engineer |
| Phòng ban | Dự án & Phát triển bền vững |
| Cấp bậc | Junior |
| Báo cáo cho | Trưởng bộ phận Dự án & Phát triển bền vững |
| Nhiệm vụ | Phụ trách công việc IoT Field Engineer; phối hợp với đội ngũ dự án & phát triển bền vững để hoàn thành mục tiêu. |
| Trình độ | Đại học chuyên ngành Kỹ thuật, Môi trường hoặc Kinh tế |
| Kinh nghiệm | Từ 1 đến 3 năm kinh nghiệm liên quan |
| Kỹ năng | AutoCAD, Excel, IoT, phân tích phát thải |
| Kỹ năng mềm | Giao tiếp, làm việc nhóm, quản lý thời gian và tư duy giải quyết vấn đề |
| Ưu tiên | Quan tâm đến phát triển bền vững và an toàn dự án |
| Mức lương | 12-28 triệu VNĐ/tháng |
| Phúc lợi | BHXH, thưởng hiệu suất, đào tạo chuyên môn và ngày nghỉ theo quy định |
| Môi trường | Định hướng tác động, an toàn và làm việc liên ngành |
| Địa điểm | Quảng Ninh, Việt Nam |
| Thời gian | Toàn thời gian |
| Hạn nộp | 31/12/2026 |
| Cách ứng tuyển | Nộp CV qua hệ thống Study2Work |
| Ngày tạo | 2026-09-16T14:42:53.509Z |
| Mô tả | Tham gia phát triển năng lượng tái tạo cùng Green Horizon Energy, tạo ra kết quả có thể đo lường. |
| doanhnghiep_id | 15 |
| Tên công ty | Green Horizon Energy |
| Ngành | Năng lượng xanh |
| Avatar | — |

##### JD 10.4 — Business Development Executive

| Trường | Giá trị |
| --- | --- |
| ID | 43 |
| Tên vị trí | Business Development Executive |
| Phòng ban | Dự án & Phát triển bền vững |
| Cấp bậc | Fresher |
| Báo cáo cho | Trưởng bộ phận Dự án & Phát triển bền vững |
| Nhiệm vụ | Phụ trách công việc Business Development Executive; phối hợp với đội ngũ dự án & phát triển bền vững để hoàn thành mục tiêu. |
| Trình độ | Đại học chuyên ngành Kỹ thuật, Môi trường hoặc Kinh tế |
| Kinh nghiệm | Từ 0 đến 1 năm kinh nghiệm hoặc có dự án tương đương |
| Kỹ năng | AutoCAD, Excel, IoT, phân tích phát thải |
| Kỹ năng mềm | Giao tiếp, làm việc nhóm, quản lý thời gian và tư duy giải quyết vấn đề |
| Ưu tiên | Quan tâm đến phát triển bền vững và an toàn dự án |
| Mức lương | 12-28 triệu VNĐ/tháng |
| Phúc lợi | BHXH, thưởng hiệu suất, đào tạo chuyên môn và ngày nghỉ theo quy định |
| Môi trường | Định hướng tác động, an toàn và làm việc liên ngành |
| Địa điểm | Quảng Ninh, Việt Nam |
| Thời gian | Toàn thời gian |
| Hạn nộp | 15/01/2027 |
| Cách ứng tuyển | Nộp CV qua hệ thống Study2Work |
| Ngày tạo | 2026-09-16T14:42:54.028Z |
| Mô tả | Tham gia phát triển năng lượng tái tạo cùng Green Horizon Energy, tạo ra kết quả có thể đo lường. |
| doanhnghiep_id | 15 |
| Tên công ty | Green Horizon Energy |
| Ngành | Năng lượng xanh |
| Avatar | — |

