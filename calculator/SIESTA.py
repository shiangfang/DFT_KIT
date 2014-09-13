# Density_Function_Theory - KIT  v1.0.0 
# August 2014
# Class for calculation with VASP

import os
import shutil
import pickle
import string
import numpy as np
import sys
import string
import xml.etree.ElementTree as ET

from DFT_KIT.core import general_tool
from DFT_KIT.core import env_parm
from DFT_KIT.core import calculator

SIESTA_flags=['SystemName','SystemLabel','WriteMullikenPop','PAO.BasisType ','PAO.EnergyShift',
'PAO.BasisSize','SpinPolarized','MeshCutoff','MaxSCFIterations','DM.MixingWeight','DM.Tolerance',
'DM.NumberPulay','DM.UseSaveDM ','NeglNonOverlapInt','SolutionMethod','ElectronicTemperature',
'MD.TypeOfRun','MD.NumCGsteps','MD.MaxCGDispl','MD.MaxForceTol']

SIE_flags='AllocReportLevel,\
AtomCoorFormatOut,\
AtomicCoordinatesAndAtomicSpecies,\
AtomicCoordinatesFormat,\
AtomicCoordinatesOrigin,\
AtomicMass,\
BandLines,\
BandLinesScale,\
BandPoints,\
BasisPressure,\
BlockSize,\
Blocksize,\
BornCharge,\
ChangeKgridInMD,\
COOP.Write,\
Diag.AllInOne,\
Diag.DivideAndConquer,\
Diag.Memory,\
Diag.NoExpert,\
Diag.ParallelOverK,\
Diag.PreRotate,\
Diag.Use2D,\
DirectPhi,\
DM.AllowExtrapolation,\
DM.AllowReuse,\
DM.Broyden.Cycle.On.Maxit,\
DM.Broyden.Variable.Weight,\
DM.EnergyTolerance,\
DM.FormattedFiles,\
DM.FormattedInput,\
DM.FormattedOutput,\
DM.Harris.Tolerance,\
DM.InitSpin,\
DM.InitSpinAF,\
DM.KickMixingWeight,\
DM.MixingWeight,\
DM.MixSCF1,\
DM.NumberBroyden,\
DM.NumberKick,\
DM.NumberPulay,\
DM.Pulay.Avoid.First.After.Kick,\
DM.PulayOnFile,\
DM.Require.Energy.Convergence,\
DM.Require.Harris.Convergence,\
DM.Tolerance,\
DM.UseSaveDM,\
EggboxRemove,\
EggboxScale,\
ElectronicTemperature,\
ExternalElectricField,\
FilterCutoff,\
FilterTol,\
FixAuxiliaryCell,\
FixSpin,\
GeometryConstraints,\
GridCellSampling,\
Harris_functional,\
kgrid_cutoff,\
kgrid_Monkhorst_Pack,\
LatticeConstant, 30
LatticeParameters, 30
LatticeVectors
LocalDensityOfStates,
LongOutput
MaxBondDistance, 39
MaxSCFIterations, 43
MD.AnnealOption, 88
119MD.Broyden.Cycle.On.Maxit, 84
MD.Broyden.History.Steps, 84
MD.Broyden.Initial.Inverse.Jacobian, 84
MD.BulkModulus, 88
MD.ConstantVolume, 82
MD.FCDispl, 92
MD.FCfirst, 92
MD.FClast, 92
MD.FinalTimeStep, 87
MD.FIRE.TimeStep, 85
MD.FireQuench, 85
MD.InitialTemperature, 87
MD.InitialTimeStep, 87
MD.LengthTimeStep, 87
MD.MaxCGDispl, 83
MD.MaxForceTol, 82
MD.MaxStressTol, 82
MD.NoseMass, 87
MD.NumCGsteps, 83
MD.ParrinelloRahmanMass, 88
MD.PreconditionVariableCell, 83
MD.Quench, 85
MD.RelaxCellOnly, 82
MD.RemoveIntramolecularPressure, 86
MD.TargetPressure, 86
MD.TargetTemperature, 87
MD.TauRelax, 88
MD.TypeOfRun, 81
MD.UseSaveCG, 84
MD.UseSaveXV, 38, 39
MD.UseSaveZM, 38
MD.UseStructFile, 36, 37
MD.VariableCell, 
MeshCutoff, 50
MeshSubDivisions
MM.Cutoff, 77
MM.Grimme.D, 77
MM.Grimme.S6, 77
MM.Potentials, 76
MM.UnitsDistance, 77
MM.UnitsEnergy,
MullikenInSCF, 
NaiveAuxiliaryCell, 54
NeglNonOverlapInt, 
NetCharge, 73
New.A.Parameter, 29
New.B.Parameter, 29
NonCollinearSpin, 
NumberOfEigenStates,
OccupationFunction, 57, 58
OccupationMPOrder, 57
ON.ChemicalPotential, 59
ON.ChemicalPotentialOrder, 60
ON.ChemicalPotentialRc, 60
ON.ChemicalPotentialTemperature, 60
ON.ChemicalPotentialUse, 59
ON.eta, 58, 59
ON.eta alpha, 59
ON.eta beta, 59
ON.etol, 58
ON.functional, 58
ON.LowerMemory, 60
ON.MaxNumIter, 58
ON.RcLWF, 59
ON.UseSaveLWF, 60
Optical.Broaden, 69
Optical.EnergyMaximum, 69
Optical.EnergyMinimum, 69
Optical.Mesh, 70
Optical.NumberOfBands, 69
Optical.OffsetMesh, 70
Optical.PolarizationType, 70
Optical.Scissor, 69
Optical.Vector
PAO.Basis, 24
PAO.BasisSize, 20
PAO.BasisSizes, 21
PAO.BasisType, 20
PAO.FixSplitTable, 22
PAO.NewSplitCode, 21
PAO.SoftDefault, 22
PAO.SoftInnerRadius, 22
PAO.SoftPotential, 22
PAO.SplitNorm, 21
PAO.SplitNormH, 21
PAO.SplitTailNorm, 
ParallelOverK, 110
PartialChargesAtEveryGeometry, 67
PartialChargesAtEveryScfStep,
PhononLabels, 93
PolarizationGrids, 
ProcessorY, 78, 110
ProjectedDensityOfStates, 65
PS.KBprojectors , 23
PS.lmax,
RcSpatial
Reparametrize.Pseudos, 
Restricted.Radial.Grid
Rmax.Radial.Grid, 
SaveBaderCharge, 75
SaveDeltaRho, 74
SaveElectrostaticPotential, 74
SaveHS, 53
SaveInitialChargeDensity, 76
SaveIonicCharge, 75
SaveNeutralAtomPotential, 75
SaveRho, 74
SaveTotalCharge, 75
SaveTotalPotential
SCF.Read.Charge.NetCDF, 48
SCF.Read.Deformation.Charge.NetCDF
SCFMustConverge
SimulateDoping, 
SingleExcitation
SlabDipoleCorrection, 
SolutionMethod, 
SpinPolarized,
SuperCell, 
SyntheticAtoms, 15
SystemLabel
SystemName
tbtrans, 
TimeReversalSymmetryForKpoints, 41
TotalSpin, 
TS.BiasContour.Eta, 100
TS.BiasContour.Method, 100
TS.BiasContour.NumPoints, 101
TS.BufferAtomsLeft, 100
TS.BufferAtomsRight, 100
TS.CalcGF, 98
TS.ComplexContour.Emin, 100
TS.ComplexContour.NumCircle, 100
TS.ComplexContour.NumLine, 100
TS.ComplexContour.NumPoles, 100
TS.GFFileLeft, 99
TS.GFFileRight, 99
TS.HSFileLeft, 99, 102
TS.HSFileRight, 99
TS.MixH, 98
TS.NumUsedAtomsLeft, 99
TS.NumUsedAtomsRight, 99
TS.SaveHS, 98
TS.TBT.Emax, 102
TS.TBT.Emin, 102
TS.TBT.NEigen, 102
TS.TBT.NPoints, 102
TS.TriDiag, 99
TS.UpdateDMCROnly, 98
Use.New.Diagk, 55
UseDomainDecomposition, 79
User.Basis, 27
User.Basis.NetCDF, 28
UseSaveData, 80
UseSpatialDecomposition, 79
UseStructFile, 38
WarningMinimumAtomicDistance, 39
WaveFuncKPoints, 64
WaveFuncKPoints, 63
WaveFuncKPointsScale, 
WFS.Band.Max, 63, 69
WFS.Band.Min, 63, 69
WFS.Energy.Max, 68
WFS.Energy.Min, 68
WFS.Write.For.Bands
WriteBands, 62
WriteCoorCerius, 37
WriteCoorInitial, 88
WriteCoorStep, 8
WriteCoorStep, 13
WriteCoorXmol, 37
WriteDenchar, 80
WriteDM, 48
WriteDM.History.NetCDF, 49
WriteDM.NetCDF, 48
WriteDMHS.History.NetCDF, 49
WriteDMHS.NetCDF, 49
WriteEigenvalues, 13, 56
WriteForces, 89
WriteForces, 13
WriteHirshfeldPop, 67
WriteKbands, 13, 62
WriteKpoints, 13, 41
WriteMDhistory, 89
WriteMDXmol, 38
WriteMullikenPop, 13, 66
WriteVoronoiPop, 67
WriteWaveFunctions, 13, 64
XC.authors, 41
XC.functional, 41
XC.hybrid, 
XML.AbortOnErrors, 115
XML.AbortOnWarnings, 115
XML.Write, 115
ZM.ForceTolAngle, 83
ZM.ForceTolLength, 83
ZM.MaxDisplAngle, 84
ZM.MaxDisplLength, 83
ZM.UnitsAngle, 36
ZM.UnitsLength, 36
Zmatrix'.split(',')


