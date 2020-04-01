from pathlib import Path
from threading import Lock
from typing import Any, Optional, Callable, List, Set, Dict

from .dependency_injection import GuiManage, GuiDialog, DependencyInjection
from .sketch import Sketch, Group, ScrollArea, TextInput, ButtonInput, RadioButton, CheckBox, ProgressBar
from .sketch.layout import Row, Column, AutoColumns
from .task import Task


class MetaSketch:

    def __init__(self) -> None:
        raise Exception(f"You shouldn't create instances of class {type(self)}")


class ExplorerDialogInput(MetaSketch):

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def single_file(uid: Any,
                    file: Optional[Path],
                    on_input: Callable[[Optional[Path]], None]) -> Sketch:
        dlg_action = DependencyInjection().open_file_action[0](on_input)
        return Group(('grp', uid), Row(), [
            ButtonInput(('btn', uid), 'Open file', dlg_action),
            TextInput(('txt', uid), file.as_posix() if file else 'No file selected', read_only=True)
        ])

    @staticmethod
    def directory(uid: Any,
                  file: Optional[Path],
                  on_input: Callable[[Optional[Path]], None]) -> Sketch:
        dlg_action = DependencyInjection().open_directory_action[0](on_input)
        return Group(('grp', uid), Row(), [
            ButtonInput(('btn', uid), 'Open folder', dlg_action),
            TextInput(('txt', uid), file.as_posix() if file else 'No folder selected', read_only=True)
        ])

    @staticmethod
    def new_file(uid: Any,
                 file: Optional[Path],
                 on_input: Callable[[Optional[Path]], None]) -> Sketch:
        dlg_action = DependencyInjection().save_file_action[0](on_input)
        return Group(('grp', uid), Row(), [
            ButtonInput(('btn', uid), 'Save file', dlg_action),
            TextInput(('txt', uid), file.as_posix() if file else 'No file selected', read_only=True)
        ])

    @staticmethod
    def multiple_files(uid: Any,
                       files: List[Path],
                       on_input: Callable[[List[Path]], None],
                       height=100) -> Sketch:
        dlg_action = DependencyInjection().open_multiple_files_action[0](on_input)
        if len(files) == 0:
            file_list = TextInput(('txt', uid), 'No files selected', read_only=True)
        elif len(files) == 1:
            file_list = TextInput(('txt', uid), files[0].as_posix(), read_only=True)
        elif len(files) <= 3:
            file_list = Group(('file_list', uid), Column(),
                              [
                                  TextInput((f'txt-{i}', uid), f.as_posix(), read_only=True)
                                  for i, f in enumerate(files)
                              ])
        else:
            file_list = ScrollArea(('flsca', uid), height,
                                   [
                                       TextInput((f'txt-{i}', uid), f.as_posix(), read_only=True)
                                       for i, f in enumerate(files)
                                   ])

        return Group(('grp', uid), Row(), [
            ButtonInput(('btn', uid), 'Open many files', dlg_action),
            file_list
        ])


class Selector(MetaSketch):

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def single_option(
            uid: Any,
            value: Any,
            options: List[Any],
            descriptions: Optional[List[str]] = None,
            on_input: Callable[[Any], None] = lambda _: None,
            columns: int = 3,
            disabled: bool = False
    ) -> Sketch:
        if descriptions:
            assert len(descriptions) == len(options)
        true_descs = descriptions if descriptions else [str(x) for x in options]

        return Group(('singl-op', uid), AutoColumns(columns), [
            RadioButton(idesc, value == ival, lambda ival=ival: on_input(ival), disabled, uid=('radio', ival, uid))
            for ival, idesc in zip(options, true_descs)
        ])

    @staticmethod
    def multiple_options(
            uid: Any,
            value: Set[Any],
            options: List[Any],
            descriptions: Optional[List[str]] = None,
            on_input: Callable[[Set[Any]], None] = lambda _: None,
            columns: int = 3,
            disabled: bool = False
    ) -> Sketch:
        if descriptions:
            assert len(descriptions) == len(options)
        true_descs = descriptions if descriptions else [str(x) for x in options]

        return Group(('singl-op', uid), AutoColumns(columns), [
            CheckBox(idesc, ival in value,
                     lambda cond, ival=ival: on_input(value | {ival}) if cond else on_input(value - {ival}),
                     disabled, uid=('check', ival, uid))
            for ival, idesc in zip(options, true_descs)
        ])


