import re

import data_preprocessor


class Parser:

    def __init__(self):

        self.titles = open("/opt/project/Data/titles.txt", "r")
        self.abstracts = open("/opt/project/Data/abstracts.txt", "r")
        self.redirects = open("/opt/project/Data/redirects.txt", "r")
        self.categories = open("/opt/project/Data/categories.txt", "r")

        self.preprocessor = data_preprocessor.DataPreprocessor()

    def parse_titles(self):
        title_p = r"""^<(?P<link>http://dbpedia\.org/resource/[^>]+)> <http://www\.w3\.org/2000/01/"""\
                  """rdf-schema#label> "(?P<title>.+)"@en \.$"""
        title_pattern = re.compile(title_p)

        for line in self.titles:
            title_match = title_pattern.match(line)
            link = title_match.group("link")
            title = re.sub(r"(\w)([A-Z])", r"\1 \2", title_match.group("title"))

            self.preprocessor.preprocess_data(link, title)

    def parse_abstracts(self):
        abstract_p = r"""^<(?P<link>http://dbpedia\.org/resource/[^>]+)> <http://www\.w3\.org/2000/01/"""\
                     """rdf-schema#comment> "(?P<abstract>.+)"@en \.$"""
        abstract_pattern = re.compile(abstract_p)

        for line in self.abstracts:
            abstract_match = abstract_pattern.match(line)
            print(abstract_match.group("link"))
            print(abstract_match.group("abstract"))
            print("################################")

    def parse_redirects(self):
        redirect_p = r"""^<http://dbpedia\.org/resource/(?P<alternative_title>[^>]+)> """\
                     """<http://dbpedia\.org/ontology/wikiPageRedirects> """\
                     """<(?P<link>http://dbpedia\.org/resource\/[^>]+)> \.$"""
        redirect_pattern = re.compile(redirect_p)

        for line in self.redirects:
            redirect_match = redirect_pattern.match(line)
            print(redirect_match.group("alternative_title"))
            print(redirect_match.group("link"))
            print("################################")

    def parse_categories(self):
        category_p = r"""^<(?P<category_link>http://dbpedia\.org/resource/[^>]+)> """\
                     """<http://www\.w3\.org/2000/01/rdf-schema#label> "(?P<category>.+)"@en \.$"""
        category_pattern = re.compile(category_p)

        for line in self.categories:
            category_match = category_pattern.match(line)
            print(category_match.group("category_link"))
            print(category_match.group("category"))
            print("################################")
