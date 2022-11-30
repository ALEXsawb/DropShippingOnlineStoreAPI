import pytest
from aredis_om import NotFoundError

from services.db.models import ProductModel
from services.schemas.schemas import ProductSchemas


@pytest.mark.asyncio
async def test_product(async_app_client, global_product_id, store_product_id):
    try:
        await ProductModel.get(f'{global_product_id} - {store_product_id}')
        raise ValueError('This product don`t must be in bd before request')
    except NotFoundError:
        pass

    response = await async_app_client.get(f'/product/{global_product_id}-{store_product_id}')

    assert response.status_code == 200
    assert ProductSchemas(**response.json())

    this_product_in_bd = await ProductModel.get(f'{global_product_id}-{store_product_id}')
    assert this_product_in_bd
    assert await this_product_in_bd.ttl() <= 60
    await ProductModel.delete(this_product_in_bd)


@pytest.mark.asyncio
async def test_product_with_invalid_ids(async_app_client):
    response = await async_app_client.get(f'/product/{1232131321312}-{734573315463744}')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}

