# OPEN_QUESTIONS

## Q-13-01 — Image transport và encoding

**Bằng chứng**

- `list_api.md`: `body{image:string!}`.
- AC-11 diagram: validate MIME/size trước khi lưu.

**Vấn đề**

- Chưa có source xác nhận media type, encoding, data URI/base64/URL, MIME allowlist hoặc size limit.

**Ảnh hưởng**

- Request parser, validation, Object Storage payload và 422 conditions.

**Quyết định tạm thời**

- Giữ `image` là `string`.
- Ghi các policy còn thiếu là `TBD`/`SOURCE_REQUIRED`.
- Không chuyển contract sang multipart.

## Q-13-02 — Object Storage mapping

**Bằng chứng**

- AC-11 diagram chỉ ghi `Object Storage lưu avatar`.

**Vấn đề**

- Chưa có adapter/interface, object key namespace, output URL/asset field, timeout, retry hoặc provider error mapping.

**Ảnh hưởng**

- Data Mapping step `3`, response `data.avatar_url`, security và 500 behavior.

**Quyết định tạm thời**

- Không tự tạo storage key hoặc URL rule.
- Ghi external operation là `SOURCE_REQUIRED`.

## Q-13-03 — UserProfile response source

**Bằng chứng**

- `list_api.md`: response là `ApiEnvelope<UserProfile>`.
- AC-11: API #13 upload avatar, sau đó API #14 cập nhật profile.

**Vấn đề**

- Flow upload-only không có profile reload hoặc DB update được phép để tạo đầy đủ `UserProfile`.

**Ảnh hưởng**

- Response Source Matrix và khả năng implementation của HTTP 201 response.

**Quyết định tạm thời**

- Giữ nguyên response contract.
- Đánh dấu profile fields chưa có source là `SOURCE_REQUIRED`.
- Không tự gọi API #4, không tự gọi API #14 và không tự update `users.avatar_url`.

## Q-13-04 — External side-effect cleanup và idempotency

**Bằng chứng**

- API #13 có Object Storage side effect.
- Không có transaction hoặc cleanup rule trong contract/diagram.

**Vấn đề**

- Chưa biết xử lý object đã upload nếu response mapping thất bại, request retry hoặc client gửi lại cùng avatar.

**Ảnh hưởng**

- Orphan object, duplicate asset, retry semantics và observability.

**Quyết định tạm thời**

- Không tự thêm retry, cleanup, deduplication hoặc idempotency key.
- Giữ API ở `Draft — Needs Confirmation`.
