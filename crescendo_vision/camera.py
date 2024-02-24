import numpy as np
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput

class Camera:
    '''
    An interface to the Pi camera
    '''

    cam: Picamera2
    enc: H264Encoder

    def __init__(self):
        self.cam = Picamera2()
        self.cam.resolution = (1080, 720)
        self.enc = H264Encoder(bitrate=50000, repeat=True, iperiod=15)

    def start_cap(self):
        '''
        Start capturing video
        '''

        # TODO(lincoln): figure out how to plug it into actual ffmpeg
        self.cam.start_encoder(self.enc)
    
    def stop_cap(self):
        '''
        Stop capturing video
        '''

        self.cam.stop_encoder()
    
    def get_frame(self) -> np.ndarray:
        '''
        Grab a numpy array
        '''

        if self.cam is not None:
            self.cam.capture_array()
