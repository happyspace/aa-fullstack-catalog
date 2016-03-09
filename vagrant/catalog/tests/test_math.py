from sample.unnecessary_math import multiply
import types


def setup_module(module: types.ModuleType):
    print("\b ***** setup_module module:%s" % module.__name__)


def teardown_module(module: types.ModuleType):
    print("\b ***** teardown_module   module:%s" % module.__name__)


def setup_function(function: types.FunctionType):
    print("***** setup_function    function:%s" % function.__name__)


def teardown_function(function: types.FunctionType):
    print("***** teardown_function function:%s" % function.__name__)


def test_numbers_3_4():
    print('test_numbers_3_4  <====== actual test code')
    assert(multiply(3, 4) == 12)


def test_strings_a_3():
    print('test_strings_a_3  <======= actual test code')
    assert multiply('a', 3) == 'aaa'


class TestUM:

    def setup(self):
        print("\n***** setup             class:TestStuff")

    def teardown(self):
        print("\n***** teardown          class:TestStuff")

    @classmethod
    def setup_class(cls: type):
        print("\n****** setup_class       class:%s" % cls.__name__)

    @classmethod
    def teardown_class(cls: type):
        print("\n****** teardown_class    class:%s" % cls.__name__)

    def setup_method(self, method: types.MethodType):
        print("setup_method      method:%s" % method.__name__)

    def teardown_method(self, method: types.MethodType):
        print("****** teardown_method   method:%s" % method.__name__)

    def test_numbers_5_6(self):
        print('test_numbers_5_6  <========= actual test code')
        assert multiply(5, 6) == 30

    def test_strings_b_2(self):
        print('test_strings_b_2  <========= actual test code')
        assert multiply('b', 2) == 'bb'
