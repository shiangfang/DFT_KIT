# Density_Function_Theory - KIT  v1.0.0 
# August 2014
# Implementation for how to construct calculation for doing VASP calculation with DFT_KIT

import numpy as np
import os
import sys

from DFT_KIT.core import job, kpoint, element, crystal_3D
from DFT_KIT.calculator import VASP, QESPRESSO, Wannier90
from DFT_KIT.apps import crystal_structure, bismuth_antimony
from DFT_KIT.interface import interface_script

input_parm=interface_script.init_simulation(0)

test_job=job.job(subdir=True)

# first round, self-consistent calculation
test_kgrid=kpoint.kpoint()
test_crystal=crystal_structure.a7_structure(bismuth_antimony.Bi_exp,length_unit=1.0)
test_calc=VASP.calculator_VASP(False,test_job,test_crystal,test_kgrid,scheme=0)
test_calc.load_parm(False, bismuth_antimony.Bi_vasp_crystal_scf)
test_calc.run_calculation()


# second round, non-self-consistent calculation
test_job.next_task(True)
#change parameters here
test_calc.set_run_vasp_mode(1)
test_job.copy_from_task(0, 'CHGCAR')
test_kgrid.set_scan_mode(50, [test_crystal.k_labels['L'],test_crystal.k_labels['Gamma'],test_crystal.k_labels['Gamma'],test_crystal.k_labels['T']])
test_calc.load_parm(True, bismuth_antimony.Bi_vasp_crystal_nscf_soi)
test_calc.run_calculation()





