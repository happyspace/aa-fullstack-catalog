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


def test_1_that_needs_resource_a(otherarg: Any):
    if otherarg:
        th = get_type_hints(resource_fix)
#    pdb.set_trace()
    print('\n test_1_that_needs_resource_a()')


def test_2_that_does_not():
    print('\n test_2_that_does_not()')


def test_3_that_does(otherarg: Any):
    print('\n test_3_that_does()' + resource_fix.__name__)


if __name__ == '__main__':
    test_1_that_needs_resource_a(resource_fix)

