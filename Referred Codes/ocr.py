import cv2
import numpy as np
import pytesseract
from PIL import Image

# Path of working folder on Disk
#src_path = "E:/Lab/Python/Project/OCR/"
src_path = "."


def get_string(img_path):
    # Read image with opencv
    img = cv2.imread(img_path)
    cv2.imshow('org', img)

    # Convert to gray
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow('gray', img)
    
    # Apply thresholding
    th, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    cv2.imshow('thresh', img)
    
    # Apple median blur to denoise
#    img = cv2.medianBlur(img, 3)
#    cv2.imshow('median', img)

    # Apply dilation and erosion to remove some noise
#    kernel = np.ones((1, 1), np.uint8)
#    img = cv2.dilate(img, kernel, iterations=1)
#    cv2.imshow('dilated', img)
#    img = cv2.erode(img, kernel, iterations=1)
#    cv2.imshow('eroded', img)

    # Write image after removed noise
    cv2.imwrite(src_path + "removed_noise.png", img)

    #  Apply threshold to get image with only black and white
    #img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

    # Write the image after apply opencv to do some ...
    cv2.imwrite(src_path + "thres.png", img)

    # Recognize text with tesseract for python
    result = pytesseract.image_to_string(Image.open(src_path + "thres.png"))

    # Remove template file
    #os.remove(temp)

    return result


print ('--- Start recognize text from image ---')
print (get_string("6.png"))

print ("------ Done -------")