# -*- coding: utf-8 -*-
"""
Created on Mon Aug 04 20:34:11 2014

@author: Administrator
"""
import logging
import numpy as np
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from sklearn.metrics import confusion_matrix


logging.getLogger().setLevel(logging.INFO)

logging.info('Loading training data and labels.')    
X = np.loadtxt('420_X.txt', delimiter=',')
y = np.loadtxt('420_Y.txt', delimiter=',')

logging.info('Split dataset for training and testing.')
from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
                                    X, y, test_size=0.25, random_state=42)

logging.info('Training the model.')
classifer = OneVsRestClassifier(LinearSVC(random_state=0))
classifer.fit(X_train, y_train)

logging.info('Testing the model')
y_hat = classifer.predict(X_test)
cm = confusion_matrix(y_test, y_hat)
print cm

logging.info('Save the model')
from sklearn.externals import joblib
filename = '420.pkl'
joblib.dump(classifer, filename, compress = 9)