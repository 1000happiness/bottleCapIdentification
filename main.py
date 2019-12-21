from json import load, dumps
from time import sleep

from ImgModel import ImgModel
from Localserver import Localserver


def main():
    imgModel = ImgModel()
    localserver = Localserver(imgModel)
    localserver.run()

if __name__ == "__main__":
    main()
    