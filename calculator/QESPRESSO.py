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

QES_control_flags='calculation  title   verbosity   restart_mode   wf_collect   nstep   iprint   tstress   tprnfor   dt   wfcdir   lkpoint_dir   max_seconds   etot_conv_thr   forc_conv_thr   disk_io   tefield   dipfield   lelfield   nberrycyc   lorbm   lberry   gdir   nppstr'.split()
QES_system_flags='ibrav   celldm   A   B   C   cosAB   cosAC   cosBC   nbnd   tot_charge   tot_magnetization   starting_magnetization   ecutwfc   ecutrho   ecutfock   nr1   nr2   nr3   nr1s   nr2s   nr3s   nosym   nosym_evc   noinv   no_t_rev   force_symmorphic   use_all_frac   occupations   one_atom_occupations   starting_spin_angle   degauss   smearing   nspin   noncolin   ecfixed   qcutz   q2sigma   input_dft   exx_fraction   screening_parameter   exxdiv_treatment   x_gamma_extrapolation   ecutvcut   nqx1   nqx2   nqx3   lda_plus_u   lda_plus_u_kind   Hubbard_U   Hubbard_J0   Hubbard_alpha   Hubbard_beta   Hubbard_J(i,ityp)   starting_ns_eigenvalue(m,ispin,I)   U_projection_type   edir   emaxpos   eopreg   eamp   angle1   angle2   constrained_magnetization   fixed_magnetization   lambda   report   lspinorb   assume_isolated   esm_bc   esm_w   esm_efield   esm_nfit   vdw_corr   london   london_s6   london_rcut   xdm   xdm_a1   xdm_a2'.split()
QES_electrons_flags='electron_maxstep   scf_must_converge   conv_thr   adaptive_thr   conv_thr_init   conv_thr_multi   mixing_mode   mixing_beta   mixing_ndim   mixing_fixed_ns   diagonalization   ortho_para   diago_thr_init   diago_cg_maxiter   diago_david_ndim   diago_full_acc   efield   efield_cart   startingpot   startingwfc   tqr'.split()
QES_ions_flags='ion_dynamics   ion_positions   phase_space   pot_extrapolation   wfc_extrapolation   remove_rigid_rot   ion_temperature   tempw   tolp   delta_t   nraise   refold_pos   upscale   bfgs_ndim   trust_radius_max   trust_radius_min   trust_radius_ini   w_1   w_2'.split()
QES_cell_flags='cell_dynamics   press   wmass   cell_factor   press_conv_thr   cell_dofree'.split()

#for .pw2wan file
QES_PW2WAN_flags=['write_amn','write_spn','write_mmn','write_unk']
QES_PW2BGW_flags='real_or_complex  symm_type  wfng_flag  wfng_file  wfng_kgrid  wfng_nk1  wfng_nk2  wfng_nk3  wfng_dk1  wfng_dk2  wfng_dk3  wfng_occupation  wfng_nvmin  wfng_nvmax  rhog_flag  rhog_file  vxcg_flag  vxcg_file  vxc0_flag  vxc0_file  vxc_flag  vxc_file  vxc_integral  vxc_diag_nmin  vxc_diag_nmax  vxc_offdiag_nmin  vxc_offdiag_nmax  vxc_zero_rho_core  vscg_flag  vscg_file  vkbg_flag  vkbg_file'.split()


