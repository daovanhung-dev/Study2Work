# Tài liệu app/core

Tài liệu này mô tả implementation hiện tại của thư mục
apps/study-server/app/core. Đây là lớp hạ tầng dùng chung cho Study API:
cấu hình, database, security, response envelope, trace ID, middleware và xử lý
exception.

> Tài liệu bám theo source hiện tại. Nếu source thay đổi, source mới là nguồn
> sự thật cuối cùng.

## Mục lục

- [Bức tranh tổng thể](#bức-tranh-tổng-thể)
- [Quy ước sử dụng chung](#quy-ước-sử-dụng-chung)
- [Tra cứu nhanh callable](#tra-cứu-nhanh-callable)
- [config.py — cấu hình](#configpy--cấu-hình)
- [database.py — SQLAlchemy và session](#databasepy--sqlalchemy-và-session)
- [responses.py — response envelope](#responsespy--response-envelope)
- [security.py — password và token](#securitypy--password-và-token)
- [trace.py — Trace ID](#tracepy--trace-id)
- [middleware.py — HTTP middleware](#middlewarepy--http-middleware)
- [exceptions.py — exception handlers](#exceptionspy--exception-handlers)
- [Các flow sử dụng thực tế](#các-flow-sử-dụng-thực-tế)
- [Giới hạn và lưu ý bảo mật](#giới-hạn-và-lưu-ý-bảo-mật)

## Bức tranh tổng thể

### Trách nhiệm từng module

| Module | Trách nhiệm | Điểm vào thường dùng |
|---|---|---|
| app/core/config.py | Đọc, parse và validate environment settings | Settings, get_settings() |
| app/core/database.py | Tạo PostgreSQL engine, session factory và query primitive | get_db, query_one, query_many |
| app/core/responses.py | Tạo success/error envelope thống nhất | success_response, error_response |
| app/core/security.py | Hash password, JWT và opaque refresh token | hash_password, create_access_token |
| app/core/trace.py | Tạo và truyền X-Trace-Id trong request context | get_trace_id, get_current_trace_id |
| app/core/middleware.py | Gắn trace ID vào toàn bộ request lifecycle | TraceIdMiddleware |
| app/core/exceptions.py | Map exception thành response an toàn | các exception handler |

app/core/__init__.py chỉ chứa module docstring, không export thêm function
hay class.

### Request lifecycle

~~~text
Client
  ↓
FastAPI / TraceIdMiddleware
  ├─ validate X-Trace-Id hoặc tạo UUID mới
  ├─ lưu vào request.state và ContextVar
  ↓
Router trong app/api
  ├─ parse request model
  └─ Depends(get_db) → request-scoped Session
  ↓
Module view/use case
  ├─ validate và business rule
  ├─ core.security nếu cần
  ├─ query qua Session
  └─ commit/rollback ở transaction boundary
  ↓
core.responses
  ↓
Response có body.traceId và header X-Trace-Id
~~~

Trong app/main.py, create_app() lắp các thành phần sau:

~~~python
app.add_middleware(TraceIdMiddleware)
app.add_exception_handler(ApiError, api_error_handler)
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
~~~

Khi truyền Settings vào create_app(settings), app sẽ tạo engine/session
factory riêng trong app.state, override get_db và bật CORS theo
settings.cors_origins. Khi không truyền settings, engine mặc định được tạo
lazy qua get_engine() khi code thật sự cần database.

## Quy ước sử dụng chung

- Code mới dùng field Python dạng snake_case; environment alias hiện tại dùng
  được cả chữ hoa (DB_HOST) và tên field (db_host).
- HTTP API nhận database bằng db: Session = Depends(get_db). View sở hữu
  commit() và rollback(); helper query không commit.
- Response mới dùng success_response() và error_response(). Các helper
  success_payload(), error_payload() và ApiResponse chỉ phục vụ tương thích
  code cũ.
- Password mới phải hash bằng Argon2id. Bcrypt chỉ dành cho verify hash legacy.
- Refresh token mới là opaque token; chỉ lưu digest từ
  hash_refresh_token(), không lưu raw token.
- Không log hoặc trả về password, password hash, token, DB credential, raw SQL
  hay stack trace cho client.
- businessCode và HTTP status là hai khái niệm khác nhau: HTTP status mô tả
  protocol, còn businessCode mô tả trạng thái nghiệp vụ/API.

## Tra cứu nhanh callable

Bảng dưới đây bao gồm function, method, validator, property, protocol method và
private helper hiện có trong app/core.

| Module | Callable | Mục đích ngắn |
|---|---|---|
| config | Settings.parse_cors_origins | Parse list hoặc chuỗi CORS |
| config | Settings.validate_db_schema | Chặn schema không an toàn |
| config | Settings.validate_jwt_key_configuration | Kiểm tra key theo JWT algorithm |
| config | Settings.DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD, DB_SCHEMA | Compatibility aliases cho DB |
| config | Settings.JWT_SECRET_KEY, JWT_ALGORITHM, JWT_ACCESS_TOKEN_EXPIRE_MINUTES, JWT_REFRESH_TOKEN_EXPIRE_DAYS, JWT_ISSUER | Compatibility aliases cho JWT |
| config | get_settings | Load và cache Settings |
| config | _LazySettings.__getattr__, __repr__ | Proxy settings lazy |
| database | build_database_url | Tạo PostgreSQL URL an toàn |
| database | build_engine | Tạo SQLAlchemy engine |
| database | build_session_factory | Tạo factory cho Session |
| database | get_engine, get_session_factory | Lazy cached default resources |
| database | SessionLocal | Tạo Session mới cho caller legacy |
| database | get_db_from_factory, get_db | Dependency theo request |
| database | execute_query | Chạy SQL parameterized |
| database | query_one, query_many | Đọc một/nhiều row dạng dict |
| responses | utc_now_iso | Lấy UTC ISO-8601 không microsecond |
| responses | ApiError.__init__ | Tạo controlled exception |
| responses | success_response, error_response | Tạo canonical envelope |
| responses | raise_api_error | Raise ApiError |
| responses | success_payload, error_payload | Compatibility adapters |
| responses | ApiResponse.success_payload, raise_error | Adapter model cũ |
| security | TokenKeyProvider.get_verification_key | Contract lấy key verify JWT |
| security | PasswordHasher.hash, verify | Hash/verify password |
| security | password_algorithm_for_hash | Nhận diện format hash |
| security | needs_password_rehash | Kiểm tra cần nâng cấp hash |
| security | hash_password, verify_password | Wrapper password khuyến nghị |
| security | _settings_secret, _signing_key, _verification_key | Chuẩn bị secret/key |
| security | _create_token | Tạo JWT dùng chung |
| security | create_access_token, create_refresh_token | Tạo access/legacy refresh JWT |
| security | decode_token, decode_access_token, decode_refresh_token | Verify và decode JWT |
| security | generate_refresh_token | Tạo opaque refresh token |
| security | hash_refresh_token, compare_token_hash | Hash và so sánh digest |
| trace | create_trace_id, normalize_trace_id | Tạo/chuẩn hóa UUID trace |
| trace | set_current_trace_id, reset_current_trace_id | Quản lý ContextVar |
| trace | get_current_trace_id, get_trace_id | Đọc trace từ context/request |
| middleware | TraceIdMiddleware.dispatch | Bao request bằng trace context |
| exceptions | _validation_field | Chuyển Pydantic location thành field path |
| exceptions | api_error_handler | Render ApiError |
| exceptions | http_exception_handler | Render HTTP error an toàn |
| exceptions | request_validation_exception_handler | Render lỗi validation |
| exceptions | unhandled_exception_handler | Log lỗi nội bộ và trả 500 an toàn |

### Bảng mục đích và thời điểm sử dụng cho từng callable

| Callable | Dùng để làm gì? | Dùng khi nào? |
|---|---|---|
| Settings | Gom toàn bộ cấu hình có type của API và infrastructure. | Tạo app/runtime hoặc test cần cấu hình riêng. Không tự tạo dict config thay thế nếu đã có Settings. |
| Settings.parse_cors_origins | Chuyển CORS_ORIGINS dạng chuỗi hoặc list thành list đã trim. | Được Pydantic tự gọi khi khởi tạo Settings; không cần gọi trực tiếp trong router. |
| Settings.validate_db_schema | Kiểm tra schema chỉ gồm ký tự an toàn cho search_path. | Được Pydantic tự gọi khi tạo Settings; dùng để phát hiện cấu hình DB sai sớm. |
| Settings.validate_jwt_key_configuration | Đảm bảo HS256 có secret hoặc ES256 có public key. | Được Pydantic tự gọi sau khi parse Settings; dùng để fail-fast khi cấu hình JWT thiếu. |
| Settings.DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD, DB_SCHEMA | Đọc cấu hình DB bằng tên uppercase cũ. | Chỉ khi code legacy còn dùng API uppercase; code mới dùng db_host, db_port... |
| Settings.JWT_SECRET_KEY, JWT_ALGORITHM, JWT_ACCESS_TOKEN_EXPIRE_MINUTES, JWT_REFRESH_TOKEN_EXPIRE_DAYS, JWT_ISSUER | Đọc một số cấu hình JWT bằng tên uppercase cũ. | Chỉ khi tương thích code cũ; code mới dùng field snake_case tương ứng. |
| get_settings | Tạo và cache Settings mặc định của process. | Khi code cần cấu hình mặc định, ví dụ security hoặc default database factory. Không dùng để thay đổi config giữa các request. |
| _LazySettings.__getattr__ | Chuyển attribute của proxy settings sang get_settings(). | Chỉ được gọi gián tiếp khi đọc biến module settings; không gọi trực tiếp trong business code. |
| _LazySettings.__repr__ | Hiển thị proxy là settings (lazy). | Chỉ phục vụ debug/repr; không dùng để lấy giá trị cấu hình. |
| build_database_url | Tạo SQLAlchemy PostgreSQL URL và escape credential đúng cách. | Khi xây engine từ một Settings cụ thể, nhất là test/runtime riêng. |
| build_engine | Tạo engine với pool, pre-ping và search_path. | Khi app/test cần engine từ config tường minh. Không tạo engine mới trong từng request. |
| build_session_factory | Tạo factory sinh Session gắn với một engine. | Khi lắp app instance hoặc test cần session factory riêng. |
| get_engine | Lấy engine mặc định đã lazy-cache. | Khi code dùng cấu hình mặc định và cần connect DB. |
| get_session_factory | Lấy session factory mặc định đã lazy-cache. | Khi viết dependency/default DB flow; test có config riêng nên dùng factory inject. |
| SessionLocal | Sinh một Session mới qua factory mặc định. | Chỉ cho caller legacy hoặc script có tự đóng Session. HTTP view nên dùng Depends(get_db). |
| get_db_from_factory | Yield một Session theo factory và luôn close sau cùng. | Khi FastAPI app/test cần inject factory riêng trong app.state. |
| get_db | FastAPI dependency cung cấp request-scoped Session mặc định. | Dùng trong router với Depends(get_db) cho mọi API cần DB. |
| execute_query | Chạy SQL text với named parameters và trả Result. | Khi cần primitive query/read/write cấp thấp. Caller phải tự commit hoặc rollback. |
| query_one | Chạy SELECT và lấy row đầu tiên thành dict hoặc None. | Khi cần đọc tối đa một bản ghi và view tự xử lý not-found. |
| query_many | Chạy SELECT và lấy toàn bộ row thành list dict. | Khi cần đọc danh sách; không có row trả []. |
| utc_now_iso | Tạo timestamp UTC ISO-8601 hậu tố Z, không microsecond. | Khi cần timestamp theo đúng format API; không dùng để lấy local time. |
| ErrorDetail | Biểu diễn một lỗi có field, code và message. | Khi tạo field error/business error đưa vào error_response hoặc ApiError. |
| ApiError.__init__ | Gắn HTTP status, business code, message, trace, errors và headers vào exception. | Khi cần ném controlled error để global handler render response chuẩn. |
| success_response | Tạo success envelope gồm success, businessCode, message, data, meta, traceId. | Khi endpoint/view trả kết quả thành công. |
| error_response | Tạo canonical error envelope; đưa ErrorDetail vào meta.fieldErrors. | Khi handler hoặc view cần tạo body lỗi chuẩn mà không raise exception. |
| raise_api_error | Tạo rồi raise ApiError trong một lệnh. | Khi business rule thất bại và cần dừng flow ngay trong view/dependency. |
| success_payload | Alias tương thích của success_response. | Chỉ khi caller cũ đang gọi tên này; code mới dùng success_response. |
| error_payload | Tạo error shape cũ với errors ở top-level. | Chỉ khi giữ contract legacy; không dùng cho API mới. |
| ApiResponse.success_payload | Chuyển model response cũ thành canonical success envelope. | Khi module cũ đang giữ dữ liệu trong ApiResponse và cần trả HTTP response. |
| ApiResponse.raise_error | Chuyển ApiResponse cũ thành ApiError rồi raise. | Khi code legacy biểu diễn lỗi bằng ApiResponse. |
| TokenKeyProvider.get_verification_key | Định nghĩa interface lấy verification key theo kid. | Khi tích hợp static key store/JWKS provider vào decode_token; không phải implementation fetch JWKS. |
| PasswordHasher.hash | Hash password bằng Argon2id hoặc Bcrypt theo algorithm chỉ định. | Dùng nội bộ hoặc khi cần hỗ trợ algorithm explicit; password mới nên gọi hash_password. |
| PasswordHasher.verify | Verify password với hash Argon2id/Bcrypt và trả bool an toàn. | Khi cần login/kiểm tra credential; không tự ném lỗi cho password sai. |
| password_algorithm_for_hash | Nhận diện loại hash qua prefix mà không verify. | Khi cần chọn verifier hoặc quyết định migration; không dùng làm bằng chứng password đúng. |
| needs_password_rehash | Kiểm tra hash đã verify có cần nâng cấp Argon2id không. | Sau khi verify password thành công, trước khi lưu hash mới. |
| hash_password | Wrapper luôn hash password mới bằng policy Argon2id chuẩn. | Dùng trong register, đổi password và migration legacy. |
| verify_password | Wrapper verify password, hỗ trợ cả Argon2id và Bcrypt legacy. | Dùng trong login hoặc kiểm tra password hiện tại. |
| _settings_secret | Unwrap SecretStr thành giá trị string hoặc trả None. | Chỉ dùng bên trong security khi thư viện cần secret thật; không gọi từ module nghiệp vụ. |
| _signing_key | Chọn private key ES256 hoặc secret HS256 để ký JWT. | Chỉ được _create_token gọi; không expose hoặc log key. |
| _verification_key | Chọn public/secret key để verify JWT, có thể qua key provider. | Chỉ được decode_token gọi; dùng key_provider khi cần key theo kid. |
| _create_token | Tạo JWT với claim chuẩn, expiration và claim bổ sung. | Chỉ dùng qua create_access_token hoặc legacy create_refresh_token. |
| create_access_token | Tạo JWT access ngắn hạn có type, issuer, audience, roles. | Sau login hoặc khi cấp credential truy cập API. |
| create_refresh_token | Tạo legacy JWT refresh có user subject và không có audience. | Chỉ để tương thích auth hiện tại; flow mới không nên dùng. |
| decode_token | Verify chữ ký và toàn bộ claim/type/subject của JWT. | Khi xây auth dependency cần decoder tổng quát; thường dùng wrapper theo token type. |
| decode_access_token | Decode JWT và bắt buộc type access cùng audience. | Khi xác thực Bearer access token cho API. |
| decode_refresh_token | Decode legacy refresh JWT, bỏ yêu cầu audience nhưng vẫn kiểm tra type refresh. | Chỉ khi xử lý legacy refresh JWT. |
| generate_refresh_token | Tạo raw opaque refresh token ngẫu nhiên không chứa user info. | Khi cấp refresh token mới cho client trước khi hash để lưu. |
| hash_refresh_token | Tạo HMAC-SHA256 digest từ raw refresh token bằng pepper. | Khi lưu token mới hoặc kiểm tra token client gửi; chỉ lưu digest. |
| compare_token_hash | So sánh hai digest bằng constant-time comparison. | Khi đối chiếu digest đã lưu với digest vừa tạo từ token client. |
| create_trace_id | Tạo UUID v4 trace ID mới. | Khi request thiếu hoặc có trace ID không hợp lệ; middleware thường gọi. |
| normalize_trace_id | Kiểm tra và đưa UUID về chuỗi canonical hoặc trả None. | Khi nhận X-Trace-Id từ header/state trước khi tin dùng. |
| set_current_trace_id | Đặt trace ID vào ContextVar và trả token reset. | Khi bắt đầu request context hoặc code async không truyền Request trực tiếp. |
| reset_current_trace_id | Khôi phục ContextVar trước request hiện tại. | Luôn gọi trong finally sau set_current_trace_id. |
| get_current_trace_id | Đọc trace ID từ ContextVar hiện tại. | Khi code/log không có Request trực tiếp nhưng đang ở request context. |
| get_trace_id | Lấy trace ID từ Request state, tạo mới nếu thiếu/sai. | Trong endpoint, response builder hoặc exception handler cần trace ID. |
| TraceIdMiddleware.dispatch | Bao downstream request bằng trace state/context và gắn response header. | Tự động chạy cho mọi request sau khi add_middleware(TraceIdMiddleware). |
| _validation_field | Chuyển Pydantic loc thành tên field như items.0.name. | Chỉ được validation exception handler dùng để map lỗi input. |
| api_error_handler | Chuyển ApiError thành JSONResponse theo status/body/headers của exception. | Đăng ký global cho ApiError trong create_app; không gọi từ view. |
| http_exception_handler | Che detail HTTP arbitrary bằng error envelope an toàn. | Đăng ký global cho HTTPException, đặc biệt 404/405/protocol error. |
| request_validation_exception_handler | Map RequestValidationError thành HTTP 422 và meta.fieldErrors. | Đăng ký global để lỗi body/query/path có cùng response contract. |
| unhandled_exception_handler | Log exception nội bộ có trace ID và trả lỗi generic HTTP 500. | Dùng làm global fallback hoặc khi TraceIdMiddleware bắt lỗi downstream. Không trả raw exception. |

Phần chi tiết bên dưới giải thích thêm chữ ký, dữ liệu vào/ra, side effect,
exception và ví dụ cho từng nhóm callable.


---

## config.py — cấu hình

### Environment và JwtAlgorithm

~~~python
Environment = Literal["local", "test", "staging", "production"]
JwtAlgorithm = Literal["ES256", "HS256"]
~~~

Đây là các type alias dùng để giới hạn giá trị hợp lệ của app_env và
jwt_algorithm. ES256 là mặc định; HS256 chỉ là compatibility mode.

### Settings

~~~python
class Settings(BaseSettings):
    ...
~~~

Settings là Pydantic Settings model dùng chung cho API và infrastructure.
Model đọc file .env ở working directory, không phân biệt hoa thường, bỏ qua
environment key không biết (extra="ignore") và cho phép truyền field bằng cả
tên Python lẫn alias environment.

#### Các field

| Field | Kiểu | Mặc định/điều kiện | Environment alias |
|---|---|---|---|
| app_env | Environment | "local" | APP_ENV, app_env |
| enable_docs | bool | True | ENABLE_DOCS, enable_docs |
| cors_origins | list[str] | [] | CORS_ORIGINS, cors_origins |
| db_host | str | bắt buộc | DB_HOST, db_host |
| db_port | int | 5432, từ 1 đến 65535 | DB_PORT, db_port |
| db_name | str | bắt buộc | DB_NAME, db_name |
| db_user | str | bắt buộc | DB_USER, db_user |
| db_password | SecretStr | bắt buộc | DB_PASSWORD, db_password |
| db_schema | str | "public", dài tối thiểu 1 | DB_SCHEMA, db_schema |
| database_pool_size | int | 5, tối thiểu 1 | DATABASE_POOL_SIZE, database_pool_size |
| database_max_overflow | int | 10, tối thiểu 0 | DATABASE_MAX_OVERFLOW, database_max_overflow |
| redis_url | str hoặc None | None | REDIS_URL, redis_url |
| jwt_secret_key | SecretStr hoặc None | None, nếu có dài tối thiểu 32 | JWT_SECRET_KEY, jwt_secret_key |
| jwt_private_key | SecretStr hoặc None | None | JWT_PRIVATE_KEY, jwt_private_key |
| jwt_public_key | str hoặc None | None | JWT_PUBLIC_KEY, jwt_public_key |
| jwt_algorithm | JwtAlgorithm | "ES256" | JWT_ALGORITHM, jwt_algorithm |
| jwt_access_token_expire_minutes | int | 15, lớn hơn 0 | JWT_ACCESS_TOKEN_EXPIRE_MINUTES, jwt_access_token_expire_minutes |
| jwt_refresh_token_expire_days | int | 30, lớn hơn 0 | JWT_REFRESH_TOKEN_EXPIRE_DAYS, jwt_refresh_token_expire_days |
| jwt_issuer | str | "study2work", dài tối thiểu 1 | JWT_ISSUER, jwt_issuer |
| jwt_audience | str | "study-api", dài tối thiểu 1 | JWT_AUDIENCE, jwt_audience |
| refresh_token_pepper | SecretStr hoặc None | None, nếu có dài tối thiểu 32 | REFRESH_TOKEN_PEPPER, refresh_token_pepper |

db_password, jwt_secret_key và refresh_token_pepper dùng SecretStr. Khi cần
giá trị thật cho thư viện hạ tầng, source dùng get_secret_value(); không dùng
str(secret) để tránh làm lộ giá trị.

Ví dụ tạo settings cho test:

~~~python
from app.core.config import Settings

test_settings = Settings(
    app_env="test",
    enable_docs=False,
    db_host="127.0.0.1",
    db_port=5432,
    db_name="study2work_test",
    db_user="study2work",
    db_password="test-password",
    db_schema="public",
    jwt_algorithm="HS256",
    jwt_secret_key="test-secret-key-that-is-at-least-32-characters",
)
~~~

#### Settings.parse_cors_origins

~~~python
@field_validator("cors_origins", mode="before")
@classmethod
def parse_cors_origins(cls, value: object) -> list[str]:
    ...
~~~

Nhận None, list hoặc chuỗi comma-separated:

~~~python
Settings.parse_cors_origins(None)
# []

Settings.parse_cors_origins("http://localhost:5173, http://localhost:5174")
# ["http://localhost:5173", "http://localhost:5174"]

Settings.parse_cors_origins([" http://localhost:5173 ", ""])
# ["http://localhost:5173"]
~~~

Mỗi phần tử được chuyển thành string, trim whitespace và loại phần tử rỗng.
Giá trị không phải list/string/None gây TypeError với message
cors_origins must be a list or comma-separated string. Khi khởi tạo Settings,
Pydantic sẽ bọc lỗi validation theo cơ chế của Pydantic.

#### Settings.validate_db_schema

~~~python
@field_validator("db_schema")
@classmethod
def validate_db_schema(cls, value: str) -> str:
    ...
~~~

Trim schema rồi chỉ chấp nhận chữ cái, chữ số và dấu gạch dưới. Mục đích là
đảm bảo giá trị có thể đưa vào PostgreSQL search_path mà không chứa ký tự nguy
hiểm như ; hoặc khoảng trắng.

~~~python
Settings.validate_db_schema(" study_dev0 ")
# "study_dev0"

Settings.validate_db_schema("study;drop table users")
# ValueError
~~~

Chuỗi rỗng hoặc giá trị không hợp lệ sẽ làm Settings(...) ném
pydantic.ValidationError.

#### Settings.validate_jwt_key_configuration

~~~python
@model_validator(mode="after")
def validate_jwt_key_configuration(self) -> Settings:
    ...
~~~

Kiểm tra key sau khi toàn bộ field đã được parse:

- jwt_algorithm == "HS256" bắt buộc có jwt_secret_key.
- jwt_algorithm == "ES256" bắt buộc có jwt_public_key.

Validator này không kiểm tra private PEM có hợp lệ hay không; private key sẽ
được kiểm tra thực tế khi create_access_token() cần signing key.

#### Compatibility properties

Các property sau giữ API uppercase cho code cũ nhưng đều đọc từ field
snake_case:

~~~python
@property
def DB_HOST(self) -> str: ...

@property
def DB_PORT(self) -> int: ...

@property
def DB_NAME(self) -> str: ...

@property
def DB_USER(self) -> str: ...

@property
def DB_PASSWORD(self) -> str: ...

@property
def DB_SCHEMA(self) -> str: ...

@property
def JWT_SECRET_KEY(self) -> SecretStr | None: ...

@property
def JWT_ALGORITHM(self) -> JwtAlgorithm: ...

@property
def JWT_ACCESS_TOKEN_EXPIRE_MINUTES(self) -> int: ...

@property
def JWT_REFRESH_TOKEN_EXPIRE_DAYS(self) -> int: ...

@property
def JWT_ISSUER(self) -> str: ...
~~~

Đây là các property read-only; assignment trực tiếp vào tên uppercase không
phải API cập nhật settings. Muốn tạo cấu hình mới, tạo instance Settings mới.

DB_PASSWORD trả về plain string qua SecretStr.get_secret_value() vì đây là
compatibility API. Code mới nên dùng settings.db_password và chỉ unwrap tại
boundary cần thiết. Source hiện không khai báo uppercase property cho mọi field
JWT mới, ví dụ JWT_PUBLIC_KEY, JWT_PRIVATE_KEY và JWT_AUDIENCE.

#### get_settings

~~~python
@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Load and cache settings for the current process."""
~~~

Mỗi process chỉ tạo một Settings cho tới khi cache bị clear. Hàm đọc .env và
environment tại thời điểm gọi đầu tiên; nếu thiếu DB field hoặc JWT key phù hợp,
lỗi validation xuất hiện tại thời điểm đó.

~~~python
from app.core.config import get_settings

settings = get_settings()
print(settings.app_env)
~~~

Trong test đổi environment giữa các case, có thể dùng API cache của
functools.lru_cache là get_settings.cache_clear() trước khi gọi lại. Không clear
cache tùy tiện trong request đang chạy.

#### _LazySettings.__getattr__ và __repr__

~~~python
class _LazySettings:
    def __getattr__(self, name: str) -> object: ...
    def __repr__(self) -> str: ...
~~~

Biến module settings là proxy tương thích:

~~~python
from app.core.config import settings

settings.app_env       # chuyển tiếp tới get_settings().app_env
repr(settings)          # "settings (lazy)"
~~~

__getattr__ chỉ gọi get_settings() khi attribute chưa có trên proxy, nhờ đó
import module không buộc production .env phải hợp lệ ngay lập tức.

---

## database.py — SQLAlchemy và session

### build_database_url

~~~python
def build_database_url(config: Settings) -> URL:
~~~

Tạo SQLAlchemy URL với driver postgresql+psycopg, lấy host/port/database và
credential từ Settings. Dùng URL.create() thay vì nối chuỗi nên password có ký
tự đặc biệt được escape đúng:

~~~python
from app.core.database import build_database_url

url = build_database_url(settings)
safe_url = url.render_as_string(hide_password=True)
~~~

Không log URL với hide_password=False trong application log. Hàm không mở kết
nối database và không tạo engine.

### build_engine

~~~python
def build_engine(config: Settings) -> Engine:
~~~

Tạo engine synchronous với các option:

- pool_pre_ping=True: kiểm tra connection trước khi dùng;
- pool_size=config.database_pool_size;
- max_overflow=config.database_max_overflow;
- PostgreSQL search_path={config.db_schema},public.

~~~python
from app.core.database import build_engine

engine = build_engine(test_settings)
~~~

create_engine() chưa thực hiện query nghiệp vụ; connection thường được mở khi
engine cần connect. Caller chịu trách nhiệm dispose engine khi lifecycle runtime
yêu cầu.

### build_session_factory

~~~python
def build_session_factory(database_engine: Engine) -> sessionmaker[Session]:
~~~

Tạo factory tạo sqlalchemy.orm.Session với autoflush=False,
expire_on_commit=False, class_=Session và bind vào engine được truyền vào.

~~~python
factory = build_session_factory(engine)
with factory() as db:
    result = db.execute(...)
~~~

Factory không tự commit và cũng không tự đóng các Session mà nó tạo.

### get_engine và get_session_factory

~~~python
@lru_cache(maxsize=1)
def get_engine() -> Engine:

@lru_cache(maxsize=1)
def get_session_factory() -> sessionmaker[Session]:
~~~

Hai hàm là default lazy resources:

1. get_engine() gọi build_engine(get_settings()) một lần mỗi process.
2. get_session_factory() gọi build_session_factory(get_engine()) một lần.

Chúng phù hợp cho app mặc định. Test/runtime cần cấu hình riêng nên dùng
build_engine()/build_session_factory() và inject factory thông qua
create_app(Settings(...)) thay vì sửa global cache.

### SessionLocal

~~~python
def SessionLocal() -> Session:
~~~

Compatibility wrapper gọi get_session_factory()() và trả về một Session mới.
Mỗi lần gọi là một object riêng. Caller bắt buộc đóng Session:

~~~python
db = SessionLocal()
try:
    ...
finally:
    db.close()
~~~

Trong HTTP view không nên gọi rải rác SessionLocal(); dùng dependency
Depends(get_db) để giữ một lifecycle theo request.

### get_db_from_factory

~~~python
def get_db_from_factory(
    session_factory: sessionmaker[Session],
) -> Generator[Session, None, None]:
~~~

Tạo một Session từ factory, yield cho caller, rồi luôn gọi close() trong
finally, kể cả khi view ném exception. Đây là primitive để inject factory riêng
trong test/runtime. create_app() tự override get_db bằng factory trong app.state.

Hàm không commit hoặc rollback. Transaction owner là view/use case.

### get_db

~~~python
def get_db() -> Generator[Session, None, None]:
~~~

FastAPI dependency dùng get_session_factory() mặc định và delegate sang
get_db_from_factory():

~~~python
from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import get_db

@router.get("/items")
def list_items(db: Session = Depends(get_db)):
    ...
~~~

Session được close sau khi request kết thúc. Dependency không biết business
transaction và không commit.

### execute_query

~~~python
def execute_query(
    db: Session,
    query: str,
    params: Mapping[str, Any] | None = None,
) -> Result[Any]:
~~~

Chạy text(query) bằng db.execute() với params được chuyển thành dict. Dùng
named parameters, không interpolate input:

~~~python
result = execute_query(
    db,
    "SELECT id, email FROM users WHERE email = :email",
    {"email": email},
)
~~~

Hàm trả về SQLAlchemy Result, không gọi commit(), rollback() hay close() trên
Session. Caller sở hữu transaction và cách consume result.

### query_one

~~~python
def query_one(
    db: Session,
    query: str,
    params: Mapping[str, Any] | None = None,
) -> dict[str, Any] | None:
~~~

Delegate tới execute_query(), gọi mappings().first() và chuyển row đầu tiên
thành plain dict. Không có row trả về None:

~~~python
user = query_one(
    db,
    "SELECT id, email FROM users WHERE id = :id",
    {"id": user_id},
)
if user is None:
    ...
~~~

Không tự báo lỗi not-found và không commit.

### query_many

~~~python
def query_many(
    db: Session,
    query: str,
    params: Mapping[str, Any] | None = None,
) -> list[dict[str, Any]]:
~~~

Delegate tới execute_query(), gọi mappings().all() và trả list dict. Không có row
trả về []:

~~~python
users = query_many(
    db,
    "SELECT id, email FROM users ORDER BY email",
)
~~~

Query helper chỉ cung cấp data access primitive. View quyết định có cần map
not-found, commit, rollback hay controlled error hay không.

---

## responses.py — response envelope

### utc_now_iso

~~~python
def utc_now_iso() -> str:
~~~

Trả thời điểm hiện tại UTC theo ISO-8601, bỏ microsecond và dùng hậu tố Z:

~~~python
utc_now_iso()
# Ví dụ: "2026-08-10T12:34:56Z"
~~~

Kết quả thay đổi theo thời gian; function không nhận tham số và không có
exception nghiệp vụ riêng.

### ErrorDetail

~~~python
class ErrorDetail(BaseModel):
    field: str | None = None
    code: str
    message: str
~~~

Đại diện một lỗi field-level hoặc business-level an toàn cho client.

- field: tên/path field, có thể None nếu lỗi không gắn với field.
- code: mã máy đọc được.
- message: message client-facing.
- model_config = ConfigDict(extra="forbid"): field ngoài schema bị từ chối.

~~~python
detail = ErrorDetail(
    field="email",
    code="INVALID_EMAIL",
    message="Email không hợp lệ.",
)
~~~

### ApiError.__init__

~~~python
class ApiError(Exception):
    def __init__(
        self,
        *,
        status_code: int,
        business_code: str,
        message: str,
        trace_id: str,
        errors: Sequence[ErrorDetail] = (),
        headers: Mapping[str, str] | None = None,
    ) -> None:
~~~

Tạo controlled exception để api_error_handler chuyển thành JSON response.

- status_code: HTTP status trả cho client.
- business_code: business code của API.
- message: message an toàn.
- trace_id: trace liên quan; handler dùng fallback từ request nếu chuỗi rỗng.
- errors: sequence được lưu thành tuple.
- headers: mapping được copy thành dict.

super().__init__(message) giúp exception có message nhưng handler không được
trả repr(exc) cho client.

~~~python
raise ApiError(
    status_code=404,
    business_code="USER_NOT_FOUND",
    message="Không tìm thấy người dùng.",
    trace_id=trace_id,
)
~~~

### success_response

~~~python
def success_response(
    *,
    business_code: str,
    message: str,
    trace_id: str,
    data: Any = None,
    meta: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
~~~

Tạo canonical success envelope:

~~~json
{
  "success": true,
  "businessCode": "COURSE_LOADED",
  "message": "Loaded",
  "data": {"id": "course-1"},
  "meta": {},
  "traceId": "uuid"
}
~~~

meta được copy thành dict; None thành {}. Hàm không validate trace ID hay
business code, vì việc đó thuộc caller/contract layer.

~~~python
return success_response(
    business_code="USER_LOADED",
    message="Lấy người dùng thành công.",
    trace_id=get_trace_id(request),
    data={"id": user["id"]},
    meta={"source": "database"},
)
~~~

### error_response

~~~python
def error_response(
    *,
    business_code: str,
    message: str,
    trace_id: str,
    errors: Sequence[ErrorDetail] = (),
    meta: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
~~~

Tạo canonical error envelope:

~~~json
{
  "success": false,
  "businessCode": "VALIDATION_ERROR",
  "message": "Dữ liệu đầu vào không hợp lệ.",
  "data": null,
  "meta": {
    "fieldErrors": [
      {"field": "email", "code": "INVALID_EMAIL", "message": "Email không hợp lệ."}
    ]
  },
  "traceId": "uuid"
}
~~~

Behavior chi tiết:

- copy meta vào response_meta;
- nếu errors không rỗng, serialize từng ErrorDetail vào meta.fieldErrors,
  loại field có giá trị None;
- luôn đặt data là None;
- không đặt errors ở top-level.

Nếu caller truyền sẵn meta["fieldErrors"] và errors cũng có phần tử, giá trị từ
errors sẽ ghi đè meta["fieldErrors"].

### raise_api_error

~~~python
def raise_api_error(
    *,
    status_code: int,
    business_code: str,
    message: str,
    trace_id: str,
    errors: Sequence[ErrorDetail] = (),
    headers: Mapping[str, str] | None = None,
) -> NoReturn:
~~~

Tạo và raise ApiError với đúng các argument tương ứng. Hàm không trả về:

~~~python
if user is None:
    raise_api_error(
        status_code=404,
        business_code="USER_NOT_FOUND",
        message="Không tìm thấy người dùng.",
        trace_id=trace_id,
    )
~~~

### success_payload

~~~python
def success_payload(
    *,
    business_code: str,
    message: str,
    trace_id: str,
    data: Any = None,
    meta: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
~~~

Compatibility alias của success_response; kết quả và behavior giống hệt. Code
mới nên gọi success_response() để thể hiện canonical API.

### error_payload

~~~python
def error_payload(
    *,
    business_code: str,
    message: str,
    trace_id: str,
    errors: Sequence[ErrorDetail],
) -> dict[str, Any]:
~~~

Compatibility adapter cho caller cũ. Nó giữ errors ở top-level, không có data
hay meta:

~~~json
{
  "success": false,
  "businessCode": "VALIDATION_ERROR",
  "message": "Invalid",
  "errors": [{"field": null, "code": "INVALID_EMAIL", "message": "Invalid email"}],
  "traceId": "uuid"
}
~~~

Không dùng cho API mới.

### ApiResponse

~~~python
class ApiResponse(BaseModel):
    business_code: str
    message: str
    result: Any = None
    trace_id: str
    meta: dict[str, Any] | None = None
    status_code: int = 200  # từ 100 đến 599
~~~

Model compatibility cho module cũ dùng naming result/trace_id dạng Python.
status_code có default 200 và bị Pydantic từ chối nếu ngoài khoảng 100–599.

#### ApiResponse.success_payload

~~~python
def success_payload(self) -> dict[str, Any]:
~~~

Chuyển model thành canonical success envelope bằng cách map result → data,
trace_id → traceId và business_code → businessCode. status_code không xuất hiện
trong body.

#### ApiResponse.raise_error

~~~python
def raise_error(self) -> NoReturn:
~~~

Gọi raise_api_error() bằng các field của model, giữ status_code và không truyền
field errors. Dùng cho code cũ cần raise từ một response model.

---

## security.py — password và token

### Constants và type aliases

~~~python
ACCESS_TOKEN = "access"
REFRESH_TOKEN = "refresh"
PASSWORD_ALGORITHM = "ARGON2ID"
PasswordAlgorithm = Literal["ARGON2ID", "BCRYPT"]
~~~

ACCESS_TOKEN và REFRESH_TOKEN là giá trị claim type. Hash password mới dùng
ARGON2ID; BCRYPT chỉ hỗ trợ dữ liệu legacy.

### TokenKeyProvider.get_verification_key

~~~python
class TokenKeyProvider(Protocol):
    def get_verification_key(self, *, key_id: str | None) -> str | bytes:
~~~

Đây là interface structural cho nơi cung cấp public verification key, ví dụ
static key store hoặc JWKS adapter. key_id lấy từ JWT header kid; provider trả
PEM/string hoặc bytes.

~~~python
class LocalKeyProvider:
    def get_verification_key(self, *, key_id: str | None) -> str:
        return public_key_for_kid(key_id)
~~~

JwksKeyProvider chỉ là alias của TokenKeyProvider, không có implementation JWKS
trong core.

### TokenError

~~~python
class TokenError(Exception):
~~~

Exception dùng cho token không đáng tin, thiếu key, token hết hạn hoặc sai type.
Caller nên map sang lỗi auth an toàn, không trả message nội bộ hay raw JWT
exception cho client.

### PasswordHasher.hash

~~~python
@staticmethod
def hash(
    password: str,
    algorithm: PasswordAlgorithm = "ARGON2ID",
) -> str:
~~~

Hash plaintext password:

- ARGON2ID: dùng policy time_cost=3, memory_cost=64 * 1024, parallelism=1;
- BCRYPT: dùng bcrypt.gensalt() và trả chuỗi bcrypt;
- algorithm khác: raise ValueError.

~~~python
from app.core.security import PasswordHasher

password_hash = PasswordHasher.hash("correct horse battery staple")
# bắt đầu bằng "$argon2id$"
~~~

Không log password hoặc password_hash. Code nghiệp vụ nên dùng wrapper
hash_password() để luôn theo policy canonical.

### PasswordHasher.verify

~~~python
@staticmethod
def verify(
    password: str,
    hashed_password: str,
    algorithm: str | None = None,
) -> bool:
~~~

Chọn algorithm theo thứ tự:

1. algorithm được truyền vào, chuyển thành uppercase;
2. nếu không có, nhận diện từ prefix của hashed_password;
3. nếu không nhận diện được, trả False.

Argon2 bắt mismatch, verification error và malformed hash; bcrypt bắt
ValueError/TypeError. Các trường hợp đó đều trả False. Algorithm được truyền
vào sẽ override detection. Algorithm không hỗ trợ cũng trả False.

### password_algorithm_for_hash

~~~python
def password_algorithm_for_hash(
    hashed_password: str,
) -> PasswordAlgorithm | None:
~~~

Nhận diện format bằng prefix, không verify:

| Prefix | Kết quả |
|---|---|
| $argon2... | ARGON2ID |
| $2a$, $2b$, $2y$ | BCRYPT |
| khác | None |

Đây chỉ là detection heuristic, không dùng nó để tin rằng password đúng.

### needs_password_rehash

~~~python
def needs_password_rehash(
    hashed_password: str,
    algorithm: str | None = None,
) -> bool:
~~~

Trả True khi password đã verify nhưng nên ghi lại theo policy Argon2id hiện tại:

- Argon2id: delegate check_needs_rehash();
- hash Argon2 malformed: True;
- bcrypt: True để migrate legacy;
- algorithm unknown hoặc không phải Argon2id: True.

Hàm không tự hash lại và không cập nhật database. Flow migration là verify
thành công → kiểm tra hàm này → hash lại bằng hash_password() → update trong
transaction phù hợp.

### hash_password và verify_password

~~~python
def hash_password(password: str) -> str:

def verify_password(
    password: str,
    hashed_password: str,
    algorithm: str | None = None,
) -> bool:
~~~

Đây là wrappers công khai khuyến nghị:

~~~python
stored_hash = hash_password(plain_password)
if verify_password(plain_password, stored_hash):
    ...
~~~

hash_password() luôn chọn Argon2id. verify_password() delegate toàn bộ behavior
của PasswordHasher.verify(), bao gồm verify bcrypt legacy.

### _settings_secret

~~~python
def _settings_secret(value: Any) -> str | None:
~~~

Helper nội bộ unwrap một secret:

- None → None;
- object có get_secret_value() → giá trị được unwrap;
- object khác → str(value).

Chỉ dùng ở security boundary, không log kết quả.

### _signing_key

~~~python
def _signing_key() -> str:
~~~

Đọc get_settings() để chọn key ký:

- ES256: lấy jwt_private_key;
- HS256: lấy jwt_secret_key.

Thiếu key sẽ raise TokenError với message tiếng Việt an toàn. Hàm được gọi
ngầm bởi _create_token(), không phải API thường gọi trực tiếp.

### _verification_key

~~~python
def _verification_key(
    token: str,
    key_provider: TokenKeyProvider | None,
) -> str | bytes:
~~~

Chọn key verify:

1. Nếu có key_provider, đọc JWT header chưa verify để lấy kid, rồi gọi
   get_verification_key(key_id=...).
2. Nếu không có provider và algorithm ES256, dùng jwt_public_key.
3. Nếu HS256, dùng jwt_secret_key.

Lỗi đọc header/provider (InvalidTokenError, KeyError, TypeError) được map thành
TokenError("Không lấy được khóa xác thực token"). Provider phải tự đảm bảo key
được chọn theo kid; việc đọc unverified header không phải là verify chữ ký.

### _create_token

~~~python
def _create_token(
    *,
    subject: str,
    token_type: str,
    expires_delta: timedelta,
    claims: Mapping[str, Any] | None = None,
    include_audience: bool = True,
) -> str:
~~~

Primitive tạo JWT với payload mặc định:

~~~text
sub  = subject
type = token_type
jti  = UUID mới
iat  = now UTC
exp  = now + expires_delta
iss  = settings.jwt_issuer
aud  = settings.jwt_audience (nếu include_audience=True)
~~~

claims được merge nhưng không được ghi đè các claim reserved: sub, type, jti,
iat, exp, iss, aud. JWT được ký bằng key từ _signing_key() và algorithm trong
settings.

Đây là private primitive; nên dùng create_access_token() hoặc legacy wrapper.

### create_access_token

~~~python
def create_access_token(
    *,
    user_id: str,
    roles: list[str] | None = None,
    claims: Mapping[str, Any] | None = None,
) -> str:
~~~

Tạo access JWT với sub=user_id, type="access", thời hạn
jwt_access_token_expire_minutes, audience bắt buộc theo jwt_audience, roles mặc
định [] và claims bổ sung không được override reserved claims.

~~~python
token = create_access_token(
    user_id="user-1",
    roles=["learner"],
    claims={"tenant": "study"},
)
~~~

Không lưu access token vào log hoặc response ngoài nơi auth contract yêu cầu.

### create_refresh_token

~~~python
def create_refresh_token(*, user_id: str) -> str:
~~~

Tạo legacy JWT refresh token với type="refresh", thời hạn
jwt_refresh_token_expire_days và không có audience claim. Token này chứa subject
user nên không phải flow refresh token mới được khuyến nghị.

Code mới nên dùng generate_refresh_token() và lưu hash. Wrapper tồn tại để
tương thích với auth module hiện tại cho tới khi session schema phù hợp.

### decode_token

~~~python
def decode_token(
    token: str,
    *,
    expected_type: str,
    key_provider: TokenKeyProvider | None = None,
    require_audience: bool = True,
) -> dict[str, Any]:
~~~

Decode và validate chặt JWT. Các claim luôn bắt buộc:

~~~text
sub, type, jti, iat, exp, iss
~~~

Nếu require_audience=True, aud cũng bắt buộc và phải bằng
settings.jwt_audience. Algorithm chỉ nhận đúng algorithm hiện tại trong
settings; issuer phải đúng settings.jwt_issuer; chữ ký được verify bằng
_verification_key().

Sau khi JWT decode thành công, hàm còn kiểm tra payload["type"] ==
expected_type và sub là non-empty string. Các lỗi JWT, key, type, value hoặc
token malformed đều được map thành TokenError an toàn. require_audience=False
dùng cho legacy refresh JWT và tắt verify audience.

### decode_access_token và decode_refresh_token

~~~python
def decode_access_token(
    token: str,
    *,
    key_provider: TokenKeyProvider | None = None,
) -> dict[str, Any]:

def decode_refresh_token(
    token: str,
    *,
    key_provider: TokenKeyProvider | None = None,
) -> dict[str, Any]:
~~~

Hai wrapper cố định expected_type:

- decode_access_token() yêu cầu type="access" và audience.
- decode_refresh_token() yêu cầu type="refresh" và không yêu cầu audience.

~~~python
claims = decode_access_token(token)
user_id = claims["sub"]
~~~

Token sai loại, hết hạn, sai signature/issuer/audience hoặc thiếu claim đều
raise TokenError.

### generate_refresh_token

~~~python
def generate_refresh_token() -> str:
~~~

Tạo opaque refresh token ngẫu nhiên bằng secrets.token_urlsafe(48). Token không
chứa user ID hay claim có thể decode. Raw token chỉ nên trả một lần cho client
qua auth response; persistence layer không được lưu raw token.

~~~python
raw_token = generate_refresh_token()
digest = hash_refresh_token(raw_token)
# lưu digest; trả raw_token cho client theo auth contract
~~~

### hash_refresh_token

~~~python
def hash_refresh_token(token: str, pepper: str | None = None) -> str:
~~~

Tạo HMAC-SHA256 hex digest để persistence layer lưu. Pepper được chọn theo thứ
tự:

1. argument pepper nếu là truthy;
2. settings.refresh_token_pepper;
3. fallback settings.jwt_secret_key để compatibility;
4. nếu vẫn thiếu, raise TokenError.

~~~python
digest = hash_refresh_token(raw_token)
# digest là chuỗi hex, không phải raw token
~~~

Hash cùng token và cùng pepper cho cùng digest, token khác cho digest khác.
Pepper không được trả hoặc log.

### compare_token_hash

~~~python
def compare_token_hash(expected: str, actual: str) -> bool:
~~~

So sánh hai digest bằng hmac.compare_digest() để giảm timing side channel. Hàm
chỉ so sánh chuỗi đã hash, không hash token và không truy cập settings:

~~~python
if compare_token_hash(stored_digest, hash_refresh_token(presented_token)):
    ...
~~~

---

## trace.py — Trace ID

### TRACE_HEADER

~~~python
TRACE_HEADER = "X-Trace-Id"
~~~

Đây là tên header chuẩn dùng cả request input và response output.

### create_trace_id

~~~python
def create_trace_id() -> str:
~~~

Tạo UUID v4 mới và trả canonical string. Dùng khi request không có trace hợp lệ
hoặc khi tạo context ngoài HTTP.

### normalize_trace_id

~~~python
def normalize_trace_id(value: str | None) -> str | None:
~~~

Nếu value rỗng/None hoặc không parse được bằng UUID(value), trả None. UUID hợp
lệ được trả về dạng canonical string:

~~~python
normalize_trace_id("7C3A2F1B-31C5-4A21-9B3E-7D1745C4748A")
# "7c3a2f1b-31c5-4a21-9b3e-7d1745c4748a"

normalize_trace_id("invalid")
# None
~~~

Hàm không tạo UUID mới; caller quyết định fallback.

### set_current_trace_id

~~~python
def set_current_trace_id(trace_id: str) -> Token[str | None]:
~~~

Set trace_id vào module-level ContextVar và trả context token. Token cần được
giữ để reset đúng context cũ:

~~~python
token = set_current_trace_id(trace_id)
try:
    process_request()
finally:
    reset_current_trace_id(token)
~~~

ContextVar phù hợp cho async/concurrent request vì mỗi context có giá trị riêng.

### reset_current_trace_id

~~~python
def reset_current_trace_id(token: Token[str | None]) -> None:
~~~

Restore trace context trước đó bằng token trả từ set_current_trace_id(). Phải
gọi trong finally sau khi request kết thúc.

### get_current_trace_id

~~~python
def get_current_trace_id() -> str | None:
~~~

Đọc trace ID từ ContextVar. Ngoài request/middleware context, kết quả mặc định
là None.

### get_trace_id

~~~python
def get_trace_id(request: Request) -> str:
~~~

Đọc request.state.trace_id, normalize lại và nếu thiếu/sai thì tạo UUID mới,
đồng thời ghi lại vào request state. Đây là fallback khi middleware bị bypass.

~~~python
@router.get("/resource")
def resource(request: Request):
    trace_id = get_trace_id(request)
    return success_response(
        business_code="RESOURCE_LOADED",
        message="Loaded",
        trace_id=trace_id,
        data={},
    )
~~~

Hàm không set ContextVar; việc đó do TraceIdMiddleware.dispatch() thực hiện.

---

## middleware.py — HTTP middleware

### TraceIdMiddleware

~~~python
class TraceIdMiddleware(BaseHTTPMiddleware):
~~~

Middleware đảm bảo một trace ID hợp lệ được dùng xuyên suốt request:

1. đọc header X-Trace-Id;
2. normalize, hoặc gọi create_trace_id() nếu invalid/thiếu;
3. lưu request.state.trace_id;
4. set ContextVar bằng set_current_trace_id();
5. gọi downstream call_next(request);
6. thêm header X-Trace-Id vào response;
7. reset context trong finally.

### TraceIdMiddleware.dispatch

~~~python
async def dispatch(
    self,
    request: Request,
    call_next: RequestResponseEndpoint,
) -> Response:
~~~

Nếu downstream ném bất kỳ Exception nào, middleware gọi
unhandled_exception_handler() để tạo response 500 an toàn, sau đó vẫn thêm
trace header. Exception không được trả raw cho client.

Đăng ký thủ công:

~~~python
app.add_middleware(TraceIdMiddleware)
~~~

Middleware cần được lắp ở app composition root, không tạo instance trong từng
router. Trace ID do middleware tạo sẽ được dùng đồng thời ở request state,
ContextVar, log/error response và response header/body.

---

## exceptions.py — exception handlers

Module dùng JSONResponse, error_response() và get_trace_id() để giữ API error
contract. Các handler đều là async vì FastAPI/Starlette gọi chúng theo exception
handling protocol.

### _validation_field

~~~python
def _validation_field(location: Sequence[Any]) -> str | None:
~~~

Chuyển loc của FastAPI/Pydantic thành field path client-facing. Các segment
transport (body, query, path, header, cookie) bị bỏ, segment còn lại được
stringify rồi nối bằng dấu chấm:

~~~python
_validation_field(("body", "email"))
# "email"

_validation_field(("body", "items", 0, "name"))
# "items.0.name"

_validation_field(("body",))
# None
~~~

Đây là private helper được request_validation_exception_handler() dùng.

### api_error_handler

~~~python
async def api_error_handler(
    request: Request,
    exc: ApiError,
) -> JSONResponse:
~~~

Render controlled ApiError:

- HTTP status = exc.status_code;
- body = error_response() với business code/message/errors của exception;
- trace ID = exc.trace_id nếu có, fallback get_trace_id(request);
- response headers = exc.headers.

Handler không expose exception repr. Đăng ký bằng
app.add_exception_handler(ApiError, api_error_handler).

### http_exception_handler

~~~python
async def http_exception_handler(
    request: Request,
    exc: HTTPException,
) -> JSONResponse:
~~~

Xử lý lỗi protocol từ Starlette/FastAPI mà không expose arbitrary detail.

- Nếu exc.detail là dict và detail["success"] is False, copy dict đó và thêm
  traceId nếu dict chưa có.
- Các detail khác được thay bằng canonical generic error:
  businessCode="HTTP_ERROR", message="Yêu cầu không thể được xử lý.".
- Giữ exc.status_code và exc.headers.

Vì vậy unknown route trả status 404 nhưng không trả raw "Not Found" trong
message API.

### request_validation_exception_handler

~~~python
async def request_validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
~~~

Map mỗi lỗi trong exc.errors() thành ErrorDetail:

- field = _validation_field(error["loc"]);
- code = error["type"] uppercase, dấu . đổi thành _, fallback INVALID_FIELD;
- message = error["msg"], fallback "Giá trị không hợp lệ.".

Trả HTTP 422 với:

~~~text
businessCode = "VALIDATION_ERROR"
message      = "Dữ liệu đầu vào không hợp lệ."
meta.fieldErrors = các ErrorDetail
~~~

### unhandled_exception_handler

~~~python
async def unhandled_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
~~~

Lấy trace ID, log exception nội bộ bằng logger.exception() với
trace_id=<id>, rồi trả:

~~~text
HTTP 500
businessCode = "INTERNAL_SERVER_ERROR"
message      = "Đã xảy ra lỗi nội bộ hệ thống."
~~~

Body không chứa exception detail, stack trace, SQL, credential hoặc token. Log
nội bộ vẫn có exc_info=exc để chẩn đoán; message/error object không được đưa ra
client.

---

## Các flow sử dụng thực tế

### 1. Tạo app với cấu hình riêng

~~~python
from fastapi import FastAPI
from app.core.config import Settings
from app.main import create_app

settings = Settings(
    app_env="test",
    enable_docs=False,
    db_host="localhost",
    db_name="study2work_test",
    db_user="study2work",
    db_password="test-password",
    db_schema="public",
    jwt_algorithm="HS256",
    jwt_secret_key="test-secret-key-that-is-at-least-32-characters",
)

app: FastAPI = create_app(settings)
~~~

create_app() tạo engine/session factory từ config và override dependency get_db;
app không dùng default cached factory cho instance đó.

### 2. Endpoint nhận request-scoped DB Session

~~~python
from typing import Any
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.core.database import get_db, query_many
from app.core.responses import success_response
from app.core.trace import get_trace_id

router = APIRouter()

@router.get("/users")
def list_users(
    request: Request,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    rows = query_many(
        db,
        "SELECT id, email FROM users ORDER BY email",
    )
    return success_response(
        business_code="USERS_LOADED",
        message="Lấy danh sách người dùng thành công.",
        trace_id=get_trace_id(request),
        data=rows,
    )
~~~

Session được tạo trước khi gọi endpoint và đóng sau request. query_many() chỉ
đọc dữ liệu; nếu use case có mutation, view phải gọi db.commit() hoặc
db.rollback() theo boundary.

### 3. Mutation với transaction ownership

~~~python
from sqlalchemy.exc import IntegrityError
from app.core.database import execute_query
from app.core.responses import raise_api_error

def create_record(db: Session, trace_id: str) -> dict[str, Any]:
    try:
        execute_query(
            db,
            "INSERT INTO records (id) VALUES (:id)",
            {"id": "record-1"},
        )
        db.commit()
    except IntegrityError:
        db.rollback()
        raise_api_error(
            status_code=409,
            business_code="RECORD_ALREADY_EXISTS",
            message="Bản ghi đã tồn tại.",
            trace_id=trace_id,
        )
~~~

Tên table/column/constraint trong ví dụ thật phải đến từ schema hiện có. Không
commit trong query.py hoặc database helper cấp thấp nếu view còn mutation phụ
thuộc cần atomicity.

### 4. Success và controlled error

~~~python
def load_course(request: Request, db: Session) -> dict[str, Any]:
    trace_id = get_trace_id(request)
    course = query_one(
        db,
        "SELECT id, title FROM courses WHERE id = :id",
        {"id": "course-1"},
    )
    if course is None:
        raise_api_error(
            status_code=404,
            business_code="COURSE_NOT_FOUND",
            message="Không tìm thấy khóa học.",
            trace_id=trace_id,
        )
    return success_response(
        business_code="COURSE_LOADED",
        message="Lấy khóa học thành công.",
        trace_id=trace_id,
        data=course,
    )
~~~

ApiError sẽ được api_error_handler chuyển sang JSONResponse; view không cần tự
dựng error JSON.

### 5. Password registration/login

~~~python
from app.core.security import (
    hash_password,
    needs_password_rehash,
    verify_password,
)

password_hash = hash_password(plain_password)

if not verify_password(plain_password, password_hash):
    raise ValueError("invalid credentials")

# Login legacy: sau khi verify bcrypt thành công, có thể migrate hash.
if needs_password_rehash(password_hash):
    upgraded_hash = hash_password(plain_password)
~~~

plain_password không được lưu/log/đưa vào response. Việc persist upgraded_hash
thuộc module view và transaction hiện tại.

### 6. Tạo và decode access token

~~~python
from app.core.security import (
    TokenError,
    create_access_token,
    decode_access_token,
)

access_token = create_access_token(
    user_id="user-1",
    roles=["learner"],
)

try:
    claims = decode_access_token(access_token)
except TokenError:
    # Map thành lỗi authentication an toàn ở auth dependency.
    raise

user_id = claims["sub"]
roles = claims.get("roles", [])
~~~

decode_access_token() kiểm tra signature, algorithm, issuer, audience, type,
required claims, expiration và subject.

### 7. Opaque refresh token và persistence

~~~python
from app.core.security import (
    compare_token_hash,
    generate_refresh_token,
    hash_refresh_token,
)

raw_refresh_token = generate_refresh_token()
stored_digest = hash_refresh_token(raw_refresh_token)

# Persistence layer chỉ lưu stored_digest.
# Auth response trả raw_refresh_token cho client đúng một lần.

presented_digest = hash_refresh_token(presented_token)
if compare_token_hash(stored_digest, presented_digest):
    ...
~~~

generate_refresh_token() không biết user/session database. Rotation, expiry
record, revoke, reuse detection và transaction persistence thuộc Identity
module/schema.

### 8. Trace ID trong endpoint và log

~~~python
from fastapi import Request

@router.get("/example")
def example(request: Request) -> dict[str, Any]:
    trace_id = get_trace_id(request)
    logger.info("Loading example; trace_id=%s", trace_id)
    return success_response(
        business_code="EXAMPLE_LOADED",
        message="Loaded",
        trace_id=trace_id,
        data={},
    )
~~~

Nếu request gửi X-Trace-Id là UUID hợp lệ, cùng giá trị được giữ lại. Nếu
header thiếu hoặc invalid, middleware tạo UUID mới và response có UUID đó ở cả
body traceId lẫn response header X-Trace-Id.

---

## Giới hạn và lưu ý bảo mật

### Database

- get_db() là request-scoped; không dùng một global mutable Session cho nhiều
  request concurrent.
- execute_query(), query_one(), query_many() không commit/rollback.
- View/use-case sở hữu transaction boundary vì chỉ view biết toàn bộ mutation có
  cần atomic hay không.
- SQL phải dùng named parameters; không nối raw user input bằng f-string.
- Không tự invent table, column hoặc constraint chưa có trong schema/source.

### Password và token

- Password mới dùng Argon2id; bcrypt chỉ verify legacy và được đánh dấu cần
  rehash.
- Không lưu plaintext password, raw refresh token hoặc password hash trong
  response/log.
- JWT ES256 cần private key để ký và public key để verify; HS256 cần secret.
- create_refresh_token()/decode_refresh_token() là legacy JWT path.
- Flow mới dùng opaque refresh token + HMAC digest; persistence/rotation/revoke
  không thuộc core.
- TokenKeyProvider chỉ là interface; core chưa triển khai JWKS fetching.

### Response và exception

- API mới dùng shape canonical:

~~~json
{
  "success": false,
  "businessCode": "...",
  "message": "...",
  "data": null,
  "meta": {"fieldErrors": []},
  "traceId": "..."
}
~~~

- error_payload() là top-level errors adapter cho code cũ, không phải shape
  khuyến nghị mới.
- unhandled_exception_handler() log exception nội bộ cùng trace ID nhưng client
  chỉ nhận message generic.
- Không đưa raw SQL, database detail, stack trace, secret hoặc token vào HTTP
  response.

### Test và kiểm tra source

Các behavior cốt lõi hiện được kiểm tra trong apps/study-server/tests:

- tests/core/test_config.py: alias environment và schema validation;
- tests/core/test_database.py: URL escaping, query helpers, session close;
- tests/core/test_responses.py: canonical/legacy envelope và ApiError;
- tests/core/test_security_tokens.py: JWT validation và opaque refresh hash;
- tests/test_security.py: Argon2id và bcrypt legacy;
- tests/test_health.py: trace header/body, validation/HTTP/500 error envelope.

Khi thay đổi core, chạy từ thư mục apps/study-server:

~~~bash
uv run ruff check .
uv run ruff format --check .
uv run mypy app
uv run pytest
~~~
