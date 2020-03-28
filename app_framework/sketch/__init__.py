from typing import Union, Type

from .component import HSplit, VSplit, Text, Header, AutoImage, Feed, VText
from .container import Group, ScrollArea, NamedPlace, Matrix
from .input import TextInput, IntegerInput, ButtonInput, FloatInput, \
    DateInput, TimeInput, DateTimeInput, SliderInput, TextMultilineInput, \
    ComboBoxInput
from .subcomponent import RadioButton, CheckBox, ProgressBar

# from typing import TypeVar

Sketch = Union[
    HSplit, VSplit, Text, Header,
    Group, ScrollArea, NamedPlace,
    TextInput, IntegerInput, ButtonInput,
    FloatInput, RadioButton, CheckBox,
    DateInput, TimeInput, DateTimeInput,
    SliderInput, TextMultilineInput, ComboBoxInput,
    Matrix, ProgressBar, AutoImage,
    Feed, VText
    # , CalendarInput
]

# Sketch = TypeVar('Sketch',
#                  HSplit, VSplit, Text, Header,
#                  Group, ScrollArea, NamedPlace,
#                  TextInput, IntegerInput, ButtonInput
#                  )

TypeSketch = Union[
    Type[HSplit], Type[VSplit], Type[Text], Type[Header],
    Type[Group], Type[ScrollArea], Type[NamedPlace],
    Type[TextInput], Type[IntegerInput], Type[ButtonInput],
    Type[FloatInput], Type[RadioButton], Type[CheckBox],
    Type[DateInput], Type[TimeInput], Type[DateTimeInput],
    Type[SliderInput], Type[TextMultilineInput], Type[ComboBoxInput],
    Type[Matrix], Type[ProgressBar], Type[AutoImage],
    Type[Feed], Type[VText]
    # , Type[CalendarInput]
]

# TypeSketch = TypeVar('TypeSketch',
#                      Type[HSplit], Type[VSplit], Type[Text], Type[Header],
#                      Type[Group], Type[ScrollArea], Type[NamedPlace],
#                      Type[TextInput], Type[IntegerInput], Type[ButtonInput]
#                      )
