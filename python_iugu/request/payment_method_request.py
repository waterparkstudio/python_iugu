from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass
class PaymentMethodRequest:
    customer_id: Optional[str] = None
    description: Optional[str] = None
    token: Optional[str] = None
    set_as_default: Optional[bool] = None