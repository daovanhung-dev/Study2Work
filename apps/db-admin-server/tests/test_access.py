from __future__ import annotations

from types import SimpleNamespace

import jwt
import pytest
from app.core.config import Settings
from app.core.responses import ApiError
from app.core.security import Principal, _decode_local_token
from app.services.access import AccessService
from app.services.audit import AuditStore
from pydantic import SecretStr


def _settings() -> Settings:
    return Settings(
        app_env="test",
        database_targets={
            "study_server": "postgresql://user:password@localhost/study",
            "work_server": "postgresql://user:password@localhost/work",
        },
        jwt_issuer="issuer",
        jwt_audience="audience",
        local_auth_enabled=True,
        local_jwt_secret=SecretStr("a" * 48),
    )


def test_local_token_restores_root_metadata_and_scope() -> None:
    settings = _settings()
    token = jwt.encode(
        {
            "sub": "user-id",
            "userId": "user-id",
            "username": "admin",
            "isRoot": True,
            "mustChangePassword": False,
            "permissions": ["db_admin:read", "db_admin:manage"],
            "targets": ["study_server", "work_server"],
            "schemaBindings": [],
            "iss": settings.jwt_issuer,
            "aud": settings.jwt_audience,
            "exp": 4_102_444_800,
        },
        settings.local_jwt_secret.get_secret_value(),
        algorithm="HS256",
    )

    principal = _decode_local_token(token, settings)

    assert principal is not None
    assert principal.is_root is True
    assert principal.user_id == "user-id"
    assert "db_admin:manage" in principal.permissions


def test_scoped_principal_cannot_select_another_target_or_schema() -> None:
    settings = _settings()
    service = AccessService(
        {"study_server": SimpleNamespace(), "work_server": SimpleNamespace()},  # type: ignore[arg-type]
        settings,
        AuditStore(50),
    )
    principal = Principal(
        subject="dev-id",
        permissions=frozenset({"db_admin:read", "db_admin:sql"}),
        roles=frozenset({"developer"}),
        claims={},
        user_id=None,
        username="study_dev",
        targets=frozenset({"study_server"}),
        schema_bindings=({"database": "study_server", "schema": "study_dev"},),
    )

    assert service.allowed_targets(principal) == {"study_server"}
    assert service.allowed_schema_names(principal, "study_server") == {"study_dev"}
    with pytest.raises(ApiError) as error:
        service.require_target(principal, "work_server", "trace")
    assert error.value.business_code == "DB_ADMIN_TARGET_FORBIDDEN"
    with pytest.raises(ApiError) as error:
        service.require_schema(principal, "study_server", "public", "trace")
    assert error.value.business_code == "DB_ADMIN_SCHEMA_FORBIDDEN"
