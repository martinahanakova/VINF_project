import re
import sys
import json


def reduce(line, previous_key, previous_kind, new_line):
    line_p = r"""^(?P<key>[^\t]+)\t(?P<kind>[a,t,c,r])\t(?P<value>.+)$"""
    line_pattern = re.compile(line_p)

    if line_pattern.match(line):
        line_match = line_pattern.match(line)
        key = line_match.group("key")
        kind = line_match.group("kind")
        value = line_match.group("value")

    if key != previous_key:
        if previous_key != "":
            sys.stdout.write(new_line)
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

    return previous_key, previous_kind, new_line


previous_link = ""
previous_kind = ""
new_line = ""
for line in sys.stdin:
    previous_link, previous_kind, new_line = reduce(line, previous_link, previous_kind, new_line)

sys.stdout.write(new_line)
