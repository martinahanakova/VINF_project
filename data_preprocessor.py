import lucene

if not lucene.getVMEnv():
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])

from java.io import StringReader
from org.apache.lucene.analysis.tokenattributes import CharTermAttribute
from lucene import JArray_char, JArray
from org.apache.lucene.analysis.core import LowerCaseFilter, StopAnalyzer, StopFilter
from org.apache.lucene.analysis.standard import StandardTokenizer
from org.tartarus.snowball.ext import EnglishStemmer

class DataPreprocessor:

    def __init__(self):
        self.stemmer = EnglishStemmer()

    def preprocess_data(self, index_id, text):
        token_list = self.tokenize(text)
        for token in token_list:
            print(token, '->', self.stem(self.stemmer, token), index_id)

    def tokenize(self, text):
        token_list = []

        tokenizer = StandardTokenizer()
        tokenizer.setReader(StringReader(text))
        tokenizer.reset()

        tokenizer = LowerCaseFilter(tokenizer)

        token = tokenizer.addAttribute(CharTermAttribute.class_)

        while tokenizer.incrementToken():
            token_list.append(token.toString())

        tokenizer.close()

        return token_list

    def stem(self, stemmer, word):
        # Add the word
        stemmer.setCurrent(JArray_char(word), len(word))
        # Fire stemming
        stemmer.stem()
        # Fetch the output (buffer & size)
        result = stemmer.getCurrentBuffer()
        l = stemmer.getCurrentBufferLength()
        return ''.join(result)[0:l]
