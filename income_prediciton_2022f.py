# -*- coding: utf-8 -*-
"""income prediciton 2022f

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-rGHa3tR2pAV9X3sevfYxjet3qpQeyz5
"""

!pip install kneed

import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import RandomOverSampler
from sklearn.model_selection import train_test_split
from kneed import KneeLocator
from sklearn.cluster import KMeans
from pandas.io.parsers.readers import read_fwf
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier
from sklearn.metrics  import roc_auc_score,accuracy_score
import csv
from sklearn.preprocessing import OneHotEncoder

train_data = pd.read_csv('train_final.csv')
test_data = pd.read_csv('test_final.csv')
train_data

#handling missing data
train_data = train_data.replace('?',np.NaN)
train_data
test_data = test_data.replace('?',np.NaN)
test_data

# get labels.
YTrain = train_data['income>50K'].replace([' <=50K' , ' >50K'], [0, 1])

# get features.
XTrain = train_data.drop(['income>50K'], axis=1)
XTest = test_data.drop(['ID'], axis=1)
# normalize numeric features.
from sklearn.preprocessing import StandardScaler
numcol = ['age', 'fnlwgt', 'education.num', 'capital.gain', 'capital.loss', 'hours.per.week']
scaler = StandardScaler()
XTrain[numcol] = scaler.fit_transform(XTrain[numcol])
XTest[numcol] = scaler.transform(XTest[numcol])
# get one-hot vectors.
X = pd.concat([XTrain,XTest])
X = pd.get_dummies(X)
XTrain = X[:len(XTrain)]
XTest = X[len(XTrain):]
print(XTrain)
print("size of training data is", XTrain.shape)
print("size of testing data is", XTest.shape)

xgboost_parameters = {"max_depth": range(5, 10, 1),"n_estimators": [100, 130,150]}
grid= GridSearchCV(XGBClassifier(objective='binary:logistic'),xgboost_parameters,verbose=3)
grid.fit(XTrain, YTrain)
xgb = XGBClassifier(max_depth=grid.best_params_['max_depth'],n_estimators= grid.best_params_['n_estimators'])
xgb.fit(XTrain,YTrain)
YPred = xgb.predict(XTest)

test_data['income>50K'] = YPred
test_data['income>50K'] = test_data['income>50K']
#print(YPred)
result = test_data[['ID', 'income>50K']]
result.rename(columns = {'income>50K':'Prediction'}, inplace = True)
result.to_csv('result_mod_XGB.csv', index=0)
#type(result)
print("end")





