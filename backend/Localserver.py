from tornado import ioloop
from tornado import web
from json import loads, dumps
from base64 import b64encode
from time import sleep

class CapIdentificationImgHandler(web.RequestHandler):
    def initialize(self, imgModel):
        self.imgModel = imgModel

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*") 
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header("Content-Type", "application/json;charset=utf-8")
        self.set_header("Access-Control-Allow-Credentials","true")

    def post(self):
        args = self.request.body
        
        args = args[args.find(b"image/jpeg\r\n\r\n") + 14 : -1]
        # print(args[0: 200])
        self.imgModel.setBase64Img(args)
        shape = self.imgModel.getImgShape()
        resBody = {
            "success": True,
            "imgWidth": shape[1],
            "imgHeight": shape[0] 
        }
        self.write(dumps(resBody))

    def get(self):
        uri = self.request.uri
        if(eval(uri[uri.find("image") + 6:]) % 2 == 0):
            self.write(self.imgModel.getInputbase64Img())
        else:
            self.write(self.imgModel.getResultbase64Img())
        
class CapIdentificationListHandler(web.RequestHandler):
    def initialize(self, imgModel):
        self.imgModel = imgModel

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*") 
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header("Content-Type", "application/json;charset=utf-8")
        self.set_header("Access-Control-Allow-Credentials","true")

    def get(self):
        self.imgModel.identify()
        resBody = {
            "success": True,
            "resultList": self.imgModel.getFormalResultList()
        }
        self.write(dumps(resBody))
        

class Localserver:
    #image model
    imgModel = None

    def __init__(self, imgModel):
        self.imgModel = imgModel

    def run(self):
        print("The local server is running in", 8000, "port")
        app = web.Application([
            (r"/setImage", CapIdentificationImgHandler, {"imgModel": self.imgModel}),  # 注册路由
            (r"/getImage", CapIdentificationImgHandler, {"imgModel": self.imgModel}),
            (r"/getResultList", CapIdentificationListHandler, {"imgModel": self.imgModel}),
        ])
        app.listen(8000)
        ioloop.IOLoop.current().start()


    
