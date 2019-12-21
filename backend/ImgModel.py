import numpy as np
import math

from copy import deepcopy
from PIL import Image
from threading import Thread

from IdentifyModel import IdentifyModel

def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target = f, args = args, kwargs = kwargs)
        thr.start()
    return wrapper

class ImgModel:
    base64Img = None
    pilImg = None
    imgId = 0

    identifyModel = None

    def __init__(self):
        self.identifyModel = IdentifyModel()

    def setBase64Image(self, base64Img):
        self.base64Img = base64Img
    
    def getResultbase64Image(self):
        return self.base64Img

    def setPilImage(self, pilImg):
        self.pilImg = pilImg
    
    def getPilImage(self):
        return self.pilImg
 
    def identify(self):
        self.pilImg, identifyList = self.identifyModel.identify(self.pilImg)
        print(identifyList)

    