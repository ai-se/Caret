from __future__ import  division, print_function
import sys
import subprocess


def call_model(data_src, param):
    # run_max.py

    # Define command and arguments
    command = 'Rscript'
    path2script = 'py_caret.R'

    # Variable number of args in a list
    args = data_src.append(param)  #['./NASA/JM1.csv', '0.000000005']

    # Build subprocess command
    cmd = [command, path2script] + args

    # check_output will run the command and store to result
    x = subprocess.check_output(cmd, universal_newlines=True)

    print('The maximum of the numbers is:', x)
    return x