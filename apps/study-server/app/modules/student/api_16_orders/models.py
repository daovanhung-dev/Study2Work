from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict


class CreateOrderRequest(BaseModel):
    course_id: int
    payment_provider: str


class Order(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: int
    course_id: int
    user_id: int
    amount: Decimal
    currency: Literal["VND"]
    status: str
    created_at: datetime
