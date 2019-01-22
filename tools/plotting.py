# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 22:52:11 2019

@author: bimta
"""



import plotly.plotly as py
import plotly.figure_factory as FF
import plotly.graph_objs as go

fig1 = FF.create_trisurf(vertices[:,0], vertices[:,1], vertices[:,2], simplices=faces,
                         title="Protein Surface")
#py.iplot(fig1, filename="Protein Test")



trace1 = go.Scatter3d(
    x=pocket[:,0],
    y=pocket[:,1],
    z=pocket[:,2],
    mode='markers',
    marker=dict(
        size=5,
        color=p[:,2],                # set color to an array/list of desired values
        colorscale='Viridis',   # choose a colorscale
        opacity=0.8
    )
)

data = [trace1, fig1.data[0], fig1.data[1]]

fig = go.Figure(data=data, layout=layout)
py.iplot(fig, filename='Protein Pocket Sample')

