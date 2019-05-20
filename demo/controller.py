import requests
import os
from . import app
import cv2

class Controller(object):
    def __init__(self, detection_api_url, classification_api_url):
        self.detection_api_url = detection_api_url
        self.classification_api_url = classification_api_url

    def detect(self, files, img_file):
        print(files)
        detection = requests.post(self.detection_api_url, files=files).json()
        name, _ = os.path.splitext(img_file.split('/')[-1])
        filename = img_file.split('/')[-1]

        #remove this when api is fixed to not remove spaces and other characters
        replace_characters = [' ', '_', ',', '-']
        for rc in replace_characters:
            name = name.replace(rc, '')
        
        detection_key = name + '.jpg'
        detection_boxes = detection[detection_key].get('boxes')
        outputfile = detection[detection_key].get('img_file')
        detection_output = {
            "path": outputfile,
            "num_objects": detection[detection_key].get('number_of_animals'),
            "org_path": img_file,
            "image_name": filename,
            "result": detection[detection_key].get('status'),
            "bboxes": detection_boxes
        }
        return detection_boxes,  detection_output

    def classify(self, detection_boxes, img, img_file):
        classification_image_result = []
        for box in detection_boxes:
            read_img = img[int(box.get('y')): int(box.get('y')) + int(box.get('h')), 
                            int(box.get('x')) : int(box.get('x')) + int(box.get('w'))]
            
            if not any(v == 0 for v in list(read_img.shape)):
                _, img_encoded = cv2.imencode('.jpg', read_img)
                files = {img_file.split('/')[-1]: img_encoded.tostring()}
                classification_crop_result = requests.post(self.classification_api_url, files=files).json()

                print(classification_crop_result)
                #convert score to percentage 
                if classification_crop_result:
                    for i in range(len(classification_crop_result)):
                        classification_crop_result[i]['score'] = round(float(classification_crop_result[i]['score']) * 100, 2)
                
                classification_image_result.append(classification_crop_result)
        return classification_image_result


detection_api_url = app.config['DETECTION_API_URL']
classification_api_url = app.config['CLASSIFICATION_API_URL']

controller = Controller(detection_api_url, classification_api_url)


