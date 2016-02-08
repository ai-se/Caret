from __future__ import division, print_function
# __author__ = 'WeiFu'
from read import Read as result
import pdb
from plots import *


class Compare(object):
  '''
  this class is to compare the improvement of the new method
  over the old one.
  '''

  def __init__(self, old_path, new_path):
    self.improve = {}
    self.old_path = old_path
    self.new_path = new_path

  def calculate(self, learner):
    '''
    calculate the improvements for one learner
    '''
    res = []
    oldresult = result(self.old_path).read()
    newresult = result(self.new_path).read()
    for old, new in zip(oldresult[learner], newresult[learner]):
      res.append(new - old)
    return res

  def tell(self):
    '''
    tell improvements of three learners
    '''
    for learner in ['Tuned_Where', 'Tuned_CART', 'Tuned_RF']:
      self.improve[learner] = self.calculate(learner)
    # pdb.set_trace()
    # print(self.improve)
    return self.improve

def JADE():
  prec_DE = "../result/1102JADE_DE/myresult_DE_gen_202015-11-02 00:21:36prec"
  prec_JADE = "../result/1102JADE_DE/myresult_JADE_gen_202015-11-01 09:30:57prec"
  f_DE = "../result/1102JADE_DE/myresult_DE_gen_202015-11-02 05:13:38f"
  f_JADE = "../result/1102JADE_DE/myresult_JADE_gen_202015-11-01 14:27:08f"
  PREC = Compare(prec_DE, prec_JADE).tell()
  F = Compare(f_DE, f_JADE).tell()
  show([PREC,F],['PREC Improvements','F Improvements'])


if __name__ == "__main__":
  JADE()
  # prec_oldsrc = '../result/0906/np=10_f_precision/myresult2015-09-06 18:44:48prec'
  # prec_newsrc = '../result/1028/myresult2015-10-28 03:50:19prec'
  # f_oldsrc = "../result/0906/np=10_f_precision/myresult2015-09-06 21:56:38f"
  # f_newsrc ="../result/1028/myresult2015-10-28 05:32:42f"
  # PREC = Compare(prec_oldsrc, prec_newsrc).tell()
  # F = Compare(f_oldsrc, f_newsrc).tell()
  # show([PREC,F],['PREC Improvements','F Improvements'])
