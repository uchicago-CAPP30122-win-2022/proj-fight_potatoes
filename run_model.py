import modelling_part2_class_collect_all as model
import pandas as pd

# TRAINING_DATES = [214, 215, 216, 217, 218, 222, 223, 224, 225, 228, 301, 302]
TRAINING_DATES = [214, 215, 216, 217]
# TESTING_DATES = [303, 304]
TESTING_DATES = [301,302]
Y_FILENAME = 'data/S&P_update.csv'  # need to combine the y_file into the same file
TOPIC = ["china", "covid"]
STOCK = ["Close"] # "Close" refer to SP500
MODELNAME = ['linear','logistic','KNN', 'SVM']

all_models = model.process_all_model()

def to_df(model_object):
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
    
    return train, test

train = pd.DataFrame()
test = pd.DataFrame()
for name, model in all_models.items():
    sector, topic, model_name = str.split(name, '_')
    if sector == 'Close':
        sector = 'All Sectors'
    tr, te = to_df(model)
    tr['model'] = te ['model'] = model_name
    tr['sector'] = te['sector'] = sector
    te['dt'] = TESTING_DATES
    train = pd.concat([train, tr])
    test = pd.concat([test, te])

train['date'] = 2022000 + train.dt
pd.to_datetime(train['date'], format='%Y%m%d')

test['date'] = 2022000 + test.dt
pd.to_datetime(test['date'], format='%Y%m%d')

train.to_csv('data/train_output.csv')
test.to_csv('data/test_output.csv')
