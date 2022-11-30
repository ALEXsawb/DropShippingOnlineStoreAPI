from fastapi import APIRouter

from StoreAPI.product.get_product import get_product
from services.schemas.schemas import ProductSchemaForView, ProductSchemas

product_router = APIRouter()


@product_router.get('/product/{global_id}-{store_id}', response_model=ProductSchemaForView)
async def product(global_id: int, store_id: int) -> ProductSchemas:
    return await get_product(global_id, store_id)
