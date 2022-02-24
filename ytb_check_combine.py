# import the necessary packages
from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2
import numpy as np

# my library 
import ytb_det_obj_move_inter as doj
import ytb_check_lid_inter as lid_check
import ytb_check_label_inter as lab_check


# active raspberry pins
import RPi.GPIO as GPIO
from time import sleep

# active camera raspberry
from picamera.array import PiRGBArray
from picamera import PiCamera

camera = PiCamera()
camera.resolution = (640,480)
camera.framerate = 27
rawCapture = PiRGBArray(camera, size=(640,480))

# config pin raspberry
GPIO.setwarnings(False)
GPIO.setmode (GPIO.BCM)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(18, GPIO.OUT)

GPIO.output(5, False)
GPIO.output(18, False)


# initialize parameter
press = False
status_press = False
stat_pr = False
g_pitong = None
g_regiter = []

# gui parameter
result_check = None
total_pr = 0
good_pr = 0
failed_pr = 0

# signal for take image
pr_cx = 0
sign_tk = 0

#lid
yn_ld = None
max_cnt = None
txt_yn_ld = None

#label
yn_lb = None
shp_lb = None
rt_lb = None
ag_lb = None
cl_lb = None
vl_shp_lb = None
vl_rt_lb = None
vl_ag_lb = None
txt_lb = None
txt_cl_lb = None

frst_F = None
img_mj = np.zeros(shape = [350, 470], dtype= np.uint8)
img_ld = np.zeros(shape = [165, 220], dtype= np.uint8)
img_lb = np.zeros(shape = [165, 220], dtype= np.uint8)
img_ag = np.zeros(shape = [165, 220], dtype= np.uint8)
img_cl =  np.zeros(shape = [30, 30], dtype= np.uint8)

def doc_lb():
    
    global g_pitong
    global g_regiter
    
    # gui parameter
    global result_check
    global total_pr
    global good_pr
    global failed_pr

    # signal for take image
    global pr_cx 
    global sign_tk

    #lid
    global yn_ld 
    global max_cnt 
    global txt_yn_ld 

    #label
    global yn_lb 
    global shp_lb 
    global rt_lb 
    global ag_lb 
    global cl_lb 
    global vl_shp_lb 
    global vl_rt_lb 
    global vl_ag_lb 
    global txt_lb 
    global txt_cl_lb 

    # initialize the first frame in the video stream
    global frst_F 
    global img_mj 
    global img_ld 
    global img_lb 
    global img_ag 
    global img_cl 

    # loop over the frames of the video
    for image in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        
        img = image.array
        
        if img is None:
            break
    
        if len(g_regiter) == 0:
            g_regiter.append("Wellcome")


        # resize the frame
        img_cp1 = img.copy()
        img_cp2 = img_cp1[20:360,130:500,:].copy()
        img_take = img_cp1[20:370,80:550,:].copy() 
    

         # if the first frame is None, initialize it
        if frst_F is None:
            frst_F = img_cp2.copy()
            pass
        else:
            cr_oj, mm_oj = doj.dom(img_cp2, frst_F)
            
            if mm_oj is not None:
                cx_oj, cy_oj = mm_oj

                if cx_oj < int(img_cp2.shape[1]/2):
                    pr_cx = 1
                elif cx_oj >= int(img_cp2.shape[1]/2) and pr_cx == 1:
                    img_mj = img_take.copy()
                    print("done")
                    pr_cx = 0
                    sign_tk = 1
                    total_pr += 1
            
            if sign_tk == 1:
                # check lid
                yn_ld, max_cnt, txt_yn_ld, img_ld = lid_check.yesno_lid(img_mj)
                # check label
                yn_lb,shp_lb,rt_lb,ag_lb,cl_lb, vl_shp_lb,vl_rt_lb,vl_ag_lb, txt_lb,txt_cl_lb, img_lb,img_ag,img_cl = lab_check.lab_che(img_mj)
                sign_tk = 0
               
                if yn_ld==0 or yn_lb==0 or shp_lb==0 or rt_lb==0 or ag_lb==0 or cl_lb==0:
                    error_pd = 1
                    result_check = "FAILED"
                    failed_pr += 1
                else:
                    error_pd = 0
                    result_check = "SUCCEED"
                    good_pr +=1
            
                if g_regiter[0] == "Wellcome":
                    g_regiter.pop(0)
            
                g_regiter.append(error_pd)        

                print(g_regiter)
        signal_4 = GPIO.input(8) #signal_4 sensor_1 ON/OFF
        if signal_4 == 0 and g_regiter[0] == 1:
            g_pitong = 1 
            GPIO.output(5, g_pitong)

        if g_pitong == 1 and signal_4 == 1:
            g_pitong = 0
            GPIO.output(5, g_pitong)
            g_regiter.pop(0)
            print(g_regiter)
        elif  g_regiter[0] == 0 and signal_4 ==0 :
            g_regiter.pop(0)
            print(g_regiter)
        
        return (txt_yn_ld,txt_lb,vl_ag_lb,txt_cl_lb, img_mj,img_ld,img_lb,img_ag,img_cl, result_check,total_pr,good_pr,failed_pr, rawCapture.truncate(0))
