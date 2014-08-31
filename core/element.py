# Density_Function_Theory - KIT  v1.0.0 
# August 2014
# Class for the period table elements

import numpy as np

magic_numbers=[2,10,18,36,54,86]
periodic_table=['H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe', 'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Uub', 'Uut', 'Uuq', 'Uup', 'Uuh', 'Uuo']

Element_A=[['H','Ne']]
Element_A.append(['Li','Na','K','Rb','Cs','Fr'])
Element_A.append(['Be','Mg','Ca','Sr','Ba','Ra'])
Element_A.append(['B','Al','Ga','In','Tl'])
Element_A.append(['C','Si','Ge','Sn','Pb'])
Element_A.append(['N','P','As','Sb','Bi'])
Element_A.append(['O','S','Se','Te','Po'])
Element_A.append(['F','Cl','Br','I','At'])
Element_A.append(['Ne','Ar','Kr','Xe','Rn'])

Element_B=[]
Element_B.append(['Sc','Y','Lu','Lr'])
Element_B.append(['Ti','Zr','Hf','Rf'])
Element_B.append(['V','Nb','Ta'])
Element_B.append(['Cr','Mo','W'])
Element_B.append(['Mn','Tc','Re'])
Element_B.append(['Fe','Ru','Os'])
Element_B.append(['Co','Rh','Ir'])
Element_B.append(['Ni','Pd','Pt'])
Element_B.append(['Cu','Ag','Au'])
Element_B.append(['Zn','Cd','Hg'])

Element_Lanthanides=['La','Ce','Pr','Nd','Pm','Sm','Eu','Gd','Tb','Dy','Ho','Er','Tm','Yb']
Element_Actinides=['Ac','Th','Pa','U','Np','Pu','Am','Cm','Bk','Cf','Es','Fm','Md','No']

def chem_number(ele_name):
    if ele_name in periodic_table:
        return periodic_table.index(ele_name)+1
    else:
        return -1
    
def chem_name(number):
    return periodic_table[number-1]


class element:
    def __init__(self,symbol=None,mass=None,nucZ=None,vale=None,**info):
        self.symbol=symbol
        self.mass=mass
        self.nucZ=nucZ
        self.vale=vale
        self.info={}
        
        #additional info can contain information for pseudopotential
        for ind_key in info:
            self.info[ind_key]=info[ind_key]


#define default objects for each elements

#from periodic table data
H_r=element('H', 1.00794,1,1)
He_r=element('He', 4.002602,2,2)
Li_r=element('Li', 6.941,3,3)
Be_r=element('Be', 9.012182,4,4)
B_r=element('B', 10.811,5,5)
C_r=element('C', 12.0107,6,6)
N_r=element('N', 14.0067,7,7)
O_r=element('O', 15.9994,8,8)
F_r=element('F', 18.9984032,9,9)
Ne_r=element('Ne', 20.1797,10,10)
Na_r=element('Na', 22.98976928,11,11)
Mg_r=element('Mg', 24.3050,12,12)
Al_r=element('Al', 26.9815386,13,13)
Si_r=element('Si', 28.0855,14,14)
P_r=element('P', 30.973762,15,15)
S_r=element('S', 32.065,16,16)
Cl_r=element('Cl', 35.453,17,17)
Ar_r=element('Ar', 39.948,18,18)
K_r=element('K', 39.0983,19,19)
Ca_r=element('Ca', 40.078,20,20)
Sc_r=element('Sc', 44.955912,21,21)
Ti_r=element('Ti', 47.867,22,22)
V_r=element('V', 50.9415,23,23)
Cr_r=element('Cr', 51.9961,24,24)
Mn_r=element('Mn', 54.938045,25,25)
Fe_r=element('Fe', 55.845,26,26)
Co_r=element('Co', 58.933195,27,27)
Ni_r=element('Ni', 58.6934,28,28)
Cu_r=element('Cu', 63.546,29,29)
Zn_r=element('Zn', 65.38,30,30)
Ga_r=element('Ga', 69.723,31,31)
Ge_r=element('Ge', 72.64,32,32)
As_r=element('As', 74.92160,33,33)
Se_r=element('Se', 78.96,34,34)
Br_r=element('Br', 79.904,35,35)
Kr_r=element('Kr', 83.798,36,36)
Rb_r=element('Rb', 85.4678,37,37)
Sr_r=element('Sr', 87.62,38,38)
Y_r=element('Y', 88.90585,39,39)
Zr_r=element('Zr', 91.224,40,40)
Nb_r=element('Nb', 92.90638,41,41)
Mo_r=element('Mo', 95.96,42,42)
Tc_r=element('Tc', [98],43,43)
Ru_r=element('Ru', 101.07,44,44)
Rh_r=element('Rh', 102.90550,45,45)
Pd_r=element('Pd', 106.42,46,46)
Ag_r=element('Ag', 107.8682,47,47)
Cd_r=element('Cd', 112.411,48,48)
In_r=element('In', 114.818,49,49)
Sn_r=element('Sn', 118.710,50,50)
Sb_r=element('Sb', 121.760,51,51)
Te_r=element('Te', 127.60,52,52)
I_r=element('I', 126.90447,53,53)
Xe_r=element('Xe', 131.293,54,54)
Cs_r=element('Cs', 132.9054519,55,55)
Ba_r=element('Ba', 137.327,56,56)
La_r=element('La', 138.90547,57,57)
Ce_r=element('Ce', 140.116,58,58)
Pr_r=element('Pr', 140.90765,59,59)
Nd_r=element('Nd', 144.242,60,60)
Pm_r=element('Pm', [145],61,61)
Sm_r=element('Sm', 150.36,62,62)
Eu_r=element('Eu', 151.964,63,63)
Gd_r=element('Gd', 157.25,64,64)
Tb_r=element('Tb', 158.92535,65,65)
Dy_r=element('Dy', 162.500,66,66)
Ho_r=element('Ho', 164.93032,67,67)
Er_r=element('Er', 167.259,68,68)
Tm_r=element('Tm', 168.93421,69,69)
Yb_r=element('Yb', 173.054,70,70)
Lu_r=element('Lu', 174.9668,71,71)
Hf_r=element('Hf', 178.49,72,72)
Ta_r=element('Ta', 180.94788,73,73)
W_r=element('W', 183.84,74,74)
Re_r=element('Re', 186.207,75,75)
Os_r=element('Os', 190.23,76,76)
Ir_r=element('Ir', 192.217,77,77)
Pt_r=element('Pt', 195.084,78,78)
Au_r=element('Au', 196.966569,79,79)
Hg_r=element('Hg', 200.59,80,80)
Tl_r=element('Tl', 204.3833,81,81)
Pb_r=element('Pb', 207.2,82,82)
Bi_r=element('Bi', 208.98040,83,83)


