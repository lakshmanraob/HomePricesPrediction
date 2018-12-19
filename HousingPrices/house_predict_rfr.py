#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 14:08:39 2018

@author: labattula
"""

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import pandas as pd



melborne_file_path = '/Users/labattula/Documents/lakshman/ML/PythonDataScience/HousingPrices/melb_data.csv'

melbourne_data = pd.read_csv(melborne_file_path)

melbourne_columns = melbourne_data.columns

melbourne_data = melbourne_data.dropna(axis=0)

y = melbourne_data.Price

print(melbourne_data.columns)
features = ['Rooms','Bathroom','Landsize','Lattitude','Longtitude']

X = melbourne_data[features]

train_X,val_X,train_y,val_y = train_test_split(X,y,random_state=1)

model = RandomForestRegressor(random_state=1)

model.fit(train_X,train_y)

val_predict = model.predict(val_X)

mae = mean_absolute_error(val_y,val_predict)

print(mae)
