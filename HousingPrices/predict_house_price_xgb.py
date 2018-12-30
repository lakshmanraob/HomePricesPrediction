#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 26 11:52:04 2018

@author: labattula
"""

import pandas as pd
from sklearn.model_selection import cross_val_score, KFold
import xgboost
import csv as csv
from xgboost import plot_importance
import matplotlib as pyplot
from sklearn.cross_validation import train_test_split
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt
from sklearn.grid_search import GridSearchCV
from scipy.stats import skew
from collections import OrderedDict

train_file_path = "/Users/labattula/Documents/lakshman/ML/PythonDataScience/HousingPrices/all/train.csv"
test_file_path = "/Users/labattula/Documents/lakshman/ML/PythonDataScience/HousingPrices/all/test.csv"

train_master = pd.read_csv(train_file_path, header=0)
test_master = pd.read_csv(test_file_path, header=0)

# print(train_master.columns)

categorical_features = ['MSSubClass', 'MSZoning', 'Street', 'Alley', 'LotShape', 'LandContour', 'Utilities',
                        'LotConfig', 'LandSlope', 'Neighborhood', 'Condition1', 'Condition2', 'BldgType', 'HouseStyle',
                        'RoofStyle', 'RoofMatl', 'Exterior1st', 'Exterior2nd', 'MasVnrType', 'ExterQual', 'ExterCond',
                        'Foundation', 'BsmtQual', 'BsmtCond', 'BsmtExposure', 'BsmtFinType1', 'BsmtFinType2', 'Heating',
                        'HeatingQC', 'CentralAir', 'Electrical', 'KitchenQual', 'Functional', 'FireplaceQu',
                        'GarageType', 'GarageFinish', 'GarageQual', 'GarageCond', 'PavedDrive', 'PoolQC', 'Fence',
                        'MiscFeature', 'SaleType', 'SaleCondition']

every_columns_except_y = [col for col in test_master.columns if col not in ['SalePrice', 'Id']]

every_column_non_categorical = [col for col in categorical_features if
                                col not in categorical_features and col not in ['Id']]

print(every_column_non_categorical)

numeric_feats = train_master[every_column_non_categorical].dtypes[train_master.dtypes != "object"].index

print(numeric_feats)
