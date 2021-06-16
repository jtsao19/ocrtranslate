# Ocrtranslate
A quick little script I wrote up that captures an area of a screen, passes it to the tesseract OCR engine (optical character recognition) to extract text, then uses the Google Translate package to translate.

I wrote this up originally for my own personal use because I was watching a few Korean cooking videos that had korean subtitles but nothing in English. The script is pretty customizable though, and can be tweaked to suit a variety of circumstances. Additionally, with Google Chrome's new Live Caption feature, it's possible to use that to generate transcribed captions from audio that can be translated with this script. 

# Usage
```
 Install the given modules to python
 -numpy
 -matplotlib
 -pytesseract
 -googletrans (alpha version seems to work best googletrans==3.1.0a0)
 -cv2
 
 Install tesseract engine
 -If not installed to the same directory as python script, uncomment this line in main.py "pytesseract.pytesseract.tesseract_cmd = r'<PATH>'" and replace path.
 -For languages besides english, OCR language packs available at https://github.com/tesseract-ocr/tessdata/ 
 
 Run main.py
 -First will be a prompt for the language to be used for OCR based upon the installed language packs
 -Next, there will be a 3 second delay (configurable) to put the window you want focused on top
 -A screenshot will be taken of the monitor, Click and drag from top left to bottom right of the zone that you wish to be translated
 -Press q to stop, ctrl + c works as well to stop the entire script. 
 ```

 
 # To-do
 - Create a GUI to make the whole process more user intuitive
 - Make a function to rebound lower and upper HSV ranges for the mask based on the image displayed. (currently calibrated towards white text on dark backgrounds)
 - Generate an onscreen display to show the translated text instead of having it outputted into python shell.
