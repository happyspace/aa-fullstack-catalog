from sample.markdown_adapter import run_markdown
import pytest
from _pytest.python import FixtureRequest
from typing import Tuple
import getpass
import time
import os
import pdb


def test_non_marked_lines():
    print('in test_non_marked_lines')
    assert run_markdown('this line has no special handling') == \
        '<p>this line has no special handling</p>'


def test_em():
    print('in test_em')
    assert run_markdown('*this should be wrapped in em tags*') == \
        '<p><em>this should be wrapped in em tags</em></p>'


def test_strong():
    print('in test_strong')
    assert run_markdown('**this should be wrapped in strong tags**') == \
        '<p><strong>this should be wrapped in strong tags</strong></p>'


@pytest.fixture( params=[
    # tuple with (input, expectedOutput)
    ('regular text', '<p>regular text</p>'),
    ('*em tags*', '<p><em>em tags</em></p>'),
    ('**strong tags**', '<p><strong>strong tags</strong></p>')
    ])
def test_data(request: FixtureRequest) -> Tuple[str, str]:
    return request.param


def test_markdown(test_data: Tuple[str, str]):
    (the_input, the_expected_output) = test_data
    the_output = run_markdown(the_input)
    print('\n test_markdown():')
    print('  input   : %s' % the_input)
    print('  output  : %s' % the_output)
    print('  expected: %s' % the_expected_output)
    assert the_output == the_expected_output


@pytest.fixture(scope="module", autouse=True)
def mod_header(request):
    pdb.set_trace()
    print(os.environ.get("USERNAME"))
    print(os.environ.get("PATH"))
    print('\n-----------------')
    print('user        : %s' % getpass.getuser())
    print('module      : %s' % request.module.__name__)
    print('-----------------')


@pytest.fixture(scope="function", autouse=True)
def func_header(request):
    print('\n-----------------')
    print('function    : %s' % request.function.__name__)
    print('time        : %s' % time.asctime())
    print('-----------------')


def test_one():
    print('in test_one()')


def test_two():
    print('in test_two()')
