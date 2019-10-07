from numpy.dual import norm

from DataProcess import readFoVData as rdFoVData
from DataProcess import generalFunctions as genFunc
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
from matplotlib import colors
from matplotlib.ticker import PercentFormatter
# import colormap as cmap
import math
import scipy.stats as stats


class BaseLineModel:
    isDrawHeatMapForVideos = False
    isfoVWithHistograms = True

    frameSkipNum = 15
    m: int = 50
    n: int = 9

    foVVideoList = []
    videosQualityMask = []
    videosFrameWiseFoVBin = []
    videosTotFoVByAllUsers = []
    X_cordAllVideos = [[0] * 50 for i in range(9)]  # [video x user]
    Y_cordAllVideos = [[0] * 50 for i in range(9)]  # [video x user]

    def __init__(self, allFoVTiles, vidoeList):
        self.allFoVTiles = allFoVTiles
        self.videoList = vidoeList
        self.numColTiles = 20
        self.numRawTiles = 10
        self.readFoVDataObj = rdFoVData.ReadFoVData()
        self.generalFucnions = genFunc.GeneralFunctions()
        self.m = 50
        self.n = 9
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

        # Since we have already got the data with FoV bin values, -chama- has commented this line
        # self.writeFoVBinData()

        self.getToTFoVBinsForVideos()

        # Exract the X,Y coordinates of the user if and only if we create scatterplots with histograms
        if self.isfoVWithHistograms:
            self.getXYCoordinates()

        # Since we have already got the data with FoV bin values, -chama- has commented this line
        # self.writeTotFoVBinData()
        self.statisticalAnalysisFoV()

        print(1)

    # This function creates quality indices for tiles in the frames
    # For each user there are 120 frames which represents whole 60s of period
    # --9 videos
    # ------50 users
    # --------------120 frames
    # --------------each frames 20 x 10 matrix
    def createQualityIndex(self):
        # access the video : 9
        for videoNum in range(len(self.foVVideoList)):
            # access the user :  50
            fovBinForFrames = np.asarray(
                [[[0 for x in range(self.numColTiles)] for y in range(self.numRawTiles)] for frames in range(120)])
            usersQualityMask = []
            for userNum in range(len(self.foVVideoList[videoNum])):
                # access frame  : 120
                chunksQualityMask = []
                for frameNum in range(len(self.foVVideoList[videoNum][userNum])):
                    tileQualityMask = np.asarray(
                        [[0 for x in range(self.numColTiles)] for y in range(self.numRawTiles)])

                    # fill the FoV tiles as quality 1
                    for tile in self.foVVideoList[videoNum][userNum][frameNum]:
                        # rowNum = self.readFoVDataObj.getRowNumber(int(tile))
                        rowNum = (int(tile) - 1) // 20
                        # colNum = self.readFoVDataObj.getColNumber(int(tile))
                        colNum = ((int(tile) - 1) % 20)

                        assert rowNum < self.numRawTiles
                        assert colNum < self.numColTiles
                        tileQualityMask[rowNum][colNum] = 1
                    # framesQualityMask.append(tileQualityMask.copy())
                    fovBinForFrames[frameNum] += tileQualityMask.copy()
                    chunksQualityMask.append(tileQualityMask.copy())
                usersQualityMask.append(chunksQualityMask.copy())
            self.videosQualityMask.append(usersQualityMask.copy())
            self.videosFrameWiseFoVBin.append(fovBinForFrames.copy())
        return

    # This funcitno reads the tiles in FoV
    # @startingFrame : starting frame to be read
    # @frameSkipNum : frame list for a user
    def totFoVTiles500Ms(self, startingFrame, userList):
        fovList = []

        for framNum in range(startingFrame, startingFrame + self.frameSkipNum):
            tilesForFrame = userList[framNum]
            for tile in tilesForFrame:
                if not tile in fovList:
                    fovList.append(tile)
        return fovList

    # This function is to get the heat map of FoV for each video. Intention of having this heat map is to represent
    # the FoV based on tiles and to identify whether if all the users have the same interesiting to the same region.

    def getToTFoVBinsForVideos(self):

        for videoNum in range(len(self.videosFrameWiseFoVBin)):
            tileQualityMask = np.asarray([[0 for x in range(self.numColTiles)] for y in range(self.numRawTiles)])
            for frameNum in range(len(self.videosFrameWiseFoVBin[videoNum])):
                tileQualityMask += self.videosFrameWiseFoVBin[videoNum][frameNum]

            self.videosTotFoVByAllUsers.append(tileQualityMask.copy())

    # This function get the X,Y coordinates for each tile and store the data in the defined list.
    def getXYCoordinates(self):

        for videoNum in range(len(self.foVVideoList)):

            for userNum in range(len(self.foVVideoList[videoNum])):
                X_cordAllFramesOneUser = []
                Y_cordAllFramesOneUser = []

                for frameNum in range(len(self.foVVideoList[videoNum][userNum])):
                    [xInd, yInd] = self.getCordinateList(self.foVVideoList[videoNum][userNum][frameNum])

                    X_cordAllFramesOneUser.append(xInd.copy())
                    Y_cordAllFramesOneUser.append(yInd.copy())

                self.X_cordAllVideos[videoNum][userNum] = X_cordAllFramesOneUser.copy()
                self.Y_cordAllVideos[videoNum][userNum] = Y_cordAllFramesOneUser.copy()

        return

    # This function is to process different opertions related to heatmaps
    # func1 = draw heatmap
    # func2 = store heatmap
    def statisticalAnalysisFoV(self):

        # Draw the heat maps for each video considering FoV data of all tiles of all the users
        if self.isDrawHeatMapForVideos:
            filePath = "E:\Dataset\Images" + "\\" + "AverageFoVDistribution" + "\\"

            if not os.path.exists(filePath):
                os.makedirs(filePath)
            for i in range(len(self.videosTotFoVByAllUsers)):
                uniform_data = (self.videosTotFoVByAllUsers[i])
                uniform_data_log = np.log(self.videosTotFoVByAllUsers[i])

                # get statistical analysis of distribution of tiles
                # if isStatAnlysisFoVForVideos:
                #     rawMean_abs = np.mean(uniform_data,axis=1)
                #     rawMean_log = np.mean(uniform_data_log, axis=1)
                #     colMean_abs = np.mean(uniform_data,axis=0)
                #     colMean_log = np.mean(uniform_data_log, axis=0)
                #
                #     gaussianMean_raw_abs = np.mean(rawMean_abs)
                #     gaussianVar_raw_abs = np.var(rawMean_abs)
                #     sigma_raw_abs = math.sqrt(gaussianVar_raw_abs)
                #
                #     gaussianMean_raw_log = np.mean(rawMean_log)
                #     gaussianVar_raw_log = np.var(rawMean_log)
                #     sigma_raw_log = math.sqrt(gaussianVar_raw_log)
                #
                #     gaussianMean_col_abs = np.mean(colMean_abs)
                #     gaussianVar_col_abs = np.var(colMean_abs)
                #     sigma_col_log = math.sqrt(gaussianVar_col_abs)
                #
                #     gaussianMean_col_log = np.mean(colMean_log)
                #     gaussianVar_col_log = np.var(colMean_log)
                #     sigma_raw_log = math.sqrt(gaussianVar_col_log)
                #
                #     col = np.asarray(range(0,20))
                #     raw = np.asarray(range(0,10))
                #
                #     plt.plot(col, colMean_abs)

                # x = np.linspace(gaussianMean_raw_abs - 3 * sigma_raw_abs, gaussianMean_raw_abs + 3 * sigma_raw_abs, 100)
                # plt.plot(x, stats.norm.pdf(x, gaussianMean_raw_abs, sigma_raw_abs))

                ax = sns.heatmap(uniform_data, linewidth=0, square=True, cmap="YlOrRd", xticklabels=False,
                                 yticklabels=False, cbar_kws={"shrink": 0.5})
                tempImageFile = filePath + self.videoList[i] + ".png"
                plt.savefig(tempImageFile)
                plt.clf()

                axlog = sns.heatmap(uniform_data_log, linewidth=0, square=True, cmap="YlOrRd", xticklabels=False,
                                    yticklabels=False, cbar_kws={"shrink": 0.5})
                tempImageFile_log = filePath + "z" + self.videoList[i] + "_log.png"
                plt.savefig(tempImageFile_log)
                plt.clf()

        # plot the FoV distribution for each video in a scatter plot with a histogram
        if self.isfoVWithHistograms:
            filePath = "E:\Dataset\Images" + "\\" + "HistogramDistribution" + "\\"

            if not os.path.exists(filePath):
                os.makedirs(filePath)

            for videoNum in range(len(self.X_cordAllVideos)):
                expandX_Cord = []
                expandY_Cord = []

                for userNum in range(len(self.X_cordAllVideos[videoNum])):

                    for frameNum in range(len(self.X_cordAllVideos[videoNum][userNum])):
                        expandX_Cord.extend(self.X_cordAllVideos[videoNum][userNum][frameNum])
                        expandY_Cord.extend(self.Y_cordAllVideos[videoNum][userNum][frameNum])

                assert (len(expandX_Cord) == len(expandY_Cord))
                self.drawHistogram(expandX_Cord, expandY_Cord,filePath,self.videoList[videoNum])

        return

    def drawHistogram(self, x, y,filePath,videoName):

        x_npArray = np.asarray(x)
        y_npArray = np.asarray(y)

        mu_x = np.mean(x_npArray)
        sigma_x = math.sqrt(np.var(x_npArray))
        mu_y = np.mean(y_npArray)
        sigma_y = math.sqrt(np.var(y_npArray))

        # x_xgaussian = mu_x + sigma_x * np.random.randn(437)
        # x_ygaussian = mu_y + sigma_y * np.random.randn(437)

        fig, axs = plt.subplots(1, 2, sharey=True, tight_layout=True, gridspec_kw={'width_ratios': [2, 1]})

        n_bins_x = 20
        n_bins_y = 10

        N_x, bins_x, patches_x = axs[0].hist(x, bins=n_bins_x, density=True)
        N_y, bins_y, patches_y = axs[1].hist(y, bins=n_bins_y, density=True)

        y_xgaussian = ((1 / (np.sqrt(2 * np.pi) * sigma_x)) * np.exp(-0.5 * (1 / sigma_x * (bins_x - mu_x)) ** 2))
        y_ygaussian = ((1 / (np.sqrt(2 * np.pi) * sigma_y)) * np.exp(-0.5 * (1 / sigma_y * (bins_y - mu_y)) ** 2))

        axs[0].plot(bins_x, y_xgaussian, '--')
        axs[1].plot(bins_y, y_ygaussian, '--')
        fig.tight_layout()

        fracs_x = N_x / N_x.max()
        fracs_y = N_y / N_y.max()

        norm_x = colors.Normalize(fracs_x.min(), fracs_x.max())
        norm_y = colors.Normalize(fracs_y.min(), fracs_y.max())

        for thisfrac_x, thispatch_x in zip(fracs_x, patches_x):
            color = plt.cm.viridis(norm_x(thisfrac_x))
            thispatch_x.set_facecolor(color)

        for thisfrac_y, thispatch_y in zip(fracs_y, patches_y):
            color = plt.cm.viridis(norm_y(thisfrac_y))
            thispatch_y.set_facecolor(color)

        axs[0].yaxis.set_major_formatter(PercentFormatter(xmax=1))
        axs[1].yaxis.set_major_formatter(PercentFormatter(xmax=1))

        axs[0].set_xlabel('Tile - X')
        axs[0].set_ylabel('Percentage frequency (%)')
        axs[0].set_title('Histogram FoV-X')

        axs[1].set_xlabel('Tile - Y')
        # axs[1].set_ylabel('Probability density')
        axs[1].set_title('Histogram FoV-Y')

        #plt.show()

        tempImageFile_log = filePath + videoName+"Hist" + ".png"
        plt.savefig(tempImageFile_log)
        plt.clf()

        return

    # This function write FoV nin values for all the videos getting total from all the users.
    # 9 videos
    # -----120 frames
    def writeFoVBinData(self):

        for i in range(len(self.videosFrameWiseFoVBin)):
            print(i)
            print(len(self.videosFrameWiseFoVBin))
            filePath = "E:\Dataset\FoVBinForVidoes" + "\\" + self.videoList[i] + "_FoVBin"
            self.generalFucnions.writeData(self.videosFrameWiseFoVBin[i], filePath, ["frameNum", ".csv"])

        return

    # this function write total of FoV bin values for all the videos
    # 9 videos
    # -----1 frame (contain total of all 120 frames)
    def writeTotFoVBinData(self):

        for i in range(len(self.videosTotFoVByAllUsers)):
            filePath = "E:\Dataset\TotFoVBinForVidoes" + "\\" + self.videoList[i] + "_TotFoVBin"
            self.generalFucnions.writeData(self.videosTotFoVByAllUsers[i], filePath, ["csvData", ".csv"])
        return

    # Function to get the tile coodinate for a given tile list
    # @ tileList = list containing the tiles
    def getCordinateList(self, tileList):
        x = []
        y = []
        for tile in tileList:
            # rowNum = self.readFoVDataObj.getRowNumber(int(tile))
            rowNum = (int(tile) - 1) // 20
            # colNum = self.readFoVDataObj.getColNumber(int(tile))
            colNum = ((int(tile) - 1) % 20)

            assert rowNum < self.numRawTiles
            assert colNum < self.numColTiles

            x.append(colNum)
            y.append(rowNum)

        return x, y
