import pytest


@pytest.yield_fixture
def passwd():
    print("\n setup before yield")
    f = open("/etc/passwd")
    yield f.readlines()
    print("treardown after yield")
    f.close()


def test_has_lines(passwd):
    print("- > test called")


