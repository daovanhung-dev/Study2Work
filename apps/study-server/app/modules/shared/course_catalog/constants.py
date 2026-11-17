from __future__ import annotations

DEFAULT_PAGE = 1
DEFAULT_SIZE = 20
MAX_SIZE = 100
SORT_FIELDS = frozenset({"id", "name", "price", "created_at"})
SORT_DIRECTIONS = frozenset({"asc", "desc"})
SORT_COLUMNS = {
    "id": "c.id",
    "name": "c.name",
    "price": "c.price",
    "created_at": "c.created_at",
}
