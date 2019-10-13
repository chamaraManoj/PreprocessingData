import os


class EncodeData:
    # =============================================================================
    #     this class basically encode the original video based on the saliency data.
    #     receive the frame encoding list and encode each tile in different bit rate
    # =============================================================================

    # list to store the encoding bitrate for each of the frame
    encFrameInfor = []

    # define the path variabled
    Executable = r'C:\ffmpeg\bin\ffmpeg.exe'
    # normal original video

    inputPathNormal = r"E:\Dataset\RawVideoOriginal"
    # saliency data video
    inputPathSal = r"E:\Dataset\RawVideoOriginal"
    # proccessed framed for the saliency videos
    outputPathSaliency = r"E:\Dataset\ProcessedVideoSaliency"
    # processed frames for
    outputPathNormal = r"E:\Dataset\ProcessedVideoOriginal"

    # outputPath for processed video using the interestingness prediction algorithms
    inputPathProceVideo = outputPathNormal
    outputPathProceVideo = r"E:\Dataset\FinalProcessedVideo"

    def __init__(self, videoSalList, videoNormList, splitTime, fps, numOfRow, numOfCol):
        self.videoSalList = videoSalList
        self.videoNormList = videoNormList
        self.splitTime = splitTime
        self.fps = fps
        self.NUM_OF_ROW = numOfRow
        self.NUM_OF_COL = numOfCol
        return

    # =============================================================================
    #     this function encode the data using ffmpeg libraries. It runs the ffmpeg
    #     code using the windows command prompt
    # =============================================================================

    # split the saliency video using the ffmpeg command using the command
    # prompt. Get the 1s slices of given video.
    # before processing any data it needs to have sliced videos of saliency.
    # Since we considering only on the I frame
    def splitVideoSaliency(self, videoID):

        # format of input saliency file = inputPathSal\_splitTime_videoname.mp4
        tempInFilePath = self.inputPathSal + "\\" + self.videoSalList[videoID] + ".mp4"
        # format of output saliency file = outputPathSa
        tempOutFilePath = self.outputPathSaliency + "\\" + self.videoSalList[videoID]
        # create the folder
        if not os.path.exists(tempOutFilePath):
            os.mkdir(tempOutFilePath)
            tempOutFilePath = tempOutFilePath + "\\"

            # command to slice the data for the given time slices
            commandUse = self.Executable + " " + "-hide_banner" + " " + \
                         "-err_detect ignore_err" + " " + \
                         "-i " + tempInFilePath + " " + "-r " + str(self.fps) + " " + "-codec:v " + "libx265" + " " + \
                         "-vsync 1 " + "-f " + "segment" + " " + "-preset " + "fast" + " " + \
                         "-segment_format " + "mpegts" + " " + "-segment_time " + str(self.splitTime) + " " + \
                         "-force_key_frames " + "\"" + "expr: gte(t, n_forced * " + str(self.splitTime) + "\")" + " " + \
                         tempOutFilePath + "out%d.mp4"

            print(commandUse)
            os.system(commandUse)

    # This function divies the video into 1s chunk and given number of tiles as well.
    # @videoID: ID of the video to be processed
    # @width: width of the video
    # @height; height of the video

    def splitToTiles(self, videoID, width, height, is4K, resolutionDict):

        # this function split a given video into 4 x 5 tiles
        if is4K:
            tempInFilePath = self.inputPathNormal + "\\" + self.videoNormList[videoID] + "4K" + ".mp4"
            tempOutFilePath = self.outputPathNormal + "\\" + self.videoNormList[videoID] + "4K"
        else:
            tempInFilePath = self.inputPathNormal + "\\" + self.videoNormList[videoID] + ".mp4"
            tempOutFilePath = self.outputPathNormal + "\\" + self.videoNormList[videoID] + "HD"

        # create the main directory to store the normal video data tiles
        if not os.path.exists(tempOutFilePath):
            os.mkdir(tempOutFilePath)
            tempOutFilePath = tempOutFilePath + "\\"

            for row in range(4):
                for col in range(5):
                    # creat a tempFolder for each tile
                    tempTileFolder = tempOutFilePath + "frame_1080_" + str(row) + "_" + str(col)
                    # check whether this filed has been created previously
                    if not os.path.exists(tempTileFolder):
                        os.mkdir(tempTileFolder)
                        tempTileFolder = tempTileFolder + "\\"

                        commandUse = self.Executable + " " + "-hide_banner" + " " + \
                                     "-err_detect ignore_err" + " " + \
                                     "-i " + tempInFilePath + " " + "-r " + str(
                            self.fps) + " " + "-codec:v " + "libx265" + " " + \
                                     "-filter:v " + "\"" + "crop=" + \
                                     "out_w=1/5 *" + str(width) + ":" + \
                                     "out_h=1/4 *" + str(height) + ":" + \
                                     "x=" + str(col) + "/5 * " + str(width) + ":" \
                                                                              "y=" + str(row) + "/4 * " + str(
                            height) + "\"" + " " + \
                                     "-vsync 1 " + "-f " + "segment" + " " + "-preset " + "fast" + " " + \
                                     "-segment_format " + "mpegts" + " " + "-segment_time " + str(
                            self.splitTime) + " " + \
                                     "-force_key_frames " + "\"" + "expr: gte(t, n_forced * " + str(
                            self.splitTime) + "\")" + " " + \
                                     tempTileFolder + "frame_%3d.mp4"
                        print(commandUse)
                        os.system(commandUse)

    def storeData(self, videoID, encodeFrameList, algorithmNum, encodeRes, qualitySet):
        # This function get the encoder FrameList and based on the bit rate values
        # new video segment is encoded in seperate file

        # specify the output file path based on the algorithm number and the video number
        tempOutFilePath = self.outputPathProceVideo + "\\" + "ProcessedVideo_algo_" + str(algorithmNum) + "_Q" + str(
            qualitySet) + "\\" + \
                          self.videoNormList[videoID]

        if not os.path.exists(tempOutFilePath):
            os.makedirs(tempOutFilePath)

            for row in range(self.NUM_OF_ROW):
                for col in range(self.NUM_OF_COL):
                    tempTilePath = tempOutFilePath + "\\" + "frame_" + str(row) + "_" + str(col)
                    if not os.path.exists(tempTilePath):
                        os.mkdir(tempTilePath)

        # check whether the first file in the folder contains any data. If not no data has been entered previously and
        # should process data
        tempTilePath = tempOutFilePath + "\\" + "frame_" + str(0) + "_" + str(0)
        if os.path.getsize(tempTilePath) == 0:
            for i in range(len(encodeFrameList)):
                for row in range(self.NUM_OF_ROW):
                    for col in range(self.NUM_OF_COL):
                        chunk = '{:03d}'.format(i)
                        tempInTileFilePath = self.inputPathProceVideo + "\\" + self.videoNormList[
                            videoID] + "\\" + "frame_1080_" + str(row) + "_" + str(
                            col) + "\\" + "frame_" + chunk + ".mp4"
                        tempOutTileFilePath = tempOutFilePath + "\\" + "frame_" + str(row) + "_" + str(
                            col) + "\\" + "frame_" + chunk + ".mp4"

                        # read the quality and get the resoltion
                        quality = encodeFrameList[i][row * self.NUM_OF_COL + col]
                        resolution = encodeRes[qualitySet][str(quality)]

                        commandUse = self.Executable + " " + \
                                     "-i " + tempInTileFilePath + " " + \
                                     "-codec:v " + "libx265" + " " + \
                                     "-s " + resolution + " " + \
                                     tempOutTileFilePath

                        print(commandUse)
                        os.system(commandUse)

    def h265Toh264(self):

        mainPath = r"E:\Dataset\FinalProcessedVideo\Rubiks\DrivingWith"

        inputPath = mainPath + "\\" + "h265"
        outputPath = mainPath + "\\" + "h264"

        for row in range(4):
            for col in range(5):
                frameInPath = inputPath + "\\" + "frame_" + str(row) + "_" + str(col)
                frameOutPath = outputPath + "\\" + "frame_" + str(row) + "_" + str(col)
                if not os.path.exists(frameOutPath):
                    os.makedirs(frameOutPath)

                for chunk in range(59):
                    chunk = '{:03d}'.format(chunk)
                    inputVideoChunkPath = frameInPath + "\\" + "frame_" + chunk + "_"
                    outputVideoChunkPath = frameOutPath + "\\" + "frame_" + chunk + "_"
                    for layer in range(4):
                        inputVideoChunkLayerPath = inputVideoChunkPath + str(layer) + ".mp4"
                        outputVideoChunkLayerPath = outputVideoChunkPath + str(layer) + ".mp4"

                        commandUse = self.Executable + " " + \
                                     "-i " + inputVideoChunkLayerPath + " " + \
                                     "-codec:v " + "libx264" + " " + \
                                     outputVideoChunkLayerPath

                        print(commandUse)
                        os.system(commandUse)
        return

    def changeFrameRate(self, inputFilePath, outputFilePath, newRate):
        for row in range(4):
            for col in range(5):
                frameInPath = inputFilePath + "\\" + "frame_" + str(row) + "_" + str(col)
                frameOutPath = outputFilePath + "\\" + "frame_" + str(row) + "_" + str(col)
                if not os.path.exists(frameOutPath):
                    os.makedirs(frameOutPath)

                for chunk in range(59):
                    chunk = '{:03d}'.format(chunk)
                    inputVideoChunkPath = frameInPath + "\\" + "frame_" + chunk + ".mp4"
                    outputVideoChunkPath = frameOutPath + "\\" + "frame_" + chunk + ".mp4"
                    # for layer in range(4):
                    #     inputVideoChunkLayerPath = inputVideoChunkPath + str(layer) + ".mp4"
                    #     outputVideoChunkLayerPath = outputVideoChunkPath + str(layer) + ".mp4"

                    commandUse = self.Executable + " " + \
                                 "-i " + inputVideoChunkPath + " " + \
                                 "-filter:v fps=fps="+str(32) + " " + \
                                 outputVideoChunkPath

                    print(commandUse)
                    os.system(commandUse)

        return

        # =============================================================================
#   ffmpeg -hide_banner  -err_detect ignore_err -i input.mp4 -r 24 -codec:v libx264  -vsync 1-codec:a aac -ac 2  -ar 48k  -f segment   -preset fast  -segment_format mpegts  -segment_time 0.5 -force_key_frames  "expr: gte(t, n_forced * 0.5)" out%d.mkv
#
#
# =============================================================================
