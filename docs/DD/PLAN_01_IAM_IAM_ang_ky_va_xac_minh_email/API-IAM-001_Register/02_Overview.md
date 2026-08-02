---
title: "Overview"
order: 2
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
| --- | --- |
| API ID | `API-IAM-001` |
| Module | `Platform Identity` |
| Method | `POST` |
| Endpoint | `/api/v1/auth/register` |
| Purpose | Nhận email/password/agreement/locale, chống replay và account enumeration, tạo account chờ xác minh cùng credential, verification token và outbox trong Identity DB. |
| Consumer/Actor | `Anonymous guest` |
| Authentication | `Anonymous`; HTTPS bắt buộc |
| Authorization | `N/A — Không yêu cầu role/permission` |
| Basis | `DIRECT` cho method/path/flow chính; `DERIVED` hoặc `SOURCE_REQUIRED` được đánh dấu tại field tương ứng |
| Status | `Draft — Needs Confirmation` |
| Transaction | `Single identity_db transaction` cho domain mutation; hash password/token được chuẩn bị trước transaction; external email delivery chỉ chạy sau COMMIT qua outbox. Boundary của idempotency claim/replay cần xác nhận. |
| Side effects | Phát verification email bất đồng bộ.<br>Tạo outbox cho registration/email delivery; event type/payload chưa được catalog hóa đầy đủ.<br>Ghi security audit đã redact. |

## Sources

- `04_DAC_TA_API.md:L19-L79, L83-L89, L495-L523, L553-L555`.
- `03_THIET_KE_CO_SO_DU_LIEU.md:L19-L40, L97-L132, L217-L240`.
- `02_BIEU_DO_HE_THONG.md:L332-L377, L845-L929, L1719-L1762`.
- `01_TONG_QUAN_DU_AN.md:L338-L345, L648-L659, L704, L757`.
- `05_DAC_TA_MAN_HINH.md:L75`.
- `PLAN_01_IAM_IAM_ang_ky_va_xac_minh_email.md`.

## Tables read

- `idempotency_keys`.
- `user_emails`.

## Tables write

- `idempotency_keys`.
- `users`.
- `user_emails`.
- `password_credentials`.
- `SOURCE_REQUIRED: agreement acceptance table`.
- `email_verification_tokens`.
- `security_audit_events`.
- `outbox_events`.

## Mục chú ý

- API name trong folder là working name DERIVED từ Plan/endpoint; chưa phải canonical display name.
- Các trường hoặc status chưa có contract field-level được ghi `SOURCE_REQUIRED`; không được triển khai như contract Final.
- Consumer UI: `SCR-IAM-001`; UI chỉ dùng để kiểm coverage, không thay đổi API contract.

## Assumptions

- `agreementVersions` được biểu diễn dạng `array<string>` theo wording “agreement versions”; exact schema vẫn SOURCE_REQUIRED.
- `locale` dùng working field string; required/default HTTP chưa được contract xác nhận.
- HTTP success example dùng `202` như placeholder Draft; không phải contract Final.

## Conflicts

- API catalog dùng `platform_users`, `user_agreement_acceptances`, `one_time_tokens`, `identity_outbox_events`, trong khi DB canonical dùng `users`, thiếu agreement table, dùng `email_verification_tokens` và `outbox_events`.
- `EMAIL_ALREADY_REGISTERED` tồn tại trong endpoint row nhưng yêu cầu chống enumeration và sequence yêu cầu generic response; điều kiện phát code chưa nhất quán.
- `identity.user.registered` được endpoint nêu nhưng không có trong event catalog versioned.

## Security note

- Không log raw email, password, raw verification token hoặc idempotency key.
- Password chỉ lưu Argon2id hash; exact Argon2 parameters SOURCE_REQUIRED.
- Email lưu ciphertext và normalized lookup key; rate-limit key dùng email hash, không dùng raw email.
- Raw token chỉ được chuyển tới email delivery path sau COMMIT; không persist raw token.

## Performance note

- Rate limit `3/giờ/email hash`.
- Mutation p95 mục tiêu ≤ 1,5 giây; email delivery không nằm trong synchronous latency.
- Idempotency record giữ 7 ngày cho register theo DB source.

---
## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `Overview`
- Dimension: `A1:BA10`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `4`
- Số vùng merge: `0`

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 1 | `A1` | 【Khái quát】 |  |
| 3 | `B3` | Get thông tin…. |  |
| 5 | `A5` | 【Mục chú ý】 |  |
| 7 | `B7` | Không có |  |

</details>
