import random

import pytest

from services.db.models import ProductModel


class TestCatalogFiltered:
    @pytest.mark.asyncio
    async def test_invalid_filters(self, async_app_client, invalid_filters):
        """After this request we will get up to first hundred products which will be stored to in db"""
        response = await async_app_client.get(f'/catalog/filter?{invalid_filters}')
        assert response.json() == {'detail': ("We couldn't find products with specified filters. "
                                              "You can make filters more softly.")}

    @pytest.mark.asyncio
    async def test_colors_filter_by_name(self, async_app_client):
        colors = await self.get_two_random_color_name()
        first_color = colors[0]

        response = await async_app_client.get(f'/catalog/filter?colors={first_color[0]}&')
        for product in response.json():
            assert first_color in [color['name'] for color in product['colors']]

        filter_text_for_request = '&'.join([f'colors={color[0]}' for color in colors])
        response = await async_app_client.get(f'/catalog/filter?{filter_text_for_request}')
        for product in response.json():
            product_colors = [color['name'] for color in product['colors']]
            assert list(set([color[0] for color in colors]) & set(color[0] for color in product_colors))

    @pytest.mark.asyncio
    async def test_colors_filter_by_code(self, async_app_client):
        colors = await self.get_two_random_color_code()
        first_code = colors[0]

        response = await async_app_client.get(f'/catalog/filter?colors=%23{first_code[0][1:]}')
        for product in response.json():
            assert first_code in [color['code'] for color in product['colors']]

        filter_text_for_request = '&'.join([f'colors=%23{color_code[0][1:]}' for color_code in colors])
        response = await async_app_client.get(f'/catalog/filter?{filter_text_for_request}')

        for product in response.json():
            product_colors = [color['code'] for color in product['colors']]
            assert list(set([color[0] for color in colors]) & set(color[0] for color in product_colors))

    @pytest.mark.asyncio
    async def test_sizes_filter(self, async_app_client):
        async def get_random_size():
            return random.choice(random.choice(await ProductModel.find().all()).sizes)

        first_size = second_size = await get_random_size()
        while second_size == first_size:
            second_size = await get_random_size()

        response = await async_app_client.get(f'/catalog/filter?sizes={first_size}')
        for product in response.json():
            assert first_size in product['sizes']

        response = await async_app_client.get(f'/catalog/filter?sizes={second_size}&sizes={first_size}')
        for product in response.json():
            try:
                assert first_size in product['sizes']
            except AssertionError:
                assert second_size in product['sizes']

    @pytest.mark.asyncio
    async def test_min_price_filter(self, async_app_client):
        min_price = random.choice(await ProductModel.find().all()).min_price
        response = await async_app_client.get(f'/catalog/filter?min_price={min_price}')
        for product in response.json():
            assert min_price <= self.get_min_price(product['price'])

    @pytest.mark.asyncio
    async def test_max_price_filter(self, async_app_client):
        max_price = random.choice(await ProductModel.find().all()).max_price
        response = await async_app_client.get(f'/catalog/filter?max_price={max_price}')
        for product in response.json():
            assert max_price >= self.get_max_price(product['price'])

    @pytest.mark.asyncio
    async def test_max_and_min_price_filter(self, async_app_client):
        product = random.choice(await ProductModel.find().all())
        max_price = product.max_price
        min_price = product.min_price
        response = await async_app_client.get(f'/catalog/filter?max_price={max_price}&min_price={min_price}')
        for product in response.json():
            price = product['price']
            if '-' in price:
                min_response_price = float(price.split('-')[0])
                max_response_price = float(price.split('-')[1])
            else:
                min_response_price = max_response_price = float(price)
            assert max_price >= max_response_price
            assert min_price <= min_response_price

    @pytest.mark.asyncio
    async def test_mixing_filters(self, async_app_client):
        random_product = random.choice(await ProductModel.find().all())
        while None in [color.name for color in random_product.colors]:
            random_product = random.choice(await ProductModel.find().all())

        colors = await self.get_two_random_color_name()

        sizes = await self.get_two_random_product_size_by_product(random_product)

        min_price_for_request = random_product.min_price
        max_price_for_request = random_product.max_price
        if max_price_for_request == min_price_for_request:
            max_price_for_request += 10

        request = f'min_price={min_price_for_request}&max_price={max_price_for_request}'
        for color in colors.copy():
            request += f'&colors={color[0]}'
        for size in sizes:
            request += f'&sizes={size}'
        response = await async_app_client.get(f'/catalog/filter?{request}')
        for product in response.json():
            assert max_price_for_request >= self.get_max_price(product['price'])
            assert min_price_for_request <= self.get_min_price(product['price'])
            assert set(sizes) & set(product['sizes'])
            product_colors = [color['name'] for color in product['colors']]
            assert set([color[0] for color in colors]) & set(color[0] for color in product_colors)

    async def get_two_random_color_name(self):
        second_color = first_color = None
        while not first_color:
            first_color = random.choice(await ProductModel.find().all()).colors[0].name

        while not second_color or second_color == first_color:
            second_color = random.choice(await ProductModel.find().all()).colors[0].name
        colors_name = [first_color, second_color]
        self.check_mixed_and_fixed_list_for_request_color_name_or_code(colors_name)
        return colors_name

    async def get_two_random_color_code(self) -> tuple[str, str]:
        async def get_code():
            return random.choice(random.choice(await ProductModel.find().all()).colors).code

        first_code = second_code = None
        while not first_code:
            first_code = await get_code()

        while not second_code or second_code == first_code:
            second_code = await get_code()
        color_codes = [first_code, second_code]
        self.check_mixed_and_fixed_list_for_request_color_name_or_code(color_codes)
        return color_codes

    @staticmethod
    async def get_two_random_product_size_by_product(random_product: ProductModel = None):
        if not random_product:
            random_product = random.choice(await ProductModel.find().all())

        sizes = [random.choice(random_product.sizes), ]
        if len(random_product.sizes) > 2:
            sizes.append(None)
            while not sizes[1] or sizes[1] == sizes[0]:
                sizes[1] = random.choice(random_product.sizes)
        elif len(random_product.sizes) == 2:
            sizes = random_product.sizes
        return sizes

    @staticmethod
    def check_mixed_and_fixed_list_for_request_color_name_or_code(color_names_or_codes: list[str]):
        for color in color_names_or_codes.copy():
            if len(color) > 1:
                mixed_color = color
                del color_names_or_codes[color_names_or_codes.index(mixed_color)]
                for color_ in mixed_color:
                    if color_ not in color:
                        color_names_or_codes.append(color_)

    @staticmethod
    def get_price(price: str, index: int) -> float:
        return float(price.split('-')[index]) if '-' in price else float(price)

    def get_min_price(self, price: str) -> float:
        return self.get_price(price, 0)

    def get_max_price(self, price: str) -> float:
        return self.get_price(price, 1)