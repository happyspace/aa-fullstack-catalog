"""
 source: https://github.com/okken/markdown.py

 Updated for Python 3, PEP 8, type hints and
 remove shadowing (even though silly in this case).

 Markdown.py
 0. just print whatever is passed in to stdin
 0. if filename passed in as a command line parameter, 
    then print file instead of stdin
 1. wrap input in paragraph tags
 2. convert single asterisk or underscore pairs to em tags
 3. convert double asterisk or underscore pairs to strong tags

"""

import fileinput
import re


def convert_strong(md_line: str):
    md_line = re.sub(r'\*\*(.*)\*\*', r'<strong>\1</strong>', md_line)
    md_line = re.sub(r'__(.*)__', r'<strong>\1</strong>', md_line)
    return md_line


def convert_em(md_line: str):
    md_line = re.sub(r'\*(.*)\*', r'<em>\1</em>', md_line)
    md_line = re.sub(r'_(.*)_', r'<em>\1</em>', md_line)
    return md_line

if __name__ == '__main__':
    for line in fileinput.input():
        line = line.rstrip()
        line = convert_strong(line)
        line = convert_em(line)
        print('<p>' + line + '</p>')
