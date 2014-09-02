import os
import subprocess

#subprocess.call("exit 1", shell=True)

virtualcmd='/opt/apps/intel13/mvapich2_1_9/espresso/5.0.3/upftools/virtual.x '

num_alloy=51
min_alloy=1.0
max_alloy=0.0
for ind in range(0,num_alloy):
   alloy_ind=min_alloy+(ind)*(max_alloy-min_alloy)/(num_alloy-1)
   print(alloy_ind)
   f = open('virtualinput', 'w')
   f.write('Bi.UPF\nSb.UPF\n' + str(alloy_ind))
   f.close()
   os.system(virtualcmd + ' < virtualinput')
   os.system('cat NewPseudo.UPF ADDINFO.UPF > bi_sb_alloy_LDA_' + str(ind) + '.UPF')


os.system('rm virtualinput')
os.system('rm NewPseudo.UPF')


