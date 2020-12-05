#!/usr/bin/python

import re
import sys
import json


def reduce(line, previous_key, dictionary):
    line_p = r"""^(?P<key>[^\t]+)\t(?P<kind>[a,t,c,r])\t(?P<value>.+)$"""
    line_pattern = re.compile(line_p)

    if line_pattern.match(line):
        line_match = line_pattern.match(line)
        key = line_match.group("key")
        kind = line_match.group("kind")
        value = line_match.group("value")
    else:
        return previous_key, dictionary

    if key != previous_key:
        if previous_key != "":
            out = json.dumps(dictionary) + '\n'
            sys.stdout.buffer.write(out.encode("utf-8"))
        previous_key = key
        dictionary.clear()
        dictionary["alternative_titles"] = []
        dictionary["category"] = []

    dictionary["key"] = key

    if kind == 'a':
        dictionary["abstract"] = value
    elif kind == 'c':
        dictionary["category"].append(value)
    if kind == 'r':
        dictionary["alternative_titles"].append(value)
    elif kind == 't':
        dictionary["title"] = value

    return previous_key, dictionary


previous_link = ""
dictionary = {}
dictionary["alternative_titles"] = []
dictionary["category"] = []

for line in sys.stdin.buffer:
    line = line.decode("utf-8")
    previous_link, dictionary = reduce(line, previous_link, dictionary)

out = json.dumps(dictionary) + '\n'
sys.stdout.buffer.write(out.encode("utf-8"))
