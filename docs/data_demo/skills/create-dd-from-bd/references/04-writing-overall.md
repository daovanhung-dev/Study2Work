# 04 — Viết Overall.md

`Overall.md` là nguồn sự thật cấp module, không phải bản sao của BD. Viết theo
thứ tự trong template:

1. Document information và status axes.
2. Business goal, measurable outcome và non-goals.
3. Module boundary và context.
4. Roles/permissions/limitations.
5. Primary entities, ownership, retention và sensitivity.
6. State machine và transition conditions.
7. Business rules có mã, điều kiện, enforcement location và violation result.
8. Happy path, alternate path và error path.
9. API/event/storage/integration dependencies và failure behavior.
10. NFR: security, integrity, performance, resilience, observability, accessibility.
11. Risks, assumptions, open questions và ADR.
12. Traceability matrix.

## Không làm

- Không ghi chi tiết function vào Overall thay cho `Function_List.md`.
- Không coi status `Approved` là bằng chứng runtime.
- Không biến implementation proposal thành business decision.
- Không bỏ qua failure path, quyền, idempotency hoặc dữ liệu nhạy cảm.
