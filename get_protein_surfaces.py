# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 00:18:55 2019

@author: bimta
"""
from tools.protein_scraper import download_and_unzip_surfaces
from tools.surface_extractor import get_surfaces
import trimesh
#To get surface xmls from ef-site
ef_url = 'https://pdbj.org/eF-site/servlet/Download?type=efvet&entry_id={}'
query_list = ['1nsf-A', '1dmk-A', '1yst-H', 'Whatever']
surfaces_path = 'ef-site_downloads'

#Run download and unzip
#download_and_unzip_surfaces(query_list, ef_url, surfaces_path)

#Assuming I have all the XMLs unpacked, this stores the surface for each protein in a dictionary
surfaces = get_surfaces(surfaces_path)

###############################################################################


#TODO: retrieve only vertices with pocket indexes
#Assume there is a list of indexes:
import random
test_list = random.sample(range(1, 100), 50)


test_list = np.loadtxt('1nsf-A.ndx')
# There is a problem with this list: unless it reliably contains indeces for connected
# points, we cannot extract both vertices and faces
# so i need to find all faces that contain indeces also present in the list

#Assume there is a dictionary containing such a list for each protein
pocket_dict = {'1nsf-A':test_list}

def retrieve_pocket(ID, pocket_dict, surfaces):
    pocket_indeces = pocket_dict[ID]
    surface = surfaces[ID]
    faces = surface['triangles']
    match = np.in1d(faces, pocket_indeces)
    match_indeces = np.any(match.reshape(-1,3), axis=1)
    vertices = surface['coordinates']
    pocket_faces = faces[match_indeces]
    v_in_f = np.unique(pocket_faces)
    pocket_vertices = vertices[v_in_f]
    
    # Update face indeces:
    for index, pos in enumerate(v_in_f): 
        pocket_faces = np.where(pocket_faces == pos, index, pocket_faces)
        #print(pocket_faces)
    
    return pocket_vertices, pocket_faces
    
    
vertices, faces = retrieve_pocket('1nsf-A', pocket_dict, surfaces)

###############################################################################
#Original protein:
surface = surfaces['1nsf-A']
ver = surface['coordinates']
fac = surface['triangles']


#Plot to check
import numpy as np
import plotly.plotly as py
import plotly.figure_factory as FF
import plotly.graph_objs as go


eps = []
for triangle in faces:
    first = vertices[triangle[0]][3]
    second = vertices[triangle[1]][3]
    third = vertices[triangle[2]][3]
    ep = np.mean([first, second, third])
    eps.append(ep)
        
#The pocket surface
fig1 = FF.create_trisurf(x=vertices[:,0], 
                         y=vertices[:,1], 
                         z=vertices[:,2],
                         simplices=faces,
                         color_func=eps,
                         title="Pocket",
                         colormap="Portland")

#The remaining atoms of the protein
trace = go.Scatter3d(
    x=ver[:,0],
    y=ver[:,1],
    z=ver[:,2],
    mode='markers',
    marker=dict(
        size=5,
        color='grey',                # set color to an array/list of desired values
        colorscale='Viridis',   # choose a colorscale
        opacity=0.8
    )
)


data = [trace,  fig1.data[0], fig1.data[1]]

fig = go.Figure(data=data)
py.iplot(fig, filename='Protein Pocket Sample')


###############################################################################
from scipy.interpolate import griddata

def sample_from_pocket(vertices, faces, nr_samples):
    mesh = trimesh.base.Trimesh(vertices[:,:3], faces)
    #sample_surface_even would be better but doesn't return accurate number
    sample = trimesh.sample.sample_surface(mesh, nr_samples)[0]
    return sample

def interpolate_sample(sample, vertices):
    interpolated = griddata(vertices[:,:3], vertices[:,3:5], sample)
    return interpolated 

sample = sample_from_pocket(vertices, faces, 100) 

interpolated = interpolate_sample(sample, vertices)  
    
###############################################################################

#Plot all surfaces:
import numpy as np
import pylab as plt
import trimesh


vertices = surfaces['1nsf-A']['coordinates']
faces = surfaces['1nsf-A']['triangles']

mesh = trimesh.base.Trimesh(vertices[:,:3], faces)
sample = trimesh.sample.sample_surface_even(mesh, 1000)
p = sample[0]



v_in_f = np.array([1,3])
t = np.array([1,2,3,4,5,6,7])

pocket_faces = np.array([[1,2,3],
                         [2,3,4],
                         [7,1,3],
                         [7,3,4]])
    
match = np.in1d(t2, t)
match = np.any(match.reshape(-1,3), axis=1)
