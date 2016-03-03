from __future__ import division, print_function
import sys
import pdb
from os.path import join, isfile
from os import listdir
from caret_learner import *
from caret_learner import *

def run(path="../dataR/"):
    folders = [f for f in listdir(path) if not isfile(join(path, f))]
    for folder in folders[:]:
        nextpath = join(path, folder)
        data = [join(nextpath, f) for f in listdir(nextpath) if
                isfile(join(nextpath, f)) and ".DS" not in f]
        for d in data:
            for l in [CART]:
                model = l()
                X = model.call_model([d],model.default)
                print(X)






if __name__ == "__main__":
    run()
