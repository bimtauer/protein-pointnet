# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 00:18:55 2019

@author: bimta
"""
from tools.protein_scraper import download_and_unzip_surfaces
from tools.surface_extractor import get_surfaces
import pandas as pd
#To get surface xmls from ef-site
ef_url = 'https://pdbj.org/eF-site/servlet/Download?type=efvet&entry_id={}'
query_list = ['1nsf-A', '1dmk-A', '1yst-H', 'Whatever']
surfaces_path = 'ef-site_downloads'

#Run download and unzip
download_and_unzip_surfaces(query_list, ef_url, surfaces_path)

#Assuming I have all the XMLs unpacked, this stores the surface for each protein in a dictionary
surfaces = get_surfaces(surfaces_path)

###############################################################################


#TODO: retrieve only vertices with pocket indexes
#Assume there is a list of indexes:
import random
test_list = random.sample(range(1, 100), 50)
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

#Plot to check

fig1 = FF.create_trisurf(x=vertices[:,0], 
                         y=vertices[:,1], 
                         z=vertices[:,2],
                         simplices=faces,
                         title="Pocket",
                         c="red")
py.iplot(fig1, filename="Pocket Extract")

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
