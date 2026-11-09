# SPEC: Vòng đời HTTP client và xử lý lỗi Ollama của AI Server

Mã tác vụ: `2026-11-09-ai-server-ollama-client-and-error-handling`

Scope phụ trách: `server-ai`

Trạng thái: `APPROVED`

## Nguồn và quyết định đã duyệt ở bước xác định phạm vi

- Developer cung cấp mô tả tác vụ trong cuộc trò chuyện ngày 2026-11-09; không có BD hoặc DD. Developer duyệt phạm vi và các giá trị đề xuất bằng tin nhắn `approve nhé` ngày 2026-11-09.
- Quyết định đã duyệt: giữ API trả một lần; dùng một `httpx.AsyncClient` chung cho mỗi tiến trình AI Server với `max_connections=100`; giới hạn `prompt` ở 8.000 ký tự; chờ tối đa 5 giây để lấy kết nối từ pool rồi trả HTTP 503 nếu hết thời gian; lỗi Ollama và pool dùng JSON an toàn `{error:{code,message}}`, còn lỗi kiểm tra đầu vào HTTP 422 giữ dạng hiện tại của FastAPI.
- Source đã kiểm tra: Git `fc980cd3` trên nhánh `ducna_dev/featrure_AI_sever`. Các file source AI Server được theo dõi không có thay đổi trong working tree khi bắt đầu; file chưa được theo dõi `apps/ai-server/uv.lock` nằm ngoài tác vụ này.
- Bằng chứng source: `apps/ai-server/app/main.py`, `app/api/v1.py`, `app/module/chat/model.py`, `app/module/chat/view.py`, `app/service/ai/ollama_service.py`, `apps/ai-server/.env.example` và các trang context tương ứng trong `.agents/server-ai/`.

## Phạm vi và ranh giới

- Chỉ sửa đường chạy chat hiện dùng của AI Server, vòng đời adapter Ollama, test tập trung, tài liệu AI Server và context trực tiếp bị ảnh hưởng.
- Giữ `POST /api/v1/chat_log_ai`, trường request `prompt` và JSON thành công `{ "response": "..." }`. Tiếp tục gọi Ollama `/api/generate` với `stream: false`.
- Không sửa FE; không thêm streaming endpoint, database, xác thực, rate limit, hàng chờ nhận request, retry hay cấu hình của Ollama server. Không kích hoạt các file `app/core` được sao chép nhưng chưa nối vào runtime.
- Mỗi request chat hợp lệ tiếp tục tạo một yêu cầu HTTP tới Ollama. Đường chạy này không ghi database.

## Hành vi mong đợi và hiện trạng

| Mục | Mong đợi theo phạm vi đã duyệt | Source hiện tại | Trạng thái |
|---|---|---|---|
| Thành công | Trả một lần `{response: string}` | Route trả `{response: result["answer"]}` | `MATCH / PRESERVE` |
| Streaming | Tắt | Adapter gửi `stream: false` | `MATCH / PRESERVE` |
| HTTP client | Một client cho mỗi tiến trình, tạo lúc ứng dụng khởi động và đóng lúc dừng; pool tối đa 100 kết nối | `_request` tạo và đóng `AsyncClient` ở mỗi lần gọi | `DISCREPANCY` |
| Prompt | Bắt buộc là chuỗi, không rỗng, tối đa 8.000 ký tự | Chỉ yêu cầu `prompt: str` | `DISCREPANCY` |
| Chờ pool | Tối đa 5 giây rồi trả HTTP 503 | Cùng giá trị `OLLAMA_TIMEOUT` đang áp dụng cho các loại timeout của HTTPX | `DISCREPANCY` |
| Lỗi Ollama | Trả phản hồi an toàn với HTTP 503/504/502 | Adapter ném exception riêng nhưng route/main chưa ánh xạ thành lỗi API | `DISCREPANCY` |
| Test | Có test thực thi cho phần thay đổi | Chưa tìm thấy file test AI Server | `NOT_FOUND` |

## Yêu cầu và tiêu chí chấp nhận

### REQ-01: Giữ nguyên contract thành công của chat

Nguồn: Mục 1 trong mô tả của developer và phạm vi đã duyệt.

