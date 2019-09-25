import cv2
import copy
import matplotlib.pyplot as plt
import math


# This class contains following functions
class ProcessData:
    threshImages = []
    qualityList = []
    linearThresh = True;

    QUALITY_LEVEL_1 = float(1 / 2);
    QUALITY_LEVEL_2 = float(1 / 4);

    def __init__(self, frameList, tileTuple, width, hieght, qualityTuple, qualityList, numOfRow, numOfCol):
        self.frameList = frameList
        self.tileTupple = tileTuple
        self.width = width
        self.hieght = hieght
        self.qualityTuple = qualityTuple
        self.tileArea = (width * hieght) / 20
        self.NUM_OF_ROW = numOfRow
        self.NUM_OF_COL = numOfCol

    def thresholdImage(self):
        'Threshold the image and process image. function fill the list for \
         thresholded images and frame encoding sets'
        # =============================================================================
        #
        #         In the imeplementation:
        #             1. extract the high saliency region
        #             2. according to the grid settings, for each tile, fins what portion
        #                portion of the area is covered by the saliency region
        #             3. considering covered area assign the values for bit rate
        #
        # =============================================================================

        for frame in self.frameList:

            # threshold the image using simple binaray thresholding
            if self.linearThresh:
                sucess, threshImage = cv2.threshold(frame, 30, 255, cv2.THRESH_BINARY)

            # if the thresholding sucess append to the thresholded images
            if sucess:
                self.threshImages.append(threshImage)
                img = copy.copy(threshImage)
                for row in range(self.NUM_OF_ROW):
                    start_x = 0
                    start_y = int(row * (self.hieght / self.NUM_OF_ROW))
                    end_x = int(self.width)
                    end_y = int(row * (self.hieght / self.NUM_OF_ROW))
                    cv2.line(img, (start_x, start_y), (end_x, end_y), (255, 255, 255), cv2.LINE_AA, 0)

                for col in range(self.NUM_OF_COL):
                    start_x = int(col * (self.width / self.NUM_OF_COL))
                    start_y = 0
                    end_x = int(col * (self.width / self.NUM_OF_COL))
                    end_y = int(self.hieght)
                    cv2.line(img, (start_x, start_y), (end_x, end_y), (255, 255, 255), cv2.LINE_AA, 0)

                path = "E:/Uni_Studies/Useful_Datasets_360\Dataset_3_360_Video_Viewing_Dataset_in_head_mounted_virtual_reality/360dataset/intermediateResults/sal2.png"
                cv2.imwrite(path, img)
                plt.imshow(img)
                plt.show()


            else:
                print("Image thresholding failed", frame)
                break
            tempQuality = []
            for row in range(self.NUM_OF_ROW):
                for col in range(self.NUM_OF_COL):
                    # tileNum = row * self.numOfCol + col

                    # defining the starting and endpoints of a tile
                    startPixel_x = int(self.width * (col / self.NUM_OF_COL))
                    endPixel_x = int(self.width * ((col + 1) / self.NUM_OF_COL))

                    # if the tiles are fallen into first and last and row
                    if row == 0:
                        startPixel_y = int(math.ceil(self.hieght * ((row + 1) / self.NUM_OF_ROW) / 2))
                        endPixel_y = int(self.hieght * ((row + 1) / self.NUM_OF_ROW))

                    elif row == 3:
                        startPixel_y = int(self.hieght * (row / self.NUM_OF_ROW))
                        endPixel_y = int(math.ceil(self.hieght * ((row + 1) / self.NUM_OF_ROW) / 2))

                    else:
                        startPixel_y = int(self.hieght * (row / self.NUM_OF_ROW))
                        endPixel_y = int(self.hieght * (row + 1) / self.NUM_OF_ROW)

                    # scan pixel in the tile if the pixel in the saliency region
                    # increase the count by one
                    numOfthreshPixels = 0

                    # print(row," ",col," ",startPixel_y," ",endPixel_y," ",startPixel_x," ",endPixel_x," ",self.width," ",self.hieght )
                    for pixel_x in range(startPixel_x, endPixel_x):
                        for pixel_y in range(startPixel_y, endPixel_y):
                            if self.linearThresh:
                                if threshImage[pixel_y][pixel_x] == 255:
                                    numOfthreshPixels += 1

                    # if the thresholded pixel count is more than 3/4 of the given tile
                    #   highest quality for the tile
                    # if the thresholded pixel count is more than 1/2 of the given tile
                    #   moderate quality for the tile
                    # if the thresholded pixel count is less than 1/2 of the given tile
                    #   lowest quality for the tile
                    threshPropotion = numOfthreshPixels / float(self.tileArea)

                    # print("threshPropotion ",threshPropotion,"tileArea ",self.tileArea,"numOfthreshPixels ",numOfthreshPixels)

                    if threshPropotion > self.QUALITY_LEVEL_1:
                        tempQuality.append(self.qualityTuple[2])

                    elif threshPropotion > self.QUALITY_LEVEL_2:
                        tempQuality.append(self.qualityTuple[1])

                    else:
                        tempQuality.append(self.qualityTuple[0])

            self.qualityList.append(tempQuality)

            for i in range(self.numOfRow):
                for j in range(self.numOfCol):
                    print(tempQuality[i * self.numOfCol + j], end=" ")
                print(" ")
