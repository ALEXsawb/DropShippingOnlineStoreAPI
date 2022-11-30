from pydantic.types import ConstrainedNumberMeta

from services.db.models import CatalogPageModel


def test_fields():
    assert isinstance(CatalogPageModel.__fields__['page'].annotation, ConstrainedNumberMeta)
    assert CatalogPageModel.__fields__['store_products_id'].annotation == list[str]


def test_global_key_prefix():
    assert CatalogPageModel._meta.global_key_prefix == 'OnlineStoreFastAPI'


def test_model_key_prefix():
    assert CatalogPageModel._meta.model_key_prefix == 'CatalogPages'