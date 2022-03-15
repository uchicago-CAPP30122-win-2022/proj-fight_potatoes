import pandas as pd
from analyze import modelling_part2_class_collect_0312 as model

'''
TRAINING_DATES = [214, 215, 216, 217, 218, 222, 223, 224, 225]
TESTING_DATES = [228, 301, 302]
Y_FILENAME = 'data/SP500_constituents_update.csv'
TOPIC = ["china", "covid"]
STOCK = ["Close", 'Industrials' , 'Health Care', 'Information Technology',
    'Communication Services' , 'Consumer Staples', 'Consumer Discretionary',
    'Utilities', 'Financials', 'Materials', 'Real Estate', 'Energy']
MODELNAME = ['linear','logistic','KNN', 'SVM']
'''

# "we now have [214, 215, 216, 217, 218, 222, 223, 224, 225, 228, 301, 302, 303, 304, 307, 308, 310, 311, 314, 315, ]] data in our database, you can choose which days to use as training data and which days as testing (or just press return)"
TRAINING_DATES = list(input("Enter training dates (list of dates), example: [214, 215, 216, 217, 218, 222, 223] (or just press return button if you want the defult value) : ")         or [214,215,216,217,218])
TESTING_DATES = list(input("Enter testing dates (list of dates), example: [301, 302] (or just press return button if you want the defult value) : ")         or [301,302])
Y_FILENAME = 'data/SP500_constituents_update.csv'  # need to combine the y_file into the same file
TOPIC = ['china', 'covid']
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
        if sector == 'Close':
            sector = 'All Sectors'
        tr, te = to_df(model)
        tr['model'] = te ['model'] = model_name
        tr['sector'] = te['sector'] = sector
        te['dt'] = TESTING_DATES
        train = pd.concat([train, tr])
        test = pd.concat([test, te])
    return train, test
