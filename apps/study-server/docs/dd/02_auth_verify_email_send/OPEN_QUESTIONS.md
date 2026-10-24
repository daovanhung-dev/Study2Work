# OPEN_QUESTIONS — Study API #02

**Trạng thái:** `Draft — Needs Confirmation`
**Endpoint:** `POST /api/v1/auth/verify-email/send`

## Q-02-01 — Ai sở hữu dispatch và điều kiện bật verification?

**Bằng chứng:** Catalog gọi API #02 là gửi verification “nếu bật”; AC-01 đặt API #02 sau khi tạo tài khoản. Current API #01 chỉ ghi `verification_dispatch_pending` sau commit, không gọi API #02 hoặc provider.

**Ảnh hưởng:** Chưa có đường đi source-backed từ registration sang verification dispatch; chưa rõ feature gate và component sở hữu lời gọi.

**Cần xác nhận:** Chốt điều kiện bật verification và owner/caller của API #02. Nếu gọi sau khi tạo tài khoản, xác định boundary lỗi trước/sau commit và cách tránh tạo account trùng khi retry. Không thêm field vào request hoặc rollback account theo suy đoán.

## Q-02-02 — `202 accepted` có nghĩa là đã xếp hàng hay provider đã nhận?

**Bằng chứng:** AC-01 mô tả log/retry khi delivery thất bại sau acceptance. Current view gọi provider đồng bộ; exception trả `500 DESIGN_INTERNAL_ERROR`; chưa có queue hoặc retry worker.

**Ảnh hưởng:** Chưa xác định `202` biểu thị request đã enqueue, provider đã nhận, hay email đã gửi; retry ownership, số lần retry và idempotency cũng chưa có contract.

**Cần xác nhận:** Chốt acceptance boundary, retry owner/policy, deduplication key và hành vi lỗi trước/sau acceptance. Không ghi retry là current behavior.

## Q-02-03 — Provider, token/link và vòng đời verification

**Bằng chứng:** Source chỉ khai báo `VerificationEmailProvider`; provider mặc định là stub trả `accepted`, không gửi email hoặc tạo token/link. API contract không mô tả token, URL, expiry, template hay provider payload.

**Ảnh hưởng:** Chưa thể chứng minh email verification hoạt động end to end hoặc mô tả token an toàn.

**Cần xác nhận:** Chọn provider thật và contract tích hợp; chốt token generation/storage, link, expiry, email template, delivery callback và secret/logging policy trước khi đặc tả chi tiết.

## Q-02-04 — Có kiểm tra `user_id` tồn tại và email thuộc user đó không?

**Bằng chứng:** API public, không yêu cầu Bearer; current route không resolve DB và view chuyển `user_id`/`email` thẳng tới provider. API #02 DD không có query contract.

**Ảnh hưởng:** Source hiện tại không ràng buộc ID với email hoặc authenticated principal. Điều kiện user không tồn tại và email không khớp chưa được định nghĩa.

**Cần xác nhận:** Chốt trust boundary, existence/ownership check và chống lạm dụng endpoint public (rate limit/abuse control). Không tự thêm DB query, auth requirement, field hoặc error code.

## Q-02-05 — Giá trị được phép của `ActionResult.status` và `reason`

**Bằng chứng:** Catalog chỉ quy định `status:string`, `reason?:string`; current view map `dispatch_result.status` và optional `reason`; default stub trả `status="accepted"`.

**Ảnh hưởng:** Không có enum hoặc semantics được duyệt cho provider status/reason; client không có contract để xử lý các giá trị khác.

**Cần xác nhận:** Phê duyệt allowed status/reason values và quy tắc khi provider không trả reason. Không thêm `operation_id` vì catalog không khai báo.

## Q-02-06 — Chuẩn hóa email và giới hạn `user_id`

**Bằng chứng:** Catalog định nghĩa `email` và `int64` nhưng không nêu trim/case/range policy. Current validator trim/validate email qua shared Pydantic `EmailStr`, yêu cầu raw `user_id` là JSON integer, nhưng module không kiểm tra int64 bounds.

**Ảnh hưởng:** Cách xử lý whitespace/normalization, integer ngoài miền int64 và mapping validation chưa được thống nhất giữa contract, OpenAPI và source.

**Cần xác nhận:** Chốt email canonicalization và miền numeric cho `user_id`; đồng bộ model, route metadata và validation sau khi contract owner duyệt. Không tự chọn giới hạn hoặc thêm policy.

