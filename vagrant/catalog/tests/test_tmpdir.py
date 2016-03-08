import os
import typing
from py._path import local


def test_needs_files(tmpdir: local):
    print(tmpdir)


def test_create_file(tmpdir:  local):
    p = tmpdir.mkdir("sub").join("hello.txt")
    p.write("content")
    assert p.read() == "content"
    assert len(tmpdir.listdir()) == 1
