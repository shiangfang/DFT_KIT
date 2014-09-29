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

APE_generalities=['Title','CalculationMode','Units','UnitsOutput','UnitsInput','Verbose']
APE_hamiltonian=['WaveEquation','SpinMode','XCFunctional','XCCorrections']
APE_specie=['NuclearCharge','Orbitals']
APE_pp=['PPCalculationTolerance','PPOutputFileFormat','CoreCorrection','LLocal']
APE_pptest=['PPTests','PPTestSCF','PPTestOrbitals','PPTestAEDir','LogDerivativeRadius','LogDerivativeEnergyMax','LogDerivativeEnergyMin','LogDerivativeEnergyStep']
APE_mesh=['MeshType','MeshStartingPoint','MeshOutmostPoint','MeshNumberOfPoints','MeshDerivMethod','MeshFiniteDiffOrder']
APE_scf=['MaximumIter','ConvAbsDens','ConvRelDens','ConvAbsEnergy','ConvRelEnergy','SmearingFunction','MixingScheme','Mixing','MixNumberSteps']
APE_solver=['EigenSolverTolerance','ODEIntTolerance','ODESteppingFunction','ODEMaxSteps']


class calculator_APE(calculator.calculator):
    def __init__(self,post_process,dft_job,ape_element,scheme=0,**parms):
        calculator.calculator.__init__(self,post_process,dft_job,None,None,**parms)
        self.apply_scheme(scheme)
        if not post_process:
            self.ape_element=ape_element
        else:
            self.ape_element=None
        self.inp_name=''
        
    def generate_files(self):
        if self.inp_name=='':
            inpname=self.ape_element.symbol
        else:
            inpname=self.inp_name
        f_=open(inpname+'.inp','w')
        
        for ind_key in self.parms:
            if ind_key in APE_generalities:
                f_.write(ind_key+' = ' + str(self.parms[ind_key])+'\n')
        f_.write('\n')
        
        for ind_key in self.parms:
            if ind_key in APE_hamiltonian:
                f_.write(ind_key+' = ' + str(self.parms[ind_key])+'\n')
        f_.write('\n')
        
        #for ind_key in self.parms:
        #    if ind_key in APE_specie:
        #        f_.write(ind_key+' = ' + str(self.parms[ind_key])+'\n')
        #f_.write('\n')
        f_.write('NuclearCharge = '+str(self.ape_element.nucZ)+'\n')
        f_.write('%Orbitals\n')
        for tmp in self.parms['Orbitals']:
            f_.write(' ' +tmp+'\n')
        f_.write('%\n\n')
        
        f_.write('%PPComponents\n')
        for tmp in self.parms['PPComponents']:
            f_.write(' ' +tmp+'\n')
        f_.write('%\n\n')
        
        for ind_key in self.parms:
            if ind_key in APE_pp:
                f_.write(ind_key+' = ' + str(self.parms[ind_key])+'\n')
        f_.write('\n')
        
        for ind_key in self.parms:
            if ind_key in APE_pptest:
                f_.write(ind_key+' = ' + str(self.parms[ind_key])+'\n')
        f_.write('\n')
        
        for ind_key in self.parms:
            if ind_key in APE_mesh:
                f_.write(ind_key+' = ' + str(self.parms[ind_key])+'\n')
        f_.write('\n')
        
        for ind_key in self.parms:
            if ind_key in APE_scf:
                f_.write(ind_key+' = ' + str(self.parms[ind_key])+'\n')
        f_.write('\n')
        
        for ind_key in self.parms:
            if ind_key in APE_solver:
                f_.write(ind_key+' = ' + str(self.parms[ind_key])+'\n')
        f_.write('\n')
        
        f_.close()
        
        env_parm.run_ape(self.dft_job.job_mamanger_mode,inpname+'.inp',self.dft_job.opt_parm['cpu'])
        
        
        
    def run_main(self):
        self.dft_job.show('APE', 'APE does not have run main function')
    def apply_scheme(self,scheme):
        self.set_parm('Verbose', '30')
        self.set_parm('CalculationMode', 'ae + pp')
        
        if scheme==0:
            pass
        
        else:
            pass
        
    def post_process(self):
        self.dft_job.show('APE', 'APE does not have post process function')
    
    def post_process_read_ae(self,ae_name,skip_rows=0):
        fname='ae/'+ae_name
        tmp=np.loadtxt(fname,skiprows=skip_rows)
        return tmp
    
    def post_process_read_pp(self,pp_name,skip_rows=0):
        fname='pp/'+pp_name
        tmp=np.loadtxt(fname,skiprows=skip_rows)
        return tmp
        
        
        
        
        
           
        
        