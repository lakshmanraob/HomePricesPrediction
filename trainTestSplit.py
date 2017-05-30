from sklearn.cross_validation import train_test_split

from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression

from sklearn.datasets import load_iris

import sklearn.metrics as metrics

iris = load_iris()

X = iris.data
y = iris.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4)

print X_train.shape
print X_test.shape

print y_train.shape
print y_test.shape

logReg = LogisticRegression()
logReg.fit(X_train, y_train)

y_log_pred = logReg.predict(X_test)

print "logistic approach..", metrics.accuracy_score(y_test, y_log_pred)
