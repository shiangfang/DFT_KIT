# Density_Function_Theory - KIT  v1.0.0 
# August 2014
# Class for the nanowire geometry with rhombohedral crystal structure

import numpy as np

from DFT_KIT.core import general_tool
from DFT_KIT.core import crystal_3D
from DFT_KIT.apps import crystal_structure


class Rhom_trigonal_nanowire(crystal_3D.crystal_3D):
    def __init__(self,element,Lx,Ly,radius,length_unit=1.0,description='Trigonal Nanowire',**parms):
        crystal_3D.crystal_3D.__init__(self, length_unit, description)
        if 'rhom_length' in parms:
            rhom_length=parms['rhom_length']
        else:
            rhom_length=element.info['rhom_length']
        
        if 'angle' in parms:
            angle=parms['angle']
        else:
            angle=element.info['angle']
            
        if 'rhom_u' in parms:
            rhom_u=parms['rhom_u']
        else:
            rhom_u=element.info['rhom_u']
            
        if 'NMmax' in parms:
            NMmax=parms['NMmax']
            del parms['NMmax']
        else:
            NMmax=100
            
        self.ref_crystal=crystal_structure.a7_structure(element,length_unit,**parms)
        
        ref_a1=self.ref_crystal.get_prim_vec(0)
        ref_a2=self.ref_crystal.get_prim_vec(1)
        ref_a3=self.ref_crystal.get_prim_vec(2)
        hex_a1=(ref_a1-ref_a3)
        hex_a2=(ref_a1-ref_a2)
        height=ref_a1[2]
        vec_d=(ref_a1+ref_a2+ref_a3)*2.0*rhom_u
        
        self.Lx=Lx
        self.Ly=Ly
        self.Lz=3.0*height
        self.radius=radius
        
        self.set_prim_vec(0,[self.Lx,0.0,0.0])
        self.set_prim_vec(1,[0.0,self.Ly,0.0])
        self.set_prim_vec(2,[0.0,0.0,self.Lz])
        self.evaluate_basic()

        #eliminate numerical errors
        hex_a1[2]=0.0
        hex_a2[2]=0.0
        #translation vector
        self.hex_a1=hex_a1
        self.hex_a2=hex_a2
        
        origin_pt=np.array([0.0,0.0,0.0])
        #produce triangular lattice!
        tmp_points=[]
        layer1=[]
        layer2=[]
        layer3=[]
        all_layer=[]
        atom=[]
        
        center1=origin_pt
        center2=np.array([0.0,0.0,height])
        center3=np.array([0.0,0.0,2.0*height])
        main_shift=np.array([self.Lx*0.5,self.Ly*0.5,0.0])
        shift1=origin_pt
        shift2=(1.0/3.0)*(hex_a1+hex_a2)
        shift3=(1.0/3.0)*(2.0*hex_a1-hex_a2)
        for ind1 in range(-NMmax,NMmax+1):
            for ind2 in range(-NMmax,NMmax+1):
                tmp1=ind1*hex_a1+ind2*hex_a2
                tmp2=tmp1+center2+shift2
                tmp3=tmp1+center3+shift3
                if general_tool.vec_distance(tmp1, center1)<=radius:
                    tmp1=tmp1+main_shift
                    layer1.append(tmp1)
                    all_layer.append(tmp1)
                    atom_=self.add_atom(element, tmp1, **parms)
                    all_layer.append(tmp1+vec_d)
                    atom_=self.add_atom(element, tmp1+vec_d, **parms)
                    
                if general_tool.vec_distance(tmp2, center2)<=radius:
                    tmp2=tmp2+main_shift
                    layer2.append(tmp2)
                    all_layer.append(tmp2)
                    atom_=self.add_atom(element, tmp2, **parms)
                    all_layer.append(tmp2+vec_d)
                    atom_=self.add_atom(element, tmp2+vec_d, **parms)
                if general_tool.vec_distance(tmp3, center3)<=radius:
                    tmp3=tmp3+main_shift
                    layer3.append(tmp3)
                    all_layer.append(tmp3)
                    atom_=self.add_atom(element, tmp3, **parms)
                    all_layer.append(tmp3+vec_d-ref_a1-ref_a2-ref_a3)
                    atom_=self.add_atom(element, tmp3+vec_d-ref_a1-ref_a2-ref_a3, **parms)
        self.all_points=all_layer
        
        
        

