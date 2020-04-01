from typing import List, Dict, Any, Tuple, NamedTuple, Set, Optional, Callable

from .layout import Layout


def add_components(src: List[Any]) -> \
        Tuple[List[Any], Dict[Any, Any], Dict[Any, int]]:
    # result collections
    dst: List[Any] = []
    dcopm: Dict[Any, Any] = {}
    duids: Dict[Any, int] = {}

    for comp in src:
        # make uid unique
        if comp.uid not in duids:
            duids[comp.uid] = 1
        else:
            duids[comp.uid] += 1
        nuid = (comp.uid, duids[comp.uid])

        if isinstance(comp, tuple):
            comp = comp._replace(uid=nuid)
        else:
            # noinspection Mypy
            # comp is Group or ScrollArea
            comp.uid = nuid

        # append new component
        dcopm[comp.uid] = comp
        dst.append(comp)

    return dst, dcopm, duids


class Group:
    uid: Any
    layout: Layout
    components: List[Any]
    _dict_components: Dict[Any, Any]
    _dict_uids: Dict[Any, int]

    def __init__(self, uid: Any, layout: Layout, components: List[Any]) -> None:
        self.uid = uid
        self.layout = layout
        self.components, self._dict_components, self._dict_uids = add_components(components)

    def __str__(self) -> str:
        return f'Group(uid={self.uid}, layout={self.layout}, components={self.components})'

    def __repr__(self):
        return self.__str__()

    def ids(self) -> Set[int]:
        return set.union({id(self)}, *[comp.ids() for comp in self.components])


class Matrix:
    uid: Any
    components: List[List[Any]]
    _flat: List[Any]
    _dict_components: Dict[Any, Any]
    _dict_uids: Dict[Any, int]

    def __init__(self, uid: Any, components: List[List[Any]]) -> None:
        self.uid = uid
        comps = [x for row in components for x in row if x is not None]
        self._flat, self._dict_components, self._dict_uids = add_components(comps)

        self.components = []
        i = 0
        for row in components:
            tmp = []
            for x in row:
                if x is None:
                    tmp.append(None)
                else:
                    tmp.append(self._flat[i])
                    i += 1
            self.components.append(tmp)

    def __str__(self) -> str:
        return f'Matrix(uid={self.uid}, components={self.components})'

    def __repr__(self):
        return self.__str__()

    def ids(self) -> Set[int]:
        return set.union({id(self)}, *[comp.ids() for comp in self._flat])


class ScrollArea:
    uid: Any
    min_height: int
    components: List[Any]
    _fixed_size: bool
    _dict_components: Dict[Any, Any]
    _dict_uids: Dict[Any, int]

    def __init__(self, uid: Any, min_height: int, components: List[Any], _fixed_size=True) -> None:
        self.uid = uid
        self.min_height = min_height
        self._fixed_size = _fixed_size
        self.components, self._dict_components, self._dict_uids = add_components(components)

    def __str__(self) -> str:
        return f'ScrollArea(uid={self.uid}, min_height={self.min_height}, components={self.components})'

    def __repr__(self):
        return self.__str__()

    def ids(self) -> Set[int]:
        return set.union({id(self)}, *[comp.ids() for comp in self.components])


class NamedPlace(NamedTuple):
    uid: Any
    title: str
    component: Any
    on_toggle: Optional[Callable[[bool], None]] = None
    checked: bool = False

    def ids(self) -> Set[int]:
        return set.union({id(self)}, self.component.ids())
