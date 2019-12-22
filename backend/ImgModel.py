import numpy as np
import math
import cv2

from copy import deepcopy
from PIL import Image
from IdentifyModel import IdentifyModel

class ImgModel:
    base64Img = None
    pilImg = None
    imgId = 0

    identifyModel = None

    def __init__(self):
        self.identifyModel = IdentifyModel()

    def setBase64Img(self, base64Img):
        self.base64Img = base64Img
    
    def getResultbase64Img(self):
        return self.base64Img

    def setPilImg(self, pilImg):
        self.pilImg = self.__preProcess(pilImg)
    
    def getPilImg(self):
        return self.pilImg
 
    def identify(self):
        self.pilImg, identifyList = self.identifyModel.identify(self.pilImg)
        print(identifyList)

    def __preProcess(self, pilImg):
        npImg = np.asarray(pilImg)
        # 去除除了白纸之外的背景，并把白纸置黑
        npImg = self.__backgroundProcess(pilImg)

        #cvImg = cv2.cvtColor(npImg)
        # cv2.imshow("OpenCV",cvImg)
        # cv2.waitKey()
        return Image.fromarray(npImg)

    def __backgroundProcess(self, pilImg):
        npImg = np.array(pilImg)
        print(npImg.shape)
        cvImg = cv2.cvtColor(npImg,cv2.COLOR_BGR2RGB)
        cvImg = cv2.blur(cvImg, (5,5))
        # counts = np.zeros(13, dtype=int)
        # print(counts)
        # for i in range(npImg.shape[0]):
        #     for k in range(npImg.shape[1]):
        #         index = int(npImg[i][k] / 20)
        #         counts[index] = counts[index] + 1 
        # #返回众数
        # print(counts)

        # total = npImg.shape[0] * npImg.shape[1]
        # for i in range(len(counts)):
        #     if(counts[i] / total > 0.15):
        #         npRange = (npImg < 20 * i + 20) * (20 * i < npImg)
        #         npImg[npRange] = 0
        #     elif(counts[i] / total < 0.03):
        #         npRange = (npImg < 20 * i + 20) * (20 * i < npImg)
        #         npImg[npRange] = 0


        return cvImg
