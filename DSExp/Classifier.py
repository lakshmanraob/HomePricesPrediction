from sklearn.neighbors import KNeighborsClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import sklearn.metrics as metrics
import numpy as np

import matplotlib.pyplot as plt

iris = load_iris()

X = iris.data
y = iris.target
score = []

# get target_names and display for the prediction

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=4)

narray = np.arange(1, 26)
for n in narray:
    knn = KNeighborsClassifier(n_neighbors=n)
    knn.fit(X_train, y_train)
    y_predict = knn.predict(X_test)
    score.append(metrics.accuracy_score(y_test, y_predict))

plt.plot(narray, score)
plt.xlabel("Value of K")
plt.ylabel("prediction accuracy")
