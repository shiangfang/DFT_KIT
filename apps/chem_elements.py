# Density_Function_Theory - KIT  v1.0.0 
# August 2014
# Bismuth-Antimony research project 

import numpy as np
import os
import sys

from DFT_KIT.core import job, kpoint, element, crystal_3D
from DFT_KIT.apps import crystal_structure





# crystal setting
#Phys Rev 137, A871
As_exp=element.element('As',74.9216,33,5,vasp_pot='As',qes_pot='As.UPF',rhom_length=4.1299,angle=0.9454,rhom_u=0.226)

#Phys Rev. B 41,11827
As_exp=element.element('As',74.9216,33,5,vasp_pot='As',qes_pot='As.UPF',rhom_length=4.1018,angle=0.9521,rhom_u=0.2276)






