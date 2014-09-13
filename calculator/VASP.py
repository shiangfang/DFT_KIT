# Density_Function_Theory - KIT  v1.0.0 
# August 2014
# Class for calculation with VASP

import numpy as np
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
from DFT_KIT.interface import interface

VASP_incar_flags=['NGX','NGY','NGZ','NGXF','NGYF' ,'NGZF' ,'NBANDS','NBLK','NWRITE', 
'ISTART' ,'ICHARG','ISPIN' ,'INIWAV','ENCUT' ,'PREC','NELM', 'LSORBIT', 'GGA_COMPAT',
'NELMIN' ,'NELMDL','EDIFF','EDIFFG','NSW','NBLOCK','KBLOCK','IBRION', 'SAXIS', 'LMAXMIX',
'ISIF','IWAVPR','ISYM','SYMPREC' ,'LCORR','POTIM','TEBEG','TEEND','AMIN',
'SMASS','NPACO','APACO','POMASS','ZVAL','RWIGS','NELECT','NUPDOWN', 
'EMIN','EMAX','ISMEAR','SIGMA','ALGO','IALGO','LREAL','ROPT','GGA','VOSKOWN','DIPOL', 
'AMIX','BMIX','WEIMIN','EBREAK','DEPER','TIME','LWAVE','LCHARG' ,'LVTOT','LVHAR', 
'LELF','LORBIT','LSCALAPACK','LSCALU','LASYNC']

VASP_kpoints_flags=[]

