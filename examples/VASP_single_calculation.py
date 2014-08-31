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

input_parm=interface_script.init_simulation(0)

os.chdir('../temp/test')

test_job=job.job(subdir=False)
test_kgrid=kpoint.kpoint()
test_crystal=crystal_structure.a7_structure(element.Bi_exp,length_unit=1.0)
test_calc=VASP.calculator_VASP(False,test_job,test_crystal,test_kgrid,scheme=0)
test_calc.run_calculation()






