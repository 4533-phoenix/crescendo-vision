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
 
while True:
    #FOR TESTING ONLY
    #img = cv2.imread('samples/3notes1robot.jpg')
    #rgb = cv2.cvtColor(img, cv2.COLOR_YUV2RGB)
    #cv2.imwrite('test.png', img=img)
    
    while True:
        # Get a frame from the camera
        frame = cam.get_frame()
        if frame is not None:
            print('got frame')

            # Run note detector on frame
            notes = ai.process_frame(frame)
    
            # If any notes were detected...
            if len(notes) > 0:
                nt.putBool('note', True)
                # Sort by distance to note (area of the bounding box) in descending order
                notes.sort(key=lambda a: a['weight'], reverse=True)
    
                # Take the closest one
                closestNote = notes[0]
    
                print(closestNote)
                # Let auto know via nettables
                nt.putInt('x', closestNote['x'])
                nt.putInt('y', closestNote['y'])
                nt.putInt('width', closestNote['width'])
                nt.putInt('height', closestNote['height'])
            else:
                nt.putBool('note', False)