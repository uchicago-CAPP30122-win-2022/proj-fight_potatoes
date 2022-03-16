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
from analyze import modelling_part1


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
    y_dic, x_dic, x3_dic = modelling_part1.collect_all_x_and_y(dates, topics, y_datafile, stocks)

    print("++++++++++++++++++ starting to prepare testing data +++++++++++++++++++")
    if test_date:
        y_test, x_dic_test, x3_dic_test = modelling_part1.collect_all_x_and_y(test_date, topics, y_datafile, stocks)
    else:
        testing_data = None
    
    
    print("++++++++++++++++++++ starting to train models ++++++++++++++++++++++++++")
    all_model = {}

    selection_on_x = list(input("Now you can select from polarity(0), subjectivity(1), moving average(2) as the regressors, example: [0, 1] (or just press return button if you want them all) : ") \
        or [0,1,2])

    for topic_name in topics:
        for stock_name in stocks:
            for name in modelname:
                training_x = select_on_xs(selection_on_x, x_dic[topic_name], x3_dic[stock_name])
                training_data = y_dic[stock_name] + (training_x, )
                if test_date:
                    training_x_test = select_on_xs(selection_on_x, x_dic_test[topic_name], x3_dic_test[stock_name])
                    testing_data = y_test[stock_name] + (training_x_test, )
                all_model[f"{stock_name}_{topic_name}_{name}"] = TrainingModel(name, 
                    dates, stock_name, topic_name, training_data, testing_data, test_date)
        
    return all_model

######################### FINISH DOC STRING #############################
def select_on_xs(selection_on_x, x1_x2, x3):
    """
    Select independent variables

    Inputs:
        selection_on_x:
        x1_x2:
        x3:

    Returns: 
    """
    training_x = []
    if 0 in selection_on_x:
        training_x.append(x1_x2[0][0])

    if 1 in selection_on_x:
        training_x.append(x1_x2[0][1])

    if 2 in selection_on_x:
        training_x.append(x3)

    return np.array(training_x).transpose()


class TrainingModel:
    """
    Class for representing a Model

    Attributes:
        training_data = training_data
        true_y: true stock price for training data
        date: training dates
        stock: stock/sector
        model_name: model_name
        topic: topic (covid or china)
        fitted_value: training fitted value
        testing_data: testing_data
        test_date: test_date
        prediction: test data predicted value
        test_accuracy: accuracy of model on test data
        true_testing_y: actual stock price for test data            
        model: represent the model
        R2: R^2

    Methods:
        model_building (self):
    """
    
    def __init__(self, model_name, dates, stock, topic, training_data, testing_data = None, test_date = None):
        """
        Initialize a model
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
        Build a model

        Inputs:
            model_name (str): model_name, e.g. "KNN", "linear", etc.
            test: (bool) whether to use test data to test

        Returns:
            model: instance of the TrainingModel class
        """
        y_dummy, y_num, Xs = self.training_data

        if model_name == "linear":
            print(Xs)
            X2 = sm.add_constant(Xs)
            model_1 = sm.OLS(y_num, X2)
            model = model_1.fit()
            self.true_y = self.training_data[1]
            self.fitted_value = model.predict()
            if test:
                test_x = self.testing_data[2]
                update_test_x = sm.add_constant(test_x)
                self.prediction = model.predict(update_test_x)
                self.true_testing_y = self.testing_data[1]
                self.test_accuracy = "Not applicable to linear model"

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
