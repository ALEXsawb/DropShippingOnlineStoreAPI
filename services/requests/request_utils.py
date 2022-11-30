import asyncio

from services.schemas.classes.Product import Product
from .requests_to_PrintfulAPI import get_store_product_data, get_global_product_data


def async_queue(funk):
    async def wrapper(*args, **kwargs):
        queue = asyncio.Queue()
        tasks = []
        result = await funk(tasks=tasks, *args, **kwargs)
        await queue.join()
        await asyncio.gather(*tasks, return_exceptions=True)
        if result:
            return result
        return [task.result() for task in tasks]
    return wrapper


@async_queue
async def get_store_products_data_by_specified_store_products(store_products: list[dict], tasks: list):
    for product in store_products:
        task = asyncio.create_task(get_store_product_data(product['id']))
        tasks.append(task)


@async_queue
async def actualization_and_supplementing_catalog_products_data(global_products_id: set[int],
                                                                products_this_page: list[Product], tasks: list):
    for global_product_id in global_products_id:
        task = asyncio.create_task(actualization_and_supplementing_products_data(global_product_id, products_this_page))
        tasks.append(task)


@async_queue
async def get_store_and_global_product_data(global_id: int, store_id: int, tasks: list):
    store_product_task = asyncio.create_task(get_store_product_data(store_id))
    global_product_task = asyncio.create_task(get_global_product_data(global_id))
    tasks.append(store_product_task)
    tasks.append(global_product_task)


async def get_store_product(global_id: int, store_id: int):
    store_product, global_product = await get_store_and_global_product_data(global_id, store_id)
    product = Product(store_product)
    actualization_and_supplementing_product_data(product, global_product)
    return product


async def actualization_and_supplementing_products_data(global_product_id: int | str,
                                                        products_this_page: list[Product]):
    global_product_with_him_variants = await get_global_product_data(global_product_id=global_product_id)
    global_product = global_product_with_him_variants['product']

    store_products_with_common_global_id = filter(lambda product: product.global_id == global_product['id'],
                                                  products_this_page)
    for store_product in store_products_with_common_global_id:
        actualization_and_supplementing_product_data(store_product, global_product_with_him_variants)


def actualization_and_supplementing_product_data(store_product: Product, global_product_with_him_variants: dict):
    for variant in store_product.variants.copy():
        for global_variant in global_product_with_him_variants['variants']:
            if global_variant['id'] == variant.global_id:
                if global_variant['in_stock']:
                    if variant.color.name:
                        variant.color.code = [global_variant['color_code'], ]
                        if global_variant['color_code2']:
                            variant.color.code.append(global_variant['color_code2'])
                else:
                    del store_product.variants[store_product.variants.index(variant)]
    store_product.colors = store_product.get_colors()
    store_product.sizes = store_product.get_sizes()
    store_product.available_colors_by_sizes_with_sync_variant_id = \
        store_product.get_available_colors_by_sizes_with_sync_variant_id()
