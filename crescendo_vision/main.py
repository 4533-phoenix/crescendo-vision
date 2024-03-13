from camera import Camera
from notedetector import NoteDetector
from nts import NT
from time import sleep
import numpy as np
import cv2
import socket
import simplejpeg
import threading
import select
import atexit

print('FRC Team 4533 "Phoenix" -- 2024 Crescendo Vision')

# Initialize nt
nt = NT()

# Initialize the note detector
ai = NoteDetector()

# Initialize the camera
cam = Camera()

srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.bind(('0.0.0.0', 1181))
srv.listen(5)
NT.publishCamera()

# Start capturing I guess
#cam.start_cap()

# exit handler
def onexit():
    #cam.stop_cap()
    srv.close()
atexit.register(onexit)

# Frame for mjpeg
jpeg_frame = None
frame = None

lock = threading.Lock()

def recv_all(sock):
    data = b""

    while len(select.select([sock], [], [])[0]) != 0:
        data += sock.recv(1024)

    return data

def sock_thread(sock):
    global jpeg_frame
    print("got connection into thread")
    recv_all(sock)
    sock.send("HTTP/1.1 200 OK\r\nServer: NoteDetector\r\nConnection: close\r\nContent-Type: multipart/x-mixed-replace;boundary=frame\r\n\r\n".encode('utf-8'))

    while True:
        if jpeg_frame is not None:
            try:
                sock.send(f'--frame\r\nContent-Type: image/jpeg\r\nContent-Length: {len(jpeg_frame)}\r\n\r\n'.encode('utf-8') + jpeg_frame.tobytes() + '\r\n\r\n'.encode('utf-8'))
            except:
                break

def sock_accept(srv):
    print("got srv")
    while True:
        sock = srv.accept()[0]
        print("accepted thread")
        threading.Thread(target=sock_thread, daemon=True, args=(sock,)).start()

def jpeg_encoder():
    global frame, jpeg_frame

    if frame is not None:
        jpeg_frame = cv2.imencode('.jpeg', frame)[1]

def grab_frames(cam: Camera):
    global frame, lock

    with lock:
        print('grab got lock')
        frame = cam.get_frame()
        print('got frame')

def ai_stuff(cam: Camera):
    global frame, lock

    with lock:
        if frame is not None:
            input_data = np.expand_dims(frame, axis=0)
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

                print(closestNote)

            else:
                nt.putBool('note', False)

#threading.Thread(target=sock_accept, daemon=True, args=(srv,)).start()
#threading.Thread(target=jpeg_encoder, daemon=True).start()

while True:
    threading.Thread(target=grab_frames, daemon=False, args=(cam,)).start()
    threading.Thread(target=ai_stuff, daemon=False, args=(cam,)).start()
    sleep(0.1)

'''
while True:
    
    #FOR TESTING ONLY
    #img = cv2.imread('samples/3notes1robot.jpg')
    #rgb = cv2.cvtColor(img, cv2.COLOR_YUV2RGB)
    #cv2.imwrite('test.png', img=img)
    
    while True:
        # Get a frame from the camera
        #frame = cam.get_frame()
        if frame is not None:
            #print('got frame')
            #image_resized = cv2.resize(frame, (720, 480))
    
            #buffer = simplejpeg.encode_jpeg(frame, fastdct=True)
            #_, buffer = cv2.imencode('.jpeg', frame)
    
            input_data = np.expand_dims(frame, axis=0)
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

        sleep(0.1)
'''
