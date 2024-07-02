
import cv2
import pytesseract
import re
from .models import CheckData
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
from paddleocr import PaddleOCR, draw_ocr
ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False)  # use_gpu=False for CPU usage
import matplotlib.pyplot as plt


def extract_ifsc_ic(image_path):
    image = cv2.imread(image_path)
    roi_start_y, roi_start_x = 0, 0
    roi_height, roi_width = 350, 650
    img_micr = image[roi_start_y:roi_start_y + roi_height, roi_start_x:roi_start_x + roi_width]
    img_micr_rgb = cv2.cvtColor(img_micr, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(img_micr_rgb, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray, lang='eng')
    ifsc_pattern = r'\b[\d][C][I][C][\d]{7}|[\d][C][\d][C][\d]{6} [\d]{1}|[I][C][\d][I][\d]{7}|[I][C][I][C][\d]{7}\b'  # Adjust
    ifsc_match = re.search(ifsc_pattern, text)
    if ifsc_match:
        return ifsc_match.group()
    else:
        return None


def extract_account_no_ic(image):
    image = cv2.imread(image)
    image=image[300:900,200:1100]
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray, lang='eng')
    account_no= r'[\d]{12}|[\d]{11} [\d]{1}|[$][\d]{11}'
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

def binarize_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 125, 250, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binary

def hand_name_ic(image_path):
    img = cv2.imread(image_path)
    img = img[190:340, 150:1700]
    binary_img = binarize_image(img)
    result = ocr.ocr(binary_img)
    plt.imshow(binary_img, cmap='gray')
    txts = [line[1][0] for line in result[0]]
    string1 = " ".join(txts)
    return string1

def amount_ic(image_path):
    img = cv2.imread(image_path)
    img = img[320:550, 1800:2500]
    binary_img = binarize_image(img)
    result = ocr.ocr(binary_img)
    plt.imshow(binary_img, cmap='gray')
    txts = [line[1][0] for line in result[0]]
    string2 = " ".join(txts)
    return string2

def amount_in_numbers_ic(image_path):
    img = cv2.imread(image_path)
    img = img[300:500, 150:1700]
    binary_img = binarize_image(img)
    result = ocr.ocr(binary_img)
    plt.imshow(binary_img, cmap='gray')
    txts = [line[1][0] for line in result[0]]
    string3 = " ".join(txts)
    return string3
