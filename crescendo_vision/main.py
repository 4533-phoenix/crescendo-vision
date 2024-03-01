from camera import Camera
from notedetector import NoteDetector
from nts import NT

print('FRC Team 4533 "Phoenix" -- 2024 Crescendo Vision')

# Initialize nt
nt = NT()

# Initialize the note detector
ai = NoteDetector()

# Initialize the camera
cam = Camera()

# Start capturing I guess
cam.start_cap()

#FOR TESTING ONLY
#img = cv2.imread('samples/3notes1robot.jpg')
#rgb = cv2.cvtColor(img, cv2.COLOR_YUV2RGB)
#cv2.imwrite('test.png', img=img)

while True:
    # Get a frame from the camera
    frame = cam.get_frame()

    # If the frame isn't null
    #   i.e. the camera has began returning frames
    if frame is not None:
        # Run note detector on frame
        notes = ai.process_frame(frame)

        # If any notes were detected...
        if len(notes) > 0:
            # Sort by distance to note (area of the bounding box) in descending order
            notes.sort(key='area', reverse=True)

            # Take the closest one
            closestNote = notes.first()

            # Let auto know via nettables
            nt.putData('x', closestNote['x'])
            nt.putData('y', closestNote['y'])
            nt.putData('width', closestNote['width'])
            nt.putData('height', closestNote['height'])
