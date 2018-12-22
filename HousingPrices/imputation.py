#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 11:47:29 2018

@author: labattula
"""

# creating the Imputation

import pandas as pd
from sklearn.preprocessing import Imputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

melbourne_file_path = "/Users/labattula/Documents/lakshman/ML/PythonDataScience/HousingPrices/melb_data.csv"
melbourne_data = pd.read_csv(melbourne_file_path)

#print(melbourne_data.head())

# price data taken in seperate data frame, this will be our target value
mlb_data_price = melbourne_data.Price
#taking the rest of the values except price
mlb_price_predictors = melbourne_data.drop(['Price'],axis=1)

#selecting only the numerice data for applying the imputation
mlb_numeric_data_frame = mlb_price_predictors.select_dtypes(exclude=['object'])

X_train,X_test,y_train,y_test = train_test_split(mlb_numeric_data_frame,
                                                    mlb_data_price,
                                                    train_size=0.7,
                                                    test_size=0.3,
                                                    random_state=1)


# for getting mean absolute error basing on the RainForestRegressor 
def score_dataset(X_train,X_test,y_train,y_test):
    model = RandomForestRegressor()
    model.fit(X_train,y_train)
    preds = model.predict(X_test)
    return mean_absolute_error(y_test,preds)

########################################################
# getting the columns which contains nan in their cells
cols_for_drop = [col for col in X_train.columns
                     if X_train[col].isnull().any()]

reduced_X_train = X_train.drop(cols_for_drop,axis=1)
reduced_X_test = X_test.drop(cols_for_drop,axis=1)

print("1. droping the columns with value as nan")
print(score_dataset(reduced_X_train,reduced_X_test,y_train,y_test))

########################################################
# initializing the Imputer
my_imputer = Imputer()

# this will replace the nan value with X_train average value
# need to recast the ndArray back to Pandas dataFrame
# the ndArrays will not be structured like Pandas DataFrame
#imputed_X_train = my_imputer.fit_transform(X_train)
imputed_X_train = pd.DataFrame(my_imputer.fit_transform(X_train))
imputed_X_test = pd.DataFrame(my_imputer.transform(X_test))

print("2. Appying the imputation on the X_train and X_test")
print(score_dataset(imputed_X_train,imputed_X_test,y_train,y_test))

########################################################
# process of notifying to the mode that these values are missing, so that the
# model can take the right predictions
print("Extension to the imputation")
imputed_X_train_plus = X_train.copy()
imputed_X_test_plus = X_test.copy()

# getting the columns which hold nan in their cells
cols_with_na_for_imputation = [col for col in X_train.columns
                                       if X_train[col].isnull().any()]

for col in cols_with_na_for_imputation:
    imputed_X_train_plus[col+"_was_missing"] = imputed_X_train_plus[col].isnull()
    imputed_X_test_plus[col+"_was_missing"] = imputed_X_test_plus[col].isnull()
    
ext_imputer = Imputer()

# this will impute the data
imputed_X_train_plus = pd.DataFrame(ext_imputer.fit_transform(imputed_X_train_plus))
imputed_X_test_plus = pd.DataFrame(ext_imputer.fit_transform(imputed_X_test_plus))

print("3. Applying the col missing valraible to the data")
print(score_dataset(imputed_X_train_plus,imputed_X_test_plus,y_train,y_test))

"""
It is observed that over the period of time, if keep running the above program, the 
effeieciency of the result is flutuating between approach 2 and 3
"""





