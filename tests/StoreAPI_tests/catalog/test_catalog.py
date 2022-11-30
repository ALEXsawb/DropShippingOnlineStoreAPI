import random

import pytest

from services.db.models import ProductModel, CatalogPageModel
from services.schemas.schemas import CatalogProductSchema


@pytest.mark.asyncio
async def test_catalog(async_app_client, delete_all_changes_in_bd):
    await delete_all_changes_in_bd
    all_products_data_in_bd_before_request = await ProductModel.find().all()
    response = await async_app_client.get('/catalog?=page=1')

    all_products_data_in_bd_after_request = await ProductModel.find().all()
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert CatalogProductSchema(**response.json()[0])
    assert len(all_products_data_in_bd_before_request) < len(all_products_data_in_bd_after_request)

    cached_important_data_about_store_products_catalog_page = await CatalogPageModel.find(CatalogPageModel.page == 1
                                                                                          ).first()
    assert cached_important_data_about_store_products_catalog_page
    assert len(all_products_data_in_bd_after_request) == \
           len(cached_important_data_about_store_products_catalog_page.store_products_id)
    assert random.choice(await ProductModel.find().all())


@pytest.mark.asyncio
async def test_catalog_with_invalid_page_number(async_app_client):
    response = await async_app_client.get('/catalog?page=200')
    assert response.status_code == 404
    assert response.json() == {'detail': "The catalog hasn't that specified page number"}
