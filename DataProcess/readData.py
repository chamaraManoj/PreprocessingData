import cv2
import matplotlib.pyplot as plt
import copy
import os
import random


class ReadData:
    NUM_OF_FRAMES = 1

    # salInFilePath = "E:\Dataset\ProcessedVideoSaliency"
    salInFilePath = "E:/Dataset/RawSaliencyData"
    normInFilePath = "E:/Dataset/RawVideoOriginal"

    frameListSal = []
    frameListOrg = []
    randomFrames = []

    def __init__(self, videoSalList, videoNormList, isAll, videoId):
        self.videoSalList = videoSalList
        self.isAll = isAll
        self.videoID = videoId
        self.videoNormList = videoNormList

    def generateRandomFrames(self, fps, length, frameCount):
        for i in range(int(length)):
            tempRanFrame = (i * 30 + random.randint(0, fps)) / frameCount
            if tempRanFrame <= self.frameCount:
                self.frameListSal.append(tempRanFrame)
        return

    def readSalData(self):
        # Read specific video data to frame list

        if not self.isAll:
            filePath = self.salInFilePath + "/" + self.videoSalList[self.videoID] + ".mp4"
            # videoList = os.listdir(filePath)  # dir is your directory path
            # numberOfFiles = len(videoList)

            for i in range(1):

                # videoFilePath = filePath + "/" + videoList[i]
                cap = cv2.VideoCapture(filePath)

                if i == 0:
                    self.widthSal = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
                    self.heightSal = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
                    self.fpsSal = cap.get(cv2.CAP_PROP_FPS)
                    cap.set(cv2.CAP_PROP_POS_AVI_RATIO, 1)
                    self.lengthSal = cap.get(cv2.CAP_PROP_POS_MSEC)
                    cap.set(cv2.CAP_PROP_POS_AVI_RATIO, 0)
                    self.frameCount = cap.get(cv2.CAP_PROP_FRAME_COUNT)

                    self.generateRandomFrames(self.fpsSal, self.lengthSal / 1000, self.frameCount)

                count = 0
                sucess = False

                if cap.isOpened:
                    sucess = True;

                while sucess:
                    frameNum = self.frameListSal[count]
                    retVal = cap.set(cv2.CAP_PROP_POS_FRAMES, frameNum)
                    sucess, frame = cap.read()

                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    # path = "E:/Uni_Studies/Useful_Datasets_360/Dataset_3_360_Video_Viewing_Dataset_in_head_mounted_virtual_reality/360dataset/intermediateResults/sal.png"
                    # cv2.imwrite(path,frame)

                    plt.imshow(frame)
                    plt.show()
                    # =============================================================================
                    # =============================================================================
                    #                 cv2.namedWindow('image', cv2.WINDOW_NORMAL)
                    #                 cv2.imshow('image',frame)
                    #                 cv2.waitKey(5000)
                    # =============================================================================
                    # =============================================================================

                    self.frameListSal.append(frame)
                    count += 1
                    print(count)
                    # if count == ReadData.NUM_OF_FRAMES:
                    #     break
                cap.release()
                cv2.destroyAllWindows()

    def readOrgData(self):
        # this function just load the video frame just in case to simulate
        # tile based segementation on top of the video frame
        if not self.isAll:

            # if not self.isAll:
            #     filePath = self.salInFilePath + "/" + self.videoSalList[self.videoID]
            filePath = self.normInFilePath + "/" + "DrivingWith" + ".mp4"
            videoList = os.listdir(filePath)  # dir is your directory path
            numberOfFiles = len(videoList)

            for i in range(numberOfFiles):

                videoFilePath = filePath + "/" + videoList[i]
                cap = cv2.VideoCapture(videoFilePath)

                if i == 0:
                    self.widthSal = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
                    self.heightSal = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
                    self.fpsSal = cap.get(cv2.CAP_PROP_FPS)

            filePath = self.normInFilePath + "/" + "DrivingWith" + ".mp4"
            cap = cv2.VideoCapture(filePath)

            if cap.isOpened:
                sucess = True;
            count = 0;
            while sucess:
                sucess, frame = cap.read()
                # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                count += 1
                img = copy.copy(frame)

                if i == 0:
                    self.widthOri = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
                    self.heightOri = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
                    self.fpsOri = cap.get(cv2.CAP_PROP_FPS)

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

                path = "E:/Uni_Studies/Useful_Datasets_360\Dataset_3_360_Video_Viewing_Dataset_in_head_mounted_virtual_reality/360dataset/intermediateResults/ori.png"
                cv2.imwrite(path, img)

                plt.imshow(img)
                plt.show()
                if count == 1:
                    break
