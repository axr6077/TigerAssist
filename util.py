'''
@author : Ayush Rout
'''
import cv2
import numpy as np
import NeuralNet_train as networkTrain

def getMaxContour(contours, min_area = 200):
    maxC =  None
    MaxArea = min_area
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if (area > MaxArea):
            maxC = cnt
    return maxC

def getGestureImg(cnt, img, th, model):
    x, y, w, h = cv2.boundingRect(cnt)
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    imgT = img[y:y+h, x:x+w]
    imgT = cv2.bitwise_and(imgT, imgT, mask = th[y:y+h, x:x+w])
    imgT = cv2.resize(imgT, (200, 200))
    imgTG = cv2.cvtColor(imgT, cv2.COLOR_BGR2YCR_CB)
    resp = networkTrain.predict(model, imgTG)
    img = cv2.imread('Traindata/' + chr(int(resp[1] + 64)) + '_2.jpg')
    if not img.any():
        print("No data received from dataset")
    return img, chr(int(resp[1] + 64))
