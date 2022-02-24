import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from math import atan2, cos, sin, sqrt, pi

def drawAxis(img, p_, q_, color, scale):
  p = list(p_)
  q = list(q_)
 
  # angle in radians
  angle = atan2(p[1] - q[1], p[0] - q[0]) 
  hypotenuse = sqrt((p[1] - q[1]) * (p[1] - q[1]) + (p[0] - q[0]) * (p[0] - q[0]))
 
  # Here we lengthen the arrow by a factor of scale
  q[0] = p[0] - scale * hypotenuse * cos(angle)
  q[1] = p[1] - scale * hypotenuse * sin(angle)
  cv.line(img, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), color, 3, cv.LINE_AA)
 
  # create the arrow hooks
  p[0] = q[0] + 9 * cos(angle + pi / 4)
  p[1] = q[1] + 9 * sin(angle + pi / 4)
  cv.line(img, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), color, 3, cv.LINE_AA)
 
  p[0] = q[0] + 9 * cos(angle - pi / 4)
  p[1] = q[1] + 9 * sin(angle - pi / 4)
  cv.line(img, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), color, 3, cv.LINE_AA)
  
 
def getOrientation(pts, img):
  
  # Construct a buffer used by the pca analysis
  sz = len(pts)
  data_pts = np.empty((sz, 2), dtype=np.float64)
  for i in range(data_pts.shape[0]):
    data_pts[i,0] = pts[i,0,0]
    data_pts[i,1] = pts[i,0,1]
 
  # Perform PCA analysis
  mean = np.empty((0))
  mean, eigenvectors, eigenvalues = cv.PCACompute2(data_pts, mean)
 
  # Store the center of the object
  cntr = (int(mean[0,0]), int(mean[0,1]))
  
  # Draw the principal components
  cv.circle(img, cntr, 3, (255, 0, 255), 2)
  p1 = (cntr[0] + 0.02 * eigenvectors[0,0] * eigenvalues[0,0], cntr[1] + 0.02 * eigenvectors[0,1] * eigenvalues[0,0])
  p2 = (cntr[0] - 0.02 * eigenvectors[1,0] * eigenvalues[1,0], cntr[1] - 0.02 * eigenvectors[1,1] * eigenvalues[1,0])
  
  drawAxis(img, cntr, p1, (255, 255, 0), 1.5)
  drawAxis(img, cntr, p2, (0, 0, 255), 1.5)
  cv.line(img, cntr, (cntr[0]+200, cntr[1]), (255,0,0), 2, cv.LINE_AA)

  # orientation in radians
  angle_radian = atan2(eigenvectors[0,1], eigenvectors[0,0]) 
 
  # Label with the rotation angle
  angle_rotation = -int(np.rad2deg(angle_radian)) 
  label = str(angle_rotation )


  textbox = cv.rectangle(img, (cntr[0]+20, cntr[1]-55), (cntr[0] + 70, cntr[1] -20), (255,255,255), -1)
  cv.putText(img, label, (cntr[0]+20, cntr[1]- 30), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv.LINE_AA)
 
  return angle_radian, angle_rotation, cntr


red_i = 0
green_i = 0
blue_i = 242

red_a = 255
green_a = 30
blue_a = 255

h_i = 0
s_i = 0
v_i = 0

h_a = 203
s_a = 224
v_a = 250

