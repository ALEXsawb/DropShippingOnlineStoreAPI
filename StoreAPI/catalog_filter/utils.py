import asyncio
import math
import re

from StoreAPI.utils import append_product_to_catalog
from services.db.models import ProductModel
from services.requests.request_utils import get_store_products_data_by_specified_store_products
from services.requests.requests_to_PrintfulAPI import get_specified_amount_of_store_products
from services.requests.request_utils import actualization_and_supplementing_catalog_products_data as \
                                            actualization_and_supplementing_data_of_specified_products
from services.schemas.classes.Product import Product


async def add_store_id_on_hundreds_of_other_products(total_products: int, products_from_response: list):
    count_next_hundreds = math.ceil(total_products / 100) - 1
    queue = asyncio.Queue()
    tasks = []
    for hundreds_number in range(1, count_next_hundreds + 1):
        task = asyncio.create_task(get_specified_amount_of_store_products(offset=hundreds_number*100, amount=100))
        tasks.append(task)
    await queue.join()
    await asyncio.gather(*tasks, return_exceptions=True)
    for task in tasks:
        products_from_response += task.result()['result']


async def add_products_to_bd_using_data_product_from_store(store_products: list[dict]):
    store_products = await get_store_products_data_by_specified_store_products(store_products)
    products = []
    global_products_id = set()
    for product in store_products:
        product = Product(product)
        products.append(product)
        global_products_id.add(product.global_id)
    await actualization_and_supplementing_data_of_specified_products(global_products_id, products)
    for product in products:
        saved_product = await ProductModel(**product.prepare_for_db_entry().to_json()).save()
        await saved_product.expire(60)


def get_products_outside_db(funk):
    async def wrapper(products_or_products_ids: list[dict | list[int]]):
        products_who_not_in_bd = []
        keys = await ProductModel.db().keys()
        for product_or_product_id in products_or_products_ids:
            funk(keys, products_who_not_in_bd, product_or_product_id)

        return products_who_not_in_bd
    return wrapper


def add_product_missing_in_keys_of_database_to_specified_list(keys: list, products_who_not_in_bd: list, product: dict):
    may_be_key = re.compile(ProductModel.get_united_prefix() + rf'\d*-{product["id"]}')
    if not list(filter(may_be_key.match, keys)):
        products_who_not_in_bd.append(product)


@get_products_outside_db
def get_products_outside_db_using_ids_from_db(keys, products_who_not_in_bd, product_id):
    add_product_missing_in_keys_of_database_to_specified_list(keys, products_who_not_in_bd, product={'id': product_id})


@get_products_outside_db
def get_products_outside_db_using_store_products(keys, products_who_not_in_bd, store_product):
    if not store_product['is_ignored']:
        add_product_missing_in_keys_of_database_to_specified_list(keys, products_who_not_in_bd, store_product)


async def get_filtered_catalog(request, **queries):
    filtered_catalog = []
    for find_product in await ProductModel.find_by_data_of_filters(**queries).all():
        await append_product_to_catalog(filtered_catalog, request, find_product)
    return filtered_catalog


async def get_products_outside_db_using_requests():
    response_by_one_hundred_products = await get_specified_amount_of_store_products(offset=0, amount=100)
    products_from_response = response_by_one_hundred_products['result']
    total_products = response_by_one_hundred_products['paging']['total']
    if total_products > 100:
        await add_store_id_on_hundreds_of_other_products(total_products, products_from_response)

    return await get_products_outside_db_using_store_products(products_from_response)


def get_only_completed_fields(entry_data: dict) -> dict:
    entry_data.pop('request')
    [entry_data.pop(key) if value is None else None for key, value in entry_data.copy().items()]
    return entry_data