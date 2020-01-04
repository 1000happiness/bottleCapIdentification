import numpy as np
import math
import cv2

from copy import deepcopy
from PIL import Image
from IdentifyModel import IdentifyModel
from io import BytesIO
from base64 import b64decode, b64encode

class ImgModel:
    base64InputImg = None
    base64ResultImg = None
    formalResultList = []
    pilImg = None
    shape = None
    newSize = None

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

    # not use
    def setPilImg(self, pilImg):
        self.pilImg = pilImg
        
        self.pilImg = self.__deleteAround(self.pilImg)

    #not use
    def getPilImg(self):
        return self.pilImg

    def getImgShape(self):
        return self.shape

    def identify(self):
        # identify
        resultList = self.identifyModel.identify(self.identifyPilImg)
        # afterProcess
        self.__afterProcess(resultList)
        
    def __beforeProcess(self):
        # 初始化
        self.pilImg = Image.open(BytesIO(self.base64InputImg))
        self.shape = np.array(self.pilImg, dtype="f").shape
        self.formalResultList = []

        #去除周边
        self.identifyPilImg, self.newSize = self.__deleteAround(self.pilImg)

    def __afterProcess(self, resultList):
        locationData = np.zeros((len(resultList), 4, 2))
        for i in range(len(resultList)):
            for k in range(4):
                locationData[i][k][0] = resultList[i][k][0] + self.newSize[2]
                locationData[i][k][1] = resultList[i][k][1] + self.newSize[0]
            location = str(round((locationData[i][0][1] + locationData[i][2][1]) / 2, 1)) + ", " + str(round((locationData[i][0][0] + locationData[i][2][0]) / 2, 1)) 
            directionDescription = None
            if(resultList[i][4][2] == 1):
                directionDescription = "上"
            elif(resultList[i][4][2] == -1):
                directionDescription = "下"
            else:
                directionDescription = "侧"

            self.formalResultList.append(
                {
                    "id": i + 1,
                    "location": location,
                    "directionDescription": directionDescription,
                    "direction": str(resultList[i][4])
                }
            )
        self.pilImg = self.__SignImg(locationData)

        outputBuffer = BytesIO()
        self.pilImg.save(outputBuffer, format='JPEG')
        byteData = outputBuffer.getvalue()
        self.base64ResultImg = byteData

    def __SignImg(self, resultList):
        cvImg = cv2.cvtColor(np.array(self.pilImg),cv2.COLOR_RGBA2RGB)
        # print(cvImg)
        for i in range(len(resultList)):
            square = np.array([resultList[i][2], resultList[i][1], resultList[i][0], resultList[i][3]], np.int32)
            square = square.reshape((-1,1,2))
            cv2.polylines(cvImg,[square],True,(255, 255,255), 6)
            cv2.putText(cvImg, str(i + 1), (int((resultList[i][2][0] + resultList[i][0][0]) / 2), int((resultList[i][2][1] + resultList[i][0][1]) / 2)), 6, int(np.array(cvImg).shape[0] / 800), (255, 255, 255), int(np.array(cvImg).shape[0] / 800))

        return Image.fromarray(cvImg)

    def __deleteAround(self, pilImg):
        #去除周边
        widthRate = pilImg.size[0] / 480
        heightRate = pilImg.size[1] / 270
        rate = max(widthRate, heightRate)
        sizedpilImg = pilImg.resize((int(pilImg.size[0] / rate), int(pilImg.size[1] / rate)))
        
        npImg = np.array(sizedpilImg)
        left, right = self.__deleteColAround(npImg)
        low, high = self.__deleteRowAround(npImg)
        # low, high = 0,0

        npImg = np.array(pilImg)
        left = int(left * rate)
        right = int(right * rate)
        low = int (low * rate)
        high = int(high * rate)
        newnpImg = deepcopy(npImg[low: high,left: right])
        identifyImg = Image.fromarray(newnpImg)

        return identifyImg, (low, high, left, right)

    def __deleteColAround(self, npImg):
        cvImg = cv2.cvtColor(npImg, cv2.COLOR_RGB2GRAY)
        cvImg = cv2.medianBlur(cvImg, 11)
        cannyImg = cv2.Canny(cvImg, 5, 80)

      
        
        col = []
        k = 0
        colRange = 15
        while (k <= np.array(cannyImg).shape[1] - colRange):
            if(np.any(cannyImg[100][k: k + colRange] == 255)):
                length = 0
                for i in range(0, np.array(cannyImg).shape[0]):
                    if(np.any(cannyImg[i][k: k + colRange] == 255)):
                        length = length + 1
                if(length > 160):
                    if(k > np.array(cannyImg).shape[1] / 2):
                        col.append(k)
                    else:
                        col.append(k + colRange)
                    
                k = k + colRange
            else:
                k = k + colRange
        if(len(col) < 2):
            return 0, -1
        first = 0
        second = 0

        if(len(col) > 2):
            colValue = np.zeros(len(col))
            gaussianImg = cv2.GaussianBlur(cvImg, (11,11), 3)
            gaussiancannyImg = cv2.Canny(gaussianImg, 5, 80)
            for k in range(np.array(gaussiancannyImg).shape[1]):
                left = 0
                right = 1
                if(col[left] <= k):
                    while(col[right] <= k):
                        left = left + 1
                        right = right + 1
                        if(right == len(col)):
                            break
                    if(right == len(col)):
                        break
                else:
                    continue
                for i in range(np.array(gaussiancannyImg).shape[0]):
                    if(gaussiancannyImg[i][k] == 255):
                        colValue[left] = colValue[left] + 1
                        colValue[right] = colValue[right] + 1
            
            for i in colValue:
                if(i > colValue[first]):
                    first = first + 1
            for i in range(len(colValue)):
                if(i != first):
                    if(colValue[i] > second):
                        second = i
        else:
            second = 1

        left = col[first]
        right = col[second]
        
        return left, right

    def __deleteRowAround(self, npImg):
        cvImg = cv2.cvtColor(npImg, cv2.COLOR_RGB2GRAY)
        cvImg = cv2.medianBlur(cvImg, 11)
        cannyImg = cv2.Canny(cvImg, 5, 80)
        row = []
        i = 0
        rowRange = 15
        while (i < np.array(cannyImg).shape[0] - rowRange):
            if(np.any(cannyImg[i : i + rowRange, 100] == 255)):
                length = 0
                for k in range(np.array(cannyImg).shape[1]):
                    if(np.any(cannyImg[i: i + rowRange, k] == 255)):
                        length = length + 1
                if(length > np.array(cannyImg).shape[1] / 3):
                    if(i > np.array(cannyImg).shape[0] / 2):
                        row.append(i)
                    else:
                        row.append(i + rowRange)
                i = i + rowRange
            else:
                i = i + rowRange
        if(len(row) < 2):
            return 0, -1
        first = 0
        second = 0

        if(len(row) > 2):
            rowValue = np.zeros(len(row))
            gaussianImg = cv2.GaussianBlur(cvImg, (11,11), 3)
            gaussiancannyImg = cv2.Canny(gaussianImg, 5, 80)
            for i in range(np.array(gaussiancannyImg).shape[0]):
                low = 0
                high = 1
                if(row[low] <= i):
                    while(row[high] <= i):
                        low = low + 1
                        high = high + 1
                        if(high == len(row)):
                            break
                    if(high == len(row)):
                        break
                else:
                    continue
                for i in range(np.array(gaussiancannyImg).shape[0]):
                    if(gaussiancannyImg[i][k] == 255):
                        rowValue[low] = rowValue[low] + 1
                        rowValue[high] = rowValue[high] + 1
            
            for i in rowValue:
                if(i > rowValue[first]):
                    first = first + 1
            for i in range(len(rowValue)):
                if(i != first):
                    if(rowValue[i] > second):
                        second = i
        else:
            second = 1

        low = row[first]
        high = row[second]
        
        return low, high