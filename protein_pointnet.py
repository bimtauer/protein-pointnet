# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 15:32:45 2019

@author: bimta
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 15:39:40 2017

@author: Gary
"""

import numpy as np
import tensorflow as tf
from keras import optimizers
from keras.layers import Input
from keras.models import Model
from keras.layers import Dense, Flatten, Reshape, Dropout
from keras.layers import Convolution1D, MaxPooling1D, BatchNormalization
from keras.layers import Lambda
from protein_import import load_data
from keras.utils import np_utils


def mat_mul(A, B):
    return tf.matmul(A, B)

# number of points in each sample
num_points = 247

# number of categories
k = 2

# Input data paths
b_path = '.\Protein Data\Binding_yes'
binders = load_data(b_path, num_points)#[:,:,:3]
nb_path = '.\Protein Data\Binding_no'
nonbinders = load_data(nb_path, num_points)#[:,:,:3]

X = np.vstack((binders, nonbinders))
y = np.hstack((np.ones(len(binders)),np.zeros(len(nonbinders))))


# Normalize to max unit length:        
all_points = X[:,:,:3].reshape(-1, 3)
max_length = max(np.sum(all_points**2, axis = 1))

X_norm = (X[:,:,:3].reshape(-1, 3)/max_length).reshape(11, num_points, 3)

X_norm = np.dstack((X_norm, X[:,:,3:]))


from sklearn.model_selection import train_test_split
#Spliting in train and test:
X_train, X_test, y_train, y_test = train_test_split(X_norm, y, test_size = 0.3)


y_train = np_utils.to_categorical(y_train, k)
y_test = np_utils.to_categorical(y_test, k)

# define optimizer
adam = optimizers.Adam(lr=0.001, decay=0.7)

# ------------------------------------ Pointnet Architecture
# input_Transformation_net
input_points = Input(shape=(num_points, 8))
x = Convolution1D(64, 1, activation='relu', input_shape=(num_points, 8))(input_points)
x = BatchNormalization()(x)
x = Convolution1D(128, 1, activation='relu')(x)
x = BatchNormalization()(x)
x = Convolution1D(1024, 1, activation='relu')(x)
x = BatchNormalization()(x)
x = MaxPooling1D(pool_size=num_points)(x)
x = Dense(512, activation='relu')(x)
x = BatchNormalization()(x)
x = Dense(256, activation='relu')(x)
x = BatchNormalization()(x)
x = Dense(64, weights=[np.zeros([256, 64]), np.identity(8).ravel().astype(np.float32)])(x)
input_T = Reshape((8, 8))(x)

# forward net
g = Lambda(mat_mul, arguments={'B': input_T})(input_points)
g = Convolution1D(64, 1, input_shape=(num_points, 8), activation='relu')(g)
g = BatchNormalization()(g)
g = Convolution1D(64, 1, input_shape=(num_points, 8), activation='relu')(g)
g = BatchNormalization()(g)

# feature transform net
f = Convolution1D(64, 1, activation='relu')(g)
f = BatchNormalization()(f)
f = Convolution1D(128, 1, activation='relu')(f)
f = BatchNormalization()(f)
f = Convolution1D(1024, 1, activation='relu')(f)
f = BatchNormalization()(f)
f = MaxPooling1D(pool_size=num_points)(f)
f = Dense(512, activation='relu')(f)
f = BatchNormalization()(f)
f = Dense(256, activation='relu')(f)
f = BatchNormalization()(f)
f = Dense(64 * 64, weights=[np.zeros([256, 64 * 64]), np.eye(64).flatten().astype(np.float32)])(f)
feature_T = Reshape((64, 64))(f)

# forward net
g = Lambda(mat_mul, arguments={'B': feature_T})(g)
g = Convolution1D(64, 1, activation='relu')(g)
g = BatchNormalization()(g)
g = Convolution1D(128, 1, activation='relu')(g)
g = BatchNormalization()(g)
g = Convolution1D(1024, 1, activation='relu')(g)
g = BatchNormalization()(g)

# global_feature
global_feature = MaxPooling1D(pool_size=num_points)(g)

# point_net_cls
c = Dense(512, activation='relu')(global_feature)
c = BatchNormalization()(c)
c = Dropout(rate=0.7)(c)
c = Dense(256, activation='relu')(c)
c = BatchNormalization()(c)
c = Dropout(rate=0.7)(c)
c = Dense(k, activation='softmax')(c)
prediction = Flatten()(c)
# --------------------------------------------------end of pointnet

# print the model summary
model = Model(inputs=input_points, outputs=prediction)
print(model.summary())


# compile classification model
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Fit model on training data
for i in range(1,50):
    model.fit(X_train, y_train, batch_size=32, epochs=1, shuffle=True, verbose=1)
    # rotate and jitter the points
    #train_points_rotate = rotate_point_cloud(train_points_r)
    #train_points_jitter = jitter_point_cloud(train_points_rotate)
    #model.fit(train_points_jitter, Y_train, batch_size=32, epochs=1, shuffle=True, verbose=1)
    s = "Current epoch is:" + str(i)
    print(s)
    if i % 5 == 0:
        score = model.evaluate(X_test, y_test, verbose=1)
        print('Test loss: ', score[0])
        print('Test accuracy: ', score[1])

# score the model
score = model.evaluate(X_test, y_test, verbose=1)
print('Test loss: ', score[0])
print('Test accuracy: ', score[1])

y_pred = model.predict(X_test)
