# Density_Function_Theory - KIT  v1.0.0 
# August 2014
# Class for calculation with VASP

import numpy as np
import os
import shutil
import pickle
import string
import numpy as np
import sys
import string
import xml.etree.ElementTree as ET

from DFT_KIT.core import general_tool
from DFT_KIT.core import env_parm
from DFT_KIT.core import calculator
from DFT_KIT.interface import interface

ABINIT_incar_flags=[]

class calculator_ABINIT(calculator.calculator):
    def __init__(self,postprocess,dft_job,crystal,kgrid,scheme=0,**parms):
        calculator.calculator.__init__(self,postprocess,dft_job,crystal,kgrid,**parms)
        self.apply_scheme(scheme)
        #central control variables
        
    def apply_scheme(self,scheme):
        pass
    
    def generate_files(self):
        pass
    
    
        