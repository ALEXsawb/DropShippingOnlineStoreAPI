import json
from typing import Optional, Any

from .SyncVariant import SyncVariant
from services.schemas.schemes_utils import try_to_change_the_type_to_int_or_float, get_price, get_uniques_colors
from .Color import Color


class SyncProduct:
    def __init__(self, product_data: dict):
        self.store_id = product_data['id']
        self.name = product_data['name'].strip()
        self.image = product_data['thumbnail_url']
        self.published = not product_data['is_ignored']


class ProductFromDict:
    def __init__(self, pk: str, currency: str, global_id: int, category_id: int, min_price: float, max_price: float,
                 description: Optional[str], image: str, published: bool, store_id: int, name: str,
                 colors: list[Color], available_colors_by_sizes_with_sync_variant_id: dict[str, tuple[str, int]],
                 sizes: list[str]):
        kwargs = locals().copy()
        kwargs.pop('self')
        [setattr(self, variable_name, kwargs[variable_name]) for variable_name in kwargs]


class ProductFromPrintfulResult(SyncProduct):
    def __init__(self, result):
        prices = set()
        self.variants = list()

        for sync_variant in result['sync_variants']:
            sync_variant = SyncVariant(sync_variant)
            self.variants.append(sync_variant)
            prices.add(float(sync_variant.price))

        self.currency = self.variants[0].currency
        self.global_id = self.variants[0].global_product_id
        self.category_id = self.variants[0].category_id
        self.min_price = min(prices)
        self.max_price = max(prices)
        self.description: Optional[str] = None
        self.colors = None
        self.sizes = None
        self.available_colors_by_sizes_with_sync_variant_id = None
        super().__init__(result['sync_product'])

    def get_sizes(self) -> list[set]:
        return list(set(variant.size for variant in self.variants))

    def get_colors(self) -> list[set]:
        return get_uniques_colors(self.variants)

    def get_available_colors_by_sizes_with_sync_variant_id(self) -> dict[str, list[Color]]:
        available_colors_by_sizes = dict()
        for variant in self.variants:
            value = (variant.color, variant.store_id, variant.price)
            if variant.color.code:
                value += (variant.files[1]['thumbnail_url'], )
            else:
                value += (variant.files[-1]['thumbnail_url'], )
            delattr(variant, 'files')
            if variant.size not in available_colors_by_sizes.keys():
                available_colors_by_sizes[variant.size] = [value, ]
            else:
                available_colors_by_sizes[variant.size].append(value)
        return available_colors_by_sizes


class Product(ProductFromDict, ProductFromPrintfulResult):
    def __init__(self, product_data_from_printful_api: Optional[dict] = None, **kwargs):
        if kwargs:
            ProductFromDict.__init__(self, **kwargs)
        else:
            ProductFromPrintfulResult.__init__(self, product_data_from_printful_api)

    def prepare_for_db_entry(self):
        delattr(self, 'variants')
        return self

    def to_json(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4))

    def __str__(self):
        return f'Product: {self.global_id};  StoreProduct: {self.store_id}'
