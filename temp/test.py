import numpy as np
import os
import scipy.io


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
BlockSize'.split(',')
print(SIE_flags)

d1=['afdsasdf',3234,5.6,'dasfad']
for val in d1:
    print(val)

str1='-prefix=hello'
str1=str1[1:]
print(str1)
tmp=str1
tmp=tmp[1:]
tmp=tmp.split('=')
print(tmp)


