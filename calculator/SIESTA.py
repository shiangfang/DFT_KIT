# Density_Function_Theory - KIT  v1.0.0 
# August 2014
# Class for calculation with VASP

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

SIESTA_flags=['SystemName','SystemLabel','WriteMullikenPop','PAO.BasisType ','PAO.EnergyShift',
'PAO.BasisSize','SpinPolarized','MeshCutoff','MaxSCFIterations','DM.MixingWeight','DM.Tolerance',
'DM.NumberPulay','DM.UseSaveDM ','NeglNonOverlapInt','SolutionMethod','ElectronicTemperature',
'MD.TypeOfRun','MD.NumCGsteps','MD.MaxCGDispl','MD.MaxForceTol']



class calculator_SIESTA(calculator.calculator):
    def __init__(self,postprocess,dft_job,crystal,kgrid,scheme=0,**parms):
        calculator.calculator.__init__(self,postprocess,dft_job,crystal,kgrid,**parms)
        
    def apply_scheme(self,scheme):
        if scheme == 0:

                          'WriteMullikenPop' : [True,'1'],
                          'PAO.BasisType ' : [True,'split'],
                          'PAO.EnergyShift' : [False,''],
                          'PAO.BasisSize' : [True,'DZP'],
                          'SpinPolarized' : [True,'F'],
                          'MeshCutoff' : [False,''],
                          'MaxSCFIterations' : [True,'100'],
                          'DM.MixingWeight' : [True,'0.1'],
                          'DM.Tolerance' : [True,'1.d-4'],
                          'DM.NumberPulay' : [False,''],
                          'DM.UseSaveDM ' : [False,''],
                          'NeglNonOverlapInt' : [True,'false'],
                          'SolutionMethod' : [False,''],
                          'ElectronicTemperature' : [False,''],
                          'MD.TypeOfRun' : [True,'cg'],
                          'MD.NumCGsteps' : [True,'100'],
                          'MD.MaxCGDispl' : [False,''],
                          'MD.MaxForceTol' : [True,'0.04 eV/Ang'],
                          }
        
        else:
            pass
       
    def generate_files(self):
        self.dft_job.show('CALC_SIESTA','generate input files for calculation')
        file_input_fdf=open(self.output_dir+'siesta_input.fdf','w')
        self.write_input_fdf(file_input_fdf)
        file_input_fdf.close()
        f_=open('siesta.in','w')

        for key in self.siesta_parm:
            value=self.siesta_parm[key]
            if value[0]:
                f_.write(key+' = '+value[1]+ '\n')
              
        f_.write('NumberOfSpecies = '+ str(len(self.crystal.basis_atom_groups)) + '\n')
        f_.write('NumberOfAtoms = '+ str(len(self.crystal.get_totnum_atoms())) + '\n')  
        
        #2nd, write atomic coordinate
        f_.write('\n')
        f_.write('%block  Chemical_Species_label \n')
        for ind, group in enumerate(self.crystal.basis_atom_groups.keys()):
            f_.write('   '+str(ind)+ ' ' + self.crystal.basis_element[group].nucZ  +' ' + group +'\n')
        f_.write('%endblock Chemical_Species_label  \n')
        
        f_.write('\n')
        f_.write('AtomicCoordinatesFormat  ScaledCartesian \n')
        f_.write('%block AtomicCoordinatesAndAtomicSpecies\n')
        for ind, group in enumerate(self.crystal.basis_atom_groups.keys()):
            for atom in self.crystal.basis_atom_groups[group]:
                f_.write(general_tool.vec_to_str(atom.get_position()) + ' ' +str(ind)+'\n')
        f_.write('%endblock  AtomicCoordinatesAndAtomicSpecies\n')
        f_.write('\n')
        
        #lattice, use crystal information
        f_.write('LatticeConstant ' + str(self.crystal.get_length_unit()) +' Ang\n')
        f_.write('%block LatticeVectors\n')
        f_.write(general_tool.vec_to_str(self.crystal.get_prim_vec(0)) +'\n')
        f_.write(general_tool.vec_to_str(self.crystal.get_prim_vec(1)) +'\n')
        f_.write(general_tool.vec_to_str(self.crystal.get_prim_vec(2)) +'\n')
        f_.write('%endblock LatticeVectors\n')
        
        f_.write('\n')
        #kgrid sampling
        if self.kgrid.kmode==0:
            f_.write('%block kgrid_Monkhorst_Pack\n')
            f_.write(' ' + str(self.kpoint_grid[0]) + ' 0 0 0.0\n')
            f_.write(' 0 ' + str(self.kpoint_grid[1]) + ' 0 0.0\n')
            f_.write(' 0 0 ' + str(self.kpoint_grid[2]) + ' 0.0\n')
            f_.write('%endblock kgrid_Monkhorst_Pack\n')
        
        #k linear mode
        if len(self.kpoint_linear_kmode)>0:
            f_.write('BandLineScale pi/a\n')
            f_.write('%block BandLines\n')
            for ind in range(len(self.kpoint_linear_kmode)):
                f_.write(str(ind)+' '+general_tool.vec_to_str(self.kpoint_linear_kmode[ind])+'\n')
            f_.write('%endblock BandLines\n')

    def post_process(self):
        pass
    
    

