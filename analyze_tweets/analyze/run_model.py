import datetime
from datetime import date
from urllib.request import BaseHandler
import pandas as pd
#from analyze import modelling_part2 as model
#from collection import auto_update_data
from analyze import modelling_part2_class_collect_all as model

# "we now have [214, 215, 216, 217, 218, 222, 223, 224, 225, 228, 301, 302, 303, 304, 307, 308, 310, 311, 314, 315, ]] data in our database, you can choose which days to use as training data and which days as testing (or just press return)"
TRAINING_DATES = list(input("Enter training dates (list of dates when the market is open), example: [214, 215, 216, 217, 218, 222, 223] (or just press return button if you want the default value) : ")         or [214, 215, 216, 217, 218, 222, 223, 224, 225])
TESTING_DATES = list(input("Enter testing dates (list of dates >= length 2), example: [301, 302] (or just press return button if you want the default value) : ")         or [228, 301, 302])
###### UPDATE THIS ######
Y_FILENAME = 'data/SP500_constituents_update.csv'
'''
auto_update = input("Do you want to download today's data to update the database? Enter Yes or No: ")         or 'No'

if auto_update.lower() == 'yes':
    today = str(date.today())
    day = today.split("-")
    day = int(day[1] + day[2])
    auto_update_data.auto_update(today)
    Y_FILENAME = 'data/y_file_update.csv'
    TESTING_DATES.append(day)
'''

TOPIC = ['china', 'covid']
#STOCK = ["SPY", 'Industrials' , 'Health Care', 'Information Technology',
#    'Communication Services' , 'Consumer Staples', 'Consumer Discretionary',
#   'Utilities', 'Financials', 'Materials', 'Real Estate', 'Energy']
STOCK = ["Close", 'Industrials' , 'Health Care', 'Information Technology',
    'Communication Services' , 'Consumer Staples', 'Consumer Discretionary',
   'Utilities', 'Financials', 'Materials', 'Real Estate', 'Energy']
MODELNAME = ['linear','logistic','KNN', 'SVM']

all_models = model.process_all_model(MODELNAME, TRAINING_DATES,
    TOPIC, Y_FILENAME, STOCK, TESTING_DATES)

def to_df(model_object):
    '''
    Take output of process_all_models
    and convert to pandas DF

    Input:
        model_object: output of process_all_model

    Returns:
        train, test (tuple): output dataframe for train/test data
    '''
    train = pd.DataFrame()
    train['dt'] = model_object.date
    train['fitted_y'] = model_object.fitted_value
    train['true_y'] = model_object.true_y
    train['topic'] = model_object.topic

    # testing data
    test = pd.DataFrame()
    test['predicted'] = model_object.prediction
    test['actual'] = model_object.true_testing_y
    test['topic'] = model_object.topic
    test['R2'] = model_object.R2
    
    return train, test


def concat(model_dict = all_models):
    '''
    Append dataframes to one df

    Input: model_dict: dictionary (output of 
        process_all_models)

    Returns:
        train, test (tuple): output dataframe for train/test data
            for all topics, models and sectors
    '''
    train = pd.DataFrame()
    test = pd.DataFrame()

    for name, model in model_dict.items():
        sector, topic, model_name = str.split(name, '_')
        #if sector == 'SPY':
        if sector == 'Close':
            sector = 'All Sectors'
        tr, te = to_df(model)
        tr['model'] = te ['model'] = model_name
        tr['sector'] = te['sector'] = sector
        te['dt'] = TESTING_DATES
        train = pd.concat([train, tr])
        test = pd.concat([test, te])
    return train, test


def each_model(df, model_name):
    '''
    Find top 3 performing sectors for a model

    Inputs: 
        df: output df
        model_name (str): a model name 
    
    Returns:
        top_3: a list of top 3 sectors
    '''
    result= df[df["model"] == model_name].sort_values(by = ["R2"], ascending = False).head(6)
    top_3 = []
    for i in result["sector"]:
        if i not in top_3:
            top_3.append("  ")
            top_3.append(i)
            top_3.append("/")
    return top_3


def GetTheTopThreeSectors(df):
    '''
    This function takes a pandas dataframe.
    For each topic(china/covid),
    we will get the top 3 sectors that have the highest 
    R-square under different model
    
    Input:
        df: a pandas dataframe

    Returns:
        dframe: a pandas dataframe shows the top 3 sectors
            with the topic and model
    
    '''
    # List 1
    topic = ['China','China','China','China',"Covid","Covid","Covid","Covid"]
    
    # List 2
    classifer = ['Linear','Logit','KNN','SVMLinear','Linear','Logit','KNN','SVMLinear']
    
    #list 3 
    
    top_3_sectors = []
    df = df[df["sector"] != "All Sectors"]
    china_df = df[df["topic"] == "china"]
    
        
    top_3_sectors.append(tuple(each_model(china_df,"linear")))
    
    top_3_sectors.append(tuple(each_model(china_df,"logistic")))
            
    top_3_sectors.append(tuple(each_model(china_df,"KNN")))
    
    top_3_sectors.append(tuple(each_model(china_df,"SVM")))

    covid_df = df[df["topic"] == "covid"]   
    
    top_3_sectors.append(tuple(each_model(covid_df,"linear")))
    
    top_3_sectors.append(tuple(each_model(covid_df,"logistic")))
            
    top_3_sectors.append(tuple(each_model(covid_df,"KNN")))
    
    top_3_sectors.append(tuple(each_model(covid_df,"SVM")))
    
    
    # and merge them by using zip().  
    list_tuples = list(zip(topic, classifer,top_3_sectors)) 
    new_list_tuples = '  '.join(str(list_tuples))
    
    # Converting lists of tuples into pandas Dataframe.  
    dframe = pd.DataFrame(list_tuples, columns=['topic', 'classifier',"top 3 sectors"])  
    
    return dframe
