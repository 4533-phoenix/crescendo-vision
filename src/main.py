from camera import Camera
from ultralytics import YOLO
from nts import NT
import multiprocessing
import os

print('FRC Team 4533 "Phoenix" -- 2024 Crescendo Vision')

FILE_LOCATION = os.path.dirname(os.path.realpath(__file__))

def process_frame(input_queue: multiprocessing.Queue, output_queue: multiprocessing.Queue):
    CONF_THRESHOLD = 0.5
    MODEL = YOLO(os.path.join(FILE_LOCATION, "models/YOLOv5n_full_integer_quant_edgetpu.tflite"), task="detect")

    while True:
        if not input_queue.empty():
            img = input_queue.get()
            objs = MODEL.predict(img, conf=CONF_THRESHOLD, verbose=False)[0]
            output_queue.put(objs.cpu().numpy().boxes.data)

def main():
    # Initialize nt
    nt = NT()

    # Initialize the camera
    cam = Camera()

    # Start capturing I guess
    cam.start_cap()

    # Create queues for communication between processes
    input_queue = multiprocessing.Queue(maxsize=1)
    output_queue = multiprocessing.Queue(maxsize=1)

    # Start a separate process for processing frames
    process = multiprocessing.Process(target=process_frame, args=(input_queue, output_queue), daemon=True)
    process.start()

    while True:
        # Get a frame from the camera
        frame = cam.get_frame()

        if frame is not None:
            # print(frame.shape)
            # Put the frame in the queue for processing
            input_queue.put(frame)

            # Get the result from the queue
            objects = output_queue.get()
            print(objects)

            # nt.putBool('note', note_detected)

            # if note_detected:
            #     # Sort by distance to note (area of the bounding box) in descending order
            #     notes.sort(key=lambda a: a['weight'], reverse=True)

            #     # Take the closest one
            #     closestNote = notes[0]

            #     print(closestNote)

            #     # Let auto know via nettables
            #     nt.putInt('x', closestNote['x'])
            #     nt.putInt('y', closestNote['y'])
            #     nt.putInt('width', closestNote['width'])
            #     nt.putInt('height', closestNote['height'])

if __name__ == '__main__':
    main()
