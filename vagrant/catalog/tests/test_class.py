
class Check:
    def __init__(self):
        self.check = 'check'


class TestClass:

    def test_one(self):
        x = "this"
        assert 'h' in x

    def test_two(self):
        x = Check()
        assert hasattr(x, 'check')
