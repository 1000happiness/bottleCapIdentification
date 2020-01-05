# 项目结构
* frontend
* backend
  * IdentifyModel.py
  * ImgModel.py
  * Localserver.py
  * main.py
  
# 环境配置

## 前端
* 安装node.js

## 后端
建议使用conda导入环境

    conda env create -f environment.yaml

注意高版本环境会导致识别问题，自行安装请务必保证版本号一致。

安装python3.6.4

    pip install tornado==4.5.3
    pip install numpy==1.14.2
    pip install opencv-python==4.1.2.30
    pip install pillow==5.0.0

# 运行
## 前端

    cd frontend
    npm install
    npm start
  
## 后端

 
    cd backend
    python3 main.py
    
 * 在main.py中编写了本地服务器的启动程序
    

