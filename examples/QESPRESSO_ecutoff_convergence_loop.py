# Density_Function_Theory - KIT  v1.0.0 
# August 2014
# Implementation for how to construct calculation for doing VASP calculation with DFT_KIT

import numpy as np
import os
import sys

from DFT_KIT.core import job, kpoint, element, crystal_3D
from DFT_KIT.calculator import QESPRESSO
from DFT_KIT.apps import crystal_structure
from DFT_KIT.interface import interface_script
from DFT_KIT.apps import bismuth_antimony

[input_parm,opt_parm]=interface_script.init_simulation(0)
e_min=15.0
e_max=50.0
e_num=36
all_es=np.linspace(e_min,e_max,e_num)

test_job=job.job(subdir=True,job_manager_mode=True)

# first round, self-consistent calculation
test_kgrid=kpoint.kpoint()
test_job.sys_info['qes_fname']='bis'
test_crystal=crystal_structure.a7_structure(bismuth_antimony.Bi_exp,length_unit=1.0)
test_calc=QESPRESSO.calculator_QESPRESSO(False,test_job,test_crystal,test_kgrid,scheme=1)
test_calc.load_parm(False, bismuth_antimony.Bi_qespresso_crystal_scf)

for ind,e_now in enumerate(all_es):
    if ind>0:
        test_job.next_task(True)
    test_calc.set_parm('ecutwfc', str(e_now))
    test_calc.run_calculation()


