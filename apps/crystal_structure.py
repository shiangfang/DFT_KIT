# Density_Function_Theory - KIT  v1.0.0 
# August 2014
# Class for the slab geometry with surface 111 

import numpy as np

from DFT_KIT.core import crystal_3D


class graphene_BN(crystal_3D.hexagonal_3D):
    def __init__(self,element_1,element_2,hex_a_length,hex_c_length,length_unit=1.0,**parms):
        crystal_3D.hexagonal_3D.__init__(self,hex_a_length,hex_c_length,length_unit)
        self.add_atom(element_1, np.array([0.0,0.0,0.0]),**parms)
        self.add_atom(element_2, np.array([hex_a_length*0.5,hex_a_length*0.5/np.sqrt(3.0),0.0]),**parms)


class graphene(crystal_3D.hexagonal_3D):
    def __init__(self,element,hex_a_length,hex_c_length,length_unit=1.0,**parms):
        crystal_3D.hexagonal_3D.__init__(self,hex_a_length,hex_c_length,length_unit)
        self.add_atom(element, np.array([0.0,0.0,0.0]),**parms)
        self.add_atom(element, np.array([hex_a_length*0.5,hex_a_length*0.5/np.sqrt(3.0),0.0]),**parms)
        
class CsCl(crystal_3D.cubic_3D):
    def __init__(self,element_1,element_2,cubic_length,length_unit=1.0,**parms):
        crystal_3D.cubic_3D.__init__(self,cubic_length,length_unit)
        self.add_atom(element_1, np.array([0.0,0.0,0.0]),**parms)
        self.add_atom(element_2, np.array([0.5*cubic_length,0.5*cubic_length,0.5*cubic_length]),**parms)

class Zinc_blende(crystal_3D.fcc_3D):
    def __init__(self,element_1,element_2,cubic_length,length_unit=1.0,**parms):
        crystal_3D.fcc_3D.__init__(self,cubic_length,length_unit)
        self.add_atom(element_1, np.array([0.0,0.0,0.0]),**parms)
        self.add_atom(element_2, np.array([0.25*cubic_length,0.25*cubic_length,0.25*cubic_length]),**parms)


class diamond(crystal_3D.fcc_3D):
    def __init__(self,element,cubic_length,length_unit=1.0,**parms):
        crystal_3D.fcc_3D.__init__(self,cubic_length,length_unit)
        self.add_atom(element, np.array([0.0,0.0,0.0]),**parms)
        self.add_atom(element, np.array([0.25*cubic_length,0.25*cubic_length,0.25*cubic_length]),**parms)

#ABX_3 material
class perovskite(crystal_3D.cubic_3D):
    def __init__(self,element_A,element_B,element_X,cubic_length,length_unit=1.0,**parms):
        crystal_3D.cubic_3D.__init__(self,cubic_length,length_unit)
        self.add_atom(element_A, np.array([0.0,0.0,0.0]),**parms)
        self.add_atom(element_B, np.array([0.5*cubic_length,0.5*cubic_length,0.5*cubic_length]),**parms)
        self.add_atom(element_X, np.array([0.0,0.5*cubic_length,0.5*cubic_length]),**parms)
        self.add_atom(element_X, np.array([0.5*cubic_length,0.0,0.5*cubic_length]),**parms)
        self.add_atom(element_X, np.array([0.5*cubic_length,0.5*cubic_length,0.0]),**parms)


class rocksalt(crystal_3D.fcc_3D):
    def __init__(self,element_1,element_2,cubic_length,length_unit=1.0,**parms):
        crystal_3D.fcc_3D.__init__(self,cubic_length,length_unit)
        self.add_atom(element_1, np.array([0.0,0.0,0.0]),**parms)
        self.add_atom(element_2, np.array([0.5*cubic_length,0.0,0.0]),**parms)


class body_center_cubic(crystal_3D.cubic_3D):
    def __init__(self,element,cubic_length,length_unit=1.0,**parms):
        crystal_3D.cubic_3D.__init__(self,cubic_length,length_unit)
        self.add_atom(element, np.array([0.0,0.0,0.0]),**parms)
        self.add_atom(element, np.array([0.5*cubic_length,0.5*cubic_length,0.5*cubic_length]),**parms)

class face_center_cubic(crystal_3D.cubic_3D):
    def __init__(self,element,cubic_length,length_unit=1.0,**parms):
        crystal_3D.cubic_3D.__init__(self,cubic_length,length_unit)
        self.add_atom(element, np.array([0.0,0.0,0.0]),**parms)
        self.add_atom(element, np.array([0.0,0.5*cubic_length,0.5*cubic_length]),**parms)
        self.add_atom(element, np.array([0.5*cubic_length,0.0,0.5*cubic_length]),**parms)
        self.add_atom(element, np.array([0.5*cubic_length,0.5*cubic_length,0.0]),**parms)




        