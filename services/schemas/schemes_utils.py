from services.schemas.classes.Color import Color


def get_price(price: set[int | float], currency: str):
    if len(price) > 1:
        return f'{min(price)}-{max(price)}'
    else:
        return str(price.pop())


def try_to_change_the_type_to_int_or_float(price: str):
    integer, hundredths = price.split('.')
    if hundredths == '00':
        return int(integer)
    else:
        return float(price)


def get_uniques_colors(variants):
    uniques_colors = []
    if isinstance(variants, dict):
        variants = [Color(**variant.color) for variant in variants]
    for variant in variants:
        if variant.color not in uniques_colors:
            uniques_colors.append(variant.color)
    return uniques_colors
