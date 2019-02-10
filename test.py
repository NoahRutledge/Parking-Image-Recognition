import os
import sys
import cv2

sys.path.append(os.getcwd()+'\Mask_RCNN')
import mrcnn.config
import mrcnn.utils
from mrcnn.model import MaskRCNN

from pathlib import Path


class MaskRCNNConfig(mrcnn.config.Config):
    NAME = "coco_model_conf"
    IMAGES_PER_GPU = 1
    GPU_COUNT = 1
    NUM_CLASSES = 81
    DETECTION_MIN_CONFIDENCE = 0.6


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

#start the video capture of device 0
video = cv2.VideoCapture(0)

#start looping over the video
while video.isOpened():
    success, frame = video.read()

    #check if successfully captured frame
    if not success:
        break

    #convert image from BGR to RGB
    rgb = frame[:, :, ::-1]

    #give image to model
    result = model.detect([rgb], verbose=0)

    #store result into non-array
    r = result[0]
