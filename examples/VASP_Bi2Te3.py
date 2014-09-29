# Density_Function_Theory - KIT  v1.0.0 
# August 2014
# Implementation for how to construct calculation for doing VASP calculation with DFT_KIT

import numpy as np
import os
import sys

from DFT_KIT.core import job, kpoint, element, crystal_3D
from DFT_KIT.calculator import VASP, QESPRESSO, Wannier90
from DFT_KIT.apps import crystal_structure,  TI_3d
from DFT_KIT.interface import interface_script

[input_parm,opt_parm]=interface_script.init_simulation(0)

dft_job=job.job(subdir=True)

# first round, self-consistent calculation
dft_kgrid=kpoint.kpoint()
dft_crystal=crystal_structure.TI_A2B3(TI_3d.Bi,TI_3d.Te,length_unit=1.0,**TI_3d.Bi2Te3)
dft_calc=QESPRESSO.calculator_QESPRESSO(False,dft_job,dft_crystal,dft_kgrid,scheme=0)
dft_calc.load_parm(False, TI_3d.Bi2Te3_qes_crystal_scf)
dft_calc.run_calculation()


# second round, non-self-consistent calculation
dft_job.next_task(True)
#change parameters here
dft_calc.set_run_vasp_mode(1)
dft_job.copy_from_task(0, 'CHGCAR')
dft_kgrid.set_scan_mode(50, [dft_crystal.k_labels['L'],dft_crystal.k_labels['Gamma'],dft_crystal.k_labels['Gamma'],dft_crystal.k_labels['T']])
dft_calc.load_parm(True, TI_3d.Bi2Te3_vasp_crystal_nscf_soi)
dft_calc.run_calculation()





