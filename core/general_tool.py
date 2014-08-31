# Density_Function_Theory - KIT  v1.0.0 
# August 2014
# Class for the keeping system-dependent variables and run commands

import numpy as np
import string

class segments:
    def __init__(self,num_,sets_):
        self.ordering=np.array(range(0,num_*sets_))
        self.subnum=num_
        self.sets=sets_
        self.tmp1=np.zeros(num_)
        self.tmp2=np.zeros(num_)
        self.tmp0=np.zeros(num_)
    def get_ordering(self):
        return self.ordering
    def print_ordering(self):
        print(self.ordering)
    def swap_groups(self,group1,group2):
        self.tmp1[:]=self.ordering[group1*self.subnum:(group1+1)*self.subnum]
        self.tmp2[:]=self.ordering[group2*self.subnum:(group2+1)*self.subnum]
        self.ordering[group1*self.subnum:(group1+1)*self.subnum]=self.tmp2[:]
        self.ordering[group2*self.subnum:(group2+1)*self.subnum]=self.tmp1[:]
    def invert_group(self,group_):
        t1=range(group_*self.subnum,(group_+1)*self.subnum)
        t2=range(group_*self.subnum,(group_+1)*self.subnum)
        t2=t1[::-1]
        self.ordering[t1]=self.ordering[t2]

def bool_to_str(bool_):
    if bool_:
        return 'T'
    else:
        return 'F'
    
def convert_vector(vec):
    if len(vec)>0:
        length1=len(vec)
        tmp=np.zeros(length1)
        for ind1 in range(length1):
                tmp[ind1]=float(vec[ind1])
        return tmp
    else:
        return []    

def convert_array_2d(arr):
    if len(arr)>0:
        length1=len(arr)
        length2=len(arr[0])
        tmp=np.zeros((length1,length2))
        for ind1 in range(length1):
            for ind2 in range(length2):
                tmp[ind1,ind2]=float(arr[ind1][ind2])
        return tmp
    else:
        return []
    

#from vec_tool
import numpy as np
import string

#basic vector operations
def vec_to_str(vec):
    tmp=[]
    for comp in vec:
        tmp.append(str(comp))
    return ' '.join(tmp)

def get_unitvec(vec):
    vec=np.array(vec)
    return vec/vec_length(vec)


    
def vec_length(vec):
    return np.sqrt(np.sum(vec**2))

def vec_distance(vec1,vec2):
    return np.sqrt(np.sum((vec1-vec2)**2))

#rotation operations
def generate_rotation_matrix():
    pass

#special matrices(rotation, etc)

def rot_x(theta):
    Rmat=np.zeros([3,3])
    Rmat[0,0]=1
    Rmat[1,1]=np.cos(theta)
    Rmat[1,2]=-np.sin(theta)
    Rmat[2,1]=np.sin(theta)
    Rmat[2,2]=np.cos(theta)
    return Rmat
        
def rot_y(theta):
    Rmat=np.zeros([3,3])
    Rmat[1,1]=1
    Rmat[0,0]=np.cos(theta)
    Rmat[0,2]=-np.sin(theta)
    Rmat[2,0]=np.sin(theta)
    Rmat[2,2]=np.cos(theta)
    return Rmat
    
def rot_z(theta):
    Rmat=np.zeros([3,3])
    Rmat[2,2]=1
    Rmat[0,0]=np.cos(theta)
    Rmat[0,1]=-np.sin(theta)
    Rmat[1,0]=np.sin(theta)
    Rmat[1,1]=np.cos(theta)
    return Rmat

def rotation_matrix(alpha,beta,gamma):
    return rot_y(gamma) * (rot_x(beta) * rot_y(alpha))



def get_parm(ind_key,**parms):
    if ind_key in parms:
        val=parms[ind_key]
    else:
        val=''
    return val




