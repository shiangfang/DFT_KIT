# Density_Function_Theory - KIT  v1.0.0 
# August 2014
# Implementation for how to construct calculation for multiple parameters

import sys
import numpy as np
import os

def init_simulation(expect_num_parm):
    print('---------------------------------------------')
    print('     DFT_KIT program')
    print('---------------------------------------------')
    print('\n')
    print('Multiple process: arguments')
    print(sys.argv)

    # The only variable to be set : expect_num_parm
    # comments: meaning of each variable: (exclude the script name)
    # 0:
    # 1:
    # 2:

    input_num_parm=len(sys.argv)
    if input_num_parm < (expect_num_parm+1):
        print('ERROR: wrong number of input parameters for the program')
        exit()

    input_parm=[]
    for ind in range(1,expect_num_parm+1):
        input_parm.append(sys.argv[ind])
        
    opt_parm={}
    if input_num_parm > expect_num_parm+1:
        for ind in range(expect_num_parm+1,input_num_parm):
            tmp=sys.argv[ind]
            if tmp[0]=='-' and tmp.find('-') > -1:
                tmp=tmp[1:]
                tmp=tmp.split('=')
                opt_parm[tmp[0]]=tmp[1]
        

    print("Prepare program with input parameters:")
    print(input_parm)
    return [input_parm,opt_parm]







