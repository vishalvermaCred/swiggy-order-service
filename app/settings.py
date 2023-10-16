from os import getenv

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

ENV = getenv("ENV", "")
SERVICE_NAME = getenv("SERVICE_NAME", "")
APP_NAME = getenv("APP_NAME", "Order Service")

BASE_ROUTE = getenv("BASE_ROUTE")
LOG_LEVEL = getenv("LOG_LEVEL", "INFO")

ORDER_DB_CONFIGS = {
    "HOST": getenv("DB_HOST"),
    "PORT": getenv("DB_PORT"),
    "NAME": getenv(f"ORDER_DB_NAME"),
    "PASSWORD": getenv("ORDER_DB_PASSWORD"),
    "USER": getenv("ORDER_DB_USER"),
}

KAFKA_BOOTSTRAP_SERVERS = getenv("KAFKA_BOOTSTRAP_SERVERS")
KAFKA_PRODUCER_CLIENT_ID = getenv("KAFKA_PRODUCER_CLIENT_ID")
RESTATURANT_EVENT_TOPIC = getenv("RESTATURANT_EVENT_TOPIC")
DELIVERY_EVENT_TOPIC = getenv("DELIVERY_EVENT_TOPIC")

INVENTORY_SERVICE_BASE_URL = getenv("INVENTORY_SERVICE_BASE_URL")
USER_SERVICE_BASE_URL = getenv("USER_SERVICE_BASE_URL")
