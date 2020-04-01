from typing import Dict, Callable

from PIL.ImageQt import ImageQt
from PyQt5.QtCore import QDate, QTime, QDateTime
from PyQt5.QtGui import QTextCursor, QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QScrollArea, QGroupBox, QRadioButton, \
    QCheckBox, QDateEdit, QDateTimeEdit, QTimeEdit, QComboBox, QGridLayout, QProgressBar, QToolButton

from .dependency_injection import make_button_catcher, make_action_catcher, get_dwidgets
from .extra_ui import IntLineEdit, FloatLineEdit, FloatSlider, AutoResizingTextEdit, AutoResizingImage, VLabel
from .gui_builder import build_widget, assign_group_layout, filling_scroll_area_layout
from ..components import VSplit, HSplit, Header, Text, TextInput, IntegerInput, ButtonInput, Group, \
    ScrollArea, NamedPlace, TypeSketch, Sketch, FloatInput, RadioButton, CheckBox, DateInput, TimeInput, \
    DateTimeInput, SliderInput, TextMultilineInput, ComboBoxInput, Matrix, ProgressBar, AutoImage, Feed, VText


def update_dwidgets(old: Sketch, new: Sketch) -> None:
    widget: QWidget = get_dwidgets()[id(old)]
    del get_dwidgets()[id(old)]
    get_dwidgets()[id(new)] = widget


def update_feed(feed: Feed, new: Feed) -> None:
    pass


def update_vsplit(vsplit: VSplit, new: VSplit) -> None:
    pass


def update_hsplit(hsplit: HSplit, new: HSplit) -> None:
    pass


def update_header(header: Header, new: Header) -> None:
    # noinspection PyTypeChecker
    widget: QLabel = get_dwidgets()[id(header)]
    if header.content != new.content:
        widget.setText(new.content)


def update_text(text: Text, new: Text) -> None:
    # noinspection PyTypeChecker
    widget: QLabel = get_dwidgets()[id(text)]
    if text.content != new.content:
        widget.setText(new.content)


def update_vtext(vtext: VText, new: VText) -> None:
    # noinspection PyTypeChecker
    widget: VLabel = get_dwidgets()[id(vtext)]
    if vtext.content != new.content:
        widget.setText(new.content)


def update_auto_image(auto_image: AutoImage, new: AutoImage) -> None:
    # noinspection PyTypeChecker
    widget: AutoResizingImage = get_dwidgets()[id(auto_image)]
    if auto_image.image != new.image:
        widget.set_image(new.image)
    if auto_image.width_range[0] != new.width_range[0]:
        if new.width_range[0] is not None:
            widget.setMinimumWidth(new.width_range[0])
        else:
            widget.setMinimumWidth(0)
    if auto_image.width_range[1] != new.width_range[1]:
        if new.width_range[1] is not None:
            widget.setMaximumWidth(new.width_range[1])
        else:
            widget.setMaximumWidth(16777215)
    if auto_image.height_range[0] != new.height_range[0]:
        if new.height_range[0] is not None:
            widget.setMinimumHeight(new.height_range[0])
        else:
            widget.setMinimumHeight(0)
    if auto_image.height_range[1] != new.height_range[1]:
        if new.height_range[1] is not None:
            widget.setMaximumHeight(new.height_range[1])
        else:
            widget.setMaximumHeight(16777215)


def update_text_input(text_input: TextInput, new: TextInput) -> None:
    # noinspection PyTypeChecker
    widget: QLineEdit = get_dwidgets()[id(text_input)]
    widget.blockSignals(True)

    if text_input.value != new.value:
        pos = widget.cursorPosition()
        widget.setText(new.value)
        widget.setCursorPosition(min(pos, len(widget.text())))
    if text_input.read_only != new.read_only:
        widget.setReadOnly(new.read_only)
    if text_input.on_input != new.on_input:
        widget.textChanged[str].disconnect()
        widget.textChanged[str].connect(make_action_catcher(new.on_input))

    widget.blockSignals(False)


