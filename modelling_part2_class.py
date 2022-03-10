#!/usr/bin/env python
# coding: utf-8

# In[2]:


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


# In[2]:


# import modeling_part_1


# In[3]:


import modeling_preparing_data


# In[4]:


############################## INPUT #######################################

# TRAINING_DATES = [214, 215, 216, 217, 218, 222, 223, 224, 225, 228, 301, 302]
TRAINING_DATES = [214, 215, 216, 217]
# TESTING_DATES = [303, 304]
TESTING_DATES = [301,302]
Y_FILENAME = 'data/S&P_update.csv'
TOPIC = "china"
STOCK = "Close" # "Close" refer to SP500


# In[ ]:





# In[ ]:





# In[ ]:





# In[5]:


class TrainingModel:
    """
    """
    
    def __init__(self, model_name, dates = TRAINING_DATES, topic = TOPIC, datafile = Y_FILENAME, stock = STOCK, test_date = TESTING_DATES):
        """
        """
        self.training_data = modeling_preparing_data.collect_all_x_and_y(dates, topic, datafile, stock)
        self.true_y = None
        self.date = dates
        self.topic = topic
        self.fitted_value = None
        if test_date:
            self.testing_data = modeling_preparing_data.collect_all_x_and_y(test_date, topic, datafile, stock)
            self.prediction = None
            self.test_accuracy = None
            self.true_testing_y = None            
        self.model = self.model_building(model_name, topic, test_date)
        self.R2 = sklearn.metrics.r2_score(self.true_y, self.fitted_value)
        

    def model_building(self, model_name, topic, test):
        """
        """
        y_dummy, y_num, Xs, corpus = self.training_data

        if model_name == "linear":
            X2 = sm.add_constant(Xs)
#             print(y_num,X2)
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
            
    #     print(model_2.summary())

        elif model_name == "logistic":
            logreg = LogisticRegression(random_state=42)
            model = logreg.fit(Xs, y_dummy)
            self.true_y = self.training_data[0]
            self.fitted_value = model.predict(self.training_data[2])
            if test:
                self.prediction = model.predict(self.testing_data[2])
                self.true_testing_y = self.testing_data[0]
                self.test_accuracy = accuracy_score(self.true_testing_y, self.prediction)

        elif model_name == "KNN":
            neigh = KNeighborsClassifier(n_neighbors = 2) # CAN SELECT?
            model = neigh.fit(Xs, y_dummy)
            self.true_y = self.training_data[0]
            self.fitted_value = model.predict(self.training_data[2])
            if test:
                self.prediction = model.predict(self.testing_data[2])
                self.true_testing_y = self.testing_data[0]
                self.test_accuracy = accuracy_score(self.true_testing_y, self.prediction)

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
    
#     def selection_on_X(self, selection):
#         pass


# In[6]:


svm_model = TrainingModel("SVM")


# In[ ]:


def random_forest_text_classification(corpus, y_dummy):
    """
    
    """
    
    vectorizer = CountVectorizer(min_df=1)
    X = vectorizer.fit_transform(corpus).toarray()
    clf = RandomForestClassifier()
    model = clf.fit(X, y_dummy)
#   clf.predict(vectorizer.transform(['apple is present']).toarray())
    return model


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




