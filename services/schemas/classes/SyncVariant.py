import json
from typing import Optional

from .Color import Color


class SyncVariantFromDict:
    def __init__(self, store_id: int, currency: str, global_id: int, category_id: int, price: str,
                 color, size: str, mockup: str, sync_product_id: int, name: str, global_product_id, **kwargs):
        self.store_id = store_id
        self.sync_product_id = sync_product_id
        self.global_id = global_id
        self.name = name
        self.color = color
        self.size = size
        self.category_id = category_id
        self.global_product_id = global_product_id
        self.mockup = mockup
        self.price = price
        self.currency = currency


class SyncVariantFromPrintfulResult:
    def __init__(self, variant_data: dict):
        self.store_id = variant_data['id']
        self.sync_product_id = variant_data['sync_product_id']
        self.global_id = variant_data['variant_id']
        self.name, color_and_size_or_only_size = variant_data['name'].strip().split(' - ')
        self.category_id = variant_data['main_category_id']
        self.global_product_id = variant_data['product']['product_id']
        self.files = variant_data['files']
        self.price = variant_data['retail_price']
        self.currency = variant_data['currency']
        try:
            color_and_size = color_and_size_or_only_size.split(' / ')
            if len(color_and_size) > 2:
                self.size = color_and_size[-1]
                self.color = color_and_size[:-1]
            else:
                self.color, self.size = color_and_size
        except ValueError:
            self.size = color_and_size_or_only_size
            if '/' in variant_data['product']['name'].split('(')[1] and 'All-Over' not in variant_data['product']['name']:
                self.color = [variant_data['product']['name'].split('(')[1].split(' / ')[0], ]
            else:
                self.color = None
        self.color = Color(self.color if not self.color or isinstance(self.color, list) else [self.color])


class SyncVariant(SyncVariantFromDict, SyncVariantFromPrintfulResult):
    def __init__(self, variant_data_from_printful_api: Optional[dict] = None, **kwargs):
        if kwargs:
            SyncVariantFromDict.__init__(self, **kwargs)
        else:
            SyncVariantFromPrintfulResult.__init__(self, variant_data_from_printful_api)

    def to_json(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4))

    def __str__(self):
        return self.color

    def __repr__(self):
        return f'{self.size} | {self.color}'
