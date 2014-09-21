# Density_Function_Theory - KIT  v1.0.0 
# August 2014
# Implementation for how to construct calculation for doing VASP calculation with DFT_KIT

import numpy as np
import os
import sys
import pickle

from DFT_KIT.core import job, kpoint, element, crystal_3D
from DFT_KIT.calculator import QESPRESSO
from DFT_KIT.apps import crystal_structure
from DFT_KIT.interface import interface_script
from DFT_KIT.apps import bismuth_antimony

[input_parm,opt_parm]=interface_script.init_simulation(0)
e_min=15.0
e_max=60.0
e_num=46
all_es=np.linspace(e_min,e_max,e_num)
#e_now=all_es[int(input_parm[0])]

dft_job=job.job(subdir=True)
dft_job.process_opt_parm(opt_parm)

# first round, self-consistent calculation
dft_kgrid=kpoint.kpoint()
dft_job.sys_info['qes_prefix']='bismuth'
dft_job.sys_info['qes_fname']='bismuth_econv'
dft_crystal=crystal_structure.a7_structure(bismuth_antimony.Bi_exp,length_unit=1.0)
dft_calc=QESPRESSO.calculator_QESPRESSO(False,dft_job,dft_crystal,dft_kgrid,scheme=1)
dft_calc.load_parm(False, bismuth_antimony.Bi_qespresso_crystal_scf)

output_es=[]
for ind,e_now in enumerate(all_es):
    if ind>0:
        dft_job.next_task(True)
    dft_calc.set_parm('ecutwfc', str(e_now))
    dft_calc.run_calculation()
    output_es.append(dft_calc.output['total_energy'])

dft_job.back_to_root()
pickle.dump(output_es,open('ecutoff_conv','wb'))

