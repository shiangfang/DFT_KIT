# Density_Function_Theory - KIT  v1.0.0 
# August 2014
# Class for the Calculator (general form)
# The class will implement how to generate the input files for calculation 
# And a separate part for how to analyze the output simulation results
# The last part will be the output of data into various forms

import os

from DFT_KIT.core import job
from DFT_KIT.interface import interface

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
        
        self.run_post_process=True
        self.save_output_data={}
        
    def dump_save_output(self):
        self.dft_job.record_save_output(self.save_output_data)
        
    def save_output(self,parms_list):
        # parm_list in the form: ['aa':'new name',bb:...,cc:...]
        for parm in parms_list:
            if parm in self.output:
                self.save_output_data[parms_list[parm]]=self.output[parm]
            

    def set_run_post_process(self,post_process):
        self.run_post_process=post_process
        
    def run_calculation(self,save_post_process=True):
        if self.postprocess:
            self.dft_job.show_error('DFT_CALC','cannot run calculation in post process mode')
            return 0
        #generate necessary files
        self.generate_files()
        self.save_output_data={}
        
        #run program including the commands
        for cmd in self.pre_commands:
            os.system(cmd)
        self.run_main()
        for cmd in self.post_commands:
            os.system(cmd)
            
        if self.run_post_process:
            self.post_process()
            if save_post_process:
                pp_fname=self.dft_job.make_fname_sysinfo('dft_post_process')
                interface.pickle_save(self.dft_job.post_process_dir+pp_fname, [self])
    
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
        self.output['num_atoms']=0
        self.output['num_types']=0
        self.output['init_volume']=[]
        self.output['init_prim_vectors']=[]
        self.output['init_positions']=[]
        self.output['init_velocities']=[]
        self.output['final_volume']=[]
        # format [[vec_0],[vec_1],[vec_2],...]
        self.output['final_prim_vectors']=[]
        self.output['final_positions']=[]
        self.output['final_velocities']=[]
        self.output['num_electrons']=0
        
        #Energy:
        self.output['total_energy']=0.0
        self.output['free_energy']=0.0
        self.output['fermi_energy']=0.0
        self.output['entropy']=0.0
        self.output['energy_cutoff']=0.0
        self.output['den_of_state']=[]
        
        #Bands:
        self.output['kpoints']=[]
        self.output['num_bands']=0
        self.output['bands_energy']=[]
        self.output['bands_occupation']=[]

        #Force:
        self.output['force']=[]
        self.output['stress']=[]
        
    def update_prim_cell(self):
        if len(self.output['final_prim_vectors']) !=3:
            self.dft_job.show_error('CALC', 'update prim cell error1')
            return
        
        for ind, vec in enumerate(self.output['final_prim_vectors']):
            if len(vec) !=3:
                self.dft_job.show_error('CALC', 'update prim cell error 2')
                return 
            else:
                self.crystal.set_prim_vec(ind,vec)
            self.crystal.evaluate_basic()
        
        
    def update_atom_pos(self):
        if len(self.output['final_positions']) != self.crystal.get_totnum_atoms():
            self.dft_job.show_error('CALC', 'mismatch atom numbers')
        
        ind=0
        for group in self.crystal.basis_atom_groups:
            for atom in self.crystal.basis_atom_groups[group]:
                atom.set_position(self.output['final_positions'][ind])
                ind=ind+1
    
    def update_crystal(self):
        self.update_prim_cell()
        self.update_atom_pos()
        
        


