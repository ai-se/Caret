# __author__ = 'WeiFu'
from __future__ import division
from settings import *
from os import listdir
from os.path import join, isfile
from time import strftime
from sk import *
# from tuner_JADE import *
from tuner import *
from smote import *
from gridSearch import *


class Learner(object):
  def __init__(i, train, tune, test):
    i.train = train
    i.tune = tune
    i.test = test

  def untuned(i):
    The.data.predict = i.test
    The.data.train = i.train
    i.default()
    The.option.tuning = False
    pdb.set_trace()
    score = i.call()
    return score

  def tuned(i):
    The.data.predict = i.tune
    The.data.train = i.train
    The.option.tuning = True
    i.optimizer()
    The.option.tuning = False
    The.data.predict = i.test
    pdb.set_trace()
    score = i.call()
    return score

  def call(i):
    raise NotImplementedError

  def optimizer(i):
    raise NotImplementedError

  def default(i):
    raise NotImplementedError


class Where(Learner):
  def __init__(i, train, tune, predict):
    super(Where, i).__init__(train, tune, predict)
    i.tunelst = ["The.tree.infoPrune", "The.tree.min", "The.option.threshold", "The.where.wriggle",
                 "The.where.depthMax", "The.where.depthMin", "The.option.minSize", "The.tree.prune", "The.where.prune"]
    i.tune_min = [0.01, 1, 0.01, 0.01, 1, 1, 0.01, True, False]
    i.tune_max = [1, 10, 1, 1, 20, 6, 1, True, False]

  def default(i):
    The.option.baseLine = True
    The.tree.infoPrune = 0.33
    The.option.threshold = 0.5
    The.tree.min = 4
    The.option.minSize = 0.5  # min leaf size
    The.where.depthMin = 2  # no pruning till this depth
    The.where.depthMax = 10  # max tree depth
    The.where.wriggle = 0.2    #  set this at init()
    The.where.prune = False  # pruning enabled?
    The.tree.prune = True

  def call(i): return main()

  def optimizer(i):
    tuner = WhereDE(i)
    tuner.DE()


class CART(Learner):
  def __init__(i, train, tune, predict):
    super(CART, i).__init__(train, tune, predict)
    i.tunelst = ["The.cart.max_features", "The.cart.max_depth", "The.cart.min_samples_split",
                 "The.cart.min_samples_leaf", "The.option.threshold"]
    i.tune_min = [0.01, 1, 2, 1, 0.01]
    i.tune_max = [1, 50, 20, 20, 1]

  def default(i):
    The.cart.max_features = None
    The.cart.max_depth = None
    The.cart.min_samples_split = 2
    The.cart.min_samples_leaf = 1
    The.option.threshold = 0.5

  def call(i): return cart()

  def optimizer(i):
    tuner = CartDE(i)
    tuner.DE()


class RF(Learner):
  def __init__(i, train, tune, predict):
    super(RF, i).__init__(train, tune, predict)
    i.tunelst = ["The.rf.min_samples_split", "The.rf.min_samples_leaf ", "The.rf.max_leaf_nodes", "The.rf.n_estimators",
                 "The.rf.max_features", "The.option.threshold"]
    i.tune_min = [1, 2, 10, 50, 0.01, 0.01]
    i.tune_max = [20, 20, 50, 150, 1, 1]
    i.default_value = [2,1,None, 100,"auto",0.5]

  def default(i):
    # for key,val in zip(i.tunelst,i.default_value):
    #   setattr(key[],key[4:],val)
    # pdb.set_trace()
    The.option.threshold = 0.5
    The.rf.max_features = "auto"
    The.rf.min_samples_split = 2
    The.rf.min_samples_leaf = 1
    The.rf.max_leaf_nodes = None
    The.rf.n_estimators = 100

  def call(i): return rf()

  def optimizer(i):
    tuner = RfDE(i)
    tuner.DE()


def createfile(objective):
  The.option.resultname = '/Users/WeiFu/Google Drive/myresult_DE_gen_20' + strftime("%Y-%m-%d %H:%M:%S") + objective
  f = open(The.option.resultname, 'w').close()


def writefile(s):
  global The
  f = open(The.option.resultname, 'a')
  f.write(s + '\n')
  f.close()


def start(obj,path="./data", isSMOTE= False):
  def keep(learner, score):  # keep stats from run
    NDef = learner + ": N-Def"
    YDef = learner + ": Y-Def"
    for j, s in enumerate(lst):
      s[NDef] = s.get(NDef, []) + [(float(score[0][j] / 100))]
      s[YDef] = s.get(YDef, []) + [(float(score[1][j] / 100))]  # [YDef] will void to use myrdiv.

  def printResult(dataname):
    def myrdiv(d):
      stat = []
      for key, val in d.iteritems():
        val.insert(0, key)
        stat.append(val)
      return stat

    print "\n" + "+" * 20 + "\n DataSet: " + dataname + "\n" + "+" * 20
    for j, k in enumerate(["pd", "pf", "prec", "f", "g","w"]):
      express = "\n" + "*" * 10 + k + "*" * 10
      writefile(express)
      rdivDemo(myrdiv(lst[j]))
    writefile("End time :" + strftime("%Y-%m-%d %H:%M:%S") + "\n" * 2)
    print "\n"

  global The
  The.option.tunedobjective = obj # 0->pd, 1->pf,2->prec, 3->f, 4->g
  objectives = {0: "pd", 1: "pf", 2: "prec", 3: "f", 4: "g", 5:"combined"}
  createfile(objectives[The.option.tunedobjective])
  folders = [f for f in listdir(path) if not isfile(join(path, f))]
  for folder in folders[:]:
    nextpath = join(path, folder)
    data = [join(nextpath, f) for f in listdir(nextpath) if isfile(join(nextpath, f))]
    for i in range(len(data)):
      random.seed(1)
      pd, pf, prec, F, g, w= {}, {}, {}, {}, {},{}
      lst = [pd, pf, prec, F, g,w]
      expname = folder + "V" + str(i)
      try:
        predict = data[i + 2]
        tune = data[i + 1]
        if isSMOTE:
          train = ["./Smote"+ data[i][1:]]
        else:
          train = data[i]
      except IndexError, e:
        print folder + " done!"
        break
      title =  "Tuning objective: " +objectives[The.option.tunedobjective] + "\nBegin time: " + strftime(
        "%Y-%m-%d %H:%M:%S")
      # pdb.set_trace()
      writefile(title)
      writefile("Dataset: "+expname)
      for model in [CART,RF]:  # add learners here!
        for task in ["Tuned_", "Naive_","Grid_"]:
          writefile("-"*30+"\n")
          timeout = time.time()
          name = task + model.__name__
          thislearner = model(train, tune, predict)
          if task == "Tuned_":
            keep(name, thislearner.tuned())
          elif task == "Naive_":
            keep(name, thislearner.untuned())
          elif task == "Grid_":
            keep(name, grid_search(thislearner))
          run_time =name + " Running Time: " + str(round(time.time() - timeout, 3))
          print run_time
          writefile(run_time)
      printResult(expname)


if __name__ == "__main__":
  # SMOTE()
  for i in [2,3]:
    start(i)

