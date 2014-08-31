# Density_Function_Theory - KIT  v1.0.0 
# August 2014
# Implementation for how to construct calculation for multiple parameters

import sys
import numpy as np
import os

from DFT_KIT.core import job, kpoint, element, crystal_3D
from DFT_KIT.calculator import VASP, QESPRESSO, Wannier90
from DFT_KIT.apps import crystal_structure
from DFT_KIT.interface import interface_script

input_parm=interface_script.init_simulation(0)

# main section for loading and running calculation

os.chdir('../test/')
#job
dft_job=job.job(False)

#crystal (can be condensed into a specialized class)
dft_lattice=crystal_3D.cubic_3D(2.56)
at1=dft_lattice.add_atom(element.Bi_exp, position=np.array([0.0,0.0,0.0]),cc=3.45)
at2=dft_lattice.add_atom(element.Bi_exp, position=np.array([1.0,1.0,1.0]),cc=3.1415)

#calculator
dft_vasp=VASP.calculator_VASP()





