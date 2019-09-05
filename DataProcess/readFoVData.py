import csv
import numpy as np


class ReadFoVData:
    strxlsxNameList = []
    allUserDetail = []
    numOfViewer = 50
    aveAllTileInChunk = False

    rowMapping = [0, 0, 0.5, 1, 1, 2, 2, 2.5, 3, 3]

    def __init__(self):
        return

    # Function to create the name list of the excel reading file
    def getNameList(self,videoName):
        self.strxlsxNameList.clear()
        filePath = "E:/Dataset/FoVData/"
        for i in range(self.numOfViewer):
            number = '{:02d}'.format(i + 1)
            tempFileName = filePath + videoName + str(number) + "_tile.csv"
            self.strxlsxNameList.append(tempFileName)
        return

    # this function to read the data from the csv files and store them in a seperate list
    # for each user it contains: number of frames read
    # list of frame ID
    # list of tiles for each frame ID
    def readExcelFiles(self, videoName):
        self.allUserDetail.clear()
        self.getNameList(videoName)
        for i in range(len(self.strxlsxNameList)):
            fileName = self.strxlsxNameList[i]
            with open(fileName, 'rt')as f:
                data = csv.reader(f)
                rowCount = 0
                frameNumber = []
                tileNumbers = []
                for row in data:
                    if rowCount != 0:
                        frameNumber.append(row[0])
                        tileNumbers.append(row[1:])
                    rowCount += 1
                tempUserdetail = [rowCount - 1, frameNumber, tileNumbers]
            self.allUserDetail.append(tempUserdetail)
        return self.allUserDetail

    def processTheTrace(self):

        allUserFoVTrace = []
        for i in range(self.numOfViewer):
            allUserFoVTrace.append(self.processOneUserTrial(i))

        allUserFoVTracenpArray = np.asarray(allUserFoVTrace)
        aveAllUserFoVTracenpArray = np.mean(allUserFoVTracenpArray, axis=0)
        # print(aveAllUserFoVTracenpArray.shape)

        self.maskArray(aveAllUserFoVTracenpArray)

        return aveAllUserFoVTracenpArray

    # function to process the data. Basically this function get one user frame and return each of the tile
    # map according our 4x5 implmentation

    def processOneUserTrial(self, userID):

        # list containing one user related data
        singleUserFoVTrace = []
        userDetail = self.allUserDetail[userID]
        numOfFrames = userDetail[0]
        fps = numOfFrames // 60
        for sec in range(0, numOfFrames, fps):
            singleUserFoVTrace.append(self.getOneSecTile(sec, fps, userDetail))

        # compute the average fov tile in bins per user. Here the bins mean 4 x 5 tile segementaion for the frame
        # aveSingleUserFoVTrace = sum(singleUserFoVTrace)//len(singleUserFoVTrace)

        return singleUserFoVTrace

    # function to get the tile distribution for 1s of the chunk
    def getOneSecTile(self, sec, fps, userDetail):

        videoFrame = np.zeros((4, 5))

        # If we consider only the first frame of 30 frames in a chunk for saliency detection, we have to
        # consider only the fov data of first frame of the same chunk. This if condition define the number
        # of frames to be consider in the chunk
        if self.aveAllTileInChunk:
            numOfTileChunk = fps
        else:
            numOfTileChunk = 1

        for i in range(numOfTileChunk):
            frameNum = sec + i

            # lsit containing the tile details for a given frame
            frameTileData = userDetail[2][frameNum]

            for tile in frameTileData:
                row = self.getRowNumber(int(tile))
                col = int(self.getColNumber(int(tile)))

                if isinstance(row, int):
                    videoFrame[row][col] += 1
                else:
                    row1 = int(row - 0.5)
                    row2 = int(row + 0.5)
                    videoFrame[row1][col] += 1
                    videoFrame[row2][col] += 1

        return videoFrame

    # return the 4 x 5 row number for given tile
    def getRowNumber(self, tile):

        tile -= 1
        tempRowVal = tile // 20
        rowVal = self.rowMapping[tempRowVal]

        return rowVal

    # return the 4 x 5 col number for a given tile
    def getColNumber(self, tile):

        tile -= 1
        tempColVal = tile % 20
        colVal = tempColVal // 4

        return colVal

    # this function select the maximum 4 indices from the array and creat a mask as 1 and
    # others are zero
    def maskArray(self, avgFoVArray):

        numOfFrames = avgFoVArray.shape[0]

        for i in range(numOfFrames):
            tempArray = avgFoVArray[i].flatten()
            maxInd = (-tempArray).argsort()[:4]
            minInd = tempArray.argsort()[:16]

            tempArray[maxInd] = 1;
            tempArray[minInd] = 0
            if i == 2:
                print("stop")
            tempArray = np.reshape(tempArray, [4, 5])
            avgFoVArray[i] = tempArray

        return
