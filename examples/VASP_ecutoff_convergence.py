# Density_Function_Theory - KIT  v1.0.0 
# August 2014
# Implementation for how to construct calculation for doing VASP calculation with DFT_KIT

import numpy as np
import os
import sys

from DFT_KIT.core import job, kpoint, element, crystal_3D
from DFT_KIT.calculator import VASP
from DFT_KIT.apps import crystal_structure


print('---------------------------------------------')
print('     DFT_KIT program')
print('---------------------------------------------')
print('\n')
print('Multiple process: arguments')
print(sys.argv)

expect_num_parm=1
input_num_parm=len(sys.argv)
if input_num_parm < (expect_num_parm+1):
    print('ERROR: wrong number of input parameters for the program')
    exit()
    
input_parm=[]
for ind in range(1,expect_num_parm+1):
    input_parm.append(sys.argv[ind])

e_ind=int(input_parm[0])
all_es=np.linspace(200,300,6)
e_now=all_es[e_ind]

test_job=job.job(subdir=False)
test_kgrid=kpoint.kpoint()
test_crystal=crystal_structure.a7_structure(element.Bi_exp,length_unit=1.0)
test_calc=VASP.calculator_VASP(False,test_job,test_crystal,test_kgrid,scheme=0,xc='PBE',ENCUT=str(e_now))
test_calc.run_calculation()




