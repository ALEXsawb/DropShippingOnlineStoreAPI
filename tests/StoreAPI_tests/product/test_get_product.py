import pytest
from services.schemas.schemas import ProductSchemaForView


@pytest.mark.asyncio
async def test_get_product_without_cached_data(non_cached_product_data):
    assert ProductSchemaForView(** await non_cached_product_data)


@pytest.mark.asyncio
async def test_get_product_with_cached_data(cached_product_data):
    assert ProductSchemaForView(** await cached_product_data)
