#!/usr/bin/env python3
# Code to get BEV transformation matrix of 360 cameras.
import sys
import numpy as np 
import logging

class_logger =logging.getLogger('BEV.bev_calibration')


#Load calibrated BEV calibration image (image with checkboard positioned in space as descirbed in README)
#Load intrinsic camera parameters
#Detected checkerboard

#Generate world points

#Get pitch yaw roll yaw

class BEV_camera:
    def __init__(self,camMat,sensPos,calImage,sensDir):
        self.camMat = camMat
        self.sensPos = sensPos
        self.calImage = calImage
        self.sensDir = sensDir
        class_logger.debug('BEV_Camera object initialised')

    """ def detectCheckerboard(self):
        #Function to detect the checkboard in image and get worldpoints
        self.calImage

    def getExtrinsicParams(self):

    

    def getBEVTransform(self, distFront, distSides):
    

    def transformImage(self):
 """
