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
import copy
from scipy.interpolate import InterpolatedUnivariateSpline

from DFT_KIT.core import general_tool
from DFT_KIT.core import env_parm
from DFT_KIT.core import calculator
from DFT_KIT.core import physics

APE_generalities=['Title','CalculationMode','Units','UnitsOutput','UnitsInput','Verbose']
APE_hamiltonian=['WaveEquation','SpinMode','XCFunctional','XCCorrections']
APE_specie=['NuclearCharge','Orbitals']
APE_pp=['PPCalculationTolerance','PPOutputFileFormat','CoreCorrection','LLocal']
APE_pptest=['PPTests','PPTestSCF','PPTestOrbitals','PPTestAEDir','LogDerivativeRadius','LogDerivativeEnergyMax','LogDerivativeEnergyMin','LogDerivativeEnergyStep']
APE_mesh=['MeshType','MeshStartingPoint','MeshOutmostPoint','MeshNumberOfPoints','MeshDerivMethod','MeshFiniteDiffOrder']
APE_scf=['MaximumIter','ConvAbsDens','ConvRelDens','ConvAbsEnergy','ConvRelEnergy','SmearingFunction','MixingScheme','Mixing','MixNumberSteps']
APE_solver=['EigenSolverTolerance','ODEIntTolerance','ODESteppingFunction','ODEMaxSteps']


class calculator_APE(calculator.calculator):
    def __init__(self,post_process,dft_job,pp_element,scheme=0,**parms):
        calculator.calculator.__init__(self,post_process,dft_job,None,None,**parms)
        self.apply_scheme(scheme)
        if not post_process:
            self.pp_element=pp_element
        else:
            self.pp_element=None
        self.inp_name=''
        
    def generate_files(self):
        if self.inp_name=='':
            inpname=self.pp_element.symbol
        else:
            inpname=self.inp_name
        f_=open(inpname+'.inp','w')
        
        for ind_key in self.parms:
            if ind_key in APE_generalities:
                f_.write(ind_key+' = ' + str(self.parms[ind_key])+'\n')
        f_.write('\n')
        
        for ind_key in self.parms:
            if ind_key in APE_hamiltonian:
                f_.write(ind_key+' = ' + str(self.parms[ind_key])+'\n')
        f_.write('\n')
        
        #for ind_key in self.parms:
        #    if ind_key in APE_specie:
        #        f_.write(ind_key+' = ' + str(self.parms[ind_key])+'\n')
        #f_.write('\n')
        f_.write('NuclearCharge = '+str(self.pp_element.nucZ)+'\n')
        f_.write('%Orbitals\n')
        for tmp in self.parms['Orbitals']:
            f_.write(' ' +tmp+'\n')
        f_.write('%\n\n')
        
        f_.write('%PPComponents\n')
        for tmp in self.parms['PPComponents']:
            f_.write(' ' +tmp+'\n')
        f_.write('%\n\n')
        
        for ind_key in self.parms:
            if ind_key in APE_pp:
                f_.write(ind_key+' = ' + str(self.parms[ind_key])+'\n')
        f_.write('\n')
        
        for ind_key in self.parms:
            if ind_key in APE_pptest:
                f_.write(ind_key+' = ' + str(self.parms[ind_key])+'\n')
        f_.write('\n')
        
        for ind_key in self.parms:
            if ind_key in APE_mesh:
                f_.write(ind_key+' = ' + str(self.parms[ind_key])+'\n')
        f_.write('\n')
        
        for ind_key in self.parms:
            if ind_key in APE_scf:
                f_.write(ind_key+' = ' + str(self.parms[ind_key])+'\n')
        f_.write('\n')
        
        for ind_key in self.parms:
            if ind_key in APE_solver:
                f_.write(ind_key+' = ' + str(self.parms[ind_key])+'\n')
        f_.write('\n')
        
        f_.close()
        
        env_parm.run_ape(self.dft_job.job_mamanger_mode,inpname+'.inp',self.dft_job.opt_parm['cpu'])
        
        
        
    def run_main(self):
        self.dft_job.show('APE', 'APE does not have run main function')
    def apply_scheme(self,scheme):
        self.set_parm('Verbose', '30')
        self.set_parm('CalculationMode', 'ae + pp')
        
        if scheme==0:
            pass
        
        else:
            pass
        
    def post_process(self):
        self.dft_job.show('APE', 'APE does not have post process function')
    
    def post_process_read_ae(self,ae_name,skip_rows=0):
        fname='ae/'+ae_name
        tmp=np.loadtxt(fname,skiprows=skip_rows)
        return tmp
    
    def post_process_read_pp(self,pp_name,skip_rows=0):
        fname='pp/'+pp_name
        tmp=np.loadtxt(fname,skiprows=skip_rows)
        return tmp
        
        
        
        
