
import logging
import cv2
import time
import numpy as np

from flask_socketio import SocketIO
from harvesterWrapper import HarvesterWrapper

class AbortedException(Exception):
    pass

class App():
    EXCEPTIONS_FUNC = str
    VERSION = "0.1.0"

    def __init__(self, socketio : SocketIO, config, camera : HarvesterWrapper):
        super().__init__()

        self.socketio = socketio
        self.camera = camera
        self.config = config

    def getImage(self):
        while True:
            image = self.camera.getImage()
            imageBytes = b""
            if image is not None:
                imgEnc = cv2.imencode("."+self.config["IMAGE_COMPRESSION"], self._resizeToMaxDimensions(image))
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
            time.sleep(0.01)
                
    def _resizeToMaxDimensions(self, image):
        f1 = self.config['IMAGE_MAX_W'] / image.shape[1]
        f2 = self.config['IMAGE_MAX_H'] / image.shape[0]
        f = min(f1, f2)  # resizing factor
        dim = (int(image.shape[1] * f), int(image.shape[0] * f))
        resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
        return resized

    
    def _formatException(self, e):
        return self.EXCEPTIONS_FUNC(e)

    

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

        try:
            nodes = self.camera.updateNode(node, value)
            return {
                "result" : True,
                "data" : nodes
            }
        except Exception as e:
            logging.exception(e)
            return {"result" : False, "data" : self._formatException(e)}
                    
    def startCapture(self, device):
        try:
            nodes = self.camera.startGrab(device)
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



    
                
    
    

