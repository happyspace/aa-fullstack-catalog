import pytest
from _pytest.monkeypatch import monkeypatch
import os
from smtplib import SMTP
import pdb
from typing import Tuple
from unittest.mock import MagicMock, Mock


@pytest.fixture
def smtp() -> SMTP:
    return SMTP("smtp.gmail.com")


def test_ehlo(smtp: SMTP):
    response, msg = smtp.ehlo()
    assert response == 250


@pytest.mark.parametrize('input, expected', [
    ('2 + 3', 5),
    ('6 - 4', 2),
    pytest.mark.xfail(('5 + 2', 8))
])
def test_equations(input: str, expected: Tuple[str, int]) -> bool:
    assert eval(input) == expected


def test_monkey_cwd(monkeypatch: monkeypatch):
    """
    Test monkeypatch pluggin.
    Args:
        monkeypatch (monkeypatch): injected monkeypatch
    """
    monkeypatch.setattr(os, "getcwd", lambda: "/")


def test_monkey_cwd_mock(monkeypatch: monkeypatch):
    """
    Test monkeypatch pluggin.
    Args:
        monkeypatch (monkeypatch): injected monkeypatch
    """
#    pdb.set_trace()
    cwd = Mock(return_value="/")
    monkeypatch.setattr(os, 'getcwd', cwd)








