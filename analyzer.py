analyzer = {
    "settings": {
      "analysis": {
        "filter": {
          "english_stop": {
            "type": "stop",
            "stopwords": "_english_"
          },
          "autocomplete_filter": {
            "type": "edge_ngram",
            "min_gram": 1,
            "max_gram": 20
          }
        },
        "analyzer": {
          "autocomplete": {
            "type": "custom",
            "tokenizer": "standard",
            "filter": [
              "lowercase",
              "autocomplete_filter"
            ]
          },
          "my_stop_word_analyzer": {
            "type": "custom",
            "tokenizer": "standard",
            "filter": [
              "lowercase",
              "english_stop"
            ]
          }
        }
      }
    },
    "mappings": {
      "properties": {
        "key": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        },
        "text": {
          "type": "text",
          "analyzer": "autocomplete",
          "search_analyzer": "standard"
        },
        "title": {
          "type": "text",
          "fields": {
            "fullsearch": {
              "type": "text",
              "analyzer": "autocomplete",
              "search_analyzer": "my_stop_word_analyzer",
              "search_quote_analyzer": "autocomplete"
            },
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        },
        "category": {
          "type": "text",
          "fields": {
            "fulltext": {
              "type": "text",
              "analyzer": "autocomplete",
              "search_analyzer": "my_stop_word_analyzer",
              "search_quote_analyzer": "autocomplete"
            },
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        },
        "abstract": {
          "type": "text",
          "fields": {
            "fulltext": {
              "type": "text",
              "analyzer": "autocomplete",
              "search_analyzer": "my_stop_word_analyzer",
              "search_quote_analyzer": "autocomplete"
            },
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        },
        "alternative_titles": {
          "type": "text",
          "fields": {
            "fulltext": {
              "type": "text",
              "analyzer": "autocomplete",
              "search_analyzer": "my_stop_word_analyzer",
              "search_quote_analyzer": "autocomplete"
            },
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        }
      }
    }
  }
