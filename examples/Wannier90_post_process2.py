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
#from DFT_KIT.apps import bismuth_antimony

os.chdir('/Users/shiangfang/Desktop/Temp/mos2/mos2.vaspwan/')
os.chdir('/Users/shiangfang/Desktop/Temp/mos2-tb-pd/')
#os.chdir('/Users/shiangfang/Desktop/Temp')


dft_job=job.job(subdir=False)
dft_job.sys_info['wan90_seedname']='wannier90'
dft_wan90=Wannier90.calculator_Wannier90(True,dft_job,None,None)
dft_wan90.parms['hr_plot']='T'
dft_wan90.parms['num_wann']='11'
dft_wan90.parms['write_xyz']='T'

dft_wan90.post_process()
dft_wan90.save_post_process()








