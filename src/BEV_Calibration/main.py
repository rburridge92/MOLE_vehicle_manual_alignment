#!/usr/bin/env python3
#Main file for BEV Calibration
import logging
import argparse
import cv2
import os
import yaml
import numpy as np

from src.bev_calibration import BEV_camera

## LOGGING
# set up logging to file
logging.basicConfig(
     filename='BEV.log',
     level=logging.DEBUG, 
     format= '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
     datefmt='%H:%M:%S'
 )

# set up logging to console
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)
main_logger = logging.getLogger('BEV.Main')

## ARGUMENT PARSER
# Create the parser
parser = argparse.ArgumentParser(add_help=True)
parser.add_argument("--images", type=str, required = False, default='resources/images', help = 'folder to images (default /resources/images)') 
parser.add_argument("--info", type=str, required = False, default='resources/camera_info', help = 'folder to camera yamls (default /resources/camera_info)') 
parser.add_arguemnt("--patternHeight", type=float, required = False, default = 1.10, help = 'height from the ground of checkboard in images in meters. This should be consistent across all images')
parser.add_argument("--squareSize", type = float, required = False, default = 0.035, help = 'Size of squares in checkboard patter in meters')
args = parser.parse_args()

directory = os.path.abspath(os.getcwd())
image_folder = os.path.join(directory,args.images)
yaml_folder = os.path.join(directory,args.info)


### MAIN 
## Import Calibration Images (these are rectified images with checkboard set up as described in README)
main_logger.debug('importing images')
# Set up array of images
imgs = []
#loop through and read images in folder
for filename in sorted(os.listdir(image_folder)):
    #print(filename)
    img = cv2.imread(os.path.join(image_folder,filename))
    if img is not None:
        imgs.append(img)

#Check how many images and therefore cameras are detected
numCams = len(imgs)
if numCams is None:
    main_logger.error('No images found')
else:
    main_logger.debug(str(numCams)+' images/cameras detected')

# Import Yaml Files
main_logger.debug('importing camera information from files')
# Set up arrays for camera information
camera_matricies = []
distortion_coeffs = []
image_widths=[]
image_heights=[]
camera_positions=[]
camera_directions=[]

#Loop through yamls files in folder and parse information into arrays
for filename in sorted(os.listdir(yaml_folder)):
    #print(filename)
    with open(os.path.join(yaml_folder,filename)) as f:
        yamlLoad = yaml.safe_load(f)
    if yamlLoad is not None:
        #Get, resize and store camera matrix
        M = np.array(yamlLoad["camera_matrix"]["data"])
        M = np.reshape(M,(3,3))
        camera_matricies.append(M)
        #Get and store camera distortion coeffs
        C = np.array(yamlLoad["distortion_coefficients"]["data"])
        C = np.reshape(C,(1,5))
        distortion_coeffs.append(C)
        #Get and store image widths and heights
        w = int(yamlLoad["image_width"])
        h = int(yamlLoad["image_height"])
        image_widths.append(w)
        image_heights.append(h)
        #Get and store camera positions and directions
        p = np.array(yamlLoad["camera_position"])
        d = str(yamlLoad["camera_direction"])
        camera_positions.append(p)
        camera_directions.append(d)

#Check the number of yamls matches the number of images/cameras
numYamls= len(image_widths)
if numYamls is None:
    main_logger.error('No yamls found')
elif numYamls == numCams:
    main_logger.debug(str(numYamls)+' Yamls found')
else:
    main_logger.error('Number of Yamls ('+str(numYamls)+') does not match number of cameras ('+str(numCams+')'))


# Set up BEV info

