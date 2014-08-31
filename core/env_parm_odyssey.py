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
vasp_pseudo_dir='/n/home09/sfang/Pseudo_Potential/VASP/'
def run_vasp_std():
    os.system('ibrun /n/home09/sfang/bin/vasp')
    
def run_vasp_ncl():
    os.system('ibrun /n/home09/sfang/bin/vasp.so')

def run_vasp_gamma():
    os.system('ibrun /n/home09/sfang/bin/vasp.gamma')

#QESPRESSO
qespresso_pseudo_dir='/n/home09/sfang/Pseudo_Potential/QESPRESSO/'
def run_qespresso(f_in,f_out):
    os.system('pw.x <  ' + f_in + ' > ' + f_out)
#WANNIER90

#SIESTA
siesta_pseudo_dir='/n/home09/sfang/Pseudo_Potential/SIESTA/'
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