def update_text_multiline_input(text_multiline_input: TextMultilineInput, new: TextMultilineInput) -> None:
    # noinspection PyTypeChecker
    widget: AutoResizingTextEdit = get_dwidgets()[id(text_multiline_input)]
    widget.blockSignals(True)

    if text_multiline_input.value != new.value:
        pos = widget.textCursor().position()
        widget.setPlainText(new.value)
        cursor = QTextCursor(widget.textCursor())
        cursor.setPosition(pos, QTextCursor.MoveAnchor)
        # widget.textCursor().setPosition(min(pos, len(widget.toPlainText())))
        widget.setTextCursor(cursor)
    if text_multiline_input.read_only != new.read_only:
        widget.setReadOnly(new.read_only)
    if text_multiline_input.on_input != new.on_input:
        widget.textValueChanged.disconnect()
        widget.textValueChanged.connect(make_action_catcher(new.on_input))

    widget.blockSignals(False)


def update_integer_input(integer_input: IntegerInput, new: IntegerInput) -> None:
    # noinspection PyTypeChecker
    widget: IntLineEdit = get_dwidgets()[id(integer_input)]
    widget.blockSignals(True)

    if integer_input.read_only != new.read_only:
        widget.setReadOnly(new.read_only)

    if integer_input.value != new.value:
        pos = widget.cursorPosition()
        widget.set_value(new.value)
        widget.setCursorPosition(min(pos, len(widget.text())))

    if integer_input.on_input != new.on_input:
        widget.intValueChanged.disconnect()
        widget.intValueChanged.connect(make_action_catcher(new.on_input))

    widget.blockSignals(False)


def update_float_input(float_input: FloatInput, new: FloatInput) -> None:
    # noinspection PyTypeChecker
    widget: FloatLineEdit = get_dwidgets()[id(float_input)]
    widget.blockSignals(True)

    if float_input.read_only != new.read_only:
        widget.setReadOnly(new.read_only)

    if float_input.value != new.value:
        pos = widget.cursorPosition()
        widget.set_value(new.value)
        widget.setCursorPosition(min(pos, len(widget.text())))

    if float_input.on_input != new.on_input:
        widget.floatValueChanged.disconnect()
        widget.floatValueChanged.connect(make_action_catcher(new.on_input))

    widget.blockSignals(False)


def update_date_input(date_input: DateInput, new: DateInput) -> None:
    # noinspection PyTypeChecker
    widget: QDateEdit = get_dwidgets()[id(date_input)]
    widget.blockSignals(True)

    if date_input.read_only != new.read_only:
        widget.setReadOnly(new.read_only)

    if date_input.value != new.value:
        widget.setDate(QDate(new.value.year, new.value.month, new.value.day))

    if date_input.on_input != new.on_input:
        widget.dateChanged.disconnect()
        widget.dateChanged[QDate].connect(make_action_catcher(lambda qdt: new.on_input(qdt.toPyDate())))

    widget.blockSignals(False)


def update_time_input(time_input: TimeInput, new: TimeInput) -> None:
    # noinspection PyTypeChecker
    widget: QTimeEdit = get_dwidgets()[id(time_input)]
    widget.blockSignals(True)

    if time_input.read_only != new.read_only:
        widget.setReadOnly(new.read_only)

    if time_input.value != new.value:
        widget.setTime(QTime(new.value.hour, new.value.minute, 0, 0))

    if time_input.on_input != new.on_input:
        widget.timeChanged.disconnect()
        widget.timeChanged[QTime].connect(make_action_catcher(lambda qtm: time_input.on_input(qtm.toPyTime())))

    widget.blockSignals(False)


def update_date_time_input(datetime_input: DateTimeInput, new: DateTimeInput) -> None:
    # noinspection PyTypeChecker
    widget: QDateTimeEdit = get_dwidgets()[id(datetime_input)]
    widget.blockSignals(True)

    if datetime_input.read_only != new.read_only:
        widget.setReadOnly(new.read_only)

    if datetime_input.value != new.value:
        widget.setDateTime(QDateTime(
            new.value.year, new.value.month, new.value.day,
            new.value.hour, new.value.minute, 0, 0
        ))

    if datetime_input.on_input != new.on_input:
        widget.dateTimeChanged.disconnect()
        widget.dateTimeChanged[QDateTime].connect(make_action_catcher(
            lambda qdtm: datetime_input.on_input(qdtm.toPyDateTime())))

    widget.blockSignals(False)


