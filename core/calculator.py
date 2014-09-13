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
        
        self.bohr=0.529177210
        self.hartree=27.211385
        self.rydberg=13.605692
        
        self.run_post_process=True

    def set_run_post_process(self,post_process):
        self.run_post_process=post_process
        
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
            
        if self.run_post_process:
            self.post_process()
    
    
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
        
        


