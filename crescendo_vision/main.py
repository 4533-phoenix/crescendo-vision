#from camera import Camera
#from drake import Drake
from notedetector import NoteDetector
from nts import NT
import multiprocessing
import cv2
import numpy as np
import platform
from time import sleep

print('FRC Team 4533 "Phoenix" -- 2024 Crescendo Vision')

nt = NT()

# Initialize the camera
#cam = Camera()

# Start capturing I guess
#cam.start_cap()

'''
def nt_loop():
    while True:
        pkt = cam.get_packet()
        if pkt is not None:
            nt.putData('frame', pkt)

queue = multiprocessing.Queue(maxsize=1)
preview_process = multiprocessing.Process(target=nt_loop)
preview_process.daemon = True
preview_process.start()
'''

img = cv2.imread('samples/3notes1robot.jpg')
#rgb = cv2.cvtColor(img, cv2.COLOR_YUV2RGB)
cv2.imwrite('test.png', img=img)

ai = DatasetPeople()
for i in range(700):
    print(i, end='')
    ai.process_frame(img)

#####
# Put the OpenCV stuff here
#####

#d = Drake(cam)
#d.run()
#d.classify_frames()

#nt.putData('x', camX)
#nt.putData('y', camY)

#d.classify_frames()

sleep(5)

# Stop capturing
cam.stop_cap()
