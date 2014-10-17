# Density_Function_Theory - KIT  v1.0.0 
# August 2014
# Class for the keeping system-dependent variables and run commands

import os

#General Environment
modules_load=[]
batch_cmd='sbatch '

#APE
def run_ape(jm_mode,f_in,num_cpu=1):
    os.system('/n/home09/sfang/APE/bin/ape < ' +f_in)


#ELK
elk_sppath="'../../species/'"
def run_elk(jm_mode,f_in,num_cpu=1):
    os.system('/n/home09/sfang/elk-2.3.22/bin/elk')

def run_spacegroup(jm_mode,f_in,num_cpu=1):
    os.system('/n/home09/sfang/elk-2.3.22/bin/spacegroup')

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
espresso51_path='/n/home09/sfang/espresso-5.1/bin/'
espresso50_path='/n/sw/centos6/espresso-5.0.2/bin/'
espresso_path=espresso50_path

def run_qes_pwx(jm_mode,f_in,num_cpu=1):
    #os.system('pw.x <  ' + f_in + ' > ' + f_out)
    if jm_mode:
        os.system('mpirun -np ' + str(num_cpu)+ ' '+ espresso_path +'pw.x <  ' + f_in+'.pwx.in' +' > ' + f_in +'.pwx.out')
    else:
        os.system(espresso_path+'pw.x <  ' + f_in+'.pwx.in' +' > ' + f_in +'.pwx.out')

#LD1X
def run_ld1x(jm_mode,f_in,num_cpu=1):
    os.system(espresso_path+'ld1.x < ' +f_in + ' > ' +f_in +'.out')
    
#pw2wannier90
def run_qes_pw2wan(jm_mode,f_in,num_cpu=1):
    os.system('/n/home09/sfang/wannier90/bin/pw2wannier90.x < ' +f_in +'.pw2wan.in') 
    
#Wannier90
def run_wannier90(jm_mode,f_in,pp_mode,num_cpu=1):
    if pp_mode:
        os.system('/n/home09/sfang/wannier90/bin/wannier90.x -pp '+f_in)
    else:
        os.system('/n/home09/sfang/wannier90/bin/wannier90.x ' +f_in)
        
def run_post_wannier90(jm_mode,f_in,num_cpu=1):
    os.system('/n/home09/sfang/wannier90/bin/postw90.x ' +f_in)

#SIESTA
siesta_pseudo_dir='/n/home09/sfang/Pseudo_Potential/SIESTA/'
def run_siesta(num_cpu=1):
    pass

