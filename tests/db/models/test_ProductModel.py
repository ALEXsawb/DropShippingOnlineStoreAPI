import pytest
from pydantic import AnyUrl

from services.db.models import *
from services.schemas.schemas import ColorSchemas


def test_fields():
    fields = ProductModel.__fields__
    assert fields['global_id'].annotation == int
    assert fields['store_id'].annotation == int
    assert fields['category_id'].annotation == int
    assert fields['name'].annotation == str
    assert fields['min_price'].annotation == float
    assert fields['max_price'].annotation == float
    assert fields['colors'].annotation == list[ColorModel]
    assert fields['sizes'].annotation == list[str]
    assert fields['image'].annotation == AnyUrl
    assert fields['published'].annotation == bool
    assert fields['currency'].annotation == str
    assert fields['description'].annotation == Optional[str]
    assert fields['available_colors_by_sizes_with_sync_variant_id'].annotation == dict[str,
                                                                                       list[tuple[ColorSchemas,
                                                                                                  int, str,
                                                                                                  AnyUrl]]]


@pytest.mark.asyncio
async def test_key(get_product):
    product = await get_product
    assert product.key() == f'OnlineStoreFastAPI:Product:{product.global_id}-{product.store_id}'


@pytest.mark.asyncio
async def test_expire_and_ttl(get_product):
    product = await get_product
    await product.expire(3)
    assert await product.ttl() == 3


def test_global_key_prefix():
    assert ProductModel._meta.global_key_prefix == 'OnlineStoreFastAPI'


def test_model_key_prefix():
    assert ProductModel._meta.model_key_prefix == 'Product'
