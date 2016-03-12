"""
 source: https://github.com/okken/markdown.py

 Updated for PEP 8,

Software API adapter for markdown.py
This module provides a function based API to markdown.py
since markdown.py only provides a CLI.
"""

from subprocess import Popen, PIPE, STDOUT
from tempfile import NamedTemporaryFile
import os
import sys

# This is here so there's one line to change if I want to swap 
# out a different script, such as markdown.pl

# for this context (tox) relative to the execution.
script = '..\sample\markdown.py'
path = os.path.join(os.path.abspath(sys.path[0]), script)
_interpreter_and_script = ['python', path]


def run_markdown(input_text: str):
    """
    The default method when we don't care which method to use.

    Args:
        input_text: str
    """
    return run_markdown_pipe(input_text)


def run_markdown_pipe(input_text: str):
    """
    Simulate: echo 'some input' | python markdown.py 

    Args:
        input_text: str
    """
    pipe = Popen(_interpreter_and_script,
                 stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    output = pipe.communicate(input=bytes(input_text, 'utf-8'))[0]
    return output.rstrip().decode('utf-8')


def run_markdown_file(input_text: str):
    """
    Simulate: python markdown.py fileName

    Args:
        input_text: str
    """
    temp_file = NamedTemporaryFile(delete=False)
    temp_file.write(input_text)
    temp_file.close()
    interp_script_and_filename = _interpreter_and_script
    interp_script_and_filename.append(temp_file.name)
    pipe = Popen(interp_script_and_filename,
                 stdout=PIPE, stderr=STDOUT)
    output = pipe.communicate()[0]
    os.unlink(temp_file.name)
    return output.rstrip()
