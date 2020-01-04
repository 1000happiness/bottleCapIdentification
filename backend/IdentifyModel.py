import numpy as np
import math
import cv2

from PIL import Image

from copy import deepcopy 

class IdentifyModel:
    def __init__(self):
        self.positiveCap = positiveCap()
        self.node_location_list1=[]
        self.node_location_list2=[]
        self.node_location_list3=[]
        self.node_location_list4=[]
        self.direction_list=[]

    def identify(self, inputPilImg):
        self.node_location_list1=[]
        self.node_location_list2=[]
        self.node_location_list3=[]
        self.node_location_list4=[]
        self.direction_list=[]
        inputCVImg = cv2.cvtColor(np.array(inputPilImg), cv2.COLOR_RGBA2RGB)
        '''
        返回的list里面前两个元组表示瓶盖所在的长方体的对角线的两个点
        第三个元组表示瓶盖平面归一化的法向量(x,y,z)
        如果是正面朝上则为(0,0,1)
        如果正面朝下则为(0,0,-1)
        如果是侧面则为(1,0,0)
        具体的方向值按照结果确定
        '''
        widthRate = inputPilImg.size[0] / 400
        heightRate = inputPilImg.size[1] / 300
        rate = max(widthRate, heightRate)
        sizedPilImg = deepcopy(inputPilImg)
        sizedPilImg = sizedPilImg.resize((int(inputPilImg.size[0] / rate), int(inputPilImg.size[1] / rate)))

        cvImg = cv2.cvtColor(np.array(sizedPilImg), cv2.COLOR_BGR2GRAY)
        cvImg = cv2.medianBlur(cvImg, 11)
        cannyImg = cv2.Canny(cvImg, 5, 80)

        # cv2.imshow("1", cannyImg)
        # cv2.waitKey()
        
        edgeImg, contours, hier = cv2.findContours(cannyImg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # 检测边缘
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)

            # 用一个最小的矩形，把找到的形状包起来,还有一个带旋转的矩形
            # 返回(x,y)为矩形左上角坐标，w,h分别是宽和高
            # cv2.rectangle(cvImg,(x,y),(x+w,y+h),(0,255,0),2)#确定对角线然后画出矩阵
            
            if x != 0 and y != 0 and 100>w >= 10 and 100>h >= 10:
                if (1 < (w / h) < 1.15 or 0.85 < (w / h) < 1 or (w / h) == 1):
                    #显示正反面瓶盖矩形
                    self.node_location_list1.append((x*rate,y*rate))
                    self.node_location_list2.append((x*rate,(y+h)*rate))
                    self.node_location_list3.append(((x+w)*rate,(y+h)*rate))
                    self.node_location_list4.append(((x+w)*rate,y*rate))
                    if(self.positiveCap.judgePositive(inputCVImg[int(y*rate - 50): int((y+h)*rate + 50), int(x*rate - 50): int((x+w)*rate + 50)])):
                        self.direction_list.append((0,0,1))
                    else:
                        self.direction_list.append((0,0,-1))
                    continue

            rect = cv2.minAreaRect(c)  # 找到最小矩形区域
            
            if 100 >rect[1][0] > 10 and 100 >rect[1][1] > 10:
                box = cv2.boxPoints(rect)  # 找到最小矩形的顶点
                #显示侧面请转换box格式，见下
                # box = np.int0(box)
                if ((rect[1][0] / rect[1][1]) > 1.2 or 0 < (rect[1][0] / rect[1][1]) < 0.8):
                    #显示侧面矩形轮廓

                    self.node_location_list1.append(box[0]*(rate,rate))
                    self.node_location_list2.append(box[1]*(rate,rate))
                    self.node_location_list3.append(box[2]*(rate,rate))
                    self.node_location_list4.append(box[3]*(rate,rate))
                    self.direction_list.append((
                        round(rect[1][0] / math.hypot(rect[1][0],rect[1][1]), 3),
                        round(rect[1][1] / math.hypot(rect[1][0],rect[1][1]), 3),
                        0
                    ))
        
        returnList = []
        for i in range(len(self.node_location_list1)):
            returnItem = (
                self.node_location_list1[i],
                self.node_location_list2[i],
                self.node_location_list3[i],
                self.node_location_list4[i],
                self.direction_list[i]
            )
            returnList.append(returnItem)
        return returnList

class positiveCap:
    def __init__(self):
        self.i = 0
        pass

    # 把图像灰度化
    def _gray(self, img):
        return cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)

    # 调整图像对比度
    def _alpha(self, img,alpha):
        mean = cv2.mean(self._gray(img))[0]
        # mean = 127
        beta = mean*(1-alpha)
        return np.uint8(np.clip((alpha * img + beta), 0, 255))

    # 主要过程，返回图中包含的圆的数量
    def _proc(self, img):
        # name = input()
        # img = cv2.imread(name + '.png')
        width = len(img[0])
        height = len(img)
        # result = cv2.bilateralFilter(img,5,11,11)
        # result = self._alpha(result,1.6)
        result = cv2.blur(img, (7,7))
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
        result = cv2.morphologyEx(result,cv2.MORPH_CLOSE,kernel)
        kernel2 = np.array([[0, -0.2, 0], [-0.2, 1.8, -0.2], [0, -0.2, 0]])
        result = cv2.filter2D(result,-1,kernel2)
        # cv2.imshow('?',result)
        gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
        canny = cv2.Canny(gray, 12.5, 25)
        # cv2.imshow('2', canny)
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1,
                                (width / 12), param1=25, param2=80, minRadius=int(width / 6))

        num = 0
        if(circles is not None):
            # print(len(circles[0]))

            # print('------------------------------')
            for circle in circles[0]:
                x = int(circle[0])
                y = int(circle[1])
                r = int(circle[2])

                delta = width / 10
                if width / 2 - delta <= x <= width / 2 + delta:
                    if height / 2 - delta <= y <= height / 2 + delta:
                        num = num+1
                        img = cv2.circle(img, (x, y), r, (0, 255, 0), 1, 8, 0)

        # cv2.imshow(name, img)
        # print("circle num is "+str(num))
        return num

    # 判断正反，圆的数量<=3即正面
    def judgePositive(self, img):
        pil = Image.fromarray(img)
        pil.save(str(self.i) + ".jpg", quality = 95)
        self.i = self.i + 1
        num = self._proc(img)
        return num <= 3

if __name__ == "__main__":
    image = Image.open("save.jpg")
    IdentifyModel = IdentifyModel()
    IdentifyModel.identify(image)