# 01 — Phân tích Input và Evidence

## Mục tiêu

Tách điều BD đã quyết định khỏi điều source đang làm, điều chưa biết và đề xuất
implementation. DD phải giúp reviewer biết câu nào là requirement và câu nào
là giả định.

## Bảng evidence tối thiểu

| Evidence | Nội dung cần ghi | Cách dùng |
|---|---|---|
| BD heading/ID | Requirement, actor, flow, rule, AC | Nguồn nghiệp vụ chính |
| DD dependency | Contract đã chốt ở module khác | Không định nghĩa lại |
| Runtime source | Route, provider, repository, API/SQL reachable | Chỉ ghi implementation claim có bằng chứng |
| Test | Assertion hoặc test case | Chứng minh behavior được kiểm tra |
| Worklog/issue | Lịch sử hoặc gap | Evidence lịch sử, không ghi đè runtime hiện tại |
| User instruction | Quyết định mới trong request | Ghi rõ là explicit user instruction |

## Conflict protocol

Khi BD, DD và source mâu thuẫn:

1. Ghi riêng từng fact và source path.
2. Không âm thầm chọn một bên.
3. Đánh dấu `OPEN QUESTION`, `ASSUMPTION` hoặc `PROPOSAL` nếu chưa có quyết định.
4. Nếu claim implementation, ưu tiên code reachable từ `lib/main.dart`, SQL/schema
   thực thi, config/package, test rồi mới tới docs.
5. Ghi conflict vào `Overall.md` và ảnh hưởng tới Feature/Function/View.

## Extraction sheet trước khi viết

- Module purpose và boundaries.
- Actor/role và permission/limitation.
- Primary entities, owner, retention và sensitivity.
- States và state transitions.
- Happy path, alternate path, error path.
- Business rules và acceptance criteria.
- API/event/storage/notification/AI dependencies.
- Open questions, assumptions, proposals và out-of-scope.
