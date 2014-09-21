#!/opt/apps/python/epd/7.3.2/bin/python

# Density_Function_Theory - KIT  v1.0.0 
# August 2014
# Implementation for how to construct calculation for multiple parameters
# this process will be system-dependent

# gen_scripts   (0|1 submit or not)  (name for the script) (number of copies)

import sys
import numpy as np
import os
import shutil

from DFT_KIT.core import env_parm
from DFT_KIT.interface import interface_script

[input_parm,opt_parm]=interface_script.init_simulation(3)
job_script=input_parm[0]
num_parm=int(input_parm[1])
job_submit=input_parm[2]
if job_submit=='0':
    job_submit=False
else:
    job_submit=True


root_dir=os.getcwd()+'/'
module_load=[]

if 'jm_cpu' in opt_parm:
    num_cpu=int(opt_parm['jm_cpu'])
else:
    num_cpu=1

if 'mem' in opt_parm:
    job_mem=int(opt_parm['mem'])
else:
    job_mem=2000 #in MB
    
if 'time' in opt_parm:
    job_time=opt_parm['time']
else:
    job_time="24:00:00"
    
if 'queue' in opt_parm:
    job_queue=opt_parm['queue']
else:
    job_queue="normal"
    
if 'jobname' in opt_parm:
    job_name=opt_parm['jobname']
else:
    job_name='DFT_KIT_JOB'
    
if 'dirprefix' in opt_parm:
    dir_prefix=opt_parm['dirprefix']
else:
    dir_prefix='DFT_JOB'
    
if 'batchname' in opt_parm:
    batch_fname=opt_parm['batchname']
else:
    batch_fname='DFT_KIT.batch'


for ind in range(0,num_parm):
    print('Start preparation/submit for job : ' + str(ind))
    
    if num_parm>1:
        task_dir=root_dir+dir_prefix+"_"+str(ind)+'/'
        os.mkdir(task_dir)
        os.chdir(task_dir)
        shutil.copy(root_dir+job_script, task_dir)
    else:
        pass #remain where we are now
    
    
    f_=open(batch_fname,'w')
    f_.write("#!/bin/bash\n")
    f_.write("#SBATCH -J "+job_name+"\n")
    f_.write("#SBATCH -o stdout.o%j \n")
    f_.write("#SBATCH -n "+ str(num_cpu)+"\n")
    f_.write("#SBATCH -p "+job_queue+"\n")
    f_.write("#SBATCH -t " +job_time+"\n\n")
    
    f_.write("# load the modules\n")
    for mod in module_load:
        f_.write("module load "+mod+"\n")
    
    f_.write("\n\n")
    
    #the main script!
    f_.write("# run the main script\n")
    f_.write("python  " + job_script + " "+ str(ind) +' ' +'-jm_cpu='+str(num_cpu))
    f_.write("\n\n")
    f_.close()

    if job_submit:
        os.system(env_parm.batch_cmd + " " + batch_fname)
    print('End preparation/submit for job : ' + str(ind))
    
    
    
