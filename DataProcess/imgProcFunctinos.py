# This class contains funcions that contains different image display funcitons.
import cv2
import numpy as np
import os

from DataProcess import settings


class displayFuncitons:

    def __init__(self):
        return

    # This function draw FoV area on top of the both original and the saliency image
    # @fovTileList :  tile list containing the fov tiles in the function
    # @ salImg : saliency image that fov tiles should be drawn
    # @ oriImg : origninal image that the fov tiles should be drawn on
    def fovTiles(self, fovTileList, salImg, oriImg):
        return

    # This fucntion change the brightness and contrast of an given image
    # @image : image to be controlled
    # @alpha : coefficient to chang ethe contrastness
    # @beta : coefficient to change the brightness
    # @videoType: Type of the video, whether it is Saliency map or RGB map
    # @return: adjusted image
    def brightnessContrastAdjust(self, image, alpha, beta, videoType):

        # new_image = np.zeros(image.shape, image.dtype)

        # for videoName in videoSaliencyNameList:
        #
        #     image = cv2.imread(r"H:\Dataset\PanoSalMaps"+"\\"+videoName+"\\" +"frame465.png")
        #
        #     filepath = r"H:\Dataset\PanoSalMaps\test_beta_alpha_values_"+videoName
        #     if not os.path.exists(filepath):
        #         os.makedirs(filepath)
        #
        dim = (image.shape[1] // 4, image.shape[0] // 4)

        # alphalist = np.arange(0.5, 5.0, 0.1)

        cropMargin = 15

        crop_img = image[cropMargin:image.shape[0] - cropMargin, cropMargin:image.shape[1] - cropMargin]
        # crop_img = cv2.resize(crop_img, (image.shape[1] // 2, image.shape[0] // 2), interpolation=cv2.INTER_AREA)
        # cv2.imshow("test", crop_img)
        # cv2.waitKey()

        maxVal = np.amax(crop_img)
        minVal = np.amin(crop_img)

        clipPercent = 5
        if minVal == 0:
            minVal = np.round(maxVal * (clipPercent / 100))
        else:
            minVal = np.round(minVal * (1 + clipPercent / 100))

        image[image < minVal] = np.uint8(minVal)
        image = cv2.resize(image, (image.shape[1] // 4, image.shape[0] // 4), interpolation=cv2.INTER_AREA)

        # for alpha in alphalist:
        #     print(alpha)
        #     for beta in range(0, 60, 5):
        #         print("   " + str(beta))
        new_image = np.uint8(np.clip(alpha * image - beta, 0, 255))

        # new_image = cv2.resize(new_image, dim, interpolation=cv2.INTER_AREA)
        # image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

        # vis = np.concatenate((new_image, image), axis=1)
        # imPath = filepath + "\\" + str(alpha) + "_" + str(beta) + ".png"
        # cv2.imwrite(imPath, vis)

        # Wait until user press some key

        return new_image
