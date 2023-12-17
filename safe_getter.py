import logging
from typing import Callable, List, Tuple, Any, Optional

def try_gete(func: Callable[[], Any], default: Any = None, log_exc: bool = False) -> Tuple[Any, Optional[Exception]]:
    """
    Execute a function and return its result and any caught exception.

    Args:
        func: The function to execute.
        default: The default value to return in case of exception.
        log_exc: Flag to log the exception.

    Returns:
        A tuple containing the result of the function or the default value, and the caught exception or None.
    """
    try:
        result = func()
        return (result if result is not None else default), None
    except Exception as e:
        if log_exc:
            logging.error('An error occurred', exc_info=True)
        return default, e

def try_get(func: Callable[[], Any], default: Any = None, return_exception: bool = False, **kwargs) -> Any:
    """
    Execute a function and return its result, or an exception if requested.

    Args:
        func: The function to execute.
        default: The default value to return in case of exception.
        return_exception: Return the caught exception instead of the default value.

    Returns:
        The result of the function, the default value, or the exception.
    """
    result, exception = try_gete(func, default, **kwargs)
    return exception if return_exception and exception is not None else result

def try_geta(arr: List[Any], func: Callable[[Any], Any], skip_none: bool = True, default_element: Any = None) -> List[Any]:
    """
    Apply a function to each element in a list and return the results.

    Args:
        arr: The list to process.
        func: The function to apply to each element.
        skip_none: Skip elements that result in None.
        default_element: Default element to use in case of exception.

    Returns:
        A list of results.
    """
    return [x for elem in arr for x in [try_get(lambda: func(elem), default_element)] if not (x is None and skip_none)]

def try_get_attrs(obj_func: Callable[[], Any], attrs: List[str], defaults: List[Any]) -> Tuple[Any, ...]:
    """
    Get attributes from an object returned by a callable.

    Args:
        obj_func: A function that returns an object.
        attrs: Attribute names to retrieve.
        defaults: Default values for each attribute.

    Returns:
        A tuple of attribute values or defaults.
    """
    if len(attrs) != len(defaults):
        raise ValueError("attrs and defaults must have the same length.")
    obj = try_get(obj_func)
    return tuple(getattr(obj, attr, default) for attr, default in zip(attrs, defaults))

def apply_to_list(lst: List[Any], func: Callable[[Any], Any], filter_func: Optional[Callable[[Any], bool]] = None, return_all: bool = True) -> List[Any]:
    """
    Apply a function to each element of a list and return the results.

    Args:
        lst: The list to process.
        func: The function to apply.
        filter_func: An optional filter function.
        return_all: Return all results or only non-None.

    Returns:
        A list of results.
    """
    return [result for item in lst if filter_func is None or filter_func(item) for result in [try_get(lambda: func(item))] if return_all or result is not None]
