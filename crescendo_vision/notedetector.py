import cv2
import numpy as np
import tflite_runtime.interpreter as tflite

class NoteDetector:
    '''
    Note detection w/ Coral Edge TPU
    '''

    base_path: str            = '/home/pi/crescendo-vision'
    model_path: str           = f'{base_path}/ssdmobilenet.tflite'
    labelmap_path: str        = f'{base_path}/labelmap.pbtxt'
    min_conf_threshold: float = 0.5
    input_mean: float         = 127.5
    input_std: float          = 127.5

    interpreter: tflite.Interpreter
    labels: list[str]
    float_input: bool
    input_details: list[dict]
    output_details: list[dict]
    width: float
    height: float

    def __init__(self):
        with open(self.labelmap_path, 'r') as f:
            self.labels = [line.strip() for line in f.readlines()]
            print(self.labels)
        
        self.interpreter = tflite.Interpreter(model_path=self.model_path, experimental_delegates=[
            tflite.load_delegate('libedgetpu.so.1')
            ])
        self.interpreter.allocate_tensors()
        
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.height = self.input_details[0]['shape'][1]
        self.width = self.input_details[0]['shape'][2]
        
        self.float_input = (self.input_details[0]['dtype'] == np.float32)
    
    def process_frame(self, frame: np.ndarray):
        image_resized = cv2.resize(frame, (self.width, self.height))
        input_data = np.expand_dims(image_resized, axis=0)
    
        if self.float_input:
            input_data = (np.float32(input_data) - self.input_mean) / self.input_std
    
        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        self.interpreter.invoke()
    
        boxes = self.interpreter.get_tensor(self.output_details[1]['index'])[0] 
        classes = self.interpreter.get_tensor(self.output_details[3]['index'])[0] 
        scores = self.interpreter.get_tensor(self.output_details[0]['index'])[0]
    
        imH, imW, _ = frame.shape
        HimH, HimW = (imH/2, imW/2)

        ret = []
    
        for i in range(len(scores)):
            if ((scores[i] > self.min_conf_threshold) and (scores[i] <= 1.0)):
                ymin = int(max(1,(boxes[i][0] * imH)))
                xmin = int(max(1,(boxes[i][1] * imW)))
                ymax = int(min(imH,(boxes[i][2] * imH)))
                xmax = int(min(imW,(boxes[i][3] * imW)))

                width = xmax-xmin
                height = ymax-ymin
                weight = width*(height/3)

                centerX = (xmin+(width/2)-HimW)/HimW
                centerY = (ymin+(height/2)-HimH)/HimH
    
                if int(classes[i]) == 1:
                    objKind = 'note'
                else:
                    objKind = 'robot'
                
                if objKind == 'note':
                    ret += [{
                        'x': centerX,
                        'y': centerY,
                        'width': width,
                        'height': height,
                        'weight': weight,
                    }]

        return ret
