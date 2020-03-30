from typing import Tuple, Dict, Callable, List, Any

from PIL.ImageQt import ImageQt
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QDate, QTime, QDateTime, QSize
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QSizePolicy, QLineEdit, QVBoxLayout, \
    QHBoxLayout, QGridLayout, QScrollArea, QSpacerItem, QGroupBox, QRadioButton, QCheckBox, QDateEdit, QTimeEdit, \
    QDateTimeEdit, QFrame, QComboBox, QProgressBar, QToolButton
from more_itertools import divide

from app_framework import VSplit, HSplit, Header, Text, TextInput, IntegerInput, ButtonInput, Group, \
    ScrollArea, NamedPlace, TypeSketch, Sketch, FloatInput, RadioButton, CheckBox, DateInput, TimeInput, \
    DateTimeInput, SliderInput, TextMultilineInput, ComboBoxInput, Matrix, ProgressBar, AutoImage, Feed, VText
from app_framework.sketch.layout import Column, Row, AutoColumns
from .dependency_injection import make_button_catcher, make_action_catcher
from .extra_ui import IntLineEdit, FloatLineEdit, FloatSlider, AutoResizingTextEdit, AutoResizingImage, HSpacer, VLabel, \
    MyQWidget


def make_feed(feed: Feed) -> Tuple[QWidget, Dict[int, QWidget]]:
    widget = HSpacer()
    return widget, {id(feed): widget}


def make_vsplit(vsplit: VSplit) -> Tuple[QWidget, Dict[int, QWidget]]:
    widget = QFrame()
    widget.setFrameShape(QFrame.VLine)
    widget.setFrameShadow(QFrame.Sunken)
    widget.setLineWidth(1)
    widget.setMidLineWidth(0)
    widget.setMinimumWidth(4)
    return widget, {id(vsplit): widget}


def make_hsplit(hsplit: HSplit) -> Tuple[QWidget, Dict[int, QWidget]]:
    widget = QFrame()
    widget.setFrameShape(QFrame.HLine)
    widget.setFrameShadow(QFrame.Sunken)
    widget.setLineWidth(1)
    widget.setMidLineWidth(0)
    widget.setMinimumHeight(4)
    return widget, {id(hsplit): widget}


def make_header(header: Header) -> Tuple[QWidget, Dict[int, QWidget]]:
    widget = QLabel(header.content)
    size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
    size_policy.setHorizontalStretch(0)
    size_policy.setVerticalStretch(0)
    size_policy.setHeightForWidth(widget.sizePolicy().hasHeightForWidth())
    widget.setSizePolicy(size_policy)
    font = QtGui.QFont()
    font.setPointSize(18)
    font.setBold(True)
    font.setWeight(75)
    widget.setFont(font)
    return widget, {id(header): widget}


def make_text(text: Text) -> Tuple[QWidget, Dict[int, QWidget]]:
    widget = QLabel(text.content)
    size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
    size_policy.setHorizontalStretch(0)
    size_policy.setVerticalStretch(0)
    size_policy.setHeightForWidth(widget.sizePolicy().hasHeightForWidth())
    widget.setSizePolicy(size_policy)
    return widget, {id(text): widget}


def make_vtext(vtext: VText) -> Tuple[QWidget, Dict[int, QWidget]]:
    widget = VLabel(vtext.content)
    size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
    size_policy.setHorizontalStretch(0)
    size_policy.setVerticalStretch(0)
    size_policy.setHeightForWidth(widget.sizePolicy().hasHeightForWidth())
    widget.setSizePolicy(size_policy)
    return widget, {id(vtext): widget}


def make_auto_image(auto_image: AutoImage) -> Tuple[QWidget, Dict[int, QWidget]]:
    widget = AutoResizingImage()
    widget.set_image(auto_image.image)
    if auto_image.width_range[0] is not None:
        widget.setMinimumWidth(auto_image.width_range[0])
    else:
        widget.setMinimumWidth(0)
    if auto_image.width_range[1] is not None:
        widget.setMaximumWidth(auto_image.width_range[1])
    else:
        widget.setMaximumWidth(16777215)
    if auto_image.height_range[0] is not None:
        widget.setMinimumHeight(auto_image.height_range[0])
    else:
        widget.setMinimumHeight(0)
    if auto_image.height_range[1] is not None:
        widget.setMaximumHeight(auto_image.height_range[1])
    else:
        widget.setMaximumHeight(16777215)
    return widget, {id(auto_image): widget}


