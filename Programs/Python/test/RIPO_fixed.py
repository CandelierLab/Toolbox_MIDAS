import os
import time
import numpy as np

from MIDAS.enums import *
from MIDAS.polar_grid import PolarGrid
from MIDAS.coefficients import Coefficients
from MIDAS.engine import Engine

os.system('clear')

# === Parameters ===========================================================

dataDir = '/home/raphael/Science/Projects/CM/MovingAgents/Data/'
movieDir = '/home/raphael/Science/Projects/CM/MovingAgents/Movies/'

# === Engine ===============================================================

E = Engine()
# E = Engine(arena=Arena.CIRCULAR)

# Number of steps
E.steps = None

# === Agents ===============================================================

# --- Fixed agents ---------------------------------------------------------

E.add_group(Agent.FIXED, 2, name='fixed')

# --- RIPO agents ----------------------------------------------------------

#  --- Inputs

# polar grid
G = PolarGrid(rZ=[], nSa = 4)

in_presence = E.add_input(Perception.PRESENCE,
                          normalization = Normalization.SAME_GROUP,
                          grid = G)

# in_orientation = E.add_input(Perception.ORIENTATION, 
#                             normalization = Normalization.NONE,
#                             grid = G,
#                             coefficients = [1, 1, 1, 1, 0, 0, 0, 18])

# --- Outputs 

out_da = E.add_output(Action.REORIENTATION,
                      activation = Activation.HSM_CENTERED)

# out_dv = E.add_output(Action.SPEED_MODULATION,
#                       activation = Activation.HSM_CENTERED)

# --- Groups

# Initial conditions
N = 2
IC = {'position': None,
      'orientation': None,
      'speed': 0.01} 

# IC = {'position': [[0,0], [0.2,0.3]],
#       'orientation': [1.5, 0],
#       'speed': 0.01}
# N = len(IC['position']) 

E.add_group(Agent.RIPO, N, name='agents',
            initial_condition = IC,
            rmax = None,
            inputs=[in_presence], outputs=[out_da])

# # --- Coefficients

E.set_coefficients(in_presence, np.array([-1, -1, -1, -1, 0.1, 0.1, 0.1, 0.1]))

# C = np.array([1,1,1,1, 0, 0, 0, 0])*2


# === Storage ==============================================================

# E.setup_storage(dataDir + 'RIPO/test.db')
# E.storage.db_commit_each_step = True

# === Visualization ========================================================

E.setup_animation(agents=AnimAgents.ALL, field=AnimField.DENSITY)
E.animation.trace_duration = 10
# E.animation.group_options['agents']['cmap'] = 'hsv'
E.animation.field_options['range'] = [0, 0.05]

# === Simulation ===========================================================

# E.window.movieFile = movieDir + 'test.mp4'

E.window.autoplay = False
E.run()