import sys
import requests
from requests.auth import HTTPBasicAuth


def post_to_elastic(line):
    data = line
    data = data.encode('utf-8')

    header = {'Content-Type': 'application/json'}

    response = requests.post("https://2eb9ed40ed504fcf9b757fecd1d22abe.eastus2.azure.elastic-cloud.com:9243/my_index/db_page", data, headers=header, auth=HTTPBasicAuth("elastic", "qzvIrfWuaXeJtqQZ3yDtU7Fl"))
    sys.stdout.write("The output of the URL is: " + response.text + "\n\n")


for line in sys.stdin:
    post_to_elastic(line)
