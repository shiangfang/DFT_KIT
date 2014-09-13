# Density_Function_Theory - KIT  v1.0.0 
# August 2014
# Class for the keeping system-dependent variables and run commands

import os

#General Environment
modules_load=[]
batch_cmd='sbatch '

#VASP
vasp_pseudo_dir='/n/home09/sfang/Pseudo_Potential/VASP/'
def run_vasp_std(jm_mode,num_cpu=1):
    if jm_mode:
        cmd='mpirun -np ' + str(num_cpu)+ ' /n/home09/sfang/VASP/bin/vasp'
    else:
        cmd='/n/home09/sfang/VASP/bin/vasp'
    print('run command: '+cmd+'\n')
    os.system(cmd)
    
def run_vasp_ncl(jm_mode,num_cpu=1):
    if jm_mode:
        cmd='mpirun -np ' + str(num_cpu)+ '  /n/home09/sfang/VASP/bin/vasp.so'
    else:
        cmd='/n/home09/sfang/VASP/bin/vasp.so'
    print('run command: '+cmd+'\n')
    os.system(cmd)

def run_vasp_gamma(jm_mode,num_cpu=1):
    if jm_mode:
        cmd='mpirun -np ' + str(num_cpu)+ ' /n/home09/sfang/VASP/bin/vasp.gamma'
    else:
        cmd='/n/home09/sfang/VASP/bin/vasp.gamma'
    print('run command: '+cmd+'\n')
    os.system(cmd)

#QESPRESSO
qespresso_pseudo_dir='/n/home09/sfang/Pseudo_Potential/QESPRESSO/'
virtualxcmd='/n/sw/centos6/espresso-5.0.2/upftools/virtual.x '

def run_qes_pwx(jm_mode,f_in,num_cpu=1):
    #os.system('pw.x <  ' + f_in + ' > ' + f_out)
    if jm_mode:
        os.system('mpirun -np ' + str(num_cpu)+ ' pw.x <  ' + f_in)
    else:
        os.system('pw.x <  ' + f_in)
    
#pw2wannier90
def run_qes_pw2wan(jm_mode,f_in,num_cpu=1):
    os.system('/n/home09/sfang/bin/pw2wannier90.x < ' +f_in)
    
#Wannier90
def run_wannier90(jm_mode,f_in,pp_mode,num_cpu=1):
    if pp_mode:
        os.system('/n/home09/sfang/bin/wannier90.2.0.x -pp '+f_in)
    else:
        os.system('/n/home09/sfang/bin/wannier90.2.0.x ' +f_in)
        
def run_post_wannier90(jm_mode,f_in,num_cpu=1):
    os.system('/n/home09/sfang/bin/postw90.2.0.x ' +f_in)

#SIESTA
siesta_pseudo_dir='/n/home09/sfang/Pseudo_Potential/SIESTA/'
def run_siesta(num_cpu=1):
    pass

