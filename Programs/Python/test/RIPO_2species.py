import os
import time
import numpy as np

from MIDAS.enums import *
from MIDAS.polar_grid import PolarGrid
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

# --- RIPO agents ----------------------------------------------------------

#  --- Inputs

# polar grid
G = PolarGrid(rZ=[], nSa = 4)

in_presence_1 = E.add_input(Perception.PRESENCE,
                          normalization = Normalization.SAME_GROUP,
                          grid = G)

in_presence_2 = E.add_input(Perception.PRESENCE,
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
N = 100

E.add_group(Agent.RIPO, N, name='agents_1',
            inputs=[in_presence_1], outputs=[out_da])

E.add_group(Agent.RIPO, N, name='agents_2',
            inputs=[in_presence_2], outputs=[out_da])

# --- Coefficients

E.set_coefficients(in_presence_1, np.array([1, 1, 1, 1, 0, 0, 0, 0]))
E.set_coefficients(in_presence_2, np.array([1, 1, 1, 1, -1, -1, -1, -1]))

# === Storage ==============================================================

# E.setup_storage(dataDir + 'RIPO/test.db')
# E.storage.db_commit_each_step = True

# === Visualization ========================================================

E.setup_animation(agents=AnimAgents.ALL)
E.animation.trace_duration = 10
E.animation.group_options['agents_1']['color'] = 'cyan'
E.animation.group_options['agents_2']['color'] = 'orange'

# === Simulation ===========================================================

# E.window.movieFile = movieDir + 'test.mp4'

# E.window.autoplay = False
E.run()