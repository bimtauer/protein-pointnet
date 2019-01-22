# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 13:16:08 2019

@author: bimta
"""

import os
import numpy as np
import random
from keras.utils import np_utils



# Categorically encode elements
def atom_encoder(atom):
    codes = {'O' : 0,
             'C' : 1,
             'N' : 2,
             'S' : 3,
             'H' : 4} 
    array = np.zeros(5).astype(int).tolist()
    array[codes[atom]] = 1
    return array

def import_pdb(path):
    filenames = [d for d in os.listdir(path)]
    proteins = []        
    for filename in filenames:
        path_to_file = os.path.join(path, filename)
        atoms = []
        for line in open(path_to_file):
            mylist = line.split()
            id = mylist[0]
            if id == 'ATOM':
                atom = mylist[2][0]
                position = list(map(float, mylist[6:9]))
                position += atom_encoder(atom)
                atoms.append(position)
        proteins.append(atoms)
    return proteins

# remove last cause its too small
def filter_small(proteins, min_atoms):
    init = len(proteins)
    for protein in proteins:
        if len(protein) < min_atoms:
            proteins.remove(protein)
    print(f'Removed {init - len(proteins)} from {init} proteins, which had fewer than {min_atoms} atoms')
    return proteins

# Downsampling to equal atom number:
def downsample(proteins, min_atoms):
    proteins = filter_small(proteins, min_atoms)
    #min_atoms = min([len(x) for x in proteins])
    print(f'Downsampling to {min_atoms} atoms per protein (Max. atoms: {max([len(x) for x in proteins])}).')
    downsampled = []
    for protein in proteins:
        if len(protein) >= min_atoms:
            protein = random.sample(protein, min_atoms)
            downsampled.append(protein)
    dataset = np.asarray(downsampled)
    return dataset


def load_data(path, min_atoms):
    proteins = import_pdb(path)
    dataset = downsample(proteins, min_atoms)
    return dataset


###############################################################################
# Labels:







""" 
###############################################################################
# Visualization 
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ex = X[0]

ax.scatter(ex[:,0], ex[:,1], ex[:,2])

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()
"""