from __future__ import division, print_function
import sys
import pdb
import random
import numpy as np
import subprocess


class Learner(object):
    def __init__(self, r_src):
        self.path2script = r_src

    def call_model(self, data_src, param):
        # Define command and arguments
        command = 'Rscript'
        path2script = self.path2script

        # Variable number of args in a list
        param_str = [ str(i) for i in  param]
        my_args = data_src + param_str
        # my_args.append(str(param))  # ['./NASA/JM1.csv', '0.000000005']

        # Build subprocess command
        pdb.set_trace()
        cmd = [command, path2script] + my_args

        # check_output will run the command and store to result
        x = subprocess.check_output(cmd, universal_newlines=True)

        print('The maximum of the numbers is:', x)
        return x


class CART(Learner):
    def __init__(self, r_src="cart.R"):
        self.tunelst = ["cp"]
        self.tune_min = [0.0001]
        self.tune_max = [0.5]
        self.default = [0.01]
        super(CART, self).__init__(r_src)

    def call_model(self, data_src, param):
        super(CART, self).call_model(data_src, param)

    def tuned_parameters(self):
        return [{'complexity': [0.0001, 0.5]}]


class C50(Learner):
    def __init__(self, r_src):
        self.tunelst = ["trials", "winnow", "model"]
        self.tune_min = [1, False, "tree"]
        self.tune_max = [50, True, "rules"]
        self.default = [1, False, "rules"]
        super(C50, self).__init__(r_src)

    def call_model(self, data_src, param):
        super(C50, self).call_model(data_src, param)


class avnnet(Learner):
    def __init__(self, r_src):
        self.tunelst = ["size", "decay", "bag"]
        self.tune_min = [1, 0, True]
        self.tune_max = [9, 0.1, False]
        self.default = [1, 0.1, False]
        super(avnnet, self).__init__(r_src)

    def call_model(self, data_src, param):
        super(avnnet, self).call_model(data_src, param)
