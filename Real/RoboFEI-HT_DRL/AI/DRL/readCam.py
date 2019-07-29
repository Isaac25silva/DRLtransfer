# -*- coding: UTF8 -*-

import cv2
import numpy as np
import time
import ctypes
import os
import argparse
from camvideostream import WebcamVideoStream
from servo import Servo


testlib = ctypes.CDLL('/home/fei/RoboFEI-HT_DRL/AI/DRL/examples/blackboard/blackboard.so') #chama a lybrary que contem as funções em c++
testlib.using_shared_memory()   #usando a função do c++
testlib.leitura_int.restype = ctypes.POINTER(ctypes.c_int) #define o tipo de retorno da função, neste caso a função retorna ponteiro int

im_width  = 400  #320 160
im_height = 250  #180 100

image_pointer = testlib.leitura_int()

cap = WebcamVideoStream(src=0).start() #Abrindo camera
#cap = cv2.VideoCapture(0) #Abrindo camera
#cap.set(3,320) #160 720 1280 1920
#cap.set(4,180) #120 480 720 1080
os.system("v4l2-ctl -d /dev/video0 -c focus_auto=0 && v4l2-ctl -d /dev/video0 -c focus_absolute=0")
os.system("v4l2-ctl -d /dev/video0 -c saturation=200")


#try:
#    os.system("v4l2-ctl -d /dev/video0 -c focus_auto=0 && v4l2-ctl -d /dev/video0 -c focus_absolute=0")
#    os.system("v4l2-ctl -d /dev/video0 -c saturation=200")
#except:
#    pass


parser = argparse.ArgumentParser(description='Robot Vision', epilog= 'Responsavel por escrever as imagens no blackboard')
parser.add_argument('--visionball', '--vb', action="store_true", help = 'visualiza imagem da camera')
parser.add_argument('--withoutservo', '--ws', action="store_true", help = 'Servos desligado')

args = parser.parse_args()


if args.withoutservo == False:
    Servo(512, 702-30)

frame = cap.read()
frame = frame[180:-50,120:-120]
im_height, im_width, channels = frame.shape

while(1):


#    ret, frame = cap.read()
    frame = cap.read()
    if args.visionball:
        cv2.imshow('frame',frame)
    frame = frame[180:-50,120:-120]  #[65:-15,80:-80]
#    cv2.imshow('frame',frame)
#    resized_image = cv2.resize(frame, (im_width, im_height))
    if args.visionball:
        cv2.imshow('resized_image',frame)

    resized_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    image_slice = resized_image.ravel()
    image_p = np.concatenate([[im_width, im_height], image_slice])
    count = 0
    for pix in image_p:
        image_pointer[count] = pix;
        count+=1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break




