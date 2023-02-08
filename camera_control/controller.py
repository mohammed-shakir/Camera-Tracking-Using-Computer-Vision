from camera_control.camera import HDIntegratedCamera
from observer_pattern.observer import Observer, Subject
import numpy
import pymysql
from dotenv import load_dotenv
from pathlib import Path
import os


class Controller(Observer):
    def update(self, subject: Subject) -> None:
        pass

    def __init__(self):
        # Instantiates all relevant tools the controller needs to operate

        self.getAllLogs()

        # Change frame rate for better performance
        self.src = "http://130.240.105.144/cgi-bin/mjpeg?resolution=1920x1080&amp;framerate=5&amp;quality=1"

        self.cam = HDIntegratedCamera("http://130.240.105.144/cgi-bin/aw_ptz?cmd=%23")

        self.camera_bedroom_pos = numpy.array([619, 3935, 2600])
        self.camera_bedroom_zero = numpy.array([-765, 4112, 2878])
        self.camera_bedroom_floor = numpy.array([531, 3377, 331])

        self.camera_kitchen_pos = numpy.array([2873, -2602, 2186])
        self.camera_kitchen_zero = numpy.array([3413, -2722, 2284])
        self.camera_kitchen_floor = numpy.array([2694, -2722, 193])

        # self.cam_trans = wf.Transform(self.camera_kitchen_pos, self.camera_kitchen_zero, self.camera_kitchen_floor)

        self.rotate(210, 140)

        # self.trackers = []
        # self.trackersDict = {}

        self.rot_amount = 6

        # self.followTarget = ""
        # self.is_follow = False

    def rotate(self, i, j):
        # A function handling a rotate command
        self.cam.rotate(i, j)

    def switchCam(self, cam):
        # A function that switches camera by changing url to camera
        # and changing its transform to have the right room values
        if cam == "Kitchen":
            self.cam = HDIntegratedCamera("http://130.240.105.144/cgi-bin/aw_ptz?cmd=%23")

        if cam == "Bedroom":
            self.cam = HDIntegratedCamera("http://130.240.105.145/cgi-bin/aw_ptz?cmd=%23")

    # Handling of manual input with arrow keys
    def up(self):
        # self.is_follow = False
        self.cam.rotate(self.cam.get_current_yaw(), self.cam.get_current_pitch() + self.rot_amount)

    def down(self):
        # self.is_follow = False
        self.cam.rotate(self.cam.get_current_yaw(), self.cam.get_current_pitch() - self.rot_amount)

    def left(self):
        # self.is_follow = False
        self.cam.rotate(self.cam.get_current_yaw() - self.rot_amount, self.cam.get_current_pitch())

    def right(self):
        # self.is_follow = False
        self.cam.rotate(self.cam.get_current_yaw() + self.rot_amount, self.cam.get_current_pitch())

    # Handling of zoom in and zoom out on interface
    def zoomIn(self):
        self.cam.zoom(100)

    def zoomOut(self):
        self.cam.zoom(0)

    def databaseConn(self):
        load_dotenv()
        env_path = Path('.') / '.env'
        load_dotenv(dotenv_path=env_path)
        DB_NAME = os.getenv("DB_NAME")
        # localhost xampp phpmyadmin database
        self.connection = pymysql.connect(host="localhost", user="root", password="", database=DB_NAME)
        self.cursor = self.connection.cursor()

        # logtable( log_id(int), entry(text), created_at(timestamp))

    def getAllLogs(self):
        # A function that connects to database and gets the 10 most relevant actions done on the interface
        self.databaseConn()

        sql = "SELECT * FROM log_table ORDER BY log_id DESC LIMIT 10"
        self.cursor.execute(sql)
        self.log_rows = self.cursor.fetchall()
        self.connection.close()

    def databaseActions(self, action):
        # A function that adds an action, done through the interface, to the database
        self.databaseConn()
        sql = "INSERT INTO log_table(entry) VALUES('" + str(action) + "');"
        print(sql)
        self.cursor.execute(sql)
        self.connection.commit()
        self.connection.close()
        self.getAllLogs()
        return self.log_rows
