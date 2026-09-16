from unittest.mock import Mock

import pytest
from scripts.bootstrap_access import (
    _allow_schema_ownership,
    _update_developer_password,
    _validate_password,
)


def _result(*, mapping=None, scalar=None, rowcount=1) -> Mock:
    result = Mock()
    result.mappings.return_value.one_or_none.return_value = mapping
    result.scalar_one_or_none.return_value = scalar
    result.rowcount = rowcount
    return result


def test_bootstrap_enables_set_role_for_schema_ownership() -> None:
    connection = Mock()

    _allow_schema_ownership(connection, '"study_dev"')

    statement = connection.execute.call_args.args[0]
    assert str(statement) == 'GRANT "study_dev" TO CURRENT_USER WITH SET TRUE'


@pytest.mark.parametrize("password", ["short", "x" * 257, "valid\x00password"])
def test_developer_password_validation(password: str) -> None:
    with pytest.raises(ValueError):
        _validate_password(password, "Developer password")


def test_developer_password_updates_only_bound_target() -> None:
    connection = Mock()
    connection.execute.side_effect = [
        _result(scalar="db_admin.admin_users"),
        _result(
            mapping={
                "user_id": "10000000-0000-0000-0000-000000000002",
                "is_root": False,
                "status": "active",
            }
        ),
        _result(
            mapping={
                "rolcanlogin": True,
                "rolsuper": False,
                "rolcreatedb": False,
                "rolcreaterole": False,
                "rolinherit": False,
                "owns_schema": True,
            }
        ),
        _result(scalar=1),
        _result(rowcount=1),
        _result(),
    ]

    _update_developer_password(
        connection,
        "study_server",
        "valid-developer-password",
        "argon2id-hash",
    )

    statements = [str(call.args[0]) for call in connection.execute.call_args_list]
    assert any("database_target = :database_target" in statement for statement in statements)
    assert any('ALTER ROLE "study_dev" PASSWORD' in statement for statement in statements)
    assert not any('ALTER ROLE "work_dev"' in statement for statement in statements)
    update_call = connection.execute.call_args_list[-2]
    assert update_call.args[1]["password_hash"] == "argon2id-hash"
