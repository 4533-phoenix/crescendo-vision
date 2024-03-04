from camera import Camera
from notedetector import NoteDetector
from nts import NT
import numpy as np
import cv2
import socket

print('FRC Team 4533 "Phoenix" -- 2024 Crescendo Vision')

# Initialize nt
nt = NT()

# Initialize the note detector
ai = NoteDetector()

# Initialize the camera
cam = Camera()

srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.bind(('0.0.0.0', 1181))
srv.listen(0)
NT.publishCamera()

# Start capturing I guess
cam.start_cap()
 
while True:
    sock, _ = srv.accept()
    
    _ = sock.recv(1024)
    sock.send("HTTP/1.1 200 OK\r\nServer: Godot\r\nConnection: close\r\nContent-Type: multipart/x-mixed-replace;boundary=frame\r\n\r\n".encode('utf-8'))
    
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
    
            image_resized = cv2.resize(frame, (720, 480))
            input_data = np.expand_dims(image_resized, axis=0)
    
            _, buffer = cv2.imencode('.jpeg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 50])
            try:
                sock.send(f'--frame\r\nContent-Type: image/jpeg\r\nContent-Length: {len(buffer)}\r\n\r\n'.encode('utf-8') + buffer.tobytes() + '\r\n\r\n'.encode('utf-8'))
            except:
                break
    
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
