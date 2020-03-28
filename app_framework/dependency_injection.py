from pathlib import Path
from typing import Tuple, List, Optional, Callable

from app_framework.singleton import Singleton


class GuiDialog(metaclass=Singleton):
    _yes_no_dialog: Tuple[Callable[[str], bool]]
    _info_dialog: Tuple[Callable[[str], None]]
    _warning_dialog: Tuple[Callable[[str], None]]
    _error_dialog: Tuple[Callable[[str], None]]

    def __init__(self) -> None:
        self._yes_no_dialog = ((lambda _: False),)
        self._info_dialog = ((lambda _: None),)
        self._warning_dialog = ((lambda _: None),)
        self._error_dialog = ((lambda _: None),)

    def yes_no_dialog(self, question: str) -> bool:
        return self._yes_no_dialog[0](question)

    def info_dialog(self, message: str):
        self._info_dialog[0](message)

    def warning_dialog(self, message: str):
        self._warning_dialog[0](message)

    def error_dialog(self, message: str):
        self._error_dialog[0](message)


class GuiManage(metaclass=Singleton):
    _refresh_view: Tuple[Callable[[], None]]
    _force_refresh_view: Tuple[Callable[[], None]]

    def __init__(self) -> None:
        self._refresh_view = ((lambda: None),)
        self._force_refresh_view = ((lambda: None),)

    def refresh_view(self):
        self._refresh_view[0]()

    def force_refresh_view(self):
        self._force_refresh_view[0]()


class DependencyInjection(metaclass=Singleton):
    open_file_action: Tuple[Callable[[Callable[[Optional[Path]], None]], Callable[[], None]]]
    open_multiple_files_action: Tuple[Callable[[Callable[[List[Path]], None]], Callable[[], None]]]
    open_directory_action: Tuple[Callable[[Callable[[Optional[Path]], None]], Callable[[], None]]]
    save_file_action: Tuple[Callable[[Callable[[Optional[Path]], None]], Callable[[], None]]]

    def __init__(self) -> None:
        self.open_file_action = ((lambda _: (lambda: None)),)
        self.open_multiple_files_action = ((lambda _: (lambda: None)),)
        self.open_directory_action = ((lambda _: (lambda: None)),)
        self.save_file_action = ((lambda _: (lambda: None)),)
