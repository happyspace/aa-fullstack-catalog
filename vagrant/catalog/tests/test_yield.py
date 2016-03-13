import pytest
import os
import sys
from typing import List, Generator
import pdb

passwd = '../data/passwd'
path = os.path.join(os.path.abspath(sys.path[0]), passwd)


@pytest.yield_fixture
def passwd() -> List[str]:
    print("\n setup before yield")
    f = open(path)
    yield f.readlines()
    print("treardown after yield")
    f.close()


def test_has_lines(passwd: List[str]):
    print("- > test called")
#    pdb.set_trace()
    assert passwd


if __name__ == '__main__':
    test_has_lines(passwd)


