#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 25 12:25:44 2018

@author: labattula
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import Imputer
from sklearn.metrics import mean_absolute_error

from xgboost import XGBRegressor


file_path = '/Users/labattula/Documents/lakshman/ML/PythonDataScience/HousingPrices/all/train.csv'

data = pd.read_csv(file_path)

# Target value
y = data.SalePrice

# values to consider to perform the prediction
X = data.drop(['SalePrice'],axis=1).select_dtypes(exclude=['object'])

# splitting the data using standard train test split technique
train_X,test_X,train_y,test_y = train_test_split(X.as_matrix(),y.as_matrix(),test_size=0.25)

# inputer for imputing the missing values
my_imputer = Imputer()

# simple Imputer this will fill the nan values with the average of the existing values
# There are few other options to apply like Imputation extension
train_X = my_imputer.fit_transform(train_X)
test_X = my_imputer.transform(test_X)

#print(train_X)

# n_estimators - specifies how many times to go through the modeling cycles
# learning_rate - this is one of the trick to improve the model, before adding the model to ensemble
# we are multiplying the prediction from each model by a small number before adding them in.
my_model = XGBRegressor(n_estimators=1000,learning_rate=0.05,n_jobs=3)

# early_stopping_rounds - it is in conjuction with the n_estimators will improve model training
# we can increase the n_estimators and fine tune the early_stopping_rounds to make sure 
# we are getting the better model
my_model.fit(train_X,train_y,
             early_stopping_rounds=5,
             eval_set=[(test_X,test_y)],
             verbose=False)

predictions = my_model.predict(test_X)

mae = mean_absolute_error(predictions,test_y)
print(mae)