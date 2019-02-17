'''
@author : Ayush Rout
'''
import cv2
import numpy as np
import NeuralNet_train as svm

def MaxContour(contours, min_area = 200):
    maxC =  None
    MaxArea = min_area
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if (area > MaxArea):
            maxC = cnt
    return maxC

