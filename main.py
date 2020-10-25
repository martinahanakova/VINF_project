import parser


if __name__ == '__main__':

    parser = parser.Parser()

    # parse datasets
    parser.parse_titles()

    parser.parse_abstracts()
    #parser.parse_redirects()
    #parser.parse_categories()

    #cat. /Data /* | python mapper.py |
    #sort - t$'\t' - k1 - k2 |
    #python reducer_1.py | sort | python reducer_2.py

