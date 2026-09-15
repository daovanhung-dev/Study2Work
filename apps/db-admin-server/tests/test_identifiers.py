from __future__ import annotations

import pytest
from app.core.responses import ApiError
from app.services.identifiers import qualified_name, quote_identifier


@pytest.mark.parametrize("value", ["users; DROP TABLE users", '"users"', "", "1users", "pg\nusers"])
def test_identifier_injection_is_rejected(value: str) -> None:
    with pytest.raises(ApiError) as error:
        quote_identifier(value, "name", "trace")
    assert error.value.business_code == "DB_ADMIN_INVALID_IDENTIFIER"


def test_valid_qualified_name_is_quoted() -> None:
    assert qualified_name("public", "users", "trace") == '"public"."users"'
