# Density_Function_Theory - KIT  v1.0.0 
# August 2014

import numpy as np
import os
import sys

from DFT_KIT.core import job, kpoint, element, crystal_3D
from DFT_KIT.calculator import VASP
from DFT_KIT.apps import crystal_structure

#single layer structure


class TMDC_monolayer(crystal_3D.hexagonal_3D):
    def __init__(self,element1,element2,hex_a_length,hex_c_length,atom_separation,length_unit=1.0,**parms):
        crystal_3D.hexagonal_3D.__init__(self,hex_a_length,hex_c_length,length_unit)
 
        self.add_atom(element1, np.array([0.0,0.0,hex_c_length]),**parms)
        
        self.add_atom(element2, np.array([0.5*hex_a_length,hex_a_length*0.5/np.sqrt(3.0),hex_c_length+0.5*atom_separation]),**parms)
        self.add_atom(element2, np.array([0.5*hex_a_length,hex_a_length*0.5/np.sqrt(3.0),hex_c_length-0.5*atom_separation]),**parms)
        
# stacks of TMDC






