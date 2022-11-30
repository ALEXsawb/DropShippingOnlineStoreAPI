import json
import pytest
import requests

from services.requests.headers import headers


@pytest.mark.asyncio
async def test_set_order(async_app_client, data_of_set_order):
    response = await async_app_client.post(f'/orders', data=json.dumps(data_of_set_order))
    assert response.status_code == 200
    order_id = json.loads(response.content)['id']
    store_header = headers
    response = requests.delete(f'https://api.printful.com/orders/{order_id}', headers=store_header)
    assert response.status_code == 200
