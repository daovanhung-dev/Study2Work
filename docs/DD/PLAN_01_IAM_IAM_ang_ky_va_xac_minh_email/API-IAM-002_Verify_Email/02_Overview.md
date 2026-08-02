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
| API ID | `API-IAM-002` |
| Module | `Platform Identity` |
| Method | `POST` |
| Endpoint | `/api/v1/auth/verify-email` |
| Purpose | Nhận one-time token, khóa token hash, kiểm purpose/expiry/unused, kích hoạt user/email, tạo session + refresh token, ghi outbox verified và trả access/refresh token. |
| Consumer/Actor | `Anonymous guest` |
| Authentication | `Anonymous`; HTTPS bắt buộc |
| Authorization | `N/A — Không yêu cầu role/permission` |
| Basis | `DIRECT` cho method/path/flow chính; `DERIVED` hoặc `SOURCE_REQUIRED` được đánh dấu tại field tương ứng |
| Status | `Draft — Needs Confirmation` |
| Transaction | `Single identity_db transaction` khóa token row và cập nhật account/token/session/refresh/outbox atomically; ký access token sau khi dữ liệu session đã được tạo trong transaction hoặc ngay sau COMMIT theo implementation contract SOURCE_REQUIRED. |
| Side effects | Phát `identity.user.verified.v1` bất đồng bộ tới Study/Work.<br>Tạo access token ES256 và opaque rotating refresh token.<br>Không gửi email đồng bộ trong transaction. |

## Sources

- `04_DAC_TA_API.md:L19-L79, L88, L450-L475, L495-L523, L553-L555`.
- `03_THIET_KE_CO_SO_DU_LIEU.md:L97-L132, L164-L178, L217-L240`.
- `02_BIEU_DO_HE_THONG.md:L332-L377, L845-L929, L1719-L1777`.
- `01_TONG_QUAN_DU_AN.md:L338-L345, L648-L659, L704, L757`.
- `05_DAC_TA_MAN_HINH.md:L76`.
- `PLAN_01_IAM_IAM_ang_ky_va_xac_minh_email.md`.

## Tables read

- `idempotency_keys`.
- `email_verification_tokens`.
- `users`.
- `user_emails`.

## Tables write

- `idempotency_keys`.
- `email_verification_tokens`.
- `users`.
- `user_emails`.
- `auth_sessions`.
- `refresh_tokens`.
- `outbox_events`.

## Mục chú ý

- API name trong folder là working name DERIVED từ Plan/endpoint; chưa phải canonical display name.
- Các trường hoặc status chưa có contract field-level được ghi `SOURCE_REQUIRED`; không được triển khai như contract Final.
- Consumer UI: `SCR-IAM-002`; UI chỉ dùng để kiểm coverage, không thay đổi API contract.

## Assumptions

- Response field names `accessToken`, `refreshToken`, `accountStatus` là DERIVED từ semantic output + camelCase convention; cần confirm.
- HTTP success status/businessCode/message chưa được định nghĩa.
- Session device/IP fields được để null hoặc hash context theo nguồn hiện có; exact client session metadata contract thiếu.

## Conflicts

- API endpoint ghi event `identity.user.verified`, event catalog ghi `identity.user.verified.v1`.
- Class diagram có `authVersion`, nhưng DB `users` không định nghĩa column này; `auth_sessions.session_epoch` required nhưng source value chưa xác định.
- Sequence nói verify trả “Email verified”, endpoint row nói access/refresh token; field-level response vẫn thiếu.

## Security note

- Hash raw token trước lookup; không log/persist raw token.
- Token row phải `SELECT ... FOR UPDATE` và transition một chiều qua security-definer procedure.
- Access token ký ES256 bằng secret manager/KMS; private key không nằm trong response/log.
- Refresh token chỉ persist hash; raw token trả đúng một lần.

## Performance note

- Rate limit `10/phút/IP`.
- Mutation p95 mục tiêu ≤ 1,5 giây.
- Outbox projection p95 ≤ 60 giây trong điều kiện bình thường.

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
