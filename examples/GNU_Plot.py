'''
Created on Oct 10, 2014

@author: shiangfang
'''
import numpy as np

from DFT_KIT.interface import interface, x_graph

gra1=x_graph.gnu_plot()
gra1.run('set xrange [0:10]; set yrange [-2:2]')
gra1.run('plot sin(x)')




