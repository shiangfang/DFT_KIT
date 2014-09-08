import numpy as np
import scipy.io
import xml.etree.ElementTree as ET
import pickle

# ASE-environment
from ase import Atoms

def dft_kit_to_ase_atoms(kit_atoms):
    for group in kit_atoms.basis_group_atoms:
        pass
    
def dft_kit_to_ase_kpts(kit_kpts):
    for group in kit_kpts:
        pass

# XML data
def load_from_xml(root_,findstr,data_):
    xml_item=root_.find(findstr)
    for item_ in xml_item:
        data_[item_.attrib['name']]=item_.text


# between numerical data

def matlab_load(fname):
    return scipy.io.loadmat(fname)

def matlab_save(fname,data_to_save):
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

# pickle output data
def pickle_save(fname,data):
    # data=[....]
    f_=open(fname,'wb')
    for var in data:
        pickle.dump(var,f_)
    f_.close()
    
def pickle_load(fname,count):
    f_=open(fname,'rb')
    data=[]
    for ind in range(0,count):
        data.append(pickle.load(f_))
    return data

# to generate figures


