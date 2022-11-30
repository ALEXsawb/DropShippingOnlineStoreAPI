from services.requests.requests_to_PrintfulAPI import set_order as set_order_request
from services.schemas.schemas import RecipientSchema, ItemOrderSchema


async def set_order(recipient: RecipientSchema, items: list[ItemOrderSchema]):
    data = {
        "recipient": recipient if isinstance(recipient, dict) else recipient.dict(),
        "items": items if isinstance(items[0], dict) else [item.dict() for item in items]
    }
    return await set_order_request(data=data)
