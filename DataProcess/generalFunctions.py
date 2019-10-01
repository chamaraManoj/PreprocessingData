import os
import numpy as np
import csv


# This class contains some general functions such as write/read invoke by any function
class GeneralFunctions:

    def __init__(self):
        return

    # function to write the data.
    # @data = python list or numpy array, data to be written
    # @filePath = string, path to write the function
    # @metaData = list, metaDataRelated to the write process i.e. ["frameNumber",".csv"] => [frame/user related, file format]
    def writeData(self, data, filePath, metaData):

        if isinstance(data, list):
            shapeList = np.asarray(data).shape
        elif isinstance(data,np.ndarray):
            shapeList = data.shape

        if not os.path.exists(filePath):
            os.makedirs(filePath)

        for iter1 in range(shapeList[0]):
            if metaData[0] == 'frameNum':
                num = '{:03d}'.format(iter1)
            elif metaData[0] == 'userNum':
                num = '{:02d}'.format(iter1)

            userFilePath = filePath + "\\" + metaData[0] + str(num) + metaData[1]
            with open(userFilePath, 'w', newline='') as writeFile:
                writer = csv.writer(writeFile)
                # print(len(oneVideoSaliencyScore[userNum]))
                if len(shapeList) > 1:
                    for iter2 in range(shapeList[1]):

                        if len(shapeList) > 2:
                            tempList = [str(item) for item in data[iter1][iter2]]
                            writer.writerow(tempList)
                        else:
                            tempList = [str(item) for item in data[iter1]]
                            writer.writerow(tempList)
            writeFile.close()
