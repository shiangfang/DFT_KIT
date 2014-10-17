# Density_Function_Theory - KIT  v1.0.0 
# August 2014
# Class for the object atom to construct the lattice and basis atoms

import os
import shutil
import pickle
import string
import numpy as np
import sys
import string
import xml.etree.ElementTree as ET
import os.path

from DFT_KIT.core import general_tool
from DFT_KIT.core import env_parm
from DFT_KIT.core import calculator
from DFT_KIT.core import physics

ELK_flags=['','']

class calculator_ELK(calculator.calculator):
    def __init__(self,postprocess,dft_job,crystal,kgrid,scheme=0,**parms):
        calculator.calculator.__init__(self,postprocess,dft_job,crystal,kgrid,**parms)
        self.apply_scheme(scheme)
        self.wannier90_analysis=False
        self.write_occupations=False
        self.write_constraints=False
        self.write_atomic_forces=False
        self.atomic_positions_ang=True
        self.parms['claculation']=''
        self.qes_vars={}
        
        
    def generate_files(self):
        f_=open('elk.in','w')
        f_.write('  ! ELK All-electron DFT calculation with DFT_KIT \n')
        
        f_.write('\n\ntasks\n')
        
        for tmpparm in self.parms:
            if tmpparm in ELK_flags:
                f_.write(tmpparm+'\n')
                for tmpval in self.parms[tmpparm]:
                    f_.write(' '+tmpval+'\n')
                f_.write('\n')
        
        f_.write('avec\n')
        f_.write(' '+general_tool.vec_to_str(self.crystal.get_prim_vec(0)/physics.bohr) +'\n')
        f_.write(' '+general_tool.vec_to_str(self.crystal.get_prim_vec(1)/physics.bohr) +'\n')
        f_.write(' '+general_tool.vec_to_str(self.crystal.get_prim_vec(2)/physics.bohr) +'\n')
        f_.write('\n') 
        
        f_.write('sppath\n')
        if 'sppath' in self.parms:
            f_.write(' '+self.parms['sppath'])
        else:
            f_.write(' '+env_parm.elk_sppath)
        f_.write('\n')
        
        f_.write('atoms\n')
        f_.write(' '+str(len(self.crystal.basis_atom_groups.keys()))+'\n')
        for group in self.crystal.basis_atom_groups.keys():
            element=self.crystal.basis_element[group]
            if 'elk_in' in element.info:
                f_.write(' '+element.info['elk_in']+'\n')
            else:
                f_.write(' '+group+'.in\n')
            f_.write(str(len(self.crystal.basis_atom_groups[group]))+'\n')    
            for atom in self.crystal.basis_atom_groups[group]:
                f_.write(' '+general_tool.vec_to_str(atom.get_position()/physics.bohr) + ' 0.00 0.00 0.00\n')
        
        f_.write('plot1d\n')
        f_.write(' '+str(len(self.kgrid.kscan))+' '+str(self.kgrid.num_kscan)+'\n')
        for ind in range(len(self.kgrid.kscan)):
            f_.write(' '+general_tool.vec_to_str(self.kgrid.kscan[ind])+ '\n')
                 
        
        
        f_.close()


    def read_files(self,fname):
        pass



