from DataProcess import readFoVData as rdFoVData


class BaseLineModel:
    frameSkipNum = 15
    foVVideoList = []
    videosQualityMask = []

    def __init__(self, allFoVTiles):
        self.allFoVTiles = allFoVTiles
        self.numColTiles = 20
        self.numRawTiles = 10
        self.readFoVDataObj = rdFoVData.ReadFoVData()
        return

    # This function control all the baseline model tasks
    def processBaseLine(self):

        # get the avergae foV tiles for each video each user
        for foVTracesVideo in self.allFoVTiles:
            foVUserList = []
            for users in foVTracesVideo:
                foVFrameList = []
                for frameNum in range(0, len(users[2]), self.frameSkipNum):
                    FoVList500ms = self.totFoVTiles500Ms(frameNum, users[2])
                    foVFrameList.append(FoVList500ms.copy())
                foVUserList.append(foVFrameList.copy())
            self.foVVideoList.append(foVUserList.copy())

        self.createQualityIndex()
        print(1)

    # This function creates quality indices for tiles in the frames
    # For each user there are 120 frames which represents whole 60s of period
    # --8 videos
    # ------50 users
    # --------------120 frames
    # --------------each frames 20 x 10 matrix
    def createQualityIndex(self):
        # access the video : 8
        for videoNum in range(len(self.foVVideoList)):
            # access the user :  50
            usersQualityMask = []
            for userNum in range(len(self.foVVideoList[videoNum])):
                # access frame  : 120
                chunksQualityMask = []
                for frameNum in range(len(self.foVVideoList[videoNum][userNum])):
                    tileQualityMask = [[0 for x in range(self.numColTiles)] for y in range(self.numRawTiles)]

                    # fill the FoV tiles as quality 1
                    for tile in self.foVVideoList[videoNum][userNum][frameNum]:
                        # rowNum = self.readFoVDataObj.getRowNumber(int(tile))
                        rowNum = (int(tile)-1) // 20
                        # colNum = self.readFoVDataObj.getColNumber(int(tile))
                        colNum = ((int(tile)-1) % 20)

                        assert rowNum < self.numRawTiles
                        assert colNum < self.numColTiles
                        print(colNum)
                        print(rowNum)
                        tileQualityMask[rowNum][colNum] = 1
                    # framesQualityMask.append(tileQualityMask.copy())
                    chunksQualityMask.append(tileQualityMask.copy())
                usersQualityMask.append(chunksQualityMask.copy())
            self.videosQualityMask.append(usersQualityMask)

        return

    # This funcitno reads the tiles in FoV
    # @startingFrame : starting frame to be read
    # @frameSkipNum : frame list for a user
    def totFoVTiles500Ms(self, startingFrame, userList):
        fovList = []

        for framNum in range(startingFrame, startingFrame + self.frameSkipNum):
            if framNum == 64:
                print(1)
            tilesForFrame = userList[framNum]
            for tile in tilesForFrame:
                if not tile in fovList:
                    fovList.append(tile)

        return fovList