class calculator_SIESTA(calculator.calculator):
    def __init__(self,postprocess,dft_job,crystal,kgrid,scheme=0,**parms):
        calculator.calculator.__init__(self,postprocess,dft_job,crystal,kgrid,**parms)
        
    def apply_scheme(self,scheme):
        if scheme == 0:

                          'WriteMullikenPop' : [True,'1'],
                          'PAO.BasisType ' : [True,'split'],
                          'PAO.EnergyShift' : [False,''],
                          'PAO.BasisSize' : [True,'DZP'],
                          'SpinPolarized' : [True,'F'],
                          'MeshCutoff' : [False,''],
                          'MaxSCFIterations' : [True,'100'],
                          'DM.MixingWeight' : [True,'0.1'],
                          'DM.Tolerance' : [True,'1.d-4'],
                          'DM.NumberPulay' : [False,''],
                          'DM.UseSaveDM ' : [False,''],
                          'NeglNonOverlapInt' : [True,'false'],
                          'SolutionMethod' : [False,''],
                          'ElectronicTemperature' : [False,''],
                          'MD.TypeOfRun' : [True,'cg'],
                          'MD.NumCGsteps' : [True,'100'],
                          'MD.MaxCGDispl' : [False,''],
                          'MD.MaxForceTol' : [True,'0.04 eV/Ang'],
                          }
        
        else:
            pass
       
    def generate_files(self):
        self.dft_job.show('CALC_SIESTA','generate input files for calculation')
        file_input_fdf=open(self.output_dir+'siesta_input.fdf','w')
        self.write_input_fdf(file_input_fdf)
        file_input_fdf.close()
        f_=open('siesta.in','w')

        for key in self.siesta_parm:
            value=self.siesta_parm[key]
            if value[0]:
                f_.write(key+' = '+value[1]+ '\n')
              
        f_.write('NumberOfSpecies = '+ str(len(self.crystal.basis_atom_groups)) + '\n')
        f_.write('NumberOfAtoms = '+ str(len(self.crystal.get_totnum_atoms())) + '\n')  
        
        #2nd, write atomic coordinate
        f_.write('\n')
        f_.write('%block  Chemical_Species_label \n')
        for ind, group in enumerate(self.crystal.basis_atom_groups.keys()):
            f_.write('   '+str(ind)+ ' ' + self.crystal.basis_element[group].nucZ  +' ' + group +'\n')
        f_.write('%endblock Chemical_Species_label  \n')
        
        f_.write('\n')
        f_.write('AtomicCoordinatesFormat  ScaledCartesian \n')
        f_.write('%block AtomicCoordinatesAndAtomicSpecies\n')
        for ind, group in enumerate(self.crystal.basis_atom_groups.keys()):
            for atom in self.crystal.basis_atom_groups[group]:
                f_.write(general_tool.vec_to_str(atom.get_position()) + ' ' +str(ind)+'\n')
        f_.write('%endblock  AtomicCoordinatesAndAtomicSpecies\n')
        f_.write('\n')
        
        #lattice, use crystal information
        f_.write('LatticeConstant ' + str(self.crystal.get_length_unit()) +' Ang\n')
        f_.write('%block LatticeVectors\n')
        f_.write(general_tool.vec_to_str(self.crystal.get_prim_vec(0)) +'\n')
        f_.write(general_tool.vec_to_str(self.crystal.get_prim_vec(1)) +'\n')
        f_.write(general_tool.vec_to_str(self.crystal.get_prim_vec(2)) +'\n')
        f_.write('%endblock LatticeVectors\n')
        
        f_.write('\n')
        #kgrid sampling
        if self.kgrid.kmode==0:
            f_.write('%block kgrid_Monkhorst_Pack\n')
            f_.write(' ' + str(self.kpoint_grid[0]) + ' 0 0 0.0\n')
            f_.write(' 0 ' + str(self.kpoint_grid[1]) + ' 0 0.0\n')
            f_.write(' 0 0 ' + str(self.kpoint_grid[2]) + ' 0.0\n')
            f_.write('%endblock kgrid_Monkhorst_Pack\n')
        
        #k linear mode
        if len(self.kpoint_linear_kmode)>0:
            f_.write('BandLineScale pi/a\n')
            f_.write('%block BandLines\n')
            for ind in range(len(self.kpoint_linear_kmode)):
                f_.write(str(ind)+' '+general_tool.vec_to_str(self.kpoint_linear_kmode[ind])+'\n')
            f_.write('%endblock BandLines\n')



