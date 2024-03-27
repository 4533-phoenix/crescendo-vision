from camera import Camera
from ultralytics import YOLO
from nts import NT
import multiprocessing
import threading
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

def handle_objects(objects_queue: multiprocessing.Queue, nt: NT):
    while True:
        if not objects_queue.empty():
            objects = [box for box in objects_queue.get() if box[5] == 0]
            nt.putBool('note', len(objects) > 0)

            if len(objects) == 0:
                continue

            objects.sort(key=lambda a: a[4], reverse=True)

            box = objects[0]
            centerX = (box[0] + box[2]) / 2
            centerY = (box[1] + box[3]) / 2
            width = box[2] - box[0]
            height = box[3] - box[1]
            confidence = box[4]

            nt.putNumber('x', centerX)
            nt.putNumber('y', centerY)
            nt.putNumber('width', width)
            nt.putNumber('height', height)
            nt.putNumber('confidence', confidence)

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
    multiprocessing.Process(target=process_frame, args=(input_queue, output_queue), daemon=True).start()

    # Start a separate process for handling objects
    threading.Thread(target=handle_objects, args=(output_queue, nt), daemon=True).start()

    while True:
        # Get a frame from the camera
        frame = cam.get_frame()

        if frame is not None:
            # print(frame.shape)
            # Put the frame in the queue for processing
            input_queue.put(frame)

if __name__ == '__main__':
    main()
