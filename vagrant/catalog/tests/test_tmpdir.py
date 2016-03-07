import os

import py


def test_needs_files(tmpdir: py.path.local):
    print(tmpdir)


def test_create_file(tmpdir:  py.path.local):
    p = tmpdir.mkdir("sub").join("hello.txt")
    p.write("content")
    assert p.read() == "content"
    assert len(tmpdir.listdir()) == 1


