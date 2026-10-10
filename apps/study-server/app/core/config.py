"""Cung cấp cấu hình có kiểu dữ liệu cho Study API, lấy giá trị mặc định từ các hằng số tĩnh."""

from __future__ import annotations

from functools import lru_cache
from typing import Any, Literal

from pydantic import (
    AliasChoices,
    BaseModel,
    ConfigDict,
    Field,
    SecretStr,
    ValidationError,
    field_validator,
    model_validator,
)

from app.core import constants

Environment = Literal["local", "test", "staging", "production"]
JwtAlgorithm = Literal["ES256", "HS256"]


class Settings(BaseModel):
    """Mô hình cấu hình có kiểu dữ liệu dùng chung cho API và các thành phần hạ tầng. Mô hình lấy
    mặc định từ app.core.constants, chấp nhận bí danh tên trường cũ và kiểm tra các ràng buộc
    cấu hình trước khi ứng dụng sử dụng."""

    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
        validate_default=True,
    )

    def __init__(self, **data: Any) -> None:
        """Khởi tạo Settings bằng các giá trị được cung cấp và để Pydantic kiểm tra kiểu cùng ràng
        buộc trường. Nếu cấu hình không hợp lệ, chuyển ValidationError thành ValueError chung để
        chi tiết cấu hình không bị lộ trực tiếp."""

        try:
            super().__init__(**data)
        except ValidationError:
            raise ValueError("Invalid application settings.") from None

    app_env: Environment = Field(
        default=constants.APP_ENV,
        validation_alias=AliasChoices("APP_ENV", "app_env"),
    )
    enable_docs: bool = Field(
        default=constants.ENABLE_DOCS,
        validation_alias=AliasChoices("ENABLE_DOCS", "enable_docs"),
    )
    cors_origins: list[str] = Field(
        default_factory=lambda: list(constants.CORS_ORIGINS),
        validation_alias=AliasChoices("CORS_ORIGINS", "cors_origins"),
    )

    database_url: SecretStr = Field(
        default=SecretStr(constants.URL_DATABASE),
        validation_alias=AliasChoices("URL_DATABASE", "database_url"),
    )

