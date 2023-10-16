from enum import Enum

"""
    create constants here to be used later
"""

PSQL_USER_DB = "user_db"
phone_regex = r"^(0\d{10}|[1-9]\d{9,11})$"
email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"


class ResponseKeys:
    DATA = "data"
    SUCCESS = "success"
    MESSAGE = "message"
    ERROR = "error"


class Tables(Enum):
    ORDERS = {
        "name": "orders",
        "columns": ["order_id", "user_id", "restaurant_id", "order_date", "total_amount", "status"],
    }
    ORDER_ITEMS = {
        "name": "ordered_items",
        "columns": ["order_item_id", "restaurant_item_id", "order_id", "quantity", "subtotal"],
    }


class Roles(Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"
    RESTATURANT = "restaurant"
    DELIVERY_PERSONNEL = "delivery_personnel"


class OrderStatus(Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    CANCELLED = "cancelled"
    DELIVERED = "delivered"
