import re
import sys
import json
import requests
from requests.auth import HTTPBasicAuth


class Search:

    def __init__(self):
        result_link_p = r"""\"key" : "(?P<link>http:\/\/dbpedia\.org\/resource\/.+)\""""
        self.result_link_pattern = re.compile(result_link_p)

        field_query_p = r"""^(?P<field>[^:]+):(?P<query>.+)$"""
        self.field_query_pattern = re.compile(field_query_p)

        phrase_query_p = r"""^(?P<field>[^:]+):"(?P<query>.+)":?(?P<slop>[0-9]+)?$"""
        self.phrase_query_pattern = re.compile(phrase_query_p)

        bool_query_p = r"""^(?P<field>[^:]+):"(?P<query>[^"]+)" (?P<logic>AND|OR) (?P<field2>[^:]+):"(?P<query2>.+)\""""
        self.bool_query_pattern = re.compile(bool_query_p)

    def search(self, search_query):
        data = self.prepare_data(search_query)

        response = requests.get(
            "https://2eb9ed40ed504fcf9b757fecd1d22abe.eastus2.azure.elastic-cloud.com:9243/my_index/db_page/_search/?pretty",
             json=data, auth=HTTPBasicAuth("elastic", "qzvIrfWuaXeJtqQZ3yDtU7Fl"))

        results_link_match = self.result_link_pattern.findall(response.text)

        sys.stdout.write("Search results: \n")
        for result in results_link_match:
            sys.stdout.write(result + '\n')

    def prepare_data(self, search_query):
        search_request = ""

        if self.phrase_query_pattern.match(search_query):
            search_request = self.phrase_query(search_query)

        elif self.field_query_pattern.match(search_query):
            search_request = self.field_query(search_query)
        else:
            search_request = {
                "query": {
                    "multi_match": {
                        "query": search_query,
                        "fields": ["title^4", "alternative_titles^2", "abstract", "category^2"]
                    }
                }
            }

        return search_request

    def phrase_query(self, search_query):
        phrase_query_match = self.phrase_query_pattern.match(search_query)
        field = phrase_query_match.group("field")
        query = phrase_query_match.group("query")
        slop = phrase_query_match.group("slop")

        search_request = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": [field],
                    "type": "phrase",
                    "slop": slop
                }
            },
            "_source": "key"
        }

        print("phrase")

        return search_request

    def field_query(self, search_query):
        field_query_match = self.field_query_pattern.match(search_query)
        field = field_query_match.group("field")
        query = field_query_match.group("query")

        search_request = {
                "query": {
                    "match": {
                       field: query
                    }
                }
        }

        return search_request

    def bool_query(self, search_query):
        bool_query_match = self.bool_query_pattern.match(search_query)
        field = bool_query_match.group("field")
        query = bool_query_match.group("query")
        field2 = bool_query_match.group("field2")
        query2 = bool_query_match.group("query2")
        logic = bool_query_match.group("logic")

        if logic == "AND":
            search_request = {
                "query": {
                    "bool": {
                        "must": {
                            "match": { field: query }
                        }
                    }
                }
            }
        elif logic == "OR":
            search_request = {
                "query": {
                    "bool": {
                        "should": [
                            {"match": {field: query}},
                            {"match": {field2: query2}}
                        ]
                    }
                }
            }
