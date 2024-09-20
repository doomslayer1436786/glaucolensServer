import os
import time
import numpy as np
import cv2
import tensorflow as tf
from tqdm import tqdm
from glob import glob
import matplotlib.pyplot as plt

height = 640
width = 640

model_path_oc = './/model//unetOCmodel.keras'
model_path_od = './/model//unetODmodel.keras'

output_path_oc = './/static//detections//oc//'
output_path_od = './/static//detections//od//'

modeloc = tf.keras.models.load_model(model_path_oc)
modelod = tf.keras.models.load_model(model_path_od)


def detectOC(img_path,model):
    img_path = os.path.join(img_path)
    name = img_path.split("/")[-1]
    #Reading the image
    x = cv2.imread(img_path,cv2.IMREAD_COLOR)
    input = x
    #Resizing and Normalizing the image
    x = cv2.resize(x, (640, 640)) / 255.0
    #Converting into npArray
    x = np.expand_dims(x,axis=0)
    #Predictions
    pred = model.predict(x)[0]
    saveoutputoc(pred,name)
    return pred

    
def detectOD(img_path,model):
    img_path = os.path.join(img_path)
    name = img_path.split("/")[-1]
    #Reading the image
    x = cv2.imread(img_path,cv2.IMREAD_COLOR)
    input = x
    #Resizing and Normalizing the image
    x = cv2.resize(x, (640, 640)) / 255.0
    #Converting into npArray
    x = np.expand_dims(x,axis=0)
    #Predictions
    pred = model.predict(x)[0]
    saveoutputod(pred,name)
    return pred
    
    

    
def saveoutputoc(pred,name):
    pred=pred*255
    cv2.imwrite(os.path.join(output_path_oc,name),pred)
def saveoutputod(pred,name):
    pred=pred*255
    cv2.imwrite(os.path.join(output_path_od,name),pred)
    
    
def calculate_cdr(od_mask, oc_mask):
    od_area = np.sum(od_mask > 0.09)
    print(od_area)
    oc_area = np.sum(oc_mask >0.99)
    print(oc_area)
    if(oc_area>od_area):
        oc_area = oc_area-od_area+(od_area/4)
        print(oc_area)
    
    cdr = oc_area / od_area if od_area > 0 else 0
    return cdr
    
    
# image_path =  'D://0PROJECTS//SIH2024//GLUCOLENS//webapp//image_0.jpg'
# print(calculate_cdr(detectOC(image_path,modeloc),detectOD(image_path,modelod)))