class calculator_VASP(calculator.calculator):
    def __init__(self,postprocess,dft_job,crystal,kgrid,scheme=0,**parms):
        calculator.calculator.__init__(self,postprocess,dft_job,crystal,kgrid,**parms)
        self.apply_scheme(scheme)
        if 'xc' in parms:
            xc=parms['xc']
        else:
            xc='PBE'
        
        #central control variables
        self.potcar_gen=True
        self.poscar_gen=True
        self.xc=xc
        self.vasp_vars={}
        self.run_vasp_mode=0
    
    def set_run_vasp_mode(self,mode):
        self.run_vasp_mode=mode
    
    def run_main(self):
        if self.run_vasp_mode==1:
            env_parm.run_vasp_ncl(self.dft_job.job_mamanger_mode,self.dft_job.opt_parm['cpu'])
        elif self.run_vasp_mode==2:
            env_parm.run_vasp_gamma(self.dft_job.job_mamanger_mode,self.dft_job.opt_parm['cpu'])
        else:
            env_parm.run_vasp_std(self.dft_job.job_mamanger_mode,self.dft_job.opt_parm['cpu'])
            
    def generate_files(self):
        #INCAR, KPOINTS, POSCAR, and copy user-defined files
        #write incar file
        self.dft_job.show('CALC_VASP',' Generate input files in ' + self.dft_job.get_maindir())
        self.dft_job.show_verbose('CALC_VASP','Generating INCAR file')
        file_incar=open(self.dft_job.get_maindir()+'INCAR','w')
        self.vasp_generate_incar(file_incar)
        file_incar.close()
        
        #write poscar file
        self.dft_job.show_verbose('CALC_VASP','Generating POSCAR file')
        if self.poscar_gen:
            file_poscar=open(self.dft_job.get_maindir()+'POSCAR','w')
            self.vasp_generate_poscar(file_poscar)
            file_poscar.close()
        
        #write kpoints file
        self.dft_job.show_verbose('CALC_VASP','VASP : Generating KPOINTS file')
        file_kpoints=open(self.dft_job.get_maindir()+'KPOINTS','w')
        self.vasp_generate_kpoints(file_kpoints)
        file_kpoints.close()
        
        if self.potcar_gen:
            pot_library=''
            if self.xc == 'PBE':
                pot_library=env_parm.vasp_pseudo_dir+'paw_pbe/'
            elif self.xc == 'LDA':
                pot_library=env_parm.vasp_pseudo_dir+'paw_lda/'
            else:
                self.dft_job.show_error('CALC_VASP','Unknown XC setting')
            file_potcar=open(self.dft_job.get_maindir()+'POTCAR','w')
            for group in self.crystal.basis_atom_groups:
                group
                group_potential=self.crystal.basis_element[group].info['vasp_pot']
                if group_potential == '':
                    group_potential=group
                group_potential_fname=pot_library+group_potential+'/POTCAR'
                with open(group_potential_fname) as potcarinfile:
                    for line_ in potcarinfile:
                        file_potcar.write(line_)
            file_potcar.close()
    def vasp_generate_incar(self,f_):
        f_.write('SYSTEM = ' + self.dft_job.system + '\n')
        
        if 'NPAR' in self.parms:
            if self.parms['NPAR'] !='0':
                f_.write('NPAR = ' +self.parms['NPAR']+'\n')
            else:
                f_.write('NPAR = ' +int(np.sqrt(int(self.dft_job.opt_parm['cpu'])))+'\n')   
        if 'MAGMOM' in self.parms:
            if self.parms['MAGMOM'] == True:
                f_.write('MAGMOM = ')
                for group in self.crystal.basis_atom_groups.keys():
                    for atom in self.crystal.basis_atom_groups[group]:
                        f_.write(general_tool.vec_to_str(atom.get_magmom())+'  ')
                f_.write('\n')
        
        for ind_key in self.parms:
            if ind_key in VASP_incar_flags:
                f_.write(ind_key+' = '+self.parms[ind_key]+ '\n')
                
                
    def vasp_generate_poscar(self,f_):
        self.dft_job.show_verbose('CALC_VASP','Generating POSCAR content cart')
        f_.write(self.crystal.description + '\n' )
        f_.write(str(self.crystal.get_length_unit()) +'\n')
        f_.write(' '+general_tool.vec_to_str(self.crystal.get_prim_vec(0)) +'\n')
        f_.write(' '+general_tool.vec_to_str(self.crystal.get_prim_vec(1)) +'\n')
        f_.write(' '+general_tool.vec_to_str(self.crystal.get_prim_vec(2)) +'\n')
        
        all_atoms=self.crystal.basis_atom_groups.keys()
        all_atoms_nums=[]
        for group in all_atoms:
            all_atoms_nums.append(str(len(self.crystal.basis_atom_groups[group])))
        f_.write(' '.join(all_atoms)+'\n')
        f_.write(' '.join(all_atoms_nums)+'\n')
        
        #if self.poscar_selective:
        #    f_.write('Selective Dynamics\n')
        
        if self.crystal.cart_coordinate:
            f_.write('Cartesian\n')
        else:
            f_.write('Primitive vector\n')
        for group in self.crystal.basis_atom_groups.keys():
            for atom in self.crystal.basis_atom_groups[group]:
                f_.write(general_tool.vec_to_str(atom.get_position()))
                #if self.poscar_selective:
                #    f_.write(' '+general_tool.bool_to_str(atom.get_attribute('XRelax'))+' '+general_tool.bool_to_str(atom.get_attribute('YRelax'))+' '+general_tool.bool_to_str(atom.get_attribute('ZRelax')) +'\n')
                #else:
                f_.write('\n')
    def vasp_generate_kpoints(self,f_):
        if self.kgrid.kmode==0:
            if self.kgrid.kgridtype==0:
                #normal grid sampling
                f_.write('K-Points with Monkhorst Pack\n 0\nMonkhorst Pack\n')
                f_.write(' ' + general_tool.vec_to_str(self.kgrid.kgrid)+'\n')
                f_.write(' '+general_tool.vec_to_str(self.kgrid.kgrid_shift))
            elif self.kgrid.kgridtype==1:
            #normal grid sampling
                f_.write('K-Points with Auto-mesh(Gamma)\n 0\nGamma\n')
                f_.write(' ' + general_tool.vec_to_str(self.kgrid.kgrid)+'\n')
                f_.write(' '+general_tool.vec_to_str(self.kgrid.kgrid_shift))
        elif self.kgrid.kmode==1:
            f_.write('K-Points for Bandstructure with Linear mode\n')
            f_.write(' '+str(self.kgrid.num_kscan)+'\nLine-mode\n')
            if self.kgrid.rec_coordinate:
                f_.write('rec\n')
            else:
                f_.write('cart\n')
            for ind in range(len(self.kgrid.kscan)):
                f_.write(general_tool.vec_to_str(self.kgrid.kscan[ind])+'\n')
                if ind%2 ==1:
                    f_.write('\n')
        elif self.kgrid.kmode==2:
            f_.write('K-Points manual mode\n')
            f_.write(' ' + str(len(self.kgrid.klist))+'\n')
            if self.kgrid.rec_coordinate:
                f_.write('rec\n')
            else:
                f_.write('cart\n')
            for ind in range(len(self.kgrid.klist)):
                tmp=self.kgrid.klist[ind]
                f_.write(' '+general_tool.vec_to_str(tmp[0:3])+'  '+str(tmp[3])+'\n')

    def apply_scheme(self,scheme):
        if scheme==0:
            #start from scratch
            #basic settings for insulator
            self.set_parm('ISTART', '0') #from scratch
            self.set_parm('ICHARG', '2')
            self.set_parm('EDIFF', '1E-6')
            self.set_parm('ISMEAR','-5')


        elif scheme==1:
            #start from scratch
            #basic settings for metal/semimetal
            self.set_parm('ISTART', '0') #from scratch
            self.set_parm('ICHARG', '2')
            self.set_parm('EDIFF', '1E-6')
            self.set_parm('ISMEAR','-5')
            self.set_parm('SIGMA','0.2')
            
        elif scheme==2:
            #non-selfconsistent calculation
            #band structure
            self.vasp_incar_turnoff('ISMEAR')
            self.vasp_incar_turnoff('SIGMA')
            self.set_parm('ICHARG', '11')
                
        elif scheme==3:
            #relaxation
            #ENCUT increase!
            self.set_parm('EDIFFG', '-0.01')
            self.set_parm('NSW', '600')
            self.set_parm('IBRION', '1')
            self.set_parm('ISIF', '4')
            self.poscar_selective=True
                
            
        elif scheme==4:
            #for spin orbit interaction (NON SC)
            self.vasp_incar_turnoff('ISMEAR')
            self.vasp_incar_turnoff('SIGMA')
            #self.set_parm('ISTART', '1')
            self.set_parm('LSORBIT', '.TRUE.')
            self.set_parm('ICHARG', '11')
            self.set_parm('ISYM', '0')
            self.set_parm('SAXIS', '0 0 1')
            self.set_parm('GGA_COMPAT', '.FALSE.')
            self.set_parm('LMAXMIX', '4')
            #need to handle magmom
            self.kpoint_mode=2
            #if overwrite:
            #    self.kpoint_num_kpoints=20
        
        elif scheme==5:
            #Spin-orbit coupling (SC)
            self.set_parm('LSORBIT', '.TRUE.')
            self.set_parm('ICHARG', '1')
            self.set_parm('ISYM', '0')
            self.set_parm('SAXIS', '0 0 1')
            self.set_parm('GGA_COMPAT', '.FALSE.')
            self.set_parm('LMAXMIX', '4')
        
        
        else:
            self.dft_job.show_error('CALC_VASP','Undefined Scheme')