LD1X_input_flags=['title','zed','atom','xmin','dx','rmax','beta','tr2','iswitch','nld','rlderiv','eminld','emaxld','deld','rpwe','rel','lsmall','noscf','lsd','dft','latt','isic','rytoev_fact','cau_fact','vdw','prefix','verbosity','config','rel_dist','write_coulomb']
LD1X_inputp_flags=['zval','pseudotype','upf_v1_format','file_pseudopw','file_recon','lloc','rcloc','nlcc','new_core_ps','rcore','tm','rho0','lpaw','which_augfun','rmatch_augfun','lsave_wfc','lgipaw_reconstruction','author','file_chi','file_beta','file_qvan','file_screen','file_core','file_wfcaegen','file_wfcncgen','file_wfcusgen']
        

        
class calculator_LD1X(calculator.calculator):
    def __init__(self,post_process,dft_job,pp_element,scheme=0,**parms):
        calculator.calculator.__init__(self,post_process,dft_job,None,None,**parms)
        self.apply_scheme(scheme)
        if not post_process:
            self.pp_element=pp_element
        else:
            self.pp_element=None
        self.inp_name=''
        self.upf_data={}
        self.pp_card=[]
        
    def generate_files(self):
        #if self.inp_name=='':
        #    inpname=self.pp_element.symbol
        #else:
        #    inpname=self.inp_name
        f_=open('LD1X.in','w')
        
        f_.write('&input\n')
        for ind_key in self.parms:
            if ind_key in LD1X_input_flags:
                f_.write(' '+ind_key+' = ' + str(self.parms[ind_key])+',\n')
        f_.write('/\n')
        
        f_.write('&inputp\n')
        for ind_key in self.parms:
            if ind_key in LD1X_inputp_flags:
                f_.write(' '+ind_key+' = ' + str(self.parms[ind_key])+',\n')
        f_.write('/\n')
        
        #pp card
        f_.write(str(len(self.pp_card))+'\n')
        for pp_item in self.pp_card:
            f_.write(pp_item+'\n')
            
        f_.close()
        
        
    
    def post_process_read_pswfc(self,pswfc_name='ld1ps.wfc',skip_rows=0):
        fname=pswfc_name
        tmp=np.loadtxt(fname,skiprows=skip_rows)
        return tmp
    
    def run_main(self):
        env_parm.run_ld1x(False,'LD1X.in')
    def apply_scheme(self,scheme):
        self.parms['iswitch']='3'
        self.parms['DFT']='PBE'
        self.parms['pseudotype']='2'
        self.parms['tm']='.true.'
    
    def post_process(self):
        self.dft_job.show('LD1X', 'LD1X does not have post process function')
    
    def vca_mixing(self,upf_data1,upf_data2,mixing_ratio):
        # mixratio*upf1+(1-mixratio)*upf2
        upf_data_mix={}
        
        #direct copy from upf1
        upf_data_mix['PP_HEADER']=[]
        for ind in range(0,len(upf_data1['PP_HEADER'])):
            tmpstr=upf_data1['PP_HEADER'][ind]
            if tmpstr.find('total_psenergy')>=0 or tmpstr.find('number_of_proj')>=0 or tmpstr.find('element')>=0 :
                pass
            else:
                upf_data_mix['PP_HEADER'].append(tmpstr)
        upf_data_mix['PP_HEADER'].append('             element="Xx"')
        upf_data_mix['PP_HEADER'].append('             number_of_proj="' +str(len(upf_data1['PP_NONLOCAL_DATA'])+len(upf_data2['PP_NONLOCAL_DATA']))+'"/>')  
        
        
        upf_data_mix['PP_MESH']=copy.copy(upf_data1['PP_MESH'])
        upf_data_mix['PP_R']=copy.copy(upf_data1['PP_R'])
        upf_data_mix['PP_R_DATA']=np.array(upf_data1['PP_R_DATA'])
        upf_data_mix['PP_RAB']=copy.copy(upf_data1['PP_RAB'])
        upf_data_mix['PP_RAB_DATA']=np.array(upf_data1['PP_RAB_DATA'])
        upf_data_mix['PP_LOCAL']=copy.copy(upf_data1['PP_LOCAL'])
        upf_data_mix['PP_RHOATOM']=copy.copy(upf_data1['PP_RHOATOM'])
        upf_data_mix['PP_NLCC']=copy.copy(upf_data1['PP_NLCC'])
        
        main_r=np.array(upf_data1['PP_R_DATA'])
        upf2_r=np.array(upf_data2['PP_R_DATA'])
        
        tmp1=np.array(upf_data1['PP_LOCAL_DATA'])
        tmp2=np.array(upf_data2['PP_LOCAL_DATA'])
        tmp3=InterpolatedUnivariateSpline(upf2_r,tmp2)
        upf_data_mix['PP_LOCAL_DATA']=mixing_ratio*tmp1+(1.0-mixing_ratio)*tmp3(main_r)
        
        tmp1=np.array(upf_data1['PP_RHOATOM_DATA'])
        tmp2=np.array(upf_data2['PP_RHOATOM_DATA'])
        tmp3=InterpolatedUnivariateSpline(upf2_r,tmp2)
        upf_data_mix['PP_RHOATOM_DATA']=mixing_ratio*tmp1+(1.0-mixing_ratio)*tmp3(main_r)
        
        upf_data_mix['PP_NONLOCAL']=[]
        upf_data_mix['PP_NONLOCAL_DATA']=[]
        indtmp=1
        tmpstr=upf_data1['PP_NONLOCAL'][0][0].split()
        tmptype=tmpstr[1]
        tmpsize=tmpstr[2]
        tmpcols=tmpstr[3]
        
        for ind,tmpbeta in enumerate(upf_data1['PP_NONLOCAL_DATA']):
            upf_data_mix['PP_NONLOCAL_DATA'].append(np.array(tmpbeta))
            tmpstr=upf_data1['PP_NONLOCAL'][ind][0].split()
            tmpang=tmpstr[6]
            upf_data_mix['PP_NONLOCAL'].append('    <PP_BETA.'+str(indtmp)+ ' '+tmptype+' '+tmpsize+' '+tmpcols+' index="'+str(indtmp)+'" '+tmpang+'>')
            indtmp=indtmp+1
            
        for ind,tmpbeta in enumerate(upf_data2['PP_NONLOCAL_DATA']):
            tmpint=InterpolatedUnivariateSpline(upf2_r,tmpbeta)
            upf_data_mix['PP_NONLOCAL_DATA'].append(np.array(tmpint(main_r)))
            tmpstr=upf_data2['PP_NONLOCAL'][ind][0].split()
            tmpang=tmpstr[6]
            upf_data_mix['PP_NONLOCAL'].append('    <PP_BETA.'+str(indtmp)+ ' '+tmptype+' '+tmpsize+' '+tmpcols+' index="'+str(indtmp)+'" '+tmpang+'>')
            indtmp=indtmp+1
            
        upf_data_mix['PP_DIJ']='    <PP_DIJ type="real" size="' +str(len(upf_data_mix['PP_NONLOCAL_DATA']))+ ' " columns="4">'
        
        tot_dim=(len(upf_data1['PP_NONLOCAL_DATA'])+len(upf_data2['PP_NONLOCAL_DATA']))
        tmp_mat=np.zeros((tot_dim,tot_dim))
        matdim1=len(upf_data1['PP_NONLOCAL_DATA'])
        tmpmat11=np.array(upf_data1['PP_DIJ_DATA']).reshape((matdim1,matdim1))
        tmpmat1=mixing_ratio*tmpmat11
        matdim2=len(upf_data2['PP_NONLOCAL_DATA'])
        tmpmat22=np.array(upf_data2['PP_DIJ_DATA']).reshape((matdim2,matdim2))
        tmpmat2=(1.0-mixing_ratio)*tmpmat22
        tmp_mat[0:len(upf_data1['PP_NONLOCAL_DATA']),0:len(upf_data1['PP_NONLOCAL_DATA'])]=tmpmat1[:,:]
        tmp_mat[len(upf_data1['PP_NONLOCAL_DATA']):tot_dim,len(upf_data1['PP_NONLOCAL_DATA']):tot_dim]=tmpmat2[:,:]
        
        upf_data_mix['PP_DIJ_DATA']=tmp_mat.reshape(tot_dim*tot_dim)
        
        
        tmpstr=upf_data1['PP_PSWFC'][0][0].split()
        tmptype=tmpstr[1]
        tmpsize=tmpstr[2]
        tmpcols=tmpstr[3]
        
        upf_data_mix['PP_PSWFC_DATA']=[]
        upf_data_mix['PP_PSWFC']=[]
        indtmp=1
        for ind, tmppswfc in enumerate(upf_data1['PP_PSWFC_DATA']):
            tmp1=np.array(upf_data1['PP_PSWFC_DATA'][ind])
            tmp2=np.array(upf_data2['PP_PSWFC_DATA'][ind])
            tmp3=InterpolatedUnivariateSpline(upf2_r,tmp2)
            upf_data_mix['PP_PSWFC_DATA'].append(mixing_ratio*tmp1+(1-mixing_ratio)*tmp3(main_r))
            tmpstrs=upf_data2['PP_PSWFC'][ind][0].split()
            tmpl=tmpstrs[6]
            tmpocc=tmpstrs[7]
            upf_data_mix['PP_PSWFC'].append('    <PP_CHI.'+str(indtmp)+ ' '+tmptype+' '+tmpsize+' '+tmpcols+' index="'+str(indtmp)+'" '+tmpl+' '+tmpocc+'>')
            indtmp=indtmp+1
        
        upf_data_mix['PP_NLCC_DATA']=[]
        if len(upf_data1['PP_NLCC_DATA'])>0:
            tmp1=np.array(upf_data1['PP_NLCC_DATA'])
            tmp2=np.array(upf_data2['PP_NLCC_DATA'])
            tmp3=InterpolatedUnivariateSpline(upf2_r,tmp2)
            upf_data_mix['PP_NLCC_DATA']=mixing_ratio*tmp1+(1-mixing_ratio)*tmp3(main_r)
        
        #spin_orb_coupling
        upf_data_mix['PP_SPIN_ORB']=[]
        for ind in range(0,len(upf_data1['PP_PSWFC_DATA'])):
            tmpstrs=upf_data1['PP_SPIN_ORB'][ind].split()
            upf_data_mix['PP_SPIN_ORB'].append('    '+tmpstrs[0]+' '+tmpstrs[1]+' '+tmpstrs[3]+' '+tmpstrs[4]+' '+tmpstrs[5]+' '+tmpstrs[6])
        
        indd=1
        for ind in range(len(upf_data1['PP_PSWFC_DATA']),len(upf_data1['PP_PSWFC_DATA'])+len(upf_data1['PP_NONLOCAL_DATA'])):
            upf_data_mix['PP_SPIN_ORB'].append(upf_data1['PP_SPIN_ORB'][ind])
            indd=indd+1
            
        for ind in range(len(upf_data2['PP_PSWFC_DATA']),len(upf_data2['PP_PSWFC_DATA'])+len(upf_data2['PP_NONLOCAL_DATA'])):
            tmpstrs=upf_data2['PP_SPIN_ORB'][ind].split()
            upf_data_mix['PP_SPIN_ORB'].append('    <PP_RELBETA.'+str(indd)+' index="'+str(indd)+'" '+tmpstrs[2]+' '+tmpstrs[3])
            indd=indd+1
        
        
        
        return upf_data_mix
    
    
    def read_UPF(self,fname):
        f_=open(fname,'r')
        upf_data={}
        tmp=f_.readline()
        if not tmp.find('UPF')>=0:
            self.dft_job.show_error('LD1X', 'Error in reading UPF file')
            return upf_data
        
        tmpstr=f_.readline()
        if tmpstr.find('<PP_INFO>')>=0:
            tmpstr=f_.readline()
            while not (tmpstr.find('</PP_INFO>')>=0):
                tmpstr=f_.readline()
            tmpstr=f_.readline()
            tmpstr=f_.readline()
            tmpstr=f_.readline()
            
        tmpstr=f_.readline()
        upf_data['PP_HEADER']=[]
        if tmpstr.find('<PP_HEADER')>=0:
            tmpstr=tmpstr[:-1]
            upf_data['PP_HEADER'].append(tmpstr)
            while True:
                tmpstr=f_.readline()
                tmpstr=tmpstr[:-1]
                upf_data['PP_HEADER'].append(tmpstr)
                if tmpstr.find('/>')>=0:
                    tmpstr=f_.readline()
                    break
                
        
        if tmpstr.find('<PP_MESH')>=0:
            tmpstr=tmpstr[:-1]
            tmpstr2=f_.readline()
            tmpstr2=tmpstr2[:-1]
            upf_data['PP_MESH']=[tmpstr,tmpstr2]
            
            tmpstr=f_.readline()
            tmpstr=tmpstr[:-1]
            upf_data['PP_R']=tmpstr
            
            upf_data['PP_R_DATA']=[]
            while True:
                tmpstr=f_.readline()
                if tmpstr.find('</PP_R>')>=0:
                    tmpstr=f_.readline()
                    break
                else:
                    tmpstrs=tmpstr.split()
                    for tmpitem in tmpstrs:
                        upf_data['PP_R_DATA'].append(float(tmpitem))
            
            tmpstr=tmpstr[:-1]
            upf_data['PP_RAB']=tmpstr
            upf_data['PP_RAB_DATA']=[]
            while True:
                tmpstr=f_.readline()
                if tmpstr.find('</PP_RAB>')>=0:
                    tmpstr=f_.readline() #/PP_MESH
                    tmpstr=f_.readline()
                    break
                else:
                    tmpstrs=tmpstr.split()
                    for tmpitem in tmpstrs:
                        upf_data['PP_RAB_DATA'].append(float(tmpitem))
            
            upf_data['PP_NLCC']=''
            upf_data['PP_NLCC_DATA']=[]
            if tmpstr.find('PP_NLCC')>=0:
                tmpstr=tmpstr[:-1]
                upf_data['PP_NLCC']=tmpstr
                while True:
                    tmpstr=f_.readline()
                    if tmpstr.find('</PP_NLCC>')>=0:
                        tmpstr=f_.readline() #PP_LOCAL
                        break
                    else:
                        tmpstrs=tmpstr.split()
                        for tmpitem in tmpstrs:
                            upf_data['PP_NLCC_DATA'].append(float(tmpitem))
            
            tmpstr=tmpstr[:-1]
            upf_data['PP_LOCAL']=tmpstr
            upf_data['PP_LOCAL_DATA']=[]
            while True:
                tmpstr=f_.readline()
                if tmpstr.find('</PP_LOCAL>')>=0:
                    tmpstr=f_.readline() #/PP_NONLOCAL
                    break
                else:
                    tmpstrs=tmpstr.split()
                    for tmpitem in tmpstrs:
                        upf_data['PP_LOCAL_DATA'].append(float(tmpitem))
            
            
            upf_data['PP_NONLOCAL_DATA']=[]
            upf_data['PP_NONLOCAL']=[]
            upf_data['PP_DIJ_DATA']=[]
            while True:
                tmpstr=f_.readline()
                if tmpstr.find('</PP_NONLOCAL>')>=0:
                    tmpstr=f_.readline()
                    break
                
                if tmpstr.find('<PP_BETA')>=0:
                    tmpstr2=f_.readline()
                    upf_data['PP_NONLOCAL'].append([tmpstr,tmpstr2])
                    tmpdata=[]
                    while True:
                        tmpstr=f_.readline()
                        if tmpstr.find('</PP_BETA')>=0:
                            upf_data['PP_NONLOCAL_DATA'].append(tmpdata)
                            break
                        
                        tmpstrs=tmpstr.split()
                        for tmpitem in tmpstrs:
                            tmpdata.append(float(tmpitem))
                            
                if tmpstr.find('<PP_DIJ')>=0:
                    tmpstr=tmpstr[:-1]
                    upf_data['PP_DIJ']=tmpstr
                    upf_data['PP_DIJ_DATA']=[]
                    while True:
                        tmpstr=f_.readline()
                        if tmpstr.find('</PP_DIJ>')>=0:
                            break
                        tmpstrs=tmpstr.split()
                        for tmpitem in tmpstrs:
                            upf_data['PP_DIJ_DATA'].append(float(tmpitem))
                    upf_data['PP_DIJ_DATA']=np.array(upf_data['PP_DIJ_DATA']).reshape((len(upf_data['PP_NONLOCAL_DATA']),len(upf_data['PP_NONLOCAL_DATA'])))

            if tmpstr.find('<PP_PSWFC>')>=0:
                upf_data['PP_PSWFC']=[]
                upf_data['PP_PSWFC_DATA']=[]
                while True:
                    tmpstr=f_.readline()
                    
                    if tmpstr.find('</PP_PSWFC>')>=0:
                        tmpstr=f_.readline()
                        break
                
                    if tmpstr.find('<PP_CHI')>=0:
                        tmpstr2=f_.readline()
                        upf_data['PP_PSWFC'].append([tmpstr,tmpstr2])
                        tmpdata=[]
                        while True:
                            tmpstr=f_.readline()
                            if tmpstr.find('</PP_CHI')>=0:
                                upf_data['PP_PSWFC_DATA'].append(tmpdata)
                                break
                        
                            tmpstrs=tmpstr.split()
                            for tmpitem in tmpstrs:
                                tmpdata.append(float(tmpitem))
                        
            if tmpstr.find('<PP_RHOATOM')>=0:
                tmpstr=tmpstr[:-1]
                upf_data['PP_RHOATOM']=tmpstr
                upf_data['PP_RHOATOM_DATA']=[]
                while True:
                    tmpstr=f_.readline()
                    if tmpstr.find('</PP_RHOATOM>')>=0:
                        tmpstr=f_.readline()
                        break
                    
                    tmpstrs=tmpstr.split()
                    for tmpitem in tmpstrs:
                        upf_data['PP_RHOATOM_DATA'].append(float(tmpitem))
                
            if tmpstr.find('<PP_SPIN_ORB>')>=0:
                upf_data['PP_SPIN_ORB']=[]
                while True:
                    tmpstr=f_.readline()
                    if tmpstr.find('</PP_SPIN_ORB>')>=0:
                        tmpstr=f_.readline() #/UPF
                        break
                    tmpstr=tmpstr[:-1]
                    upf_data['PP_SPIN_ORB'].append(tmpstr)
                    
            
            return upf_data #write the data
                        
            
            
            
    def write_UPF(self,upf_data,fname):
        f_=open(fname,'w')
        f_.write(' <UPF version="2.0.1">\n')
        f_.write('  <PP_INFO>\n')
        f_.write('  Virtual crystal approximation by DFT_KIT\n')
        f_.write('  by Shiang Fang\n')
        f_.write('  </PP_INFO>\n')
        
        for item_header in upf_data['PP_HEADER']:
            f_.write(item_header+'\n')
            
        f_.write(upf_data['PP_MESH'][0]+'\n')
        f_.write(upf_data['PP_MESH'][1]+'\n')
        
        f_.write(upf_data['PP_R']+'\n')
        tot_num_r=len(upf_data['PP_R_DATA'])
        ind=0
        for indtmp in range(tot_num_r/4):
            f_.write(' '+("%.15e" % upf_data['PP_R_DATA'][ind])+' '+("%.15e" % upf_data['PP_R_DATA'][ind+1])+' '+("%.15e" % upf_data['PP_R_DATA'][ind+2])+' '+("%.15e" % upf_data['PP_R_DATA'][ind+3])+'\n')
            ind=ind+4
        
        for indtmp in range(tot_num_r%4):
            f_.write(' '+("%.15e" % upf_data['PP_R_DATA'][ind]))
            ind=ind+1
        f_.write('\n')
        f_.write('    </PP_R>\n')
        
        f_.write(upf_data['PP_RAB']+'\n')
        tot_num_r=len(upf_data['PP_RAB_DATA'])
        ind=0
        for indtmp in range(tot_num_r/4):
            f_.write(' '+("%.15e" % upf_data['PP_RAB_DATA'][ind])+' '+("%.15e" % upf_data['PP_RAB_DATA'][ind+1])+' '+("%.15e" % upf_data['PP_RAB_DATA'][ind+2])+' '+("%.15e" % upf_data['PP_RAB_DATA'][ind+3])+'\n')
            ind=ind+4
        
        for indtmp in range(tot_num_r%4):
            f_.write(' '+("%.15e" % upf_data['PP_RAB_DATA'][ind]))
            ind=ind+1
        f_.write('\n')
        f_.write('    </PP_RAB>\n')
        f_.write('  </PP_MESH>\n')
        
        if len(upf_data['PP_NLCC_DATA'])>0:
            f_.write(upf_data['PP_NLCC']+'\n')
            tot_num_r=len(upf_data['PP_NLCC_DATA'])
            ind=0
            for indtmp in range(tot_num_r/4):
                f_.write(' '+("%.15e" % upf_data['PP_NLCC_DATA'][ind])+' '+("%.15e" % upf_data['PP_NLCC_DATA'][ind+1])+' '+("%.15e" % upf_data['PP_NLCC_DATA'][ind+2])+' '+("%.15e" % upf_data['PP_NLCC_DATA'][ind+3])+'\n')
                ind=ind+4
        
            for indtmp in range(tot_num_r%4):
                f_.write(' '+("%.15e" % upf_data['PP_NLCC_DATA'][ind]))
                ind=ind+1
            f_.write('\n')
            f_.write('  </PP_NLCC>\n')
        
        f_.write(upf_data['PP_LOCAL']+'\n')
        tot_num_r=len(upf_data['PP_LOCAL_DATA'])
        ind=0
        for indtmp in range(tot_num_r/4):
            f_.write(' '+("%.15e" % upf_data['PP_LOCAL_DATA'][ind])+' '+("%.15e" % upf_data['PP_LOCAL_DATA'][ind+1])+' '+("%.15e" % upf_data['PP_LOCAL_DATA'][ind+2])+' '+("%.15e" % upf_data['PP_LOCAL_DATA'][ind+3])+'\n')
            ind=ind+4
        
        for indtmp in range(tot_num_r%4):
            f_.write(' '+("%.15e" % upf_data['PP_LOCAL_DATA'][ind]))
            ind=ind+1
        f_.write('\n')
        f_.write('  </PP_LOCAL>\n')
        
        f_.write('  <PP_NONLOCAL>\n')
        #upf
        for ind, tmpstr in enumerate(upf_data['PP_NONLOCAL']):
            f_.write(upf_data['PP_NONLOCAL'][ind]+'\n')
            indd=0
            for indtmp in range(tot_num_r/4):
                f_.write(' '+("%.15e" % upf_data['PP_NONLOCAL_DATA'][ind][indd])+' '+("%.15e" % upf_data['PP_NONLOCAL_DATA'][ind][indd+1])+' '+("%.15e" % upf_data['PP_NONLOCAL_DATA'][ind][indd+2])+' '+("%.15e" % upf_data['PP_NONLOCAL_DATA'][ind][indd+3])+'\n')
                indd=indd+4
        
            for indtmp in range(tot_num_r%4):
                f_.write(' '+("%.15e" % upf_data['PP_NONLOCAL_DATA'][ind][indd]))
                indd=indd+1
            f_.write('\n')
            f_.write('    </PP_BETA.'+str(ind+1)+'>\n')
        
        tot_num=len(upf_data['PP_NONLOCAL_DATA'])*len(upf_data['PP_NONLOCAL_DATA'])
        f_.write('    <PP_DIJ type="real" size="'+str(tot_num)+'" columns="4">\n')
        ind=0
        for indtmp in range(tot_num/4):
            f_.write(' '+("%.15e" % upf_data['PP_DIJ_DATA'][ind])+' '+("%.15e" % upf_data['PP_DIJ_DATA'][ind+1])+' '+("%.15e" % upf_data['PP_DIJ_DATA'][ind+2])+' '+("%.15e" % upf_data['PP_DIJ_DATA'][ind+3])+'\n')
            ind=ind+4
        
        for indtmp in range(tot_num%4):
            f_.write(' '+("%.15e" % upf_data['PP_DIJ_DATA'][ind]))
            ind=ind+1
        f_.write('\n')
        f_.write('    </PP_DIJ>\n')    
        f_.write('  </PP_NONLOCAL>\n')
        
        f_.write('  <PP_PSWFC>\n')
        #upf
        for ind, tmpstr in enumerate(upf_data['PP_PSWFC']):
            f_.write(upf_data['PP_PSWFC'][ind]+'\n')
            indd=0
            for indtmp in range(tot_num_r/4):
                f_.write(' '+("%.15e" % upf_data['PP_PSWFC_DATA'][ind][indd])+' '+("%.15e" % upf_data['PP_PSWFC_DATA'][ind][indd+1])+' '+("%.15e" % upf_data['PP_PSWFC_DATA'][ind][indd+2])+' '+("%.15e" % upf_data['PP_PSWFC_DATA'][ind][indd+3])+'\n')
                indd=indd+4
        
            for indtmp in range(tot_num_r%4):
                f_.write(' '+("%.15e" % upf_data['PP_PSWFC_DATA'][ind][indd]))
                indd=indd+1
            f_.write('\n    </PP_CHI.'+str(ind+1)+'>\n')
        f_.write('  </PP_PSWFC>\n')
        

        f_.write(upf_data['PP_RHOATOM']+'\n')
        tot_num_r=len(upf_data['PP_RHOATOM_DATA'])
        ind=0
        for indtmp in range(tot_num_r/4):
            f_.write(' '+("%.15e" % upf_data['PP_RHOATOM_DATA'][ind])+' '+("%.15e" % upf_data['PP_RHOATOM_DATA'][ind+1])+' '+("%.15e" % upf_data['PP_RHOATOM_DATA'][ind+2])+' '+("%.15e" % upf_data['PP_RHOATOM_DATA'][ind+3])+'\n')
            ind=ind+4
        
        for indtmp in range(tot_num_r%4):
            f_.write(' '+("%.15e" % upf_data['PP_RHOATOM_DATA'][ind]))
            ind=ind+1
        f_.write('\n')
        f_.write('  </PP_RHOATOM>\n')
        
        
        f_.write('  <PP_SPIN_ORB>\n')
        for tmpstr in upf_data['PP_SPIN_ORB']:
            f_.write(tmpstr+'\n')
        f_.write('  </PP_SPIN_ORB>\n')
        f_.write(' </UPF>\n')



        