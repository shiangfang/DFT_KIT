# Density_Function_Theory - KIT  v1.0.0 
# August 2014
# Implementation for how to construct calculation for doing VASP calculation with DFT_KIT

import numpy as np
import os
import sys

from DFT_KIT.core import job, kpoint, element, crystal_3D
from DFT_KIT.calculator import QESPRESSO, Wannier90
from DFT_KIT.apps import crystal_structure

print('---------------------------------------------')
print('     DFT_KIT program')
print('---------------------------------------------')
print('\n')
print('Multiple process: arguments')
print(sys.argv)

os.chdir('../test')

test_job=job.job(subdir=False)
test_kgrid=kpoint.kpoint()
test_crystal=crystal_structure.a7_structure(element.Bi_exp,length_unit=1.0)
test_calc=QESPRESSO.calculator_QESPRESSO(False,test_job,test_crystal,test_kgrid,scheme=1)
test_calc.run_calculation()