def make_text_input(text_input: TextInput) -> Tuple[QWidget, Dict[int, QWidget]]:
    widget = QLineEdit(text_input.value)
    widget.setReadOnly(text_input.read_only)
    widget.textChanged[str].connect(make_action_catcher(text_input.on_input))
    return widget, {id(text_input): widget}


def make_text_multiline_input(text_multiline_input: TextMultilineInput) -> Tuple[QWidget, Dict[int, QWidget]]:
    widget = AutoResizingTextEdit()
    widget.setPlainText(text_multiline_input.value)
    widget.setReadOnly(text_multiline_input.read_only)
    widget.textValueChanged.connect(make_action_catcher(text_multiline_input.on_input))
    return widget, {id(text_multiline_input): widget}


def make_integer_input(integer_input: IntegerInput) -> Tuple[QWidget, Dict[int, QWidget]]:
    widget = IntLineEdit()
    widget.setReadOnly(integer_input.read_only)

    widget.set_value(integer_input.value)

    widget.intValueChanged.connect(make_action_catcher(integer_input.on_input))
    return widget, {id(integer_input): widget}


def make_float_input(float_input: FloatInput) -> Tuple[QWidget, Dict[int, QWidget]]:
    widget = FloatLineEdit()
    widget.setReadOnly(float_input.read_only)

    widget.set_value(float_input.value)

    widget.floatValueChanged.connect(make_action_catcher(float_input.on_input))
    return widget, {id(float_input): widget}


def make_date_input(date_input: DateInput) -> Tuple[QWidget, Dict[int, QWidget]]:
    widget = QDateEdit()

    widget.setMinimumDate(QDate(1752, 9, 14))
    widget.setMaximumDate(QDate(7999, 12, 31))
    widget.setCalendarPopup(True)

    widget.setReadOnly(date_input.read_only)
    widget.setDate(QDate(date_input.value.year, date_input.value.month, date_input.value.day))

    widget.dateChanged[QDate].connect(make_action_catcher(lambda qdt: date_input.on_input(qdt.toPyDate())))
    return widget, {id(date_input): widget}


def make_time_input(time_input: TimeInput) -> Tuple[QWidget, Dict[int, QWidget]]:
    widget = QTimeEdit()

    widget.setReadOnly(time_input.read_only)
    widget.setTime(
        QTime(time_input.value.hour, time_input.value.minute, 0, 0))

    widget.timeChanged[QTime].connect(make_action_catcher(lambda qtm: time_input.on_input(qtm.toPyTime())))
    return widget, {id(time_input): widget}


def make_date_time_input(datetime_input: DateTimeInput) -> Tuple[QWidget, Dict[int, QWidget]]:
    widget = QDateTimeEdit()

    widget.setReadOnly(datetime_input.read_only)
    widget.setDateTime(QDateTime(
        datetime_input.value.year, datetime_input.value.month, datetime_input.value.day,
        datetime_input.value.hour, datetime_input.value.minute, 0, 0
    ))
    widget.setCalendarPopup(True)

    widget.dateTimeChanged[QDateTime].connect(make_action_catcher(
        lambda qdtm: datetime_input.on_input(qdtm.toPyDateTime())))
    return widget, {id(datetime_input): widget}


def make_slider_input(slider_input: SliderInput) -> Tuple[QWidget, Dict[int, QWidget]]:
    widget = FloatSlider(slider_input.precision)

    widget.setEnabled(not slider_input.disabled)
    widget.set_range(slider_input.min_value, slider_input.max_value)
    widget.set_value(slider_input.value)

    widget.floatValueChanged.connect(make_action_catcher(slider_input.on_input))

    return widget, {id(slider_input): widget}


