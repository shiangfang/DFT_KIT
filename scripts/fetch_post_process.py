

import numpy as np
import pickle

from DFT_KIT.core import calculator
from DFT_KIT.calculator import QESPRESSO


start_ind=0
end_ind=50

base_dir='DFT_JOB'
sub_dir='dft_post_process'
fname1='dft_post_process_3'
fname2='dft_post_process_4'

fermi_level=[]
bands_LGT=[]

for ind in range(start_ind,end_ind+1):
    f1_=open(base_dir+'_'+str(ind)+'/'+sub_dir+'/'+fname1,'rb')
    tmp=pickle.load(f1_)
    fermi_level.append(tmp.qes_vars['fermi_energy'])
    
    f1_.close()
    
    f2_=open(base_dir+'_'+str(ind)+'/'+sub_dir+'/'+fname2,'rb')
    tmp=pickle.load(f2_)
    bands_LGT.append(tmp.qes_vars['eigenvalues'])
    
    
    f2_.close()
    
f_=open('final_data','wb')
pickle.dump(fermi_level,f_)
pickle.dump(bands_LGT,f_)
f_.close()
    
