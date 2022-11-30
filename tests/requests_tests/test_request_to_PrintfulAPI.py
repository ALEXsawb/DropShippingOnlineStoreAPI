import fastapi
import pytest

from services.requests.requests_to_PrintfulAPI import *

""""""


class TestGetGlobalProduct:

    def test_response_type(self, response_global_product_data):
        response = response_global_product_data
        assert isinstance(response, dict)

    def test_response_keys(self, response_global_product_data):
        response = response_global_product_data
        assert list(response.keys()) == ['product', 'variants']

    def test_product_from_response_has_important_keys(self, response_global_product_data):
        important_keys = ['id', ]
        response = response_global_product_data
        for key in important_keys:
            assert key in response['product']

    def test_variants_from_response_have_important_keys(self, response_global_product_data):
        important_keys = ['id', 'in_stock', 'color_code', 'color_code2']
        response = response_global_product_data
        for key in important_keys:
            for variant in response['variants']:
                assert key in variant

    @pytest.mark.asyncio
    async def test_request_with_invalid_global_product_id(self):
        try:
            await get_global_product_data(23432232343223243)
        except fastapi.exceptions.HTTPException as except_:
            assert except_


class TestGetStoreProductData:

    def test_response_type(self, response_store_product_data):
        response = response_store_product_data
        assert isinstance(response, dict)

    def test_response_keys(self, response_store_product_data):
        response = response_store_product_data
        assert list(response.keys()) == ['sync_product', 'sync_variants']

    def test_product_from_response_has_important_keys(self, response_store_product_data):
        response = response_store_product_data
        important_keys = ['id', 'name', 'thumbnail_url', 'is_ignored', ]
        for key in important_keys:
            assert key in response['sync_product']

    def test_variants_from_response_have_important_keys(self, response_store_product_data):
        response = response_store_product_data
        important_keys = ('id', 'currency', 'main_category_id', 'sync_product_id', 'variant_id', 'name',
                          'main_category_id', 'product', 'files', 'retail_price')
        for key in important_keys:
            for variant in response['sync_variants']:
                assert key in variant

    @pytest.mark.asyncio
    async def test_request_with_invalid_store_product_id(self):
        try:
            await get_store_product_data(2343243223243)
        except fastapi.exceptions.HTTPException as except_:
            assert except_


class TestGetStoreProductsByPage:

    def test_response_type(self, get_response_by_specified_in_env_page_number):
        assert isinstance(get_response_by_specified_in_env_page_number, list)

    def test_product_from_response_has_important_keys(self, get_response_by_specified_in_env_page_number):
        result = get_response_by_specified_in_env_page_number
        important_keys = ['id', ]
        for key in important_keys:
            for product_from_first_page in result:
                assert key in product_from_first_page

    @pytest.mark.asyncio
    async def test_nonexistent_page(self):
        response = await get_store_products_by_page(page=20)
        assert isinstance(response, list)
        assert len(response) == 0


class TestGetSpecifiedAmountOfStoreProducts:

    def test_relevance_provided_data(self, response_by_first_ten_products):
        response = response_by_first_ten_products
        paging = response['paging']
        limit_from_response = paging['limit']
        offset_from_response = paging['offset']
        assert 0 == offset_from_response
        assert 10 == limit_from_response
        assert isinstance(response['result'], list)
        assert isinstance(response['result'][0], dict)

    def test_availability_of_products(self, response_by_first_ten_products):
        response = response_by_first_ten_products
        total = response['paging']['total']
        result = response['result']
        assert response['paging']['total'] >= 10
        if total >= 10:
            assert len(result) == 10
            assert isinstance(response['result'], list)
            assert isinstance(response['result'][0], dict)

        elif total > 0:
            assert len(result) == total
            assert isinstance(response['result'], list)
            assert isinstance(response['result'][0], dict)
        else:
            assert len(result) == 0

    @pytest.mark.asyncio
    async def test_pass_to_request_offset_which_more_total(self, response_by_first_ten_products):
        first_request_for_understand_how_many_to_be_products = response_by_first_ten_products
        offset_which_more_total = first_request_for_understand_how_many_to_be_products['paging']['total'] + 1
        response = await get_specified_amount_of_store_products(offset=offset_which_more_total, amount=10)
        assert len(response['result']) == 0

    @pytest.mark.asyncio
    async def test_pass_to_request_limit_more_one_hundred(self):
        try:
            await get_specified_amount_of_store_products(offset=0, amount=101)
        except fastapi.exceptions.HTTPException as exception_:
            assert exception_


class TestSetOrder:

    def test_response_type(self, response_set_order):
        assert isinstance(response_set_order, dict)

    def test_user_data(self, response_set_order, data_of_set_order):
        data = data_of_set_order
        response = response_set_order
        for user_data_key in data['recipient'].keys():
            assert response['recipient'][user_data_key] == data['recipient'][user_data_key]

    def test_comparison_of_data_items_from_request_and_response(self, response_set_order, data_of_set_order):
        response = response_set_order
        for item in data_of_set_order['items']:
            for response_item in response['items'].copy():
                if item['sync_variant_id'] == response_item['sync_variant_id'] \
                        and item['quantity'] == response_item['quantity']:
                    response['items'].remove(response_item)
                    data_of_set_order['items'].remove(item)
        assert response['items'] == []
        assert data_of_set_order['items'] == []
