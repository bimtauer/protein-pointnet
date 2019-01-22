# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 22:27:14 2019

@author: bimta
"""
# Parse surface XML
import os
import numpy as np
import xml.etree.ElementTree as ET
from tqdm import tqdm

def get_surface(path, XML):
    tree = ET.parse(os.path.join(path, XML))
    root = tree.getroot()
    #TODO: Make sure this works for all files:
    tag = root.tag.split('}')[0] + '}'
    
    cords = []
    for neighbor in root.iter(tag + 'vertex'):
        xyz = [float(x) for x in neighbor.get('image').split()][:3]
        #electrostatic potential & hydrophobicity
        values = [float(x) for x in neighbor.get('property').split()][:2]
        cords.append(xyz + values)
    cords = np.array(cords)
    
    edges = []
    for neighbor in root.iter(tag + 'edge'):
        edges.append([int(x)-1 for x in neighbor.get('vertex').split()])
    edges = np.array(edges)
    
    tri = []
    for neighbor in root.iter(tag + 'triangle'):
        tri.append([int(x)-1 for x in neighbor.get('vertex').split()])
    tri = np.array(tri)
    return {'coordinates': cords,
            'edges': edges, 
            'triangles': tri}

def get_surfaces(path):
    surface_dict = {}
    print(f'Collecting protein surfaces from {path}')
    for file in tqdm(os.listdir(path)):
        if file.endswith('.xml'):
            surface = get_surface(path, file)
            surface_dict[file[:-4]] = surface
    return surface_dict



#Returns a dictionary containing the pocket indeces for each protein.ndx file in path
def get_pocket_indeces(path):
    print(f'Collecting pocket indeces from {path}')
    pocket_dict = {}
    for file in tqdm(os.listdir(path)):
        name = file[:-4]
        indeces = np.loadtxt(os.path.join(path, file))
        pocket_dict[name] = indeces
    return pocket_dict