'''
Created on Oct 10, 2014

@author: shiangfang
'''
import numpy as np

import os

from DFT_KIT.interface import interface, x_graph

gra1=x_graph.xm_grace('mydata.dat','qq.eps')
gra1.run('TITLE "TEST PLOT"')
gra1.run('TITLE COLOR 3')
gra1.run('PRINT')