class TaskManager(MetaSketch):
    _ping_progress_dict: Dict[str, str] = {
        '[   ]': '[|  ]',
        '[|  ]': '[|| ]',
        '[|| ]': '[|||]',
        '[|||]': '[ ||]',
        '[ ||]': '[  |]',
        '[  |]': '[   ]',
    }

    class _TaskPing:
        suffix: str
        is_pinged: bool

        def __init__(self, suffix: str) -> None:
            self.suffix = suffix
            self.is_pinged = False

    _tasks_ping_dict: Dict[Task, _TaskPing] = {}
    _manage_lock: Lock = Lock()

    @staticmethod
    def _confirm(question: str, action: Callable[[], None]) -> None:
        if GuiDialog().yes_no_dialog(question):
            action()

    @staticmethod
    def _is_pinged_action(tp: _TaskPing, action: Callable[[], None]):
        def ping():
            tp.is_pinged = True
            action()

        return ping

    @classmethod
    def manage(cls, uid: Any, t: Task) -> Sketch:
        cls._manage_lock.acquire()

        to_del: List[Task] = []
        for it in cls._tasks_ping_dict:
            if it.state in (it.State.Done, it.State.Stop):
                to_del.append(it)
        for it in to_del:
            del cls._tasks_ping_dict[it]

        if t not in cls._tasks_ping_dict:
            cls._tasks_ping_dict[t] = cls._TaskPing(next(iter(cls._ping_progress_dict)))

        t.set_callback(
            cls._is_pinged_action(cls._tasks_ping_dict[t], GuiManage().refresh_view),
            cls._is_pinged_action(cls._tasks_ping_dict[t], GuiManage().force_refresh_view))
        comps: List[Sketch] = []
        # start button
        if t.state is t.State.Stop:
            comps.append(ButtonInput((uid, 'start-btn'), 'start', t.start))
        # pause button
        if t.state is t.State.Work and t.status is not t.Status.Cancelling:
            comps.append(ButtonInput((uid, 'pause-btn'), 'pause', t.pause, disabled=t.status is t.Status.Pausing))
        # resume button
        if t.state is t.State.Wait and t.status is not t.Status.Cancelling:
            comps.append(ButtonInput((uid, 'resume-btn'), 'resume', t.resume, disabled=t.status is t.Status.Resuming))
        # cancel button
        if t.state in (t.State.Work, t.State.Wait):
            comps.append(ButtonInput((uid, 'cancel-btn'), 'cancel',
                                     lambda t=t: cls._confirm('Do you want to cancel running task?', t.cancel),
                                     disabled=t.status is t.Status.Cancelling))
        # kill button
        if t.state in (t.State.Work, t.State.Wait):
            comps.append(ButtonInput((uid, 'kill-btn'), 'kill',
                                     lambda t=t: cls._confirm('Do you want to *kill* running task?', t.kill)))
        # ok button
        if t.state is t.State.Done:
            comps.append(ButtonInput((uid, 'ok-btn'), 'ok', t.finish))
        # progress bar
        if cls._tasks_ping_dict[t].is_pinged:
            cls._tasks_ping_dict[t].suffix = cls._ping_progress_dict[cls._tasks_ping_dict[t].suffix]
            cls._tasks_ping_dict[t].is_pinged = False
        comps.append(
            ProgressBar((uid, 'ok-btn'), t.progress, cls._tasks_ping_dict[t].suffix, t.state is not t.State.Work))

        cls._manage_lock.release()

        return Group(uid, Row(), comps)
