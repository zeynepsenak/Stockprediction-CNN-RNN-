# -*- coding: utf-8 -*-
"""CNN-STOCKPREDICKTION(plot).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/165nHgZrffvKXAVaRC2sfisNhDDPL9hks
"""

#CNN - Stock Prediction 
import numpy as np
import os
from keras.models import Sequential  
from keras.layers import Dense, Dropout, Activation, Flatten  
from keras.optimizers import SGD
from keras.utils import np_utils
from scipy import misc
import glob
import matplotlib.pyplot as plt
from PIL import Image
import math
import pandas_datareader as web
from sklearn.preprocessing import MinMaxScaler
from pylab import figure, axes, pie, title, show
import keras
from keras.datasets import mnist
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
import numpy as np
from IPython.display import Image
import matplotlib.image as mpimg
from google.colab import drive
import cv2
plt.style.use('fivethirtyeight')

df = web.DataReader('AAPL', data_source='yahoo', start='2004-01-01', end='2020-01-01') 

#Visualizieren die Schlusspreisverlauff
plt.figure(figsize=(16,8))
plt.title('_Schlusspreisverlauf_')
plt.plot(df['Close'])
plt.xlabel('Datum',fontsize=18)
plt.ylabel('Schlusspreis USD ($)',fontsize=18)
plt.show()

data_cl = df.filter(['Close']) #Schluss (Close) Column von Daten : data_cl
clset = data_cl.values #numpy array - data_cl : cl_set
data_op = df.filter(['Open']) #Öffnüng (Open) Column von Daten : data_op
opset = data_op.values #numpy array - data_op : op_set
data_vol = df.filter(['Volume']) #Volumen (Volume) Column von Daten : data_vol
volset = data_vol.values #numpy array - data_vol : vol_set

print(len(clset))

training_data_len = math.ceil( len(clset) *.8) #Train Reiheanzahl

training_data_len

#Skalierung zwischen 0-1 
sc = MinMaxScaler(feature_range=(0, 1)) 
sc_data = sc.fit_transform(clset)

sc_data

train_data = sc_data[0:training_data_len  , : ] #scaliertes trainingsset
#Data teilen: x_train und y_train 
prex_train=[]
y_train=[]

#61. günün kapanış fiyatını tahmin etmek için önceki 60 günlük veri seti
for i in range(60,len(train_data)):
    prex_train.append(train_data[i-60:i, 0]) #x_train : column1: 0-59 , column2: 1-60, column3: 2-61, ... 
    y_train.append(train_data[i, 0]) #y_train : column1: 60, column2: 61, column3: 62, ...    

print(prex_train)

dirName = 'xtr_img'
if not os.path.exists(dirName):
    os.mkdir(dirName)
    print("Directory " , dirName ,  " Created ")
else:    
    print("Directory " , dirName ,  " already exists")

dirName = 'xtest_img'
if not os.path.exists(dirName):
    os.mkdir(dirName)
    print("Directory " , dirName ,  " Created ")
else:    
    print("Directory " , dirName ,  " already exists")

train_images = []
def convert_img(xtrainzahl, imgname): #3161-0
  #Visualizieren die letzte 60 Tag
  plt.figure(figsize=(2,2))
  axes = plt.gca()
  #axes.set_xlim([xmin,xmax])
  axes.set_ylim([0,0.5])
  plt.plot(prex_train[xtrainzahl])
  plt.savefig('xtr_img/' + imgname)

test_images = []
def tconvert_img(xtestzahl, imgname): #3161-4027
  #Visualizieren die letzte 60 Tag
  plt.figure(figsize=(2,2))
  axes = plt.gca()
  #axes.set_xlim([xmin,xmax])
  axes.set_ylim([0,0.5])
  plt.plot(prex_train[xtestzahl])
  plt.savefig('xtest_img/' + imgname)

for i in range(0, 999):
  xtrainzahl = i
  imgname = 'xtrimg' + str(i)
  convert_img(xtrainzahl, imgname)

for i in range(999, 1999):
  xtrainzahl = i
  imgname = 'xtrimg' + str(i)
  convert_img(xtrainzahl, imgname)

for i in range(1999, 3162):
  xtrainzahl = i
  imgname = 'xtrimg' + str(i)
  convert_img(xtrainzahl, imgname)

x_train = []
xtrlabels = []
def xTrainProcess(path):
  p = 0
  x = 0
  images = [f for f in os.listdir(path)]
  for iname in images:
    images = str(path + '/' + iname)
    img = cv2.imread(images, cv2.IMREAD_COLOR)
    x_train.append(img)
    xtrlabels.append(x)
    x = x+1
    p = p+1

    if(p%100==0):
      print(str(p) + ' ist fertig')

path = '/content/xtr_img'
xTrainProcess(path)

x_train = np.asarray(x_train)

#l = len(xtrlabels)
#k = 1053
#x_train = [(x_train)
#        for i in range(l)]
#x_train = np.asarray(x_train)

model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3),
                 activation='relu',
                 input_shape=(144,144,3)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(1, activation='softmax'))

model.summary()

#Compile => optimizer:adam loss:ortalama kara hatası
model.compile(optimizer='adam', loss='mean_squared_error')

#Train das Modell
model.fit(x_train, y_train, batch_size=1, epochs=10)

#Test Daten
test_data = sc_data[training_data_len - 60: , : ]
#x_test und y_test Daten
xi = 0
x_test = []
y_test =  clset[training_data_len : , : ]
for i in range(60,len(test_data)):
    x_test.append(test_data[i-60:i,0])    
    xi = xi + 1

for i in range(xi):
  xtestzahl = i
  imgname = 'xtestimg' + str(i)
  tconvert_img(xtestzahl, imgname)

x_test = []
xtestlabels = []
def xTestProcess(path):
  p = 0
  x = 0
  images = [f for f in os.listdir(path)]
  for iname in images:
    images = str(path + '/' + iname)
    img = cv2.imread(images, cv2.IMREAD_COLOR)
    x_test.append(img)
    xtestlabels.append(x)
    x = x+1
    p = p+1

    if(p%100==0):
      print(str(p) + ' ist fertig')

path = '/content/xtest_img'
xTestProcess(path)

x_test = np.asarray(x_test)

#Vorhergesagte Preis Werte Model
predictions = model.predict(x_test) 
predictions = sc.inverse_transform(predictions)#Undo Skalierung

#RMSE Wert - Perfektion des Modells - (Perfekt:0)
rmse=np.sqrt(np.mean(((predictions- y_test)**2)))
rmse

#Plot/Create the data for the graph
train = data_cl[:training_data_len]
valid = data_cl[training_data_len:]
valid['Predictions'] = predictions

#Graph
plt.figure(figsize=(16,8))
plt.title('_Aktienprognose_')
plt.xlabel('Datum', fontsize=18)
plt.ylabel('Schluss Preis USD ($)', fontsize=18)
plt.plot(train['Close'])
plt.plot(valid[['Close', 'Predictions']])
plt.legend(['Train', 'Wert', 'Vorhergesagte Werte'], loc='lower right')
plt.show()

#Schluss Werte und vorhergesagte Werte
valid