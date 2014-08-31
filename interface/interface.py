import numpy as np
import scipy.io

from ase import Atoms

def dft_kit_to_ase_atoms(kit_atoms):
    for group in kit_atoms.basis_group_atoms:
        pass
    
def dft_kit_to_ase_kpts(kit_kpts):
    for group in kit_kpts:
        pass


# between numerical data

def read_mat_file(fname):
    return scipy.io.loadmat(fname)

def write_mat_file(fname,data_to_save):
    #data_to_save is a dictionary
    scipy.io.savemat(fname,data_to_save)

def DFT_postana_serieswrite_csv(series_,vars_,f_):
    #series_ is of type DFT_post_ana array
    out_={}
    for var_ in vars_:
        out_[var_]=[]
        
    for obj_ in series_:
        for var_ in vars_:
            out_[var_].append(obj_.get_basic_var(var_))
    
    nobj=len(series_)
    for ind in range(0,nobj):
        f_.write(str(ind))
        for key_ in out_:
            f_.write(', ' + out_[key_][ind])
        f_.write('\n')
        


# to generate figures