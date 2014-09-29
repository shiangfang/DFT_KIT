# Density_Function_Theory - KIT  v1.0.0 
# August 2014
# Implementation for how to construct calculation for doing VASP calculation with DFT_KIT

import numpy as np
import os
import sys

from DFT_KIT.core import job, kpoint, element, crystal_3D
from DFT_KIT.calculator import APE
from DFT_KIT.apps import crystal_structure
from DFT_KIT.interface import interface_script
from DFT_KIT.apps import bismuth_antimony


[input_parm,opt_parm]=interface_script.init_simulation(0)

dft_job=job.job(subdir=False,job_manager_mode=False,write_post_process=False)
dft_calc=APE.calculator_APE(dft_job,bismuth_antimony.Bi_exp)
dft_calc.load_parm(False,bismuth_antimony.Bi_ape)
dft_calc.generate_files()


