import requests


class HDIntegratedCamera:
    """
    Class enabling connection and interaction with HD Integrated Camera.

    Args:
        baseurl (str): URL for communication with camera.

    """

    class Conversion:
        """Contains values for translating degrees to camera's hex values."""
        DEG_TO_HEX_YAW = 42480 / 350
        DEG_TO_HEX_PITCH = 14562 / 120

    class Commands:
        """Contains strings for different commands the camera accepts."""
        ROTATE = "APC"
        ZOOM = "AXZ"

    class Status:
        """Contains status values from camera."""
        OK = 200

    def __init__(self, baseurl: str):
        # Communication variables
        self.__BASEURL = baseurl

        # Orientation variables
        self.__current_yaw = 180
        self.__current_pitch = 140

    def get_current_yaw(self):
        return self.__current_yaw

    def get_current_pitch(self):
        return self.__current_pitch

    def set_current_yaw(self, new_yaw: int):
        self.__current_yaw = new_yaw % 360

    def set_current_pitch(self, new_pitch: int):
        if new_pitch > 180:
            new_pitch = 180

        if new_pitch < 0:
            new_pitch = 0

        self.__current_pitch = new_pitch

    @staticmethod
    def convert_degrees(degrees: int, conv: float) -> str:
        """Converts degrees to hexadecimal for rotation command to HD Integrated Camera"""

        degrees *= conv
        degrees = int(degrees)
        degrees += (int("0x2d08", 16) - 5)
        degrees = hex(degrees)
        return str(degrees)[2:].upper()

    @staticmethod
    def convert_zoom(new_zoom: int):
        clamped_input = max(0, min(100, new_zoom))
        res = hex(int(1365 + clamped_input * 27.30))
        return res[2:].upper()

    def rotate(self, new_yaw: int, new_pitch: int):
        """Rotate camera relative to zero pointer"""
        url = self.__BASEURL + self.Commands.ROTATE  # Rotate command
        url += self.convert_degrees(new_yaw, self.Conversion.DEG_TO_HEX_YAW)  # Yaw argument
        url += self.convert_degrees(new_pitch, self.Conversion.DEG_TO_HEX_PITCH)  # Pitch argument
        url += "&res=1"

        req = requests.get(url=url)

        if req.status_code != self.Status.OK:
            raise Exception("Communication with camera failed")

        self.set_current_yaw(new_yaw)
        self.set_current_pitch(new_pitch)

    def zoom(self, new_zoom: int):
        """takes an integer representing the zoom-percentage"""
        url = self.__BASEURL + self.Commands.ZOOM
        url += self.convert_zoom(new_zoom)
        url += "&res=1"

        req = requests.get(url=url)

        if req.status_code != self.Status.OK:
            raise Exception("Communication with camera failed")

    def move_left(self, degrees: int):
        """Move camera left by specified number of degrees"""
        new_yaw = (self.__current_yaw - degrees) % 360
        self.rotate(new_yaw, self.__current_pitch)
        print("Moving left")

    def move_right(self, degrees: int):
        """Move camera right by specified number of degrees"""
        new_yaw = (self.__current_yaw + degrees) % 360
        self.rotate(new_yaw, self.__current_pitch)
        print("Moving right")

    def move_up(self, degrees: int):
        """Move camera up by specified number of degrees"""
        new_pitch = self.__current_pitch + degrees
        self.set_current_pitch(new_pitch)
        self.rotate(self.__current_yaw, new_pitch)
        print("Moving up")

    def move_down(self, degrees: int):
        """Move camera down by specified number of degrees"""
        new_pitch = self.__current_pitch - degrees
        self.set_current_pitch(new_pitch)
        self.rotate(self.__current_yaw, new_pitch)
        print("Moving down")
