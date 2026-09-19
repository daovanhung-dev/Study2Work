# 11 — NanoBio Source Truth và Constraints

## Thứ tự nguồn hiện hành

1. Runtime reachable từ `lib/main.dart` và composed router/provider wiring.
2. SQLite schema/migration, Supabase build/seed, Edge Function và executable config.
3. Package/platform manifests.
4. Executable tests.
5. README, BD, DD, checklist, design, audit và historical worklog.

Code tồn tại nhưng không reachable phải ghi `Source-only`, không mô tả là user
capability đang dùng.

## NanoBio guardrails

- Guest/basic, authenticated access, paid access và Sale/referral là các trục
  độc lập; route presence không chứng minh entitlement.
- Membership, quota, payment, referral, commission và FamilyPlus access phải dựa
  trên trusted backend/Supabase contract, không dựa vào local UI state.
- Supabase schema/RLS/RPC/seed change phải đọc và cập nhật canonical scripts đúng
  workflow; DD không tự thay thế schema evidence.
- UI text dùng tiếng Việt/Nabitone và không lộ database, query, parser, exception,
  stack trace, tier, entitlement, gate, webhook.
- Không đưa secret, token, PII, raw health/payment/webhook payload vào DD.
