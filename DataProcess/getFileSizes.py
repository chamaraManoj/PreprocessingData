import matplotlib.pyplot as plt
import numpy as np
import os
import csv
import subprocess as sp
import re


class GetFileSizes:
    frameCateogry = ("MuxedFrames", "DemuxedFrames", "DemuxedFramesWithout_I_Frames")
    fovPlus = ("FoV_only", "FoV_plus")

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

        filePath = r"E:\Dataset\FinalProcessedVideo" + "\\" + "ProcessedVideo_algo_1_Q" + str(qualityLevl) + "\\" + \
                   videoList[videoId] + "\\" + "frame_"
        allFramesAllFileSize = []
        allFramesChunkFileSize = []
        allFramesAllDemuxFileSize = []
        allFramesChunkDemuxFileSize = []

        allFramesAllFileSizeFOVPlus = []
        allFramesChunkFileSizeFOVPlus = []
        allFramesAllDemuxFileSizeFOVPlus = []
        allFramesChunkDemuxFileSizeFOVPlus = []

        # self.fovTraces.shape[0] - 1
        for i in range(self.fovTraces.shape[0] - 1):  # this -1 is applied because, procced video has only 59 tiles
            singleFrame = self.fovTraces[i]

            tileIndices = np.where(singleFrame > 0)
            rowIndi = tileIndices[0]
            colIndi = tileIndices[1]

            addRowIndi, addColIndi = self.getAdditionalcol(rowIndi, colIndi)

            chunknumber = '{:03d}'.format(i)
            singleFrameFileSize = []
            singleFrameDemuxFileSize = []
            singleFrameFileSizeFoVPlus = []
            singleFrameDemuxFileSizeFoVPlus = []

            for j in range(len(rowIndi)):
                tempfilePath = filePath + str(rowIndi[j]) + "_" + str(colIndi[j]) + "\\" + "frame_" + str(
                    chunknumber) + ".mp4"
                singleFrameFileSize.append(os.path.getsize(tempfilePath))
                singleFrameDemuxFileSize.append(self.readFramesSize(tempfilePath))

            for j in range(len(addRowIndi)):
                tempfilePath = filePath + str(addRowIndi[j]) + "_" + str(addColIndi[j]) + "\\" + "frame_" + str(
                    chunknumber) + ".mp4"
                singleFrameFileSizeFoVPlus.append(os.path.getsize(tempfilePath))
                singleFrameDemuxFileSizeFoVPlus.append(self.readFramesSize(tempfilePath))

            # normal muxed type video file size reading
            allFramesChunkFileSize.append(sum(singleFrameFileSize))
            allFramesAllFileSize.append(singleFrameFileSize)

            # Demuxed video file size reading
            allFramesAllDemuxFileSize.append(singleFrameDemuxFileSize)
            tempSum = 0
            for l in range(len(singleFrameDemuxFileSize)):
                tempSum += sum(singleFrameDemuxFileSize[l])
            allFramesChunkDemuxFileSize.append(tempSum)

            # normal muxed type video file size readingFoVPlus
            allFramesChunkFileSizeFOVPlus.append(sum(singleFrameFileSize))
            allFramesAllFileSizeFOVPlus.append(singleFrameFileSize)

            # Demuxed video file size reading
            allFramesAllDemuxFileSizeFOVPlus.append(singleFrameDemuxFileSize)
            tempSum = 0
            for l in range(len(singleFrameDemuxFileSize)):
                tempSum += sum(singleFrameDemuxFileSize[l])
            allFramesChunkDemuxFileSizeFOVPlus.append(tempSum)

        self.writeDataNewMethod(allFramesAllFileSize, allFramesChunkFileSize, qualityLevl, videoId, videoList, algo,
                                self.fovPlus[0], self.frameCateogry[0])
        self.writeDataNewMethod(allFramesAllDemuxFileSize, allFramesChunkDemuxFileSize, qualityLevl, videoId, videoList,
                                algo,
                                self.fovPlus[0], self.frameCateogry[1])

        self.writeDataNewMethod(allFramesAllFileSizeFOVPlus, allFramesChunkFileSizeFOVPlus, qualityLevl, videoId,
                                videoList, algo, self.fovPlus[1], self.frameCateogry[0])
        self.writeDataNewMethod(allFramesAllDemuxFileSizeFOVPlus, allFramesChunkDemuxFileSizeFOVPlus, qualityLevl,
                                videoId, videoList, algo, self.fovPlus[1], self.frameCateogry[1])

        return

    # This function read the video sizes related to the Rubiks implementation
    def readRubiksFileSize(self, videoId, videoList):

        filePath = r"E:\Dataset\FinalProcessedVideo" + "\\" + "Rubiks" + "\\" + \
                   videoList[videoId] + "\\" + "frame_"
        allFramesAllFileSize = []
        allFramesChunkFileSize = []
        allFramesAllDemuxFileSize = []
        allFramesChunkDemuxFileSize = []
        allFramesAllDemuxFileSizeWithoutIFrames = []
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
            tempSum = 0
            for l in range(len(singleFrameDemuxFileSize)):
                tempSum += sum(singleFrameDemuxFileSize[l])
            allFramesChunkDemuxFileSize.append(tempSum)

            tempList = []
            for l in range(len(singleFrameDemuxFileSize)):
                if l < 20:
                    tempList.append(singleFrameDemuxFileSize[l])
                else:
                    tempList.append(singleFrameDemuxFileSize[l][1:])
            allFramesAllDemuxFileSizeWithoutIFrames.append(tempList)

            tempSum = 0
            for l in range(len(tempList)):
                tempSum += sum(tempList[l])

            allFramesChunkDemuxFileSizeWithoutIFrames.append(tempSum)

        self.writeDataRubiksMethod(allFramesAllFileSize, allFramesChunkFileSize, videoId, videoList,
                                   self.frameCateogry[0])
        self.writeDataRubiksMethod(allFramesAllDemuxFileSize, allFramesChunkDemuxFileSize, videoId, videoList,
                                   self.frameCateogry[1])
        self.writeDataRubiksMethod(allFramesAllDemuxFileSizeWithoutIFrames, allFramesChunkDemuxFileSizeWithoutIFrames,
                                   videoId, videoList, self.frameCateogry[2], )

        return

    def readFramesSize(self, videoInput):
        # This function read the encoded frame sizes of the video

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
    def writeDataNewMethod(self, allFramesAllFileSize, allFramesChunkFileSize, qualityLevl, videoId, videoList, algo, fovPlus,
                           frameCategory):

        filePath = "E:\Dataset\FileSizeStat" + "\\" + "FileSize_algo_" + str(algo) + "_" + "Q" + str(
            qualityLevl) + "_" + str(fovPlus)+"\\" + videoList[videoId] + "\\" + str(frameCategory)

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

    # function override to write the data related to Rubiks Video
    def writeDataRubiksMethod(self, allFramesAllFileSize, allFramesChunkFileSize, videoId, videoList, frameCategory):
        filePath = "E:\Dataset\FileSizeStat" + "\\" + "FileSize_algo_" + "Rubiks" + "_" + "\\" + videoList[
            videoId] + "\\" + str(frameCategory)

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

    # if enable the FoV+ attribute, this function calculate the additional tiles to be fetch indorder to maintatin the
    # sufficient QoE
    def getAdditionalcol(self, rowInd, colInd):

        fovTiles = []

        for i in range(len(rowInd)):
            tempCord = [rowInd[i], colInd[i]]
            fovTiles.append(tempCord)

        for i in range(len(fovTiles)):
            tempCord = fovTiles[i]
            row = tempCord[0]
            col = tempCord[1]

            # select all row coord
            if row == 0:
                rowCord = [1, 0]
            elif row == 3:
                rowCord = [2, 3]
            else:
                rowCord = [row - 1, row, row + 1]

            # select all col coord

            if col == 0:
                colCord = [4, 0, 1]
            elif col == 4:
                colCord = [3, 4, 0]
            else:
                colCord = [col - 1, col, col + 1]

            for row in rowCord:
                for col in colCord:
                    tempCord = [row, col]
                    if not tempCord in fovTiles:
                        fovTiles.append(tempCord)

        totRowIndi = []
        totColIndi = []
        for i in range(len(fovTiles)):
            totRowIndi.append(fovTiles[i][0])
            totColIndi.append(fovTiles[i][1])

        return [totRowIndi, totColIndi]
