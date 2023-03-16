from flask import Flask, render_template, Response
from flask_socketio import SocketIO
from engineio.async_drivers import gevent #kvuli pyinstalleru
import hjson
import logging
import os
import sys
from logs import ConfigureLogging
from app import App
from harvesterWrapper import HarvesterWrapper

config = hjson.load(open("config.hjson", "r"))
configCamera = hjson.load(open("cameraConfig.hjson", "r"))

ConfigureLogging(config["LOG_LEVEL"])

cam = HarvesterWrapper(configCamera)

# nastartovat flask app se socket io
# static folder pres cwd jinak nefunguje zapakovane do exe
flaskApp = Flask(__name__, static_folder=os.getcwd() + "/www/public", static_url_path="")
flaskApp.config['SECRET_KEY'] = 'manufacturingCameraReader'
#bez asyncmode nejde zaroven streaming
#viz Limitations of Streaming: https://blog.miguelgrinberg.com/post/video-streaming-with-flask
socketio = SocketIO(flaskApp, ping_timeout=60, logger=True, async_mode="threading") 

app = App(socketio, config, cam)

# zpracovani web requestu
@flaskApp.route('/', methods = ['GET', 'POST'])
def index():
    return flaskApp.send_static_file("index.html")

@flaskApp.route('/video')
def video():
    return Response(app.getImage(), mimetype="multipart/x-mixed-replace; boundary=frame")

@socketio.on_error_default
def handlerError(e):
    socketio.emit("SOCKET_IO_ERROR", str(e))

socketio.on_event("GET_CONFIG",  app.getConfig)
socketio.on_event("GET_DEVICES",  app.getDevices)
socketio.on_event("START_CAPTURE",  app.startCapture)
socketio.on_event("STOP_CAPTURE",  app.stopCapture)

@socketio.on('connect')
def test_connect(auth):
    logging.info("Connected")

@socketio.on('disconnect')
def test_disconnect():
    logging.info("Disonnected")



if __name__ == '__main__':
    print(f"Starting: http://{config['HOST']}:{config['PORT']}")
    socketio.run(flaskApp, config['HOST'], config['PORT'])