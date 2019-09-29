import cv2
import matplotlib.pyplot as plt
import copy
import os
import random
import csv


# This class contains following functions
# generateRandomFrames : generate rnadom number representing the image index
# readSalData : Read saliency images from the saliency video files according to the indices given by generateRandomFrames
# readOrgData : Read original images from the original video files according to the indices given by generateRandomFrames
# readAnyVideoSegment : Read given video frame from a given video file
# readImageFrames : read images from a file (this is not a video file, a normal file containing images)

class ReadData:
    NUM_OF_FRAMES = 10

    # salInFilePath = "E:\Dataset\ProcessedVideoSaliency"
    salInFilePath = "E:/Dataset/RawSaliencyData"
    normInFilePath = "E:/Dataset/RawVideoOriginal"

    # lsit containging the read images
    frameListSal = []
    frameListOrg = []
    randomFrames = []
    frameListPanoSal = []  # contain the saliency maps from new Panosalnet images

    # list containing the size of the image
    initialSalImgSize = []
    panoSalNetSalImgSize = []
    rgbImgSize = []

    # Const
    # @videoSalList : names of the Saliency videos,
    # ['coaster_saliency_n', 'pacman_saliency_n', 'diving_saliency_n', 'drive_saliency_n', 'game_saliency_n',
    # 'landscape_saliency_n', 'panel_saliency_n', 'ride_saliency_n', 'sport_saliency_n']
    # @videoNormaList : names of the original videos,
    # ['RollerCoster', 'PacMan', 'SharkShipWreck', 'DrivingWith', 'HogRider','KangarooIsland',
    # 'PerlisPanel', 'ChariotRace', 'SFRSport']
    # @isAll : whether to read all the video files or not
    def __init__(self, videoSalList, videoNormList, isAll):
        self.videoSalList = videoSalList
        self.isAll = isAll
        self.videoNormList = videoNormList

    # this function generate random number list between 1 -1800 to refer the saliency and corresponding images
    # @fps : frames per second for the video, this is 30
    # framecount : maximum frame number of the video.
    def generateRandomFrames(self, fps, length, frameCount):
        self.randomFrames.clear()
        for i in range(10):
            # ---ch--this is the original one random frame generator
            # tempRanFrame = (i * fps * 5 + random.randint(0, fps * 5))
            # ---ch--generate random image of multiplier of 15
            tempRanFrame = (i * 12 + random.randint(0, 12)) * 15
            if tempRanFrame <= frameCount:
                self.randomFrames.append(tempRanFrame)
        return

    # This function read the saliency images from the saliency video indexed by the given ID.
    # @videoID : number between 1- len(videoSalList), videoSalList is a parameter passed to the constuctor of this class
    # videoSalList contains the names of saliency video files
    def readSalData(self, videoID):
        # Read specific video data to frame list
        self.frameListSal.clear()
        if not self.isAll:
            filePath = self.salInFilePath + "/" + self.videoSalList[videoID] + ".mp4"
            # videoList = os.listdir(filePath)  # dir is your directory path
            # numberOfFiles = len(videoList)
            for i in range(1):

                # videoFilePath = filePath + "/" + videoList[i]
                cap = cv2.VideoCapture(filePath)

                if i == 0:
                    self.initialSalImgSize.append(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    self.initialSalImgSize.append(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    frameCount = cap.get(cv2.CAP_PROP_FRAME_COUNT)
                    print(frameCount)
                    self.generateRandomFrames(cap.get(cv2.CAP_PROP_FPS), 60, frameCount)

                count = 0
                sucess = False

                if cap.isOpened:
                    sucess = True;

                while sucess:
                    frameNum = self.randomFrames[count]
                    retVal = cap.set(cv2.CAP_PROP_POS_FRAMES, frameNum - 1)
                    sucess, frame = cap.read()

                    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                    # path = "E:/Uni_Studies/Useful_Datasets_360/Dataset_3_360_Video_Viewing_Dataset_in_head_mounted_virtual_reality/360dataset/intermediateResults/sal.png"
                    # cv2.imshow('',colorFrame)

                    # plt.figure(count + 1)
                    # plt.imshow(frame)
                    # plt.ioff()
                    # plt.show(block=False)

                    # =============================================================================
                    # =============================================================================
                    #                 cv2.namedWindow('image', cv2.WINDOW_NORMAL)
                    #                 cv2.imshow('image',frame)
                    #                 cv2.waitKey(5000)
                    # =============================================================================
                    # =============================================================================

                    self.frameListSal.append(frame)
                    count += 1
                    # print(count)
                    if count == ReadData.NUM_OF_FRAMES:
                        break
                cap.release()

    # This function read the original images from the original video indexed by the given ID.
    # @videoID : number between 1- len(videoNormList), videoNormList is a parameter passed to the constuctor of this class
    # videoSalList contains the names of Normal (original) video files
    def readOrgData(self, videoID):
        # this function just load the video frame just in case to simulate
        # tile based segementation on top of the video frame
        self.frameListOrg.clear()
        if not self.isAll:
            filePath = self.normInFilePath + "/" + self.videoNormList[videoID] + ".mp4"
            # if not self.isAll:
            #     filePath = self.salInFilePath + "/" + self.videoSalList[self.videoID]
            # filePath = self.normInFilePath + "/" + "DrivingWith" + ".mp4"
            # videoList = os.listdir(filePath)  # dir is your directory path
            # numberOfFiles = len(videoList)

            # for i in range(1):

            # videoFilePath = filePath + "/" + videoList[i]
            # cap = cv2.VideoCapture(filePath)

            # if i == 0:
            #     self.widthSal = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            #     self.heightSal = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            #     self.fpsSal = cap.get(cv2.CAP_PROP_FPS)

            # filePath = self.normInFilePath + "/" + "DrivingWith" + ".mp4"
            cap = cv2.VideoCapture(filePath)
            # frameCount = cap.get(cv2.CAP_PROP_FRAME_COUNT)
            # print(frameCount)
            self.rgbImgSize.append(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.rgbImgSize.append(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            if cap.isOpened:
                sucess = True;
            count = 0;
            while sucess:
                frameNum = self.randomFrames[count]
                retVal = cap.set(cv2.CAP_PROP_POS_FRAMES, frameNum - 1)
                sucess, frame = cap.read()
                # print(frame)
                frameBGR = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # cv2.imshow('video',frame)
                # img = copy.copy(frame)

                # plt.figure(10 + count + 1)
                # plt.imshow(frameBGR)
                # plt.ioff()
                # plt.show(block=False)

                # if i == 0:
                #     self.widthOri = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
                #     self.heightOri = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
                #     self.fpsOri = cap.get(cv2.CAP_PROP_FPS)

                # print(self.width, self.height, frame.shape)

                # for row in range(4):
                #     start_x = 0
                #     start_y = int(row * (frame.shape[0] / 4))
                #     end_x = int(frame.shape[1])
                #     end_y = int(row * (frame.shape[0] / 4))
                #     cv2.line(img, (start_x, start_y), (end_x, end_y), (255, 255, 255), cv2.LINE_AA, 0)
                #
                # for col in range(5):
                #     start_x = int(col * (frame.shape[1] / 5))
                #     start_y = 0
                #     end_x = int(col * (frame.shape[1] / 5))
                #     end_y = int(frame.shape[0])
                #     cv2.line(img, (start_x, start_y), (end_x, end_y), (255, 255, 255), cv2.LINE_AA, 0)

                # path = "E:/Uni_Studies/Useful_Datasets_360\Dataset_3_360_Video_Viewing_Dataset_in_head_mounted_virtual_reality/360dataset/intermediateResults/ori.png"
                # cv2.imwrite(path, img)

                self.frameListOrg.append(frame)
                count += 1
                # print(count)
                if count == ReadData.NUM_OF_FRAMES:
                    break
            cap.release()
            # cv2.destroyAllWindows()

    # This function read any specific video frames from any video file
    # @framNumber : video frame number to be read
    # @videoName : videoName of the video file
    # @videoType : Specifiy whether it is saliency video or original video
    def readAnyVideoSegment(self, frameNumber, videoName, videoType):

        frameList = []
        if videoType == 0:  # if it is a saliency video
            filePath = self.salInFilePath + "/" + videoName + ".mp4"
        else:
            filePath = self.normInFilePath + "/" + videoName + ".mp4"

        cap = cv2.VideoCapture(filePath)

        sucess = False

        if cap.isOpened:
            sucess = True;
        count = 0;
        while sucess:
            # frameNum = self.randomFrames[count]
            retVal = cap.set(cv2.CAP_PROP_POS_FRAMES, frameNumber + count - 1)
            sucess, frame = cap.read()

            # if it is saliency data request convert to GRAY scale
            if videoType == 0:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # if it is normal video data convert to Color scale
            else:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # path = "E:/Uni_Studies/Useful_Datasets_360/Dataset_3_360_Video_Viewing_Dataset_in_head_mounted_virtual_reality/360dataset/intermediateResults/sal.png"
            # cv2.imshow('',colorFrame)

            # plt.figure(count + 1)
            # plt.imshow(frame)
            # plt.ioff()
            # plt.show(block=False)

            # =============================================================================
            # =============================================================================
            #                 cv2.namedWindow('image', cv2.WINDOW_NORMAL)
            #                 cv2.imshow('image',frame)
            #                 cv2.waitKey(5000)
            # =============================================================================
            # =============================================================================

            frameList.append(frame)
            count += 1
            # print(count)
            if count == 15:  # 500ms
                break
        cap.release()
        # cv2.destroyAllWindows()

        return frameList

    # This functino reads set of video frames for given indices from a given normal file containing PNG images
    # @imgIndexList = list containing the images indices to be read
    # @filePath = path for the video file
    # additional : This function was originally created to read the saliency outputs from  PanoSalNet model
    def readImageFrames(self, imgIndexList, filePath):
        onlyfiles = next(os.walk(filePath))[2]
        for i in range(len(imgIndexList)):
            if imgIndexList[i] < len(onlyfiles) * 15:
                tempImagePath = filePath + "/frame" + str(int(imgIndexList[i])) + '.png'
                img = cv2.imread(tempImagePath)

                # get image size and width
                if i == 0:
                    self.panoSalNetSalImgSize.append(img.shape[1])  # width
                    self.panoSalNetSalImgSize.append(img.shape[0])  # height
                self.frameListPanoSal.append(img)

        return

    # This function returns a list containing the meta data of the images read
    # @return : our initial saliency vide frames [width,height]
    #             PanoSalNet frame [width,height]
    #             Original Image [width, height]
    def getImageMetaData(self):

        return [self.initialSalImgSize, self.panoSalNetSalImgSize, self.rgbImgSize]
