from flask import Blueprint, render_template, request, Response, Flask
from controller import Controller
import json


app = Flask(__name__, template_folder='templates')

# Instantiate a blueprint of views and a controller
views = Blueprint('views', __name__)
controller = Controller()


@views.route('/')
def home():
    """
    Render the home page of the application
    :return: rendered HTML template
    """
    return render_template('/index.html')


# Default route with a few variables passed to the html file

# Rotate function that takes 2 variables as input through json and rotates the camera using the controller
@views.route('/rotate', methods=['POST'])
def rotate():
    """
    Rotate the camera to the specified position
    :return: response indicating the status of the operation
    """
    controller.is_follow = False
    jsonData = request.get_json()
    i = int(jsonData['i'])
    j = int(jsonData['j'])
    controller.rotate(i, j)
    action = "Has rotated to (" + str(i) + "," + str(j) + ")"
    response = controller.databaseActions(action)
    return Response(str(response))


# Switch function that takes the value passed to the function through fetch and passes it to the controller, so it can
# switch the camera
@views.route('/switchCam/<cam>')
def switchCam(cam):
    controller.switchCam(cam)
    if cam == "Kitchen":
        controller.src = "http://130.240.105.144/cgi-bin/mjpeg?resolution=1920x1080&amp;framerate=5&amp;quality=1"
    if cam == "Bedroom":
        controller.src = "http://130.240.105.145/cgi-bin/mjpeg?resolution=1920x1080&amp;framerate=5&amp;quality=1"
    action = "Has switched to " + cam + ""
    response = controller.databaseActions(action)
    return Response(str(response))


# Manual control stuff
@views.route('/up')
def up():
    controller.up()
    return '', 204


@views.route('/down')
def down():
    controller.down()
    return '', 204


@views.route('/left')
def left():
    controller.left()
    return '', 204


@views.route('/right')
def right():
    controller.right()
    return '', 204


@views.route('/zoomIn')
def zoomIn():
    controller.zoomIn()
    return '', 204


@views.route('/zoomOut')
def zoomOut():
    controller.zoomOut()
    return '', 204


@views.route("/updateLog")
def updateLog():
    # A function that updates log on interface by sending the newest version of it to index.html through a json response
    arr = []
    for row in controller.log_rows:
        arr.append(row[1])
    response = arr
    return Response(json.dumps(response))
