:while:# Density_Function_Theory - KIT  v1.0.0 
# August 2014
# Bismuth-Antimony research project 

import numpy as np
import os
import sys

from DFT_KIT.core import job, kpoint, element, crystal_3D
from DFT_KIT.apps import crystal_structure

#Structure for describing the element:
# crystal
#APE, VASP, 

#element.element:
# parameters for running VASP and Qespresso



# Antimony
#APE:
Sb_ape={'Title':'Bismuth','WaveEquation':'dirac','Orbitals':["\"Kr\"","4  |  2  |  10","5  |  0  |  2","5  |  1  |  3"],'PPComponents':["5 | 0 | 0.5  | 1.45 | ham","5 | 1 | 0.5  | 1.45 | ham","5 | 1 | 1.5  | 1.6 | ham"]}


#Phys. Rev. 141, 562
Sb_exp_1={'lattice_constant':4.489,'angle':(57.0+14.0/60.0)*np.pi/180.0,'rhom_u':0.2336}
#Phys Rev. B 41,11827
Sb_exp_2={'lattice_constant':4.4898,'angle':(57.233)*np.pi/180.0,'rhom_u':0.23362}

# crystal setting
Sb_exp=element.element('Sb',121.760,51,5,vasp_pot='Sb',qes_pot='Sb.UPF',rhom_length=4.489,angle=0.9989,rhom_u=0.2336)
Sb_d=element.element('Sb',121.760,51,15,vasp_pot='Sb_d',qes_pot='Sb_d.UPF')

# DFT setting
Sb_vasp_scf={}
Sb_vasp_nscf_soi={}
Sb_vasp_crystal_scf={'ISTART':'0','ENCUT':'250','EDIFF':'1E-6','ISMEAR':'-5','SIGMA':'0.2','LMAXMIX':'4','LREAL':'Auto'}
Sb_vasp_crystal_nscf_soi={'ISTART':'0','ICHARG':'11','ENCUT':'250','EDIFF':'1E-6','GGA_COMPAT':'.FALSE.','ISYM':'0','SAXIS':'0 0 1','LSORBIT':'.TRUE.','LMAXMIX':'4','MAGMOM':True,'LREAL':'Auto'}


Sb_qespresso_crystal_scf={'noncolin':'.true.','lspinorb':'.true.','ecutwfc':'25.0','occupations':"'smearing'",'smearing':"'marzari-vanderbilt'",'degauss':'0.005'}
Sb_qespresso_crystal_bands={'noncolin':'.true.','lspinorb':'.true.','ecutwfc':'25.0'}

Sb_qespresso_crystal_nscf_soi={}
Sb_qespresso_slab_scf={'mixing mode':'local-TF'}
Sb_qespresso_slab_nscf_soi={}

Sb_wannier90={'num_wann':'16','num_iter':'200','dis_num_iter':'500','dis_win_min':'-10','dis_win_max':'30','dis_froz_min':'-10','dis_froz_max':'10','length_unit':'Ang','spinors':'true','hr_plot':'true','write_xyz':'true','write_r2mn':'true'}    
Sb_pw2wan={'write_amn':'.true.','write_spn':'.true.','write_mmn':'.true.','write_unk':'.false.'}





# Bismuth

#APE
Bi_ape={'Title':'Bismuth','WaveEquation':'dirac','Orbitals':["\"Xe\"","4 | 3 | 14","5 | 2 | 10","6 | 0 | 2","6 | 1 | 3"],'PPComponents':["6 | 0 | 0.5  | 1.6 | ham","6 | 1 | 0.5  | 1.6 | ham","6 | 1 | 1.5  | 1.8 | ham"]}
 
#LD1X
Bi_ld1x={'title':"'Bi'",'zed':'83','rel':'2','config':"'[Xe] 4f14 5d10 6s2 6p3'",'lloc':'-1','file_pseudopw':"'Bi.UPF'",'dft':"'LDA'"}
 
