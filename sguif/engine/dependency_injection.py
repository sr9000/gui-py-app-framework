from typing import Tuple, Callable, Optional, Any, List, Dict

from PyQt5.QtWidgets import QWidget

from ..components import Sketch
from ..components.singleton import Singleton


class DependencyInjectionApp(metaclass=Singleton):
    update_gui: Tuple[Callable[..., None]]
    refresh_gui: Tuple[Callable[[], None]]
    weak_refresh_gui: Tuple[Callable[[], None]]

    get_dwidgets: Tuple[Callable[[], Dict[int, QWidget]]]

    def __init__(self) -> None:
        def stub(*args):
            pass

        self.update_gui = (stub,)
        self.refresh_gui = ((lambda: None),)
        self.weak_refresh_gui = ((lambda: None),)
        self.get_dwidgets = ((lambda: {}),)


def make_button_catcher(action: Callable[[], None],
                        transition: Callable[[], Optional[Tuple[Any, Callable[[Any], List[List[Sketch]]]]]]) \
        -> Callable[[], None]:
    def catcher():
        action()
        upd = transition()
        if upd is None:
            DependencyInjectionApp().refresh_gui[0]()
        else:
            DependencyInjectionApp().update_gui[0](*upd)

    return catcher


def make_action_catcher(action: Callable[..., None]) -> Callable[..., None]:
    def catcher(*args):
        action(*args)
        DependencyInjectionApp().refresh_gui[0]()

    return catcher


def get_dwidgets() -> Dict[int, QWidget]:
    return DependencyInjectionApp().get_dwidgets[0]()
