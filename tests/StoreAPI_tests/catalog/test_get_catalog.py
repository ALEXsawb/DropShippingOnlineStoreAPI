import pytest

from services.schemas.schemas import CatalogProductSchema

page_number = 1


@pytest.mark.asyncio
async def test_get_catalog(catalog_data_without_cached_product_data, catalog_data_with_all_cached_product_data,
                           catalog_data_with_some_cached_product_data):
    for catalog_name, catalog in locals().items():
        catalog = await catalog
        assert isinstance(catalog, list)
        for product_data in catalog:
            assert CatalogProductSchema(**product_data)
