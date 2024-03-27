import threading
import numpy as np
from picamera2 import Picamera2
from libcamera import controls

class Camera:
    '''
    An interface to the Pi camera
    '''

    cam: Picamera2

    def __init__(self, resolution=(640, 480)):
        self.cam = Picamera2()
        self.cam.resolution = resolution

        self.frame = None
        self.running = False
        self.thread = None

    def _capture(self):
        while self.running:
            self.frame = self.cam.capture_array()

    def start_cap(self):
        '''
        Start capturing video
        '''
        cfg = self.cam.create_video_configuration(main={
            'size': self.cam.resolution,
            'format': 'RGB888'
            })
        self.cam.configure(cfg)
        self.cam.start()
        self.cam.set_controls({'AfMode': controls.AfModeEnum.Continuous})

        self.running = True
        self.thread = threading.Thread(target=self._capture)
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