# Chấp nhận các thiết lập CSDL theo từng trường để tương thích với hàm khởi tạo cũ,
# nhưng app.core.database không dùng chúng để tạo engine.
    db_host: str | None = Field(
        default=None,
        validation_alias=AliasChoices("DB_HOST", "db_host"),
    )
    db_port: int | None = Field(
        default=None,
        ge=1,
        le=65535,
        validation_alias=AliasChoices("DB_PORT", "db_port"),
    )
    db_name: str | None = Field(
        default=None,
        validation_alias=AliasChoices("DB_NAME", "db_name"),
    )
    db_user: str | None = Field(
        default=None,
        validation_alias=AliasChoices("DB_USER", "db_user"),
    )
    db_password: SecretStr | None = Field(
        default=None,
        validation_alias=AliasChoices("DB_PASSWORD", "db_password"),
    )
    db_schema: str = Field(
        default=constants.DB_SCHEMA,
        min_length=1,
        validation_alias=AliasChoices("DB_SCHEMA", "db_schema"),
    )
    database_pool_size: int = Field(
        default=constants.DATABASE_POOL_SIZE,
        ge=1,
        validation_alias=AliasChoices("DATABASE_POOL_SIZE", "database_pool_size"),
    )
    database_max_overflow: int = Field(
        default=constants.DATABASE_MAX_OVERFLOW,
        ge=0,
        validation_alias=AliasChoices("DATABASE_MAX_OVERFLOW", "database_max_overflow"),
    )

    redis_url: str | None = Field(
        default=constants.REDIS_URL,
        validation_alias=AliasChoices("REDIS_URL", "redis_url"),
    )

    jwt_secret_key: SecretStr | None = Field(
        default=SecretStr(constants.JWT_SECRET_KEY) if constants.JWT_SECRET_KEY else None,
        min_length=32,
        validation_alias=AliasChoices("JWT_SECRET_KEY", "jwt_secret_key"),
    )
    jwt_private_key: SecretStr | None = Field(
        default=SecretStr(constants.JWT_PRIVATE_KEY) if constants.JWT_PRIVATE_KEY else None,
        validation_alias=AliasChoices("JWT_PRIVATE_KEY", "jwt_private_key"),
    )
    jwt_public_key: str | None = Field(
        default=constants.JWT_PUBLIC_KEY,
        validation_alias=AliasChoices("JWT_PUBLIC_KEY", "jwt_public_key"),
    )
    jwt_algorithm: JwtAlgorithm = Field(
        default=constants.JWT_ALGORITHM,
        validation_alias=AliasChoices("JWT_ALGORITHM", "jwt_algorithm"),
    )
    jwt_access_token_expire_minutes: int = Field(
        default=constants.JWT_ACCESS_TOKEN_EXPIRE_MINUTES,
        gt=0,
        validation_alias=AliasChoices(
            "JWT_ACCESS_TOKEN_EXPIRE_MINUTES",
            "jwt_access_token_expire_minutes",
        ),
    )
    jwt_refresh_token_expire_days: int = Field(
        default=constants.JWT_REFRESH_TOKEN_EXPIRE_DAYS,
        gt=0,
        validation_alias=AliasChoices(
            "JWT_REFRESH_TOKEN_EXPIRE_DAYS",
            "jwt_refresh_token_expire_days",
        ),
    )
    jwt_issuer: str = Field(
        default=constants.JWT_ISSUER,
        min_length=1,
        validation_alias=AliasChoices("JWT_ISSUER", "jwt_issuer"),
    )
    jwt_audience: str = Field(
        default=constants.JWT_AUDIENCE,
        min_length=1,
        validation_alias=AliasChoices("JWT_AUDIENCE", "jwt_audience"),
    )
    refresh_token_pepper: SecretStr | None = Field(
        default=SecretStr(constants.REFRESH_TOKEN_PEPPER),
        min_length=32,
        validation_alias=AliasChoices("REFRESH_TOKEN_PEPPER", "refresh_token_pepper"),
    )

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: object) -> list[str]:
        """Chuẩn hóa CORS origins trước khi Pydantic kiểm tra trường.

        None thành danh sách rỗng; chuỗi được tách theo dấu phẩy, rồi bỏ khoảng
        trắng và phần tử rỗng. Kiểu đầu vào khác bị từ chối bằng ValueError.
        """

        if value is None:
            return []
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        if isinstance(value, list):
            return [str(origin).strip() for origin in value if str(origin).strip()]
        raise ValueError("CORS_ORIGINS must be a string or list.")

    @field_validator("db_schema")
    @classmethod
    def validate_db_schema(cls, value: str) -> str:
        """Loại khoảng trắng ở hai đầu tên schema rồi chỉ chấp nhận chữ, số và dấu gạch dưới. Tên
        chứa ký tự khác bị từ chối để không đưa giá trị schema không an toàn vào cấu hình."""

        normalized = value.strip()
        if not normalized.replace("_", "").isalnum():
            raise ValueError("DB_SCHEMA contains unsupported characters.")
        return normalized

    @model_validator(mode="after")
    def validate_jwt_key_configuration(self) -> Settings:
        """Kiểm tra cấu hình khóa phù hợp với thuật toán JWT đã chọn: HS256 cần secret key, còn
        ES256 cần cả private key và public key. Trả lại chính Settings khi hợp lệ; thiếu khóa
            bắt buộc sẽ phát sinh ValueError."""

        if self.jwt_algorithm == "HS256" and self.jwt_secret_key is None:
            raise ValueError("HS256 requires a JWT secret key.")
        if self.jwt_algorithm == "ES256":
            if self.jwt_private_key is None:
                raise ValueError("ES256 requires a JWT private key.")
            if self.jwt_public_key is None:
                raise ValueError("ES256 requires a JWT public key.")
        return self

    # Bí danh tương thích với API cấu hình viết hoa trước đây.
    @property
    def DB_HOST(self) -> str | None:
        """Cung cấp bí danh viết hoa tương thích ngược cho trường db_host. Giá trị trả về là host
        cũ nếu được cấu hình, nếu không thì là None."""
        return self.db_host

    @property
    def DB_PORT(self) -> int | None:
        """Cung cấp bí danh viết hoa tương thích ngược cho trường db_port. Giá trị trả về là cổng
        cũ nếu được cấu hình, nếu không thì là None."""
        return self.db_port

    @property
    def DB_NAME(self) -> str | None:
        """Cung cấp bí danh viết hoa tương thích ngược cho trường db_name. Giá trị trả về là tên
        database cũ nếu được cấu hình, nếu không thì là None."""
        return self.db_name

    @property
    def DB_USER(self) -> str | None:
        """Cung cấp bí danh viết hoa tương thích ngược cho trường db_user. Giá trị trả về là tên
        user cũ nếu được cấu hình, nếu không thì là None."""
        return self.db_user

    @property
    def DB_PASSWORD(self) -> str | None:
        """Cung cấp bí danh viết hoa cho mật khẩu database cũ. Nếu có SecretStr, hàm trả về giá trị
        bí mật đã mở; nếu chưa cấu hình thì trả về None."""
        return self.db_password.get_secret_value() if self.db_password else None

    @property
    def DB_SCHEMA(self) -> str:
        """Cung cấp bí danh viết hoa cho db_schema và trả về tên schema đã được
        Settings chuẩn hóa."""
        return self.db_schema

    @property
    def URL_DATABASE(self) -> str:
        """Cung cấp bí danh URL_DATABASE cũ bằng cách mở SecretStr của database_url để các caller
        tương thích đọc được chuỗi kết nối."""
        return self.database_url.get_secret_value()

    @property
    def JWT_SECRET_KEY(self) -> SecretStr | None:
        """Cung cấp bí danh viết hoa cho jwt_secret_key và giữ nguyên kiểu SecretStr để caller
        không vô tình đọc secret dưới dạng văn bản."""
        return self.jwt_secret_key

    @property
    def JWT_ALGORITHM(self) -> JwtAlgorithm:
        """Cung cấp bí danh viết hoa cho jwt_algorithm và trả về thuật toán JWT đã được kiểm tra
        kiểu."""
        return self.jwt_algorithm

    @property
    def JWT_ACCESS_TOKEN_EXPIRE_MINUTES(self) -> int:
        """Cung cấp bí danh viết hoa cho thời hạn access token tính bằng phút."""
        return self.jwt_access_token_expire_minutes

    @property
    def JWT_REFRESH_TOKEN_EXPIRE_DAYS(self) -> int:
        """Cung cấp bí danh viết hoa cho thời hạn refresh token tính bằng ngày."""
        return self.jwt_refresh_token_expire_days

    @property
    def JWT_ISSUER(self) -> str:
        """Cung cấp bí danh viết hoa cho issuer được ghi vào và kiểm tra trong JWT."""
        return self.jwt_issuer


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Tạo Settings từ app.core.constants và cache một instance trong tiến trình bằng lru_cache.
    Các lần gọi sau dùng lại instance đó thay vì xác thực lại cấu hình."""

    return Settings()


class _LazySettings:
    """Proxy tương thích với API settings cũ. Đối tượng chỉ tạo và kiểm tra Settings khi một thuộc
    tính được truy cập, nhờ đó việc import module chưa kích hoạt quá trình xác thực cấu hình."""

    def __getattr__(self, name: str) -> object:
        """Ủy quyền việc đọc thuộc tính chưa định nghĩa cho Settings được tạo bởi get_settings. Lần
        truy cập đầu tiên có thể kích hoạt khởi tạo và xác thực cấu hình."""
        return getattr(get_settings(), name)

    def __repr__(self) -> str:
        """Trả về nhãn biểu diễn ổn định cho proxy settings trì hoãn, không khởi tạo Settings hay
        đọc giá trị bí mật."""
        return "settings (lazy)"


settings = _LazySettings()
