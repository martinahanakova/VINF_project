#!/usr/bin/python

import re
import sys


def reduce(line, previous_key, previous_kind, new_line, category_name):
    line_p = r"""^(?P<key>[^\t]+)\t(?P<kind>[a,t,c,r,l])\t(?P<value>.+)$"""
    line_pattern = re.compile(line_p)

    if line_pattern.match(line):
        line_match = line_pattern.match(line)
        key = line_match.group("key")
        kind = line_match.group("kind")
        value = line_match.group("value")
    else:
        return previous_key, previous_kind, new_line, category_name

    if key != previous_key:
        if previous_key != "" and previous_kind != 'r' and previous_kind != 'c':
            sys.stdout.buffer.write(new_line.encode("utf-8"))
        previous_key = key
        previous_kind = kind
        new_line = ""
        category_name = ""

    if key == previous_key:
        if previous_kind == 'a':
            sys.stdout.buffer.write(new_line.encode("utf-8"))
            previous_key = key
            previous_kind = kind
            new_line = ""
        elif previous_kind == 'l':
            sys.stdout.buffer.write(new_line.encode("utf-8"))
            previous_key = key
            previous_kind = kind
            new_line = ""

    if kind == 'r':
        new_line = value + '\tr\t'
    elif kind == 't':
        if previous_kind == 'r':
            new_line = new_line + value + '\n'
        else:
            new_line = key + '\t' + kind + '\t' + value + '\n'
    elif kind == 'c':
        category_name = value
    elif kind == 'l':
        if category_name != "":
            new_line = value + '\t' + 'c' + '\t' + category_name + '\n'
    else:
        new_line = key + '\t' + kind + '\t' + value + '\n'

    previous_kind = kind

    return previous_key, previous_kind, new_line, category_name


previous_link = ""
previous_kind = ""
new_line = ""
category_name = ""
for line in sys.stdin.buffer:
    line = line.decode("utf-8")
    previous_link, previous_kind, new_line, category_name = \
        reduce(line, previous_link, previous_kind, new_line, category_name)

sys.stdout.buffer.write(new_line.encode("utf-8"))
