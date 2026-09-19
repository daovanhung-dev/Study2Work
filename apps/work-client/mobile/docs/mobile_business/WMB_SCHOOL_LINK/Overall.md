# WMB_SCHOOL_LINK / Liên kết nhà trường

## Evidence và status

| Trục | Giá trị |
|---|---|
| Lifecycle | Current |
| DD decision | Draft |
| Implementation | Source-only |
| Verification | Static-verified; Runtime-unverified |
| Source baseline | 212455f627846c0a3dc56107ee162415014d85b5 |
| Evidence | User request, mobile-work context và exact Flutter source |
| Business source | Chưa có BD/BRD mobile; unresolved decisions là OPEN QUESTION |

## Mục đích và boundary

- **Mục đích:** Cung cấp UI shell cho liên kết doanh nghiệp - nhà trường.
- **Actor:** Doanh nghiệp
- **Trong phạm vi:** View/controller/helper/model trace và side effect đã có evidence.
- **Ngoài phạm vi:** API/schema mới, migration, runtime implementation và production behavior chưa được chốt.
- **Boundary:** TrangChu → LienKetScreen → local UI; external integration chưa source-backed.

## Current data flow

| Nhóm | Evidence |
|---|---|
| Data | UI state only; chưa có backend contract/persistence. |
| Integration | `lib/views/trang_chu/tien_ich/Lien_ket_nha_truong/lien_ket_nha_truong.dart`; `lib/views/trang_chu/main/trang_chu.dart` |
| Side effect | TrangChu → LienKetScreen → local UI; external integration chưa source-backed. |
| Security | Không ghi credential literal; direct client data access là prototype boundary. |

## WMB_SCHOOL_LINK-BR01 — Current source rule

Không claim đã liên kết nhà trường vì source chỉ có UI surface.

- Cách kiểm tra: đối chiếu exact source paths trong [Import_File.md](Import_File.md).
- Status: CURRENT_SOURCE_RULE, chưa phải approved business requirement.

## Open questions

- **OPEN QUESTION:** Cần owner chốt partner model, authorization, approval và integration contract.
- BA/PO phải chốt các rule chưa có evidence trước khi code feature mới.

## Traceability

| Requirement/evidence | Feature | Rule | Functions | Views | Source | Tests |
|---|---|---|---|---|---|---|
| User request + current source inventory | WMB_SCHOOL_LINK-F01 | WMB_SCHOOL_LINK-BR01 | WMB_SCHOOL_LINK-FN01..FN01 | WMB_SCHOOL_LINK-V01..V01 | [Import_File.md](Import_File.md) | WMB_SCHOOL_LINK-TC01..TC01 |
