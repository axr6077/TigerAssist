'''
@author : Ayush Rout
'''
from sklearn import svm
import numpy as np
import csv, re

#wrapper classes
class DataComare():
    def __init__(self):
        self.clf = svm.SVC()

    def setData(self, data, targets):
        '''
        setup algo with given data
        :return: NONE
        '''
        self.data = data
        self.targets = targets
        self.clf.fit(data, targets)

    def matchGesture(self, formattedData):
        result = str(self.clf.predict([formattedData]))[2:-2]
        return result

    def getTargets(self):
        return self.targets

'''
machine init
'''
compareMachine = DataComare()

def getGestureDataFromFile():
    with open('../data/gestureDataLong.csv', 'rb') as dataFile:
        reader = csv.reader(dataFile)
        numCol = len(next(reader))
        dataFile.seek(0)
        numRow = len(list(reader))
        dataFile.seek(0)
        targets = np.empty(numRow, dtype = object)
        data = np.empty([numRow, numCol - 1], np.float64)
        rowCount = 0
        for row in reader:
            column = -1
            for col in row:
                if column is -1:
                    targets[rowCount] = col
                else:
                    data[rowCount, column] = col
                column = column + 1
            rowCount = rowCount + 1
        #start machine
        global compareMachine
        compareMachine.setData(data, targets)
