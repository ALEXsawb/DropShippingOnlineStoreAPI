from typing import Optional

from services.db.models import ColorModel


class TestColorModel:
    def test_fields(self):
        assert ColorModel.__fields__['name'].annotation == Optional[list[str]]
        assert ColorModel.__fields__['code'].annotation == Optional[list[str]]

    def test_global_key_prefix(self):
        assert ColorModel._meta.global_key_prefix == 'OnlineStoreFastAPI'

    def test_model_key_prefix(self):
        assert ColorModel._meta.model_key_prefix == 'Color'