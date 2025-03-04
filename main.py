import cv2
import numpy as np
#from matplotlib import pyplot as plt
import pyautogui
import time
from scipy import misc
def hunt(path="exit.png", scale=False, floor=.3):
    #Will only find first and x's then y's down
    img_rgb = pyautogui.screenshot()
    img_rgb = np.asarray(img_rgb)
    if scale == False:
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)# Screenshot in Grayscale
        template = cv2.imread(path,0)#Read template in grayscale
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= np.amax(res))
        if len(loc[0]) == 0 or np.amax(res) < floor:
            return None
        for pt in zip(*loc[::-1]):
            newx = pt[0] + (w/2)
            newy = pt[1] + (h/2)
            break
        return(newx, newy)
    if scale == True:
        image = cv2.imread(path, 0)
        img_1= [image[:, :image.shape[1]//2]]
        img_2 = [image[:, image.shape[1]//2:]]
        shape1, shape2 = (img_1[0].shape[0], img_1[0].shape[1])
        shape1_count, shape2_count = (0, 0)
        minsize = 15
        while shape1//2 >= minsize or shape2//2 >= minsize:
            if shape1//2 >= minsize:
                shape1 = shape1//2
                shape1_count +=1
            if shape2//2 >= minsize:
                shape2 = shape2//2
                shape2_count +=1
        minemum = min(shape1_count, shape2_count)
        for x in range(minemum):
            img_1.append(cv2.pyrDown(img_1[x]))
            img_2.append(cv2.pyrDown(img_2[x]))
        for x in range(minemum):
            img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
            res = cv2.matchTemplate(img_gray,img_1[x],cv2.TM_CCOEFF_NORMED)
            res_2 = cv2.matchTemplate(img_gray,img_2[x],cv2.TM_CCOEFF_NORMED)
            loc = np.where(res >= np.amax(res))
            loc2 = np.where(res_2 >= np.amax(res_2))
            if np.amax(res) < floor:#If maximum found does not meet minimum threshold
                break
            if len(loc[0]) == 0 and x == minemum and x >= 1:#If iterated with no findings
                return None
            w, h = image.shape[::-1]#Need to find if both shapes are next to eachother
            for pt1 in zip(*loc[::-1]):#iterate backwards through valid matches
                for pt2 in zip(*loc2[::-1]):#iterate backwards through valid matches
                    #newx = pt[0] + (w/2)
                    print(pt2)
                    print(pt1)
                    #newy = pt[1] + (h/2)
                    if pt1[0] == (pt2[0]+(w)):
                        print("S")
                    #break
            #return(newx, newy)
#Functions find&click
def click(newx, newy):
    win32api.SetCursorPos((newx,newy))
    ctypes.windll.user32.mouse_event(2, 0, 0, 0,0)
    ctypes.windll.user32.mouse_event(4, 0, 0, 0,0)
def move(newx, newy):
    win32api.SetCursorPos((newx,newy))
def back(newx, newy):
    prevx, prevy = win32api.GetCursorPos()
    win32api.SetCursorPos((newx,newy))
    ctypes.windll.user32.mouse_event(2, 0, 0, 0,0)
    ctypes.windll.user32.mouse_event(4, 0, 0, 0,0)
    win32api.SetCursorPos((prevx,prevy))
def move_back(newx, newy, delay=0):
    prevx, prevy = win32api.GetCursorPos()
    win32api.SetCursorPos((newx,newy))
    if delay != 0:
        time.sleep(delay)
    win32api.SetCursorPos((prevx,prevy))
#move(*hunt(path="exit.PNG", floor=.2, scale=True))
#auto scale

