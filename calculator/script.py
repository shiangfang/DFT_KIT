# Density_Function_Theory - KIT  v1.0.0 
# August 2014
# Class for calculation with VASP using python script or calling external program like Matlab

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


VASP_incar_flags=['NGX','NGY','NGZ','NGXF','NGYF' ,'NGZF' ,'NBANDS','NBLK','NWRITE', 
'ISTART' ,'ICHARG','ISPIN' ,'MAGMOM','INIWAV','ENCUT' ,'PREC','NELM', 
'NELMIN' ,'NELMDL','EDIFF','EDIFFG','NSW','NBLOCK','KBLOCK','IBRION', 
'ISIF','IWAVPR','ISYM','SYMPREC' ,'LCORR','POTIM','TEBEG','TEEND', 
'SMASS','NPACO','APACO','POMASS','ZVAL','RWIGS','NELECT','NUPDOWN', 
'EMIN','EMAX','ISMEAR','SIGMA','ALGO','IALGO','LREAL','ROPT','GGA','VOSKOWN','DIPOL', 
'AMIX','BMIX','WEIMIN','EBREAK','DEPER','TIME','LWAVE','LCHARG' ,'LVTOT','LVHAR', 
'LELF','LORBIT','NPAR','LSCALAPACK','LSCALU','LASYNC']

VASP_kpoints_flags=[]

class calculator_script(calculator.calculator):
    def __init__(self,postprocess,dft_job,crystal,kgrid,**parms):
        calculator.calculator.__init__(self,postprocess,dft_job,crystal,kgrid,**parms)
        #central control variables
        pass
        
    def run_main(self):
        #this is the place to process the script for calculation
        pass
    
    def generate_files(self):
        pass

#Post Process tools for VASP
    def post_process(self):
        pass

    





