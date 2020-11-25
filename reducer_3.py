import sys
import requests
import json
from requests.auth import HTTPBasicAuth

import analyzer


def post_to_elastic(line):
    data = json.loads(line)

    response = requests.post(
        "https://2eb9ed40ed504fcf9b757fecd1d22abe.eastus2.azure.elastic-cloud.com:9243/test_index/_doc",
        json=data, auth=HTTPBasicAuth("elastic", "qzvIrfWuaXeJtqQZ3yDtU7Fl"))
    sys.stdout.write("The output of the URL is: " + response.text + "\n\n")


def set_analyzer(analyzer: dict):
    response = requests.put(
        "https://2eb9ed40ed504fcf9b757fecd1d22abe.eastus2.azure.elastic-cloud.com:9243/test_index/",
        json=analyzer, auth=HTTPBasicAuth("elastic", "qzvIrfWuaXeJtqQZ3yDtU7Fl"))
    sys.stdout.write("The output of the URL is: " + response.text + "\n\n")


set_analyzer(analyzer.analyzer)

for line in sys.stdin:
    post_to_elastic(line)
