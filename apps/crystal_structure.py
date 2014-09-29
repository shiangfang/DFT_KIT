# Density_Function_Theory - KIT  v1.0.0 
# August 2014
# Class for the slab geometry with surface 111 

import numpy as np

from DFT_KIT.core import crystal_3D

class a7_structure(crystal_3D.rhombohedral_3D):
    def __init__(self,element,length_unit=1.0,**parms):
        if 'rhom_length' in parms:
            rhom_length=parms['rhom_length']
            del parms['rhom_length']
        else:
            rhom_length=element.info['rhom_length']
            
        if 'angle' in parms:
            angle=parms['angle']
            del parms['angle']
        else:
            angle=element.info['angle']
        
        if 'rhom_u' in parms:
            rhom_u=parms['rhom_u']
            del parms['rhom_u']
        else:
            rhom_u=element.info['rhom_u']
        
        crystal_3D.rhombohedral_3D.__init__(self,rhom_length,angle,length_unit)
        self.add_atom(element, np.array([0.0,0.0,0.0]), **parms)
        tmp_vec=(self.get_prim_vec(0)+self.get_prim_vec(1)+self.get_prim_vec(2))*2.0*rhom_u
        self.add_atom(element, np.array(tmp_vec), **parms)
    
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
        

class graphene(crystal_3D.hexagonal_3D):
    def __init__(self,element,hex_a_length,hex_c_length,length_unit=1.0,**parms):
        crystal_3D.hexagonal_3D.__init__(self,hex_a_length,hex_c_length,length_unit)
        self.add_atom(element, np.array([0.0,0.0,0.0]),**parms)
        
        self.add_atom(element, np.array([0.0,0.0,0.0]),**parms)
        
        
class layer_material(crystal_3D.crystal_3D):
    def __init__(self,length_unit=1.0):
        crystal_3D.crystal_3D.__init__(self,length_unit)


class diamond(crystal_3D.crystal_3D):
    def __init__(self,length_unit=1.0):
        crystal_3D.crystal_3D.__init__(self,length_unit)

class perovskite(crystal_3D.crystal_3D):
    def __init__(self,length_unit=1.0):
        crystal_3D.crystal_3D.__init__(self,length_unit)

class rocksalt(crystal_3D.crystal_3D):
    def __init__(self,length_unit=1.0):
        crystal_3D.crystal_3D.__init__(self,length_unit)

class body_center(crystal_3D.cubic_3D):
    def __init__(self,cubic_length,length_unit=1.0):
        crystal_3D.crystal_3D.__init__(self,cubic_length,length_unit)

class face_center(crystal_3D.cubic_3D):
    def __init__(self,cubic_length,length_unit=1.0):
        crystal_3D.crystal_3D.__init__(self,cubic_length,length_unit)

        