import numpy as np
import os

import DFT_job
import DFT_atom
import DFT_element
import DFT_crystal_3D
import DFT_kpoint
import DFT_calculator_QESPRESSO

#os.chdir('gen_period_table')

test_job=DFT_job.DFT_job(subdir=False)
test_kgrid=DFT_kpoint.DFT_kpoint()
test_crystal=DFT_crystal_3D.cubic_3D(2.56)
test_atom1=test_crystal.add_atom(DFT_element.Bi_exp, position=np.array([0.0,0.0,0.0]))
test_atom2=test_crystal.add_atom(DFT_element.Bi_exp, position=np.array([1.0,1.0,1.0]))
test_atom3=test_crystal.add_atom(DFT_element.Sb, position=np.array([1.0,2.0,1.0]))

test_calc=DFT_calculator_QESPRESSO.DFT_calculator_QESPRESSO(False,test_job,test_crystal,test_kgrid,scheme=0)
test_calc.run_calculation()
print(os.getcwd())




