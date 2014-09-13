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

[input_parm,opt_parm]=interface_script.init_simulation(0)

test_job=job.job(subdir=True)


#os.chdir('../temp/test')

# first round, vc-relaxation
test_kgrid=kpoint.kpoint()
test_job.sys_info['qes_fname']='bi.scf'
test_crystal=crystal_structure.a7_structure(bismuth_antimony.Bi_exp,length_unit=1.0)
test_calc=QESPRESSO.calculator_QESPRESSO(False,test_job,test_crystal,test_kgrid,scheme=0)
test_calc.load_parm(False, bismuth_antimony.Bi_qespresso_crystal_scf)
test_calc.run_calculation()

test_calc.update_crystal()
# second round, non-self-consistent calculation
test_job.next_task(True)
test_job.sys_info['qes_fname']='bi.nscf'
test_calc.set_parm('calculation', "'nscf'")
#change parameters here
test_kgrid.set_scan_mode(50, [test_crystal.k_labels['L'],test_crystal.k_labels['Gamma'],test_crystal.k_labels['Gamma'],test_crystal.k_labels['T']])
#test_calc.load_parm(True, bismuth_antimony.Bi_qespresso_crystal_nscf_soi)
test_calc.run_calculation()