Po_r=element('Po',209,84,84)
At_r=element('At',210,85,85)
Rn_r=element('Rn',222,86,86)
Fr_r=element('Fr',223,87,87)
Ra_r=element('Ra',226.03,88,88)
Ac_r=element('Ac',227.03,89)
Th_r=element('Th',232.04,90)
Pa_r=element('Pa',231.04,91)
U_r=element('U',238.03,92,92)
Np_r=element('Np',237.05,93,93)
Pu_r=element('Pu',244,94,94)
Am_r=element('Am',243,95,95)    
Cm_r=element('Cm',247,96,96)
Bk_r=element('Bk',247,97,97)
Cf_r=element('Cf',251,98,98)
Es_r=element('Es',254,99,99)
Fm_r=element('Fm',257,100,100)  
Md_r=element('Md',258,101,101) 
No_r=element('No',259,102,102) 
Lr_r=element('Lr',260,103,103) 


#used for research


# Antimony
#Phys. Rev. 141, 562
Sb_exp_1={'lattice_constant':4.489,'angle':(57.0+14.0/60.0)*np.pi/180.0,'rhom_u':0.2336}
#Phys Rev. B 41,11827
Sb_exp_2={'lattice_constant':4.4898,'angle':(57.233)*np.pi/180.0,'rhom_u':0.23362}

Sb=element('Sb',121.760,51,5,vasp_pot='Sb',qes_pot='')
Sb_d=element('Sb',121.760,51,15,vasp_pot='Sb_d',qes_pot='')

# Bismuth
#experimental value at 4.2K cf. PRB 56, 6620. ->careful about the units a.u. vs Angstron
# Phys. Rev. 166, 643
Bi_exp_1={'lattice_constant':4.7212,'angle':(57.0+19.0/60.0)*np.pi/180.0,'rhom_u':0.23407}
#Phys Rev. B 41,11827
Bi_exp_2={'lattice_constant':4.7236,'angle':(57.35)*np.pi/180.0,'rhom_u':0.23407}

Bi_dft_1={'lattice_constant':4.7973,'angle':(53.0+56.0/60.0)*np.pi/180.0,'rhom_u':0.2348} #RMM-IIS
Bi_dft_2={'lattice_constant':4.7827,'angle':(56.0+17.0/60.0)*np.pi/180.0,'rhom_u':0.2351} #RMM-IIS SCAN
Bi_dft_3={'lattice_constant':4.8038,'angle':(53.0+36.0/60.0)*np.pi/180.0,'rhom_u':0.2347} #CONJ-GRAD


Bi_exp=element('Bi',208.9804,83,5,vasp_pot='Bi',qes_pot='Bi.UPF',rhom_length=4.7236,angle=1.0009,rhom_u=0.23407)
Bi_d=element('Bi',208.9804,83,15,vasp_pot='Bi_d',qes_pot='')

C=element('C',12.011,6,4,vasp_pot='C')


