# VERIFICATION_REPORT — Study API #02

**Endpoint:** `POST /api/v1/auth/verify-email/send`
**DD status:** `Draft — Needs Confirmation`
**Source status:** route/module/provider source present; default provider is a non-sending stub.

## Phạm vi và nguồn đã kiểm tra

- [Catalog API #02 và schemas](../../../../../docs/lists/list_api.md).
- [AC-01 index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) và [AC-01 activity diagram](../../diagrams/AC_UNICA/AC_01_GUEST_ACCOUNT.drawio).
- Current route, API #02 model/validator/view, email provider, response/middleware context và focused test source.
- Tám sheet DD hiện có và API #01 connected `OPEN_QUESTIONS.md`/`VERIFICATION_REPORT.md`.
- Registered `createDD-markdown` template và Study Markdown-only workflow.

## Kiểm tra package

| Kiểm tra | Kết quả | Trạng thái |
|---|---|---|
| File manifest | Chính xác 11 Markdown files: 8 sheet + 3 report chuẩn; không có file ZIP. | PASS |
| Front matter/template appendix | 8/8 sheet có front matter; appendix khớp registered template 8/8. Template fingerprint: `3dc7fd2242dd1ed1bd9faba50aadad913a31b97ebf1392d6144bb905c5208137`. | PASS |
| Catalog contract | Public POST, body `user_id:int64!`/`email:email!`, `ApiEnvelope<ActionResult>`, HTTP 202 và lỗi 422/500 giữ nguyên. | VERIFIED_STATIC_ONLY |
| JSON examples | 4/4 JSON blocks parse hợp lệ. | PASS |
| Local links/anchors | 42 link nội bộ/path/anchor đã resolve; gồm link sang API #01 reports và current source. | PASS |
| Markdown tables | 31 bảng; 370 dòng table được kiểm tra, độ rộng cột nhất quán. | PASS |
| Fences/whitespace/newlines | Code fences cân bằng; không trailing whitespace; mọi file có final newline. | PASS |
| Fingerprint output | SHA-256 trên 8 sheet + `PLAN_RESULT.md` + `OPEN_QUESTIONS.md` theo quy ước basename/NUL/bytes/NUL: `a4dd09da6e992fde1f0741e7889bcaf07ffda09cabacf4b7fc3ebd24781ca29a`. | PASS |
| `git diff --check` | Không có diagnostics. | PASS |
| Application tests/runtime | Không chạy trong task tài liệu. Test source được đọc. | NOT_RUN |

## Expected behavior và current-source boundary

AC-01 mô tả registration gọi API #02 khi verification được bật, provider gửi verification, và delivery failure được log/retry sau acceptance. Current API #01 chỉ log `verification_dispatch_pending`; không invoke API #02/provider. Current API #02 route là public và không cần DB; validator kiểm tra request, view gọi provider đồng bộ, map exception thành `500 DESIGN_INTERNAL_ERROR`, và trả `202 DESIGN_OPERATION_ACCEPTED` khi provider trả kết quả. Provider mặc định trả `accepted` nhưng không gửi email hoặc tạo token/link; chưa có retry worker. Đây là `DISCREPANCY`; không sửa contract hoặc xem source stub là email delivery thực.

AC-01 connected group review theo API #01: flow design có bước #01 → #02 → Email Provider. Current source chưa thực hiện điểm nối giữa hai API; API #02 chỉ được gọi độc lập qua route nếu caller gửi request. Không có account creation retry hoặc email delivery acceptance nào được chứng minh end to end.

## Source trace

```text
POST /api/v1/auth/verify-email/send -> VerifyEmailSendRequest/raw JSON -> validate integer and normalized email -> synchronous VerificationEmailProvider.dispatch -> 500 on exception or 202 envelope with status/optional reason -> no DB operation -> focused test source (not run)
```

## Câu hỏi và giới hạn

- Feature gate/dispatch owner, acceptance boundary, retry/deduplication policy, provider integration, token/link lifecycle, user-email binding, public abuse controls, validation range/normalization và `ActionResult.status/reason` cần được chốt; xem [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).
- Không chạy application tests, không gọi provider thật, không kiểm tra live database, deployment hoặc email delivery.
- Inventory sau khi hoàn tất API #02 package: 103 API folders/core DDs; 93 full 11-file packages; #03–#12 còn 10 package thiếu reports. Source route-plus-matching-view vẫn là 12/103 (#01–#09, #12–#14); 91 chưa có cặp source.

