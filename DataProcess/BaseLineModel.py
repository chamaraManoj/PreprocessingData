class BaseLineModel:
    frameSkipNum = 15
    foVVideoList= []

    def __init__(self, allFoVTiles):
        self.allFoVTiles = allFoVTiles
        return

    #This function control all the baseline model tasks
    def processBaseLine(self):

        # get the avergae foV tiles for each video each user
        for foVTracesVideo in self.allFoVTiles:
            foVUserList = []
            for users in foVTracesVideo:
                foVFrameList = []
                for frameNum in range(1, len(users), self.frameSkipNum):
                    FoVList500ms = self.totFoVTiles500Ms(frameNum, users)
                    foVFrameList.append(FoVList500ms.copy())
                foVUserList.append(foVFrameList.copy())
            self.foVVideoList.append(foVUserList.copy())

    # This funcitno reads the tiles in FoV
    # @startingFrame : starting frame to be read
    # @frameSkipNum : frame skipping number for skipiing the frames
    def totFoVTiles500Ms(self, startingFrame, userList):
        fovList = []
        for framNum in range(startingFrame, startingFrame + self.frameSkipNum):
            tile = userList[framNum]
            if not tile in fovList:
                fovList.append(tile)
        return fovList
