# Nguồn tham khảo quốc tế áp dụng vào UTC Screen Skill

Bộ skill này **tham khảo phương pháp** kiểm thử và tài liệu hóa; không phải biểu mẫu do các tổ chức phát hành, không chứng nhận tuân thủ.

| Nguồn chính thức | Tài liệu / URL | Cách áp dụng |
|---|---|---|
| ISTQB | CTFL Syllabus v4.0.1, https://istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf | Phân tích & thiết kế test, phân hoạch tương đương, giá trị biên, bảng quyết định, chuyển trạng thái, truy vết và đánh giá kết quả |
| ISO | ISO/IEC/IEEE 29119-3:2021, https://www.iso.org/standard/79429.html | Nguyên tắc chuẩn hóa tài liệu kiểm thử: định danh, điều kiện, dữ liệu, bước, expected/actual, kết quả và quản lý tài liệu; không sao chép nội dung tiêu chuẩn trả phí |
| W3C | WCAG 2.2, https://www.w3.org/TR/WCAG22/ | Câu hỏi kiểm thử khả năng tiếp cận (bàn phím, focus, label, lỗi) khi điều kiện nghiệm thu có căn cứ |
| OWASP | Web Security Testing Guide, https://owasp.org/www-project-web-security-testing-guide/ | Tình huống security khi DD có xác thực/phân quyền/phiên/đầu vào; không coi UTC Screen thay cho kiểm thử an ninh chuyên sâu |

## Quy tắc áp dụng

1. **DD và hợp đồng API của dự án là nguồn yêu cầu nghiệp vụ.** Tài liệu quốc tế là nguồn phương pháp, không có quyền tạo tính năng chưa được phê duyệt.
2. Các phép thử thuộc WCAG/OWASP chưa có DD có thể đề xuất nhưng phải có trạng thái `Chờ xác nhận` nếu chưa được chọn làm yêu cầu nghiệm thu.
3. Không chấm tính tuân thủ ISTQB/ISO/WCAG/OWASP một cách tuyệt đối từ một file UTC; phải có audit ngoài phạm vi skill.
4. Luôn ghi nguồn cụ thể và phiên bản/đường dẫn tài liệu đã dùng khi phát hành chính thức.
