# Density_Function_Theory - KIT  v1.0.0 
# August 2014
# Implementation for how to construct calculation for doing VASP calculation with DFT_KIT

import numpy as np
import os
import sys

from DFT_KIT.core import job, kpoint, element, crystal_3D
from DFT_KIT.calculator import Pseudo_Potential
from DFT_KIT.apps import crystal_structure
from DFT_KIT.interface import interface_script
from DFT_KIT.apps import bismuth_antimony


[input_parm,opt_parm]=interface_script.init_simulation(0)
os.chdir('/Users/shiangfang/Shiang DrobBox/Dropbox/Physics Research/Tim Kaxiras Group/temp')

dft_job=job.job(subdir=False,job_manager_mode=False,write_post_process=False)
dft_calc=Pseudo_Potential.calculator_LD1X(True,dft_job,None)
dft_calc.read_UPF('Sb.UPF')

print(dft_calc.upf_data['PP_SPIN_ORB'])


