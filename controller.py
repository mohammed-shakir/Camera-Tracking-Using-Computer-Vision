import os
from pathlib import Path

import pymysql
from dotenv import load_dotenv
from camera import HDIntegratedCamera
from observer_pattern.observer import Observer, Subject


class Controller(Observer):
    def update(self, subject: Subject) -> None:
        pass

    def __init__(self):
        # Instantiates all relevant tools the controller needs to operate

        self.bedroomCameraURL = "http://130.240.105.145/cgi-bin/" \
                                "mjpeg?resolution=1920x1080&amp;framerate=30&amp;quality=1"
        self.kitchenCameraURL = "http://130.240.105.144/cgi-bin/" \
                                "mjpeg?resolution=1920x1080&amp;framerate=30&amp;quality=1"

        self.log_rows = None
        self.cursor = None
        self.connection = None
        self.rot_amount = 2
        self.getAllLogs()

        self.src = "http://130.240.105.145/cgi-bin/mjpeg?resolution=1920x1080&amp;framerate=30&amp;quality=1"
        # which camera to control
        self.cam = HDIntegratedCamera("http://130.240.105.145/cgi-bin/aw_ptz?cmd=%23")

    def followPerson(self, x, y, w, camera):
        # Define the horizontal and vertical margins
        self.switchCam(camera)
        x_margin_left = 80
        x_margin_right = 200
        y_margin_up = 30
        y_margin_down = 180

        # Check if the person is too far to the left
        if x < x_margin_left:
            self.cam.move_left(10)
        # Check if the person is too far to the right
        elif (x + w) > x_margin_right:
            self.cam.move_right(10)
        # else:
        #     print("Centered horizontally")

        # Check if the person is too high up
        if y < y_margin_up:
            self.cam.move_up(10)
        # Check if the person is too low
        elif y > y_margin_down:
            self.cam.move_down(10)
        # else:
        #     print("Centered vertically")

    def rotate(self, i, j):
        # A function handling a rotate command
        self.cam.rotate(i, j)

    def switchCam(self, cam):
        # A function that switches camera by changing url to camera
        # and changing its transform to have the right room values
        if cam == "Kitchen":
            self.cam = HDIntegratedCamera("http://130.240.105.144/cgi-bin/aw_ptz?cmd=%23")
            self.rotate(180, 140)

        if cam == "Bedroom":
            self.cam = HDIntegratedCamera("http://130.240.105.145/cgi-bin/aw_ptz?cmd=%23")
            self.rotate(250, 160)

    # Handling of manual input with arrow keys
    def up(self):
        self.cam.move_up(2)

    def down(self):
        self.cam.move_down(2)

    def left(self):
        # debugging why the camera is moving randomly after selecting a new camera
        print(self.cam.get_current_yaw())
        print(self.cam.get_current_pitch())
        self.cam.move_left(2)

    def right(self):
        self.cam.move_right(2)

    # Handling of zoom in and zoom out on interface
    def zoomIn(self):
        self.cam.zoom(100)

    def zoomOut(self):
        self.cam.zoom(0)

    def databaseConn(self):
        load_dotenv()
        env_path = Path('camera_control') / '.env'
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
