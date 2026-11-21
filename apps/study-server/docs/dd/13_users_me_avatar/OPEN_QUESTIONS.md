# OPEN_QUESTIONS

## Q-13-01 — Image transport và encoding — Resolved

**Bằng chứng**

- `list_api.md`: `body{image:string!}`.
- AC-11 diagram: validate MIME/size trước khi lưu.

**Quyết định đã duyệt**

- JSON body giữ field `image` dạng Data URL Base64.
- Chỉ nhận `image/png`, `image/jpeg` và `image/webp`; signature phải khớp MIME.
- Giới hạn payload là 5 MiB sau giải mã; field ngoài contract bị từ chối.
- Không nhận multipart hoặc URL đầu vào.

## Q-13-02 — Object Storage mapping — Resolved

**Bằng chứng**

- AC-11 diagram chỉ ghi `Object Storage lưu avatar`.

**Quyết định đã duyệt**

- Dùng S3-compatible provider với environment variables được ghi trong `PLAN_RESULT.md`.
- Object key là `avatars/{user_id}`; URL ghép từ public base URL.
- Timeout kết nối 5 giây, đọc 30 giây; một attempt, không retry.
- Provider/configuration failure trả `500 DESIGN_INTERNAL_ERROR` bằng message an toàn.

## Q-13-03 — UserProfile response source — Resolved

**Bằng chứng**

- `list_api.md`: response là `ApiEnvelope<UserProfile>`.
- AC-11: API #13 upload avatar, sau đó API #14 cập nhật profile.

**Quyết định đã duyệt**

- Thêm response schema `AvatarUploadResult` chỉ chứa `avatar_url`.
- Success response là `ApiEnvelope<AvatarUploadResult>`.
- API #13 chỉ upload; API #14 vẫn cập nhật profile.
- API #13 không query hoặc mutation database.

## Q-13-04 — External side-effect cleanup và idempotency — Resolved

**Bằng chứng**

- API #13 có Object Storage side effect.
- Không có transaction hoặc cleanup rule trong contract/diagram.

**Quyết định đã duyệt**

- Upload mới của cùng user ghi đè object tại key cố định.
- Không thêm retry, cleanup riêng, deduplication hoặc idempotency key.
- Không kiểm tra storage/credentials từ xa trong task triển khai.
