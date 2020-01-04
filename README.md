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
建议使用conda导入环境

    conda env create -f environment.yaml

注意高版本环境会导致识别问题，自行安装请务必保证版本号一致。
* 安装python3.6.4

    pip install tornado==4.5.3
    pip install numpy==1.14.2
    pip install opencv-python==4.1.2.30
    pip install pillow==5.0.0
    pip install tkinter //tkinter只在自己测试时使用

# 运行
## 前端

    cd front
    npm install
    npm start
  
## 后端
 * 在验证自己的模型时，输入
 
    cd backend
    python3 test.py
    
 * 在test.py中编写了（简陋的）GUI界面用来测试，所以测试时不需要运行前端，但是使用test.py会压缩图片，可能无法得到理想的结果

 * 在与前端联调时，输入
 
    cd backend
    python3 main.py
    
 * 在main.py中编写了本地服务器的启动程序
