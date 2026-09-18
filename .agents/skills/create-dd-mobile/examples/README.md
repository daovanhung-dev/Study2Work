# 10 DD Examples

Đây là 10 snapshot DD đầy đủ độc lập để học cách áp dụng template. Mỗi thư mục
được sao chép từ DD canonical hiện hành trong `docs/DD/`; các file bổ sung như
Implementation Delta được giữ lại nếu có.

| # | Snapshot | Canonical source | Điều nên học |
|---:|---|---|---|
| 1 | [ONBOARDING_PROFILE](01-onboarding_profile/) | `docs/DD/onboarding_profile/` | Multi-step flow, profile ownership |
| 2 | [PERSONAL_SCHEDULE_AI](02-personal_schedule_ai/) | `docs/DD/personal_schedule_ai/` | AI generation, quota, idempotency |
| 3 | [DASHBOARD_SCHEDULE](03-dashboard_schedule/) | `docs/DD/dashboard_schedule/` | Schedule state, proof, reward integration |
| 4 | [AI_CHAT](04-ai_chat/) | `docs/DD/ai_chat/` | Access gate, quota, voice, verification boundary |
| 5 | [SCHEDULE_NOTIFICATIONS](05-schedule_notifications/) | `docs/DD/schedule_notifications/` | Notification lifecycle and deep-link action |
| 6 | [FAMILYPLUS](06-familyplus/) | `docs/DD/familyplus/` | Subject access, member limit, RLS boundary |
| 7 | [PAYMENT_MEMBERSHIP](07-payment_membership/) | `docs/DD/payment_membership/` | Payment state, manual review, entitlement activation |
| 8 | [SALE_POINTS](08-sale_points/) | `docs/DD/sale_points/` | Ledger, commission, reversal, conversion |
| 9 | [ADMIN_OPS](09-admin_operations/) | `docs/DD/admin_operations/` | Role matrix, mutation, audit/RPC contract |
| 10 | [AUDIT_SECURITY](10-audit_security/) | `docs/DD/audit_security/` | Cross-cutting security, audit, privacy |

## Snapshot policy

- Snapshot lifecycle là `Reference`; canonical DD vẫn ở `docs/DD/<module>/`.
- Snapshot được kiểm tra không còn template placeholder.
- Runtime status trong snapshot là historical evidence tại thời điểm copy, không
  phải claim mới về production hoặc sandbox.
- Khi canonical DD thay đổi, snapshot cần được refresh có chủ đích và ghi lại ngày.