- AC-01.1: Request hợp lệ tới `POST /api/v1/chat_log_ai` vẫn gửi nguyên văn `prompt` cùng model đã cấu hình đến Ollama `/api/generate` với `stream: false`.
- AC-01.2: Với phản hồi sinh nội dung hợp lệ từ Ollama, API trả HTTP 200 và chỉ có `{ "response": "<answer>" }`.
- AC-01.3: Tác vụ này không đổi FE, database, xác thực, streaming hoặc cấu hình Ollama server.

### REQ-02: Dùng chung HTTP client trong một tiến trình

Nguồn: Mục 2 trong mô tả của developer và quyết định `max_connections=100` đã duyệt.

- AC-02.1: Khi ứng dụng khởi động, tạo một `httpx.AsyncClient` cho tiến trình với `max_connections=100` được khai báo rõ; adapter Ollama dùng client đó cho các lần gọi tiếp theo, gồm `generate`, `chat` và lấy danh sách model.
- AC-02.2: Các request đồng thời có thể dùng chung client; không tạo client mới khi pool đang bận.
- AC-02.3: Khi ứng dụng dừng, đóng client. Vòng đời client không gắn với phiên của một người dùng.
- AC-02.4: Các thông số pool khác giữ mặc định của HTTPX, trừ khi plan được duyệt chỉ ra chi tiết cần thiết cho vòng đời client. Giới hạn pool không bảo đảm Ollama suy luận đồng thời 100 request.

### REQ-03: Kiểm tra prompt của chat

Nguồn: Mục 3 trong mô tả của developer và quyết định giới hạn 8.000 ký tự đã duyệt.

- AC-03.1: `prompt` thiếu, không phải chuỗi, rỗng, chỉ có khoảng trắng hoặc dài hơn 8.000 ký tự bị từ chối bằng phản hồi kiểm tra đầu vào HTTP 422 của FastAPI trước khi gọi Ollama.
- AC-03.2: Chuỗi không rỗng dài đúng 8.000 ký tự được chấp nhận. Chỉ bỏ qua khoảng trắng khi kiểm tra chuỗi có rỗng hay không; nội dung được chấp nhận phải gửi nguyên văn, kể cả khoảng trắng và định dạng code.
- AC-03.3: Giới hạn ký tự chỉ kiểm soát kích thước đầu vào; nó không bảo đảm phù hợp với giới hạn token hoặc context của model.

### REQ-04: Tách thời gian chờ pool khỏi thời gian chờ Ollama

Nguồn: Mục 2 trong mô tả của developer và quyết định chờ pool 5 giây đã duyệt.

- AC-04.1: Request chờ kết nối trống trong HTTPX pool tối đa 5 giây; nếu hết thời gian, API trả HTTP 503 với code `AI_BUSY` và thông báo an toàn.
- AC-04.2: Giá trị mặc định 180 giây của `OLLAMA_TIMEOUT` tiếp tục áp dụng cho các loại timeout HTTPX ngoài pool. Không mô tả nó là thời hạn tuyệt đối cho toàn bộ request.
- AC-04.3: Khi pool đầy, không tạo thêm `AsyncClient` hoặc âm thầm tăng `max_connections`.

### REQ-05: Chuyển lỗi Ollama thành phản hồi API an toàn

Nguồn: Mục 3 trong mô tả của developer và quyết định về HTTP status/JSON lỗi đã duyệt.

| Trường hợp | HTTP | Error code | Thông báo cho người dùng |
|---|---:|---|---|
| Không thiết lập hoặc duy trì được kết nối tới Ollama | 503 | `OLLAMA_UNAVAILABLE` | `Dịch vụ AI tạm thời không khả dụng` |
| Ollama phản hồi quá thời gian sau khi lấy được kết nối | 504 | `OLLAMA_TIMEOUT` | `Dịch vụ AI phản hồi quá lâu` |
| Ollama trả HTTP khác 2xx, JSON không hợp lệ, JSON không phải object, hoặc object sinh nội dung thiếu `response` dạng chuỗi | 502 | `OLLAMA_BAD_RESPONSE` | `Dịch vụ AI trả về phản hồi không hợp lệ` |
| Không lấy được kết nối từ pool trong 5 giây | 503 | `AI_BUSY` | `Dịch vụ AI đang bận, vui lòng thử lại` |

