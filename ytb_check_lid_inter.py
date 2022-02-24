import numpy as np
import cv2 as cv

# initialize hsv value for lid
hue_min = 1
saturation_min = 1
value_min = 1

hue_max = 255
saturation_max = 255 
value_max = 118

# program check lid
def yesno_lid(image):
    yn_lid= None
    txt_lid = None
    max_cnt = None

    img = image.copy()
    img_cp1 = img.copy()
    img_draw = img.copy()

    # mask for region lid
    img_np = np.zeros(shape = img.shape[:2], dtype= np.uint8)
    img_np[13: 160, 140: 350] = 1
    img_ba = cv.bitwise_and(img_cp1,img_cp1, mask = img_np)

    # check lid
    hsv = cv.cvtColor(img_ba, cv.COLOR_BGR2HSV)
    blur = cv.GaussianBlur(hsv,(21,21),5)

    mina = np.array([hue_min, saturation_min, value_min])
    maxa = np.array([hue_max, saturation_max, value_max])
    mask = cv.inRange(hsv, mina, maxa)
    

    kernel1 = np.ones((8,8))
    kernel2 = np.ones((9,9))

    mask_erode = cv.erode(mask, kernel1, iterations = 1)
    mask_dilate = cv.dilate(mask_erode,kernel2, iterations = 1)
    img_bsd = cv.bitwise_and(img, img, mask = mask_dilate)

    
    cnts, hierarchy = cv.findContours(mask_dilate, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    len_cnt = len(cnts)
    
    
    if len_cnt != 0:
        # find the largest contour
        max_cnt = max(cnts, key = cv.contourArea)
        if cv.contourArea(max_cnt) > 500:
            tmps_p = cnts[0]
            tmps_img = cv.minAreaRect(tmps_p)
            box = cv.boxPoints(tmps_img)
            box = np.int0(box)
            cv.drawContours(img_draw, [box], 0,(255, 0, 0), 2)
            yn_lid = 1
            txt_lid = "Lid"
            
        else:
            yn_lid = 0
            txt_lid = "Not Lid"
    else:
        yn_ld = 0
        txt_lid = "Not Lid"
    img_draw = img_draw[4:169, 135: 355]
    return yn_lid, max_cnt, txt_lid, img_draw
