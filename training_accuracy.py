'''
@author : Ayush Rout
'''
import cv2
import numpy as np
from numpy.linalg import norm
# from NeuralNet_train import SVM

svm_params = dict(kernel_type = cv2.ml.SVM_RBF,
                  svm_type = cv2.ml.SVM_C_SVC,
                  C= 2.67, gamma = 5.383)

def preprocess_hog(digits):
    samples = []
    for img in digits:
        gx = cv2.Sobel(img, cv2.CV_32F, 1, 0)
        gy = cv2.Sobel(img, cv2.CV_32F, 0, 1)
        mag, ang = cv2.cartToPolar(
            gx, gy
        )
        bin_n = 16
        bin = np.int32(bin_n * ang / 2 * np.pi)
        bin_cells = bin[:100, :100], bin[100:, :100], bin[:100, 100:], bin[100:, 100:]
        mag_cells = mag[:100, :100], mag[100:, :100], mag[:100, 100:], mag[100:, 100:]
        hists = [np.bincount(b.ravel(), m.ravel(), bin_n) for b, m in zip(bin_cells, mag_cells)]
        hist = np.hstack(hists)

        #hellinger kernel
        eps = 1e-7
        hist /= hist.sum() + eps
        hist = np.sqrt(hist)
        hist /= norm(hist) + eps
        samples.append(hist)
    return np.float32(samples)

def hog_single(img):
    samples = []
    gx = cv2.Sobel(img, cv2.CV_32F, 1, 0)
    gy = cv2.Sobel(img, cv2.CV_32F, 0, 1)
    mag, ang = cv2.cartToPolar(gx, gy)
    bin_n = 16
    bin = np.int32(bin_n*ang / (2*np.pi))
    bin_cells = bin[:100, :100], bin[100:, :100], bin[:100, 100:], bin[100:, 100:]
    mag_cells = mag[:100, :100], mag[100:, :100], mag[:100, 100:], mag[100:, 100:]
    hists = [np.bincount(b.ravel(), m.ravel(), bin_n) for b, m in zip(bin_cells, mag_cells)]
    hist = np.hstack(hists)
    eps = 1e-7
    hist /= hist.sum() + eps
    hist = np.sqrt(hist)
    hist /= norm(hist) + eps
    samples.append(hist)
    return np.float32(samples)

def NeuralNet_train(num):
    imgs = []
    for i in range(65, num + 65):
        for j in range(1, 91):
            print("loading TrainData/" + chr(i) + "_" + str(j) + ".jpg")
            imgs.append(cv2.imread('TrainData/' + chr(i) + '_' + str(j) + '.jpg', 0))
    labels = np.repeat(np.arange(1, num + 1), 90)
    samples = preprocess_hog(imgs)
    print('training with support vector machine')
    print(len(labels))
    print(len(samples))
    model = cv2.SVM()
    model.train(samples, labels, params = svm_params)
    return model

def testNeuralNet_train(num):
    imgs = []
    for i in range(65, num + 65):
        for j in range(91, 101):
            print("loading TestData/" + chr(i) + '_' + str(j) + '.jpg')
            imgs.append(cv2.imread('TrainData/' + chr(i) + '_' + str(j) + '.jpg', 0))
    labels_testing = np.repeat(np.arange(1, num+1), 10)
    print("Testing Neural Network")
    print(len(labels_testing))
    print(len(imgs))
    return imgs, labels_testing

model = NeuralNet_train(4)

test_imgs, test_labels = testNeuralNet_train(4)
count = 0.0
k = 0

for i in test_imgs:
    test_sample = hog_single(i)
    resp = model.predict_all(test_sample).ravel()
    #print(int)(resp[0])
    if test_labels[k] == (int)(resp[0]):
        count += 1.0
    k += 1

print("Accuracy= ", (count/k)*100, "%")
#EOF