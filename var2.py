# -*- coding: utf-8 -*-
"""var2

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13hej_BN_eevXYNyPnWqCHVFCJDA5XegA

Variant 2: Remove the maxpool layers. Using stride=2 in the conv layer before the maxpool to
achieve similar size reduction. Would the performance improve?
"""

# Commented out IPython magic to ensure Python compatibility.
import sys
import time
import numpy as np
import tensorflow as tf
from keras.optimizers import SGD
from keras.layers.core import Dense
from keras.models import Sequential
from keras.datasets import cifar10
from keras.utils import to_categorical
from keras.layers.core import Flatten
from keras.layers.core import Dropout
from keras.layers.core import Reshape
from keras.layers.core import Activation
from keras.layers.convolutional import Conv2D, Conv3D
from keras.layers.convolutional import MaxPooling2D, MaxPooling3D 
from keras.losses import CategoricalCrossentropy
from sklearn.model_selection import train_test_split

import matplotlib.pyplot as plt
# %matplotlib inline

# using cifar-10 dataset from TensorFlow
(x_train, y_train), (x_test_base, y_test_base) = cifar10.load_data()
x_test, x_val, y_test, y_val = train_test_split(x_test_base, y_test_base, test_size=0.5)

print("x_train shape", x_train.shape)
print("x_test shape", x_test.shape)
print("x_val shape", x_val.shape)
print("y_train shape", y_train.shape)
print("y_test shape", y_test.shape)
print("y_val shape", y_val.shape)

#Prepare Dataset:
y_train = to_categorical(y_train)
y_test = to_categorical(y_test)
y_val = to_categorical(y_val)

x_train = x_train.astype("float") / 255.0 
x_test = x_test.astype("float") / 255.0 
x_val = x_val.astype("float")/255.0

class MiniVGG:
  
  def build(height, width, depth, classes):
    model = Sequential()
    inputShape = (height, width, depth)
   
    #The layer configuration:
    #Input -> Conv3-64 -> Conv3-64 -> Maxpool(2x2) 
          #-> Conv3-128 -> Conv3-128 -> Maxpool(2x2) 
          #-> Conv3-256 -> Conv3-256 -> Maxpool(2x2) 
          #-> Flatten -> FC-512 -> Output

    # first Conv3-64 -> Conv3-64 -> Maxpool(2x2) 
    model.add(Conv2D(64, (3, 3),  activation='relu', padding="same", input_shape=inputShape))
    model.add(Conv2D(64, (3, 3), activation='relu', padding="same"))
    model.add(Conv2D(64, (3, 3), strides=2, padding='same', activation='relu'))
  

    # second Conv3-128 -> Conv3-128 -> Maxpool(2x2) 
    model.add(Conv2D(128, (3, 3), activation='relu', padding="same"))
    model.add(Conv2D(128, (3, 3), activation='relu', padding="same"))
    model.add(Conv2D(128, (3, 3), strides=2, padding='same', activation='relu'))
    

    # third Conv3-256 -> Conv3-256 -> Maxpool(2x2)  
    model.add(Conv2D(256, (3, 3), activation='relu', padding="same"))
    model.add(Conv2D(256, (3, 3), activation='relu', padding="same"))
    model.add(Conv2D(256, (3, 3), strides=2, padding='same', activation='relu'))

    # Flatten -> FC-512 -> Output
    model.add(Flatten())
    model.add(Dense(512,  activation='relu'))
    
     # softmax classifier
    model.add(Dense(10, activation='softmax' ))
 
    return model

#Create an instance of the Model...
model = MiniVGG.build(height = 32,width = 32, depth = 3, classes=10)

#Describe the architecture of the Model....
model.summary()

model.compile(loss=CategoricalCrossentropy(from_logits=True), optimizer=SGD(learning_rate= 0.001), metrics=['accuracy'])

#Start time before the training begins...
start_time = round(time.time() * 1000)

pred_history = model.fit(x_train, y_train, validation_data=(x_val, y_val),batch_size=64, epochs=20, verbose=1)

#Total train time...
total_train_time = round(time.time() * 1000) - start_time
print('Total Train Time: %d' % (total_train_time))

test_accuracy = model.evaluate(x_test, y_test, verbose=0)
print('Test Accuracy: %.2f' % (test_accuracy[1] * 100.0))

val_accuracy = model.evaluate(x_val, y_val, verbose=0)
print('Val Accuracy: %.2f' % (val_accuracy[1] * 100.0))

#Plot Train vs Validation Accuracy
plt.figure(figsize=(4, 6))
plt.plot(np.arange(0, 20), pred_history.history["accuracy"], label="train_acc")
plt.plot(np.arange(0, 20), pred_history.history["val_accuracy"], label="val_acc")
plt.title("Training Accuracy vs Validation Accuracy")
plt.xlabel("Number of Epochs")
plt.ylabel("Accuracy")
plt.legend()
plt.show()

#Plot Train vs Validation Loss
plt.figure(figsize=(4, 6))
plt.plot(np.arange(0, 20), pred_history.history["loss"], label="train_loss")
plt.plot(np.arange(0, 20), pred_history.history["val_loss"], label="val_loss")
plt.title("Training Loss vs Validation Loss")
plt.xlabel("Number of Epochs")
plt.ylabel("Loss")
plt.legend()
plt.show()