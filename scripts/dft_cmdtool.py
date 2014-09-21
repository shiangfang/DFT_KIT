# Density_Function_Theory - KIT  v1.0.0 
# August 2014
# Class for the Command tool collection

import numpy as np
import pickle
import sys
import os

from DFT_KIT.core import job, kpoint, element, crystal_3D
from DFT_KIT.calculator import VASP, QESPRESSO, Wannier90
from DFT_KIT.apps import crystal_structure

dft_job=job.job(False)

print('Density Functional Theory - KIT command tool collection')
root_dir=os.getcwd()+'/'
print('Current working directory: '+root_dir)

numargs=len(sys.argv)
if numargs>1:
    #for specific usage
    dft_job.show('dft_cmdtool','Script mode!')
    scriptfile=sys.argv[1]
    dft_job.load_script(scriptfile)
    
while True:
    input_cmd = dft_job.get_info('dft_cmdtool','input command',True)
    #main basic functions, directories,...
    cmd_first=input_cmd.split()[0]
    cmd_num=len(input_cmd.split())
    cmds=input_cmd.split()
    root_dir=os.getcwd()+'/'
        
    #basic functions of 
    if (cmd_first == 'quit' or cmd_first == 'exit'):
        dft_job.show('dft_cmdtool','Exit!')
        break
    dft_job.show('dft_cmdtool', cmd_first)
