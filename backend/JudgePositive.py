import cv2
import numpy as np

# 把图像灰度化
def _gray(img):
    return cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)

# 调整图像对比度
def _alpha(img,alpha):
    mean = cv2.mean(_gray(img))[0]
    # mean = 127
    beta = mean*(1-alpha)
    return np.uint8(np.clip((alpha * img + beta), 0, 255))

# 主要过程，返回图中包含的圆的数量
def _proc(img):
    # name = input()
    # img = cv2.imread(name + '.png')
    width = len(img[0])
    height = len(img)
    result = cv2.bilateralFilter(img,5,11,11)
    result = _alpha(result,1.6)
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
                    print(r)
                    num = num+1
                    img = cv2.circle(img, (x, y), r, (0, 255, 0), 1, 8, 0)

    # cv2.imshow(name, img)
    # print("circle num is "+str(num))
    return num

# debug用，通过文件名读取图片并调用_proc
def _fuckImg(name):
    img = cv2.imread(name+".png")
    print(name + "   " + str(_proc(img)))

# imgs = ["a1","b1","c1","d1","e1","f1","g1","h1","i1"]
# for name in imgs:
#     _fuckImg(name)

# 判断正反，圆的数量<=3即正面
def _judgePositive(img):
    num = _proc(img)
    if num <= 3:
        return True
    return False