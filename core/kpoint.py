# Density_Function_Theory - KIT  v1.0.0 
# August 2014
# Class for controling k grid and band scan

import numpy as np

class kpoint:
    def __init__(self,mode=0):
        # mode 0 : grid
        # mode 1 : scan of k lines
        # mode 2 : specify k points and weights
        self.kmode=mode
        #mode 0
        #type 0: M-Horst, type 1: Gamma type
        self.kgridtype=0
        self.kgrid=np.array([10,10,10])
        self.kgrid_shift=np.array([0.0,0.0,0.0])
        self.rec_coordinate=True
        
        #mode 1
        self.num_kscan=10
        self.kscan=[]
        
        #mode 2
        self.klist=[]

    #mode 0


    #mode 1
    def add_kscan_point(self,kpoint):
        self.kscan.append(kpoint)
    def set_num_kscan(self,num):
        self.num_kscan=num
    def set_grid_mode(self,grid_):
        self.kmode=0
        self.kgrid=grid_    
    
    def set_scan_mode(self,num,kpoints):
        self.kmode=1
        self.num_kscan=num
        self.kscan=[]
        for kpt in kpoints:
            self.add_kscan_point(kpt)

    #mode 2
    def add_klist_point(self,kpoint):
        # k position and weight
        self.kline.append(kpoint)
        
    def generate_kgrid(self,write_weight):
        return generate_kgrid(self.kgrid[0],self.kgrid[1],self.kgrid[2],write_weight)
        
def generate_kgrid(n1,n2,n3,write_weight=True):
    n_tot=n1*n2*n3
    avg_weight=1.0/float(n_tot)
    n1s=np.linspace(0,1,n1+1)
    n1s=n1s[0:n1]
    n2s=np.linspace(0,1,n2+1)
    n2s=n2s[0:n2]
    n3s=np.linspace(0,1,n3+1)
    n3s=n3s[0:n3]

    klist=[]
    for ind1 in range(0,n1):
        for ind2 in range(0,n2):
            for ind3 in range(0,n3):
                if not write_weight:
                    klist.append(np.array([n1s[ind1],n2s[ind2],n3s[ind3]]))
                else:
                    klist.append(np.array([n1s[ind1],n2s[ind2],n3s[ind3],avg_weight]))
    return klist


