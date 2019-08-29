from DataProcess import encodeData as encData
from DataProcess import readData as rdData
from DataProcess import processData as procData
from DataProcess import readFoVData as rdFoVData

# ==========================================================
# main implemenataion starts================================
videoSalList = ['coaster_saliency_n', 'coaster2_saliency_n', 'diving_saliency_n', 'drive_saliency_n', 'game_saliency_n',
                'landscape_saliency_n', 'pacman_saliency_n', 'panel_saliency_n', 'ride_saliency_n', 'sport_saliency_n']

videoNormList = ['ChariotRace', 'DrivingWith_4K', 'HogRider', 'KangarooIsland', 'MegaCoster', 'PacMan', 'PerlisPanel',
                 'RollerCoster', 'SFRSport', 'SharkShipWreck']
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

resolution = {"1": "8K",
              "2": "4K",
              "3": "HD"}

encoderResList = [encodeResLow, encodeResMid, encodeResHigh, encodeResUltraHigh]
ALGORITHM_1 = 1

# ==========================================================
# [raw,col] is the index of a given tile

tileTuple = ([0, 0], [0, 1], [0, 2], [0, 3], [0, 4],
             [1, 0], [1, 1], [1, 2], [1, 3], [1, 4],
             [2, 0], [2, 1], [2, 2], [2, 3], [2, 4],
             [3, 0], [3, 1], [3, 2], [3, 3], [3, 4],)

# quality ratings
encRateTuple = (480, 720, 1080)

NUM_OF_COL = 5
NUM_OF_ROW = 4
# ==========================================================

# slice the corresponding video to 1s equal size video segments
# preProcee = PreProcessData(videoSalList)
preProcessData = encData.EncodeData(videoSalList, videoNormList, 1, 30, NUM_OF_ROW, NUM_OF_COL)
##preProcessData.splitVideoSaliency(3)
##preProcessData.splitToTiles(1, 3840, 2160, 2,resolution)

# whether to read all the frames or specific video
isAll = False
videoId = 3

# ==========================================================
# Start reading the frame
##readFrame = rdData.ReadData(videoSalList,isAll,videoId)
##readFrame.readSalData()
# readFrame.readOrgData()
# ========================================================
# read the data related to the frames
##widthOfFrame = readFrame.width
##hieghtOfFrame = readFrame.height
# reference to the extracted data
##frameList = readFrame.frameList
# =========================================================
# =========================================================

# processing the data using a naive algorithm. More details are in the class
# implementation
##qualityList = []
# processFrames = procData.ProcessData(frameList,tileTuple,widthOfFrame,hieghtOfFrame,encRateTuple,qualityList,NUM_OF_ROW,NUM_OF_COL)
##processFrames.thresholdImage();
##qualityList = processFrames.qualityList
# =============================================================================
# try:
#     f= open("bitRateList.txt","w+")
#     for i in range(len(qualityList)):
#         for j in range(len(qualityList[i])):
#             f.write("%d," % qualityList[i][j])
#         f.write("\n")
#
# except:
#     print("file not opened")
#
# =============================================================================

# Open the file with read only permit
f = open('naiveBinaryThresh.txt')
# use readline() to read the first line
line = f.readline()
# use the read line to read further.
# If the file is not empty keep reading one line
# at a time, till the file is empty

bitRateList = []
tempList = []
while line:
    # in python 2+
    # print line
    # in python 3 print is a builtin function, so
    # print(line)
    # use realine() to read next line
    line = line.strip()
    if line != "":
        valueStr = line.split(",")

        if len(valueStr) != 0:
            for strVal in valueStr:
                tempList.append(int(strVal))
        # print(tempList)

    bitRateList.append(tempList.copy())
    tempList.clear()
    line = f.readline()
# for i in range(len(encoderResList)):
    # if (i == 3):
        # preProcessData.storeData(1, bitRateList, ALGORITHM_1, encoderResList, i)
f.close()

#read the FoV data and process the tiles  for each frame
fovReader = rdFoVData.ReadFoVData()
fovReader.readExcelFiles()
fovReader.processOneUserTrial(0)



# =========================================================
# =========================================================
# main implementation ends=================================

