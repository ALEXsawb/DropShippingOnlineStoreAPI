from typing import Optional

import redis
from aredis_om import Field, JsonModel, EmbeddedJsonModel
from aredis_om.model.model import Expression

from services.db.db_conection import db
from services.schemas.schemas import ProductSchemas, OrderSchema


class MetaMixin:
    global_key_prefix = 'OnlineStoreFastAPI'
    database = db


class ColorModel(EmbeddedJsonModel):
    name: Optional[list[str]] = Field(index=True)
    code: Optional[list[str]] = Field(index=True)

    class Meta(MetaMixin):
        model_key_prefix = 'Color'


class ProductModel(JsonModel, ProductSchemas):
    global_id: int = Field(index=True)
    store_id: int = Field(index=True)
    category_id: int = Field(index=True, full_text_search=True)
    name: str = Field(index=True, full_text_search=True)
    min_price: float = Field(index=True)
    max_price: float = Field(index=True)
    colors: list[ColorModel]
    sizes: list[str] = Field(index=True)

    class Meta(MetaMixin):
        model_key_prefix = 'Product'

    def key(self):
        return self.make_primary_key(f'{self.global_id}-{self.store_id}')

    async def expire(self, seconds: int):
        await ProductModel.db().expire(self.key(), seconds)

    async def ttl(self):
        return await ProductModel.db().ttl(self.key())

    async def save(self, pipeline: Optional[redis.client.Pipeline] = None) -> "JsonModel":
        saved_product = await super().save(pipeline)
        await self.expire(60)
        return saved_product

    @classmethod
    def get_united_prefix(cls):
        return f'{cls.Meta.global_key_prefix}:{cls.Meta.model_key_prefix}:'

    @classmethod
    def find_by_data_of_filters(cls, *args, **kwargs):
        return super().find(cls.__get_formed_query(kwargs))

    @classmethod
    def __get_formed_query(cls, kwargs):
        cls.__define_bind_fields_with_search_methods()
        cls.__kwargs = kwargs
        if 'colors' in kwargs:
            first_part_of_query = cls.__color_field_processing()
            if first_part_of_query:
                return cls.__united_all_search_queries(kwargs.items(), first_part_of_query)

        data_of_filter = iter(kwargs.items())
        first_part_of_query = cls.__get_first_part_of_query(data_of_filter)
        return cls.__united_all_search_queries(data_of_filter, first_part_of_query)

    @classmethod
    def __define_bind_fields_with_search_methods(cls) -> dict:
        cls.__bind_fields_with_search_methods = {
            'min_price': cls.min_price.__ge__,
            'max_price': cls.max_price.__le__,
            'colors_codes': cls.colors.code.__lshift__,
            'colors_names': cls.colors.name.__lshift__,
            'sizes': cls.sizes.__lshift__
        }

    @staticmethod
    def __get_colors_names_and_codes_from_request(kwargs: dict):
        colors_names = []
        colors_codes = []
        for color in kwargs.pop('colors'):
            if color.isdigit():
                colors_codes.append('#' + str(color))
            elif '#' in color:
                colors_codes.append(color)
            else:
                colors_names.append(color)
        return colors_names, colors_codes

    @classmethod
    def __color_field_processing(cls) -> None | Expression:
        colors_names, colors_codes = cls.__get_colors_names_and_codes_from_request(cls.__kwargs)
        if colors_codes and colors_names:
            return cls.__bind_fields_with_search_methods['colors_names'](colors_names) | \
                   cls.__bind_fields_with_search_methods['colors_codes'](colors_codes)
        elif colors_names:
            cls.__kwargs['colors_names'] = colors_names
        elif colors_codes:
            cls.__kwargs['colors_codes'] = colors_codes

    @classmethod
    def __united_all_search_queries(cls, data_of_filter, query):
        for field_name, value in data_of_filter:
            query = query & cls.__bind_fields_with_search_methods[field_name](value)
        return query

    @classmethod
    def __get_first_part_of_query(cls, data_of_filter):
        field_name, field_value = next(data_of_filter)
        return cls.__bind_fields_with_search_methods[field_name](field_value)


class OrderModel(JsonModel, OrderSchema):
    class Meta(MetaMixin):
        model_key_prefix = 'Orders'


class CatalogPageModel(JsonModel):
    page: int = Field(..., ge=1)
    store_products_id: list[str]

    class Meta(MetaMixin):
        model_key_prefix = 'CatalogPages'

    async def save(self, pipeline: Optional[redis.client.Pipeline] = None) -> "JsonModel":
        saved_data = await super().save(pipeline)
        await CatalogPageModel.db().expire(self.key(), 60)
        return saved_data

    def key(self):
        return self.make_primary_key(self.page)
