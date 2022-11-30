from typing import Optional


class Color:
    def __init__(self, name: Optional[list[str]] = None, code: Optional[list[str]] = None):
        self.name = name
        self.code = code

    def __str__(self):
        return f'name: {self.name};  code: {self.code};'

    def __repr__(self):
        return f'Class: Color --> date: {{{self.__str__()}}}'

    def __eq__(self, other):
        if isinstance(other, Color) and self.name == other.name and self.code == other.code:
            return True
        return False
