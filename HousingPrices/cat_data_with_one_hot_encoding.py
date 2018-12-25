#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 24 06:35:37 2018

@author: labattula
"""

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score


#### This process became very common
train_path = '/Users/labattula/Documents/lakshman/ML/PythonDataScience/HousingPrices/all/train.csv'
test_path = '/Users/labattula/Documents/lakshman/ML/PythonDataScience/HousingPrices/all/test.csv'

# reading the data using Panda
train_data = pd.read_csv(train_path)
test_data = pd.read_csv(test_path)

# dropping the NAN values from the sepecified column ex : SalePrice
train_data.dropna(axis=0,subset=['SalePrice'],inplace=True)

# this is target data
target = train_data.SalePrice

print(target.head())

# finding out the columns with missing values
col_with_missing = [col for col in train_data.columns if train_data[col].isnull().any()]

# dropping the missing values from the columns
candidate_train_predictors = train_data.drop(['Id','SalePrice']+col_with_missing,axis=1)

candidate_test_predictors = test_data.drop(['Id']+col_with_missing,axis=1)

# checking the columns with unique values, target - 10 and the element of data type object
low_cardinality_cols = [cname for cname in candidate_train_predictors.columns if
                                                        candidate_train_predictors[cname].nunique() < 10 and
                                                        candidate_train_predictors[cname].dtype == "object"]

# finding out the numberic columns
numeric_cols = [cname for cname in candidate_train_predictors.columns if
                    candidate_train_predictors[cname].dtype in ['int64','float64']]

# forming the columns elements with Object and numreric columns
my_cols = low_cardinality_cols + numeric_cols

# train predictors - data creation with the columns
train_predictors = candidate_train_predictors[my_cols]
test_predictors = candidate_test_predictors[my_cols]

print(train_predictors.head())

#print(train_predictors.dtypes.sample(10))
#print(test_predictors.dtypes.sample(10))

# get_dummies is from Pandas to apply the one-hot encoding technique
one_hot_encoded_training_predictors = pd.get_dummies(train_predictors)
one_hot_encoded_testing_predictors = pd.get_dummies(test_predictors)

# method for calculating the mae by using RandomForestRegressor and 
def get_mae(X,y):
    # cross_val_score - estimates the expected accuracy of you model out-of training data 
    # multiply by -1 to make positive mae score instead of neg value returned as Sklearn convention
    return -1 * cross_val_score(RandomForestRegressor(50),X,y,scoring='neg_mean_absolute_error').mean()
    
predictors_with_out_categoricals = train_predictors.select_dtypes(exclude=['object'])
#print(predictors_with_out_categoricals.head())

mae_with_out_categoricals = get_mae(predictors_with_out_categoricals,target)
#print(mae_with_out_categoricals)

mae_with_hot_encoded = get_mae(one_hot_encoded_training_predictors,target)
#print(mae_with_hot_encoded)

print("mean absolute error when dropping categoricals "+str(int(mae_with_out_categoricals)))

print("mean absolute error With one hot-encoding "+str(int(mae_with_hot_encoded)))

# align make sure that the columns show up in same order in both datasets
# join = left -> If there are ever columns that show up in one dataset and not in other, we will keep exactly
# the columns from our training data
# join = inner -> keeping only the columns that are showing up in both data sets
final_train, final_test = one_hot_encoded_training_predictors.align(one_hot_encoded_testing_predictors,join='left',axis=1)


