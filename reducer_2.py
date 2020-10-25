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

    if key != previous_key:
        if previous_key != "":
            sys.stdout.write(json.dumps(dictionary) + '\n')
        previous_key = key
        dictionary.clear()
        dictionary["alternative_titles"] = []

    dictionary["key"] = key

    if kind == 'a':
        dictionary["abstract"] = value
    elif kind == 'c':
        dictionary["category"] = value
    if kind == 'r':
        dictionary["alternative_titles"].append(value)
    elif kind == 't':
        dictionary["title"] = value

    return previous_key, dictionary


previous_link = ""
dictionary = {}
dictionary["alternative_titles"] = []
for line in sys.stdin:
    previous_link, dictionary = reduce(line, previous_link, dictionary)

sys.stdout.write(json.dumps(dictionary) + '\n')
