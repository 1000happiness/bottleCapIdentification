import cv2
import matplotlib.pyplot as plt
import numpy as np

font = cv2.FONT_HERSHEY_SIMPLEX  # 使用默认字体


img =cv2.imread('test.png',cv2.IMREAD_UNCHANGED)

img1 = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(img1,127,255,cv2.THRESH_BINARY_INV)
#先将图像转化成灰度，再转化成二值图像

contours,hier=cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
#检测边缘

for c in contours:
    x,y,w,h = cv2.boundingRect(c)
    #用一个最小的矩形，把找到的形状包起来,还有一个带旋转的矩形
    #返回(x,y)为矩形左上角坐标，w,h分别是宽和高
    #cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)#确定对角线然后画出矩阵

    rect = cv2.minAreaRect(c)#找到最小矩形区域
    if rect[0]!=0 and rect[1][0]!=0 and rect[1][1]!=0 and rect[2] != 0 :
        box = cv2.boxPoints(rect)  # 找到最小矩形的顶点
        box = np.int(box)
        print(rect[0])
        print(rect[1][0])
        print(rect[1][1])
        print(rect[2])
        if 1 < (rect[1][0] / rect[1][1]) < 1.1 or 0.9 < (rect[1][0] / rect[1][1]) < 1:
            bottle_class = "front or reverse"
            print("正面")
            cv2.drawContours(img, [box], 0, (0, 0, 255), 3)
            cv2.putText(img, bottle_class + ' ' + '('+str(int(rect[0][0]))+','+str(int(rect[0][1]))+')', (int(rect[0][0]),int(rect[0][1])), font, 0.4,(255, 0, 0), 1)
        else :
            print("侧面")
            bottle_class = "side"
            cv2.drawContours(img, [box], 0, (0, 255, 0), 3)
            cv2.putText(img, bottle_class + ' ' + '('+str(int(rect[0][0]))+','+str(int(rect[0][1]))+')',(int(rect[0][0]),int(rect[0][1])), font, 0.4,(255, 0, 0), 1)


cv2.resizeWindow('contours',200, 200)
cv2.imshow('contours',img)
cv2.imwrite("test_detection.jpg", img)
cv2.waitKey()



