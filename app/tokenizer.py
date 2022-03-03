from tkinter.messagebox import NO
import pandas as pd
import datetime
import numpy as np
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer

import app.setup_dictionaries as fx_dict

class fx_news_tokenizer():
    def __init__(self):
        self.fx_news_path = 'app/data/fx-news-archive.csv'
        self.eng_stopwords = stopwords.words('english') 
        self.scraped_news_df = None
        try:
            self.scraped_news_df = pd.read_csv(self.fx_news_path, header = 0, sep = ',', error_bad_lines = False, encoding = 'utf-8', parse_dates = [2])
        
        except:
            print ('no archive file. try creating one first')
            return
    
    def lemmatizer(self,text):
        return [WordNetLemmatizer().lemmatize(word, 'v') for word in text]

    def setup_and_token(self,dataframe):
        del dataframe['body']
        self.eng_stopwords = stopwords.words('english') 

        dataframe.title = dataframe.title.str.replace("- ()", "")
        dataframe.title = dataframe.title.str.replace("[()\"{:,;%]", "")
        
        news_title = dataframe.title.astype(str)
        news_title = news_title.str.lower()
        
        #tokenize
        news_title = news_title.apply(word_tokenize)
        #remove stop words
        news_title = news_title.apply(lambda x:[item for item in x if item not in self.eng_stopwords])
        #lemmatize
        news_title = news_title.apply(self.lemmatizer)
        
        dataframe['tokenized'] = news_title
        
        #print (dataframe)
        return dataframe

    def found_char(self, char, lst):
        the_pair =''
        for word in lst:
            if char in word:
                the_pair = word
        
        return the_pair

    #search for pairs_collection in news
    def search_pairs (self, lst):
        found_pair = ''
        for trade_pair in fx_dict.pair_list['pairs']:
            if lst[0] in trade_pair and lst[1] in trade_pair:
                found_pair = trade_pair
        return found_pair

    # returns a dataframe with pairs' bull/bear direction by
    # comparing tokenized news to a bear/bull financial vocabulary 
    def sentimental_calculator(self, news):
        some_news = []
        
        for i in range(0,news.shape[0]):
            currency_pair = []

            action = 'na' #default value
            bull_counter = 0
            bear_counter = 0
            for word in news.tokenized[i]:
                if word in fx_dict.bull_words:
                    bull_counter += 1

                if word in fx_dict.bear_words:
                    bear_counter += 1

                if '/' in word:
                    for trade_pair in fx_dict.pair_list['pairs']:
                        if word in trade_pair:
                            if trade_pair not in currency_pair:
                                currency_pair.append(trade_pair)
                                
                else:
                    for x in fx_dict.pair_vocabulary.keys():
                        if word.startswith(x.lower()):
                            if x.lower() not in currency_pair:
                                currency_pair.append(x.lower())

                        if word.endswith(x.lower()):
                            if x.lower() not in currency_pair:
                                currency_pair.append(x.lower())

                        else:
                            for trade_pair_vocab in fx_dict.pair_vocabulary[x]:
                                if word == trade_pair_vocab:
                                    if x.lower() not in currency_pair:
                                        currency_pair.append(x.lower())

            x = self.found_char('/', currency_pair)                            
            if x != '':
                currency_pair = self.found_char('/', currency_pair)
            
            else:
                if len(currency_pair) > 1:
                    if len(currency_pair) < 3:
                        currency_pair = self.search_pairs(currency_pair)

            sentiment = bull_counter - bear_counter
            if sentiment > 0:
                action = 'bull'

            else:
                if sentiment < 0:
                    action = 'bear'

            some_news.append([news.page[i], news.date[i], news.title[i], news.tokenized[i], action, currency_pair])
        
        some_news = pd.DataFrame(some_news, columns =['page', 'date', 'title', 'tokenized', 'action', 'pair'])
        
        return some_news

    def start_tokenizing(self):
        if self.scraped_news_df is not None:
            news_dataframe_processed = self.setup_and_token(self.scraped_news_df)
            some_news = pd.DataFrame(self.sentimental_calculator(news_dataframe_processed), columns =['page', 'date', 'title', 'tokenized', 'action', 'pair'])
            try:
                some_news.to_csv('app/data/fx-news-tokenized.csv')
                print ('tokenizing completed')
                print ('output --> app/data/fx-news-tokenized.csv')
            
            except:
                print ( 'tokenized csv write error!')