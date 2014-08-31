# Density_Function_Theory - KIT  v1.0.0 
# August 2014
# Class for the slab geometry with surface 111 
import numpy as np

from DFT_KIT.core import crystal_3D
from DFT_KIT.apps import crystal_structure

class Rhom_trigonal_surface(crystal_3D.crystal_3D):
    def __init__(self,element,num_layers,vacuum_layers,length_unit=1.0,description='Trigonal Surface',**parms):
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
        
        self.ref_crystal=crystal_structure.a7_structure(element,length_unit,**parms)
        ref_a1=self.ref_crystal.get_prim_vec(0)
        ref_a2=self.ref_crystal.get_prim_vec(1)
        ref_a3=self.ref_crystal.get_prim_vec(2)
        vec_d=(ref_a1+ref_a2+ref_a3)*2.0*rhom_u
        
        self.num_layers=num_layers
        self.vacuum_layers=vacuum_layers
        self.rhom_constant=rhom_length
        self.angle=angle
        self.rhom_u=rhom_u
        
        self.set_prim_vec(0,ref_a1-ref_a2)
        self.set_prim_vec(1,ref_a1-ref_a3)
        self.set_prim_vec(2,(ref_a1+ref_a2+ref_a3)*(num_layers+vacuum_layers))
        self.evaluate_basic()
        
        deltaz=(ref_a1+ref_a2+ref_a3)
        delta_vac=0.5*vacuum_layers*deltaz
        vecs=[]
        vecs.append(np.array([0.0,0.0,0.0]))
        vecs.append(vec_d-ref_a1)
        vecs.append(ref_a1)
        vecs.append(vec_d)
        vecs.append(ref_a2+ref_a3)
        vecs.append(ref_a1+vec_d)
        
        for ind in range(0,num_layers):
            for ind2 in range(0,6):
                atom_=self.add_atom(element, delta_vac+deltaz*ind+vecs[ind2], **parms)
                

class Rhom_parallel_trigonal_surface(crystal_3D.crystal_3D):
    def __init__(self,element,num_layers,vacuum_layers,length_unit=1.0,description='Trigonal Surface',**parms):
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
        
        self.ref_crystal=crystal_structure.a7_structure(element,length_unit,**parms)
        ref_a1=self.ref_crystal.get_prim_vec(0)
        ref_a2=self.ref_crystal.get_prim_vec(1)
        ref_a3=self.ref_crystal.get_prim_vec(2)
        vec_d=(ref_a1+ref_a2+ref_a3)*2.0*rhom_u
        

        vacuum_thickness=vacuum_layers*2/np.sqrt(3)
        
        delta_x=ref_a1-ref_a3
        delta_vac=np.array([(self.vacuum_thickness)*0.5*np.sqrt(3),(self.vacuum_thickness)*0.5,0.0])
        
        self.set_prim_vec(0,[(self.num_layers*rhom_length+self.vacuum_thickness)*0.5,(self.num_layers*rhom_length+self.vacuum_thickness)*0.5*np.sqrt(3),0.0])
        self.set_prim_vec(1,ref_a2-ref_a3)
        self.set_prim_vec(2,[0.0,0.0,3.0*ref_a3[2]])
        self.evaluate_basic()
        
        vecs=[]
        vecs.append(np.array([0.0,0.0,0.0]))
        vecs.append(np.array([0,0,6.0*rhom_u*ref_a1[2]]))
        vecs.append(np.array(ref_a1))
        vecs.append(np.array([ref_a1[0],ref_a1[1],ref_a1[2]+6.0*rhom_u*ref_a1[2]]))
        vecs.append(np.array(ref_a2+ref_a3))
        vecs.append(np.array([ref_a2[0]+ref_a3[0],ref_a2[1]+ref_a3[1],ref_a2[2]+ref_a3[2]+6.0*rhom_u*ref_a1[2]-ref_a1[2]*3.0]))
        
        for ind in range(0,num_layers):
            for ind2 in range(0,6):
                atom_=self.add_atom(element, delta_vac+delta_x*ind+vecs[ind2], **parms)
           


        
                
