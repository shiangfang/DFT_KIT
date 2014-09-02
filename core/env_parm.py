# Density_Function_Theory - KIT  v1.0.0 
# August 2014
# Class for the keeping system-dependent variables and run commands

import os

#General Environment
modules_load=[]
batch_cmd='sbatch '

#VASP
vasp_std_path=''
vasp_complex_path=''
vasp_gamma_path=''
vasp_pseudo_dir='/home1/03051/sfang/Pseudo_Potential/VASP/'
def run_vasp_std(jm_mode):
    if jm_mode:
        cmd='ibrun /home1/03051/sfang/VASP/bin/vasp533_std_MDVDW'
    else:
        cmd='/home1/03051/sfang/VASP/bin/vasp533_std_MDVDW'
    print('run command: '+cmd+'\n')
    os.system(cmd)
    
def run_vasp_ncl(jm_mode):
    if jm_mode:
        cmd='ibrun /home1/03051/sfang/VASP/bin/vasp533_ncl_MDVDW'
    else:
        cmd='/home1/03051/sfang/VASP/bin/vasp533_ncl_MDVDW'
    print('run command: '+cmd+'\n')
    os.system(cmd)

def run_vasp_gamma(jm_mode):
    if jm_mode:
        cmd='ibrun /home1/03051/sfang/VASP/bin/vasp533_gamma_MDVDW'
    else:
        cmd='/home1/03051/sfang/VASP/bin/vasp533_gamma_MDVDW'
    print('run command: '+cmd+'\n')
    os.system(cmd)

#QESPRESSO
qespresso_pseudo_dir='/home1/03051/sfang/Pseudo_Potential/QESPRESSO/'
virtualxcmd='/opt/apps/intel13/mvapich2_1_9/espresso/5.0.3/upftools/virtual.x '

def run_qes_pwx(f_in,f_out):
    os.system('pw.x <  ' + f_in + ' > ' + f_out)

#pw2wannier90
pw2wannier90cmd='pw2wannier90.x'

#WANNIER90
wannier90cmd='wannier90.x'


#SIESTA
siesta_pseudo_dir='/home1/03051/sfang/Pseudo_Potential/SIESTA/'
def run_siesta():
    pass



#obsolete

job_manager={'cpu':'16','mem':'30000','time':'100:00:00','queue':'general','email':''}
job_manager_write={'cpu':True,'mem':True,'time':True,'queue':True,'email':False}
job_sub_head='#!/bin/bash'
job_sub_name='#SBATCH -J '
job_manager_sub={'cpu':'#SBATCH -n ','mem':'#SBATCH --mem=','time':'#SBATCH -t ','queue':'#SBATCH -p ','email':'#SBATCH --mail-user='}
job_submit_cmd='sbatch '

vasp_job_precommand=['module load hpc/openmpi-intel-latest','module load math/fftw-3.2.2']
#vasp_location=[' /n/home09/sfang/VASP/vasp.5.3/vasp',' /n/home09/sfang/VASP/vasp.5.3/vasp.so']
vasp_location=[' /n/home09/sfang/bin/vasp',' /n/home09/sfang/bin/vasp.so',' /n/home09/sfang/bin/vasp.gamma',' /n/home09/sfang/bin/vasp.z']



#vasp options


#siesta options
#module load
siesta_job_precommand=['module load centos6/siesta-3.2-pl3-openmpi-1.7.2_intel-13.0.079']


#qespresso options
qespresso_job_precommand=['module load centos6/espresso-5.0.2_openmpi-1.7.2_intel-13.0.079']
