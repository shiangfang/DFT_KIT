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
e_min=20.0
e_max=50.0
e_num=31
all_es=np.linspace(e_min,e_max,e_num)
e_now=all_es[scan_index]

dft_job=job.job(subdir=False)
dft_job.process_opt_parm(opt_parm)

# first round, self-consistent calculation
dft_kgrid=kpoint.kpoint()
dft_job.sys_info['qes_fname']='bis'
dft_crystal=crystal_structure.a7_structure(bismuth_antimony.Bi_exp,length_unit=1.0)
dft_calc=QESPRESSO.calculator_QESPRESSO(False,dft_job,dft_crystal,dft_kgrid,scheme=0)
dft_calc.load_parm(False, bismuth_antimony.Bi_qespresso_crystal_scf)
dft_calc.set_parm('ecutwfc', float(e_now))
dft_calc.run_calculation()