def update_slider_input(slider_input: SliderInput, new: SliderInput) -> None:
    # noinspection PyTypeChecker
    widget: FloatSlider = get_dwidgets()[id(slider_input)]
    widget.blockSignals(True)

    if slider_input.precision != new.precision:
        widget.set_precision(new.precision)

    if (slider_input.min_value, slider_input.max_value) != (new.min_value, new.max_value):
        widget.set_range(new.min_value, new.max_value)

    if slider_input.value != new.value:
        widget.set_value(new.value)

    if slider_input.disabled != new.disabled:
        widget.setEnabled(not new.disabled)

    # if slider_input.on_input != new.on_input:
    widget.floatValueChanged.disconnect()
    widget.floatValueChanged.connect(make_action_catcher(new.on_input))

    widget.blockSignals(False)


# def update_calendar_input(calendar_input: CalendarInput, new: CalendarInput) -> None:
#     # noinspection PyTypeChecker
#     widget: QCalendarWidget = get_dwidgets()[id(calendar_input)]
#     widget.blockSignals(True)
#
#     if calendar_input.value != new.value:
#         widget.setSelectedDate(QDate(new.value.year, new.value.month, new.value.day))
#
#     if calendar_input.on_input is not new.on_input:
#         widget.selectionChanged.disconnect()
#         widget.selectionChanged.connect(make_action_catcher(
#             lambda: calendar_input.on_input(widget.selectedDate().toPyDate())))
#
#     widget.blockSignals(False)
#     update_dwidgets(calendar_input, new)


def update_button_input(button_input: ButtonInput, new: ButtonInput) -> None:
    # noinspection PyTypeChecker
    widget: QToolButton = get_dwidgets()[id(button_input)]

    if button_input.caption != new.caption:
        widget.setText(new.caption)
    if button_input.disabled != new.disabled:
        widget.setDisabled(new.disabled)
    if (button_input.on_input != new.on_input) or (button_input.transition != new.transition):
        widget.clicked.disconnect()
        widget.clicked.connect(make_button_catcher(new.on_input, new.transition))
    if button_input.img != new.img:
        widget.setIcon(QIcon(QPixmap.fromImage(ImageQt(new.img))))
    if button_input.img_size != new.img_size:
        widget.setIconSize(*new.img_size)


def update_combo_box_input(combobox_input: ComboBoxInput, new: ComboBoxInput) -> None:
    # noinspection PyTypeChecker
    widget: QComboBox = get_dwidgets()[id(combobox_input)]

    if new.descriptions:
        assert len(new.descriptions) == len(new.options)

    widget.blockSignals(True)

    if combobox_input.disabled != new.disabled:
        widget.setDisabled(new.disabled)

    descs = combobox_input.descriptions if combobox_input.descriptions else [str(x) for x in combobox_input.options]
    new_descs = new.descriptions if new.descriptions else [str(x) for x in new.options]
    if descs != new_descs:
        widget.clear()
        widget.addItems(new_descs)

    current_index = new.options.index(new.value)
    widget.setCurrentIndex(current_index)

    if combobox_input.on_input != new.on_input or combobox_input.options != new.options:
        widget.currentIndexChanged.disconnect()
        widget.currentIndexChanged.connect(
            make_action_catcher(lambda index, cbi=new: cbi.on_input(cbi.options[index])))

    widget.blockSignals(False)


def update_radio_button(radio_button: RadioButton, new: RadioButton) -> None:
    # noinspection PyTypeChecker
    widget: QRadioButton = get_dwidgets()[id(radio_button)]

    if radio_button.selected != new.selected:
        widget.setChecked(new.selected)
    if radio_button.caption != new.caption:
        widget.setText(new.caption)
    if radio_button.disabled != new.disabled:
        widget.setEnabled(not new.disabled)
    if radio_button.on_input != new.on_input:
        widget.clicked.disconnect()
        widget.clicked.connect(make_action_catcher(lambda _: new.on_input()))


