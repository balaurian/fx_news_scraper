from json import load
import pandas as pd
import datetime
import math
#import numpy as np

def start_sorting():
    try:
        df = pd.read_csv('app/data/fx-news-tokenized.csv', header = 0, sep = ',', error_bad_lines = False, encoding = 'utf-8', parse_dates = [2])
        sorted_orders = []
        for i in range(0,df.shape[0]):
            for pair in df.pair[[i]]:
                if df.action[i] != 'na':
                    if type(pair).__name__ != 'float':
                        if '/' in pair:
                            sorted_orders.append([df.page[i], df.date[i], df.title[i], df.action[i], df.pair[i]])
        
        sorted_orders = pd.DataFrame(sorted_orders, columns = ['page', 'date', 'title', 'action', 'pair'])           
        
        try:
            sorted_orders.to_csv('app/data/fx-news-sorted.csv')
            print ('sorting completed')
            print ('output --> app/data/fx-news-sorted.csv')
        except:
            print ( 'sorted csv write error')
    
    except:
        print ('no tokenized file found, try scraping and tokenizing first')
        return
