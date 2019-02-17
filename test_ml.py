'''
@author : Ayush Rout
'''

import numpy as np
import csv

with open('../data/data.csv', 'rb') as dataFile:
    reader = csv.reader(dataFile)
    numCol = len(next(reader))
    dataFile.seek(0)
    numRow = len(next(reader))
    dataFile.seek(0)
    targets = np.empty(numRow, dtype=object)
    data = np.empty([numRow, numCol - 1], np.float64)

    rowCount = 0
    for row in reader:
        column = -1
        for col in row:
            if column == -1:
                targets[rowCount] = col
            else:
                data[rowCount, column] = col
            column = column + 1
        rowCount = rowCount + 1

    print(targets)
    print(data)