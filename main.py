import sys
import search


if __name__ == '__main__':

    search = search.Search()

    while True:
        sys.stdout.write("Type your search: ")

        search_query = sys.stdin.readline()
        search.search(search_query)
