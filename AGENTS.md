# Study2Work agent router

Đây là điểm vào bắt buộc cho coding agent. File này chỉ định tuyến; chi tiết nằm
trong `.agents/` và source hiện tại luôn phải được kiểm tra lại trước khi sửa.

## 1. Phân loại task

Trước khi đọc sâu, ghi ngắn:

```text
primary_task_type: coding | fix | docs | test
secondary_task_types:
  - <loại khác, nếu có>
project_scope: mobile-work | web-work | server-work | server-study | server-ai
```

- `coding`: requirement/DD -> pattern hiện có -> implementation -> test.
- `fix`: reproduce -> trace caller/callee/effect -> root cause -> smallest fix -> regression test.
- `docs`: source -> verified tests/contracts -> tài liệu hiện có -> cập nhật.
- `test`: requirement/contract -> implementation -> edge cases -> convention test.

## 2. Định tuyến scope

| Scope | Source chính | Đọc tiếp |
|---|---|---|
| `mobile-work` | `apps/work-client/mobile/` | `.agents/mobile-work/AGENTS.md` |
| `web-work` | `apps/study-client/`, `apps/work-client/web/` | `.agents/web-work/AGENTS.md` |
| `server-work` | `apps/work-server/` | `.agents/server-work/AGENTS.md` |
| `server-study` | `apps/study-server/` | `.agents/server-study/AGENTS.md` |
| `server-ai` | `apps/ai-server/` | `.agents/server-ai/AGENTS.md` |

Không nạp hoặc trộn scope khác nếu chưa xác nhận dependency. Task qua nhiều
scope phải ghi từng dependency và contract nối giữa chúng.

## 3. Progressive loading

```text
AGENTS.md
  -> .agents/<scope>/AGENTS.md
  -> module/API context được scope chỉ định
  -> core/service/database context thực sự được gọi
  -> exact source + tests + config liên quan
```

Không đọc toàn bộ repository cho task cục bộ. Xem `.agents/AGENTS.md` khi cần
tra index hoặc cập nhật chính bộ context.

## 4. Source of truth

1. Yêu cầu mới nhất của người dùng.
2. Router/context này để xác định file cần đọc.
3. DD/contract canonical còn tồn tại trong working tree.
4. `docs/business_code/`.
5. Runtime/source code hiện tại.
6. Test đã xác minh.
7. Config/dependency và tài liệu hỗ trợ.

Khi nội dung mâu thuẫn, không âm thầm chọn một bên. Ghi discrepancy; với mô tả
runtime, ưu tiên `source đang chạy > test đã xác minh > tài liệu`. Hiện trạng
nguồn quan trọng nằm tại `.agents/project/source-status.md`.

## 5. Luật bắt buộc

- Không tự tạo API, field, table, validation, service, business code hoặc HTTP
  behavior khi chưa có bằng chứng từ requirement, DD, contract, source, schema
  hoặc test đáng tin cậy.
- Chỉ sửa file tối thiểu cho task; không refactor ngoài phạm vi.
- Trước khi sửa function, trace caller, callee, DB/side effect, response,
  business code và test bị ảnh hưởng.
- Tái sử dụng helper/pattern hiện có; không ép kiến trúc của một server lên
  server khác.
- Giữ API contract ngoài phạm vi thay đổi; kiểm tra regression và cập nhật
  context tương ứng khi code/contract/DB/convention đổi.
