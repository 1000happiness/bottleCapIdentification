import numpy as np
import math
import cv2

from copy import deepcopy
from PIL import Image
from IdentifyModel import IdentifyModel
from io import BytesIO
from base64 import b64decode, b64encode

from time import sleep

class ImgModel:
    base64InputImg = None
    base64ResultImg = None
    formalResultList = []
    pilImg = None
    shape = None
    #imgId = 0

    identifyModel = None

    def __init__(self):
        self.identifyModel = IdentifyModel()

    def setBase64Img(self, base64Img):
        self.base64InputImg = base64Img
        self.__beforeProcess()
    
    def getInputbase64Img(self):
        return self.base64InputImg
    
    def getResultbase64Img(self):
        
        return self.base64ResultImg

    def getFormalResultList(self):
        
        return self.formalResultList

    def setPilImg(self, pilImg):
        self.pilImg = pilImg
        
        cvImg = cv2.cvtColor(np.array(self.pilImg),cv2.COLOR_RGB2GRAY)
        # print(np.array(pilImg.convert("L")))
        cvImg = cv2.medianBlur(cvImg, 5)
        # cvImg = cv2.Canny(cvImg, 45, 70)

        self.pilImg = Image.fromarray(cvImg)

    def getPilImg(self):
        return self.pilImg

    def getImgShape(self):
        return self.shape

    def identify(self):
        # identify
        self.pilImg, resultList = self.identifyModel.identify(self.pilImg)
        
        # afterProcess
        self.__afterProcess(resultList)
        

    def __beforeProcess(self):
        # 初始化
        self.pilImg = Image.open(BytesIO(self.base64InputImg))
        self.shape = np.array(self.pilImg, dtype="f").shape
        self.formalResultList = []

    def __afterProcess(self, resultList):
        for i in range(len(resultList)):
            location = "(" + str((resultList[i][0][0] + resultList[i][2][0]) / 2) + ","  + str((resultList[i][0][1] + resultList[i][2][1]) / 2) + ")"
            directionDescription = None
            if(resultList[i][4][2] == 1):
                directionDescription = "上"
            elif(resultList[i][4][2] == -1):
                directionDescription = "下"
            else:
                directionDescription = "侧"

            self.formalResultList.append(
                {
                    "id": i,
                    "location": location,
                    "directionDescription": directionDescription,
                    "direction": str(resultList[i][4])
                }
            )
        self.__SignImg(resultList)

        outputBuffer = BytesIO()
        self.pilImg.save(outputBuffer, format='JPEG')
        byteData = outputBuffer.getvalue()
        self.base64ResultImg = byteData

    def __SignImg(self, resultList):
        cvImg = cv2.cvtColor(np.array(self.pilImg),cv2.COLOR_RGBA2RGB)
        # print(cvImg)
        for item in resultList:
            square = np.array([item[0], item[1], item[2], item[3]], np.int32)
            square = square.reshape((-1,1,2))
            cv2.polylines(cvImg,[square],True,(255, 255,255), 6)

        self.pilImg = Image.fromarray(cvImg)