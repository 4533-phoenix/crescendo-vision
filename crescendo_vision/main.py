from camera import Camera
from notedetector import NoteDetector
from nts import NT
import multiprocessing
import time

print('FRC Team 4533 "Phoenix" -- 2024 Crescendo Vision')

# Initialize nt
nt = NT()

# Initialize the note detector
ai = NoteDetector()

# Initialize the camera
cam = Camera()

# Start capturing I guess
cam.start_cap()

def process_frame(frame_queue, result_queue):
    while True:
        ctime, frame = frame_queue.get()
        if frame is not None:
            # Run note detector on frame
            notes = ai.process_frame(frame)

            # If any notes were detected...
            if len(notes) > 0:
                result_queue.put((True, ctime, notes))
            else:
                result_queue.put((False, ctime, []))

if __name__ == '__main__':
    # Create queues for communication between processes
    frame_queue = multiprocessing.Queue()
    result_queue = multiprocessing.Queue()

    # Start a separate process for processing frames
    process = multiprocessing.Process(target=process_frame, args=(frame_queue, result_queue))
    process.start()

    while True:
        # Get a frame from the camera
        ctime, frame = cam.get_frame()

        if frame is not None:
            # Put the frame in the queue for processing
            frame_queue.put((ctime, frame))

            # Get the result from the queue
            note_detected, ctime, notes = result_queue.get()
            elapsed = time.time() - ctime

            nt.putBool('note', note_detected)
            nt.putInt('elapsed', elapsed)

            if note_detected:
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