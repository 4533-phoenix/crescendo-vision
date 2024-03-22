import threading
import numpy as np
from picamera2 import Picamera2, Preview
from libcamera import controls

class Camera:
    '''
    An interface to the Pi camera
    '''

    cam: Picamera2

    def __init__(self, normal_resolution=(640, 480), downscaled_resolution=(320, 240)):
        self.normal_resolution = normal_resolution
        self.downscaled_resolution = downscaled_resolution

        self.cam = Picamera2()

        self.frame = None
        self.thread = None
        self.running = False

    def capture_thread(self):
        while self.running:
            self.frame = self.cam.capture_buffer("lowres")

    def start_cap(self):
        '''
        Start capturing video
        '''
        self.cam.start_preview(Preview.QTGL)
        cfg = self.cam.create_video_configuration(main={
            'size': self.normal_resolution,
            'format': 'RGB888'
        }, lowres={
            'size': self.downscaled_resolution,
            'format': 'RGB888'
        })
        self.cam.configure(cfg)
        self.cam.start()
        self.cam.set_controls({'AfMode': controls.AfModeEnum.Continuous})

        self.running = True
        self.thread = threading.Thread(target=self.capture_thread)
        self.thread.start()
    
    def stop_cap(self):
        '''
        Stop capturing video
        '''

        self.running = False
        self.thread.join()
        self.cam.stop()
        self.thread = None
    
    def get_frame(self) -> np.ndarray:
        '''
        Grab a numpy array
        '''

        return self.frame
