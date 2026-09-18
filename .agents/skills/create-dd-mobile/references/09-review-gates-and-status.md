# 09 — Review Gates và Status

## Bốn trục độc lập

| Trục | Giá trị |
|---|---|
| Lifecycle | `Current`, `Historical`, `Generated`, `Reference`, `Source`, `Binary` |
| DD decision | `Draft`, `In Review`, `Approved`, `Deprecated` |
| Implementation | `Implemented`, `Partial`, `Placeholder`, `Source-only`, `Absent`, `N/A` |
| Verification | `Static-verified`, `Runtime-unverified`, `Sandbox-unverified`, `Historical` |

`Approved` chỉ là quyết định tài liệu. `Implemented` chỉ được dùng khi capability
reachable/source evidence tồn tại. Device, production và Supabase sandbox phải
ghi verification riêng.

## Gates

1. **Preflight:** source BD, module code, dependency và context đã xác định.
2. **Authoring:** đủ required files, scope/rule/flow/traceability.
3. **Review:** BA/PO chốt business, Tech Lead chốt architecture, QA chốt testability.
4. **Static validation:** validator PASS, link không hỏng, không placeholder ở DD thật.
5. **Project validation:** worklog, docs/context integrity và whitespace check PASS.

Open question ảnh hưởng behavior, schema, security, payment, quota hoặc acceptance
không được ẩn dưới implementation default và không được coi là Done.
