from tornado import ioloop
from tornado import web
from json import loads
from base64 import b64encode

class CapIdentificationHandler(web.RequestHandler):
    def initialize(self, imgModel):
        self.imgModel = imgModel

    def post(self):
        args = self.request.body
        
        args = args[args.find(b"image/jpeg\r\n\r\n") + 14 : -1]
        self.imgModel.setBase64Image(b64encode(args))

        self.write("{\"success\": true}")

    def get(self):
        self.write(self.imgModel.getResultbase64Image())

class Localserver:
    #image model
    imgModel = None

    def __init__(self, imgModel):
        self.imgModel = imgModel

    def run(self):
        print("The local server is running in", 8000, "port")
        app = web.Application([
            (r"/setImage", CapIdentificationHandler, {"imgModel": self.imgModel}),  # 注册路由
            (r"/getImage", CapIdentificationHandler, {"imgModel": self.imgModel}),
        ])
        app.listen(8000)
        ioloop.IOLoop.current().start()


    
