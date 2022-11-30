import pytest
from aredis_om import NotFoundError

from StoreAPI.product.get_product import get_product
from services.db.models import ProductModel
from tests.conftest import variables_for_test


async def get_product_by_key(global_product_id=variables_for_test["global_product_id"],
                             store_product_id=variables_for_test["store_product_id"]):
    return await ProductModel.get(f'OnlineStoreFastAPI:Product:{global_product_id}-{store_product_id}')


@pytest.fixture
@pytest.mark.asyncio
async def non_cached_product_data():
    try:
        await get_product_by_key().delete()
    finally:
        return await get_product(variables_for_test['global_product_id'], variables_for_test['store_product_id'])


@pytest.fixture
@pytest.mark.asyncio
async def cached_product_data():
    try:
        if await get_product_by_key().ttl() < 5:
            raise NotFoundError
    except NotFoundError:
        await get_product(variables_for_test['global_product_id'], variables_for_test['store_product_id'])
    finally:
        return await get_product(variables_for_test['global_product_id'], variables_for_test['store_product_id'])
