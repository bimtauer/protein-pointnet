# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 00:18:55 2019

@author: bimta
"""
from .get_stuff import get_surfaces
from .get_stuff import get_pocket_indeces
from scipy.interpolate import griddata
import trimesh
import numpy as np
import os

# Assume files are already downloaded
"""Example use for download if not:
    
from tools.protein_scraper import download_and_unzip_surfaces
ef_url = 'https://pdbj.org/eF-site/servlet/Download?type=efvet&entry_id={}'
query_list = ['1nsf-A', '1dmk-A', '1yst-H', 'Whatever']
surfaces_path = 'ef-site_downloads'
#Run download and unzip
download_and_unzip_surfaces(query_list, ef_url, surfaces_path)
"""


def retrieve_pocket(pocket_indeces, surface):
    """extracts pocket trimesh from an entire protein surface"""
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

def interpolate_sample(sample, vertices):
    """Interpolates electrostatic potential and hydrophobicity for each sample
    point, given the original pocket vertices"""
    interpolated = griddata(vertices[:,:3], vertices[:,3:5], sample)
    return interpolated 

def sampler(vertices, faces, nr_samples):
    """Returns a number of sample points from a trimesh surface"""
    mesh = trimesh.base.Trimesh(vertices[:,:3], faces)
    #sample_surface_even would be better but doesn't return accurate number
    sample = trimesh.sample.sample_surface(mesh, nr_samples)[0]
    return sample

def sample_from_pocket(pocket_indeces, surface, nr_samples):
    """Samples a given number of sample points from a protein pocket surface 
    and return the samples and the original pocket vertices and faces as a
    dictionary"""
    vertices, faces = retrieve_pocket(pocket_indeces, surface)    
    sample = sampler(vertices, faces, nr_samples) 
    interpolated = interpolate_sample(sample, vertices)  
    sample = np.hstack([sample, interpolated])
    return {'sample':sample, 
            'vertices':vertices, 
            'faces':faces}

def sample_all(path, nr_samples):
    samples = {}
    surfaces_path = os.path.join(path, 'Surfaces')
    indeces_path = os.path.join(path, 'Pocket_Indeces')
    #Check whether all files are there
    assert len(os.listdir(surfaces_path)) == len(os.listdir(indeces_path))
    
    IDs = [ID[:-4] for ID in os.listdir(surfaces_path)]
    #print(IDs)
    surfaces_dict = get_surfaces(surfaces_path)
    pocket_dict = get_pocket_indeces(indeces_path)
    
    for ID in IDs:
        print(f'Retrieving pocket surface sample for {ID}')
        surface = surfaces_dict[ID]
        pocket_indeces = pocket_dict[ID]
        sample = sample_from_pocket(pocket_indeces, surface, nr_samples)
        samples[ID] = sample
    return samples

    
