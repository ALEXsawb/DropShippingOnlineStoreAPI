import pytest

from services.db.models import ProductModel
from services.schemas.schemas import ColorSchemas


@pytest.fixture
async def get_product():
    product_data = {'global_id': 515,
                    'store_id': 4839204839,
                    'name': 'I',
                    'image': 'https://aka/something',
                    'published': True,
                    'category_id': 12,
                    'currency': 'USD',
                    'min_price': 12.0,
                    'max_price': 23.0,
                    'description': None,
                    'available_colors_by_sizes_with_sync_variant_id': {
                        'S': [(ColorSchemas(name=['Black'], code=['#090909']), 2443885201, '12',
                               'https://aka/something'),
                              (ColorSchemas(name=['Navy'], code=['#080f1f']), 2443885205, '22',
                               'https://aka/something'),
                              (ColorSchemas(name=['Light Steel'], code=['#c2c2c0']), 2443885209, '15',
                               'https://aka/something')]},
                    'colors': [ColorSchemas(name=['Black'], code=['#090909']),
                               ColorSchemas(name=['Navy'], code=['#080f1f']),
                               ColorSchemas(name=['Light Steel'], code=['#c2c2c0'])],
                    'sizes': ['S', ]}
    return await ProductModel(**product_data).save()
