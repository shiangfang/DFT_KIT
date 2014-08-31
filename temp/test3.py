import numpy as np
import os

import DFT_job
import DFT_atom
import DFT_element
import DFT_crystal_3D
import DFT_kpoint
import DFT_calculator_VASP

import DFT_crystal_structure
import wire_rhom

os.chdir('../test')

test_job=DFT_job.DFT_job(subdir=False)
test_kgrid=DFT_kpoint.DFT_kpoint()
test_crystal=wire_rhom.Rhom_trigonal_nanowire(DFT_element.Bi_exp,20,20,8,length_unit=1.0)
#print(test_crystal.get_totnum_atoms())

test_calc=DFT_calculator_VASP.DFT_calculator_VASP(False,test_job,test_crystal,test_kgrid,scheme=0,xc='PBE')
test_calc.run_calculation()