# def make_calendar_input(calendar_input: CalendarInput) -> Tuple[QWidget, Dict[int, QWidget]]:
#     widget = QCalendarWidget()
#
#     widget.setMinimumDate(QDate(1752, 9, 14))
#     widget.setMaximumDate(QDate(7999, 12, 31))
#     widget.setFirstDayOfWeek(Qt.Monday)
#     widget.setEnabled(False)
#
#     widget.setSelectedDate(QDate(calendar_input.value.year, calendar_input.value.month, calendar_input.value.day))
#
#     widget.selectionChanged.connect(make_action_catcher(
#         lambda: calendar_input.on_input(widget.selectedDate().toPyDate())))
#     return widget, {id(calendar_input): widget}


def make_button_input(button_input: ButtonInput) -> Tuple[QWidget, Dict[int, QWidget]]:
    widget = QToolButton()
    widget.setText(button_input.caption)
    widget.setDisabled(button_input.disabled)
    widget.clicked.connect(make_button_catcher(button_input.on_input, button_input.transition))
    if button_input.img:
        widget.setIcon(QIcon(QPixmap.fromImage(ImageQt(button_input.img))))
        widget.setIconSize(QSize(*button_input.img_size))
    return widget, {id(button_input): widget}


def make_combo_box_input(combobox_input: ComboBoxInput) -> Tuple[QWidget, Dict[int, QWidget]]:
    if combobox_input.descriptions:
        assert len(combobox_input.descriptions) == len(combobox_input.options)

    widget = QComboBox()
    widget.setSizeAdjustPolicy(QComboBox.AdjustToContents)
    widget.setDisabled(combobox_input.disabled)

    descs = combobox_input.descriptions if combobox_input.descriptions else [str(x) for x in combobox_input.options]
    widget.addItems(descs)

    current_index = combobox_input.options.index(combobox_input.value)
    widget.setCurrentIndex(current_index)

    widget.currentIndexChanged.connect(
        make_action_catcher(lambda index, cbi=combobox_input: cbi.on_input(cbi.options[index])))

    return widget, {id(combobox_input): widget}


def make_radio_button(radio_button: RadioButton) -> Tuple[QWidget, Dict[int, QWidget]]:
    widget = QRadioButton(radio_button.caption)
    widget.setEnabled(not radio_button.disabled)
    widget.setChecked(radio_button.selected)
    widget.clicked.connect(make_action_catcher(lambda _: radio_button.on_input()))
    return widget, {id(radio_button): widget}


def make_check_box(check_box: CheckBox) -> Tuple[QWidget, Dict[int, QWidget]]:
    widget = QCheckBox(check_box.caption)
    widget.setEnabled(not check_box.disabled)
    widget.setChecked(check_box.checked)
    widget.clicked[bool].connect(make_action_catcher(check_box.on_input))
    return widget, {id(check_box): widget}


def make_progress_bar(progress_bar: ProgressBar) -> Tuple[QWidget, Dict[int, QWidget]]:
    widget = QProgressBar()
    widget.setValue(int(progress_bar.progress * 100))
    widget.setFormat(f'%p% {progress_bar.suffix}')
    widget.setDisabled(progress_bar.disabled)
    return widget, {id(progress_bar): widget}


def make_group(group: Group) -> Tuple[QWidget, Dict[int, QWidget]]:
    widgets, dwidgets = build_subcomponents(group.components)
    widget = QWidget()
    assign_group_layout(group, widget, widgets)

    dwidgets[id(group)] = widget
    return widget, dwidgets


def make_matrix(matrix: Matrix) -> Tuple[QWidget, Dict[int, QWidget]]:
    widgets, dwidgets = build_subcomponents(matrix._flat)
    widget = QWidget()

    layout = QGridLayout(widget)
    for i, row in enumerate(matrix.components):
        for j, local_comp in enumerate(row):
            if local_comp is not None:
                layout.addWidget(dwidgets[id(local_comp)], i, j, 1, 1)

    dwidgets[id(matrix)] = widget
    return widget, dwidgets


