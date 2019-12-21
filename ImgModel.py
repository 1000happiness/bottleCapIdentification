import numpy as np
import math

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
        self.pilImg = pilImg
    
    def getPilImg(self):
        return self.pilImg
 
    def identify(self):
        self.pilImg, identifyList = self.identifyModel.identify(self.pilImg)
        print(identifyList)

    def __preProcess(self):
        pass