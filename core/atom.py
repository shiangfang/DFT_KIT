# Density_Function_Theory - KIT  v1.0.0 
# August 2014
# Class for the object atom to construct the lattice and basis atoms

import numpy as np
import math
import sys
import copy

class atom:
    def __init__(self,element,position=np.array([0.0,0.0,0.0]),**parms):
        self.element=copy.copy(element)
        self.position=position
        self.magmom=np.array([0,0,0])
        self.velocity=np.array([0.0,0.0,0.0])
        self.position_update=[False,False,False]
        self.parms={}
        
        for ind_parm in parms:
            self.parms[ind_parm]=parms[ind_parm]
    def set_magmom(self,magmom):
        self.magmom=np.array(magmom)
    def get_magmom(self):
        return self.magmom    
    def set_position(self,pos_):
        self.position=pos_
    def get_position(self):
        return self.position
    def set_parms(self,**parms):
        for ind_parm in parms:
            self.parms[ind_parm]=parms[ind_parm]
    def get_parms(self,ind_parm):
        return self.parms[ind_parm]
    def remove_parm(self,ind_parm):
        pass
    
    
    