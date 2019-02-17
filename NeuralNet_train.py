'''
@author : Ayush Rout
'''
import cv2
import numpy as np
from numpy.linalg import norm

svm_params = dict(kernel_type = cv2.ml.SVM_RBF,
                  svm_type = cv2.ml.SVM_C_SVC,
                  C= 2.67, gamma = 5.383)

class StatModel(object):
    def load(self, fn):
        self.model.load(fn)
    def save(self, fn):
        self.model.save(fn)

class SVM(StatModel):
    def __init__(self, C = 1, gamma = 0.5):
        self.model = cv2.ml.SVM_create()
        self.model.setGamma(gamma)
        self.model.setC(C)
        self.model.setKernel(cv2.ml.SVM_RBF)
        self.model.setType(cv2.ml.SVM_C_SVC)

    def train(self, samples, responses):
        print("Number of Sample = " + str(len(samples)))
        print("Number of responses = " + str(len(responses)))
        self.model.train(samples, cv2.ml.ROW_SAMPLE, responses)

    def predict(self, samples):
        results = np.array(self.model.predict(samples)). ravel()
        return results

def preprocess_hog(digits):
    samples = []
    for img in digits:
        gx = cv2.Sobel(img, cv2.CV_32F, 1, 0)
        gy = cv2.Sobel(img, cv2.CV_32F, 0, 1)
        mag, ang = cv2.cartToPolar(
            gx, gy
        )
        bin_n = 16
        bin = np.int32(bin_n*ang / 2*np.pi)
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
    for i in range (65, num + 65):
        for j in range(1, 401):
            print('Class ' + chr(i) + ' is being loaded ')
            imgs.append(cv2.imread('TrainData/' + chr(i) + '_' + str(j) + '.jpg', 0)) #store images in a list
        labels = np.repeat(np.arrange(1, num+1), 400)
        samples = preprocess_hog(imgs)
        print('SVM is building')
        #print('got here')
        print(len(labels))
        print(len(samples))
        model = SVM(C = 2.97, gamma = 5.383)
        model.train(np.array(samples), np.array(labels))
    return model

def predict(model, img):
    samples = hog_single(img)
    resp = model.predict(samples)
    return resp

#EOF