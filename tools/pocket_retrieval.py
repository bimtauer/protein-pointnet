# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 15:52:42 2019

@author: bimta
"""

import os
import numpy as np

#Returns a dictionary containing the pocket indeces for each protein.ndx file in path
def get_pocket_indeces(path):
    print(f'Collecting pocket indeces from {path}')
    pocket_dict = {}
    for file in os.listdir(path):
        name = file[:-4]
        indeces = np.loadtxt(os.path.join(path, file))
        pocket_dict[name] = indeces
    return pocket_dict