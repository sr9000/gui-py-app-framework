from typing import Any, NamedTuple, Set, Optional, Tuple

from PIL.Image import Image


class VSplit(NamedTuple):
    uid: Any = 'vsplit'

    def ids(self) -> Set[int]:
        return {id(self)}


class HSplit(NamedTuple):
    uid: Any = 'hsplit'

    def ids(self) -> Set[int]:
        return {id(self)}


class Header(NamedTuple):
    content: str
    uid: Any = 'header'

    def ids(self) -> Set[int]:
        return {id(self)}


class Text(NamedTuple):
    content: str
    uid: Any = 'text'

    def ids(self) -> Set[int]:
        return {id(self)}


class VText(NamedTuple):
    content: str
    uid: Any = 'text'

    def ids(self) -> Set[int]:
        return {id(self)}


class AutoImage(NamedTuple):
    image: Image
    width_range: Tuple[Optional[int], Optional[int]] = (None, None)
    height_range: Tuple[Optional[int], Optional[int]] = (None, None)
    uid: Any = 'image'

    def ids(self) -> Set[int]:
        return {id(self)}


class Feed(NamedTuple):
    uid: Any = 'feed'

    def ids(self) -> Set[int]:
        return {id(self)}
