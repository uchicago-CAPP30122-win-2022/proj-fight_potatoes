import datetime
from datetime import date
import pandas as pd
import yfinance as yf
from collection import collecting_tweets
from collection import update


def auto_update(today):
    """
    """
    
    comp = pd.read_csv('data/constituents.csv')
    comp_lst = pd.Series(comp['Symbol']).str.replace(".", '-')
    comp_lst = list(comp_lst)
    comp_lst = ['SPY'] + comp_lst
    
    print("----------------------------------- start to collect today's tweet data -----------------------------------")
    collecting_tweets.collect_tweets("china", today)
    collecting_tweets.collect_tweets("covid", today)

    print("----------------------------------- start to collect today's stock data -----------------------------------")
    # collect stock data
    y_file = yf.download(comp_lst, start='2022-02-04', end = today)    
    
    y_file = update.clean_stock_information(y_file)
    y_file = update.add_sector_y_datafile(y_file, comp)
    
    print("-----------------------------------finishing update-----------------------------------")
