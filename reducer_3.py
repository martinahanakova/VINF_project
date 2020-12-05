#!/usr/bin/python

import sys
import requests
import json
from requests.auth import HTTPBasicAuth

import analyzer


def post_to_elastic(line):
    data = json.loads(line)

    response = requests.post(
        "https://e6fbbd886c5b4eea9f2230c887a4e4d3.eastus2.azure.elastic-cloud.com:9243/vinf_index/_doc",
        json=data, auth=HTTPBasicAuth("elastic", "sroyNGq5cNz7irv4TV8Iot6Q"))
    sys.stdout.write("The output of the URL is: " + response.text + "\n\n")


def set_analyzer(analyzer: dict):
    response = requests.put(
        "https://e6fbbd886c5b4eea9f2230c887a4e4d3.eastus2.azure.elastic-cloud.com:9243/vinf_index/",
        json=analyzer, auth=HTTPBasicAuth("elastic", "sroyNGq5cNz7irv4TV8Iot6Q"))
    sys.stdout.write("The output of the URL is: " + response.text + "\n\n")


def batch_post(data):
    response = requests.post(
        url="https://e6fbbd886c5b4eea9f2230c887a4e4d3.eastus2.azure.elastic-cloud.com:9243/_bulk",
        data=data, auth=HTTPBasicAuth("elastic", "sroyNGq5cNz7irv4TV8Iot6Q"),
        headers={'Content-Type': 'application/x-ndjson'})
    sys.stdout.write("The output of the URL is: " + response.text + "\n\n")


set_analyzer(analyzer.analyzer)
request = {"index": {"_index": "vinf_index"}}
data = ""
count = 0

for line in sys.stdin:
    count += 1
    data = data + json.dumps(request) + '\n' + line + '\n'
    if count == 1000:
        count = 0
        batch_post(data)
        data = ""

if data != "":
    batch_post(data)
