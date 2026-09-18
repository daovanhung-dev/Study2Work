# 08 — Import/File map, Diagrams, Assets và History

## Import_File.md

Ghi file create/modify, layer, responsibility, allowed imports, forbidden imports,
public exports, API/datasource/model mapping, config key và test file. Đây là
dependency intent map, không phải danh sách import tự động của IDE.

Không cho phép:

- Presentation → DAO/database/API client trực tiếp.
- Domain/use case → UI framework hoặc implementation cụ thể.
- Import ngược layer hoặc circular dependency.
- Hard-code secret/config production.

## Diagrams

Chỉ thêm sơ đồ khi giúp hiểu flow, sequence, state, context hoặc dependency.
Tên file khuyến nghị: `context.mmd`, `overall-flow.mmd`,
`feature-flow-Fxx.mmd`, `sequence-Fxx.mmd`, `state-entity.mmd`.
Mỗi sơ đồ phải liên kết tới ID DD; sơ đồ không thay thế bảng mô tả.

## Assets

Chỉ lưu mockup, wireframe, screenshot test không chứa production PII, secret,
token hoặc raw payment/health evidence. Ghi asset thiếu dưới dạng open question.

## History

`history/CHANGELOG.md` ghi ngày, version, source, người/agent, thay đổi, ảnh
hưởng, validation và unresolved decisions. Không sửa nội dung lịch sử đã thay thế.
