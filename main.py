import os
import numpy as np
import cv2 as cv
import time
import pyautogui
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets
from mss import mss
import pytesseract
import selectArea
from googletrans import Translator # install alpha pip install googletrans==3.1.0a0

###Config###
#install tesseract binary from https://github.com/UB-Mannheim/tesseract/wiki
#Language packs available at https://github.com/tesseract-ocr/tessdata/, put in tessdata folder

# configurable wait time between screenshots. 1 second delay means it checks every second to see if there are new subtitles or not
#Since video subtitles are rather static, a high delay/low fps doesn't affect result as much and can reduces proccessing
DELAY = 1.0
OUTPUTLANG = 'zh-cn'

# configurable path to tesseract binary if not installed in same folder
# uncomment next line and replace path if using
### pytesseract.pytesseract.tesseract_cmd = r'<PATH>'


### /// ###


screenshot = mss()
translator = Translator(service_urls=['translate.googleapis.com'])

    
def image(zone,monitor):
    if not zone:
        # Screenshot then preprocess
        capture = np.array(screenshot.grab(screenshot.monitors[1]))
        capture = capture[:, :, :3]   # Remove alpha
        capture = capture[:, :, ::-1] # Reverse BGR <-> RGB
        return capture
    else:
        capture = np.array((screenshot.grab(monitor)))
        capture = capture[:, :, :3]   # Remove alpha
        capture = capture[:, :, ::-1] # Reverse BGR <-> RGB
        return capture
    

#print out available language packs installed with tesseract
print(pytesseract.get_languages(config=''))
print("Enter language of subtitles: ")
lang = input()



print("Bring video to forefront and draw selection area over the screenshot")

#3 sec delay timer so video can be brought to front
time.sleep(3)

#initializing monitor coords
monitor = []
#calling image function to ss and preprocess
img = image(0,monitor)
#creating array for storing coordinates
coords = []
    
#        
coords.append(selectArea.select(img))
    
# Get the rs parameters
coords = np.array(coords, dtype=int)

coords = [list(x) for x in coords]
###debug coord statement
print(coords)

top = coords[0][2]
left = coords[0][0]
height = coords[0][3]
width = coords[0][1]

#converting from np int to native python int
top = top.tolist()
left = left.tolist()
width = width.tolist()
height = height.tolist()

width = width - left
height = height - top

old = ""

###ss_time = time()
while(True):
    # adds in a delay for hows many screenshots are polled
    time.sleep(DELAY)

    
    #bounds the selected "monitor" range for capture function then passes it along to get ss
    monitor = {"top": top, "left": left, "width": width, "height": height}
    capture = image(1,monitor)

    #Hue Sat Value masking
    hsv = cv.cvtColor(capture,cv.COLOR_BGR2HSV)
    lower = np.array([0,0,218])
    upper = np.array([157,255,255])
    mask = cv.inRange(hsv,lower,upper)

    kernel = cv.getStructuringElement(cv.MORPH_RECT,(5,3))
    dilate = cv.dilate(mask,kernel,iterations=5)

    cnts = cv.findContours(dilate,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        x,y,w,h = cv.boundingRect(c)
        ar = w/float(h)
        if ar<5:
            cv.drawContours(dilate,[c],-1,(0,0,0),-1)

    result = 255- cv.bitwise_and(dilate,mask)
    data = pytesseract.image_to_string(result, lang ='eng',config = '--psm 6')

    # for first loop through, saves the read subtitles value to a seperate variable
    if old == "":
        old = data
        translation = translator.translate(data, dest = OUTPUTLANG)
        print(translation.text)
        pass

    #subsequent loops
    if data == old:
        #if subtitles havent changed, no need to print out the same text again, loop again to check for update
        pass

    elif data != old:
        translation = translator.translate(data, dest = OUTPUTLANG)
        print(translation.text)

    #displays image with extracted text mask 
    cv.imshow('mask', result)

    
    # exit key = q
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done')




