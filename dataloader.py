# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 17:14:53 2019

@author: bimta
"""

from tools.get_protein_surfaces import sample_all
import os
import numpy as np
path = 'Protein Data'
atp = 'ATP'
clr = 'CLR'
sam = 'SAM'

ATP = sample_all(os.path.join(path, atp), 1000)
CLR = sample_all(os.path.join(path, clr), 1000)
SAM = sample_all(os.path.join(path, sam), 1000)

def return_samples(what):
    bindings = [ATP, CLR, SAM]
    names = [atp, clr, sam]
    for_each_ligand = {}
    for binding, name in zip(bindings, names):
        all_samples = []
        for key, values in binding.items():
            points = np.array(values[what])
            all_samples.append(points)
        all_samples = np.array(all_samples)
        for_each_ligand[name] = all_samples
    return for_each_ligand