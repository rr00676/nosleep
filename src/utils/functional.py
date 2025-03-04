import inspect
from functools import reduce
from typing import Callable, Any, Dict

def compose(*functions:Callable) -> Callable:
    """Left to right function composition."""
    return reduce(lambda f, g: lambda x: g(f(x)), functions, lambda x: x)


def f_kwargs(func:Callable, arg_dict:Dict[str, Any]) -> Any:
    """Calls a function with a dictionary of arguments, filtering out any that are not valid for the function."""
    sig = inspect.signature(func)
    valid_args = set(sig.parameters)
    filtered_dict = {k: v for k, v in arg_dict.items() if k in valid_args}
    return func(**filtered_dict)