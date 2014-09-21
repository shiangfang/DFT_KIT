# Density_Function_Theory - KIT  v1.0.0 
# August 2014
# Implementation for how to construct calculation for doing VASP calculation with DFT_KIT

import numpy as np
import os
import sys

from DFT_KIT.core import job, kpoint, element, crystal_3D
from DFT_KIT.calculator import QESPRESSO
from DFT_KIT.apps import crystal_structure
from DFT_KIT.interface import interface_script
from DFT_KIT.apps import bismuth_antimony

[input_parm,opt_parm]=interface_script.init_simulation(1)

#create the VCA element
vca_index=int(input_parm[0])
n_vca_tot=10
x_start=1.0
x_end=0.0
num_xs=51
vca_xs=np.linspace(x_start,x_end,num_xs)
vca_x=vca_xs[vca_index]
alloy_pot='Bi_Sb_Alloy'
vca_mass=(1.0-vca_x)*bismuth_antimony.Bi_exp.mass+(vca_x)*bismuth_antimony.Sb_exp.mass
bi_sb_vca=element.element('Xx',vca_mass,83,5,vasp_pot='Xx',qes_pot=alloy_pot+'_'+str(vca_index)+'.UPF')
bi_sb_vca.info['rhom_length']=(1.0-vca_x)*bismuth_antimony.Bi_exp.info['rhom_length']+(vca_x)*bismuth_antimony.Sb_exp.info['rhom_length']
bi_sb_vca.info['angle']=(1.0-vca_x)*bismuth_antimony.Bi_exp.info['angle']+(vca_x)*bismuth_antimony.Sb_exp.info['angle']
bi_sb_vca.info['rhom_u']=(1.0-vca_x)*bismuth_antimony.Bi_exp.info['rhom_u']+(vca_x)*bismuth_antimony.Sb_exp.info['rhom_u']

# vca job, kgrid and crystal construction.
dft_job=job.job(subdir=True)
dft_job.process_opt_parm(opt_parm)
dft_job.sys_info['qes_prefix']='bi_sb_vca_alloy'
dft_kgrid=kpoint.kpoint()
dft_crystal=crystal_structure.a7_structure(bi_sb_vca,length_unit=1.0)
dft_crystal.get_atom('Xx', 0).set_relax_all(False)
dft_crystal.get_atom('Xx', 1).set_relax(False,False,True)


# first round, vc-relaxation
dft_job.sys_info['qes_fname']='bi_sb_alloy_relax'
dft_calc=QESPRESSO.calculator_QESPRESSO(False,dft_job,dft_crystal,dft_kgrid,scheme=4)
dft_calc.load_parm(False, bismuth_antimony.Bi_Sb_qespresso_crystal_scf)
dft_calc.set_parm('ecutwfc', '40')
dft_calc.run_calculation()
dft_calc.update_crystal()

# first round with higher energy cutoff
dft_job.next_task(True)
dft_kgrid.set_grid_mode([15,15,15])
dft_calc.set_parm('ecutwfc', '65')
dft_calc.set_parm('press_conv_thr', '0.05')
dft_calc.run_calculation()
dft_calc.update_crystal()


# second round, self-consistent calculation
dft_job.next_task(True)
dft_job.sys_info['qes_fname']='bi_sb_alloy_scf'
dft_calc.apply_scheme(0)
dft_calc.run_calculation()

# third round, self-consistent calculation
dft_job.next_task(False)
dft_job.sys_info['qes_fname']='bi_sb_alloy_bands'
dft_calc.apply_scheme(2)
#change parameters here
dft_kgrid.set_scan_mode(50, [dft_crystal.k_labels['L'],dft_crystal.k_labels['Gamma'],dft_crystal.k_labels['Gamma'],dft_crystal.k_labels['T']])
dft_calc.run_calculation()



