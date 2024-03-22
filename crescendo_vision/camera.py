import io
import numpy as np
from picamera2 import Picamera2
from libcamera import controls

class Camera:
    '''
    An interface to the Pi camera
    '''

    cam: Picamera2

    def __init__(self):
        self.cam = Picamera2()
        self.cam.resolution = (720, 480)

    def start_cap(self):
        '''
        Start capturing video
        '''
        cfg = self.cam.create_video_configuration(main={
            'size': (720, 480),
            'format': 'RGB888'
            })
        self.cam.configure(cfg)
        self.cam.start()
        self.cam.set_controls({'AfMode': controls.AfModeEnum.Continuous})
    
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
