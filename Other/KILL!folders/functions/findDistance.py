import pygame, sys,os
from pygame.locals import *
import math
import random, os.path

def findDistance(firstx, firsty, secondx, secondy):
    return math.sqrt(math.pow(secondx-firstx,2)+math.pow(secondy-firsty,2))
