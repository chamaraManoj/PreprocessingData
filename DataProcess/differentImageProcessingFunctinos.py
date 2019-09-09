import os
import cv2
import numpy as np
import csv
from DataProcess import readData as rdData
from DataProcess import readFoVData as rdFoVData


class ImageProcessingFunc:

    def __init__(self):
        return

    # function to extract the salient region in the funciton and print saliency map on top of the original frame
    def getSalientRegion(self, frameListSal, frameListOri, frameNumList, videoNormList, videoIdSal):
        print(type(frameListSal[0]))
        shapeFrameSal = frameListSal[0].shape
        shapeFrameOri = frameListOri[0].shape
        # cv2.imshow('', frameListSal[0])
        alpha = 0.2
        beta = 1 - alpha

        fileOutPath = "E:/Dataset/RawSaliePlusRawData/" + videoNormList[videoIdSal] + "/"
        if not os.path.exists(fileOutPath):
            os.mkdir(fileOutPath)

        for i in range(len(frameListSal)):
            colorFrame = cv2.applyColorMap(frameListSal[i], cv2.COLORMAP_HOT)
            # cv2.imshow('', colorFrame)
            # finalImage = cv2.addWeighted(frameListOri[i], alpha, frameListSal[i], beta, 0)
            print(frameNumList[i])
            print(colorFrame.shape)
            print(frameListOri[i].shape)

            finalImage = cv2.add(frameListOri[i], colorFrame)
            dim = (960, 540)
            finalImage = cv2.resize(finalImage, dim, cv2.INTER_LINEAR)
            resizedOriImage = cv2.resize(frameListOri[i], dim, cv2.INTER_LINEAR)

            numpy_vertical_concat = np.concatenate((finalImage, resizedOriImage), axis=0)

            tempFilePath = fileOutPath + str(frameNumList[i]) + ".png"

            cv2.imwrite(tempFilePath, numpy_vertical_concat)

        return

    # This function return a list contatining for each user to what extent the saliency lies on her FoV
    def getNormalizedSaliencyForTile(self, fovOneVideo, videoName, videoType):

        # This lisr contains fov and saliency score in that region
        totSalMap = []
        for frameSetIndex in range(0, 1800, 15): #0, 1800, 15
            print(frameSetIndex)
            totSalMap.append(self.getAverageSaliency500ms(frameSetIndex, videoName, videoType))

        oneVideoSaliencyScore = []
        for userNum in range(len(fovOneVideo)):  # len(fovOneVideo)
            print("User " + str(userNum))
            user = fovOneVideo[userNum]
            # For a given video, for a given user, FoV region and containing saliency data is included
            # in this list
            oneUserSaliencyScore = []
            # sample the FoV traces every 500 ms
            for frameNum in range(0, len(user[2]), 15):  #0, len(user[2]), 15
                print("     subFrames  " + str(frameNum))
                tilesInSampledFrames = []
                # get the total number of tiles in 500 ms sample period
                for subframe in range(15):
                    for singletile in user[2][subframe]:
                        if not singletile in tilesInSampledFrames:
                            tilesInSampledFrames.append(singletile)

                # get the avaerage saliency map of 500 ms period of frames
                #averageSaliencyMap = self.getAverageSaliency500ms(frameNum, videoName, videoType)
                saliencyScore500ms = self.getNormalizedSaliency500ms(totSalMap[int(frameNum/15)], tilesInSampledFrames)
                oneUserSaliencyScore.append(saliencyScore500ms.copy())
                saliencyScore500ms.clear()
                tilesInSampledFrames.clear()
            oneVideoSaliencyScore.append(oneUserSaliencyScore.copy())
            oneUserSaliencyScore.clear()

        self.writeSaliecnyScore(fovOneVideo, oneVideoSaliencyScore, videoName)

        return oneUserSaliencyScore

    def getAverageSaliency500ms(self, initFrameNum, videoName, videoType):

        readVideoData = rdData.ReadData(None, None, None)
        saliencyVideoFrames = readVideoData.readAnyVideoSegment(initFrameNum, videoName, videoType)

        averageSaliencyMap = np.mean(saliencyVideoFrames, axis=0)

        return averageSaliencyMap

    def getNormalizedSaliency500ms(self, averageSalMap500ms, totTilesin500ms):

        normalizedSaliency = []

        tileWidth = int(averageSalMap500ms.shape[1] / 20)
        tileHeight = int(averageSalMap500ms.shape[0] / 10)
        tileSize = tileWidth * tileHeight

        for row in range(10):
            for col in range(20):
                sumOfPixels = np.sum(
                    averageSalMap500ms[row * tileHeight:(row + 1) * tileHeight, col * tileWidth:(col + 1) * tileWidth])
                noramlizedSalForTile = sumOfPixels / (255 * tileSize)
                # sumOfPixels = averageSalMap500ms[row * tileHeight:(row + 1) * tileHeight, col * tileWidth:(col + 1) * tileWidth]
                #
                tileNumber = " " + str(row * 20 + col + 1)
                if tileNumber in totTilesin500ms:
                    normalizedSaliency.append([1, tileNumber, noramlizedSalForTile])
                else:
                    normalizedSaliency.append([0, tileNumber, noramlizedSalForTile])

        return normalizedSaliency

    # this function write the Saliency score for each video user by user

    def writeSaliecnyScore(self, fovOnevideo, oneVideoSaliencyScore, videoName):

        filePath = "E:\Dataset\SaliencyScore" + "\\" + videoName

        if not os.path.exists(filePath):
            os.makedirs(filePath)
        #print(len(oneVideoSaliencyScore))
        for userNum in range(len(oneVideoSaliencyScore)):
            num = '{:02d}'.format(userNum)
            userFilePath = filePath + "\\" + "userNum" + str(num) + ".csv"
            with open(userFilePath, 'w') as writeFile:
                writer = csv.writer(writeFile)
                #print(len(oneVideoSaliencyScore[userNum]))
                for i in range(len(oneVideoSaliencyScore[userNum])):
                    #print(len(oneVideoSaliencyScore[userNum][i]))
                    for j in range(len(oneVideoSaliencyScore[userNum][i])):
                        tempList = [str(item) for item in oneVideoSaliencyScore[userNum][i][j]]
                        writer.writerow(tempList)

            writeFile.close()

        return
