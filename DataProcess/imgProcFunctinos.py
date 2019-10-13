# This class contains funcions that contains different image display funcitons.
import cv2
import numpy as np

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
    # @return: adjusted image
    def brightnessContrastAdjust(self, image, alpha, beta, videoType):

        #new_image = np.zeros(image.shape, image.dtype)

        # for y in range(image.shape[0]):
        #     for x in range(image.shape[1]):
        #         if videoType == settings.RGB_VIDEO:
        #             for c in range(image.shape[2]):
        #                 new_image[y, x, c] = np.clip(alpha * image[y, x, c] + beta, 0, 255)
        #         elif videoType == settings.SALIENCY_VIDEO:
        filepath = r"E:\Dataset\PanoSalMaps\test_beta_alpha_values"
        dim = (image.shape[1]//4,image.shape[0]//4)
        alphalist = np.arange(0.5,5.0,0.1)
        for alpha in alphalist:
            print(alpha)
            for beta in range(10,60,5):
                print("   "+str(beta))
                new_image = np.uint8(np.clip( alpha* image + 30, 0, 255))

                new_image = cv2.resize(new_image, dim, interpolation=cv2.INTER_AREA)
                image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

                vis = np.concatenate((new_image, image), axis=1)
                imPath = filepath+"\\"+str(alpha)+"_"+str(beta)+".png"
                cv2.imwrite(imPath,vis)





        # Wait until user press some key
        cv2.waitKey()

        return new_image
