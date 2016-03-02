from __future__ import  division, print_function
import sys
import subprocess

# run_max.py
import subprocess

# Define command and arguments
command = 'Rscript'
path2script = 'testPython.R'

# Variable number of args in a list
args = ['./NASA/JM1.csv', '0.000000005']

# Build subprocess command
cmd = [command, path2script] + args

# check_output will run the command and store to result
x = subprocess.check_output(cmd, universal_newlines=True)

print('The maximum of the numbers is:', x)