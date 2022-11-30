import asyncio
import os

import pytest
import pytest_asyncio
from aredis_om import get_redis_connection, Migrator
from decouple import config
from httpx import AsyncClient

from main import app
from services.db.models import ProductModel
from services.requests.requests_to_PrintfulAPI import set_order

variables_for_test = {
    'invalid_filters': os.environ.get('INVALID_FILTERS', config('INVALID_FILTERS', default='colors=["blacksdsadwsaw"]')),
    'global_product_id': int(os.environ.get('GLOBAL_PRODUCT_ID', config('GLOBAL_PRODUCT_ID', default=515))),
    'store_product_id': int(os.environ.get('STORE_PRODUCT_ID', config('STORE_PRODUCT_ID', default=286167527))),
    'page_number': int(os.environ.get('PAGE_NUMBER', config('PAGE_NUMBER', default=1))),
    'sync_variant_id': int(os.environ.get('SYNC_VARIANT_ID', config('SYNC_VARIANT_ID', default=3505521038))),
}


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def redis():
    yield get_redis_connection()


@pytest.fixture(scope="session")
def data_of_set_order():
    return get_data_for_set_order()


@pytest.mark.asyncio
@pytest.fixture()
async def delete_all_changes_in_bd():
    """This fixture deletes all data in bd then make migration"""
    await ProductModel.db().flushall()
    await Migrator().run()


@pytest_asyncio.fixture
async def async_app_client():
    async with AsyncClient(app=app, base_url='http://test') as client:
        yield client


def get_data_for_set_order():
    data = {
        "items": [
            {
                "sync_variant_id": variables_for_test['sync_variant_id'],
                "quantity": 5
            }
        ],
        "recipient": {
            "name": "string",
            "address1": "string",
            "city": "string",
            "country_code": "IT",
            "country_name": "Italy",
            "zip": "20199",
            "email": "sawv@gmail.com"
        }
    }
    return data


@pytest.fixture
def invalid_filters():
    return variables_for_test['invalid_filters']


@pytest.fixture
def global_product_id():
    return variables_for_test['global_product_id']


@pytest.fixture
def page_number():
    return variables_for_test['page_number']


@pytest.fixture
def sync_variant_id():
    return variables_for_test['sync_variant_id']


@pytest.fixture
def store_product_id():
    return variables_for_test['store_product_id']


@pytest_asyncio.fixture(scope="session")
async def response_set_order():
    return await set_order(data=get_data_for_set_order())
