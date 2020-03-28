from typing import NamedTuple, Callable, Set, Any


class RadioButton(NamedTuple):
    caption: str
    selected: bool
    on_input: Callable[[], None] = lambda: None
    disabled: bool = False
    uid: Any = 'radio'

    def ids(self) -> Set[int]:
        return {id(self)}


class CheckBox(NamedTuple):
    caption: str
    checked: bool
    on_input: Callable[[bool], None] = lambda _: None
    disabled: bool = False
    uid: Any = 'check'

    def ids(self) -> Set[int]:
        return {id(self)}


class ProgressBar(NamedTuple):
    uid: Any
    progress: float
    suffix: str = ''
    disabled: bool = False

    def ids(self) -> Set[int]:
        return {id(self)}
