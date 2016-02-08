from __future__ import division, print_function
from main import *
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn import svm
from sklearn.naive_bayes import GaussianNB
from sklearn import linear_model
from newabcd import *

def csv2py(f):
  if isinstance(f, list):
    tbl = [table(src) for src in f]  # tbl is a list of tables
  else:
    tbl = table(f)
  tbl_num = tbl[0] if isinstance(tbl, list) else tbl  # no symbol data col in defect data sets.
  return tbl_num


def _Abcd(predicted, actual):
  predicted_txt = []
  abcd = Abcd(db='Traing', rx='Testing')
  global The

  def isDef(x):
    return "Defective" if x >= The.option.threshold else "Non-Defective"  # use the.option.threshold for cart,
    # rf and where!!

  for data in predicted:
    predicted_txt += [isDef(data)]
  # for act, pre in zip(actual, predicted_txt):
  #   abcd.tell(act, pre)
  # abcd.header()
  # score = abcd.ask()
  # pdb.set_trace()
  score =sk_abcd(predicted_txt,actual)
  return score


def learn(clf):
  def conv(x):
    return [float(i) for i in x]
  testdata, actual = buildtestdata1(The.data.predict)
  traintable = csv2py(The.data.train)
  traindata_X = [conv(row.cells[:-1]) for row in traintable._rows]
  traindata_Y = [(row.cells[-1]) for row in traintable._rows]
  predictdata_X = [conv(row.cells[:-1]) for row in testdata]
  predictdata_Y = [(row.cells[-1]) for row in testdata]
  clf = clf.fit(traindata_X, traindata_Y)
  array = clf.predict(predictdata_X)
  predictresult = [i for i in array]
  scores = _Abcd(predictresult, actual)
  return scores


def cart():
  clf = DecisionTreeRegressor(max_features=The.cart.max_features, max_depth=The.cart.max_depth,
                                min_samples_split=The.cart.min_samples_split,
                                min_samples_leaf=The.cart.min_samples_leaf, random_state=1)
  return learn(clf)

def rf():
  clf = RandomForestRegressor(n_estimators=The.rf.n_estimators, max_features=The.rf.max_features,
                                min_samples_split=The.rf.min_samples_split, min_samples_leaf=The.rf.min_samples_leaf,
                                max_leaf_nodes=The.rf.max_leaf_nodes, random_state=1)
  return learn(clf)



# def callsvm():
#   clf = None
#   if The.classifier.svmtuned:
#     assert isinstance(The.svm.degree, int) == True
#     clf = svm.SVR(C=The.svm.C, epsilon=The.svm.epsilon, kernel='sigmoid')
#   # , degree=The.svm.degree, gamma=The.svm.gamma,coef0=The.svm.coef0, shrinking=The.svm.shrinking,tol=The.svm.tol
#   elif The.classifier.svm:
#     clf = svm.SVR(C=1.0, epsilon=0.1, kernel='sigmoid')
#   return learn(clf)


def callbayes():
  clf = GaussianNB()
  return learn(clf)


def calllogistic():
  clf = linear_model.LogisticRegression()
  return learn(clf)


if __name__ == "__main__":
  eval(cmd())
