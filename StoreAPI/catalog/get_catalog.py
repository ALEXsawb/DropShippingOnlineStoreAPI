from fastapi import Request

from StoreAPI.utils import append_product_to_catalog
from services.db.queries import get_product_by_store_id_field, get_ids_store_products_by_catalog_page
from services.requests.requests_to_PrintfulAPI import get_store_products_by_page
from services.requests.request_utils import actualization_and_supplementing_catalog_products_data, \
    get_store_products_data_by_specified_store_products
from services.schemas.classes.Product import Product
from services.db.models import ProductModel, CatalogPageModel


async def get_catalog(request: Request, page: int):
    catalog = []

    store_products = await get_ids_store_products_by_catalog_page(page)
    if not store_products:
        store_products = await get_store_products_by_page(page=page)
        await CatalogPageModel(store_products_id=[store_product['id'] for store_product in store_products],
                               page=page).save()

    for store_product in store_products.copy():
        product_from_db = await get_product_by_store_id_field(store_product['id'])
        if product_from_db:
            await append_product_to_catalog(catalog, request, product_from_db)
            store_products.remove(store_product)

    catalog_page_products = await get_store_products_data_by_specified_store_products(store_products)
    global_products_id = set()
    products_this_page = []
    for product in catalog_page_products:
        product = Product(product)
        products_this_page.append(product)
        global_products_id.add(product.global_id)

    await actualization_and_supplementing_catalog_products_data(global_products_id, products_this_page)
    for product in products_this_page:
        saved_product = await ProductModel(**product.prepare_for_db_entry().to_json()).save()
        await append_product_to_catalog(catalog, request, saved_product)
    return catalog
