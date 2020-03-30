from typing import NamedTuple, Union


class Column(NamedTuple):
    pass


class Row(NamedTuple):
    pass


class AutoColumns(NamedTuple):
    columns: int


Layout = Union[Column, Row, AutoColumns]
