

import numpy as np
import pickle
import os

from DFT_KIT.core import calculator, job
from DFT_KIT.calculator import QESPRESSO


start_ind=0
end_ind=50

base_dir='DFT_JOB'
sub_dir='dft_post_process'
fname1='dft_post_process_3'
fname2='dft_post_process_4'

fermi_level=[]
bands_LGT=[]

root_dir=os.getcwd()+'/'

for ind in range(start_ind,end_ind+1):
    os.chdir(root_dir)
    f1_=open(base_dir+'_'+str(ind)+'/'+sub_dir+'/'+fname1,'rb')
    tmp=pickle.load(f1_)
    fermi_level.append(tmp.qes_vars['fermi_energy'])
    
    f1_.close()
    
    os.chdir(root_dir+base_dir+'_'+str(ind)+'/task_2/')
    dft_job=job.job(subdir=False)
    dft_job.sys_info['qes_fname']='bi_sb_alloy_bands'
    dft_job.sys_info['qes_prefix']='bi_sb_vca_alloy'
    dft_calc=QESPRESSO.calculator_QESPRESSO(True,dft_job,None,None)
    dft_calc.post_process()
    
    
    #f2_=open(base_dir+'_'+str(ind)+'/'+sub_dir+'/'+fname2,'rb')
    #tmp=pickle.load(f2_)
    bands_LGT.append(dft_calc.qes_vars['eigenvalues'])
    
    
    #f2_.close()
    
f_=open('final_data','wb')
pickle.dump(fermi_level,f_)
pickle.dump(bands_LGT,f_)
f_.close()
    
