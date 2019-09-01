import matplotlib.pyplot as plt
import numpy as np
import os
import csv
import subprocess as sp
import re


class GetFileSizes:

    def __init__(self, fovTrces, numOfRow, numOfCol):
        self.fovTraces = fovTrces
        self.numOfRow = numOfRow
        self.numOfCol = numOfCol
        self.FFMPEG_BIN = r"C:\FFmpeg\bin\ffprobe.exe"
        self.withIframes = True

        return

    def readFileSizeOurImp(self, qualityLevl, videoId, videoList, algo):
        # this function read the file sizes based on our implmentation. It reads the file sizes based on users FoV pattern
        # For each second of chunk, file size is stored

        filePath = r"H:\Dataset\FinalProcessedVideo" + "\\" + "ProcessedVideo_algo_1_Q" + str(qualityLevl) + "\\" + \
                   videoList[videoId] + "\\" + "frame_"
        allFramesAllFileSize = []
        allFramesChunkFileSize = []

        for i in range(self.fovTraces.shape[0] - 1):  # this -1 is applied because, procced video has only 59 tiles
            singleFrame = self.fovTraces[i]

            tileIndices = np.where(singleFrame > 0)
            rowIndi = tileIndices[0]
            colIndi = tileIndices[1]
            chunknumber = '{:03d}'.format(i)
            singleFrameFileSize = []
            for j in range(len(rowIndi)):
                tempfilePath = filePath + str(rowIndi[j]) + "_" + str(colIndi[j]) + "\\" + "frame_" + str(
                    chunknumber) + ".mp4"
                singleFrameFileSize.append(os.path.getsize(tempfilePath))

            # print(singleFrameFileSize)

            allFramesChunkFileSize.append(sum(singleFrameFileSize))
            allFramesAllFileSize.append(singleFrameFileSize)

        self.writeData(allFramesAllFileSize, allFramesChunkFileSize, qualityLevl, videoId, videoList, algo)
        return

    # This function read the video sizes related to the Rubiks implementation
    def readRubiksFileSize(self, videoId, videoList):

        filePath = r"H:\Dataset\FinalProcessedVideo" + "\\" + "Rubiks" + "\\" + \
                   videoList[videoId] + "\\" + "frame_"
        allFramesAllFileSize = []
        allFramesChunkFileSize = []
        allFramesAllDemuxFileSize = []
        allFramesChunkDemuxFileSize = []
        allFramesAllDemuxFileSizeWithoutIFrames=[]
        allFramesChunkDemuxFileSizeWithoutIFrames = []

        for i in range(self.fovTraces.shape[0] - 1):

            singleFrame = self.fovTraces[i]
            tileIndices = np.where(singleFrame > 0)
            rowIndi = tileIndices[0]
            colIndi = tileIndices[1]
            chunknumber = '{:03d}'.format(i)
            singleFrameFileSize = []
            singleFrameDemuxFileSize = []

            for row in range(self.numOfRow):
                for col in range(self.numOfCol):
                    tempFilePath = filePath + str(row) + "_" + str(col) + "\\" + "frame_" + str(chunknumber) + "_0.mp4"
                    singleFrameFileSize.append(os.path.getsize(tempFilePath))
                    singleFrameDemuxFileSize.append(self.readFramesSize(tempFilePath))

            for j in range(len(rowIndi)):
                # since we have already read first layer tile from each layer, we just have to extract
                # remaining 3 layers for each tile in the FoV

                for k in range(1, 4):
                    tempFilePath = filePath + str(rowIndi[j]) + "_" + str(colIndi[j]) + "\\" + "frame_" + str(
                        chunknumber) + "_" + str(k) + ".mp4"
                    singleFrameFileSize.append(os.path.getsize(tempFilePath))
                    singleFrameDemuxFileSize.append(self.readFramesSize(tempFilePath))
                    # for Enhance layer it is redundant to stream the I frame each time. Therefore we measure the
                    # enhance layer byte size without the I frame size

            allFramesAllFileSize.append(singleFrameFileSize)
            allFramesChunkFileSize.append(sum(singleFrameFileSize))
            allFramesAllDemuxFileSize.append(singleFrameDemuxFileSize)
            allFramesChunkDemuxFileSize.append(sum(singleFrameDemuxFileSize))
            allFramesAllDemuxFileSizeWithoutIFrames.append(singleFrameDemuxFileSize[1:])
            allFramesChunkDemuxFileSizeWithoutIFrames.append(sum(singleFrameDemuxFileSize[1:]))

        self.writeData(allFramesAllFileSize, allFramesChunkFileSize, videoId, videoList)

        return


def readFramesSize(self, videoInput):
    # This function read the encoded frame sizes of the video

    videoInput = videoInput.encode('unicode_escape')

    command = [self.FFMPEG_BIN,
               '-i', videoInput,
               '-show_frames',
               '-of', 'compact',
               '-show_entries', 'frame=pkt_size']

    proc = sp.Popen(command, shell=True, stdout=sp.PIPE)
    serviceList = proc.communicate()[0]
    s = str(serviceList)
    s.encode('unicode_escape')

    frameSizes = [int(s) for s in re.split(r'=|\\', s) if s.isdigit()]

    return frameSizes


# this function writes the data read from the muxed video
def writeData(self, allFramesAllFileSize, allFramesChunkFileSize, qualityLevl, videoId, videoList, algo):
    filePath = "E:\Dataset\FileSizeStat" + "\\" + "FileSize_algo_" + str(algo) + "_" + "Q" + str(
        qualityLevl) + "\\" + videoList[videoId]

    if not os.path.exists(filePath):
        os.makedirs(filePath)

    textFileAllframesSize = filePath + "\\" + "allFramesAllFileSize.csv"
    textFileChunkSize = filePath + "\\" + "allFramesChunkFileSize.csv"

    with open(textFileAllframesSize, 'w') as writeFile:
        writer = csv.writer(writeFile)
        for i in range(len(allFramesAllFileSize)):
            tempList = [str(item) for item in allFramesAllFileSize[i]]
            writer.writerow(tempList)
    writeFile.close()

    with open(textFileChunkSize, 'w') as writeFile:
        writer = csv.writer(writeFile)
        for i in range(len(allFramesAllFileSize)):
            tempList = [str(allFramesChunkFileSize[i])]
            writer.writerow(tempList)
    writeFile.close()

    return


# function override to display the data
def writeData(self, allFramesAllFileSize, allFramesChunkFileSize, videoId, videoList):
    filePath = "E:\Dataset\FileSizeStat" + "\\" + "FileSize_algo_" + "Rubiks" + "_" + "\\" + videoList[videoId]

    if not os.path.exists(filePath):
        os.makedirs(filePath)

    textFileAllframesSize = filePath + "\\" + "allFramesAllFileSize.csv"
    textFileChunkSize = filePath + "\\" + "allFramesChunkFileSize.csv"

    with open(textFileAllframesSize, 'w') as writeFile:
        writer = csv.writer(writeFile)
        for i in range(len(allFramesAllFileSize)):
            tempList = [str(item) for item in allFramesAllFileSize[i]]
            writer.writerow(tempList)
    writeFile.close()

    with open(textFileChunkSize, 'w') as writeFile:
        writer = csv.writer(writeFile)
        for i in range(len(allFramesAllFileSize)):
            tempList = [str(allFramesChunkFileSize[i])]
            writer.writerow(tempList)
    writeFile.close()

    return
