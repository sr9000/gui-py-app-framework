from datetime import date, time, datetime
from typing import NamedTuple, Any, Optional, Callable, List, Tuple, Set

from PIL.Image import Image


class TextInput(NamedTuple):
    uid: Any
    value: str
    on_input: Callable[[str], None] = lambda _: None
    read_only: bool = False

    def ids(self) -> Set[int]:
        return {id(self)}


class TextMultilineInput(NamedTuple):
    uid: Any
    value: str
    on_input: Callable[[str], None] = lambda _: None
    read_only: bool = False

    def ids(self) -> Set[int]:
        return {id(self)}


class IntegerInput(NamedTuple):
    uid: Any
    value: int
    on_input: Callable[[int], None] = lambda _: None
    read_only: bool = False

    def ids(self) -> Set[int]:
        return {id(self)}


class FloatInput(NamedTuple):
    uid: Any
    value: float
    on_input: Callable[[float], None] = lambda _: None
    read_only: bool = False

    def ids(self) -> Set[int]:
        return {id(self)}


class ButtonInput(NamedTuple):
    uid: Any
    caption: str
    on_input: Callable[[], None] = lambda: None
    transition: Callable[[], Optional[Tuple[Any, Callable[[Any], List[List[Any]]]]]] = lambda: None
    disabled: bool = False
    img: Optional[Image] = None
    img_size: Tuple[int, int] = (24, 24)

    def ids(self) -> Set[int]:
        return {id(self)}


class DateInput(NamedTuple):
    uid: Any
    value: date
    on_input: Callable[[date], None] = lambda _: None
    read_only: bool = False

    def ids(self) -> Set[int]:
        return {id(self)}


class TimeInput(NamedTuple):
    uid: Any
    value: time
    on_input: Callable[[time], None] = lambda _: None
    read_only: bool = False

    def ids(self) -> Set[int]:
        return {id(self)}


class DateTimeInput(NamedTuple):
    uid: Any
    value: datetime
    on_input: Callable[[datetime], None] = lambda _: None
    read_only: bool = False

    def ids(self) -> Set[int]:
        return {id(self)}


class SliderInput(NamedTuple):
    uid: Any
    value: float
    min_value: float
    max_value: float
    on_input: Callable[[float], None] = lambda _: None
    precision: int = 1000
    disabled: bool = False

    def ids(self) -> Set[int]:
        return {id(self)}


class ComboBoxInput(NamedTuple):
    uid: Any
    value: Any
    options: List[Any]
    descriptions: Optional[List[str]] = None
    on_input: Callable[[Any], None] = lambda _: None
    disabled: bool = False

    def ids(self) -> Set[int]:
        return {id(self)}

# class CalendarInput(NamedTuple):
#     uid: Any
#     value: date
#     on_input: Callable[[date], None] = lambda _: None
#
#     def ids(self) -> Set[int]:
#         return {id(self)}
