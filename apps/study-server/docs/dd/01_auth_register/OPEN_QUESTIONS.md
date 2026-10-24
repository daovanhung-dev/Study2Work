# OPEN_QUESTIONS — Study API #01

**Trạng thái:** `Draft — Needs Confirmation`
**Endpoint:** `POST /api/v1/auth/register`

## Q-01-01 — Ai và khi nào dispatch API #02?

**Bằng chứng:** Catalog gọi API #02 là gửi verification “nếu bật”; AC-01 vẽ bước gọi `POST /api/v1/auth/verify-email/send` sau khi tạo user và ghi log/retry khi provider lỗi. Current API #01 sau commit chỉ log `verification_dispatch_pending`; không gọi API #02/provider. API #02 current view gọi provider đồng bộ; exception trả 500, không có retry worker; default provider chỉ trả `accepted` mà không gửi email thật.

**Ảnh hưởng:** Tài khoản được tạo nhưng flow xác thực được vẽ trong AC-01 không chạy từ API #01 hiện tại. Không rõ feature condition, nơi sở hữu lần gọi, hay retry/monitoring. API #02 hiện xử lý provider exception đồng bộ thành HTTP 500, khác note retry sau acceptance trong DD/API flow.

**Cần quyết định:** Xác nhận feature enablement và owner của dispatch; nếu API #01 gọi API #02 thì chốt boundary sau commit, lỗi trước/sau acceptance, retry và cách tránh tạo account trùng. Không thêm field vào request hoặc rollback account theo suy đoán.

## Q-01-02 — Hồ sơ mặc định và `UserProfile.bio`

**Bằng chứng:** AC-01 nói tạo user và hồ sơ mặc định; DB ERD/legacy Study chỉ có `users`. Catalog `UserProfile` có `bio?:string`; ERD không có `bio`, và current API #01 `RETURNING` không trả field này.

**Ảnh hưởng:** Không có physical mapping được duyệt cho hồ sơ riêng hoặc `bio`; client không biết field absent/null/omit theo contract hiện tại.

**Cần quyết định:** Chọn model hồ sơ và mapping `bio` trước khi chốt schema/response; không tự tạo table/column hay synthesize giá trị.

## Q-01-03 — Validation policy và chuẩn hóa email

**Bằng chứng:** Catalog yêu cầu `email`, `password`, `full_name` nhưng không nêu min/max/password character policy. AC-01 yêu cầu password policy nhưng không liệt kê rule. Current source trim/validate email tối đa 255; từ chối password chỉ có whitespace; trim `full_name` và giới hạn 1–150. Route OpenAPI metadata khai báo email max 255, password min 1, name 1–150; model chỉ khai báo ba field dạng string.

**Ảnh hưởng:** Chưa biết runtime limits có phải approved contract không; semantics so sánh email sau normalize/case và password whitespace chưa được định nghĩa trong catalog.

**Cần quyết định:** Phê duyệt password min/max/character rules, name length, email trim/case/uniqueness semantics và đồng bộ contract/OpenAPI/validator. Không áp thêm policy dựa trên best practice.

## Q-01-04 — User schema và tính duy nhất trong môi trường triển khai

**Bằng chứng:** Current query/insert và `infra/postgres/study-server/DB.sql` dùng BIGSERIAL `users` với email UNIQUE. V1-PILOT dùng identity/profile model UUID riêng. Live database metadata/migration state chưa được kiểm tra.

**Ảnh hưởng:** Source query và race handling chưa chứng minh relation/constraint đang có trong môi trường triển khai.

**Cần quyết định:** Xác nhận schema/migration được Study runtime dùng, email uniqueness constraint/name và quy tắc case sensitivity trước khi chốt data mapping. Không xem DDL artifact là live schema.

## Q-01-05 — Trạng thái tài khoản mặc định

**Bằng chứng:** AC-01 yêu cầu trạng thái phù hợp nhưng không nêu giá trị; DD/legacy ERD dùng `ACTIVE`; current INSERT bỏ qua `status` và dựa vào DB default. V1-PILOT identity status có `PENDING_EMAIL_VERIFICATION`.

**Ảnh hưởng:** Không thể suy ra account được đăng nhập ngay hay phải chờ verification chỉ từ API #01 source/DDL candidates.

**Cần quyết định:** Chốt trạng thái tạo account cùng với verification policy và schema model; không chọn `ACTIVE` hay pending từ một DDL không xác nhận là live.
