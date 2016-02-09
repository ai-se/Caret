from __future__ import division, print_function
from sklearn import grid_search
from sklearn.tree import DecisionTreeClassifier
import numpy as np
from scikitlearners2 import *

def getParam(learner):
  params = None
  if learner.__class__.__name__.lower() == "cart":
    params = [{'max_features': np.arange(0.01, 1, 0.1),
               'max_depth': np.arange(1, 51, 5),
               'min_samples_split': np.arange(2, 20, 5),
               'min_samples_leaf': np.arange(2, 20, 5)}]
  clf = DecisionTreeClassifier
  return clf, params


def getScoring(goal):
  scoring = None
  if goal.lower() =="pd":
    scoring = 'recall'
  elif goal.lower() =="pf":
    raise ValueError("this goal is not implemented by scikit-learn!")
  elif goal.lower() =="prec":
    scoring = 'precision'
  elif goal.lower() == "f":
    scoring = 'f1_weighted'
  elif goal.lower() =="g":
    raise ValueError("this goal is not implemented by scikit-learn!")
  return scoring

def getData(learner):
  def conv(x):
    return [float(i) for i in x]
  train_src = [learner.train,learner.tune] ### remember, here, used both train and tune
  traintable = csv2py(train_src)
  traindata_X = [conv(row.cells[:-1]) for row in traintable._rows]
  traindata_Y = [(row.cells[-1]) for row in traintable._rows]
  traindata_Y = [1 if i >0 else 0 for i in traindata_Y ]
  # pdb.set_trace()
  # from sklearn.preprocessing import LabelBinarizer
  #
  # lb = LabelBinarizer()
  # y_train = np.array([number[0] for number in lb.fit_transform(traindata_Y)])
  return traindata_X, traindata_Y


def predict(test_src,clf_fitted):
  def conv(x):
    return [float(i) for i in x]

  testdata, actual = buildtestdata1(test_src)
  predictdata_X = [conv(row.cells[:-1]) for row in testdata]
  predictdata_Y = [(row.cells[-1]) for row in testdata]
  array = clf_fitted.predict(predictdata_X)
  predictresult = [i for i in array]
  scores = N_Abcd(predictresult, actual)
  return scores


def gridSearch(learner, goal):
  clf_init, parameters = getParam(learner)
  score_fun = getScoring(goal)
  train_X, train_Y = getData(learner)
  clf = grid_search.GridSearchCV(clf_init(random_state=1), parameters, cv=5, scoring=score_fun, refit=True)
  clf.fit(train_X,train_Y)
  best_params = clf.best_params_
  best_params["random_state"] = 1
  clf_fitted = clf_init(**best_params)
  clf_fitted.fit(train_X,train_Y)
  scores = predict(learner.test,clf_fitted)
  pdb.set_trace()
  return scores

