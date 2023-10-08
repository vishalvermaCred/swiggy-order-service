from typing import Optional, List
from pydantic.fields import Field
from pydantic import BaseModel, Extra
from pydantic.class_validators import validator

from app.constants import OrderStatus


class OrderBaseModel(BaseModel):
    class Config:
        use_enum_values = True  # Uses Enum Values
        extra = Extra.ignore  # Ignores Extra Values
        str_strip_whitespace = True  # Removes Whitespaces


class PlaceOrder(OrderBaseModel):
    user_id: str = Field(...)
    restaurant_id: str = Field(...)
    order_date: str = Field(...)
    status: OrderStatus = "Pending"
    total_amount: float = Field(...)
    order_items: List = Field(...)

    @validator("order_items")
    def validate_order_items(cls, value):
        for items in value:
            for key, val in items.items():
                if key not in ["restaurant_item_id", "order_id", "quantity", "subtotal"]:
                    raise ValueError(f"all order items are not provided")
        return value


class UpdateMenu(OrderBaseModel):
    item_id: str = Field(...)
    restaurant_id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    price: float = Field(None)
    ordered_quantity: int = 0
    restock_quantity: int = 0
    is_available: bool = False
