from DataProcess import encodeData as encData
from DataProcess import readData as rdData
from DataProcess import processData as procData
from DataProcess import readFoVData as rdFoVData
from DataProcess import getFileSizes as gtFileVSize
from DataProcess import saliencyProcessing as saliencyProcFunc
from DataProcess import processNormalSalMaps as procNorSalMaps
from DataProcess import imgProcFunctinos as imgProcFunc
from DataProcess import settings
from DataProcess import BaseLineModel as baselineMod
import numpy as np
import os

# ====================================================================================================================
# main implemenataion starts==========================================================================================



# Names of the original saliency map videos
videoSaliencyNameList = ['coaster_saliency_n', 'pacman_saliency_n', 'diving_saliency_n','drive_saliency_n', 'game_saliency_n',
                'landscape_saliency_n', 'panel_saliency_n', 'ride_saliency_n', 'sport_saliency_n'] # diving_saliency_n add again, removed for PanosalMap

# Names of the original videos
videoNormList = ['ChariotRace', 'DrivingWith', 'HogRider', 'KangarooIsland', 'MegaCoster', 'PacMan', 'PerlisPanel',
                 'RollerCoster', 'SFRSport', 'SharkShipWreck']

# 'MegaCoster'  #SharkShipWreck add again
# Defined the names list for reading original videos which is exactly matching the saliency map video details
videoNormListForSaliencyAnalysis = ['RollerCoster', 'PacMan', 'SharkShipWreck', 'DrivingWith', 'HogRider',
                                    'KangarooIsland',
                                    'PerlisPanel', 'ChariotRace', 'SFRSport']

# file names containing the FoV traces of the users
fovUserList = ["coaster_user", "pacman_user","diving_user", "drive_user", "game_user",
               "landscape_user", "panel_user", "ride_user", "sport_user"] #"diving_user" is removed fro, 2 index since at the moment proecessing saliency score for panosal map, saliency of that video was no there.

# Names of the list containing the
normSalList = ["coaster_saliency_n_SalScore", "diving_saliency_n_SalScore", "diving_saliency_n_SalScore",
               "drive_saliency_n_SalScore", "game_saliency_n_SalScore",
               "landscape_saliency_n_SalScore", "panel_saliency_n_SalScore", "ride_saliency_n_SalScore",
               "sport_saliency_n_SalScore"]

# 360p: 426x240 => 426/5 x 240/4
# 480p: 854x480
# 720p: 1280x720
# 1080p: 1920x1080
# 2160p: 3840x2160
encodeResLow = {"3": "128x90",
                "2": "170x120",
                "1": "256x180"}

encodeResMid = {"3": "170x120",
                "2": "256x180",
                "1": "384x270"}

encodeResHigh = {"3": "256x180",
                 "2": "384x270",
                 "1": "768x540"}

encodeResUltraHigh = {"3": "384x270",
                      "2": "768x540",
                      "1": "1536x1080"}

resolution = {"1": "HD",
              "2": "4K",
              "3": "8K"}

encoderResList = [encodeResLow, encodeResMid, encodeResHigh, encodeResUltraHigh]
qualityTuple = ("3", "2", "1")
ALGORITHM_1 = 1

SALIENCY_VIDEO = 0
RGB_VIDEO = 1

NUM_OF_COL = 5
NUM_OF_ROW = 4

# whether to read all the frames or specific video
isAll = False
videoIdSal = 3
videoIdNor = 1

# Boolean variables to enable and disable the functions
isEncodeFunctions = False
isReadDataFunctions = False
isProcessDataFunctions = False
isReadFoVData = True
isSaliencyProcessing = True

# functions to store common data
allFoVTraces = []

#Creating class objects need for different functions

#object needs for reading and processing saliency map contained in videos and separate images as well.
saliencyFunctinos_obj = saliencyProcFunc.ImageProcessingFunc()
imageProcFuncitons_obj = imgProcFunc.displayFuncitons()

#Temporarly used function for storing the data.
# imageProcFuncitons_obj.brightnessContrastAdjust(None, None,None,settings.SALIENCY_VIDEO,videoSaliencyNameList)




# ====================================================================================================================
# slice the corresponding video to 1s equal size video segments
if isEncodeFunctions:
    encodeFunctions = encData.EncodeData(videoSaliencyNameList, videoNormList, 1, 30, NUM_OF_ROW, NUM_OF_COL)
    # encodeFunctions.splitVideoSaliency(3)
    # for i in range(len(videoNormList)):
    #     encodeFunctions.splitToTiles(i, 3840, 2160, True, resolution)
    #encodeFunctions.h265Toh264()
    encodeFunctions.changeFrameRate(r"E:\Dataset\FinalProcessedVideo\ProcessedVideo_algo_1_Q2\DrivingWith",
                                    r"E:\Dataset\FinalProcessedVideo\ProcessedVideo_algo_1_Q2\DrivingWith_recent",
                                    32)
    print(1)
# ====end of prepocessing data=========================================================================================


