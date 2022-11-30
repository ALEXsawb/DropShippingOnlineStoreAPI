from datetime import datetime

from services.db.models import OrderModel
from services.schemas.schemas import ItemOrderSchema


def test_fields():
    assert OrderModel.__fields__['items'].annotation == list[ItemOrderSchema]
    assert OrderModel.__fields__['date'].annotation == datetime


def test_global_key_prefix():
    assert OrderModel._meta.global_key_prefix == 'OnlineStoreFastAPI'


def test_model_key_prefix():
    assert OrderModel._meta.model_key_prefix == 'Orders'