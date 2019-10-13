import os
import cv2
import numpy as np
import csv
from DataProcess import readData as rdData
from DataProcess import readFoVData as rdFoVData
from DataProcess import BaseLineModel as baselineMod
from DataProcess import settings


class ImageProcessingFunc:
    frameSkipCount = 15
    numOfRows = 10
    numOfCol = 20

    def __init__(self):
        self.readVideoDataObj = rdData.ReadData(None, None, None)
        self.baseLineModelObj = baselineMod.BaseLineModel(None, None)
        return

    # function to extract the salient region in the funciton and print saliency map on top of the original frame
    # @frameListSal: Desired saliecny frames to be drawn on top of the original frames
    # @frameListOri: Desired original framed to be drawn on top of the saliency frames
    # @fremaNumList: Desired number list for the frames to be read. previous 2 parameters contains frames related to these indices
    # @videoNormList : list of the names of videos
    # @ videoIdSal: Index of currently processing video

    def getSalientRegion(self, frameListSal, frameListOri, frameNumList, videoNormList, videoIdSal):
        print(type(frameListSal[0]))
        shapeFrameSal = frameListSal[0].shape
        shapeFrameOri = frameListOri[0].shape
        # cv2.imshow('', frameListSal[0])
        alpha = 0.2
        beta = 1 - alpha

        fileOutPath = "H:/Dataset/RawSaliePlusRawData/" + videoNormList[videoIdSal] + "_Pano" + "/"
        if not os.path.exists(fileOutPath):
            os.mkdir(fileOutPath)

        for i in range(len(frameNumList)):
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
    # @foVOneVideo : FoV traces for one video, 50 users for each video. 1800 frames for one user
    # @videoName : video name according to  the saliency video list
    # @videoType : whther it is Saliency Video or original RGB video
    # @isFrameAveraging: If we get 1800 frames for the saliency map, then we have to do frame averaging. If have frames
    # @with 500 ms interval time we do not average frames in this funcitons
    def getNormalizedSaliencyForTile(self, fovOneVideo, videoName, videoType, saliencyMapApgorithm):

        # This list contains fov and normalized saliency score in a given tile. There 200 tiles in one frame
        totNormalizedSaliency = []

        # For each 15 frames, 500ms, for loop extract the average saliency of 15 frames.
        # In addition it takes the normalized saliency of for each not tile.
        # Algo for getting the normalized saliency for a given tile
        # calculate the sum of pixel values in the given region. If a given pixel has the maximum saliency, gracscale
        # value of that pixel should be 255. Thereforemm divide the calculated sum of pixel value by 255 * total num of
        # pixels in the tile.

        # for loop to get the average saliecny map from the corresponding video. This is done only for the saliency map
        # given in the original data set because it contains video files for the salieny map
        if saliencyMapApgorithm == settings.SALIENCY_FROM_ORIGINAL_DATA:
            for frameSetIndex in range(0, 1800, self.frameSkipCount):  # 0, 1800, 15
                print(frameSetIndex)
                salMap = self.getAverageSaliency500ms(frameSetIndex, videoName, videoType)
                totNormalizedSaliency.append(self.getNormalizedSaliency500ms(salMap))

        # For the PanoSal saliency map at the moment we are reading only the frames in every 15 interval.
        elif saliencyMapApgorithm == settings.SALIENCY_FROM_PANOSAL:

            filePath = r"H:\Dataset\PanoSalMaps" + "\\" + videoName
            imageIndexList = list(range(0, 1800, 15))

            # saliency frmes for a given video. returned list [frame_lists, frame_dimensions]
            saliencyFrameData = self.readVideoDataObj.readImageFrames(imgIndexList=imageIndexList,
                                                                      filePath=filePath,
                                                                      videoType=settings.SALIENCY_VIDEO)

            # compute the normalised saliency values for all the saliency frames taken from the saliencyframeData objects
            for salFrames in saliencyFrameData[0]:
                totNormalizedSaliency.append(self.getNormalizedSaliency500ms(salFrames))

        oneVideoSaliencyScore = []


        for userNum in range(len(fovOneVideo)):  # len(fovOneVideo)
            print("User " + str(userNum))
            user = fovOneVideo[userNum]
            oneUserSaliencyScore = []
            # For a given video, for a given user, FoV region and containing saliency data is included
            # in this list

            # tilesInSampledFrames = []
            # sample the FoV traces every 500 ms
            # print(len(user[2]))
            for frameNum in range(0, len(user[2]), self.frameSkipCount):  # 0, len(user[2]), 15
                tilesInSampledFrames = []
                # print("     subFrames  " + str(frameNum))

                #get the total number of tiles in 500 ms sample period
                for subframe in range(self.frameSkipCount):
                    for singletile in user[2][frameNum + subframe]:
                        if not singletile in tilesInSampledFrames:
                            tilesInSampledFrames.append(singletile)
                # tilesInSampledFrames = self.baseLineModelObj.totFoVTiles500Ms(frameNum, user[2])

                tilesInSampledFrames.sort()
                # total FoV in every 15 frames
                #tUserFOVData.append(tilesInSampledFrames.copy())

                # get the avaerage saliency map of 500 ms period of frames
                # averageSaliencyMap = self.getAverageSaliency500ms(frameNum, videoName, videoType)
                saliencyScore500ms = self.getSaliencyScore(totNormalizedSaliency[int(frameNum / self.frameSkipCount)],
                                                           tilesInSampledFrames.copy())

                oneUserSaliencyScore.append(saliencyScore500ms.copy())
                # saliencyScore500ms.clear()
                # tilesInSampledFrames.clear()

            oneVideoSaliencyScore.append(oneUserSaliencyScore.copy())


        # Write the read normalized saliency map details in a file
        self.writeSaliecnyScore(fovOnevideo=fovOneVideo,
                                oneVideoSaliencyScore=oneVideoSaliencyScore,
                                videoName=videoName,
                                saliencyMapApgorithm=saliencyMapApgorithm)

        # for i in range(int(len(tUserFOVData)/2)):
        #     print(i)
        #     print(list(set(tUserFOVData[i]) - set(tUserFOVData[2+i])))

        return oneUserSaliencyScore

    # This function read the saliency of 15 frames
    # @initFrameNum : Starting frame number
    # @videoName: name of the video
    # @videoTye: Whether the video is Saliency of Orignal RGB video
    def getAverageSaliency500ms(self, initFrameNum, videoName, videoType):

        saliencyVideoFrames = self.readVideoDataObj.readAnyVideoSegment(initFrameNum, videoName, videoType)

        averageSaliencyMap = np.mean(saliencyVideoFrames, axis=0)

        return averageSaliencyMap

    # Get the average saliency score for given 15 frames
    # @ avergedSalMap : average saliency map for 15 frames for given time stap of 500ms multiplication
    # @ tilesInSampledFrames: FoV tiles in corresponding to the sampled 15 frames in for the given timestamp
    def getSaliencyScore(self, averagedSalMap, tilesInSampledFrames):

        normalizedSaliency = []

        for row in range(self.numOfRows):
            for col in range(self.numOfCol):
                tileNumber = " " + str(row * self.numOfCol + col)
                if tileNumber in tilesInSampledFrames:
                    print([1, tileNumber, averagedSalMap[row * self.numOfCol + col]])
                    normalizedSaliency.append([1, tileNumber, averagedSalMap[row * self.numOfCol + col]])
                else:
                    normalizedSaliency.append([0, tileNumber, averagedSalMap[row * self.numOfCol + col]])

        return normalizedSaliency

    # def getNormalizedSaliency500ms(self, averageSalMap500ms, totTilesin500ms):
    #
    #     normalizedSaliency = []
    #
    #     tileWidth = int(averageSalMap500ms.shape[1] / 20)
    #     tileHeight = int(averageSalMap500ms.shape[0] / 10)
    #     tileSize = tileWidth * tileHeight
    #
    #     for row in range(10):
    #         for col in range(20):
    #              sumOfPixels = np.sum(
    #                 averageSalMap500ms[row * tileHeight:(row + 1) * tileHeight, col * tileWidth:(col + 1) * tileWidth])
    #             noramlizedSalForTile = sumOfPixels / (255 * tileSize)
    #             sumOfPixels = averageSalMap500ms[row * tileHeight:(row + 1) * tileHeight, col * tileWidth:(col + 1) * tileWidth]

    # tileNumber = " " + str(row * 20 + col + 1)
    # if tileNumber in totTilesin500ms:
    #     print([1, tileNumber, noramlizedSalForTile])
    #     normalizedSaliency.append([1, tileNumber, noramlizedSalForTile])
    # else:
    #     normalizedSaliency.append([0, tileNumber, noramlizedSalForTile])
    #
    # return normalizedSaliency

    # This function is to get the normalized saliency map from each of the tile
    # @evarageSalMap500ms : list of average saliency image frames to be taken for getting normalized saliency map
    def getNormalizedSaliency500ms(self, averageSalMap500ms):

        normalizedSaliency = []

        tileWidth = int(averageSalMap500ms.shape[1] / 20)
        tileHeight = int(averageSalMap500ms.shape[0] / 10)
        tileSize = tileWidth * tileHeight

        for row in range(10):
            for col in range(20):
                sumOfPixels = np.sum(
                    averageSalMap500ms[row * tileHeight:(row + 1) * tileHeight, col * tileWidth:(col + 1) * tileWidth])
                noramlizedSalForTile = sumOfPixels / (255 * tileSize)
                normalizedSaliency.append(noramlizedSalForTile)
                # sumOfPixels = averageSalMap500ms[row * tileHeight:(row + 1) * tileHeight, col * tileWidth:(col + 1) * tileWidth]
                #
                # tileNumber = " " + str(row * 20 + col + 1)
                # if tileNumber in totTilesin500ms:
                #     print([1, tileNumber, noramlizedSalForTile])
                #     normalizedSaliency.append([1, tileNumber, noramlizedSalForTile])
                # else:
                #     normalizedSaliency.append([0, tileNumber, noramlizedSalForTile])

        return normalizedSaliency

    # this function write the Saliency score for each video user by user
    # @fovOneVide: video that has been considered. This also contains the FoV data
    # @oneVideoSaliencyScore: Video related to one video
    # --video
    # -----50 users
    # ---------120 frames
    # @videoName : name of the video as a string
    # @saliencyMapAlogorithm : saliency mapping algorithm. Based on this file path is changed
    def writeSaliecnyScore(self, fovOnevideo, oneVideoSaliencyScore, videoName, saliencyMapApgorithm):

        if saliencyMapApgorithm == settings.SALIENCY_FROM_ORIGINAL_DATA:
            filePath = "H:\Dataset\SaliencyScore" + "\\" + videoName + "_SalScore" + "\\" + "Saliency_from_original_data"
        elif saliencyMapApgorithm == settings.SALIENCY_FROM_PANOSAL:
            filePath = "H:\Dataset\SaliencyScore" + "\\" + videoName + "_SalScore" + "\\" + "Saliency_from_Panosal_algo"

        if not os.path.exists(filePath):
            os.makedirs(filePath)
        # print(len(oneVideoSaliencyScore))
        for userNum in range(len(oneVideoSaliencyScore)):
            num = '{:02d}'.format(userNum)
            userFilePath = filePath + "\\" + "userNum" + str(num) + ".csv"
            with open(userFilePath, 'w', newline='') as writeFile:
                writer = csv.writer(writeFile)
                # print(len(oneVideoSaliencyScore[userNum]))
                for i in range(len(oneVideoSaliencyScore[userNum])):
                    # print(len(oneVideoSaliencyScore[userNum][i]))
                    for j in range(len(oneVideoSaliencyScore[userNum][i])):
                        tempList = [str(item) for item in oneVideoSaliencyScore[userNum][i][j]]
                        writer.writerow(tempList)

            writeFile.close()

        return
