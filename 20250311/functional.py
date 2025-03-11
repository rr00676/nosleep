import inspect
from functools import reduce, partial
from typing import Callable, Any, Dict

def compose(*functions:Callable) -> Callable:
    """Left to right function composition."""
    return reduce(lambda f, g: lambda x: g(f(x)), functions, lambda x: x)


def filter_kwargs(func:Callable, arg_dict:Dict[str, Any]) -> Dict[str, Any]:
    """Filters a dictionary of arguments to only include those that are valid for the function."""
    valid_args = set(inspect.signature(func).parameters)
    return {k: v for k, v in arg_dict.items() if k in valid_args}

def f_kwargs(func:Callable, arg_dict:Dict[str, Any]) -> Any:
    """Calls a function with a dictionary of arguments, filtering out any that are not valid for the function."""
    return func(**filter_kwargs(func, arg_dict))

def partial_kwargs(func:Callable, arg_dict:Dict[str, Any]) -> Any:
    """Calls a function with a dictionary of arguments, filtering out any that are not valid for the function."""
    return partial(func, **filter_kwargs(func, arg_dict))