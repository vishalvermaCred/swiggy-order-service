import aiohttp
from uuid import uuid4
from http import HTTPStatus
from fastapi.logger import logger

from app.context import app_context
from app.constants import Tables
from app.settings import INVENTORY_SERVICE_BASE_URL

LOGGER_KEY = "app.service"


async def update_inventory(kwargs):
    logger.info(f"{LOGGER_KEY}.update_inventory")
    try:
        url = f"{INVENTORY_SERVICE_BASE_URL.rstrip('/')}/menu"
        payload = {"item_id": kwargs.get("restaurant_item_id"), "ordered_quantity": kwargs.get("quantity")}
        logger.info(f"url: {url}, payload: {payload}")
        async with aiohttp.ClientSession() as client:
            response = await client.patch(
                url=url,
                json=payload,
            )
            logger.info(f"{LOGGER_KEY}.update_inventory.response.status_code: {response.status}")
            response_text = await response.text()
            logger.info(f"{LOGGER_KEY}.update_inventory.response_text: {response_text}")
            if response.status != HTTPStatus.OK.value:
                return {"success": False, "message": response_text, "code": HTTPStatus.FAILED_DEPENDENCY.value}
            return {"success": True, "message": "Inventory updated", "code": HTTPStatus.OK.value}
    except Exception as e:
        logger.error(f"{LOGGER_KEY}.update_inventory.exceptiopn: {str(e)}")
        return {"success": False, "message": str(e), "code": HTTPStatus.INTERNAL_SERVER_ERROR.value}


async def process_order_items(kwargs):
    logger.info(f"{LOGGER_KEY}.process_order_items")
    try:
        columns = ", ".join(Tables.ORDER_ITEMS.value["columns"])
        insert_query = f"INSERT INTO {Tables.ORDER_ITEMS.value['name']} ({columns}) VALUES "
        order_items = kwargs.get("order_items")
        order_id = kwargs.get("order_id")
        for item in order_items:
            order_item_id = uuid4().hex
            inventory_response = await update_inventory(item)
            if not inventory_response.get("success"):
                return inventory_response
            insert_query += f"('{order_item_id}','{item.get('restaurant_item_id')}', '{order_id}', {item.get('quantity')}, {item.get('subtotal')}), "
        insert_query = insert_query.strip(", ")
        insert_query += ";"
        insert_response = await app_context.db.execute_insert_or_update_query(insert_query)
        logger.info(f"insert_response: {insert_response}")
        return {"success": True, "message": "Item added in Menu successfully", "code": HTTPStatus.OK.value}
    except Exception as e:
        logger.error(f"{LOGGER_KEY}.process_order_items.exceptiopn: {str(e)}")
        return {"success": False, "message": str(e), "code": HTTPStatus.INTERNAL_SERVER_ERROR.value}


async def process_order(kwargs):
    logger.info(f"{LOGGER_KEY}.process_order")
    try:
        order_id = uuid4().hex
        columns = ", ".join(Tables.ORDERS.value["columns"])
        insert_query = f"INSERT INTO {Tables.ORDERS.value['name']} ({columns}) VALUES ('{order_id}', '{kwargs.get('user_id')}', '{kwargs.get('restaurant_id')}', '{kwargs.get('order_date')}', '{kwargs.get('total_amount')}', '{kwargs.get('status')}');"
        insert_response = await app_context.db.execute_insert_or_update_query(insert_query)
        logger.info(f"insert_response: {insert_response}")
        logger.info(f"{LOGGER_KEY}.process_order.order_id: {order_id}")

        kwargs["order_id"] = order_id
        order_items_response = await process_order_items(kwargs)
        logger.info(f"order_items_response: {order_items_response}")
        if not order_items_response.get("success"):
            return order_items_response
        return {"success": True, "message": "Item added in Menu successfully", "code": HTTPStatus.OK.value}
    except Exception as e:
        logger.error(f"{LOGGER_KEY}.process_order.exceptiopn: {str(e)}")
        return {"success": False, "message": str(e), "code": HTTPStatus.INTERNAL_SERVER_ERROR.value}
