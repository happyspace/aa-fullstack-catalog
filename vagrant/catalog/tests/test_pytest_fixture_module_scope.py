import pytest
from _pytest.python import FixtureRequest
from typing import Callable, get_type_hints, Any
from types import FunctionType
import pdb


@pytest.fixture(scope='module')
def resource_fix(request: FixtureRequest):
    print('\n * resource_fix(request: FixtureRequest)')

    def resource_release():
        print('\n * resource_release()')

    request.addfinalizer(resource_release)


@pytest.fixture(scope="function", params=[1, 2])
def otherarg(request: Any):
    return request.param


def test_1_that_needs_resource_a(resource_fix: Any):
    #    pdb.set_trace()
    print('\n test_1_that_needs_resource_a()')


def test_2_that_does_not():
    print('\n test_2_that_does_not()')


def test_3_that_does(resource_fix: Any):
    print('\n test_3_that_does()')


def test_4_otherarg_decorator(otherarg):
    print('\n --> parameter is ' + str(otherarg))


@pytest.fixture()
def some_data():
    data = {'foo':1, 'bar':2, 'baz':3}
    return data


def test_foo(some_data):
    assert some_data['foo'] == 1


@pytest.fixture()
def my_fixture(request):
    print('\n-----------------')
    print('fixturename : %s' % request.fixturename)
    print('scope       : %s' % request.scope)
    print('function    : %s' % request.function.__name__)
    print('cls         : %s' % request.cls)
    print('module      : %s' % request.module.__name__)
    print('fspath      : %s' % request.fspath)
    print('-----------------')

    if request.function.__name__ == 'test_three':
        request.applymarker(pytest.mark.xfail)


def test_one(my_fixture):
    print('test_one():')


class TestClass():
    def test_two(self, my_fixture):
        print('test_two()')


def test_three(my_fixture):
    print('test_three()')
    assert False
