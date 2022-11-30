from services.schemas.schemas import *


class TestProductSchemas:
    def test_attributes_names_and_their_types(self):
        annotations = ProductSchemas.__annotations__
        assert annotations['global_id'] == int
        assert annotations['store_id'] == int
        assert annotations['name'] == str
        assert annotations['image'] == AnyUrl
        assert annotations['published'] == bool
        assert annotations['category_id'] == int
        assert annotations['currency'] == str
        assert annotations['description'] == Optional[str]
        assert annotations['colors'] == list[ColorSchemas]
        assert annotations['sizes'] == list[str]
        assert annotations['available_colors_by_sizes_with_sync_variant_id'] == dict[str, list[tuple[ColorSchemas,
                                                                                                     int, str, AnyUrl]]]


class TestColorSchemas:
    def test_attributes_names_and_their_types(self):
        annotations = ColorSchemas.__annotations__
        assert annotations['name'] == Optional[list[str]]
        assert annotations['code'] == Optional[list[str]]


class TestSyncVariant:
    def test_attribute_names_and_their_types(self):
        annotations = SyncVariantSchemas.__annotations__
        assert annotations['store_id'] == int
        assert annotations['category_id'] == int
        assert annotations['color'] == ColorSchemas
        assert annotations['currency'] == str
        assert annotations['global_id'] == int
        assert annotations['global_product_id'] == int
        assert annotations['mockup'] == AnyUrl
        assert annotations['name'] == str
        assert annotations['price'] == str
        assert annotations['size'] == str
        assert annotations['sync_product_id'] == int


class TestProductSchemaForView:
    def test_attribute_names_and_their_types(self):
        annotations = ProductSchemaForView.__annotations__
        assert annotations['price'] == str

    def test__init__schema(self):
        product_data = {"global_id": 319,
                        "store_id": 287276628,
                        "name": "Champion Hoodie",
                        "image": "https://files.cdn.printful.com/files/e43/e439b71c006094c30e57faab96fe44b2_preview.png",
                        "published": True,
                        "category_id": 7,
                        "currency": "USD",
                        "description": None,
                        "available_colors_by_sizes_with_sync_variant_id": {
                            "L": [
                                [
                                    {
                                        "name": [
                                            "Light Steel"
                                        ],
                                        "code": [
                                            "#c2c2c0"
                                        ]
                                    },
                                    3522441549,
                                    "51.00",
                                    "https://files.cdn.printful.com/files/e43/e439b71c006094c30e57faab96fe44b2_thumb.png"
                                ]
                            ],
                            "M": [
                                [
                                    {
                                        "name": [
                                            "Light Steel"
                                        ],
                                        "code": [
                                            "#c2c2c0"
                                        ]
                                    },
                                    3522441548,
                                    "51.00",
                                    "https://files.cdn.printful.com/files/e43/e439b71c006094c30e57faab96fe44b2_thumb.png"
                                ]
                            ],
                            "S": [
                                [
                                    {
                                        "name": [
                                            "Light Steel"
                                        ],
                                        "code": [
                                            "#c2c2c0"
                                        ]
                                    },
                                    3522441547,
                                    "51.00",
                                    "https://files.cdn.printful.com/files/e43/e439b71c006094c30e57faab96fe44b2_thumb.png"
                                ]
                            ],
                            "XL": [
                                [
                                    {
                                        "name": [
                                            "Light Steel"
                                        ],
                                        "code": [
                                            "#c2c2c0"
                                        ]
                                    },
                                    3522441550,
                                    "51.00",
                                    "https://files.cdn.printful.com/files/e43/e439b71c006094c30e57faab96fe44b2_thumb.png"
                                ]
                            ]
                        },
                        "colors": [
                            {
                                "name": [
                                    "Light Steel"
                                ],
                                "code": [
                                    "#c2c2c0"
                                ]
                            }
                        ],
                        "sizes": [
                            "S",
                            "M",
                            "L",
                            "XL"
                        ],
                        "min_price": "45.0",
                        "max_price": "51.0",
                        "url": "http://127.0.0.1:8000/product/319-287276628"}
        product_for_view = ProductSchemaForView(**product_data)
        product_for_view_dict = product_for_view.dict()
        assert product_for_view
        assert not product_for_view_dict.get('min_price', None)
        assert not product_for_view_dict.get('max_price', None)
        assert product_for_view_dict.get('price', None)


class TestCatalogProductSchema:

    def test_attribute_names_and_their_types(self):
        annotations = CatalogProductSchema.__annotations__
        assert annotations['url'] == Optional[AnyUrl]


class TestRecipientSchema:
    def test_attribute_names_and_their_types(self):
        annotations = RecipientSchema.__annotations__
        assert annotations['name'] == str
        assert annotations['company'] == Optional[str]
        assert annotations['address1'] == str
        assert annotations['address2'] == Optional[str]
        assert annotations['city'] == str
        assert annotations['state_code'] == Optional[str]
        assert annotations['state_name'] == Optional[str]
        assert annotations['country_code'] == str
        assert annotations['country_name'] == Optional[str]
        assert annotations['zip'] == str
        assert annotations['phone'] == Optional[str]
        assert annotations['email'] == str
        assert annotations['tax_number'] == Optional[str]


class TestItemOrderSchema:
    def test_attribute_names_and_their_types(self):
        annotations = ItemOrderSchema.__annotations__
        assert annotations['sync_variant_id'] == int
        assert annotations['quantity'] == int


class TestOrderSchema:
    def test_attribute_names_and_their_types(self):
        annotations = OrderSchema.__annotations__
        assert annotations['items'] == list[ItemOrderSchema]
        assert annotations['date'] == datetime.datetime
