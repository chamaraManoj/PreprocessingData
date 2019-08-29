import csv
import numpy as np


class ReadFoVData:
    strxlsxNameList = []
    userDetail = []
    numOfViewer = 50

    rowMapping = [0, 0, 0.5, 1, 1, 2, 2, 2.5, 3, 3]

    def __init__(self):
        return

    # Function to create the name list of the excel reading file
    def getNameList(self):
        for i in range(self.numOfViewer):
            number = '{:02d}'.format(i + 1)
            fileName = "drive_user" + str(number) + "_tile.csv"
            self.strxlsxNameList.append(fileName)
        return

    # this function to read the data from the csv files and store them in a seperate list
    # for each user it contains: number of frames read
    # list of frame ID
    # list of tiles for each frame ID
    def readExcelFiles(self):
        self.getNameList()
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
            self.userDetail.append(tempUserdetail)
        print("ok")
        return

    # function to process the data. Basically this function get one user frame and return each of the tile
    # map according our 4x5 implmentation

    def processOneUserTrial(self, userID):

        # list containing one user related data
        userDetail = self.userDetail[userID]
        numOfFrames = userDetail[0]
        fps = numOfFrames // 60
        for sec in range(0, numOfFrames, fps):
            self.getOneSecTile(sec, fps, userDetail)

        return

    # function to get the tile distribution for 1s of the chunk
    def getOneSecTile(self, sec, fps, userDetail):

        videoFrame = np.zeros((4, 5))
        for i in range(fps):
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
            print("ok")
        print("ok")
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
