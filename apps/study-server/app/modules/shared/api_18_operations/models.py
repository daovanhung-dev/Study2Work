from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class Operation(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: UUID
    kind: str
    status: str
    owner_id: int
    submitted_at: datetime
    updated_at: datetime
    completed_at: datetime | None = None
    result: dict[str, object] | None = None
