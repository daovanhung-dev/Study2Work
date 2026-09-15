from __future__ import annotations

from app.services.catalog import _rows
from sqlalchemy import create_engine


def test_rows_converts_sqlalchemy_mapping_rows_to_dicts() -> None:
    engine = create_engine("sqlite://")

    with engine.connect() as connection:
        assert _rows(connection, "SELECT 1 AS name") == [{"name": 1}]
