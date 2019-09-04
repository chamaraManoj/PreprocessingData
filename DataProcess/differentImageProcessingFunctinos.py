import cv2
import numpy as np


class ImageProcessingFunc:

    def __init__(self):
        return

    # function to extract the salient region in the funciton
    def getSalientRegion(self, frameListSal, frameListOri):
        print(type(frameListSal[0]))
        shapeFrame = frameListSal[0].shape
        cv2.imshow('',frameListSal[0])
        for i in range(1):
            finalImage = np.zeros([1080, 1920, 0], int)
            if frameListSal[i].all() > 30:
                alpha = frameListSal[i] / 255
                finalImage = (alpha) * frameListSal[i] + (1 - alpha) * frameListOri[i]

            cv2.imshow('',finalImage)

        return
