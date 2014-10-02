# Density_Function_Theory - KIT  v1.0.0 
# August 2014
# Implementation for how to construct calculation for doing VASP calculation with DFT_KIT

import numpy as np
import os
import sys

from DFT_KIT.core import job, kpoint, element, crystal_3D
from DFT_KIT.calculator import QESPRESSO, Wannier90
from DFT_KIT.apps import crystal_structure
from DFT_KIT.interface import interface_script
from DFT_KIT.apps import bismuth_antimony

[input_parm,opt_parm]=interface_script.init_simulation(0)

test_job=job.job(subdir=False)


#os.chdir('../temp/test')

# first round, self-consistent calculation
test_kgrid=kpoint.kpoint()
test_job.sys_info['qes_fname']='bi.scf'
test_job.sys_info['qes_prefix']='bi_prefix'
test_crystal=crystal_structure.a7_structure(bismuth_antimony.Bi_exp,length_unit=1.0)
test_wan90=Wannier90.calculator_Wannier90(True,test_job,test_crystal,test_kgrid)
test_calc=QESPRESSO.calculator_QESPRESSO(False,test_job,test_crystal,test_kgrid,scheme=0)
test_calc.load_parm(False, bismuth_antimony.Bi_qespresso_crystal_scf)
test_calc.run_calculation()


test_kgrid.set_klist_grid([3,3,3])
test_calc.load_parm(False, bismuth_antimony.Bi_pw2wan)
test_wan90.load_parm(False, bismuth_antimony.Bi_wannier90)
test_wan90.add_projections(['random','Bi: l=0;l=1'])

# second round, non-self-consistent calculation for k-grid
test_job.next_task(False)
test_job.sys_info['qes_fname']='bi.nscf'
test_calc.set_parm('calculation', "'nscf'")
test_calc.set_parm('nbnd', "20")
test_wan90.set_parm('num_bands','20')

test_calc.run_calculation()

# third round: wannier90
test_wan90.run_wannier(True,True)

# fourth round: pw2wannier
test_calc.run_pw2wan()

# fifth round: wannier90 as post-process
test_wan90.run_wannier(False,False)




