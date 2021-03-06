#!/usr/bin/python
"""mapper.py"""

import re
import sys


def parse_input(line):
    title_p = r"""^<(?P<link>http://dbpedia\.org/resource/[^>]+)> <http://www\.w3\.org/2000/01/""" \
              """rdf-schema#label> "(?P<title>.+)"@en \.$"""
    title_pattern = re.compile(title_p)

    abstract_p = r"""^<(?P<link>http://dbpedia\.org/resource/[^>]+)> <http://www\.w3\.org/2000/01/""" \
                 """rdf-schema#comment> "(?P<abstract>.+)"@en \.$"""
    abstract_pattern = re.compile(abstract_p)

    redirect_p = r"""^<(?P<alternative_link>http://dbpedia\.org/resource/[^>]+)> """ \
                 """<http://dbpedia\.org/ontology/wikiPageRedirects> """ \
                 """<(?P<real_link>http://dbpedia\.org/resource\/[^>]+)> \.$"""
    redirect_pattern = re.compile(redirect_p)

    category_p = r"""^<(?P<link>http://dbpedia\.org/resource/[^>]+)> """ \
                 """<http://purl.org/dc/terms/subject> """ \
                 """<(?P<category_link>http://dbpedia\.org/resource/Category:[^>]+)> \.$"""
    category_pattern = re.compile(category_p)

    category_title_p = r"""^<(?P<category_link>http://dbpedia\.org/resource/Category:[^>]+)> """ \
                 """<http://www\.w3\.org/2000/01/rdf-schema#label> "(?P<category_title>.+)"@en \.$"""
    category_title_pattern = re.compile(category_title_p)

    if category_title_pattern.match(line):
        category_title_match = category_title_pattern.match(line)
        category_link = category_title_match.group("category_link")
        category_title = category_title_match.group("category_title")
        output = category_link + '\t' + 'c' + '\t' + category_title + '\n'

    elif category_pattern.match(line):
        category_match = category_pattern.match(line)
        link = category_match.group("link")
        category_link = category_match.group("category_link")
        output = category_link + '\t' + 'l' + '\t' + link + '\n'

    elif abstract_pattern.match(line):
        abstract_match = abstract_pattern.match(line)
        link = abstract_match.group("link")
        abstract = abstract_match.group("abstract")
        output = link + '\t' + 'a' + '\t' + abstract + '\n'

    elif redirect_pattern.match(line):
        redirect_match = redirect_pattern.match(line)
        real_link = redirect_match.group("real_link")
        alternative_link = redirect_match.group("alternative_link")
        output = alternative_link + '\t' + 'r' + '\t' + real_link + '\n'

    elif title_pattern.match(line):
        title_match = title_pattern.match(line)
        link = title_match.group("link")

        pre_title = title_match.group("title")
        pre_title = pre_title[:-1] + pre_title[-1].lower()

        title = ' '.join(list(re.findall(r"(?![a-z]).[a-z0-9-+!'/]*", pre_title)))

        output = link + '\t' + 't' + '\t' + title + '\n'

    else:
        output = ""

    sys.stdout.buffer.write(output.encode("utf-8"))


for line in sys.stdin:
    parse_input(line)

  #cat ./Data/* | python mapper.py |
  #sort -t$'\t' -k1 -k2 |
  #python reducer_1.py | sort | python reducer_2.py | python3 reducer_3.py
