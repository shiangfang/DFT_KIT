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




upfdata1=dft_calc.read_UPF('Sb.UPF')
#print(upfdata1['PP_HEADER'])
upfdata2=dft_calc.read_UPF('Sb.UPF')
upfdata3=dft_calc.vca_mixing(upfdata1,upfdata2,0.5)
dft_calc.write_UPF(upfdata3,'SBMIX.UPF')


#print(len(upfdata['PP_R_DATA']))
#print(upfdata['PP_R_DATA'])

#print(len(upfdata['PP_RAB_DATA']))
#print(upfdata['PP_RAB_DATA'])

#print(len(upfdata['PP_LOCAL_DATA']))
#print(upfdata['PP_LOCAL_DATA'])

#print(len(upfdata['PP_NONLOCAL']))
#print(upfdata['PP_NONLOCAL_DATA'])
#print(len(upfdata['PP_NONLOCAL_DATA'][0]))
#print(len(upfdata['PP_NONLOCAL_DATA'][1]))
#print(len(upfdata['PP_NONLOCAL_DATA'][2]))
#print(upfdata['PP_NONLOCAL_DATA'][0])
#print(upfdata['PP_NONLOCAL_DATA'][1])
#print(upfdata['PP_NONLOCAL_DATA'][2])

#print(upfdata['PP_DIJ_DATA'])

#print(len(upfdata['PP_PSWFC_DATA']))
#print(upfdata['PP_PSWFC_DATA'][0])
#print(upfdata['PP_PSWFC_DATA'][1])
#print(upfdata['PP_PSWFC_DATA'][2])

#print(upfdata['PP_RHOATOM_DATA'])

#cc=np.array([2,3,4,5])
#dd=np.array(cc)

#print(2.0*(np.array([3,4,5,6]).reshape((2,2))))
#print('%.9e' % 100.0)

