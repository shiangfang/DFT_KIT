#!/usr/bin/python

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

if len(sys.argv)< 4:
    print("ERROR: too few input parameter")
    exit()

job_script=sys.argv[2]
num_parm=int(sys.argv[3])

if sys.argv[1]=='0':
    job_submit=False
else:
    job_submit=True


root_dir=os.getcwd()+'/'
dir_prefix='task'
job_name='DFT_KIT_JOB'
num_cpu=2
job_queue="normal"
job_time="24:00:00"
module_load=[]
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
    f_.write("python  " + job_script + " "+ str(ind))
    f_.write("\n\n")
    f_.close()

    if job_submit:
        os.system(env_parm.batch_cmd + " " + batch_fname)
    print('End preparation/submit for job : ' + str(ind))
    
    
    