#experimental value at 4.2K cf. PRB 56, 6620. ->careful about the units a.u. vs Angstron
# Phys. Rev. 166, 643
Bi_exp_1={'lattice_constant':4.7212,'angle':(57.0+19.0/60.0)*np.pi/180.0,'rhom_u':0.23407}
#Phys Rev. B 41,11827
Bi_exp_2={'lattice_constant':4.7236,'angle':(57.35)*np.pi/180.0,'rhom_u':0.23407}

Bi_dft_1={'lattice_constant':4.7973,'angle':(53.0+56.0/60.0)*np.pi/180.0,'rhom_u':0.2348} #RMM-IIS
Bi_dft_2={'lattice_constant':4.7827,'angle':(56.0+17.0/60.0)*np.pi/180.0,'rhom_u':0.2351} #RMM-IIS SCAN
Bi_dft_3={'lattice_constant':4.8038,'angle':(53.0+36.0/60.0)*np.pi/180.0,'rhom_u':0.2347} #CONJ-GRAD

# Crystal setting
Bi_exp=element.element('Bi',208.9804,83,5,vasp_pot='Bi',qes_pot='Bi.UPF',rhom_length=4.7236,angle=1.0009,rhom_u=0.23407)
Bi_d=element.element('Bi',208.9804,83,15,vasp_pot='Bi_d',qes_pot='Bi_d.UPF')

# DFT setting
Bi_vasp_slab_scf={'ISTART':'0','ENCUT':'250','EDIFF':'1E-4','ISMEAR':'-5','SIGMA':'0.2','LMAXMIX':'4','LREAL':'Auto','AMIN':'0.01'}
Bi_vasp_slab_nscf_soi={'ISTART':'0','ICHARG':'11','ENCUT':'250','EDIFF':'1E-4','GGA_COMPAT':'.FALSE.','ISYM':'0','SAXIS':'0 0 1','LSORBIT':'.TRUE.','LMAXMIX':'4','MAGMOM':True,'LREAL':'Auto','AMIN':'0.01'}
Bi_vasp_crystal_scf={'ISTART':'0','ENCUT':'250','EDIFF':'1E-6','ISMEAR':'-5','SIGMA':'0.2','LMAXMIX':'4','LREAL':'Auto'}
Bi_vasp_crystal_nscf_soi={'ISTART':'0','ICHARG':'11','ENCUT':'250','EDIFF':'1E-6','GGA_COMPAT':'.FALSE.','ISYM':'0','SAXIS':'0 0 1','LSORBIT':'.TRUE.','LMAXMIX':'4','MAGMOM':True,'LREAL':'Auto'}

Bi_qespresso_crystal_scf={'noncolin':'.true.','lspinorb':'.true.','ecutwfc':'25.0','occupations':"'smearing'",'smearing':"'marzari-vanderbilt'",'degauss':'0.005'}
Bi_qespresso_crystal_bands={'noncolin':'.true.','lspinorb':'.true.','ecutwfc':'25.0'}

Bi_qespresso_crystal_nscf_soi={}
Bi_qespresso_slab_scf={'mixing mode':'local-TF'}
Bi_qespresso_slab_nscf_soi={}

Bi_wannier90={'num_wann':'16','num_iter':'200','dis_num_iter':'500','dis_win_min':'-10','dis_win_max':'30','dis_froz_min':'-10','dis_froz_max':'10','length_unit':'Ang','spinors':'true','hr_plot':'true','write_xyz':'true','write_r2mn':'true'}    
Bi_pw2wan={'write_amn':'.true.','write_spn':'.true.','write_mmn':'.true.','write_unk':'.false.'}

#Alloy for Bi/Sb:
Bi_Sb_qespresso_crystal_scf={'noncolin':'.true.','lspinorb':'.true.','ecutwfc':'25.0','occupations':"'smearing'",'smearing':"'marzari-vanderbilt'",'degauss':'0.005'}

