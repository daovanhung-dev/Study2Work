from __future__ import annotations

from app.core.security import _principal_from_claims, require_permission
from fastapi import HTTPException


def test_db_admin_role_expands_to_all_permissions() -> None:
    principal = _principal_from_claims({"sub": "operator", "roles": ["DB_ADMIN"]})

    assert principal.permissions == frozenset({"db_admin:read", "db_admin:write", "db_admin:sql"})


def test_permission_dependency_rejects_missing_permission() -> None:
    dependency = require_permission("db_admin:write")
    principal = _principal_from_claims({"sub": "reader", "permissions": ["db_admin:read"]})

    try:
        dependency(principal)
    except HTTPException as error:
        assert error.status_code == 403
    else:
        raise AssertionError("Expected missing permission to be rejected")
