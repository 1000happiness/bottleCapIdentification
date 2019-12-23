import numpy as np
import math
import cv2

from copy import deepcopy
from PIL import Image
from IdentifyModel import IdentifyModel
from io import BytesIO
from base64 import b64decode
# import base64
# from io import BytesIO

# from PIL import Image


# def base64_to_image(base64_str, image_path=None):
#     base64_data = re.sub('^data:image/.+;base64,', '', base64_str)
#     byte_data = base64.b64decode(base64_data)
#     image_data = BytesIO(byte_data)
#     img = Image.open(image_data)
#     if image_path:
#         img.save(image_path)
#     return img
class ImgModel:
    base64InputImg = None
    base64ResultImg = None
    resultList = []
    formalResultList = []
    pilImg = None
    #imgId = 0

    identifyModel = None

    def __init__(self):
        self.identifyModel = IdentifyModel()

    def setBase64Img(self, base64Img):
        self.base64InputImg = base64Img
        self.base64ResultImg = base64Img
        self.pilImg = Image.open(BytesIO(self.base64InputImg))
        # self.resultList = [((0,0),(2,0),(2,2),(0,2),(0,0,-1))]
        self.formalResultList = []
        for i in range(len(self.resultList)):
            location = "(" + str((self.resultList[i][0][0] + self.resultList[i][2][0]) / 2) + ","  + str((self.resultList[i][0][1] + self.resultList[i][2][1]) / 2) + ")"
            directionDescription = None
            if(self.resultList[i][4][2] == 1):
                directionDescription = "上"
            elif(self.resultList[i][4][2] == -1):
                directionDescription = "下"
            else:
                directionDescription = "侧"

            self.formalResultList.append(
                {
                    "id": i,
                    "location": location,
                    "directionDescription": directionDescription,
                    "direction": str(self.resultList[i][4])
                }
            )
    
    def getInputbase64Img(self):
        return self.base64InputImg
    
    def getResultbase64Img(self):
        return self.base64ResultImg

    def getFormalResultList(self):
        return self.formalResultList

    def setPilImg(self, pilImg):
        self.pilImg = self.__preProcess(pilImg)
    
    def getPilImg(self):
        return self.pilImg
 
    def identify(self):
        self.pilImg, self.resultList = self.identifyModel.identify(self.pilImg)
        for i in range(self.resultList):
            location = "(" + str((self.resultList[i][0][0] + self.resultList[i][2][0]) / 2) + ","  + str((self.resultList[i][0][1] + self.resultList[i][2][1]) / 2) + ")"
            directionDescription = None
            if(self.resultList[i][4][2] == 1):
                directionDescription = "上"
            elif(self.resultList[i][4][2] == -1):
                directionDescription = "下"
            else:
                directionDescription = "侧"

            self.formalResultList.append(
                {
                    "id": i,
                    "location": location,
                    "directionDescription": directionDescription,
                    "direction": str(self.resultList[i][4])
                }
            )
        print(self.resultList)

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
