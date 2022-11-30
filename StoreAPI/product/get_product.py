from services.db.models import ProductModel
from services.db.queries import get_product_by_key
from services.requests.request_utils import get_store_product


async def get_product(global_id: int = None, store_id: int = None) -> ProductModel:
    product_from_db = await get_product_by_key(f'{global_id}-{store_id}')
    if product_from_db:
        return product_from_db.dict()

    product_from_request = await get_store_product(global_id, store_id)
    saved_product_data = await ProductModel(**product_from_request.prepare_for_db_entry().to_json()).save()
    return saved_product_data.dict()
