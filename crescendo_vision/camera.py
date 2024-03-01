import io
import numpy as np
from picamera2 import Picamera2
from picamera2.outputs import FileOutput
from picamera2.encoders import H264Encoder

class Camera:
    '''
    An interface to the Pi camera
    '''

    cam: Picamera2

    def __init__(self):
        self.cam = Picamera2()
        self.cam.resolution = (640,480)

    def start_cap(self):
        '''
        Start capturing video
        '''
        cfg = self.cam.create_preview_configuration({
            'format': 'RGB888'
            })
        self.cam.configure(cfg)
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

        self.cam.capture_array()
