import os
from pathlib import Path
import time
import pymysql
from dotenv import load_dotenv
from camera import HDIntegratedCamera
from observer_pattern.observer import Observer, Subject

BUFFER_SIZE = 10
X_MARGIN = (80, 200)
Y_MARGIN = (30, 180)
SCALING_FACTOR = 0.1
SLEEP_TIME = 1


class Controller(Observer):
    def update(self, subject: Subject) -> None:
        pass

    def __init__(self):
        # Instantiates all relevant tools the controller needs to operate

        self.bedroomCameraURL = "http://130.240.105.145/cgi-bin/" \
                                "mjpeg?resolution=1920x1080&amp;framerate=200&amp;quality=1"
        self.kitchenCameraURL = "http://130.240.105.144/cgi-bin/" \
                                "mjpeg?resolution=1920x1080&amp;framerate=200&amp;quality=1"

        self.log_rows = None
        self.cursor = None
        self.connection = None
        self.position_buffer = []
        self.rot_amount = 2
        self.getAllLogs()

        self.src = "http://130.240.105.144/cgi-bin/mjpeg?resolution=1920x1080&amp;framerate=200&amp;quality=1"
        # which camera to control
        self.cam = HDIntegratedCamera("http://130.240.105.144/cgi-bin/aw_ptz?cmd=%23")

    def follow_person(self, x, y, w, camera):
        self.switch_cam(camera)

        # Add the current position to the buffer and remove the oldest position if the buffer is full
        self.position_buffer.append((x, y))
        if len(self.position_buffer) > BUFFER_SIZE:
            self.position_buffer.pop(0)

        # Calculate the average position of the person detected over the last few frames
        x_avg, y_avg = tuple(map(lambda x: sum(x) / len(x), zip(*self.position_buffer)))

        # Calculate the distance between the current position and the target position
        dist_x = abs(x_avg - X_MARGIN[0]) if x_avg < X_MARGIN[0] else abs(x_avg + w - X_MARGIN[1])
        dist_y = abs(y_avg - Y_MARGIN[0]) if y_avg < Y_MARGIN[0] else abs(y_avg + w - Y_MARGIN[1])

        # Move the camera based on the distance between the current position and the target position
        if dist_x > 0 or dist_y > 0:
            # Define a scaling factor for the amount by which the camera should move
            move_x = int(dist_x * SCALING_FACTOR)
            move_y = int(dist_y * SCALING_FACTOR)

            # Determine which direction to move the camera
            if x_avg < X_MARGIN[0]:
                self.cam.move_left(move_x)
            elif x_avg + w > X_MARGIN[1]:
                self.cam.move_right(move_x)

            if y_avg < Y_MARGIN[0]:
                self.cam.move_up(move_y)
            elif y_avg + w > Y_MARGIN[1]:
                self.cam.move_down(move_y)

            # Add a sleep time to make the movement smoother
            time.sleep(SLEEP_TIME)

    def rotate(self, i, j):
        # A function handling a rotate command
        self.cam.rotate(i, j)

    def switch_cam(self, cam):
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
        self.cam.move_up(1)

    def down(self):
        self.cam.move_down(1)

    def left(self):
        # debugging why the camera is moving randomly after selecting a new camera
        # print(self.cam.get_current_yaw())
        # print(self.cam.get_current_pitch())
        self.cam.move_left(10)

    def right(self):
        self.cam.move_right(10)

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
