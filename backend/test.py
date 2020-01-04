# -*- coding: utf-8 -*-
import tkinter as tk
import numpy as np
import math

from copy import deepcopy
from PIL import Image, ImageTk
from tkinter import filedialog

from ImgModel import ImgModel

class GUI(tk.Frame):
    #model
    imgModel = None

    inputImgPath = "test.png"

    imgWidth = 480
    imgHeight = 270
    
    def __init__(self, master, imgModel):
        super().__init__(master, width=1000, height=1000)
        self.imgModel = imgModel
        self.pack()

        #选择图片路径
        self.selectInputImgPathButtonText = tk.StringVar()
        self.selectInputImgPathButtonText.set("请选择图片路径")
        self.selectInputImgPathButton = tk.Button(self, textvariable=self.selectInputImgPathButtonText, command=self.__selectIamge)
        self.selectInputImgPathButton.grid(row = 0, column = 0, padx = 10, pady = 10)

        self.selectInputImgPathEntryText = tk.StringVar()
        self.selectInputImgPathEntryText.set("")
        self.selectInputImgPathEntry = tk.Entry(self, textvariable=self.selectInputImgPathEntryText, width = 30)
        self.selectInputImgPathEntry.grid(row = 0, column = 1, columnspan = 2, padx = 10, pady = 10)

        #处理函数选择
        self.functionButtonList = []
        self.functionButtonNameList = ["获取结果"]
        self.functionButtonCommandList = [self.__getResult]
        for i in range(len(self.functionButtonNameList)):
            self.functionButtonList.append(tk.Button(self, text=self.functionButtonNameList[i],  command=self.functionButtonCommandList[i]).grid(row = 2, column = 2 * i + 1, sticky="W"))
            
        #参数输入框
        self.argsNameList = []
        self.argsValue = {
        }
        self.argsLabelList = []
        self.argsEntryList = []
        for i in range(len(self.argsNameList)):
            temp = tk.StringVar()
            temp.set(self.argsNameList[i])
            self.argsLabelList.append(tk.Label(self, textvariable = temp).grid(row = 1 , column = 2 * i, padx = 2, sticky="W"))
            temp = tk.StringVar()
            temp.set(self.argsValue[self.argsNameList[i]])
            self.argsValue[self.argsNameList[i]] = temp
            self.argsEntryList.append(tk.Entry(self, textvariable = temp, width = 3).grid(row = 1, column = 2 * i + 1, sticky="W"))

        #显示图片
        self.selectInputImgPathLabelText = tk.StringVar()
        self.selectInputImgPathLabelText.set("输入图片")
        self.selectInputImgPathLabel = tk.Label(self, textvariable=self.selectInputImgPathLabelText)
        self.selectInputImgPathLabel.grid(row = 5, column = 0)

        self.pilInputImg = Image.fromarray(np.zeros((self.imgHeight, self.imgWidth)))
        self.tkInputImg = ImageTk.PhotoImage(image=self.pilInputImg)
        self.inputImgLabel = tk.Label(self, image=self.tkInputImg)
        self.inputImgLabel.grid(row = 6, column = 0, columnspan = 6)

        self.selectOutputImgPathLabelText = tk.StringVar()
        self.selectOutputImgPathLabelText.set("处理后图片")
        self.selectOutputImgPathLabel = tk.Label(self, textvariable=self.selectOutputImgPathLabelText)
        self.selectOutputImgPathLabel.grid(row = 5, column = 6)

        self.pilOutputImg = Image.fromarray(np.zeros((self.imgHeight, self.imgWidth)))
        self.tkOutputImg = ImageTk.PhotoImage(image=self.pilOutputImg)
        self.outputImgLabel = tk.Label(self, image=self.tkOutputImg)
        self.outputImgLabel.grid(row = 6, column = 6, columnspan = 6)

        

    #事件函数
    def __selectIamge(self):
        filePath = filedialog.askopenfilename()
        if(filePath != ""):
            self.inputImgPath = filePath
            self.selectInputImgPathEntryText.set(filePath)

            self.pilInputImg = Image.open(self.inputImgPath)
            self.pilInputImg = self.__resize(self.pilInputImg, self.imgWidth, self.imgHeight)
            self.imgModel.setPilImg(self.pilInputImg)
            self.imgModel.identify()
            self.tkInputImg = ImageTk.PhotoImage(image=self.pilInputImg)
            self.inputImgLabel = tk.Label(self, image=self.tkInputImg)
            self.inputImgLabel.grid(row = 6, column = 0, columnspan = 6)
            

            self.pilOutputImg = Image.fromarray(np.zeros((self.imgHeight, self.imgWidth)))
            self.tkOutputImg = ImageTk.PhotoImage(image=self.pilOutputImg)
            self.outputImgLabel = tk.Label(self, image=self.tkOutputImg)
            self.outputImgLabel.grid(row = 6, column = 6, columnspan = 6)
        else:
            self.pilOutputImg = Image.fromarray(np.zeros((self.imgHeight, self.imgWidth)))
            self.tkOutputImg = ImageTk.PhotoImage(image=self.pilOutputImg)
            self.outputImgLabel = tk.Label(self, image=self.tkOutputImg)
            self.outputImgLabel.grid(row = 6, column = 6, columnspan = 6)
        
        return filePath

    def __getResult(self):
        self.tkOutputImg = ImageTk.PhotoImage(image=imgModel.getPilImg())
        self.outputImgLabel = tk.Label(self, image=self.tkOutputImg)
        self.outputImgLabel.grid(row = 6, column = 6, columnspan = 6)
        return 

    def __resize(self, pilImg, width, height):
        widthRate = pilImg.size[0] / width
        heightRate = pilImg.size[1] / height
        rate = max(widthRate, heightRate)
        pilImg = pilImg.resize((int(pilImg.size[0] / rate), int(pilImg.size[1] / rate)))

        return pilImg


if __name__ == "__main__":
    root = tk.Tk()
    root.title("test")
    imgModel = ImgModel()
    app = GUI(root, imgModel)
    app.mainloop()



