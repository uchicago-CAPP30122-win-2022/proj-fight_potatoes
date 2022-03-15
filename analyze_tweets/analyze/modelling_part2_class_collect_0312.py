import numpy as np
import sklearn
from sklearn.linear_model import LinearRegression as lr
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn import datasets
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import statsmodels.api as sm
# import modeling_part_1
#import modeling_preparing_data
from analyze import Modeling_part1_prepare_X_Y_0312


############################## INPUT 2 ###################################
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
'''

def process_all_model(modelname, dates, topics, y_datafile, stocks, test_date):
    """
    Process all models and save results
    Input:
        modelname (list): models to run
        dates (list): training dates
        topics (list): TOPIC
        y_datafile (list): filename/path for stock data
        stocks (list): STOCK
        test_date (list): dates for testing data
    
    Returns:
        all_model: dict mapping stock, topic and model to 
            the results
    """
    print("++++++++++++++++++ starting to prepare training data ++++++++++++++++++")
    y_dic, x_dic, x3_dic = Modeling_part1_prepare_X_Y_0312.collect_all_x_and_y(dates, topics, y_datafile, stocks)

    print("++++++++++++++++++ starting to prepare testing data +++++++++++++++++++")
    if test_date:
        y_test, x_dic_test, x3_dic_test = Modeling_part1_prepare_X_Y_0312.collect_all_x_and_y(test_date, topics, y_datafile, stocks)
    else:
        testing_data = None
    
    
    print("++++++++++++++++++++ starting to train models ++++++++++++++++++++++++++")
    all_model = {}
    
    select_on_x = list(input("Now you can select from polarity(0), subjectivity(1), moving average(2) as the regressors, example: [0, 1] (or just press return button if you want them all) : ")         or [0,1,2])
    
    possible_regressor = possible_regressor[:, select_on_x]
    possible_regressor_test = possible_regressor_test[:, select_on_x]
    for topic_name in topics:
        for stock_name in stocks:
            for name in modelname:
                training_x = select_on_xs(select_on_x, x_dic[topic_name], x3_dic[stock_name])
                training_data = y_dic[stock_name] + training_x
                if test_date:
                    training_x_test = select_on_xs(select_on_x, x_dic_test, x3_dic_test)
                    testing_data = y_test[stock_name] + training_x_test
                all_model[f"{stock_name}_{topic_name}_{name}"] = TrainingModel(name, 
                    dates, stock_name, topic_name, training_data, testing_data, test_date)
        
    return all_model


def select_on_xs(selection_on_x, x1_x2, x3):
    """

    """
    training_x = []
    if 0 in select_on_x:
        training_x.append(x1_x2[:, 0])
    if 1 in select_on_x:
        training_x.append(x1_x2[:, 1])
    if 2 in select_on_x:
        training_x.append(x3)
        
    return np.array(lst).transpose()


class TrainingModel:
    """
    Class for representing a Model

    Attributes:
       

    Methods:
        model_building (self):
        compute the gini coefficient
    
    """
    
    def __init__(self, model_name, dates, stock, topic, training_data, testing_data = None, test_date = None):
        """
        """
        self.training_data = training_data
        self.true_y = None
        self.date = dates
        self.stock = stock
        self.model_name = model_name
        self.topic = topic
        self.fitted_value = None
        self.testing_data = testing_data
        self.test_date = test_date
        self.prediction = None
        self.test_accuracy = None
        self.true_testing_y = None            
        self.model = self.model_building(model_name, testing_data)
        self.R2 = sklearn.metrics.r2_score(self.true_y, self.fitted_value)
        

    def model_building(self, model_name, test):
        """
        """
        y_dummy, y_num, Xs, corpus = self.training_data

        if model_name == "linear":
            X2 = sm.add_constant(Xs)
            model_1 = sm.OLS(y_num,X2)
            model = model_1.fit()
            self.true_y = self.training_data[1]
            self.fitted_value = model.predict()
            if test:
                test_x = self.testing_data[2]
                update_test_x = sm.add_constant(test_x) 
                self.prediction = model.predict(update_test_x)
                self.true_testing_y = self.testing_data[1]
                self.test_accuracy = "Not application for linear model"

        else:
            if model_name == "logistic":
                logreg = LogisticRegression(random_state=42)
                model = logreg.fit(Xs, y_dummy)

            if model_name == "KNN":
                neigh = KNeighborsClassifier(n_neighbors = 2) # CAN SELECT?
                model = neigh.fit(Xs, y_dummy)

            else:
                svm_linear = SVC( kernel = 'linear')
                model = svm_linear.fit(Xs, y_dummy)
            
            self.true_y = self.training_data[0]
            self.fitted_value = model.predict(self.training_data[2])
            if test:
                self.prediction = model.predict(self.testing_data[2])
                self.true_testing_y = self.testing_data[0]
                self.test_accuracy = accuracy_score(self.true_testing_y, self.prediction)

        return model


def random_forest_text_classification(corpus, y_dummy):
    """
    
    """
    vectorizer = CountVectorizer(min_df=1)
    X = vectorizer.fit_transform(corpus).toarray()
    clf = RandomForestClassifier()
    model = clf.fit(X, y_dummy)
#   clf.predict(vectorizer.transform(['apple is present']).toarray())
    return model
