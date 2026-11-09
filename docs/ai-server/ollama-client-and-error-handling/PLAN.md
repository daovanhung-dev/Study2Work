# PLAN: Vòng đời HTTP client và xử lý lỗi Ollama của AI Server

Mã tác vụ: `2026-11-09-ai-server-ollama-client-and-error-handling`

Trạng thái: `APPROVED`

SPEC nguồn: [SPEC.md](SPEC.md), SHA256 hiện hành `01F1A9133C3732A71A826AFDC42E1D0BB3CBB2DFFBD356AB94962454730B5AD9` (approval giữ nguyên sau chỉnh định dạng Markdown).

## Căn cứ và phạm vi

- Developer đã duyệt nội dung SPEC tiếng Việt SHA256 `FF2FC393212178F7E55641857E0DEF2628768191AAA72C5CB19141E0F441E635` ngày 2026-11-09. Sau đó chỉ bổ sung metadata phê duyệt, sổ trạng thái và chỉnh định dạng Markdown; worklog ghi rõ các revision và lý do giữ approval.
- Source đang được lập plan: Git `fc980cd3` trên nhánh `ducna_dev/featrure_AI_sever`. Route hiện gọi `ai_service.generate`, service tạo `AsyncClient` cho mỗi request, chưa có test AI Server.
- Chỉ sửa `server-ai`: giữ route và JSON thành công, không streaming hoặc sửa FE/Ollama server. Không thêm DB, xác thực, rate limit, retry hay hàng chờ nhận request.
- `apps/ai-server/uv.lock` đang là file chưa được theo dõi và nằm ngoài phạm vi; không sửa, stage hoặc dọn file này.

## Liên kết yêu cầu và bước thực hiện

| Bước | Yêu cầu SPEC | File/hàm dự kiến | Việc thực hiện và ảnh hưởng |
|---|---|---|---|
| P-01 | REQ-02, REQ-04 | `app/service/ai/ollama_service.py:OllamaService.__init__`, method mở/đóng client, `_request`; `app/main.py` lifespan | Quản lý một `httpx.AsyncClient` cho singleton `ai_service` trong mỗi tiến trình. Tạo khi ứng dụng khởi động, dùng lại cho các method adapter, đóng khi dừng; khai báo `httpx.Limits(max_connections=100)` và `httpx.Timeout(self.timeout, pool=5.0)`. Không tạo thêm client khi pool bận. Caller trực tiếp phải gọi `start()` và `close()` tường minh theo `PLAN-D01` B. |
| P-02 | REQ-03 | `app/module/chat/model.py:ChatLogRequest` | Dùng kiểu chuỗi nghiêm ngặt và giới hạn tối đa 8.000 ký tự; validator chỉ dùng `strip()` để phát hiện chuỗi toàn khoảng trắng, không sửa nội dung hợp lệ. FastAPI tiếp tục tạo HTTP 422 mặc định trước khi gọi Ollama. |
| P-03 | REQ-04, REQ-05 | `app/service/ai/ollama_service.py:_request`, `generate`; `app/service/ai/__init__.py` | Phân loại `PoolTimeout` trước các timeout khác thành lỗi `AI_BUSY`; lỗi thiết lập/duy trì kết nối thành `OLLAMA_UNAVAILABLE`; timeout sau khi lấy kết nối thành `OLLAMA_TIMEOUT`; HTTP/JSON/schema phản hồi Ollama sai thành `OLLAMA_BAD_RESPONSE`. Không đưa body thô của Ollama vào exception công khai hoặc log. Kiểm tra `response` của `/api/generate` phải là chuỗi. Export exception mới nếu được tạo. |
| P-04 | REQ-05 | `app/main.py` exception handlers | Ánh xạ lỗi adapter thành HTTP 503/504/502 và JSON `{error:{code,message}}` đúng SPEC. Giữ nguyên handler HTTP 422 mặc định và JSON thành công; không đăng ký các file `app/core` đang `UNWIRED`. |
| P-05 | REQ-01 đến REQ-05 | `apps/ai-server/tests/test_ollama_service.py`, `tests/test_chat_api.py` | Viết test bằng `unittest` chuẩn của Python, `httpx.MockTransport`, `fastapi.testclient.TestClient` và mock có kiểm soát; không thêm dependency test hoặc thay `uv.lock`. Bao phủ test case bên dưới, gồm caller API, adapter và vòng đời ứng dụng. |
| P-06 | REQ-01 đến REQ-05 | `apps/ai-server/README.md`, `app/service/ai/README.md`, `.agents/server-ai/architecture.md`, `apis/chat.md`, `modules/chat.md`, `services/ollama.md`, `tests.md`; worklog | Cập nhật đúng hành vi đã triển khai. README service hiện có ví dụ gọi trực tiếp `ai_service.generate/chat/health_check`; ghi rõ điểm mở, tái sử dụng và đóng client theo phương án `PLAN-D01` được chọn. Không mở rộng context của scope khác. |
| P-07 | REQ-01 đến REQ-05 | Test, diff và context validator | Chạy test tập trung, kiểm tra import/route và diff, đối chiếu từng TC với code; chạy context validator và tách lỗi nền DB Admin khỏi lỗi do task này. Trình kết quả code/test để developer duyệt trước bàn giao. |

