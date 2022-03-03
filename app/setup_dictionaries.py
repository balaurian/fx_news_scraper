import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer

import pandas as pd

from collections import defaultdict

with open('app/data/fx-bear-terms.csv', 'r') as bears:
    bear_words = bears.read()

with open('app/data/fx-bull-terms.csv', 'r') as bulls:
    bull_words = bulls.read()

#with open('app/data/fx-pairs-slang.csv', 'r') as pairs:
#    pair_vocabulary = pairs.read()

pair_list = pd.read_csv('app/data/fx-pairs-collection.csv', header = 0, sep = ',', error_bad_lines = False, encoding = 'utf-8')

pair_vocabulary = pd.read_csv('app/data/fx-pairs-slang.csv', header = 0, sep = ',', error_bad_lines = False, encoding = 'utf-8', parse_dates = [2])

def pair_to_dictionary(pair_vocabulary):
    pair_vocab_dic = defaultdict(dict)
    for i in pair_vocabulary.columns:
        pair_vocab_dic[i] = pair_vocabulary[i].to_list()
        
    return pair_vocab_dic

def pairs_lematizer(pair_vocabulary):
    for x in pair_vocabulary.keys():
        
        for word in pair_vocabulary[x]:
            word = lem.lemmatize(word, 'n')

    return pair_vocabulary

def pairs_tokenize(pair_vocabulary):
    for x in pair_vocabulary.keys():
        for word in pair_vocabulary[x]:
            word = word_tokenize(word)

    return pair_vocabulary

pair_vocabulary = pair_to_dictionary(pair_vocabulary)
lem = WordNetLemmatizer()
stem = PorterStemmer()

eng_stopwords = stopwords.words('english')

bear_words = lem.lemmatize(bear_words, 'v')
bull_words = lem.lemmatize(bull_words, 'v')

pair_vocabulary      = pairs_lematizer(pair_vocabulary)    

bear_words = word_tokenize(bear_words)
bull_words = word_tokenize(bull_words)

pair_vocabulary      = pairs_tokenize(pair_vocabulary)

bear_words = [word for word in bear_words if word not in eng_stopwords] 
bull_words = [word for word in bull_words if word not in eng_stopwords]