import json

from .models import ProductModel, OrderModel, CatalogPageModel
from aredis_om.model.model import NotFoundError
from services.db.db_conection import db as redis


def not_found(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except NotFoundError:
            return None
    return wrapper


@not_found
async def get_product_by_store_id_field(store_id: int) -> ProductModel:
    return await ProductModel.find(ProductModel.store_id == store_id).first()


@not_found
async def get_product_by_key(key: str):
    return await ProductModel.get(key)


@not_found
async def get_product_by_color_name(color: str):
    return await ProductModel.find(ProductModel.colors.name == color).all()


@not_found
async def get_pending_order() -> dict:
    pending_order = await OrderModel.find().first()
    return pending_order.dict()


@not_found
async def get_ids_store_products_by_catalog_page(page: int) -> list:
    catalog_page = await CatalogPageModel.find(CatalogPageModel.page == page).first()
    return [{'id': id_store_product} for id_store_product in catalog_page.store_products_id]


@not_found
async def set_all_products_ids(all_products_ids: list[int]):
    await redis.set(name='all_products_ids', value=json.dumps(all_products_ids))
    await redis.expire('all_products_ids', 60)


async def get_all_products_ids():
    all_products_ids = await redis.get(name='all_products_ids')
    if all_products_ids:
        return json.loads(all_products_ids)
