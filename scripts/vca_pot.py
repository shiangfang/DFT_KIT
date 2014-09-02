# script to mix the pseudo potential with the tool virtual.x to take care of spinor part in the potential (addinfo)

import os
from DFT_KIT.core import env_parm

ps_pot1='Bi.UPF'
ps_pot2='Sb.UPF'
shell_pot1=3
shell_pot2=3
betas_pot1=3
betas_pot2=3
num_alloy=51
min_alloy=1.0
max_alloy=0.0

mix_add_info=[' <PP_ADDINFO>']

pot1_add_shell=[]
pot1_add_beta=[]
pot1_add_mesh=''
f_=open(ps_pot1,'r')
while True:
    line=f_.readline()
    if not line: break
    if line.rfind('<ADDINFO>') > -1: 
        for ind in range(0,shell_pot1):
            tmp=f_.readline()
            pot1_add_shell.append(tmp)
            mix_add_info.append(tmp)
        for ind in range(0,betas_pot1):
            f_.readline()
            pot1_add_beta.append(tmp)
            mix_add_info.append(tmp)
        pot1_add_mesh=f_.readline()
        f_.readline()
f_.close()

pot2_add_shell=[]
pot2_add_beta=[]
pot2_add_mesh=''
f_=open(ps_pot2,'r')
while True:
    line=f_.readline()
    if not line: break
    if line.rfind('<ADDINFO>') > -1: 
        for ind in range(0,shell_pot1):
            pot2_add_shell.append(f_.readline())
        for ind in range(0,betas_pot1):
            tmp=f_.readline()
            pot2_add_beta.append(tmp)
            mix_add_info.append(tmp)
        pot2_add_mesh=f_.readline()
        f_.readline()
f_.close()

mix_add_info.append(pot1_add_mesh)
mix_add_info.append(' </PP_ADDINFO>')

for ind in range(0,num_alloy):
    alloy_ind=min_alloy+(ind)*(max_alloy-min_alloy)/(num_alloy-1)
    print(alloy_ind)
    f = open('virtualinput', 'w')
    f.write(ps_pot1+'\n'+ps_pot2+'\n' + str(alloy_ind))
    f.close()
    os.system(env_parm.virtualxcmd + ' < virtualinput')
    #os.system('cat NewPseudo.UPF ADDINFO.UPF > bi_sb_alloy_LDA_' + str(ind) + '.UPF')
    f_=open('NewPseudo.UPF','a')
    for line in mix_add_info:
        f_.write(line)
    f_.close()
    

os.system('rm virtualinput')
os.system('rm NewPseudo.UPF')