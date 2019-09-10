import csv
import numpy as np
import os


# This class is specific to process the normlized saliency data processing.
# All the fucntions related to normalized saliency mappin is included here
class ProcNorSalMaps:
    mulVideo = []
    limitOfLargestElements = 40

    def __init__(self, normSalList):
        self.normSaLlist = normSalList

        return

    def readData(self):
        filePath = "E:/Dataset/SaliencyScore"

        for i in range(len(self.normSaLlist)):  # len(self.normSaLlist)
            tempFilePathFile = filePath + "/" + self.normSaLlist[i]

            singleVideoMulUser = []
            for userNum in range(50):
                num = '{:02d}'.format(userNum)
                tempFilePathFileUser = tempFilePathFile + "/" + "userNum" + str(num) + ".csv"
                singleVideoSinglUserMulFramesets = []
                with open(tempFilePathFileUser, 'rt')as f:
                    data = csv.reader(f)
                    rowCount = 0
                    framSets = []
                    isFovTile = []
                    normalizeScore = []
                    for row in data:
                        isFovTile.append(row[0])
                        normalizeScore.append(row[2])
                        if rowCount % 200 == 199:
                            framSets.append([isFovTile.copy(), normalizeScore.copy()])
                            isFovTile.clear()
                            normalizeScore.clear()
                        rowCount += 1
                singleVideoMulUser.append(framSets.copy())

            self.mulVideo.append(singleVideoMulUser.copy())

        return

    def getPercentageSaliencyOnTiles(self):

        mulVideoData = []
        for videoNum in range(len(self.mulVideo)):  # len(self.mulVideo)

            singleVideoData = []
            for userNum in range(len(self.mulVideo[videoNum])):  # len(self.mulVideo[videoNum])

                singleVideoSingleUserData = []
                for frameSet in self.mulVideo[videoNum][userNum]:  # len(self.mulVideo[videoNum][userNum])
                    #
                    # for tileNum in range(len(self.mulVideo[videoNum][userNum][
                    #                                     frameSetNum])):  # len(self.mulVideo[videoNum][userNum][singleFrameNum])
                    isInFoV = frameSet[0]
                    normSalVal = frameSet[1]

                    npInFoV = np.asarray(isInFoV)
                    npInFoV = npInFoV.astype(np.int)
                    npNormSalVal = np.asarray(normSalVal)

                    largest40Elements = np.argpartition(npNormSalVal, -self.limitOfLargestElements)[
                                        -self.limitOfLargestElements:]
                    # for ind in largest40Elements:
                    #     print(npNormSalVal[ind])
                    # npNormSalVal.sort()

                    numOfFoVTilesInSal = 0
                    numofOoVTilesInSal = 0

                    for ind in largest40Elements:
                        if int(isInFoV[ind]) == 1:
                            numOfFoVTilesInSal += 1
                        else:
                            numofOoVTilesInSal += 1

                    percFoVTilesRelative2LargestSalValues = numOfFoVTilesInSal * 100 / self.limitOfLargestElements
                    percOoVTilesRelative2LargestSalValues = numofOoVTilesInSal * 100 / self.limitOfLargestElements

                    totalFoVTiles = sum((npInFoV) > 0)

                    percFoVTilesRelative2TotFoVTiles = numOfFoVTilesInSal * 100 / totalFoVTiles
                    percOoVTilesRelative2TotOoVTiles = numofOoVTilesInSal * 100 / (200 - totalFoVTiles)

                    singleFramestData = [percFoVTilesRelative2LargestSalValues,
                                         percOoVTilesRelative2LargestSalValues, percFoVTilesRelative2TotFoVTiles,
                                         percOoVTilesRelative2TotOoVTiles]
                    singleVideoSingleUserData.append(singleFramestData)
                singleVideoData.append(singleVideoSingleUserData)
            mulVideoData.append(singleVideoData)

        return

    def writePercentageSaliency(self, fovOnevideo, oneVideoSaliencyScore, videoName):

        filePath = "E:\Dataset\SaliencyScore" + "\\" + videoName + "_SalScore"

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
