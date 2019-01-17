# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 17:06:27 2019

@author: bimta
"""

import h5py
import os
import numpy as np

def load_h5(h5_filename):
    f = h5py.File(h5_filename)
    data = f['data'][:]
    label = f['label'][:]
    return (data, label)

num_points = 2048

path = os.path.dirname(os.path.realpath(__file__))
train_path = os.path.join(path, "PrepData")
filenames = [d for d in os.listdir(train_path)]
print(train_path)
print(filenames)

train_points = None
train_labels = None
for d in filenames:
    cur_points, cur_labels = load_h5(os.path.join(train_path, d))
    cur_points = cur_points.reshape(1, -1, 3)
    cur_labels = cur_labels.reshape(1, -1)
    if train_labels is None or train_points is None:
        train_labels = cur_labels
        train_points = cur_points
    else:
        train_labels = np.hstack((train_labels, cur_labels))
        train_points = np.hstack((train_points, cur_points))
train_points_r = train_points.reshape(-1, num_points, 3)
train_labels_r = train_labels.reshape(-1, 1)


# load test points and labels
test_path = os.path.join(path, "PrepData_test")
filenames = [d for d in os.listdir(test_path)]
print(test_path)
print(filenames)
test_points = None
test_labels = None
for d in filenames:
    cur_points, cur_labels = load_h5(os.path.join(test_path, d))
    cur_points = cur_points.reshape(1, -1, 3)
    cur_labels = cur_labels.reshape(1, -1)
    if test_labels is None or test_points is None:
        test_labels = cur_labels
        test_points = cur_points
    else:
        test_labels = np.hstack((test_labels, cur_labels))
        test_points = np.hstack((test_points, cur_points))
test_points_r = test_points.reshape(-1, num_points, 3)
test_labels_r = test_labels.reshape(-1, 1)


from open3d import *
import time
np.where(cur_labels == 6)

len(np.where(cur_labels_t == 6)[0])

for i in np.where(cur_labels_t == 6)[0]:
    pcd = PointCloud()
    pcd.points = Vector3dVector(cur_points_t[i])
    draw_geometries([pcd])




pcd = PointCloud()
pcd.points = Vector3dVector(cur_points_t[398])
draw_geometries([pcd])


import matplotlib.pyplot as plt
import pandas as pd

unique, counts = np.unique(train_labels_r, return_counts=True)
df = pd.DataFrame.from_dict(dict(zip(unique, counts)), orient = 'index')

df.plot.bar()
