import cv2
import pytesseract
import re
from .models import CheckData
from paddleocr import PaddleOCR, draw_ocr
ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False)  # use_gpu=False for CPU usage
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
import matplotlib.pyplot as plt



def extract_ifsc_ca(image_path):
    image = cv2.imread(image_path)
    image=image[0:350,0:2357]
    text = pytesseract.image_to_string(image, lang='eng')
    ifsc_pattern = r'[C][N][R][B]{7}|[C][N][R][B][\d]{6} [\d]{1}|[C][N][\d][B][\d]{7}|[C][N][R][B][\d]{7}'  # Adjust
    ifsc_match = re.search(ifsc_pattern, text)
    if ifsc_match:
        return ifsc_match.group()
    else:
        return None

def extract_account_no_ca(image):
    imageca = cv2.imread(image)
    image=imageca[300:900,300:1600]
    text = pytesseract.image_to_string(imageca, lang='eng')
    account_no= r'[\d]{13}|[\d]{12} [\d]{1}|[$][\d]{12}'
    print(text)
    acc_match = re.search(account_no, text)
    if acc_match:   
        print(text)
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
 micr_code=rea[10:18]


 crp_dets={'Chkno':chkno,'micr_cd':micr_code}
 
 return crp_dets

import cv2
import matplotlib.pyplot as plt
from paddleocr import PaddleOCR

# Initialize OCR model
ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False)

def binarize_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 125, 250, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binary

def hand_name_ca(image_path):
    img = cv2.imread(image_path)
    img = img[190:340, 150:1700]
    binary_img = binarize_image(img)
    result = ocr.ocr(binary_img)
    plt.imshow(binary_img, cmap='gray')
    txts = [line[1][0] for line in result[0]]
    string1 = " ".join(txts)
    return string1

def amount_ca(image_path):
    img = cv2.imread(image_path)
    img = img[320:550, 1800:2500]
    binary_img = binarize_image(img)
    result = ocr.ocr(binary_img)
    plt.imshow(binary_img, cmap='gray')
    txts = [line[1][0] for line in result[0]]
    string2 = " ".join(txts)
    return string2

def amount_in_numbers_ca(image_path):
    img = cv2.imread(image_path)
    img = img[300:500, 150:1700]
    binary_img = binarize_image(img)
    result = ocr.ocr(binary_img)
    plt.imshow(binary_img, cmap='gray')
    txts = [line[1][0] for line in result[0]]
    string3 = " ".join(txts)
    return string3

