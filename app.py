
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
    VERSION = "1.0.0"
    USER_CONFIG_FILE = "userSettings.hjson"

    def __init__(self, socketio : SocketIO, config, camera : HarvesterWrapper):
        super().__init__()

        self.socketio = socketio
        self.camera : HarvesterWrapper = camera
        self.config = config
        self.currImage : CameraImg = None

        # aktualne spustena kamera
        self.captureDeviceName = ""

        # aktualni devices a nodes kamery
        self.currDevices = []
        self.currNodes = []

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

    def getInitState(self, unused):
        capturing = self.camera.isCapturing()
        if capturing:
            data = {
                "capturing" : True,
                "devices" : self.currDevices,
                "nodes" : self.currNodes,
            }
        else:
            self.currDevices = self.camera.getDevices()
            data = {
                "capturing" : False,
                "devices" : self.currDevices,
                "nodes" : [],
            }
        try:
            return {
                "result" : True,
                "data" : data
            }
        except Exception as e:
            logging.exception(e)
            return {"result" : False, "data" : self._formatException(e)}
        
    
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
            self.currDevices = self.camera.getDevices()
            return {
                "result" : True,
                "data" : self.currDevices
            }
        except Exception as e:
            logging.exception(e)
            return {"result" : False, "data" : self._formatException(e)}
        
    def getMeasuringData(self, unused):
        try:
            return {
                "result" : True,
                "data" : self.currImage.get_calculated_data() if self.currImage else None
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
            self.currNodes = self.camera.updateNode(node["name"], value)
            return {
                "result" : True,
                "data" : self.currNodes
            }
        except Exception as e:
            logging.exception(e)
            return {"result" : False, "data" : self._formatException(e)}
                    
    def startCapture(self, device):
        try:
            self.currNodes = self.camera.startGrab(device, self.userConfig["CAMERA"])
            self.captureDeviceName = device["model"]
            return {
                "result" : True,
                "data" : self.currNodes
            }
        except Exception as e:
            logging.exception(e)
            return {"result" : False, "data" : self._formatException(e)}
        
    def stopCapture(self, unused):
        try:
            self.camera.stopGrab()
            self.currNodes = []
            return {
                "result" : True,
                "data" : None
            }
        except Exception as e:
            logging.exception(e)
            return {"result" : False, "data" : self._formatException(e)}



    
                
    
    

