from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from services.db.queries import get_pending_order
from services.schemas.schemas import ItemOrderSchema, RecipientSchema
from StoreAPI.orders.set_order import set_order as set_order_function

orders_router = APIRouter()


@orders_router.post('/orders')
async def set_order(items: list[ItemOrderSchema], recipient: RecipientSchema):
    order_data = await set_order_function(recipient, items)
    pending_order = await get_pending_order()
    if pending_order:
        pending_order.pop('date')
        await set_order_function(items=pending_order.pop('items'), recipient=pending_order)
    return jsonable_encoder(order_data)
