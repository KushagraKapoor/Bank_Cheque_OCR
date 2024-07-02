import cv2
import pytesseract
import re
from .models import CheckData
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
from paddleocr import PaddleOCR, draw_ocr
ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False)  # use_gpu=False for CPU usage

def extract_ifsc_ax(image_path):
    imageas = cv2.imread(image_path)
    roi_start_y, roi_start_x = 0, 0
    roi_height, roi_width = 350, 700
    imageas = imageas[roi_start_y:roi_start_y + roi_height, roi_start_x:roi_start_x + roi_width]
    text = pytesseract.image_to_string(imageas, lang='eng')
    text = text.replace("O", "0") 
    ifsc_pattern = r'[U][T][Ili][B][O0]\d{6}\b|[U][T][I][B][\d]{6} [\d]{1}'  # Adjust
    ifsc_match = re.search(ifsc_pattern, text)
    if ifsc_match:
        return ifsc_match.group()
    else:
        return None
    
def extract_account_no_ax(image):
    image_path=image
    image1 = cv2.imread(image_path)
    image1=image1[510:620,300:850]
    text = pytesseract.image_to_string(image1, lang='eng')
    account_no= r'[\d]{15}'
    acc_match = re.search(account_no, text)
    if acc_match:   
        return acc_match.group(0)
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

def amount_in_numbers_a(image_path):
    img = cv2.imread(image_path)
    img = img[297:450, 350:2200]
    result = ocr.ocr(img)
    plt.imshow(img)
    txts=[line[1][0] for line in result[0]]
    string3=" ".join(txts)

    return string3