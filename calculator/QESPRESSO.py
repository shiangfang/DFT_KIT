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

from DFT_KIT.core import general_tool
from DFT_KIT.core import env_parm
from DFT_KIT.core import calculator

QES_control_flags='calculation   title   verbosity   restart_mode   wf_collect   nstep   iprint   tstress   tprnfor   dt   wfcdir   lkpoint_dir   max_seconds   etot_conv_thr   forc_conv_thr   disk_io   tefield   dipfield   lelfield   nberrycyc   lorbm   lberry   gdir   nppstr'.split()
QES_system_flags='ibrav   celldm   A   B   C   cosAB   cosAC   cosBC   nbnd   tot_charge   tot_magnetization   starting_magnetization   ecutwfc   ecutrho   ecutfock   nr1   nr2   nr3   nr1s   nr2s   nr3s   nosym   nosym_evc   noinv   no_t_rev   force_symmorphic   use_all_frac   occupations   one_atom_occupations   starting_spin_angle   degauss   smearing   nspin   noncolin   ecfixed   qcutz   q2sigma   input_dft   exx_fraction   screening_parameter   exxdiv_treatment   x_gamma_extrapolation   ecutvcut   nqx1   nqx2   nqx3   lda_plus_u   lda_plus_u_kind   Hubbard_U   Hubbard_J0   Hubbard_alpha   Hubbard_beta   Hubbard_J(i,ityp)   starting_ns_eigenvalue(m,ispin,I)   U_projection_type   edir   emaxpos   eopreg   eamp   angle1   angle2   constrained_magnetization   fixed_magnetization   lambda   report   lspinorb   assume_isolated   esm_bc   esm_w   esm_efield   esm_nfit   vdw_corr   london   london_s6   london_rcut   xdm   xdm_a1   xdm_a2'.split()
QES_electrons_flags='electron_maxstep   scf_must_converge   conv_thr   adaptive_thr   conv_thr_init   conv_thr_multi   mixing_mode   mixing_beta   mixing_ndim   mixing_fixed_ns   diagonalization   ortho_para   diago_thr_init   diago_cg_maxiter   diago_david_ndim   diago_full_acc   efield   efield_cart   startingpot   startingwfc   tqr'.split()
QES_ions_flags='ion_dynamics   ion_positions   phase_space   pot_extrapolation   wfc_extrapolation   remove_rigid_rot   ion_temperature   tempw   tolp   delta_t   nraise   refold_pos   upscale   bfgs_ndim   trust_radius_max   trust_radius_min   trust_radius_ini   w_1   w_2'.split()
QES_cell_flags='cell_dynamics   press   wmass   cell_factor   press_conv_thr   cell_dofree'.split()

#for .pw2wan file
QES_PW2WAN_flags=['write_amn','write_spn','write_mmn','write_unk']



