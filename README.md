# 项目结构
* frontend
* backend
  * IdentifyModel.py
  * ImgModel.py
  * Localserver.py
  * main.py
  * test.py
  
# 环境配置

## 前端
* 安装node.js
* 安装react

## 后端
* 安装python3
* >pip install tornado
* >pip install numpy
* >pip install tkinter //tkinter只在自己测试时使用
* 程序中需要的其他包都是python3自带的，如果使用Anaconda3进行包管理，在那么上面的tornado、numpy、tkinter都已经装好了


# 运行
## 前端
  * >cd front
  * >npm install
  * >npm start
  
## 后端
 * 在验证自己的模型时，输入
 * >cd backend
 * >python3 test.py
 * 在test.py中编写了（简陋的）GUI界面用来测试，所以测试时不需要运行前端，但是使用test.py会压缩图片，可能无法得到理想的结果

 * 在与前端联调时，输入
 * >cd backend
 * >python3 main.py
 * 在main.py中编写了本地服务器的启动程序
