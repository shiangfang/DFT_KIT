# Density_Function_Theory - KIT  v1.0.0 
# August 2014
# Class for the Calculator (general form)
# The class will implement how to generate the input files for calculation 
# And a separate part for how to analyze the output simulation results
# The last part will be the output of data into various forms

import os

from DFT_KIT.core import job

class calculator:
    def __init__(self,postprocess,dft_job,crystal,kgrid,**parms):
        self.output_dir=''
        self.crystal=crystal
        self.kgrid=kgrid
        self.parms={}
        self.postprocess=postprocess
        if postprocess and dft_job is None:
            dft_job=job.job(subdir=False)
        self.dft_job=dft_job
        
        for ind_key in parms:
            self.parms[ind_key]=parms[ind_key]
            
        self.pre_commands=[]
        self.post_commands=[]
        self.output={}
        self.reset_simulation_data()
              
    def run_calculation(self):
        if self.postprocess:
            self.dft_job.show_error('DFT_CALC','cannot run calculation in post process mode')
            return 0
        #generate necessary files
        self.generate_files()
        
        #run program including the commands
        for cmd in self.pre_commands:
            os.system(cmd)
        self.run_main()
        for cmd in self.post_commands:
            os.system(cmd)
    
    
    def get_maindir(self):
        return self.dft_job.get_maindir()
        
    def set_output_dir(self,dir_):
        self.output_dir=dir_
    def get_output_dir(self):
        return self.output_dir
    def set_parm(self,ind_key,parm_val):
        self.parms[ind_key]=parm_val
    def get_parm(self,ind_key):
        return self.parms[ind_key]
    def load_parm(self,cleanup,new_parm):
        #new parm is a dictionary just like parms
        if cleanup:
            self.parms={}
        for ind_key in new_parm:
            self.parms[ind_key]=new_parm[ind_key]
    
    def remove_parm(self,ind_key):
        if ind_key in self.parms:
            del self.parms[ind_key]
    def get_crystal(self):
        return self.crystal
    def set_crystal(self,crystal):
        self.crystal=crystal
    
    def set_postprocess(self,pp):
        self.postprocess=pp
    def clean(self):
        pass
    
    def reset_simulation_data(self):
        self.output={}
        
        #DFT calculation and computation resource:
        self.output['dft_xc']=''
        self.output['cputime']=0.0
        
        #Crystal and Atoms:
        self.output['new_volume']=[]
        self.output['new_prim_vectors']=[]
        self.output['new_positions']=[]
        self.output['new_velocities']=[]
        
        #Energy:
        self.output['total_energy']=0.0
        self.output['fermi_energy']=0.0
        self.output['entropy']=0.0
        self.output['den_of_state']=[]
        
        #Bands:
        self.output['kpoints']=[]
        self.output['num_bands']=0
        self.output['bands_energy']=[]
        self.output['bands_occupation']=[]

        #Force:
        self.output['force']=[]
        self.output['stress']=[]
        
  
        
        


