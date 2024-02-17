import numpy as np
from picamera2 import Picamera2

class Camera:
    '''
    An interface to the Pi camera
    '''

    cam: Picamera2

    def __init__(self):
        cam = Picamera2()
        cam.resolution = (1080, 720)

    def start_cap(self):
        '''
        Start capturing video
        '''

        # TODO(lincoln): figure out how to plug it into actual ffmpeg
        self.cam.start_and_record_video('out.h264')
    
    def stop_cap(self):
        '''
        Stop capturing video
        '''

        self.cam.stop_recording()
    
    def get_frame(self) -> np.ndarray:
        '''
        Grab a numpy array
        '''

        if self.cam is not None:
            self.cam.capture_array()
