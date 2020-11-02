import sys
import requests


def post_to_elastic(line):
    data = line
    data = data.encode('utf-8')

    header = {'Content-Type': 'application/json'}

    response = requests.post("http://localhost:9200/my_index/hnhn", data, headers=header)
    sys.stdout.write("The output of the URL is: " + response.text + "\n\n")


for line in sys.stdin:
    post_to_elastic(line)
