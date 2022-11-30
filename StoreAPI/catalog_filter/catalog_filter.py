from fastapi import Request, HTTPException, APIRouter, Query

from services.db.queries import get_all_products_ids, set_all_products_ids
from services.schemas.schemas import CatalogProductSchema
from .utils import get_only_completed_fields, get_products_outside_db_using_ids_from_db, \
    get_products_outside_db_using_requests, add_products_to_bd_using_data_product_from_store, get_filtered_catalog

catalog_filter_router = APIRouter()


@catalog_filter_router.get('/catalog/filter', response_model=list[CatalogProductSchema])
async def catalog_filtered(request: Request,
                           colors: list[str | int] = Query(None, min_length=3,
                                                           description=('List of desired products colors. '
                                                                        'You can give colors name or cod or mixed'
                                                                        'If you use code which contain something other'
                                                                        'that number then you must be use # before code'
                                                                        )),
                           sizes: list[str | int] = Query(None, description='List of desired products sizes'),
                           min_price: float = Query(None, description='Min product price for search'),
                           max_price: float = Query(None, description='Max product price for search')):
    kwargs = get_only_completed_fields(locals().copy())
    all_products_ids = await get_all_products_ids()
    if all_products_ids:
        products_who_not_in_bd = await get_products_outside_db_using_ids_from_db(all_products_ids)
    else:
        products_who_not_in_bd = await get_products_outside_db_using_requests()
        await set_all_products_ids([product['id'] for product in products_who_not_in_bd])

    if products_who_not_in_bd:
        await add_products_to_bd_using_data_product_from_store(products_who_not_in_bd)

    filtered_catalog = await get_filtered_catalog(request, **kwargs)
    if filtered_catalog:
        return filtered_catalog
    raise HTTPException(status_code=400, detail=("We couldn't find products with specified filters. "
                                                 "You can make filters more softly."))
