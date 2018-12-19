import numpy as np
import pandas as pd

from pandas import Series, DataFrame

file = '/Users/labattula/Documents/Lakshman/Future-ML/MyDS/matches.csv'

DF_matches = pd.read_csv(file)
# print DF_matches.head()

team_name = "Royal Challengers Bangalore"

print DF_matches.loc[(DF_matches['team1'] == team_name) | (DF_matches['team2'] == team_name)]