def update_check_box(check_box: CheckBox, new: CheckBox) -> None:
    # noinspection PyTypeChecker
    widget: QCheckBox = get_dwidgets()[id(check_box)]

    if check_box.checked != new.checked:
        widget.setChecked(new.checked)
    if check_box.caption != new.caption:
        widget.setText(new.caption)
    if check_box.disabled != new.disabled:
        widget.setEnabled(not new.disabled)
    if check_box.on_input != new.on_input:
        widget.clicked.disconnect()
        widget.clicked.connect(make_action_catcher(new.on_input))


def update_progress_bar(progress_bar: ProgressBar, new: ProgressBar) -> None:
    # noinspection PyTypeChecker
    widget: QProgressBar = get_dwidgets()[id(progress_bar)]

    if progress_bar.progress != new.progress:
        widget.setValue(int(new.progress * 100))
    if progress_bar.suffix != new.suffix:
        widget.setFormat(f'%p% {new.suffix}')
    if progress_bar.disabled != new.disabled:
        widget.setDisabled(new.disabled)


def update_group(group: Group, new: Group) -> None:
    widget: QWidget = get_dwidgets()[id(group)]

    orig_uids = [(type(x), x.uid) for x in group.components]
    new_uids = [(type(x), x.uid) for x in new.components]
    if (orig_uids != new_uids) or (not isinstance(group.layout, type(new.layout))) or (group.layout != new.layout):
        old_layout = widget.layout()
        for comp in group.components:
            old_layout.removeWidget(get_dwidgets()[id(comp)])

        refresh_subcomponents(group._dict_components, new._dict_components)

        # rebuild layout
        tmp = QWidget()
        tmp.setLayout(old_layout)
        widgets = [get_dwidgets()[id(comp)] for comp in new.components]
        assign_group_layout(new, widget, widgets)
        old_layout.deleteLater()
    else:
        for new_comp in new.components:
            comp = group._dict_components[new_comp.uid]
            refresh_widget(comp, new_comp)


def update_matrix(matrix: Matrix, new: Matrix) -> None:
    widget: QWidget = get_dwidgets()[id(matrix)]

    orig_uids = [(type(x), x.uid, i, j)
                 for i, row in enumerate(matrix.components)
                 for j, x in enumerate(row)
                 if x is not None]
    new_uids = [(type(x), x.uid, i, j)
                for i, row in enumerate(new.components)
                for j, x in enumerate(row)
                if x is not None]
    if orig_uids != new_uids:
        old_layout = widget.layout()
        for comp in matrix._flat:
            old_layout.removeWidget(get_dwidgets()[id(comp)])

        refresh_subcomponents(matrix._dict_components, new._dict_components)

        # rebuild layout
        tmp = QWidget()
        tmp.setLayout(old_layout)

        layout = QGridLayout(widget)
        for i, row in enumerate(new.components):
            for j, local_comp in enumerate(row):
                if local_comp is not None:
                    layout.addWidget(get_dwidgets()[id(local_comp)], i, j, 1, 1)

        old_layout.deleteLater()
    else:
        for new_comp in new._flat:
            comp = matrix._dict_components[new_comp.uid]
            refresh_widget(comp, new_comp)


def update_scroll_area(scroll_area: ScrollArea, new: ScrollArea) -> None:
    assert scroll_area._fixed_size == new._fixed_size

    # noinspection PyTypeChecker
    widget: QScrollArea = get_dwidgets()[id(scroll_area)]

    orig_uids = [(type(x), x.uid) for x in scroll_area.components]
    new_uids = [(type(x), x.uid) for x in new.components]
    if orig_uids != new_uids:
        layout = widget.widget().layout()
        for comp in scroll_area.components:
            layout.removeWidget(get_dwidgets()[id(comp)])

        # delete vertical feed
        layout.takeAt(0)

        refresh_subcomponents(scroll_area._dict_components, new._dict_components)

        # rebuild layout
        widgets = [get_dwidgets()[id(comp)] for comp in new.components]
        filling_scroll_area_layout(layout, widgets)
    else:
        for new_comp in new.components:
            comp = scroll_area._dict_components[new_comp.uid]
            refresh_widget(comp, new_comp)

    if scroll_area.min_height != new.min_height:
        widget.setMinimumHeight(new.min_height)
        if new._fixed_size:
            widget.setFixedHeight(new.min_height)


