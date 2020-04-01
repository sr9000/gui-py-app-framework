from pathlib import Path
from string import digits
from typing import Iterable, Any, Tuple, Callable, Optional, List

from PIL.Image import Image
from PIL.ImageQt import ImageQt
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import pyqtSignal, Qt, QSize, QPoint
from PyQt5.QtGui import QValidator, QTextOption, QPixmap, QPainter
from PyQt5.QtWidgets import QSlider, QLineEdit, QSizePolicy, QPlainTextEdit, QFileDialog, QMainWindow, QFrame, QLabel, \
    QWidget, QSpacerItem, QHBoxLayout
from more_itertools import chunked

from sguif.engine.dependency_injection import make_action_catcher

negdigits = '-' + digits


class FloatSlider(QSlider):
    # create our our signal that we can connect to if necessary
    floatValueChanged = pyqtSignal(object)
    _minimum: float
    _maximum: float
    _value: float
    _precision: int

    def __init__(self, precision: int = 100, *args, **kargs) -> None:
        assert precision > 2
        super().__init__(*args, **kargs)
        self.setOrientation(Qt.Horizontal)
        self._precision = precision
        self._value = 0.0
        self._minimum = 0.0
        self._maximum = 10.0

        super().setMinimum(0)
        super().setMaximum(self._precision)
        super().setValue(0)
        self._step_update()

        self.valueChanged[int].connect(self._emit_float_value_changed)

    def _emit_float_value_changed(self, value: int):
        percents = value / self._precision
        rng = self._maximum - self._minimum
        self._value = self._minimum + percents * rng
        self.floatValueChanged.emit(self._value)

    def value(self):
        return self._value

    def set_minimum(self, lower):
        if lower >= self._maximum:
            raise Exception(f'DoubleSlider new lower bound "{lower}" greater than upper bound "{self._maximum}"')
        self._minimum = lower
        self._update_qslider()

    def set_maximum(self, upper):
        if upper <= self._minimum:
            raise Exception(f'DoubleSlider new upper bound "{upper}" less than lower bound "{self._minimum}"')
        self._minimum = upper
        self._update_qslider()

    def set_range(self, lower, upper):
        if lower >= upper:
            raise Exception(f'DoubleSlider new upper bound "{upper}" less than new lower bound "{lower}"')
        self._minimum, self._maximum = lower, upper
        self._update_qslider()

    def set_precision(self, precision: int):
        assert precision > 2
        self._precision = precision
        self._step_update()
        self._update_qslider()

    def set_value(self, value):
        if value < self._minimum:
            raise Exception(f'DoubleSlider set value "{value}" less than lower bound "{self._minimum}"')
        if value > self._maximum:
            raise Exception(f'DoubleSlider set value "{value}" greater than upper bound "{self._maximum}"')
        self._value = value
        self._update_qslider()

    def _update_qslider(self):
        self._value = min(self._maximum, max(self._minimum, self._value))
        diff = self._value - self._minimum
        rng = self._maximum - self._minimum
        step = rng / self._precision
        actual = round(diff / step)
        wasnt_blocked = not self.signalsBlocked()
        if wasnt_blocked:
            self.blockSignals(True)
        super().setValue(actual)
        if wasnt_blocked:
            self.blockSignals(False)

    def _step_update(self):
        super().setSingleStep(-(-self._precision // 100))
        super().setPageStep(-(-self._precision // 10))


class IntValidator(QValidator):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def validate(self, text: str, pos: int) -> Tuple['QValidator.State', str, int]:
        try:
            broken = ''.join(filter(lambda x: x not in (' ' + negdigits), text))
            if len(broken) > 0:
                raise ValueError()

            ftext = ''.join(filter(lambda x: x in negdigits, text))

            if len(ftext) == 0:
                return QValidator.Acceptable, '0', 1

            if ftext == '-':
                ftext = '0'

            number = int(ftext)

            after = ilen(filter(lambda x: x in negdigits, text[pos:]))
            formatted_tail = after + max(0, after - 1) // 3
            text = ' '.join(''.join(x) for x in chunked(str(number)[::-1], 3))[::-1]

            return QValidator.Acceptable, text, (len(text) - formatted_tail)
        except ValueError:
            return QValidator.Invalid, text, pos


class IntLineEdit(QLineEdit):
    intValueChanged = pyqtSignal(object)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setText('0')
        self.setValidator(IntValidator())
        self.setAlignment(Qt.AlignRight)
        self.textChanged[str].connect(self._emit_int_value_changed)

    def _emit_int_value_changed(self, value: str):
        self.intValueChanged.emit(int(''.join(filter(lambda x: x in negdigits, value))))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Backspace:
            pos = self.cursorPosition()
            text = self.text()
            head = ''.join(filter(lambda x: x in negdigits, text[:pos]))[:-1]
            text = head + text[pos:]

            amount = ilen(filter(lambda x: x in negdigits, text))
            if amount % 3 == 0:
                pos -= 1
            pos = max(0, pos - 1)

            if text == '-':
                text = '0'

            vstatus, _, _ = self.validator().validate(text, pos)
            if vstatus is QValidator.Acceptable:
                self.setText(text)
                self.setCursorPosition(pos)
        else:
            super().keyPressEvent(event)

    def set_value(self, value: int):
        if value != int(''.join(filter(lambda x: x in negdigits, self.text()))):
            self.setText(str(value))


class FloatValidator(QValidator):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def validate(self, text: str, pos: int) -> Tuple['QValidator.State', str, int]:
        try:
            dfirst = {'-+': '-', '+-': '+', '++': '+', '--': '-'}
            dlast = {'-+': '+', '+-': '-', '++': '+', '--': '-'}
            if text[pos - 1:pos + 1] in dfirst.keys():
                s = [x for x in text]
                s[pos - 1:pos + 1] = dfirst[text[pos - 1:pos + 1]]
                text = ''.join(s)
            if text[pos - 2:pos] in dlast.keys():
                s = [x for x in text]
                s[pos - 2:pos] = dlast[text[pos - 2:pos]]
                text = ''.join(s)
                pos -= 1
            if text in ('', '+', '-', '.'):
                text = '0'
            if text[-1] == 'e':
                text += '+0'
            if text[-2:] in ('e+', 'e-'):
                # text = text[:-2]
                text += '0'
            float(text)
            return QValidator.Acceptable, text, min(pos, len(text))
        except ValueError:
            return QValidator.Invalid, text, pos


class FloatLineEdit(QLineEdit):
    floatValueChanged = pyqtSignal(object)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setText('0')
        self.setValidator(FloatValidator())
        self.setAlignment(Qt.AlignRight)
        self.textChanged[str].connect(self._emit_float_value_changed)

    def _emit_float_value_changed(self, value: str):
        self.floatValueChanged.emit(float(value))

    def set_value(self, value: float):
        if value != float(self.text()):
            self.setText(str(value))


class AutoResizingTextEdit(QPlainTextEdit):
    textValueChanged = pyqtSignal(object)

    # https://github.com/cameel/auto-resizing-text-edit
    def __init__(self, parent=None):
        super(AutoResizingTextEdit, self).__init__(parent)

        # This seems to have no effect. I have expected that it will cause self.hasHeightForWidth()
        # to start returning True, but it hasn't - that's why I hardcoded it to True there anyway.
        # I still set it to True in size policy just in case - for consistency.
        size_policy = self.sizePolicy()
        size_policy.setHeightForWidth(True)
        size_policy.setVerticalPolicy(QSizePolicy.Preferred)
        self.setSizePolicy(size_policy)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setCenterOnScroll(False)
        self.verticalScrollBar().setDisabled(True)
        self.setWordWrapMode(QTextOption.WordWrap)
        self.setLineWrapMode(QPlainTextEdit.WidgetWidth)

        # self.textChanged.connect(self.updateGeometry)
        self.textChanged.connect(self.updateGeometry)
        self.textChanged.connect(self._emit_text_value_changed)

    def _emit_text_value_changed(self):
        self.textValueChanged.emit(self.toPlainText())

    def set_minimum_lines(self, num_lines):
        """ Sets minimum widget height to a value corresponding to specified number of lines
            in the default font. """

        self.setMinimumSize(self.minimumSize().width(), self.line_count2widget_height(num_lines))

    def hasHeightForWidth(self):
        return True

    def updateGeometry(self) -> None:
        super().updateGeometry()
        self.verticalScrollBar().setValue(0)

    def heightForWidth(self, width):
        margins = self.contentsMargins()

        mw = (
                margins.left() + margins.right() + self.verticalScrollBar().width() +
                self.verticalScrollBar().contentsMargins().right() + self.verticalScrollBar().contentsMargins().left()
        )

        if width >= mw:
            document_width = width - mw
        else:
            # If specified width can't even fit the margin, there's no space left for the document
            document_width = 0

        # document cloning overkill
        document = self.document().clone()
        document.setPlainText(document.toPlainText() + '\n')
        document.setTextWidth(document_width)
        document_height = document.size().height()
        document_margin = document.documentMargin()
        document.deleteLater()

        v = (
                margins.top() +
                document_height +
                document_margin +
                margins.bottom()
        )

        return v

    def sizeHint(self):
        original_hint = super(AutoResizingTextEdit, self).sizeHint()
        return QSize(original_hint.width(), self.heightForWidth(original_hint.width()))

    def line_count2widget_height(self, num_lines):
        """ Returns the number of pixels corresponding to the height of specified number of lines"""
        assert num_lines >= 0

        margins = self.contentsMargins()

        # document cloning overkill
        document = self.document().clone()
        document.setPlainText('\n' * max(num_lines - 1, 0))
        document_height = document.size().height()
        document_margin = document.documentMargin()
        document.deleteLater()

        return (
                margins.top() +
                document_height +
                document_margin +
                margins.bottom()
        )


class AutoResizingImage(QLabel):
    _pixmap: Optional[QPixmap]

    def __init__(self):
        super().__init__()
        self.setFrameStyle(QFrame.StyledPanel)
        self._pixmap = None

        size_policy = self.sizePolicy()
        size_policy.setHeightForWidth(True)
        size_policy.setHorizontalPolicy(QSizePolicy.Preferred)
        size_policy.setVerticalPolicy(QSizePolicy.Preferred)
        self.setSizePolicy(size_policy)

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        return width / self._pixmap.width() * self._pixmap.height()

    def sizeHint(self):
        hint = super().sizeHint()
        return QSize(hint.width(), self.heightForWidth(hint.width()))

    def set_image(self, img: Optional[Image]):
        if img is None:
            self._pixmap = None
        else:
            self._pixmap = QPixmap.fromImage(ImageQt(img))

    def paintEvent(self, event):
        if self._pixmap is not None:
            spix = self._pixmap.scaled(self.size(), Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
            p1 = QPoint(self.size().width(), self.size().height())
            p2 = QPoint(spix.size().width(), spix.size().height())
            QPainter(self).drawPixmap(0.5 * (p1 - p2), spix)


class HSpacer(QWidget):

    def __init__(self) -> None:
        super().__init__()
        self.setMinimumWidth(0)
        self.setMinimumHeight(0)
        self.setLayout(QHBoxLayout())
        self.layout().addItem(QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum))


class MyQWidget(QFrame):
    resized = pyqtSignal()

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        super().resizeEvent(a0)
        self.resized.emit()


class VLabel(QLabel):

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        painter = QPainter(self)
        painter.translate(self.sizeHint().width(), self.sizeHint().height())
        painter.rotate(270)
        painter.drawText(0, 0, self.text())

    def minimumSizeHint(self) -> QtCore.QSize:
        s = super().minimumSizeHint()
        return QSize(s.height(), s.width())

    def sizeHint(self) -> QtCore.QSize:
        s = super().sizeHint()
        return QSize(s.height(), s.width())


def ilen(iterable: Iterable[Any]) -> int:
    return sum(1 for _ in iterable)


def existing_single_file_dialog(mwnd: QMainWindow,
                                on_input: Callable[[Optional[Path]], None]) -> Callable[[], None]:
    def catcher():
        dlg = QFileDialog(mwnd)
        dlg.setFileMode(QFileDialog.ExistingFile)
        dlg.rejected.connect(make_action_catcher(lambda: on_input(None)))
        dlg.accepted.connect(make_action_catcher(lambda dlg=dlg: on_input(Path(dlg.selectedFiles()[0]))))
        dlg.exec()
        dlg.deleteLater()

    return catcher


def existing_multiple_files_dialog(mwnd: QMainWindow,
                                   on_input: Callable[[List[Path]], None]) -> Callable[[], None]:
    def catcher():
        dlg = QFileDialog(mwnd)
        dlg.setFileMode(QFileDialog.ExistingFiles)
        dlg.rejected.connect(make_action_catcher(lambda: on_input([])))
        dlg.accepted.connect(make_action_catcher(lambda dlg=dlg: on_input([Path(p) for p in dlg.selectedFiles()])))
        dlg.exec()
        dlg.deleteLater()

    return catcher


def new_file_dialog(mwnd: QMainWindow,
                    on_input: Callable[[Optional[Path]], None]) -> Callable[[], None]:
    def catcher():
        dlg = QFileDialog(mwnd)
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setAcceptMode(QFileDialog.AcceptSave)
        dlg.rejected.connect(make_action_catcher(lambda: on_input(None)))
        dlg.accepted.connect(make_action_catcher(lambda dlg=dlg: on_input(Path(dlg.selectedFiles()[0]))))
        dlg.exec()
        dlg.deleteLater()

    return catcher


def directory_dialog(mwnd: QMainWindow,
                     on_input: Callable[[Optional[Path]], None]) -> Callable[[], None]:
    def catcher():
        dlg = QFileDialog(mwnd)
        dlg.setFileMode(QFileDialog.Directory)
        dlg.rejected.connect(make_action_catcher(lambda: on_input(None)))
        dlg.accepted.connect(make_action_catcher(lambda dlg=dlg: on_input(Path(dlg.selectedFiles()[0]))))
        dlg.exec()
        dlg.deleteLater()

    return catcher
