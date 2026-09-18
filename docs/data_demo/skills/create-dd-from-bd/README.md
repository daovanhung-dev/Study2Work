# NanoBio DD Creation Skill Pack

Bộ tài liệu và công cụ để đọc BD/BRD/product flow, tạo DD module có thể triển khai,
giữ traceability và review được bằng checklist/validator.

## Bắt đầu nhanh

1. Đọc [SKILL.md](SKILL.md).
2. Đi theo [references/INDEX.md](references/INDEX.md).
3. Sao chép [template/](template/) cho module mới.
4. Xem [examples/README.md](examples/README.md) để chọn mẫu tương tự.
5. Chạy validator trước khi gửi review.

## Quy tắc nguồn

`docs/DD/<module>/` là nguồn DD canonical hiện hành. Thư mục `examples/` là các
snapshot `Reference` độc lập để học và copy offline, không thay thế DD canonical.

Package này được xây dựng từ workflow `docs-dd`, skill `create-dd-from-bd`, DD
guide/template và các DD M01-M19 đã hoàn thiện trong repo.

## Thành phần

- `SKILL.md`: entrypoint ngắn và output contract.
- `references/`: hướng dẫn theo từng giai đoạn, đọc theo thứ tự.
- `template/`: skeleton DD có placeholder có chủ đích.
- `examples/`: 10 module DD đầy đủ làm mẫu.
- `checklists/`: preflight, authoring, review và Ready/Done.
- `scripts/validate_dd_pack.py`: kiểm tra tĩnh cấu trúc, ID, link, status và placeholder.
