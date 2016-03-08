"""
http://pythontesting.net/framework/doctest/doctest-introduction/#example
"""
from typing import Union


def multiply(a: Union[int, str], b: Union[int, str]):
    """
    Args:
        a: Union[int, str]
        b: Union[int, str]

    Returns: Union[int, str]

    >>> multiply(4, 3)
    12
    >>> multiply('a', 3)
    """
    return a * b
