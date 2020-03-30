import os
import sys
from datetime import datetime, timedelta
from os.path import join, dirname, abspath
from threading import RLock
from typing import List, Dict, Tuple, Callable, Any

import qtmodern.styles
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow

from components import *
from components.dependency_injection import GuiManage, GuiDialog, DependencyInjection
from components.singleton import Singleton
from components.sketch.layout import Row
from udef import main_model, main_view, icon_path, window_title
from .dependency_injection import DependencyInjectionApp
from .extra_ui import existing_single_file_dialog, existing_multiple_files_dialog, new_file_dialog, directory_dialog
from .gui_builder import build_widget
from .gui_refresher import refresh_widget
from .user_dialog import yes_no_dialog, info_dialog, warning_dialog, error_dialog


class WidgetContainer(QMainWindow):
    widget: QWidget

    def __init__(self, init_widget: QWidget, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.widget = init_widget
        self.setCentralWidget(self.widget)
        self.setWindowIcon(QIcon(join(dirname(abspath(__file__)), '..', icon_path)))
        self.setWindowTitle(window_title)

    def replace_widget(self, new_widget: QWidget) -> None:
        self.widget = new_widget
        self.setCentralWidget(self.widget)


class App(metaclass=Singleton):
    _application: QApplication
    _dwidgets: Dict[int, QWidget]
    _refresh_lock: RLock
    _last_refresh: datetime

    class _QObject(QObject):
        _refresh_signal = pyqtSignal()
        _weak_refresh_signal = pyqtSignal()

    _qobject_signals: _QObject

    widget_sketch: Sketch
    widget_container: WidgetContainer
    current_model: Any
    current_view: Tuple[Callable[[Any], List[List[Sketch]]]]

    def __init__(self) -> None:
        self._qobject_signals = self._QObject()
        self._last_refresh = datetime.now()
        self._refresh_lock = RLock()
        self._application = QApplication([])
        if os.name == 'nt':
            self._application.setFont(QFont('Arial'))
        self.current_model = main_model
        self.current_view = (main_view,)
        self.widget_sketch = sketch_decorator(self.current_view[0](self.current_model))

        widget, self._dwidgets = build_widget(self.widget_sketch)
        self.widget_container = WidgetContainer(widget)

        # hack
        # self.widget_container.widget: ScrollableArea
        # self.widget_container.widget.widget(): MyQWidget
        self.widget_container.widget.widget().resized.connect(self.update_window_min_size)

        DependencyInjectionApp().refresh_gui = (self.refresh_gui,)
        DependencyInjectionApp().weak_refresh_gui = (self.weak_refresh,)
        DependencyInjectionApp().update_gui = (self.update_gui,)
        DependencyInjectionApp().get_dwidgets = ((lambda: self._dwidgets),)

        self._qobject_signals._refresh_signal.connect(DependencyInjectionApp().refresh_gui[0])
        self._qobject_signals._weak_refresh_signal.connect(DependencyInjectionApp().weak_refresh_gui[0])

        GuiManage()._refresh_view = ((lambda: self._qobject_signals._weak_refresh_signal.emit()),)
        GuiManage()._force_refresh_view = ((lambda: self._qobject_signals._refresh_signal.emit()),)

        GuiDialog()._yes_no_dialog = ((lambda q: yes_no_dialog(self.widget_container, q)),)
        GuiDialog()._info_dialog = ((lambda q: info_dialog(self.widget_container, q)),)
        GuiDialog()._warning_dialog = ((lambda q: warning_dialog(self.widget_container, q)),)
        GuiDialog()._error_dialog = ((lambda q: error_dialog(self.widget_container, q)),)

        DependencyInjection().open_file_action = (
            (lambda x: existing_single_file_dialog(self.widget_container, x)),)
        DependencyInjection().open_multiple_files_action = (
            (lambda x: existing_multiple_files_dialog(self.widget_container, x)),)
        DependencyInjection().save_file_action = (
            (lambda x: new_file_dialog(self.widget_container, x)),)
        DependencyInjection().open_directory_action = (
            (lambda x: directory_dialog(self.widget_container, x)),)

    def update_window_min_size(self):
        # hack
        # self.widget_container.widget: ScrollableArea
        # self.widget_container.widget.widget(): MyQWidget
        self.widget_container.setMinimumWidth(self.widget_container.widget.widget().minimumSizeHint().width())

    def forever_loop(self, dark=False) -> None:
        if dark:
            qtmodern.styles.dark(self._application)
        else:
            qtmodern.styles.light(self._application)

        self.widget_container.show()
        sys.exit(self._application.exec())

    def weak_refresh(self, rate: int = 6):
        dt = timedelta(seconds=1) / rate
        if datetime.now() - self._last_refresh > dt:
            if self._refresh_lock.acquire(timeout=dt.total_seconds()):
                self.refresh_gui()
                self._refresh_lock.release()

    def refresh_gui(self):
        self._refresh_lock.acquire()
        self._last_refresh = datetime.now()
        self.widget_container.widget.hide()

        resketch = sketch_decorator(self.current_view[0](self.current_model))
        refresh_widget(self.widget_sketch, resketch)
        self.widget_sketch = resketch

        self.widget_container.widget.show()
        self._refresh_lock.release()

    def update_gui(self, next_model: Any, next_view: Callable[[Any], List[List[Sketch]]]) -> None:
        self._refresh_lock.acquire()
        # self.widget_container.widget.hide()

        self.current_model = next_model
        self.current_view = (next_view,)

        self.refresh_gui()

        # self.widget_sketch = sketch_decorator(self.current_view[0](self.current_model))
        # widget, self.dwidgets = build_widget(self.widget_sketch)
        # self.widget_container.replace_widget(widget)

        # self.widget_container.widget.show()
        self._refresh_lock.release()


def sketch_decorator(rows_list: List[List[Sketch]]) -> Sketch:
    return ScrollArea('main', 50, [Group('group', Row(), row) for row in rows_list], _fixed_size=False)
