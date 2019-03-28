#basic packages
import os
import sys
import cv2
import numpy
import MySQLdb as mysql
from pathlib import Path

#personal scripts
from screenshot import get_screenshot
from crop import cropImage

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
    DETECTION_MIN_CONFIDENCE = 0.7

#Create root path for use and path to model/logs that never get generated
ROOT = Path("./Mask_RCNN")
MODEL = os.path.join(ROOT, "results")

#Path to the COCO file
COCO = os.path.join(ROOT, "mask_rcnn_coco.h5")
if not os.path.exists(COCO):
    mrcnn.utils.download_trained_weights(COCO)

#create model in inference mode
model = MaskRCNN(mode="inference", model_dir=MODEL, config=MaskRCNNConfig())
model.load_weights(COCO, by_name=True)


def add_entry(count):
    db = mysql.connect("localhost","root","toor","SeniorProject")
    cursor = db.cursor()
    cursor.execute("INSERT INTO ParkingSpaces VALUES ('Test Lot', "+str(count)+", 0, 0)")
    db.close()

def detect_cars_image(bounds, ids, scores, img):
    car_bounds = []
    count = 0
    for i, bound in enumerate(bounds):
        if(ids[i] in [3,6,8]):
            #return 1
            count += 1
            y1, x1, y2, x2 = bound
            #print("%d,%d - %d,%d" %(x1,y1,x2,y2))
            cv2.rectangle(img, (x1, y1), (x2, y2), (0,255,0), 1)
            cv2.putText(img, str(scores[i]), (x1, y1), cv2.FONT_HERSHEY_PLAIN, 0.75, (0,0,255))
    return count

def detect_image(path):
    img = cv2.imread(path)
    img = cv2.resize(img,(960,540))
    rgb = img[:, :, ::-1]
    result = model.detect([rgb], verbose=0)
    r = result[0]
    
    n = detect_cars_image(r['rois'], r['class_ids'], r['scores'], img)
    print("I see", n, "cars")
    #img = cv2.resize(img, (1920,1080))
    cv2.imshow("img", img)

def main():
    #if(len(sys.argv) != 3):
    #    raise Exception("Expected 3 arguments; got {}\nExpected format is ~.py /path/to/coordinates.txt /path/to/image.jpg".format(len(sys.argv)))
    
    #coordPath = sys.argv[1]
    #imagePath = sys.argv[2]
    try:
        coordPath = 'coords.txt'
        imagePath = 'Videos/Parking1.jpg'
        """
        TODO:
            Open file and loop through it taking 4 coords at a time putting it in a [][4]
            Crop given image to each coord space, save it, and give that path to the detect_image
            If it sees 0, add one to a count
        """
        availableSpots = 0
        
        coordFile = open(coordPath, "r")
        file = coordFile.read().split("\n")
        for line in file:
            lineSplit = line.split(",")
            croppedPath = cropImage(imagePath, lineSplit)

            result = detect_image(croppedPath)
            if(result == 0):
                availableSpots += 1

        print("There are",availableSpots,"available spots open")
        #Retreive screenshot
        #identifier = 'movie_player'
        #link = 'https://www.youtube.com/watch?v=PmrWwYTlAVQ&feature=player_embedded'
        #get_screenshot(identifier, link)

        #detect_image()

        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
    except:
        print("Something happened")
#main()
detect_image('Videos/Parking2Cut.jpg')
