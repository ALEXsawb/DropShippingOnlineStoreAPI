import pytest

import pytest_asyncio

from services.requests.requests_to_PrintfulAPI import get_specified_amount_of_store_products, \
    get_store_products_by_page, get_store_product_data, get_global_product_data, set_order
from tests.conftest import variables_for_test


@pytest_asyncio.fixture(scope="session")
async def response_by_first_ten_products():
    offset = 0
    limit = 10
    return await get_specified_amount_of_store_products(offset=offset, amount=limit)


@pytest_asyncio.fixture(scope="session")
async def get_response_by_specified_in_env_page_number():
    return await get_store_products_by_page(page=variables_for_test['page_number'])


@pytest_asyncio.fixture(scope="session")
async def response_store_product_data():
    return await get_store_product_data(variables_for_test['store_product_id'])


@pytest_asyncio.fixture(scope="session")
async def response_global_product_data():
    return await get_global_product_data(variables_for_test['global_product_id'])
