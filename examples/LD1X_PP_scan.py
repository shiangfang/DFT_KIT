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
dft_job=job.job(subdir=False,job_manager_mode=False,write_post_process=False)
dft_calc=Pseudo_Potential.calculator_LD1X(False,dft_job,None)
dft_calc.load_parm(False,bismuth_antimony.Bi_ld1x)

numrc=16
nums1=16
nump1=16
nump2=16
allrc=np.linspace(2.5,4.0,numrc)
alls1=np.linspace(2.5,4.0,nums1)
allp1=np.linspace(2.5,4.0,nump1)
allp2=np.linspace(2.5,4.0,nump2)

ind=0
root_dir=os.getcwd()+'/'

for indrc in allrc:
    for inds1 in alls1:
        for indp1 in allp1:
            for indp2 in allp2:
                newdir=root_dir+'task_'+str(ind)+'/'
                os.mkdir(newdir)
                os.chdir(newdir)
                dft_calc.set_parm('rcloc',str(indrc))
                tmp=[]
                tmp.append('6S 1 0 2.00 0.00 '+ str(inds1)+' '+str(inds1) +' 0.5')
                tmp.append('6P 2 1 2.00 0.00 '+ str(indp1)+' '+str(indp1) +' 0.5')
                tmp.append('6P 2 1 0.00 0.45 '+ str(indp1)+' '+str(indp1) +' 0.5')
                tmp.append('6P 2 1 1.00 0.00 '+ str(indp2)+' '+str(indp2) +' 1.5')
                tmp.append('6P 2 1 0.00 0.45 '+ str(indp2)+' '+str(indp2) +' 1.5')
                dft_calc.pp_card=tmp
                
                dft_calc.run_calculation()
                ind=ind+1