# ====================================================================================================================
# Start reading the frame
# This set of function to read the image frames from desired saliency map and draw on top of the original image frames.
if isReadDataFunctions:
    readFrame = rdData.ReadData(videoSaliencyNameList, videoNormListForSaliencyAnalysis, isAll)
    # Draw saliency region on top of the video frame
    for i in range(len(videoSaliencyNameList)):
        print("frame")
        print(i)
        if i == 1:
            print(1)

        # if i == len(videoSalList):
        readFrame.readSalData(i)
        readFrame.readOrgData(i)

        # get the reandom frame indices from the readFrame objects generated in readSalData funciton
        randomFrames = readFrame.randomFrames
        tempNewPanoSalpath = "E:/Dataset/PanoSalMaps/" + videoNormListForSaliencyAnalysis[
            i]  # path for Panosalnet data set
        readFrame.readImageFrames(randomFrames, tempNewPanoSalpath)

        frameListSal = readFrame.frameListSal
        frameListOri = readFrame.frameListOrg
        frameListPanoSal = readFrame.frameListPanoSal
        frameNumList = readFrame.randomFrames
        saliencyFunctinos_obj.getSalientRegion(frameListPanoSal, frameListOri, frameNumList, videoNormListForSaliencyAnalysis,
                                               i)

    # read the data related to the frames
    # widthOfFrame = readFrame.
    # hieghtOfFrame = readFrame.height
    # reference to the extracted data
    # frameList = readFrame.frameList
    imageMetaData = readFrame.getImageMetaData()
# ======End of reading frame data=====================================================================================


# =============Image thresholding======================================================================================
# This class for threshoding images, particularly for saliency area detection
#implementation
# if isProcessDataFunctions:
# qualityList = []
#
#
#-chamar- This class contains function to threshold the images. This function should be modified
# processFrames = procData.ProcessData(frameList, tileTuple, widthOfFrame, hieghtOfFrame, encRateTuple, qualityList,
#                                      NUM_OF_ROW, NUM_OF_COL)
# processFrames.thresholdImage();
# qualityList = processFrames.qualityList
#
# try:
#     f = open("bitRateList.txt", "w+")
#     for i in range(len(qualityList)):
#         for j in range(len(qualityList[i])):
#             f.write("%d," % qualityList[i][j])
#         f.write("\n")
#
# except:
#     print("file not opened")
# ======================================================================================================================




# ======================================================================================================================
# Open the file with read only permit
# f = open('naiveBinaryThresh.txt')
# use readline() to read the first line
# line = f.readline()
# use the read line to read further.
# If the file is not empty keep reading one line
# at a time, till the file is empty

# bitRateList = []
# tempList = []
# while line:

# line = line.strip()
# if line != "":
#     valueStr = line.split(",")
#
#     if len(valueStr) != 0:
#         for strVal in valueStr:
#             tempList.append(int(strVal))
#     print(tempList)

# bitRateList.append(tempList.copy())
# tempList.clear()
# line = f.readline()
# for i in range(len(encoderResList)):
# if (i == 3):
# -chamr- important function where encoding of tile is done according to our algorithm

# encodeFunctions.storeData(1, bitRateList, ALGORITHM_1, encoderResList, i)
# f.close()




# =============Reading FoV data ======================================================================================
# read the FoV data and process the tiles  for each frame
if isReadFoVData:
    fovReader = rdFoVData.ReadFoVData()
    for i in range(2):  # len(fovUserList)
        allFoVTraces.append(fovReader.readExcelFiles(fovUserList[i]))
# =====================================================================================================================




# =============Function anlyzes the FoV traces of the videos===========================================================
# Function to create baseline benchmark algorithms based on the FoV
# baseLineObj = baselineMod.BaseLineModel(allFoVTraces, videoNormListForSaliencyAnalysis)
# baseLineObj.processBaseLine()
# =====================================================================================================================



#===================Read Normalized saliency data======================================================================
# Read the normalized saliency data from the file and process them to find the percentage saliecny in the FoV and OoV
# regions
# @normSalList = List containing the file names which includes the normalized saliency map data

if isSaliencyProcessing:
    for i in range(1,2):  # len(allFoVTraces)
        saliencyFunctinos_obj.getNormalizedSaliencyForTile(allFoVTraces[i], videoSaliencyNameList[i], SALIENCY_VIDEO, settings.SALIENCY_FROM_PANOSAL)  #[SaliencyInOriginalDataSet or Panosal]
    processSalData = procNorSalMaps.ProcNorSalMaps(normSalList)

# read the normalized saliency map data
processSalData.readData()
# process the percentage saliency in the region.
isRelative = False
processSalData.getPercentageSaliencyOnTiles(isRelative)
# isRelative = True
# processSalData.getPercentageSaliencyOnTiles(isRelative)
# =====================================================================================================================




# =====================================================================================================================
# This set of codes read the file sizes of the video using the avarage FoV traces of the users. We assume that data
# transmission and the client end process do not have any issues in processing. In the mean time we try to read the
# file sizes related to Rubiks as well

# aveAllUserFoVTraceNpArray = fovReader.processTheTrace()
# fileSizeReader = gtFileVSize.GetFileSizes(aveAllUserFoVTraceNpArray, NUM_OF_ROW, NUM_OF_COL)

# for i in range(qualityTuple.__len__()):
#     if i == 1:
#         fileSizeReader.readFileSizeOurImp(qualityTuple[i], videoIdNor, videoNormList, ALGORITHM_1)
# fileSizeReader.readRubiksFileSize(videoIdNor, videoNormList)

# ====================================================================================================================
# ==== main implementation ends=======================================================================================
