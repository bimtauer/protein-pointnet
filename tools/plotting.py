# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 22:52:11 2019

@author: bimta
"""



import plotly.plotly as py
import plotly.figure_factory as FF
import plotly.graph_objs as go

fig1 = FF.create_trisurf(pdb_cords[:,0], pdb_cords[:,1], pdb_cords[:,2], simplices=pdb_tri,
                         title="Protein Surface")
py.iplot(fig1, filename="Protein Test")