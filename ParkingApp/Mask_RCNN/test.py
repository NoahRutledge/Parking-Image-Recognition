#basic packages
import os
import sys
import cv2
import numpy
import time
import MySQLdb as mysql
from pathlib import Path

#Screenshot stuff
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
from io import BytesIO

#Mask RCNN stuff
sys.path.append(os.getcwd()+'\Mask_RCNN')
import mrcnn.config
import mrcnn.utils
from mrcnn.model import MaskRCNN

class MaskRCNNConfig(mrcnn.config.Config):
    NAME = "coco_model_conf"
    IMAGES_PER_GPU = 1
    GPU_COUNT = 1
    NUM_CLASSES = 81
    DETECTION_MIN_CONFIDENCE = 0.6

def add_entry(count):
    db = mysql.connect("localhost","root","toor","SeniorProject")
    cursor = db.cursor()
    cursor.execute("INSERT INTO ParkingSpaces VALUES ('Test Lot', "+str(count)+", 0, 0)")
    db.close()

def get_screenshot(identifier):
    chrome_options = Options()
    chrome_options.add_argument("headless")
    chrome = webdriver.Chrome(chrome_options=chrome_options)
    chrome.get('https://www.youtube.com/watch?v=PmrWwYTlAVQ&feature=player_embedded')
    element = chrome.find_element_by_id(identifier)
    location = element.location
    size = element.size
    png = chrome.get_screenshot_as_png()
    chrome.quit()

    im = Image.open(BytesIO(png))

    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']
    
    im = im.crop((left, top, right, bottom))
    im.save('Videos/screenshot.png')

def detect_cars_image(bounds, ids, scores, img):
    car_bounds = []
    count = 0
    for i, bound in enumerate(bounds):
        if(ids[i] in [3,6,8]):
            count += 1
            y1, x1, y2, x2 = bound
            cv2.rectangle(img, (x1, y1), (x2, y2), (0,255,0), 1)
            cv2.putText(img, str(scores[i]), (x1, y1), cv2.FONT_HERSHEY_PLAIN, 0.75, (0,0,255))
    return count

def detect_image():
    img = cv2.imread("Videos/screenshot.png", 1)
    img = cv2.resize(img, (960,540))
    rgb = img[:, :, ::-1]
    result = model.detect([rgb], verbose=0)
    r = result[0]
    n = detect_cars_image(r['rois'], r['class_ids'], r['scores'], img)
    add_entry(n)
    print("I see", n, "cars")
    cv2.imshow('Video', img)


#Create root path for use
ROOT = Path("./Mask_RCNN")

#Place to save model and logs
MODEL = os.path.join(ROOT, "results")

#Path to the COCO file
COCO = os.path.join(ROOT, "mask_rcnn_coco.h5")
#Something tends to remove the file(?)
if not os.path.exists(COCO):
    mrcnn.utils.download_trained_weights(COCO)

#create model in inference mode
model = MaskRCNN(mode="inference", model_dir=MODEL, config=MaskRCNNConfig())

#load weights
model.load_weights(COCO, by_name=True)

#Detect example image
time.sleep(1)
identifier = 'movie_player'

#get_screenshot(identifier)
detect_image()

cv2.waitKey(0)
cv2.destroyAllWindows()
