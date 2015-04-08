import pygame, sys,os
from pygame.locals import *
import math
import random, os.path

def findAngle(firstx, firsty, secondx, secondy):
    if firstx<secondx and firsty>secondy:
        angle = -1*(math.atan((1.0*(firsty-secondy))/(1.0*(firstx-secondx))))*(180.0/math.pi)
    elif firstx>secondx and firsty>secondy:
        angle = -1*(math.atan((1.0*(firsty-secondy))/(1.0*(firstx-secondx))))*(180.0/math.pi)+180
    elif firstx>secondx and firsty<secondy:
        angle = -1*(math.atan((1.0*(firsty-secondy))/(1.0*(firstx-secondx))))*(180.0/math.pi)-180
    elif firstx<secondx and firsty<secondy:
        angle = -1*(math.atan((1.0*(firsty-secondy))/(1.0*(firstx-secondx))))*(180.0/math.pi)
    elif firstx==secondx and firsty==secondy:
        angle = 0
    elif firstx==secondx and firsty>secondy:
        angle = 90
    elif firstx==secondx and firsty<secondy:
        angle = -90
    elif firstx>secondx and firsty==secondy:
        angle = 360
    elif firstx<secondx and firsty==secondy:
        angle = 180
    return angle
