import io
import numpy as np
from picamera2 import Picamera2

class Camera:
    '''
    An interface to the Pi camera
    '''

    cam: Picamera2

    def __init__(self):
        self.cam = Picamera2()
        self.cam.resolution = (1080, 720)

    def start_cap(self):
        '''
        Start capturing video
        '''
        cfg = self.cam.create_video_configuration({
            'format': 'RGB888'
            })
        self.cam.configure(cfg)
        self.cam.resolution = (640,480)
        self.cam.start()
    
    def stop_cap(self):
        '''
        Stop capturing video
        '''

        self.cam.stop()
    
    def get_frame(self) -> np.ndarray:
        '''
        Grab a numpy array
        '''

        arr = self.cam.capture_array()
        return arr
