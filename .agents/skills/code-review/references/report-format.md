# Code review report format

Write concise Vietnamese. Keep code identifiers, file paths, and contract names
as written in the repository.

```markdown
## Tóm tắt
- Mục tiêu/phạm vi: <đoạn diff hoặc path/module đã review>
- Kết quả: <số vấn đề và tóm tắt ngắn>
- Kiểm tra: <test source đã đọc; không chạy test>

## Trạng thái tiêu chí
- Tuân thủ quy tắc: <Có vấn đề | Không thấy vấn đề trong phạm vi đã review | Chưa đủ bằng chứng>
- Tái sử dụng: <cùng các trạng thái trên>
- Mã sạch và dễ bảo trì: <cùng các trạng thái trên>
- Bảo mật: <cùng các trạng thái trên>

## Phát hiện
### [P1] <tiêu đề ngắn, nêu đúng vấn đề>
- Nguồn gốc: <do diff gây ra | vấn đề hiện trạng>
- Vị trí: `path/to/file.ext:line`
- Tình huống và ảnh hưởng: <điều gì xảy ra và vì sao có tác động>
- Bằng chứng: <caller/contract/test/source liên quan>
- Hướng xử lý: <gợi ý ngắn; không áp dụng thay đổi>

## Giới hạn
- <source còn thiếu, contract chưa rõ hoặc giới hạn xác minh>
```

For no findings, replace the findings list with:

> Không có vấn đề cần xử lý trong phạm vi đã review.

Keep the criterion status distinct from the issue list. Use `Chưa đủ bằng
chứng` when the relevant path, rule, contract, or comparison range could not be
verified; do not turn missing evidence into a clean result. Always say tests
were not run. Do not add generic praise or long lists of hypothetical
recommendations.
