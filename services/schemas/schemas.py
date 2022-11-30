import datetime
from typing import Optional

from pydantic import AnyUrl, BaseModel, Field


class ColorSchemas(BaseModel):
    name: Optional[list[str]]
    code: Optional[list[str]]


class SyncVariantSchemas(BaseModel):
    store_id: int
    category_id: int
    color: ColorSchemas
    currency: str
    global_id: int
    global_product_id: int
    mockup: AnyUrl
    name: str
    price: str
    size: str
    sync_product_id: int


class ProductSchemas(BaseModel):
    global_id: int
    store_id: int
    name: str
    image: AnyUrl
    published: bool
    category_id: int
    currency: str
    description: Optional[str]
    available_colors_by_sizes_with_sync_variant_id: dict[str, list[tuple[ColorSchemas, int, str, AnyUrl]]]
    colors: list[ColorSchemas]
    sizes: list[str]


class ProductSchemaForView(ProductSchemas):
    price: str

    def __init__(self, *args, **kwargs):
        if 'price' not in kwargs:
            if kwargs['min_price'] != kwargs['max_price']:
                kwargs['price'] = f'{kwargs["min_price"]}-{kwargs["max_price"]}'
            else:
                kwargs['price'] = kwargs['max_price']
            kwargs.pop('min_price')
            kwargs.pop('max_price')
        super().__init__(*args, **kwargs)


class CatalogProductSchema(ProductSchemaForView):
    url: Optional[AnyUrl]


class RecipientSchema(BaseModel):
    name: str
    company: Optional[str] = None
    address1: str
    address2: Optional[str] = None
    city: str
    state_code: Optional[str] = None
    state_name: Optional[str] = None
    country_code: str
    country_name: Optional[str] = None
    zip: str
    phone: Optional[str] = None
    email: str
    tax_number: Optional[str] = None


class ItemOrderSchema(BaseModel):
    sync_variant_id: int
    quantity: int = Field(..., gt=0, le=10)


class OrderSchema(RecipientSchema):
    items: list[ItemOrderSchema]
    date: datetime.datetime = datetime.datetime.now()
