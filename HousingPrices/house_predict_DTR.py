# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

import pandas as pd

melboune_file_path = '/Users/labattula/Documents/lakshman/ML/PythonDataScience/HousingPrices/melb_data.csv'
melbourne_data = pd.read_csv(melboune_file_path)

melbourne_columns = melbourne_data.columns

melbourne_data = melbourne_data.dropna(axis=0)

y = melbourne_data.Price

print(melbourne_data.columns)
features = ['Rooms','Bathroom','Landsize','Lattitude','Longtitude']

X = melbourne_data[features]

def get_train_data(random_state):
    train_X,val_X,train_y,val_y = train_test_split(X,y,random_state=random_state)
    return train_X,val_X,train_y,val_y

max_leaf_nodes = [5,10,25,50,100,1000,2000,5000]

def get_mae(max_leaf):
    random_state = 1
    model = DecisionTreeRegressor(max_leaf_nodes = max_leaf,random_state=random_state)
    train_X,val_X,train_y,val_y = train_test_split(X,y,random_state=random_state)
    model.fit(train_X,train_y)
    val_predict = model.predict(val_X)
    mae = mean_absolute_error(val_y,val_predict)
    return (mae)

d = []
for leaf_node in max_leaf_nodes:
    cal_mae = get_mae(leaf_node)
    d.append((leaf_node,cal_mae))
df = pd.DataFrame(d,columns=('leaf_node','mae'))
mae_min = df.min().mae
print(df.loc[df['mae'] == df.min().mae])