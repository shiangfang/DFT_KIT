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

dft_job=job.job(subdir=False)


#os.chdir('../temp/test')

# first round, self-consistent calculation
dft_kgrid=kpoint.kpoint()
dft_job.sys_info['qes_fname']='sb.scf'
dft_job.sys_info['qes_prefix']='sb_prefix'
dft_crystal=crystal_structure.a7_structure(bismuth_antimony.Sb_exp,length_unit=1.0)
dft_wan90=Wannier90.calculator_Wannier90(True,dft_job,dft_crystal,dft_kgrid)
dft_calc=QESPRESSO.calculator_QESPRESSO(False,dft_job,dft_crystal,dft_kgrid,scheme=0)
dft_calc.load_parm(False, bismuth_antimony.Sb_qespresso_crystal_scf)
dft_calc.run_calculation()


dft_kgrid.set_klist_grid([7,7,7])
dft_calc.load_parm(False, bismuth_antimony.Sb_pw2wan)
dft_wan90.load_parm(False, bismuth_antimony.Sb_wannier90)
dft_wan90.add_projections(['random','Sb: l=0;l=1'])

# second round, non-self-consistent calculation for k-grid
dft_job.next_task(False)
dft_job.sys_info['qes_fname']='sb.nscf'
dft_calc.set_parm('calculation', "'nscf'")
dft_calc.set_parm('nbnd', "20")
dft_wan90.set_parm('num_bands','20')

dft_calc.run_calculation()

# third round: wannier90
dft_wan90.run_wannier(True,True)

# fourth round: pw2wannier
dft_calc.run_pw2wan()

# fifth round: wannier90 as post-process
dft_wan90.run_wannier(False,False)




