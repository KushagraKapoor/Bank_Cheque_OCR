
import cv2
import pytesseract
import re
from .models import CheckData
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def syndicate_extract(image_path):
    # Load the image using OpenCV
    img = cv2.imread(image_path)
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))  # Adjust kernel size
    dilate0 = cv2.erode(thresh, kernel, iterations=2)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (55,27))  # Adjust kernel size
    dilate = cv2.dilate(dilate0, kernel, iterations=1)
    cv2.imwrite("index_dilate.png", dilate)

    # Find contours
    contours = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    contours = sorted(contours, key=lambda x: cv2.boundingRect(x)[0])
    rois = []
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        if 35 < h < 135 and w > 13:
            roi = img[y:y+h, x:x+w]
            rois.append(roi)

    return rois

def extract_ifsc(imagesy):
    graysy = cv2.cvtColor(imagesy, cv2.COLOR_BGR2GRAY)
    threshsy = cv2.threshold(graysy, 200, 270, cv2.THRESH_BINARY)[1]
    text = pytesseract.image_to_string(threshsy, lang='eng')
    ifsc_pattern = r'[S][Y][N][B]\d{7}|[S][Y][N][B][\d]{6} [\d]{1}'  # Adjust
    ifsc_match = re.search(ifsc_pattern, text)
    if ifsc_match:
        return ifsc_match.group()
    else:
        return None
    

def extract_account_no(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 200, 270, cv2.THRESH_BINARY)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4,4))  # Adjust kernel size
    dilate0 = cv2.dilate(thresh, kernel, iterations=2)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4,4))  # Adjust kernel size
    dilate = cv2.erode(dilate0, kernel, iterations=2)
    text = pytesseract.image_to_string(dilate, lang='ocr')
    account_no= r'[\d]{14}|[\d]{13} [\d]{1}|[$][\d]{13}'
    acc_match = re.search(account_no, text)
    if acc_match:   
        return acc_match.group()
    else:
        return None
    


def micr_account_no(image_path):
    
 img = cv2.imread(image_path)
 height, width, _ = img.shape
 bottom_height = 150
 img_bottom = img[height - bottom_height:height, :]
 img_rgb = cv2.cvtColor(img_bottom, cv2.COLOR_BGR2RGB)
 rea = pytesseract.image_to_string(img_rgb, lang='mcr')
 chkno=rea[1:7]
 micr_code=rea[9:18]


 crp_dets={'Chkno':chkno,'micr_cd':micr_code}
 
 return crp_dets

import cv2
import matplotlib.pyplot as plt
from paddleocr import PaddleOCR, draw_ocr

ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False)  # use_gpu=False for CPU usage


def hand_name(image_path):
    # Perform OCR on the cropped image
     img = cv2.imread(image_path)
     img = img[190:340, 150:1700]
     result = ocr.ocr(img)
     plt.imshow(img)
     txts=[line[1][0] for line in result[0]]
     string1=" ".join(txts)

     return string1
 
def amount(image_path):
    # Perform OCR on the cropped image
     img = cv2.imread(image_path)
     img = img[320:550, 1800:2500]
     result = ocr.ocr(img)
     plt.imshow(img)
     txts=[line[1][0] for line in result[0]]
     string2=" ".join(txts)

     return string2
 
def amount_in_numbers(image_path):
    img = cv2.imread(image_path)
    img = img[300:500, 150:1700]
    result = ocr.ocr(img)
    plt.imshow(img)
    txts=[line[1][0] for line in result[0]]
    string3=" ".join(txts)

    return string3