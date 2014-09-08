# Density_Function_Theory - KIT  v1.0.0 
# August 2014
# Implementation for how to construct calculation for doing VASP calculation with DFT_KIT

import numpy as np
import os
import sys

from DFT_KIT.core import job, kpoint, element, crystal_3D
from DFT_KIT.calculator import VASP
from DFT_KIT.apps import crystal_structure
from DFT_KIT.interface import interface_script
from DFT_KIT.apps import bismuth_antimony

[input_parm,opt_parm]=interface_script.init_simulation(1)
scan_parm_index=int(input_parm[0])

k_mesh=range(10,21)
scan_k=k_mesh[scan_parm_index]

test_job=job.job(subdir=True)
test_kgrid=kpoint.kpoint()
test_kgrid.set_grid_mode([scan_k,scan_k,scan_k])
test_crystal=crystal_structure.a7_structure(bismuth_antimony.Bi_exp,length_unit=1.0)
test_calc=VASP.calculator_VASP(False,test_job,test_crystal,test_kgrid,scheme=0)
test_calc.run_calculation()