def update_named_place(named_place: NamedPlace, new: NamedPlace) -> None:
    # noinspection PyTypeChecker
    widget: QGroupBox = get_dwidgets()[id(named_place)]

    layout = widget.layout()
    layout.removeWidget(get_dwidgets()[id(named_place.component)])

    # quad dmg 0v3rki11 XD
    old_dict_components = {named_place.component.uid: named_place.component}
    new_dict_components = {new.component.uid: new.component}
    refresh_subcomponents(old_dict_components, new_dict_components)

    # rebuild layout
    layout.addWidget(get_dwidgets()[id(new.component)])

    # refreshing named_place itself
    if named_place.title != new.title:
        widget.setTitle(new.title)

    if named_place.on_toggle != new.on_toggle:
        widget.setCheckable(False)
        widget.clicked[bool].disconnect()
        if new.on_toggle is not None:
            widget.setCheckable(True)
            widget.setChecked(new.checked)
            widget.clicked[bool].connect(make_action_catcher(new.on_toggle))


def detect_subcomponents_changes(old_dict_components, new_dict_components):
    existed = set(old_dict_components.keys())
    proposed = set(new_dict_components.keys())
    removed = existed - proposed
    added = proposed - existed
    saved = existed & proposed
    for uid in list(saved):
        if not isinstance(old_dict_components[uid], type(new_dict_components[uid])):
            saved.discard(uid)
            added.add(uid)
            removed.add(uid)
    return added, saved, removed


def create_new_widgets(added, new_dict_components):
    dwidgets = get_dwidgets()
    for uid in added:
        comp = new_dict_components[uid]
        _, local_dwidgets = build_widget(comp)
        for comp_id, widget in local_dwidgets.items():
            dwidgets[comp_id] = widget


def update_saved_components(saved, old_dict_components, new_dict_components):
    for uid in saved:
        comp = old_dict_components[uid]
        new_comp = new_dict_components[uid]
        refresh_widget(comp, new_comp)


def delete_removed_widgets(removed, old_dict_components):
    dwidgets = get_dwidgets()
    for uid in removed:
        comp = old_dict_components[uid]
        dwidgets[id(comp)].deleteLater()
        for comp_id in comp.ids():
            del dwidgets[comp_id]


def refresh_subcomponents(old_dict_components, new_dict_components):
    added, saved, removed = detect_subcomponents_changes(old_dict_components, new_dict_components)
    create_new_widgets(added, new_dict_components)
    update_saved_components(saved, old_dict_components, new_dict_components)
    delete_removed_widgets(removed, old_dict_components)


widget_refresher: Dict[TypeSketch, Callable[[Sketch, Sketch], None]] = {
    Feed: update_feed,
    VSplit: update_vsplit,
    HSplit: update_hsplit,
    Header: update_header,
    Text: update_text,
    VText: update_vtext,
    TextInput: update_text_input,
    IntegerInput: update_integer_input,
    FloatInput: update_float_input,
    ButtonInput: update_button_input,
    Group: update_group,
    ScrollArea: update_scroll_area,
    NamedPlace: update_named_place,
    RadioButton: update_radio_button,
    CheckBox: update_check_box,
    DateInput: update_date_input,
    TimeInput: update_time_input,
    DateTimeInput: update_date_time_input,
    SliderInput: update_slider_input,
    TextMultilineInput: update_text_multiline_input,
    ComboBoxInput: update_combo_box_input,
    Matrix: update_matrix,
    ProgressBar: update_progress_bar,
    AutoImage: update_auto_image
    # CalendarInput: update_calendar_input
}


def refresh_widget(original: Sketch, new: Sketch) -> None:
    widget_refresher[type(original)](original, new)
    update_dwidgets(original, new)
