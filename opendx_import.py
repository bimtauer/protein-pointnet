# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 21:14:13 2019

@author: bimta
"""

from gridData import Grid 
g = Grid("pot.dx")
""" The data structure
A Grid consists of a rectangular, regular, N-dimensional array of data. It contains

    The position of the array cell edges.
    The array data itself.

This is equivalent to knowing

    The origin of the coordinate system (i.e. which data cell corresponds to (0,0,…,0)
    The spacing of the grid in each dimension.
    The data on a grid.

attributes and methods:
    

.grid

    histogram or density, defined on numpy nD array
.edges

    list of arrays, the lower and upper bin edges along the axes (both are output by numpy.histogramdd())
.origin

    cartesian coordinates of the center of grid[0,0,…,0]
.delta

    Either n x n array containing the cell lengths in each dimension, or n x 1 array for rectangular arrays.
.metadata

    a user defined dictionary of arbitrary values associated with the density; the class does not touch metadata[] but stores it with save()
.interpolation_spline_order

    order of interpolation function for resampling; cubic splines = 3 [3]

  
# Comments
  object 1 class gridpositions counts nx ny nz
  origin xmin ymin zmin
  delta hx 0.0 0.0
  delta 0.0 hy 0.0 
  delta 0.0 0.0 hz
  object 2 class gridconnections counts nx ny nz
  object 3 class array type double rank 0 times n
  u(0,0,0) u(0,0,1) u(0,0,2)
  ...
  u(0,0,nz-3) u(0,0,nz-2) u(0,0,nz-1)
  u(0,1,0) u(0,1,1) u(0,1,2)
  ...
  u(0,1,nz-3) u(0,1,nz-2) u(0,1,nz-1)
  ...
  u(0,ny-3,nz-3) u(0,ny-2,nz-2) u(0,ny-1,nz-1)
  u(1,0,0) u(1,0,1) u(1,0,2)
  ...
  attribute "dep" string "positions"
  object "regular positions regular connections" class field
  component "positions" value 1
  component "connections" value 2
  component "data" value 3
"""
g.
edge1 = g.edges[0]
edge2 = g.edges[1]
edge3 = g.edges[2]

test = g.grid

edges = g.edges


g.interpolated([2,3,2], [2,3,2], [2,3,2])

# Visualization 
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')



ax.plot_surface(test[5], test[1], test[2])

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()