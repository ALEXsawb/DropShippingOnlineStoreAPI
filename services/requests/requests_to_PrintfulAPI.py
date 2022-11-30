from fastapi.exceptions import HTTPException
from httpx import AsyncClient

import json

from .headers import headers
from services.db.models import OrderModel


def async_requests(funk):
    async def wrapper(*args, **kwargs):
        async with AsyncClient() as client:
            response = await funk(client=client, *args, **kwargs)
            if response.status_code == 200:
                return response.json()['result']
            else:
                if response.status_code == 429 and response.request.url == 'https://api.printful.com/orders':
                    await OrderModel(**kwargs['data'].pop('recipient'), **kwargs['data']).save()
                raise HTTPException(status_code=response.status_code, detail=response.json()['result'])
    return wrapper


@async_requests
async def get_global_product_data(global_product_id: str | int, client: AsyncClient) -> dict[str, dict | list]:
    return await client.get(f'https://api.printful.com/products/{global_product_id}', headers=headers)


@async_requests
async def get_store_product_data(product_id: int | str, client: AsyncClient) -> dict[str, dict | list]:
    return await client.get(f'https://api.printful.com/store/products/{product_id}', headers=headers)


@async_requests
async def get_store_products_by_page(client: AsyncClient, page: int) -> dict[str, dict | list]:
    offset = (page - 1) * 12 if page > 1 else 0
    return await client.get(f'https://api.printful.com/store/products?offset={offset}&limit=12', headers=headers)


@async_requests
async def set_order(client: AsyncClient, data: dict) -> dict[str, dict | list]:
    return await client.post('https://api.printful.com/orders', data=json.dumps(data), headers=headers)


async def get_specified_amount_of_store_products(offset: int, amount: int):
    async with AsyncClient() as client:
        response = await client.get(f'https://api.printful.com/store/products?offset={offset}&limit={amount}',
                                    headers=headers)
        if 200 <= response.status_code < 300:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json()['result'])
