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
from DFT_KIT.apps import bismuth_antimony, slab_surface_rhom

[input_parm,opt_parm]=interface_script.init_simulation(0)

test_job=job.job(subdir=False)


#os.chdir('../temp/test')

# first round, self-consistent calculation
test_kgrid=kpoint.kpoint()
test_job.sys_info['qes_fname']='bi.scf'
test_crystal=slab_surface_rhom.Rhom_trigonal_surface(bismuth_antimony.Bi_exp,3,2,length_unit=1.0)
test_calc=QESPRESSO.calculator_QESPRESSO(False,test_job,test_crystal,test_kgrid,scheme=0)
test_calc.load_parm(False, bismuth_antimony.Bi_qespresso_crystal_scf)
test_calc.run_calculation()


# second round, non-self-consistent calculation
test_job.next_task(False)
test_job.sys_info['qes_fname']='bi.nscf'
test_calc.set_parm('calculation', "'nscf'")
#change parameters here
test_kgrid.set_scan_mode(50,[np.array([0.0,0.0,0.0]),np.array([1.0,0.0,0.0])])
#test_calc.load_parm(True, bismuth_antimony.Bi_qespresso_crystal_nscf_soi)
test_calc.run_calculation()

