'''
Smart coefficients management
'''

import numpy as np
from MIDAS.enums import *
from MIDAS.polar_grid import PolarGrid

class Coefficients:

  def __init__(self, engine, i, C):

    # --- Relevant properties ----------------------------------------------

    self.engine = engine
    self.i = i

    self.nO = len(self.engine.outputs)
    self.nG = self.engine.groups.N

    if self.engine.inputs[self.i].grid is None:
      self.nCpO = 1

    else:
      grid = self.engine.inputs[self.i].grid
      self.nCpO = self.nG*grid.nZ  
      self.nSa = grid.nSa
      self.nSb = grid.nSb
      
    # Number of coefficients
    self.nC = self.nO*self.nCpO

    # --- Coefficients -----------------------------------------------------

    if isinstance(C, CoeffSet):
      match C:

        case CoeffSet.IGNORE: self.C = np.zeros(self.nC)

    else:
      self.C = np.array(C)

  def to_weights(self):
    '''
    Export the coeffificients to a weights array
    '''

    if self.engine.inputs[self.i].grid is None:
      return self.C

    W = []

    for i, Out in enumerate(self.engine.outputs):
      for j in range(self.nCpO):

        k = self.nCpO*i + j

        match Out.action:

          case Action.SPEED_MODULATION:
            W.append(self.C[k] if ((j+self.nSa/4) % self.nSa)<self.nSa/2 else -self.C[k])

          case Action.REORIENTATION:
            W.append(self.C[k] if (j % self.nSa)<self.nSa/2 else -self.C[k])

    return np.array(W)