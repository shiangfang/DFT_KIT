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
os.chdir('/Users/shiangfang/Shiang DrobBox/Dropbox/Physics Research/Tim Kaxiras Group/temp/allps')

dft_job=job.job(subdir=False,job_manager_mode=False,write_post_process=False)
dft_calc=Pseudo_Potential.calculator_LD1X(True,dft_job,None)

x_start=0.0
x_end=1.0
num_xs=21
vca_xs=np.linspace(x_start,x_end,num_xs)


upfdata_bi=dft_calc.read_UPF('Bi.UPF')
upfdata_sb=dft_calc.read_UPF('Sb.UPF')

for indx in range(0,num_xs):
    alloy_x=vca_xs[indx]

    upfdata_vca=dft_calc.vca_mixing(upfdata_bi,upfdata_sb,1.0-alloy_x)
    dft_calc.write_UPF(upfdata_vca,'BiSb_ALLOY_B_'+str(indx)+'.UPF')

