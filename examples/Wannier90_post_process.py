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
from DFT_KIT.apps import bismuth_antimony

[input_parm,opt_parm]=interface_script.init_simulation(1)

test_job=job.job(subdir=False)
test_job.sys_info['wan90_seedname']=input_parm[0]
test_wan90=Wannier90.calculator_Wannier90(True,test_job,None,None)
test_wan90.load_parm(False, bismuth_antimony.Bi_wannier90)
test_wan90.add_projections(['random','Bi: l=0;l=1'])
test_wan90.post_process()
test_wan90.save_post_process()








