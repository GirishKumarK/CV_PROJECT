# OCR ~ MOUSE
# By GIRISH KUMAR KANNAN
# UCF ID : 4196719

# Import Necessary Packages
import numpy as np
import imutils
import cv2
import pytesseract
from PIL import Image
from collections import deque
from googletrans import Translator
import clipboard as cb
import pyautogui as pag

# Initialize WebCam
cam = cv2.VideoCapture(0)

# Declare Global Variavles
global ocr_res
ocr_res = ''
global ocr_trans
ocr_trans = ''
global card_res
card_res = ''

# Initialize Google Translator
gt = Translator()

# Define the Lower and the Upper Boundaries of Colors Selected in HSV Color Space
lower = {'red' : (160, 120, 120), 'green' : (90, 120, 10), 'yellow' : (10, 120, 120)}
upper = {'red' : (180, 200, 200), 'green' : (110, 250, 100), 'yellow' : (30, 200, 200)}
# Define Standard Colors for the Circle Around the Object
colors = {'red' : (90, 60, 160), 'green' : (145, 140, 60), 'yellow' : (60, 130, 160)}

# Mouse Sensitivity
msensx = pag.size()[0] / 640
msensy = pag.size()[1] / 480

# Start Looping Infinitely
while (True):
    # Capture frame-by-frame
    ret, frame = cam.read()
    
    # Draw a Rectangles
    # Rectangle for OCR
    cv2.rectangle(frame, (160, 20), (480, 120), (255, 0, 0), 2)
    cv2.putText(frame, 'OCR : ', (160, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    # Rectangle for Credit Card OCR
    cv2.rectangle(frame, (5, 400), (380, 455), (255, 0, 0), 2)
    cv2.putText(frame, 'Card : ', (5, 395), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    
    # Operations for OCR Read
    if cv2.waitKey(1) & 0xFF == ord('o'):
        
        # If 'o' is Pressed, Capture the OCR Image from Frame
        ocr_img = frame[20:120, 160:480]
        
        # Convert from BGR to RGB
        ocr_img = cv2.cvtColor(ocr_img, cv2.COLOR_BGR2RGB)
        ocr1 = Image.fromarray(ocr_img)
        
        # Convert from RGB to GRAY
        ocr_img = cv2.cvtColor(ocr_img, cv2.COLOR_RGB2GRAY)
        ocr2 = Image.fromarray(ocr_img)
        
        # Obtain the Threshold for the GRAY Image
        ocr_thr, ocr_img = cv2.threshold(ocr_img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        ocr3 = Image.fromarray(ocr_img)
        
        # Rotate the Image to DeSkew It
        coords = np.column_stack(np.where(ocr_img > 0))
        angle = cv2.minAreaRect(coords)[-1]
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
        (h, w) = ocr_img.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        ocr_img = cv2.warpAffine(ocr_img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        ocr4 = Image.fromarray(ocr_img)
        
        # Remove Noises
        kernel = np.ones((1, 1), np.uint8)
        # Dilating the Image
        ocr_img = cv2.dilate(ocr_img, kernel, iterations=1)
        ocr5 = Image.fromarray(ocr_img)
        # Eroding the Image
        ocr_img = cv2.erode(ocr_img, kernel, iterations=1)
        ocr6 = Image.fromarray(ocr_img)
        
        # Obtain the OCR Text
        ocr_res = pytesseract.image_to_string(Image.fromarray(ocr_img)).lower()
    
    # Print The OCR Result
    cv2.putText(frame, ocr_res, (210, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    # Operations for OCR Translate
    if cv2.waitKey(1) & 0xFF == ord('t'):
        # If 't' is Pressed Translate the OCR Result to Translation Language
        ocr_trans = gt.translate(ocr_res, dest='tr', src='en').text
    # Print the Translated Text
    cv2.putText(frame, 'Translated Text : ' + ocr_trans, (160, 135), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    
    # Operations for Credit Card OCR
    if cv2.waitKey(1) & 0xFF == ord('r'):
        # If 'r' is Pressed, Capture the Card OCR Image from Frame
        card_img = frame[400:455, 5:380]
        
        # Convert from BGR to RGB
        card_img = cv2.cvtColor(card_img, cv2.COLOR_BGR2RGB)
        card1 = Image.fromarray(card_img)
        
        # Convert from BGR to GRAY
        card_img = cv2.cvtColor(card_img, cv2.COLOR_RGB2GRAY)
        card2 = Image.fromarray(card_img)
        
        # Invert the Grayscale Image
        card_img = cv2.bitwise_not(card_img)
        card3 = Image.fromarray(card_img)
        
        # Threshold the Images for Blacks
        card_img[card_img > 31] = 255
        card4 = Image.fromarray(card_img)
        
        # Perform Histogram Equalization
        card_img = cv2.equalizeHist(card_img)
        card5 = Image.fromarray(card_img)
        
        # Remove Noises
        kernel = np.ones((2, 2), np.uint8)
        # Dilating the Image
        card_img = cv2.dilate(card_img, kernel, iterations=1)
        card6 = Image.fromarray(card_img)
        # Eroding the Image
        card_img = cv2.erode(card_img, kernel, iterations=2)
        card7 = Image.fromarray(card_img)
        
        # Rotate the Image to DeSkew It
        coords = np.column_stack(np.where(card_img > 0))
        angle = cv2.minAreaRect(coords)[-1]
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
        (h, w) = card_img.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        card_img = cv2.warpAffine(card_img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        card8 = Image.fromarray(card_img)
        
        # Obtain the OCR Text
        card_res = pytesseract.image_to_string(Image.fromarray(card_img)).lower()
    
    # Print The OCR Result
    cv2.putText(frame, card_res, (60, 395), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    
    # Operations for Card OCR Number Copy to Clipboard
    if cv2.waitKey(1) & 0xFF == ord('c'):
        # If 'c' is Pressed, Copy the Card OCR Result to Clipboard
        cb.copy(card_res)
        cv2.putText(frame, 'Copied To Clipboard !', (5, 472), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    
    # Operations for Mouse Functions based on Color Tracked
    # Blur the Image
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    # Transform Image to HSV Color Space
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    
    # For Each Color in the Dictionary Check the Object in Frame
    for key, value in upper.items():
        # Contruct a Mask for the Color from The Dictionary and Perform
        # A Series of Dilations and Erosions to Remove Any Small
        # Blobs Left in the Mask
        kernel = np.ones((9,9),np.uint8)
        mask = cv2.inRange(hsv, lower[key], upper[key])
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        
        # Find Contours in the Mask and Initialize the Current Center
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        
        # Only Proceeed If At Least One Center is Found
        if len(cnts) > 0:
            # Find the Largest Contour in the Mask, then Use
            # It to Compute the Minimum Enclosing Circle and Centroid
            # print('len cnts : ' + str(len(cnts)))
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            # print(str(key) + str(center))
            
            # Only Proceed If the Radius Meets A Minimum Size. Correct this Value for the Application
            if radius > 1.0:
                # Draw the Circle and Centroid on the Frame
                # Then Update The List of Tracked Points
                cv2.circle(frame, (int(x), int(y)), int(radius), colors[key], 2)
                cv2.putText(frame, key, (int(x-radius), int(y-radius)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, colors[key], 2)
            
            # Get the New Position of Cursor w.r.t. Centers
            mposx = msensx * center[0]
            mposy = msensy * center[1]
            
            # If Green is Tracked - Move Move with Green
            if key == 'green':
                pag.moveTo(mposx,mposy)
            
            # If Red is Tracked - Perform a CLick
            if key ==  'red':
                pag.click()
            
            # If Yellow is Tracked - Perform a Right CLick
            if key == 'yellow':
                pag.click(button='right')

                
                
    # Display The Resulting Grabbed Frame
    cv2.imshow('Capture', frame)
    # Quit if 'q' is Pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When Everything is Complete Release the Capture
cam.release()
# Destory All Open Windows
cv2.destroyAllWindows()

# End of File