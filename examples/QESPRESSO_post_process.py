# Density_Function_Theory - KIT  v1.0.0 
# August 2014
# Implementation for how to construct calculation for doing VASP calculation with DFT_KIT

import numpy as np
import os
import sys

from DFT_KIT.core import job, kpoint, element, crystal_3D
from DFT_KIT.calculator import VASP, Wannier90, QESPRESSO
from DFT_KIT.apps import crystal_structure
from DFT_KIT.interface import interface_script

[input_parm,opt_parm]=interface_script.init_simulation(0)



