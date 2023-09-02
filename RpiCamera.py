import time
# import threading
from picamera2 import Picamera2, Preview


class Camera(object):
    cam = None

    def __init__(self, width=360, height=240):
        self.open_camera(width, height)

    def open_camera(self, width=360, height=240):
        self.cam = Picamera2()
        self.cam.configure(self.cam.create_preview_configuration(main={"size": (width, height)}, buffer_count=18))

    def start_preview(self, a_preview: bool = False):
        if a_preview == True:
            self.cam.start_preview(Preview.QTGL)
        else:
            self.cam.start_preview()

        self.cam.start()

    def stop_preview(self):
        self.cam.stop_preview()
        self.cam.stop()

    def close(self):
        self.cam.close()


if __name__ == "__main__":
    camera = Camera()
    camera.start_preview(True)
    while True:
        time.sleep(1)

    # camera.stop_preview(True)
    # camera.close()