class calculator_QESPRESSO(calculator.calculator):
    def __init__(self,postprocess,dft_job,crystal,kgrid,scheme=0,**parms):
        calculator.calculator.__init__(self,postprocess,dft_job,crystal,kgrid,**parms)
        self.apply_scheme(scheme)
        self.wannier90_analysis=False
        self.write_occupations=False
        self.write_constraints=False
        self.write_atomic_forces=False
        self.atomic_positions_ang=True
        self.parms['claculation']=''
        self.qes_vars={}
        
    def apply_scheme(self,scheme):
        self.set_parm('ibrav','0')
        if scheme==0:
            # general scf (for insulator)
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
            self.set_parm('calculation', "'relax'")

        elif scheme==4:
            #variable cell relaxation
            #ENCUT increase!
            self.set_parm('calculation', "'vc-relax'")

        
        
            
        elif scheme==5:
            #for spin orbit interaction (NON SC)
            self.set_parm('noncolin', '.true.')
            self.set_parm('lspinorb', '.true.')
            
    
    def run_main(self):
        env_parm.run_qes_pwx(self.dft_job.job_mamanger_mode,self.dft_job.sys_info['qes_fname'])
        
    def run_pw2wan(self):
        self.qes_generate_pw2wan()
        env_parm.run_qes_pw2wan(self.dft_job.job_mamanger_mode, self.dft_job.sys_info['qes_fname'])
    
    def qes_generate_pw2wan(self):
        f_=open(self.dft_job.sys_info['qes_fname']+'.pw2wan.in','w')
        f_.write(' &inputpp\n')
        f_.write("   prefix = '" + self.dft_job.sys_info['qes_prefix'] + "'\n")
        f_.write("   outdir = '" + self.dft_job.get_maindir() +"'\n")
        f_.write("   seedname = '" +self.dft_job.sys_info['wan90_seedname'] +"'\n")
        for ind_key in self.parms:
            if ind_key in QES_PW2WAN_flags:
                f_.write('   '+ind_key+' = ' + self.parms[ind_key]+' \n')
        f_.write(' /')
        f_.write('\n')
        f_.close()
        
    def generate_files(self):
        #control section
        f_=open(self.dft_job.sys_info['qes_fname']+'.pwx.in','w')
        if 'calculation' not in self.parms or self.parms['calculation']=='':
            self.dft_job.show_error('CALC', 'calculation mode not set')
            return
        
        f_.write(' &control\n')
        f_.write("   prefix = '" + self.dft_job.sys_info['qes_prefix'] + "',\n")
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
                if self.parms['calculation']=="'vc-relax'" or self.parms['calculation']=="'relax'" or self.parms['calculation']=="'md'" or self.parms['calculation']=="'vc-md'":
                    f_.write(' '+ group + ' ' +general_tool.vec_to_str(atom.get_position())+'  ' +str(general_tool.bool_to_10(atom.relax[0]))+ ' '+str(general_tool.bool_to_10(atom.relax[1])) + ' '+str(general_tool.bool_to_10(atom.relax[2]))+ '\n')
                else:
                    f_.write(' '+ group + ' ' +general_tool.vec_to_str(atom.get_position()) + '\n')
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
        
        #other parts in qespresso
        f_.write('CELL_PARAMETERS angstrom\n')
        f_.write(' '+general_tool.vec_to_str(self.crystal.get_prim_vec(0)) +'\n')
        f_.write(' '+general_tool.vec_to_str(self.crystal.get_prim_vec(1)) +'\n')
        f_.write(' '+general_tool.vec_to_str(self.crystal.get_prim_vec(2)) +'\n')
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
        
        
        
    def post_process(self):
        self.qespresso_post_process_xml(self.dft_job.sys_info['qes_prefix']+'.save/' ,'data-file.xml')
        if os.path.isfile(self.dft_job.sys_info['qes_fname']+'.pwx.out'):
            self.qespresso_post_process_outfile(self.dft_job.sys_info['qes_fname']+'.pwx.out')
        else:
            self.dft_job.show_error('QESPRESSO', 'pp-no out file')
        
        #fill in basic information
        #crystal
        self.output['num_atoms']=self.qes_vars['num_atoms']
        self.output['num_types']=self.qes_vars['num_types']
        self.output['final_prim_vectors']=np.array([self.qes_vars['prim_a1'],self.qes_vars['prim_a2'],self.qes_vars['prim_a3']])
        self.output['final_positions']=np.array(self.qes_vars['atom_pos'])

        #Energy:
        self.output['total_energy']=self.qes_vars['tot_energy']*self.rydberg
        
        
        
        #eigenvalues/bands
        
    def qespresso_post_process_outfile(self,fname):
        f_=open(fname,'r')
        self.qes_vars['sc_tot_energy']=[]
        self.qes_vars['sc_harrisf_energy']=[]
        self.qes_vars['sc_energy_accu']=[]
        iteration=0
        
        end_scf=False
        calc_scf=False
        calc_band=False
        self.qes_vars['tot_energy']=0.0
        self.qes_vars['harrisf_energy']=0.0
        self.qes_vars['energy_accu']=0.0
        self.qes_vars['onee_energy']=0.0
        self.qes_vars['hartree_energy']=0.0
        self.qes_vars['xc_energy']=0.0
        self.qes_vars['ewald_energy']=0.0
        
        while True:
            tmpstr=f_.readline()
            tmpstrs=tmpstr.split()
            if tmpstr=='':
                break
            
            if tmpstr.find('Self-consistent Calculation')>=0:
                calc_scf=True
                
            if tmpstr.find('Band Structure Calculation')>=0:
                calc_band=True
            
            if tmpstr.find('iteration #')>=0:
                iteration = int(tmpstrs[2])
                
            if tmpstr.find('End of self-consistent calculation')>=0:
                end_scf=True
                
            #cpu/mem
            if tmpstr.find('PWSCF')>=0 and tmpstr.find('CPU')>=0:
                self.qes_vars['cpu_time']=tmpstrs[2]
                self.qes_vars['wall_time']=tmpstrs[4]
            
            if tmpstr.find('total energy')>=0 and tmpstr.find('=')>=0:
                if tmpstr.find('!')>=0:
                    self.qes_vars['tot_energy']=float(tmpstrs[4])
                else:
                    self.qes_vars['sc_tot_energy'].append(float(tmpstrs[3]))

            if tmpstr.find('Harris-Foulkes estimate')>=0:
                if tmpstr.find('!')>=0:
                    self.qes_vars['harrisf_energy']=float(tmpstrs[3])
                else:
                    self.qes_vars['sc_harrisf_energy'].append(float(tmpstrs[3]))
            
            if tmpstr.find('estimated scf accuracy')>=0:
                if tmpstr.find('!')>=0:
                    self.qes_vars['energy_accu']=float(tmpstrs[4])
                else:
                    self.qes_vars['sc_energy_accu'].append(float(tmpstrs[4]))
                
            if tmpstr.find('one-electron contribution')>=0:
                self.qes_vars['onee_energy']=float(tmpstrs[3])
            if tmpstr.find('hartree contribution')>=0:
                self.qes_vars['hartree_energy']=float(tmpstrs[3])
            if tmpstr.find('xc contribution')>=0:
                self.qes_vars['xc_energy']=float(tmpstrs[3])
            if tmpstr.find('ewald contribution')>=0:
                self.qes_vars['ewald_energy']=float(tmpstrs[3])
            #error message handling
            
            
            
        
    def qespresso_post_process_xml(self,xmldir,xmlfile='data-file.xml'):
        tree = ET.parse(xmldir+xmlfile)
        root = tree.getroot()
        
        root_header=root.find('HEADER')
        root_control=root.find('CONTROL')
        
        root_cell=root.find('CELL')
        prim_vec_a1=root_cell.find('DIRECT_LATTICE_VECTORS/a1')
        self.qes_vars['prim_a1']=self.bohr*general_tool.str_to_vec(prim_vec_a1.text.split())
        prim_vec_a2=root_cell.find('DIRECT_LATTICE_VECTORS/a2')
        self.qes_vars['prim_a2']=self.bohr*general_tool.str_to_vec(prim_vec_a2.text.split())
        prim_vec_a3=root_cell.find('DIRECT_LATTICE_VECTORS/a3')
        self.qes_vars['prim_a3']=self.bohr*general_tool.str_to_vec(prim_vec_a3.text.split())
        rec_vec_b1=root_cell.find('RECIPROCAL_LATTICE_VECTORS/b1')
        self.qes_vars['rec_b1']=(1.0/self.bohr)*general_tool.str_to_vec(rec_vec_b1.text.split())
        rec_vec_b2=root_cell.find('RECIPROCAL_LATTICE_VECTORS/b2')
        self.qes_vars['rec_b2']=(1.0/self.bohr)*general_tool.str_to_vec(rec_vec_b2.text.split())
        rec_vec_b3=root_cell.find('RECIPROCAL_LATTICE_VECTORS/b3')
        self.qes_vars['rec_b3']=(1.0/self.bohr)*general_tool.str_to_vec(rec_vec_b3.text.split())
        
        root_ions=root.find('IONS')
        tmp=root_ions.find('NUMBER_OF_ATOMS')
        self.qes_vars['num_atoms']=int(tmp.text)
        tmp=root_ions.find('NUMBER_OF_SPECIES')
        self.qes_vars['num_types']=int(tmp.text)
        
        self.qes_vars['atom_pos']=[]
        for ind in range(1,self.qes_vars['num_atoms']+1):
            tmp=root_ions.find('ATOM.'+str(ind))
            self.qes_vars['atom_pos'].append(general_tool.str_to_vec(tmp.attrib['tau'].split()))
        
        root_symmetries=root.find('SYMMETRIES')
        root_electric_field=root.find('ELECTRIC_FIELD')
        root_pw=root.find('PLANE_WAVES')
        tmp=root_pw.find('WFC_CUTOFF')
        
        root_spin=root.find('SPIN')
        root_mag=root.find('MAGNETIZATION_INIT')
        root_xc=root.find('EXCHANGE_CORRELATION')
        tmp=root_xc.find('DFT')
        self.qes_vars['xc']=tmp.text
        
        root_occ=root.find('OCCUPATIONS')
        root_bz=root.find('BRILLOUIN_ZONE')
        tmp=root_bz.find('NUMBER_OF_K-POINTS')
        self.qes_vars['num_kpts']=int(tmp.text)
        self.qes_vars['kpts']=[]
        self.qes_vars['kpts_weight']=[]
        for ind in range(1,self.qes_vars['num_kpts']+1):
            tmp=root_bz.find('K-POINT.'+str(ind))
            self.qes_vars['kpts'].append(tmp.attrib['XYZ'].split())
            self.qes_vars['kpts_weight'].append(tmp.attrib['WEIGHT'])
        
        root_par=root.find('PARALLELISM')
        tmp=root_par.find('NUMBER_OF_PROCESSORS')
        
        root_charge_den=root.find('CHARGE-DENSITY')
        
        
        root_band=root.find('BAND_STRUCTURE_INFO')
        tmp=root_band.find('UNITS_FOR_ENERGIES')
        self.qes_vars['unit_energy']=tmp.text
        tmp=root_band.find('FERMI_ENERGY')
        self.qes_vars['fermi_energy']=float(tmp.text)
        tmp=root_band.find('NUMBER_OF_BANDS')
        self.qes_vars['num_bands']=int(tmp.text)
        tmp=root_band.find('NUMBER_OF_ELECTRONS')
        self.qes_vars['num_electrons']=float(tmp.text)
        
        
        root_eigval=root.find('EIGENVALUES')
        self.qes_vars['eigenvalues']=np.zeros((self.qes_vars['num_bands'],self.qes_vars['num_kpts']))
        self.qes_vars['occupations']=np.zeros((self.qes_vars['num_bands'],self.qes_vars['num_kpts']))
        
        for indk in range(1,self.qes_vars['num_kpts']+1):
            tmp=root_eigval.find('K-POINT.'+str(ind))
            subtmp=tmp.find('DATAFILE')
            eigxml=subtmp.attrib['iotk_link']
            
            #analyze the xml for the k point
            eigtree = ET.parse(xmldir+eigxml)
            eigroot = eigtree.getroot()
            
            eigroot_val=eigroot.find('EIGENVALUES')
            tmp_vals=eigroot_val.text.split()
            for ind2 in range(0,self.qes_vars['num_bands']):
                self.qes_vars['eigenvalues'][ind2,indk-1]=(float(tmp_vals[ind2]))

            eigroot_occ=eigroot.find('OCCUPATIONS')
            tmp_occs=eigroot_occ.text.split()
            for ind2 in range(0,self.qes_vars['num_bands']):
                self.qes_vars['occupations'][ind2,indk-1]=(float(tmp_occs[ind2]))

            
            
        root_eigvec=root.find('EIGENVECTORS')
        

