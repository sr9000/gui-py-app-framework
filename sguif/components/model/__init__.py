from typing import Any

from ..singleton import Singleton


class Model:
    pass


class StaticModel(metaclass=Singleton):
    pass


class ModalStaticModel(StaticModel):
    _rm: Any
    _rv: Any
    _cnd: bool

    def __init__(self) -> None:
        self._rm = None
        self._rv = None
        self._cnd = True

    def allow_leave(self):
        self._cnd = True

    def forbid_leave(self):
        self._cnd = False

    def enter(self, rm: Any, rv: Any, view: Any):
        self._rm = rm
        self._rv = rv
        return self, view

    def condition_leave(self, cv: Any):
        if self._cnd:
            return self.leave()
        else:
            return self, cv

    def leave(self):
        return self._rm, self._rv