### Chi tiết vòng đời và lựa chọn còn mở cho service dùng trực tiếp

`ai_service` hiện là singleton được import bởi `view.py`; giữ đối tượng này để không thay caller. Trong **cả A và B**, FastAPI lifespan tạo một client lúc `ai-server` khởi động, các request cùng dùng client đó, và lifespan đóng client khi tiến trình dừng, kể cả sau lỗi trong giai đoạn phục vụ. Việc người dùng đóng trình duyệt không đóng client. `PLAN-D01` chỉ quyết định cách dùng một `OllamaService` **trực tiếp ngoài FastAPI**, như README service đang minh họa.

**A — Mở ở lần gọi đầu.** Constructor chưa mở client. Lần đầu gọi `generate`, `chat` hoặc `health_check` sẽ tạo một client cho instance; các lần gọi sau, kể cả hai lời gọi đồng thời, dùng lại client đó. Service không thể biết caller đã dùng xong sau request nào, nên **caller vẫn phải gọi `close()`**, tốt nhất trong `finally`. Nếu caller quên đóng, kết nối có thể tồn tại tới khi tiến trình kết thúc. Sau khi đã đóng, lần gọi tiếp theo có thể tạo client mới. Cách này giữ cú pháp gọi method hiện tại nhưng che thời điểm mở client.

```python
service = OllamaService()
try:
    first = await service.generate(prompt="Câu hỏi 1")   # Mở client
    second = await service.generate(prompt="Câu hỏi 2")  # Dùng lại client
finally:
    await service.close()  # Caller quyết định khi đã dùng xong
```

**B — Mở và đóng tường minh (đề xuất sau khi làm rõ vòng đời).** Constructor chưa mở client. Caller gọi `start()` trước lời gọi đầu; mọi lời gọi trong cùng phạm vi dùng lại client; `close()` nằm trong `finally` để vẫn chạy khi có lỗi. Nếu quên `start()`, service báo lỗi vòng đời rõ ràng thay vì tự mở ngầm. Sau khi đóng, caller phải gọi `start()` lại trước khi gửi request mới. README và caller trực tiếp phải đổi cách gọi; các request qua FastAPI không đổi.

```python
service = OllamaService()
await service.start()  # Caller chỉ rõ điểm bắt đầu
try:
    first = await service.generate(prompt="Câu hỏi 1")
    second = await service.generate(prompt="Câu hỏi 2")  # Dùng lại client
finally:
    await service.close()  # Caller chỉ rõ điểm kết thúc
```

Hai ví dụ là giao diện **dự kiến** trong plan, chưa phải code hiện có. Với cả hai cách, không đóng client sau từng request và không mở thêm client khi pool đầy. B được đề xuất vì phạm vi sử dụng và trách nhiệm đóng nhìn thấy ngay trong caller; A ít thay đổi cú pháp hơn.

Nếu khi triển khai thấy nhánh dùng trực tiếp buộc phải thay đổi contract public của service, dừng phần đó và trình sửa đổi PLAN để duyệt; không âm thầm bỏ ví dụ hoặc tạo client tạm cho từng request.

## Ma trận test case

Các TC dưới đây đều là **kế hoạch**, chưa chạy. Đường dẫn test dự kiến tương đối với `apps/ai-server/`.

