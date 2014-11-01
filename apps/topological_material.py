# Density_Function_Theory - KIT  v1.0.0 
# August 2014
# Bismuth-Antimony research project 

import numpy as np
import os
import sys

from DFT_KIT.core import job, kpoint, element, crystal_3D
from DFT_KIT.calculator import VASP
from DFT_KIT.apps import crystal_structure

#Bi and Sb
Bi=element.element('Bi',208.9804,83,5,vasp_pot='Bi',qes_pot='Bi_TI.UPF',rhom_length=4.7236,angle=1.0009,rhom_u=0.23407)
Bi_d=element.element('Bi',208.9804,83,15,vasp_pot='Bi_d',qes_pot='Bi_d.UPF')


Sb=element.element('Sb',121.760,51,5,vasp_pot='Sb',qes_pot='Sb_TI.UPF',rhom_length=4.489,angle=0.9989,rhom_u=0.2336)
Sb_d=element.element('Sb',121.760,51,15,vasp_pot='Sb_d',qes_pot='Sb_d.UPF')



#Se
Se=element.element('Se',78.971,34,6,vasp_pot='Se',qes_pot='Se.UPF')
Se_d=element.element('Se',78.971,34,16,vasp_pot='Se_d',qes_pot='Se_d.UPF')



#Te
Te=element.element('Te',127.60,52,6,vasp_pot='Te',qes_pot='Te.UPF')
Te_d=element.element('Te',127.60,52,16,vasp_pot='Te_d',qes_pot='Te_d.UPF')



#Bi2Se3
#J Phys Chem Solids 24, 479 (1963)
Bi2Se3={'rhom_length':9.8405,'angle':0.4242,'a2b3_u':0.4008,'a2b3_v':0.2117}
#


#Bi2Te3
#J Phys Chem Solids 24, 479 (1963)
Bi2Te3={'rhom_length':10.476,'angle':0.4218,'a2b3_u':0.4000,'a2b3_v':0.2095}

Bi2Te3_vasp_crystal_scf={'ISTART':'0','ENCUT':'250','EDIFF':'1E-6','ISMEAR':'-5','SIGMA':'0.2','LMAXMIX':'4'}
Bi2Te3_vasp_crystal_nscf_soi={'ISTART':'0','ICHARG':'11','ENCUT':'250','EDIFF':'1E-6','GGA_COMPAT':'.FALSE.','ISYM':'0','SAXIS':'0 0 1','LSORBIT':'.TRUE.','LMAXMIX':'4','MAGMOM':True}

Bi2Te3_qespresso_crystal_scf={'noncolin':'.true.','lspinorb':'.true.','ecutwfc':'40.0'}
Bi2Te3_qespresso_crystal_bands={'noncolin':'.true.','lspinorb':'.true.','ecutwfc':'40.0'}



#Sb2Te3
#crystal structures vol 2
Sb2Te3={'rhom_length':10.41,'angle':0.4112,'a2b3_u':0.400,'a2b3_v':0.211}

class TI_A2B3(crystal_3D.rhombohedral_3D):
    def __init__(self,element_A,element_B,length_unit=1.0,**parms):
        rhom_length=parms['rhom_length']
        del parms['rhom_length']
        angle=parms['angle']
        del parms['angle']
        a2b3_u=parms['a2b3_u']
        del parms['a2b3_u']
        a2b3_v=parms['a2b3_v']
        del parms['a2b3_v']
        crystal_3D.rhombohedral_3D.__init__(self,rhom_length,angle,length_unit)
        
        vec_tot=self.get_prim_vec(0)+self.get_prim_vec(1)+self.get_prim_vec(2)
        vecz=vec_tot[2]
        self.add_atom(element_B, np.array([0.0,0.0,0.0]), **parms)
        self.add_atom(element_B, np.array([0.0,0.0,a2b3_v*vecz]), **parms)
        self.add_atom(element_B, np.array([0.0,0.0,(1.0-a2b3_v)*vecz]), **parms)
        
        self.add_atom(element_A, np.array([0.0,0.0,a2b3_u*vecz]), **parms)
        self.add_atom(element_A, np.array([0.0,0.0,(1.0-a2b3_u)*vecz]), **parms)
        

class half_heusler(crystal_structure.face_center):
    def __init__(self,element_X,element_Y,element_Z,cubic_length,length_unit=1.0,**parms):
        crystal_structure.face_center.__init__(self, cubic_length, length_unit)
        self.add_atom(element_Z, np.array([0.0,0.0,0.0]), **parms)
        self.add_atom(element_Y, np.array([cubic_length*0.25,cubic_length*0.25,cubic_length*0.25]), **parms)
        self.add_atom(element_X, np.array([cubic_length*0.5,0.0,0.0]), **parms)
    
class trigonal_crystal(crystal_3D.hexagonal_3D):
    def __init__(self,element,hex_a_length,hex_c_length,inner_radius,length_unit=1.0,**parms):
        crystal_3D.hexagonal_3D.__init__(self,hex_a_length,hex_c_length,length_unit)
        self.add_atom(element, np.array([inner_radius,0.0,0.0]), **parms)
        self.add_atom(element, np.array([-0.5*inner_radius,0.5*np.sqrt(3.0)*inner_radius,hex_c_length/3.0]), **parms)
        self.add_atom(element, np.array([-0.5*inner_radius,-0.5*np.sqrt(3.0)*inner_radius,hex_c_length*2.0/3.0]), **parms)
        
        
        
        