def lab_che(image):
    yn_label =     None
    shape_label =    None
    value_shape_label = None
    rate_label =     None
    value_rate_label =  None
    angle_label =     None
    value_angle_label =  None
    color_label =     None
    img_color_label = None
    center_points = None
    txt_label = None
    txt_angle_label = None
    txt_color_label = "UnKnow"


    img = image.copy()
    img_cp1 = img.copy()

    # "take label image"
    img_cp3 = img.copy()
    img_cp4 = img.copy()
    img_cp5 = img.copy()
    mask_dilate = np.zeros(shape =[30,30] , dtype= np.uint8)

    img_np = np.zeros(shape = img.shape[:2], dtype= np.uint8)
    img_np[195:360, 140:360] = 1
    img_ba = cv.bitwise_and(img_cp1,img_cp1, mask = img_np)

    # "check yes or no label"
    img_hsv = cv.cvtColor(img_ba, cv.COLOR_BGR2HSV)
    img_blur = cv.GaussianBlur(img_hsv, (21, 21), 5)
 
    mina_lb = np.array([h_i, s_i, v_i])
    maxa_lb = np.array([h_a, s_a, v_a])
    mask_in = cv.inRange(img_hsv, mina_lb, maxa_lb)
    mask_not = cv.bitwise_not(mask_in)
 
    kernel1_1 = np.ones((1,1))
    kernel2_1 = np.ones((2,2))
    mask_erode1 = cv.erode(mask_not, kernel1_1, iterations = 1)
    mask_dilate1 = cv.dilate(mask_erode1,kernel2_1, iterations = 1)

    img_gr = mask_dilate1
    ret, thresh = cv.threshold(img_gr, 226, 255, cv.THRESH_BINARY)
    cnts, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)


    if len(cnts) == 0:
        yn_label = 0
        txt_label = "Failed"
    else:
        yn_label = 1
        cnt_max = max(cnts, key = cv.contourArea)
        cnt_area = cv.contourArea(cnt_max)
       
        cv.drawContours(img_cp5, cnt_max, -1, (0,255,0), 3)
        epsilon = 0.1*(cv.arcLength(cnt_max, True))
        vl_shp_lb = len(cv.approxPolyDP(cnt_max, epsilon, True))
        
        if value_shape_label != 4:
            shape_label = 0
            txt_label = "Failed"
        else:
            shape_label = 1

            tmps_p = cnt_max
            tmps_img = cv.minAreaRect(tmps_p)
       
            box = cv.boxPoints(tmps_img)
            box = np.int0(box)

            temp_w_box = abs(box[0][0] - box[0][1])
            temp_h_hox = abs(box[1][0] - box[1][1])
                
            if temp_h_hox > temp_w_box:
                value_rate_label = float(temp_w_box / temp_h_hox)
            else:
                value_rate_label = float(temp_h_hox/ temp_w_box )

            if value_rate_label == 1:
                rate_label = 0
                txt_label = "Failed"
            
            elif cnt_area < 200: 
                rate_label = 0
                txt_label = "Failed"
            else:
                rate_label = 1
                txt_label = "Succeed"

                # angle label
                max_cnt = max(cnts, key = cv.contourArea)
                angle_radian, value_angle_label, center_point = getOrientation(max_cnt, img_cp3)

                if value_angle_label > 10 or value_angle_label < -10:
                    angle_label = 0
                    txt_angle_label = " angle label out of range"

                else:

                    angle_label = 1
                    txt_angle_label = " angle label within range"

                    # color label
                img_color_label = (img_cp4[(center_pt[1] - 15):(center_point[1] + 15), (center_point[0] - 15):(center_point[0] + 15)]).copy()

                img_color_hsv = cv.cvtColor(img_color_label, cv.COLOR_BGR2HSV)
                blur = cv.GaussianBlur(img_color_hsv,(21,21),5)

                mina = np.array([red_i, green_i, blue_i])
                maxa = np.array([red_a, green_a, blue_a])
                mask = cv.inRange(img_color_hsv, mina, maxa)

                kernel1 = np.ones((1,1))
                kernel2 = np.ones((2,2))
                mask_erode = cv.erode(mask, kernel1, iterations = 1)
                mask_dilate = cv.dilate(mask_erode,kernel2, iterations = 1)
                value_mask = mask_dilate[15,15]
                if value_mask != 255:
                    color_label = 0
                    txt_color_label = "Not White"
                else:
                    color_label = 1
                    txt_color_label = "White"
    
    img_cp3 = img_cp3[185:360, 140:360]#[195:360, 140:360]
    img_cp5 = img_cp5[185:360, 140:360]#[195:360, 140:360]
    return yn_label,shape_label,rate_label,angle_label,color_label, value_shape_label,value_rate_label,value_angle_label, txt_label,txt_color_label, img_cp5,img_cp3,mask_dilate





