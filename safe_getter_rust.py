import logging
from typing import Any, Callable, Generic, TypeVar, Union, NoReturn

T = TypeVar("T")
E = TypeVar("E", bound=Exception)

class Ok(Generic[T,E]):
    value: T
    __match_args__ = ("_value",)
    def __init__(self, value: T):
        self.value = value

    def __repr__(self):
        return f"Ok({repr(self.value)})"

    def unwrap(self) -> T:
        return self.value

    def unwrap_or(self, default: T) -> T:
        return self.value

    def unwrap_or_else(self, op: Callable[[E], T]) -> T:
        return self.value

class Err(Generic[E]):
    def __init__(self, error: E):
        self.error = error

    def __repr__(self):
        return f"Err({repr(self.error)})"

    def unwrap(self) -> NoReturn:
        raise self.error

    def unwrap_or(self, default: T) -> T:
        return default

    def unwrap_or_else(self, op: Callable[[E], T]) -> T:
        return op(self.error)

Result = Union[Ok[T], Err[E]]


def result(func: Callable[[], T]) -> Result[T, E]:
    try:
        return Ok(func())
    except E as e:
        logging.exception('Exception occuried',exc_info=True)
        return Err(e)

# Пример функции, использующей этот механизм
def divide(x: float, y: float) -> Result[float, ZeroDivisionError]:
    if y == 0:
        return Err(ZeroDivisionError("Cannot divide by 0"))
    return Ok(x / y)
x,y=5,10
match divide(x, y):
    case Ok(v): print(f"The value is {v}")
    case Err(e): print(f"The error is {e}")

# unwrap the result and let an error be raised if the function failed
value = divide(x, y).unwrap()