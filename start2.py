# __author__ = 'WeiFu'
from __future__ import division
from settings import *
from os import listdir
from os.path import join, isfile
from sk import *
from smote import *
from os import getenv
from learner import *
import time
from gridSearch import *


def createfile(objective):
    home_path = getenv("HOME")
    The.option.resultname = (home_path + '/Google Drive/EXP/myresult'
                             + strftime("%Y-%m-%d %H:%M:%S") + objective)
    f = open(The.option.resultname, 'w').close()


def writefile(s):
    global The
    f = open(The.option.resultname, 'a')
    f.write(s + '\n')
    f.close()


def start(obj, path="./data", isSMOTE=False, repeats=5):
    def keep(learner, score):  # keep stats from run
        NDef = learner + ": N-Def"
        YDef = learner + ": Y-Def"
        for j, s in enumerate(lst):
            # s[NDef] = s.get(NDef, []) + [(float(score[0][j] / 100))]
            s[YDef] = s.get(YDef, []) + [(float(score[1][j] / 100))]
            # [YDef] will void to use myrdiv.

    def printResult(dataname):
        def count_better(dicts):
            temp = {}
            learner_name = set([i[i.index("_") + 1:i.index(":")] for i in dicts.keys()])
            for key, val in dicts.iteritems():
                if "Y-Def" in key and ("Tuned_" in key or "Grid_" in key):
                    temp[key] = np.median(val)
            for each in learner_name:
                tune = "Tuned_" + each + ": Y-Def"
                grid = "Grid_" + each + ": Y-Def"
                if temp[tune] >= temp[grid]:
                    which_is_better[tune] = which_is_better.get(tune, 0) + 1
                else:
                    which_is_better[grid] = which_is_better.get(grid, 0) + 1

        def myrdiv(d):
            stat = []
            for key, val in d.iteritems():
                val.insert(0, key)
                stat.append(val)
            return stat

        print "\n" + "+" * 20 + "\n DataSet: " + dataname + "\n" + "+" * 20
        obj = ["pd", "pf", "prec", "f", "g", "auc"]
        for j, k in enumerate(obj):
            express = "\n" + "*" * 10 + " " + k + " " + "*" * 10
            print express
            writefile(express)
            # pdb.set_trace()
            if j == The.option.tunedobjective:
                count_better(lst[j])
            rdivDemo(myrdiv(lst[j]))
        out_better = "\n In terms of " + obj[The.option.tunedobjective] + " : the times of better tuners are" + str(
            which_is_better)
        print out_better
        writefile(out_better)
        writefile("End time :" + strftime("%Y-%m-%d %H:%M:%S") + "\n" * 2)
        print "\n"

    global The
    which_is_better = {}
    The.option.tunedobjective = obj  # 0->pd, 1->pf,2->prec, 3->f, 4->g
    objectives = {0: "pd", 1: "pf", 2: "prec", 3: "f", 4: "g", 5: "auc"}
    createfile(objectives[The.option.tunedobjective])
    folders = [f for f in listdir(path) if not isfile(join(path, f))]
    for folder in folders[:]:
        nextpath = join(path, folder)
        data = [join(nextpath, f) for f in listdir(nextpath)
                if isfile(join(nextpath, f)) and ".DS" not in f]
        for i in range(len(data)):
            pd, pf, prec, F, g, auc = {}, {}, {}, {}, {}, {}
            lst = [pd, pf, prec, F, g, auc]
            expname = folder + "V" + str(i)
            try:
                predict = data[i + 2]
                tune = data[i + 1]
                if isSMOTE:
                    train = ["./Smote" + data[i][1:]]
                else:
                    train = data[i]
            except IndexError, e:
                print folder + " done!"
                break
            title = ("Tuning objective: " + objectives[The.option.tunedobjective]
                     + "\nBegin time: " + strftime("%Y-%m-%d %H:%M:%S"))
            # pdb.set_trace()
            writefile(title)
            writefile("Dataset: " + expname)
            for model in [CART, RF]:  # add learners here!
                for task in ["Naive_","Tuned_","Grid_"]:
                    random.seed(1)
                    writefile("-" * 30 + "\n")
                    timeout = time.time()
                    name = task + model.__name__
                    thislearner = model(train, tune, predict)
                    # keep(name, thislearner.tuned() if task == "Tuned_" else thislearner.untuned())
                    if task == "Tuned_":
                        for _ in xrange(repeats):
                            temp = thislearner.tuned()
                            keep(name, temp)
                    elif task == "Naive_":
                        keep(name, thislearner.untuned())
                    elif task == "Grid_":
                        for _ in xrange(repeats):
                            temp = gridSearch(thislearner, objectives[The.option.tunedobjective])
                            keep(name, temp)
                    run_time = name + " Running Time: " + str(round(time.time() - timeout, 3)/repeats)
                    print run_time
                    writefile(run_time)
            printResult(expname)


if __name__ == "__main__":
    # SMOTE()
    for i in [2,3,5]:
        start(i)