| TC | Nguồn → REQ → bước | Thiết lập / đầu vào và thao tác | Kết quả mong đợi | Lớp và file |
|---|---|---|---|---|
| TC-01 | Developer mục 1 → REQ-01 → P-03, P-04, P-05 | Mock Ollama trả `response` hợp lệ; POST prompt có định dạng code | HTTP 200, chỉ `{response: ...}`; upstream nhận nguyên prompt, model đã cấu hình và `stream: false` | API: `tests/test_chat_api.py` |
| TC-02 | Developer mục 2 → REQ-02 → P-01, P-05 | Mở rồi đóng lifespan của app | Một client được tạo với `max_connections=100`, đóng khi shutdown; import app đơn thuần không tạo client hoạt động | Lifespan: `tests/test_chat_api.py` |
| TC-03 | Developer mục 2 → REQ-02 → P-01, P-05 | Gửi hai lời gọi adapter đồng thời qua mock transport | Cùng một client được dùng cho cả hai; kết quả của từng request không trộn lẫn | Service: `tests/test_ollama_service.py` |
| TC-04 | Developer mục 2 → REQ-02 → P-01, P-05 | Gọi `chat`, `list_models`, `health_check` với mock transport theo vòng đời `PLAN-D01` B | Chưa `start()` thì báo lỗi vòng đời; sau `start()` các method dùng lại client; `close()` chạy được cả khi lời gọi lỗi; không tạo client cho từng call | Service: `tests/test_ollama_service.py` |
| TC-05 | Developer mục 3 → REQ-03 → P-02, P-05 | POST thiếu prompt, prompt không phải chuỗi, `""` hoặc chỉ khoảng trắng | HTTP 422 dạng FastAPI hiện tại; không gửi request tới Ollama | API: `tests/test_chat_api.py` |
| TC-06 | Developer mục 3 → REQ-03 → P-02, P-05 | POST prompt dài 8.001 ký tự | HTTP 422; không gọi Ollama | API: `tests/test_chat_api.py` |
| TC-07 | Developer mục 3 → REQ-03 → P-02, P-05 | POST prompt không rỗng dài đúng 8.000 ký tự, có khoảng trắng có ý nghĩa | Được chấp nhận và gửi nguyên văn tới Ollama | API: `tests/test_chat_api.py` |
| TC-08 | Developer mục 2 → REQ-04 → P-01, P-03, P-05 | Kiểm tra cấu hình client và gây `httpx.PoolTimeout` có kiểm soát | Pool timeout là 5 giây; API trả 503 `AI_BUSY`; không tạo client bổ sung | Service + API: hai file test |
| TC-09 | Developer mục 2 → REQ-04 → P-01, P-05 | Đặt `OLLAMA_TIMEOUT` trong test rồi tạo service | Connect/read/write dùng giá trị cấu hình; pool vẫn 5 giây; không diễn giải là tổng deadline | Service: `tests/test_ollama_service.py` |
| TC-10 | Developer mục 3 → REQ-05 → P-03, P-04, P-05 | Mock lỗi kết nối, timeout lúc connect và đứt kết nối | HTTP 503, code `OLLAMA_UNAVAILABLE`, thông báo an toàn | Service + API: hai file test |
| TC-11 | Developer mục 3 → REQ-05 → P-03, P-04, P-05 | Mock timeout đọc/ghi sau khi có kết nối | HTTP 504, code `OLLAMA_TIMEOUT`, thông báo an toàn | Service + API: hai file test |
| TC-12 | Developer mục 3 → REQ-05 → P-03, P-04, P-05 | Mock upstream HTTP lỗi, JSON hỏng, JSON không phải object, thiếu hoặc sai kiểu `response` | HTTP 502, code `OLLAMA_BAD_RESPONSE`; không trả body thô | Service + API: hai file test |
| TC-13 | Developer mục 3 → REQ-05 → P-03, P-04, P-05 | Dùng prompt và upstream body có chuỗi nhạy cảm giả trong các nhánh lỗi | JSON trả về không chứa prompt, upstream body, URL nội bộ hoặc stack trace; log không chứa prompt hoặc upstream body | Service + API: hai file test |
| TC-14 | Developer mục 1 → REQ-01 → P-04, P-05 | GET `/` và POST chat hợp lệ sau khi đăng ký handler | Route gốc và chat vẫn hoạt động; handler mới không đổi phản hồi thành công | API: `tests/test_chat_api.py` |

Không có nhánh xác thực để test vì route hiện không có auth và SPEC không thêm auth. TC-03 kiểm tra chia sẻ client ở ứng dụng, không chứng minh Ollama thật xử lý hai lượt suy luận đồng thời. Test pool timeout dùng exception giả lập để không phải chờ 5 giây thực.

## Thứ tự thực hiện và kiểm tra

1. Trước khi sửa từng hàm, đọc lại caller/callee và source mới nhất. Thực hiện P-01, rồi P-02, P-03, P-04; giữ route `v1.py` và view nếu không cần đổi để đáp ứng SPEC.
2. Thực hiện P-05, chạy `& .venv/Scripts/python.exe -m unittest discover -s tests -v` từ thư mục `apps/ai-server` trong PowerShell. Nếu test path hoặc môi trường khác thực tế, ghi rõ lệnh đã chạy và lý do điều chỉnh.
3. Thực hiện P-06 sau khi code ổn định; chạy `node scripts/validate-agent-context.mjs` vì context scope thay đổi. Đối chiếu kết quả với lỗi nền DB Admin đã biết, không coi lỗi nền là test ứng dụng thất bại.
4. Chạy `git diff --check`, rà tất cả file sửa và đối chiếu REQ → P → TC → code/test. Báo TC `PASS`, `FAIL`, `NOT_RUN` hoặc `BLOCKED` theo kết quả thực tế. Chỉ sau đó gửi diff và kết quả để developer duyệt.

