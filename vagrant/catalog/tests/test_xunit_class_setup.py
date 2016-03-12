

def resource_setup():
    print('*** resources_setup()')


def resource_teardown():
    print('*** resources_teardown()')


class TestClassXunit:

    @classmethod
    def setup_class(cls):
        print('\n setup_class(cls)')
        resource_setup()

    @classmethod
    def teardown_class(cls):
        print('\n teardown_class(cls)')

    def test_needs_resource(self):
        print('\n test_needs_resource(self) ')


def test_that_does_not():
    print('\n test_that_does_not()')
