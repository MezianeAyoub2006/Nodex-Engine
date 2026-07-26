from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .expression import Expression

type Value = int | float | str | bool
type Node = Union["Expression", Value]