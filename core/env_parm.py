# Density_Function_Theory - KIT  v1.0.0 
# August 2014
# Class for the keeping system-dependent variables and run commands

import os

#General Environment
modules_load=[]
batch_cmd='sbatch '

#APE
def run_ape(jm_mode,f_in,num_cpu=1):
    os.system('/home1/03051/sfang/APE/bin/ape < ' +f_in)

#VASP
#vasp_std_path=''
#vasp_complex_path=''
#vasp_gamma_path=''
vasp_pseudo_dir='/home1/03051/sfang/Pseudo_Potential/VASP/'
def run_vasp_std(jm_mode,num_cpu=1):
    if jm_mode:
        cmd='ibrun /home1/03051/sfang/VASP/bin/vasp533_std_MDVDW'
    else:
        cmd='/home1/03051/sfang/VASP/bin/vasp533_std_MDVDW'
    print('run command: '+cmd+'\n')
    os.system(cmd)
    
def run_vasp_ncl(jm_mode,num_cpu=1):
    if jm_mode:
        cmd='ibrun /home1/03051/sfang/VASP/bin/vasp533_ncl_MDVDW'
    else:
        cmd='/home1/03051/sfang/VASP/bin/vasp533_ncl_MDVDW'
    print('run command: '+cmd+'\n')
    os.system(cmd)

def run_vasp_gamma(jm_mode,num_cpu=1):
    if jm_mode:
        cmd='ibrun /home1/03051/sfang/VASP/bin/vasp533_gamma_MDVDW'
    else:
        cmd='/home1/03051/sfang/VASP/bin/vasp533_gamma_MDVDW'
    print('run command: '+cmd+'\n')
    os.system(cmd)

#QESPRESSO
qespresso_pseudo_dir='/home1/03051/sfang/Pseudo_Potential/QESPRESSO/'
virtualxcmd='/opt/apps/intel13/mvapich2_1_9/espresso/5.0.3/upftools/virtual.x '
new_espresso_path='/home1/03051/sfang/espresso/bin/'
old_espresso_path='/opt/apps/intel13/mvapich2_1_9/espresso/5.0.3/bin/'


def run_qes_pwx(jm_mode,f_in,num_cpu=1):
    #os.system('pw.x <  ' + f_in + ' > ' + f_out)
    if jm_mode:
        os.system('ibrun pw.x <  ' + f_in+'.pwx.in' +' > ' + f_in +'.pwx.out')
    else:
        os.system('pw.x <  ' + f_in +'.pwx.in' +' > ' + f_in +'.pwx.out')
    
#pw2wannier90
def run_qes_pw2wan(jm_mode,f_in,num_cpu=1):
    os.system('~/wannier90/bin/pw2wannier90.x < ' +f_in)
    
#Wannier90
def run_wannier90(jm_mode,f_in,pp_mode,num_cpu=1):
    if pp_mode:
        os.system('~/wannier90/bin/wannier90.2.0.x -pp '+f_in)
    else:
        os.system('~/wannier90/bin/wannier90.2.0.x ' +f_in)
        
def run_post_wannier90(jm_mode,f_in,num_cpu=1):
    os.system('~/wannier90/bin/postw90.2.0.x ' +f_in)

#SIESTA
siesta_pseudo_dir='/home1/03051/sfang/Pseudo_Potential/SIESTA/'
def run_siesta(num_cpu=1):
    pass

