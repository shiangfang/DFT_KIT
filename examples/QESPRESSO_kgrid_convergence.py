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

[input_parm,opt_parm]=interface_script.init_simulation(1)
scan_index=int(input_parm[0])
k_min=5
k_max=10
all_ks=range(k_min,k_max+1)
k_now=all_ks[scan_index]

test_job=job.job(subdir=False)

# first round, self-consistent calculation
test_kgrid=kpoint.kpoint()
#set the kgrid

test_job.sys_info['qes_fname']='bis'
test_crystal=crystal_structure.a7_structure(bismuth_antimony.Bi_exp,length_unit=1.0)
test_calc=QESPRESSO.calculator_QESPRESSO(False,test_job,test_crystal,test_kgrid,scheme=0)
test_calc.load_parm(False, bismuth_antimony.Bi_qespresso_crystal_scf)
test_calc.run_calculation()



