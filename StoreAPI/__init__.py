from fastapi import APIRouter

from .catalog.catalog import catalog_router
from .catalog_filter.catalog_filter import catalog_filter_router
from .orders.orders import orders_router
from .product.product import product_router


StoreAPI_router = APIRouter()
StoreAPI_router.include_router(catalog_router)
StoreAPI_router.include_router(catalog_filter_router)
StoreAPI_router.include_router(orders_router)
StoreAPI_router.include_router(product_router)