## Tương thích, rủi ro và hoàn tác

- Không có migration hoặc thay đổi database. Đường success vẫn tương thích về path và JSON; HTTP 422 sẽ được áp dụng cho các prompt trước đây được nhận nhưng rỗng/quá dài. Các lỗi Ollama trước đây chưa được ánh xạ nay có HTTP/JSON xác định; consumer bên ngoài chưa được xác minh.
- Rủi ro chính: vòng đời client khi service được gọi ngoài FastAPI, phân loại `PoolTimeout` trước timeout khác, và vô tình ghi prompt/body thô vào log. TC-02 đến TC-04 và TC-08 đến TC-13 nhắm đúng các rủi ro này.
- `max_connections=100` giới hạn kết nối ra Ollama cho mỗi tiến trình, không bảo đảm throughput. Không điều chỉnh `OLLAMA_NUM_PARALLEL` hay `OLLAMA_MAX_QUEUE`; không suy kết luận hiệu năng từ mock test.
- Nếu cần hoàn tác trước triển khai, đảo các thay đổi trong AI Server, tài liệu và context thuộc task này; giữ nguyên các file không liên quan trong working tree, đặc biệt `uv.lock` chưa được theo dõi.

## Sổ quyết định, vấn đề và xác minh

| Mã | Hiện trạng và bằng chứng | Trạng thái; chặn bước tiếp? | Phương án và hệ quả |
|---|---|---|---|
| PLAN-D01 | `app/service/ai/README.md` minh họa gọi `ai_service.generate/chat/health_check` trực tiếp; phần trên mô tả chính xác điểm mở, tái sử dụng và đóng của A/B. | `DECIDED`; không chặn | Developer chọn **B**: caller gọi `start()` trước và `close()` trong `finally`; thiếu `start()` báo lỗi vòng đời, sau `close()` muốn dùng tiếp phải `start()` lại. A chỉ giữ làm phương án đã xem xét. |
| PLAN-V01 | Chưa có phép đo Ollama trên máy host sẽ triển khai; mock test chỉ xác minh ứng dụng. Liên kết `SPEC-V01`. | `DEFERRED`; không chặn code cục bộ | Developer chọn **A**: chạy test mock ở bước code; đo tải Ollama trên host khi triển khai. Không diễn giải mock test thành kết luận hiệu năng. |
| PLAN-V02 | Tìm kiếm tập trung chưa thấy FE gọi route này; consumer bên ngoài chưa xác minh. | `NOT_FOUND`; không chặn theo scope đã duyệt | Giữ path và JSON thành công như REQ-01; nếu cần khảo sát consumer ngoài scope, mở quyết định scope mới trước khi sửa phần đó. |
| PLAN-V03 | Validator context toàn repo hiện lỗi do thiếu cây DB Admin; chưa có lỗi nêu tên task này. | `BASELINE_FAILURE`; không chặn nếu kiểm tra task không phát sinh lỗi mới | Khi code xong, chạy lại và tách lỗi nền khỏi lỗi của task; không sửa DB Admin trong phạm vi này. |
| PLAN-A01 | Developer đã chọn `PLAN-D01` B và `PLAN-V01` A, rồi yêu cầu “thực hiện tiếp đi” ngày 2026-11-09. | `APPROVED`; cho phép code/test | Lựa chọn B/A được áp dụng trong revision này. Nếu đổi hành vi hoặc contract, cập nhật artifact liên quan và xin developer duyệt lại. |

Những mục đã được duyệt trong SPEC không được hỏi lại khi yêu cầu và revision
liên quan không đổi. Nếu developer nhập phương án riêng làm đổi hành vi hoặc
contract, đối chiếu lại SPEC trước khi tiếp tục.

## Phê duyệt

- PLAN: `APPROVED` theo lựa chọn `PLAN-D01` B, `PLAN-V01` A và chỉ dẫn tiếp tục triển khai của developer ngày 2026-11-09. Revision này chỉ chốt các lựa chọn đã trình, không đổi yêu cầu SPEC.
- Nếu implementation cần đổi hành vi hoặc contract, cập nhật artifact liên quan và xin developer duyệt lại.
