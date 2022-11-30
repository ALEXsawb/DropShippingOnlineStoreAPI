from fastapi import Request

from services.db.models import ProductModel
from services.schemas.classes.Product import Product


def get_product_url(request, product_data: ProductModel | Product) -> str:
    return request.url_for('product', global_id=product_data.global_id, store_id=product_data.store_id)


async def append_product_to_catalog(catalog: list, request: Request, saved_product_or_from_db: ProductModel):
    product_data = saved_product_or_from_db.dict()
    product_data['url'] = get_product_url(request, saved_product_or_from_db)
    catalog.append(product_data)
