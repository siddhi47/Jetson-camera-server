import threading

import cv2
from bottle import template, static_file, response, Bottle, redirect, auth_basic
import os

print(__file__)
PROJECT_PATH = os.path.dirname(os.path.realpath(__file__))

streamedFrame = None
securityFrame = None
info = None
info_flag = False
lock = threading.Lock()
app = Bottle()
security_mode = False
graphs = None

print("PROJECT PATH")
print(PROJECT_PATH)
#TODO: counts


def is_authenticated_user(user,password):
    if user == "siddhi" and password == "Auth@Siddhi123":
        return True

@app.route("/")
@auth_basic(is_authenticated_user)
def index():
    i = info
    if i is None:
        i = []
    return template(os.path.join(PROJECT_PATH,'views/index'),
                    info=i,
                    feed=app.get_url('/feed'),
                    )


@app.route("/dashboard")
def dashboard():
    return template(os.path.join(PROJECT_PATH,'views/dashboard'),
                    graphs=graphs)


@app.route("/body.css")
def body():
    return static_file('body.css', root=os.path.join(PROJECT_PATH,'views/'))


@app.route("/feed")
def feed():
    response.content_type = "multipart/x-mixed-replace; boundary=frame"
    return generate()

#TODO: not really doing this anymore
@app.post('/toggle')
def do_toggle():
    global security_mode
    security_mode = not security_mode
    redirect('/')

#TODO: we're not really doing this anymore
@app.post('/template')
def update_template():
    global update_template
    with lock:
        update_template = True
    redirect('/')


def generate():
    global streamedFrame, securityFrame, lock
    while True:
        with lock:
            if streamedFrame is None:
                continue
            (flag, encodedImage) = None, None
            if security_mode:
                (flag, encodedImage) = cv2.imencode(".jpg", securityFrame)
            else:
                (flag, encodedImage) = cv2.imencode(".jpg", streamedFrame)
            if not flag:
                continue
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(
            encodedImage) + b'\r\n')

#TODO: may want to take this to port 80
def serve():
    app.run(host='0.0.0.0', port='8080', server='waitress')