class a7_structure_hex(crystal_3D.hexagonal_3D):
    def __init__(self,element,length_unit=1.0,**parms):
        if 'rhom_length' in parms:
            rhom_length=parms['rhom_length']
            del parms['rhom_length']
        else:
            rhom_length=element.info['rhom_length']
            
        if 'angle' in parms:
            angle=parms['angle']
            del parms['angle']
        else:
            angle=element.info['angle']
        
        if 'rhom_u' in parms:
            rhom_u=parms['rhom_u']
            del parms['rhom_u']
        else:
            rhom_u=element.info['rhom_u']
            
        self.ref_crystal=crystal_3D.rhombohedral_3D(rhom_length,angle)
        a1=self.ref_crystal.get_prim_vec(0)
        a2=self.ref_crystal.get_prim_vec(1)
        a3=self.ref_crystal.get_prim_vec(2)
        d=(a1+a2+a3)*2.0*rhom_u
        tmpvec=a2-a1
        hex_a=np.sqrt(np.dot(tmpvec,tmpvec))
        
        crystal_3D.hexagonal_3D.__init__(hex_a,3.0*a1[2],length_unit)
        
        self.add_atom(element, np.array([0.0,0.0,0.0]), **parms)
        self.add_atom(element, np.array(d-a1), **parms)
        self.add_atom(element, np.array(a1), **parms)
        self.add_atom(element, np.array(d), **parms)
        self.add_atom(element, np.array(a1+a2), **parms)
        self.add_atom(element, np.array(a1+d), **parms)
        

class a7_structure(crystal_3D.rhombohedral_3D):
    def __init__(self,element,length_unit=1.0,**parms):
        if 'rhom_length' in parms:
            rhom_length=parms['rhom_length']
            del parms['rhom_length']
        else:
            rhom_length=element.info['rhom_length']
            
        if 'angle' in parms:
            angle=parms['angle']
            del parms['angle']
        else:
            angle=element.info['angle']
        
        if 'rhom_u' in parms:
            rhom_u=parms['rhom_u']
            del parms['rhom_u']
        else:
            rhom_u=element.info['rhom_u']
        
        crystal_3D.rhombohedral_3D.__init__(self,rhom_length,angle,length_unit)
        self.add_atom(element, np.array([0.0,0.0,0.0]), **parms)
        tmp_vec=(self.get_prim_vec(0)+self.get_prim_vec(1)+self.get_prim_vec(2))*2.0*rhom_u
        self.add_atom(element, np.array(tmp_vec), **parms)
    

        


class rhom_bilayer(crystal_3D.hexagonal_3D):
    def __init__(self,element,hex_c,length_unit=1.0,**parms):
        if 'rhom_length' in parms:
            rhom_length=parms['rhom_length']
            del parms['rhom_length']
        else:
            rhom_length=element.info['rhom_length']
            
        if 'angle' in parms:
            angle=parms['angle']
            del parms['angle']
        else:
            angle=element.info['angle']
        
        if 'rhom_u' in parms:
            rhom_u=parms['rhom_u']
            del parms['rhom_u']
        else:
            rhom_u=element.info['rhom_u']
            
        self.ref_crystal=crystal_3D.rhombohedral_3D(rhom_length,angle)
        tmpvec=self.ref_crystal.get_prim_vec(1)-self.ref_crystal.get_prim_vec(0)
        hex_a=np.sqrt(np.dot(tmpvec,tmpvec))
        
        crystal_3D.hexagonal_3D.__init__(hex_a,hex_c,length_unit)
        self.add_atom(element, np.array([0.0,0.0,0.0]))
        self.add_atom(element, (self.ref_crystal.get_prim_vec(0)+self.ref_crystal.get_prim_vec(1)+self.ref_crystal.get_prim_vec(2))*2.0*rhom_u-self.ref_crystal.get_prim_vec(0))
        
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
        
        self.set_prim_vec(0,ref_a2-ref_a1)
        self.set_prim_vec(1,ref_a3-ref_a1)
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
        
        
        
        