- AC-05.1: Các lỗi trên trả JSON `{ "error": { "code": "<code>", "message": "<thông báo>" } }`, không chứa body thô từ Ollama, prompt, URL nội bộ, stack trace hoặc chuỗi exception.
- AC-05.2: Lỗi kiểm tra request HTTP 422 giữ dạng phản hồi FastAPI hiện tại. JSON thành công không đổi.
- AC-05.3: Log ở server ghi loại lỗi và trạng thái/ngữ cảnh cần thiết; không ghi toàn bộ prompt hoặc body thô từ Ollama.

## Bề mặt bị ảnh hưởng

| Vị trí | Thay đổi trực tiếp | Ảnh hưởng và cách kiểm tra |
|---|---|---|
| `apps/ai-server/app/main.py` | Quản lý client lúc khởi động/dừng ứng dụng và ánh xạ lỗi API | Lệnh chạy Uvicorn phải thực thi lifespan; chỉ import app chưa chứng minh client đã hoạt động. |
| `apps/ai-server/app/service/ai/ollama_service.py` | Dùng client chung, tách timeout pool và phân loại lỗi transport/Ollama | Các method `generate`, `chat`, `list_models`, `health_check` tiếp tục dùng được. |
| `apps/ai-server/app/module/chat/model.py` | Kiểm tra trường `prompt` hiện có | FastAPI chặn đầu vào sai trước khi gọi adapter. |
| `apps/ai-server/app/api/v1.py` và `app/module/chat/view.py` | Giữ route, luồng gọi và phản hồi thành công | Test route kiểm tra tính tương thích và các lỗi mới. |
| `apps/ai-server/README.md`, `.agents/server-ai/*` | Ghi lại hành vi runtime, cấu hình và lỗi thực sự thay đổi | Context và ví dụ phải khớp implementation. |
| FE | Không sửa code; tìm kiếm tập trung chưa thấy client source gọi route AI này | Trạng thái consumer là `NOT_FOUND`, không suy ra không tồn tại consumer bên ngoài. |
| Database | Không thay đổi hoặc sử dụng trong luồng runtime này | Không cần migration hay test database. |

## Giới hạn xác minh

- Plan phải có test tập trung cho vòng đời/tái sử dụng client, hai request đồng thời, ranh giới độ dài prompt, timeout pool, từng nhóm lỗi Ollama, JSON/log an toàn và phản hồi thành công không đổi.
- Test dùng HTTP mock chứng minh hành vi của ứng dụng, không chứng minh Ollama chịu tải thực tế. Việc đo tải trên máy host Ollama khi triển khai là một bước riêng.

## Quyết định còn mở và phê duyệt

| Mã | Hiện trạng và bằng chứng | Trạng thái | Chặn bước tiếp? | Hướng xử lý |
|---|---|---|---|---|
| SPEC-D01 | Developer đã chọn API trả một lần, client chung tối đa 100 kết nối, prompt tối đa 8.000 ký tự, pool chờ 5 giây và cấu trúc lỗi như các REQ ở trên. | `APPROVED` | Không | Không hỏi lại khi yêu cầu này chưa đổi. |
| SPEC-V01 | Source xác nhận đường gọi Ollama; khả năng chịu tải trên máy host khi triển khai chưa được đo. | `NOT_VERIFIED` | Không chặn SPEC | Việc chọn thời điểm xác minh và đo tải thuộc `PLAN-V01` trong PLAN; không coi mock test là số liệu hiệu năng. |
| SPEC-A01 | Developer duyệt nội dung SPEC qua tin nhắn `tôi approve nhé làm bước tiếp theo đii` ngày 2026-11-09. | `APPROVED` | Không | Approval áp dụng cho bản nội dung SHA256 `FF2FC393212178F7E55641857E0DEF2628768191AAA72C5CB19141E0F441E635`; các lần cập nhật metadata sau đó không đổi hành vi. |

Không còn quyết định bắt buộc về yêu cầu hoặc contract ở bước SPEC. Hash của
file sau các cập nhật chỉ mang tính biên tập được ghi trong worklog và PLAN;
nếu thay đổi REQ hoặc AC, cần trình bày lại SPEC để developer duyệt.