class calculator_QESPRESSO(calculator.calculator):
    def __init__(self,postprocess,dft_job,crystal,kgrid,scheme=0,**parms):
        calculator.calculator.__init__(self,postprocess,dft_job,crystal,kgrid,**parms)
        self.apply_scheme(scheme)
        self.wannier90_analysis=False
        self.write_occupations=False
        self.write_constraints=False
        self.write_atomic_forces=False
        self.atomic_positions_ang=True
        
    def apply_scheme(self,scheme):
        self.set_parm('ibrav','0')
        if scheme==0:
            # general scf for insulator
            self.set_parm('calculation', "'scf'")

            
        elif scheme == 1:
            # general scf for metal
            self.set_parm('calculation', "'scf'")
            self.set_parm('occupations',"'smearing'")
            self.set_parm('smearing',"'gaussian'")
            self.set_parm('degauss','0.005')
            
        elif scheme == 2:
            # band structure calculation
            self.set_parm('calculation', "'nscf'")

        elif scheme==3:
            #relaxation
            #ENCUT increase!
            pass
            
        elif scheme==4:
            #for spin orbit interaction (NON SC)
            self.set_parm('noncolin', '.true.')
            self.set_parm('lspinorb', '.true.')
            
    
    def run_main(self):
        
        if self.wannier90_analysis:
            self.run_wannier()
    
    def qes_generate_pw2wan(self):
        f_=open('qes.pw2wan','w')
        f_.write(' &inputpp\n')
        f_.write("   prefix = '" + self.dft_job.prefix + "',\n")
        f_.write("   outdir = '" + self.dft_job.get_maindir() +"',\n")
        f_.write("   seedname = '" +str() +"',\n")
        for ind_key in self.parms:
            if ind_key in QES_PW2WAN_flags:
                f_.write('   '+ind_key+' = ' + self.parms[ind_key]+' ,\n')
        f_.write(' /')
        f_.write('\n')


        
    def generate_files(self):
        #control section
        f_=open('qes.scf.in','w')
        
        f_.write(' &control\n')
        f_.write("   prefix = '" + self.dft_job.prefix + "',\n")
        f_.write("   outdir = '" + self.dft_job.get_maindir() +"',\n")
        f_.write("   pseudo_dir = '" + env_parm.qespresso_pseudo_dir +"',\n")
        for ind_key in self.parms:
            if ind_key in QES_control_flags:
                f_.write('   '+ind_key+' = ' + self.parms[ind_key]+' ,\n')
        f_.write(' /')
        f_.write('\n')
        
        #system section
        f_.write(' &system\n')
        f_.write('   nat = ' + str(self.crystal.get_totnum_atoms()) + ',\n')
        f_.write('   ntyp = ' + str(len(self.crystal.basis_atom_groups)) + ',\n')
        for ind_key in self.parms:
            if ind_key in QES_system_flags:
                f_.write('   '+ind_key+' = ' + self.parms[ind_key]+' ,\n')
        f_.write(' /')
        f_.write('\n')
        
        #electrons section
        f_.write(' &electrons\n')
        for ind_key in self.parms:
            if ind_key in QES_electrons_flags:
                f_.write('   '+ind_key+' = ' + self.parms[ind_key]+' ,\n')
        f_.write(' /')
        f_.write('\n')
        
        #ions section
        f_.write(' &ions\n')
        for ind_key in self.parms:
            if ind_key in QES_ions_flags:
                f_.write('   '+ind_key+' = ' + self.parms[ind_key]+' ,\n')
        f_.write(' /')
        f_.write('\n')
        
        #cell section
        f_.write(' &cell\n')
        for ind_key in self.parms:
            if ind_key in QES_cell_flags:
                f_.write('   '+ind_key+' = ' + self.parms[ind_key]+' ,\n')
        f_.write(' /')
        f_.write('\n')
        
        #other parts in qespresso
        f_.write('CELL_PARAMETERS angstrom\n')
        f_.write(' '+general_tool.vec_to_str(self.crystal.get_prim_vec(0)) +'\n')
        f_.write(' '+general_tool.vec_to_str(self.crystal.get_prim_vec(1)) +'\n')
        f_.write(' '+general_tool.vec_to_str(self.crystal.get_prim_vec(2)) +'\n')
        f_.write('\n')
        
        f_.write('ATOMIC_SPECIES\n')
        #name, mass, pseudopotential
        for group in self.crystal.basis_atom_groups.keys():
            element=self.crystal.basis_element[group]
            f_.write(' '+group + '  '+str(element.mass) + '  ' + element.info['qes_pot'] +'\n')        
        f_.write('\n')
        
        if self.atomic_positions_ang:
            f_.write('ATOMIC_POSITIONS angstrom\n')
        else:
            f_.write('ATOMIC_POSITIONS crystal\n')
        #species, coordinate x and y
        for ind, group in enumerate(self.crystal.basis_atom_groups.keys()):
            for atom in self.crystal.basis_atom_groups[group]:
                f_.write(' '+ group + ' ' +general_tool.vec_to_str(atom.get_position())+'\n')
        f_.write('\n')
        
        if self.kgrid.kmode ==0:
            f_.write('K_POINTS automatic\n')
            f_.write(' ' + general_tool.vec_to_str(self.kgrid.kgrid)+ ' '+ general_tool.vec_to_str(self.kgrid.kgrid_shift)+ '\n')
        
        elif self.kgrid.kmode ==1:
            f_.write('K_POINTS crystal_b\n')
            f_.write(' '+str(len(self.kgrid.kscan))+'\n')
            for ind in range(len(self.kgrid.kscan)):
                if ind%2 ==1:
                    f_.write(general_tool.vec_to_str(self.kgrid.kscan[ind])+' 1 \n')
                else:
                    f_.write(general_tool.vec_to_str(self.kgrid.kscan[ind])+ ' '+ str(self.kgrid.num_kscan) +'\n')
            
        elif self.kgrid.kmode ==2:
            f_.write('K_POINTS crystal\n')
            f_.write(' '+str(len(self.kgrid.klist))+'\n')
            for ind in range(len(self.kgrid.klist)):
                tmp=self.kgrid.klist[ind]
                f_.write(' '+general_tool.vec_to_str(tmp)+'\n')

            
        f_.write('\n')        

        # optional part
        if self.write_constraints:
            f_.write('CONSTRAINTS\n')
            f_.write('\n')
        
        if self.write_occupations:
            f_.write('OCCUPATIONS\n')
            f_.write('\n')
        
        if self.write_atomic_forces:
            f_.write('ATOMIC_FORCES\n')
            f_.write('\n')
        
        f_.close()
        
    def qespresso_postana_xml(self):
        start_k=1
        end_k=102
        n_bands=40
        all_bands=np.zeros((end_k-start_k+1,n_bands))
        indexs=range(start_k,end_k+1)
        name_prefix='Bi/bismuth.save'

        for ind in range(0,end_k-start_k+1):
            path_ind=name_prefix+'/K'+"{0:05d}".format(indexs[ind])+'/eigenval.xml'
            #print(path_ind)
            xml_tree = ET.parse(path_ind)
            root = xml_tree.getroot()
            #for tmp in root:
            #    print(tmp)
            root_val=root.find('EIGENVALUES')
            #print(root_val.tag)
            #print(root_val.attrib)
            eigen_vals=root_val.text.split()
            for ind2 in range(0,n_bands):
                all_bands[ind,ind2]=(float(eigen_vals[ind2]))
        

    def post_process(self):
        pass
    
    def run_wannier(self):
        pass

