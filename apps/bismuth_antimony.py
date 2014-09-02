# Density_Function_Theory - KIT  v1.0.0 
# August 2014
# Bismuth-Antimony research project 

import numpy as np
import os
import sys

from DFT_KIT.core import job, kpoint, element, crystal_3D
from DFT_KIT.calculator import VASP
from DFT_KIT.apps import crystal_structure

#element.element:
# parameters for running VASP and Qespresso



# Antimony
#Phys. Rev. 141, 562
Sb_exp_1={'lattice_constant':4.489,'angle':(57.0+14.0/60.0)*np.pi/180.0,'rhom_u':0.2336}
#Phys Rev. B 41,11827
Sb_exp_2={'lattice_constant':4.4898,'angle':(57.233)*np.pi/180.0,'rhom_u':0.23362}

# crystal setting
Sb=element.element('Sb',121.760,51,5,vasp_pot='Sb',qes_pot='')
Sb_d=element.element('Sb',121.760,51,15,vasp_pot='Sb_d',qes_pot='')

# DFT setting
Sb_vasp_scf={}
Sb_vasp_nscf_soi={}

Sb_qespresso_scf={}
Sb_qespresso_nscf_soi={}

Sb_wannier90={}




# Bismuth
#experimental value at 4.2K cf. PRB 56, 6620. ->careful about the units a.u. vs Angstron
# Phys. Rev. 166, 643
Bi_exp_1={'lattice_constant':4.7212,'angle':(57.0+19.0/60.0)*np.pi/180.0,'rhom_u':0.23407}
#Phys Rev. B 41,11827
Bi_exp_2={'lattice_constant':4.7236,'angle':(57.35)*np.pi/180.0,'rhom_u':0.23407}

Bi_dft_1={'lattice_constant':4.7973,'angle':(53.0+56.0/60.0)*np.pi/180.0,'rhom_u':0.2348} #RMM-IIS
Bi_dft_2={'lattice_constant':4.7827,'angle':(56.0+17.0/60.0)*np.pi/180.0,'rhom_u':0.2351} #RMM-IIS SCAN
Bi_dft_3={'lattice_constant':4.8038,'angle':(53.0+36.0/60.0)*np.pi/180.0,'rhom_u':0.2347} #CONJ-GRAD

# Crystal setting
Bi_exp=element.element('Bi',208.9804,83,5,vasp_pot='Bi',qes_pot='Bi.UPF',rhom_length=4.7236,angle=1.0009,rhom_u=0.23407)
Bi_d=element.element('Bi',208.9804,83,15,vasp_pot='Bi_d',qes_pot='')

# DFT setting
Bi_vasp_slab_scf={'ISTART':'0','ENCUT':'250','EDIFF':'1E-4','ISMEAR':'-5','SIGMA':'0.2','LMAXMIX':'4','LREAL':'Auto','AMIN':'0.01'}
Bi_vasp_slab_nscf_soi={'ISTART':'0','ICHARG':'11','ENCUT':'250','EDIFF':'1E-4','GGA_COMPAT':'.FALSE.','ISYM':'0','SAXIS':'0 0 1','LSORBIT':'.TRUE.','LMAXMIX':'4','MAGMOM':True,'LREAL':'Auto','AMIN':'0.01'}
Bi_vasp_crystal_scf={'ISTART':'0','ENCUT':'250','EDIFF':'1E-6','ISMEAR':'-5','SIGMA':'0.2','LMAXMIX':'4'}
Bi_vasp_crystal_nscf_soi={'ISTART':'0','ICHARG':'11','ENCUT':'250','EDIFF':'1E-6','GGA_COMPAT':'.FALSE.','ISYM':'0','SAXIS':'0 0 1','LSORBIT':'.TRUE.','LMAXMIX':'4','MAGMOM':True}

Bi_qespresso_crystal_scf={}
Bi_qespresso_crystal_nscf_soi={}
Bi_qespresso_slab_scf={}
Bi_qespresso_slab_nscf_soi={}

Bi_wannier90={}

