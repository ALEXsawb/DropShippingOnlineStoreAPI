from random import choice

import pytest

from StoreAPI.catalog.get_catalog import get_catalog
from main import app
from services.db.models import ProductModel
from tests.conftest import variables_for_test


class PseudoRequest:
    @staticmethod
    def url_for(name, **kwargs):
        url_path = app.router.url_path_for(name, **kwargs)
        return url_path.make_absolute_url(base_url='http://127.0.0.1:8000')


async def get_product_keys_with_ttl_more_specified_number(number):
    product_keys = []
    for key in await ProductModel.db().keys():
        if 'index:hash' not in key and 'OnlineStoreFastAPI:Product:' in key:
            product = await ProductModel.get(key.split(':')[-1])
            if await product.ttl() >= number:
                product_keys.append(key)
    return product_keys


@pytest.fixture
@pytest.mark.asyncio
async def catalog_data_without_cached_product_data():
    for key in await ProductModel.db().keys():
        if 'index:hash' not in key:
            await ProductModel.db().delete(key)
    return await get_catalog(page=variables_for_test['page_number'], request=PseudoRequest())


@pytest.fixture
@pytest.mark.asyncio
async def catalog_data_with_all_cached_product_data():
    product_keys = await get_product_keys_with_ttl_more_specified_number(10)
    catalog = await get_catalog(page=variables_for_test['page_number'], request=PseudoRequest())
    if len(catalog) == len(product_keys):
        return catalog
    else:
        return await get_catalog(page=variables_for_test['page_number'], request=PseudoRequest())


@pytest.fixture
@pytest.mark.asyncio
async def catalog_data_with_some_cached_product_data():
    product_keys = await get_product_keys_with_ttl_more_specified_number(20)
    for i in range(len(product_keys)//2):
        await ProductModel.db().delete(choice(product_keys))
    return await get_catalog(page=variables_for_test['page_number'], request=PseudoRequest())
