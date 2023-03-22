
import logging
import cv2
import time
import hjson
import numpy as np

from flask_socketio import SocketIO
from harvesterWrapper import HarvesterWrapper
from cameraImg import CameraImg

class AbortedException(Exception):
    pass

class App():
    EXCEPTIONS_FUNC = str
    VERSION = "0.1.0"
    USER_CONFIG_FILE = "userSettings.hjson"

    captureDeviceName = ""

    def __init__(self, socketio : SocketIO, config, camera : HarvesterWrapper):
        super().__init__()

        self.socketio = socketio
        self.camera = camera
        self.config = config
        self.currImage = None
        with open(self.USER_CONFIG_FILE, "r") as f:
            self.userConfig = hjson.load(f)

    def getCutImage(self, type):
        while True:
            if self.currImage is not None:
                imgToSend = self.currImage.cut_vertical if type=="vertical"else self.currImage.cut_horizontal
                imgEnc = cv2.imencode("."+self.config["IMAGE_COMPRESSION"], imgToSend)
                if imgEnc[0]:
                    imageBytes = imgEnc[1].tobytes()
                
                res = bytes("--frame\r\n", encoding="utf-8")
                res += bytes(f"Content-Type: image/{self.config['IMAGE_COMPRESSION']}\r\n\r\n", encoding="utf-8")
                res += imageBytes
                res += bytes("\r\n", encoding="utf-8")
                yield res

    def getImage(self):
        while True:
            image = self.camera.getImage()
            imageBytes = b""
            if image is not None:
                newImg = CameraImg(
                    image,
                    self.config["PIXEL_SIZE"][self.captureDeviceName],
                    self.config["PROCESSING"]["THRESHOLD_PERC"],
                    self.config['IMAGE_MAX_W'],
                    self.config['IMAGE_MAX_H']
                )
                newImg.process()
                self.currImage = newImg
                imgEnc = cv2.imencode("."+self.config["IMAGE_COMPRESSION"], self.currImage.img_dst)
                if imgEnc[0]:
                    imageBytes = imgEnc[1].tobytes()
                
                res = bytes("--frame\r\n", encoding="utf-8")
                res += bytes(f"Content-Type: image/{self.config['IMAGE_COMPRESSION']}\r\n\r\n", encoding="utf-8")
                res += imageBytes
                res += bytes("\r\n", encoding="utf-8")
                yield res
            else:
                # TODO
                # dodelat nejaky prazdny image "Capture off"
                pass
    
    def _formatException(self, e):
        return self.EXCEPTIONS_FUNC(e)

    def _saveUserConfig(self):
        with open(self.USER_CONFIG_FILE, "w") as f:
            f.write(hjson.dumps(self.userConfig, indent="\t"))

    def getConfig(self, unused):
        try:
            return {
                "result" : True,
                "data" : self.config
            }
        except Exception as e:
            logging.exception(e)
            return {"result" : False, "data" : self._formatException(e)}
        
    def getDevices(self, unused):
        try:
            return {
                "result" : True,
                "data" : self.camera.getDevices()
            }
        except Exception as e:
            logging.exception(e)
            return {"result" : False, "data" : self._formatException(e)}
        
    def updateNode(self, data):
        assert "value" in data and "node" in data, "Value or node not in data"
        value = data["value"]
        node = data["node"]

        self.userConfig["CAMERA"][node["name"]] = value
        self._saveUserConfig()

        try:
            nodes = self.camera.updateNode(node["name"], value)
            return {
                "result" : True,
                "data" : nodes
            }
        except Exception as e:
            logging.exception(e)
            return {"result" : False, "data" : self._formatException(e)}
                    
    def startCapture(self, device):
        try:
            nodes = self.camera.startGrab(device, self.userConfig["CAMERA"])
            self.captureDeviceName = device["model"]
            return {
                "result" : True,
                "data" : nodes
            }
        except Exception as e:
            logging.exception(e)
            return {"result" : False, "data" : self._formatException(e)}
        
    def stopCapture(self, unused):
        try:
            self.camera.stopGrab()
            return {
                "result" : True,
                "data" : None
            }
        except Exception as e:
            logging.exception(e)
            return {"result" : False, "data" : self._formatException(e)}



    
                
    
    