#Post Process tools for VASP
    def post_process(self):
        #xml analysis
        self.vasp_post_process_xml()
        
        #analyze other files with info not in xml
        self.vasp_post_process_OUTCAR() #to read job running information
        
        #fill in basic info (c.f. calculator.py for list)
        
        #crystal and atoms
        self.output['num_atoms']=int(self.vasp_vars['N_atoms'])
        self.output['num_types']=int(self.vasp_vars['N_atoms'])
        self.output['init_prim_vectors']=self.vasp_vars['Init_prim']
        self.output['init_volume']=float(self.vasp_vars['Init_vol'])
        self.output['final_prim_vectors']=self.vasp_vars['Final_prim']
        self.output['final_volume']=float(self.vasp_vars['Final_vol'])
        
        
        #energy
        self.output['total_energy']=float(self.final_calculation['Etotsig0'])
        self.output['free_energy']=float(self.final_calculation['Efree'])
        self.output['fermi_energy']=float(self.final_calculation['EFermi'])
        self.output['entropy']=float(self.final_calculation['Eentropy'])
        self.output['energy_cutoff']=float(self.vasp_vars['ENMAX'])
        self.output['num_electrons']=round(float(self.vasp_vars['NELECT']))
    
        self.output['num_bands']=int(self.vasp_vars['NBANDS'])
        
    
    


    def vasp_load_calculation_xml(self,root_cals,data_):
        root_cals1=root_cals.findall("scstep")
        data_['SC_Etotsig0']=[]
        data_['SC_EwoEntropy']=[]
        data_['SC_Efree']=[]
        for scstep in root_cals1:
            tmp=scstep.find("./energy/*[@name='e_0_energy']")
            data_['SC_Etotsig0'].append(tmp.text)
            tmp=scstep.find("./energy/*[@name='e_wo_entrp']")
            data_['SC_EwoEntropy'].append(tmp.text)
            tmp=scstep.find("./energy/*[@name='e_fr_energy']")
            data_['SC_Efree'].append(tmp.text)
        
        final_sc=root_cals1[len(root_cals1)-1]
        tmp=final_sc.find("./energy/*[@name='e_0_energy']")
        data_['Etotsig0']=tmp.text
        tmp=final_sc.find("./energy/*[@name='e_wo_entrp']")
        data_['EwoEntropy']=tmp.text
        tmp=final_sc.find("./energy/*[@name='e_fr_energy']")
        data_['Efree']=tmp.text
        tmp=final_sc.find("./energy/*[@name='alphaZ']")
        data_['EalphaZ']=tmp.text
        tmp=final_sc.find("./energy/*[@name='ewald']")
        data_['Eewald']=tmp.text
        tmp=final_sc.find("./energy/*[@name='hartreedc']")
        data_['Ehartree']=tmp.text
        tmp=final_sc.find("./energy/*[@name='XCdc']")
        data_['Excdc']=tmp.text
        tmp=final_sc.find("./energy/*[@name='pawpsdc']")
        data_['Epawpsdc']=tmp.text
        tmp=final_sc.find("./energy/*[@name='pawaedc']")
        data_['Epawaedc']=tmp.text
        tmp=final_sc.find("./energy/*[@name='eentropy']")
        data_['Eentropy']=tmp.text
        tmp=final_sc.find("./energy/*[@name='bandstr']")
        data_['Ebandstr']=tmp.text
        tmp=final_sc.find("./energy/*[@name='atom']")
        data_['Eatom']=tmp.text
    
        root_cal_forces=root_cals.find(".//*[@name='forces']")
        data_['Forces']=[]
        for force in root_cal_forces:
            data_['Forces'].append(force.text.split())
            
        root_cal_stress=root_cals.find(".//*[@name='stress']")
        data_['Stress']=[]
        if root_cal_stress is not None:
            for stress in root_cal_stress:
                data_['Stress'].append(stress.text.split())
        
        root_cal_str=root_cals.find("structure")
        
        if root_cal_str is not None:
            calstr_pos=root_cal_str.find(".//*[@name='positions']")
            data_['CAL_pos']=[]
            for tmp in calstr_pos:
                data_['CAL_pos'].append(tmp.text.split())
            calstr_prim=root_cal_str.find("./crystal/*[@name='basis']")
            data_['CAL_prim']=[]
            for tmp in calstr_prim:
                data_['CAL_prim'].append(tmp.text.split())
            tmp=root_cal_str.find("./crystal/*[@name='volume']")
            data_['CAL_vol']=tmp.text
            calstr_rec=root_cal_str.find("./crystal/*[@name='rec_basis']")
            data_['CAL_rec']=[]
            for tmp in calstr_rec:
                data_['CAL_rec'].append(tmp.text.split())
            
        
        root_cal_kpts=root_cals.find("eigenvalues/array/set/set")
        data_['KPTS_BAND']=[]
        data_['KPTS_OCCU']=[]
        if root_cal_kpts is not None:
            for kpt in root_cal_kpts:
                band_=[]
                occu_=[]
                for kpt_data in kpt:
                    kptmp=kpt_data.text.split()
                    band_.append(kptmp[0])
                    occu_.append(kptmp[1])
                data_['KPTS_BAND'].append(band_)
                data_['KPTS_OCCU'].append(occu_)
        
        root_cal_projected=root_cals.find("projected/array/set")
        data_['PROJECT_BAND']=[]
        if root_cal_projected is not None:
            tmp_=[]
            for proj_spin in root_cal_projected:
                tmp_spin=[]
                for kpt_ in proj_spin:
                    tmp_kpt=[]
                    for band_ in kpt_:
                        tmp_band=[]
                        for proj_val in band_:
                            tmp_band.append(proj_val.text.split())
                        tmp_kpt.append(tmp_band)
                    tmp_spin.append(tmp_kpt)
                tmp_.append(tmp_spin)
            data_['PROJECT_BAND']=tmp_
        
        
        #working...!!!
        root_cal_dos_fermi=root_cals.find("./dos/*[@name='efermi']")
        data_['EFermi']=[]
        if root_cal_dos_fermi is not None:
            data_['EFermi']=root_cal_dos_fermi.text
        
        root_cal_dossets=root_cals.find("dos/total/array/set")
        data_['CAL_DOS']=[]
        if root_cal_dossets is not None:
            for dosset in root_cal_dossets:
                for data_dosset in dosset:
                    data_['CAL_DOS'].append(data_dosset.text.split())



    def vasp_post_process_xml(self,xmlfile='vasprun.xml'):
        #this will read from XML file
        tree = ET.parse(xmlfile)
        root = tree.getroot()
        
        #generator
        root_gen=root.find('generator')
        tmp=root_gen.find(".//*[@name='version']")
        self.vasp_vars['VASPversion']=tmp.text
        tmp=root_gen.find(".//*[@name='subversion']")
        self.vasp_vars['VASPsubversion']=tmp.text
        tmp=root_gen.find(".//*[@name='platform']")
        self.vasp_vars['VASPplatform']=tmp.text
        tmp=root_gen.find(".//*[@name='date']")
        self.vasp_vars['VASPdate']=tmp.text
        tmp=root_gen.find(".//*[@name='time']")
        self.vasp_vars['VASPtime']=tmp.text
        #incar
        root_incar=root.find('incar')
        tmp_incar={}
        for opt_incar in root_incar:
            tmp_incar[opt_incar.attrib['name']]=opt_incar.text
        self.vasp_vars['INCAR']=tmp_incar
        
        #kpoints
        root_kpoints=root.find('kpoints')
        root_kptgen=root_kpoints.find('generation')
        self.vasp_vars['kpt_generation']=''
        self.vasp_vars['kpt_gen_div']=''
        self.vasp_vars['kpt_gen_vs']=[]
        if root_kptgen is not None:
            self.vasp_vars['kpt_generation']=root_kptgen.attrib['param']
            root_kptgen_div=root_kptgen.find(".//*[@name='divisions']")
            self.vasp_vars['kpt_gen_div']=root_kptgen_div.text
        
            root_kptgen_vs=root_kptgen.findall('v')
            for gen_vs in root_kptgen_vs:
                self.vasp_vars['kpt_gen_vs'].append(gen_vs.text.split())
        
        kptslist=root_kpoints.find(".//*[@name='kpointlist']")
        self.vasp_band_kpoints=[]
        for tmp in kptslist:
            self.vasp_band_kpoints.append(tmp.text.split())
            
        kptsweg=root_kpoints.find(".//*[@name='weights']")
        self.vasp_band_kpoints_weight=[]
        for tmp in kptsweg:
            self.vasp_band_kpoints_weight.append(tmp.text)
        
        #parameters
        root_pars=root.find('parameters')
        
        tmp=root_pars.find(".//*[@name='GGA_COMPAT']")
        self.vasp_vars['GGA_COMPACT']=tmp.text
        tmp=root_pars.find(".//*[@name='LDAU']")
        self.vasp_vars['LDAU']=tmp.text
        tmp=root_pars.find(".//*[@name='LBERRY']")
        self.vasp_vars['LBERRY']=tmp.text
    
        interface.load_from_xml(root_pars,".//*[@name='general']",self.vasp_vars)
        interface.load_from_xml(root_pars,".//*[@name='electronic']",self.vasp_vars)
        interface.load_from_xml(root_pars,".//*[@name='electronic smearing']",self.vasp_vars)
        interface.load_from_xml(root_pars,".//*[@name='electronic projectors']",self.vasp_vars)
        interface.load_from_xml(root_pars,".//*[@name='electronic startup']",self.vasp_vars)
        interface.load_from_xml(root_pars,".//*[@name='electronic spin']",self.vasp_vars) 
        interface.load_from_xml(root_pars,".//*[@name='electronic exchange-correlation']",self.vasp_vars)
        interface.load_from_xml(root_pars,".//*[@name='electronic convergence']",self.vasp_vars) 
        interface.load_from_xml(root_pars,".//*[@name='electronic convergence detail']",self.vasp_vars)
        interface.load_from_xml(root_pars,".//*[@name='electronic mixer']",self.vasp_vars) 
        interface.load_from_xml(root_pars,".//*[@name='electronic mixer details']",self.vasp_vars)
        interface.load_from_xml(root_pars,".//*[@name='electronic dipolcorrection']",self.vasp_vars)
        interface.load_from_xml(root_pars,".//*[@name='grids']",self.vasp_vars)
        interface.load_from_xml(root_pars,".//*[@name='ionic']",self.vasp_vars) 
        interface.load_from_xml(root_pars,".//*[@name='ionic md']",self.vasp_vars)
        interface.load_from_xml(root_pars,".//*[@name='symmetry']",self.vasp_vars)
        interface.load_from_xml(root_pars,".//*[@name='dos']",self.vasp_vars) 
        interface.load_from_xml(root_pars,".//*[@name='writing']",self.vasp_vars)
        interface.load_from_xml(root_pars,".//*[@name='performance']",self.vasp_vars)
        interface.load_from_xml(root_pars,".//*[@name='miscellaneous']",self.vasp_vars)
        interface.load_from_xml(root_pars,".//*[@name='electronic exchange-correlation']",self.vasp_vars)
        interface.load_from_xml(root_pars,".//*[@name='vdW DFT']",self.vasp_vars)
        interface.load_from_xml(root_pars,".//*[@name='model GW']",self.vasp_vars)
        interface.load_from_xml(root_pars,".//*[@name='linear response parameters']",self.vasp_vars)
        interface.load_from_xml(root_pars,".//*[@name='orbital magnetization']",self.vasp_vars)
        interface.load_from_xml(root_pars,".//*[@name='response functions']",self.vasp_vars)
        
        #atom info
        root_atom=root.find('atominfo')
        tmp=root_atom.find('atoms')
        self.vasp_vars['N_atoms']=tmp.text
        tmp=root_atom.find('types')
        self.vasp_vars['N_types']=tmp.text
        root_atom_set=root_atom.find(".//*[@name='atoms']/set")
        self.vasp_vars['N_atoms_set']=[]
        self.vasp_vars['N_atoms_type']=[]
        for at_ in root_atom_set:
            tm_=[]
            for siat_ in at_:
                tm_.append(siat_.text)
            self.vasp_vars['N_atoms_set'].append(tm_)
        root_atom_type=root_atom.find(".//*[@name='atomtypes']/set")
        for at_ in root_atom_type:
            tm_=[]
            for siat_ in at_:
                tm_.append(siat_.text)
            self.vasp_vars['N_atoms_type'].append(tm_)
        
        #structure (init)
        root_initstr=root.find(".//*[@name='initialpos']")
        initstr_pos=root_initstr.find(".//*[@name='positions']")
        self.vasp_vars['Init_pos']=[]
        for tmp in initstr_pos:
            self.vasp_vars['Init_pos'].append(tmp.text.split())
        initstr_prim=root_initstr.find("./crystal/*[@name='basis']")
        self.vasp_vars['Init_prim']=[]
        for tmp in initstr_prim:
            self.vasp_vars['Init_prim'].append(tmp.text.split())
        tmp=root_initstr.find("./crystal/*[@name='volume']")
        self.vasp_vars['Init_vol']=tmp.text
        initstr_rec=root_initstr.find("./crystal/*[@name='rec_basis']")
        self.vasp_vars['Init_rec']=[]
        for tmp in initstr_rec:
            self.vasp_vars['Init_rec'].append(tmp.text.split())
        initstr_selec=root_initstr.find(".//*[@name='selective']")
        self.vasp_vars['Init_selective']=[]
        if initstr_selec is not None:
            for selec_ in initstr_selec:
                self.vasp_vars['Init_selective'].append(selec_.text.split())
        initstr_velocity=root_initstr.find(".//*[@name='velocities']")
        self.vasp_vars['Init_velocities']=[]
        if initstr_velocity is not None:
            for vel_ in initstr_velocity:
                self.vasp_vars['Init_velocities'].append(vel_.text.split())
        
        #structure (final)
        root_finalstr=root.find(".//*[@name='finalpos']")
        finalstr_pos=root_finalstr.find(".//*[@name='positions']")
        self.vasp_vars['Final_pos']=[]
        for tmp in finalstr_pos:
            self.vasp_vars['Final_pos'].append(tmp.text.split())
        finalstr_prim=root_finalstr.find("./crystal/*[@name='basis']")
        self.vasp_vars['Final_prim']=[]
        for tmp in finalstr_prim:
            self.vasp_vars['Final_prim'].append(tmp.text.split())
        tmp=root_finalstr.find("./crystal/*[@name='volume']")
        self.vasp_vars['Final_vol']=tmp.text
        finalstr_rec=root_finalstr.find("./crystal/*[@name='rec_basis']")
        self.vasp_vars['Final_rec']=[]
        for tmp in finalstr_rec:
            self.vasp_vars['Final_rec'].append(tmp.text.split())
        finalstr_selec=root_finalstr.find(".//*[@name='selective']")
        self.vasp_vars['Final_selective']=[]
        if finalstr_selec is not None:
            for selec_ in finalstr_selec:
                self.vasp_vars['Final_selective'].append(selec_.text.split())
        finalstr_velocity=root_finalstr.find(".//*[@name='velocities']")
        self.vasp_vars['Final_velocities']=[]
        if finalstr_velocity is not None:
            for vel_ in finalstr_velocity:
                self.vasp_vars['Final_velocities'].append(vel_.text.split())
        
        #calculation
        root_cals=root.findall('calculation')
        root_cal_final=root_cals[len(root_cals)-1]
        self.vasp_load_calculation_xml(root_cal_final,self.vasp_vars)
        self.vasp_band_energies=self.vasp_vars['KPTS_BAND']
        self.vasp_band_occupations=self.vasp_vars['KPTS_OCCU']
        self.vasp_dos=self.vasp_vars['CAL_DOS']
        self.vasp_vars['Calculations']=[]
        for root_cal in root_cals:
            cal_={}
            self.vasp_load_calculation_xml(root_cal,cal_)
            self.vasp_vars['Calculations'].append(cal_)
        
        self.final_calculation=cal_
          
    def vasp_post_process_OUTCAR(self):
        file_outcar=open('OUTCAR','r')
        pre_tmpstr=''
        
        while True:
            tmpstr=file_outcar.readline()
            if tmpstr=='':
                break
            
            if tmpstr.find('total amount of memory used by VASP on root node')>=0:
                self.vasp_vars['Memory']=tmpstr.split()[10]
                tmpstr=file_outcar.readline()
                tmpstr=file_outcar.readline()
                str1=''
                for ind in range(6):
                    tmpstr=file_outcar.readline()
                    str1+=tmpstr+'\n'
                self.vasp_vars['VaspMemoryDetail']=str1
                
            if tmpstr.find('General timing and accounting informations for this job')>=0:
                tmpstr=file_outcar.readline()
                tmpstr=file_outcar.readline()
                tmpstr=file_outcar.readline()
                str1=''
                self.vasp_vars['CPUtime']=tmpstr.split()[5]
                str1+=tmpstr+'\n'
                str1+=file_outcar.readline()+'\n'
                str1+=file_outcar.readline()+'\n'
                str1+=file_outcar.readline()+'\n'
                str1+=file_outcar.readline()+'\n'
                tmpstr=file_outcar.readline()
                self.vasp_vars['MEMmax']=tmpstr.split()[4]
                str1+=tmpstr+'\n'
                str1+=file_outcar.readline()+'\n'
                str1+=file_outcar.readline()+'\n'
                str1+=file_outcar.readline()+'\n'
                str1+=file_outcar.readline()+'\n'
                str1+=file_outcar.readline()+'\n'
                
            pre_tmpstr=tmpstr
        file_outcar.close()
            
    def vasp_post_process_calculation(self,item,array=False,num=-1):
        tmp=[]
        if num==-1:
            for cal in self.vasp_vars['Calculations']:
                if not array:
                    tmp.append(cal[item])
                else:
                    for val in cal[item]:
                        tmp.append(val)
        else:
            cal=self.vasp_vars['Calculations'][num]
            if not array:
                tmp.append(cal[item])
            else:
                for val in cal[item]:
                    tmp.append(val)
        return tmp

# section for post processing and data output
        





