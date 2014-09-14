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

test_kgrid=kpoint.kpoint()
test_crystal=crystal_structure.a7_structure(bismuth_antimony.Bi_exp,length_unit=1.0)
test_crystal.get_atom('Bi', 0).set_relax_all(False)
test_crystal.get_atom('Bi', 1).set_relax_all(True)

test_job=job.job(subdir=True)
test_job.sys_info['qes_fname']='bi.relax'
test_job.sys_info['qes_prefix']='bismuth'

# first round, vc-relaxation
test_calc=QESPRESSO.calculator_QESPRESSO(False,test_job,test_crystal,test_kgrid,scheme=0)
test_calc.apply_scheme(4)
test_calc.load_parm(False, bismuth_antimony.Bi_qespresso_crystal_scf)
test_calc.run_calculation()

test_calc.update_crystal()
# second round, self-consistent calculation
test_job.next_task(True)
test_job.sys_info['qes_fname']='bi.scf'
test_calc.apply_scheme(0)
test_calc.run_calculation()

# third round, self-consistent calculation
test_job.next_task(False)
test_job.sys_info['qes_fname']='bi.bands'
test_calc.apply_scheme(2)
#change parameters here
test_kgrid.set_scan_mode(50, [test_crystal.k_labels['L'],test_crystal.k_labels['Gamma'],test_crystal.k_labels['Gamma'],test_crystal.k_labels['T']])
test_calc.run_calculation()

