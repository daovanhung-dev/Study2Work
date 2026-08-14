# Payment checkpoint

- APIs in checkpoint: 16.
- Status: all DDs remain Draft until missing contract/schema decisions are supplied.
- Source gaps/conflicts: see each Main gap value and root [OPEN_QUESTIONS.md](../OPEN_QUESTIONS.md); no conflict is resolved by this batch.
- Validation: see root [VERIFICATION_REPORT.md](../VERIFICATION_REPORT.md).

| API | Method | Endpoint | Transport | Status | Main gap |
| ---: | --- | --- | --- | --- | --- |
| [API-PAY-001](API-PAY-001_get-api-v1-billing-products/00_Cover.md) | `GET` | `/api/v1/billing/products` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-PAY-002](API-PAY-002_post-api-v1-billing-orders/00_Cover.md) | `POST` | `/api/v1/billing/orders` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-PAY-003](API-PAY-003_get-api-v1-billing-orders-order-id/00_Cover.md) | `GET` | `/api/v1/billing/orders/{orderId}` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-PAY-004](API-PAY-004_post-api-v1-billing-orders-order-id-retry/00_Cover.md) | `POST` | `/api/v1/billing/orders/{orderId}/retry` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-PAY-005](API-PAY-005_get-api-v1-billing-entitlements/00_Cover.md) | `GET` | `/api/v1/billing/entitlements` | `public_http` | `Draft — Needs Confirmation` | OQ-PAY-ENTITLEMENT-HOLD |
| [API-PAY-006](API-PAY-006_post-api-v1-billing-refund-requests/00_Cover.md) | `POST` | `/api/v1/billing/refund-requests` | `public_http` | `Draft — Needs Confirmation` | OQ-PAY-ENTITLEMENT-HOLD |
| [API-PAY-007](API-PAY-007_post-api-v1-admin-refunds-refund-id-approve/00_Cover.md) | `POST` | `/api/v1/admin/refunds/{refundId}/approve` | `public_http` | `Draft — Needs Confirmation` | OQ-PAY-ENTITLEMENT-HOLD |
| [API-PAY-008](API-PAY-008_get-api-v1-admin-payments-reconciliation/00_Cover.md) | `GET` | `/api/v1/admin/payments/reconciliation` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-PAY-009](API-PAY-009_post-api-v1-admin-payments-order-id-reconcile/00_Cover.md) | `POST` | `/api/v1/admin/payments/{orderId}/reconcile` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-PAY-010](API-PAY-010_post-api-v1-enterprises-enterprise-id-promotions/00_Cover.md) | `POST` | `/api/v1/enterprises/{enterpriseId}/promotions` | `public_http` | `Draft — Needs Confirmation` | OQ-PAY-PROMOTION-METRICS |
| [API-PAY-011](API-PAY-011_post-api-v1-me-profile-promotions/00_Cover.md) | `POST` | `/api/v1/me/profile-promotions` | `public_http` | `Draft — Needs Confirmation` | OQ-PAY-PROMOTION-METRICS |
| [API-PAY-012](API-PAY-012_post-api-v1-promotions-promotion-id-impressions/00_Cover.md) | `POST` | `/api/v1/promotions/{promotionId}/impressions` | `public_http` | `Draft — Needs Confirmation` | OQ-PAY-PROMOTION-METRICS |
| [API-PAY-013](API-PAY-013_post-api-v1-promotions-promotion-id-clicks/00_Cover.md) | `POST` | `/api/v1/promotions/{promotionId}/clicks` | `public_http` | `Draft — Needs Confirmation` | OQ-PAY-PROMOTION-METRICS |
| [API-PAY-014](API-PAY-014_post-api-v1-webhooks-vnpay-ipn/00_Cover.md) | `POST` | `/api/v1/webhooks/vnpay/ipn` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-PAY-015](API-PAY-015_post-api-v1-webhooks-momo/00_Cover.md) | `POST` | `/api/v1/webhooks/momo` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-PAY-016](API-PAY-016_get-api-v1-billing-returns-provider/00_Cover.md) | `GET` | `/api/v1/billing/returns/{provider}` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