def make_scroll_area(scroll_area: ScrollArea) -> Tuple[QWidget, Dict[int, QWidget]]:
    widgets, dwidgets = build_subcomponents(scroll_area.components)
    widget = QScrollArea()

    size_policy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
    size_policy.setHorizontalStretch(0)
    size_policy.setVerticalStretch(0)
    size_policy.setHeightForWidth(widget.sizePolicy().hasHeightForWidth())
    widget.setSizePolicy(size_policy)

    widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    widget.setWidgetResizable(True)
    widget.setMinimumHeight(scroll_area.min_height)
    if scroll_area._fixed_size:
        widget.setFixedHeight(scroll_area.min_height)

    widget_contents = MyQWidget()  # QWidget()
    layout = QVBoxLayout(widget_contents)
    filling_scroll_area_layout(layout, widgets)

    widget.setWidget(widget_contents)

    dwidgets[id(scroll_area)] = widget
    return widget, dwidgets


def make_named_place(named_place: NamedPlace) -> Tuple[QWidget, Dict[int, QWidget]]:
    subwidget, dwidgets = build_widget(named_place.component)
    widget = QGroupBox(named_place.title)
    layout = QVBoxLayout(widget)
    layout.addWidget(subwidget)

    if named_place.on_toggle is not None:
        widget.setCheckable(True)
        widget.setChecked(named_place.checked)
        widget.clicked[bool].connect(make_action_catcher(named_place.on_toggle))

    dwidgets[id(named_place)] = widget
    return widget, dwidgets


def build_subcomponents(components: List[Any]) -> Tuple[List[QWidget], Dict[int, QWidget]]:
    recursive_call: List[Tuple[QWidget, Dict[int, QWidget]]] = [build_widget(comp) for comp in components]
    widgets: List[QWidget] = [w for w, _ in recursive_call]
    dwidgets: Dict[int, QWidget] = {k: v for _, dw in recursive_call for k, v in dw.items()}
    return widgets, dwidgets


def assign_group_layout(group, widget, subwidgets):
    if isinstance(group.layout, Column):
        layout = QVBoxLayout(widget)
        for local_widget in subwidgets:
            layout.addWidget(local_widget)
    elif isinstance(group.layout, Row):
        layout = QHBoxLayout(widget)
        for local_widget in subwidgets:
            layout.addWidget(local_widget)
    elif isinstance(group.layout, AutoColumns):
        assert group.layout.columns > 0
        layout = QGridLayout(widget)
        splitted_widgets = [list(x) for x in divide(group.layout.columns, subwidgets)]
        for i, column in enumerate(splitted_widgets):
            for j, local_widget in enumerate(column):
                layout.addWidget(local_widget, j, i, 1, 1)
    else:
        raise Exception(f'Unknown layout {group.layout} in group {group}')
    # widget.setLayout(layout)


def filling_scroll_area_layout(layout, widgets):
    for w in widgets:
        layout.addWidget(w)
    spacer_item = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
    layout.addItem(spacer_item)


widget_builder: Dict[TypeSketch, Callable[[Sketch], Tuple[QWidget, Dict[int, QWidget]]]] = {
    Feed: make_feed,
    VSplit: make_vsplit,
    HSplit: make_hsplit,
    Header: make_header,
    Text: make_text,
    VText: make_vtext,
    TextInput: make_text_input,
    IntegerInput: make_integer_input,
    FloatInput: make_float_input,
    ButtonInput: make_button_input,
    Group: make_group,
    ScrollArea: make_scroll_area,
    NamedPlace: make_named_place,
    RadioButton: make_radio_button,
    CheckBox: make_check_box,
    DateInput: make_date_input,
    TimeInput: make_time_input,
    DateTimeInput: make_date_time_input,
    SliderInput: make_slider_input,
    TextMultilineInput: make_text_multiline_input,
    ComboBoxInput: make_combo_box_input,
    Matrix: make_matrix,
    ProgressBar: make_progress_bar,
    AutoImage: make_auto_image
    # CalendarInput: make_calendar_input
}


def build_widget(sk: Sketch) -> Tuple[QWidget, Dict[int, QWidget]]:
    return widget_builder[type(sk)](sk)
